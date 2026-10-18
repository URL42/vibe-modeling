"""Export capped, intermediate scan cuts. No joints, union repair, or print approval.

Uses the installed scale master and established neck plane. Closure is verified
after binary float32 encoding, including the new cap edges. The base intentionally
retains the source's three overlapping closed shells.
"""
import argparse
import json
import struct
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

from measure_scale import ROOT, DESIGN, OUT, DTYPE, read_stl, render, sha
from analyze_splits import clip, area


def indexed(t):
    v, ids = np.unique(t.astype(np.float32).reshape(-1, 3), axis=0, return_inverse=True)
    f = ids.reshape(-1, 3)
    good = (f[:, 0] != f[:, 1]) & (f[:, 1] != f[:, 2]) & (f[:, 2] != f[:, 0])
    return v.astype(float), f[good]


def edge_data(f):
    directed = np.concatenate([f[:, [0, 1]], f[:, [1, 2]], f[:, [2, 0]]])
    edges, ids, counts = np.unique(np.sort(directed, axis=1), axis=0, return_inverse=True, return_counts=True)
    return directed, edges, ids, counts


def triangulate_polygon(points):
    """Ear clipping retains every boundary vertex, including collinear chains."""
    order = list(range(len(points)))
    signed_area = np.sum(points[:, 0] * np.roll(points[:, 1], -1) - points[:, 1] * np.roll(points[:, 0], -1)) / 2
    sign = 1 if signed_area > 0 else -1
    result = []
    while len(order) > 3:
        found = False
        for k in range(len(order)):
            indices = [order[(k - 1) % len(order)], order[k], order[(k + 1) % len(order)]]
            a, b, c = points[indices]
            def cross(x, y):
                return x[..., 0] * y[..., 1] - x[..., 1] * y[..., 0]
            if sign * cross(b - a, c - b) <= 1e-10:
                continue
            others = [i for i in order if i not in indices]
            q = points[others]
            inside = ((sign * cross(b - a, q - a) >= -1e-10) &
                      (sign * cross(c - b, q - b) >= -1e-10) &
                      (sign * cross(a - c, q - c) >= -1e-10))
            if inside.any():
                continue
            result.append(indices)
            order.pop(k)
            found = True
            break
        if not found:
            raise ValueError("Cannot triangulate cap without discarding boundary vertices")
    result.append(order)
    return np.array(result)


def capped_cut(t, normal, offset):
    """Keep normal dot p >= offset; cap exposed loops with outward -normal."""
    clipped = clip(t, normal, offset)
    # The same edge can be evaluated in opposite directions by adjacent faces.
    # Snap only numerically on-plane points before float32 encoding, avoiding
    # distinct +/-1e-15 coordinates at an axis-aligned cut such as X=0.
    signed = clipped @ normal - offset
    on_plane = np.abs(signed) < 1e-7
    clipped[on_plane] -= signed[on_plane, None] * normal / float(normal @ normal)
    vertices, faces = indexed(clipped)
    directed, edges, ids, counts = edge_data(faces)
    boundary = edges[counts == 1]
    if not len(boundary):
        return vertices[faces], {"cap_triangles": 0, "cap_loops": 0}
    if np.any(counts > 2):
        raise ValueError("Nonmanifold clipped surface")
    adjacency = {}
    for a, b in boundary:
        adjacency.setdefault(int(a), []).append(int(b))
        adjacency.setdefault(int(b), []).append(int(a))
    if any(len(neighbors) != 2 for neighbors in adjacency.values()):
        raise ValueError("Cut boundary is not a set of closed simple loops")
    normal = normal / np.linalg.norm(normal)
    u = np.cross(normal, [1., 0, 0])
    if np.linalg.norm(u) < .1:
        u = np.cross(normal, [0., 1, 0])
    u /= np.linalg.norm(u)
    v = np.cross(normal, u)
    remaining = set(adjacency)
    caps = []
    loops = 0
    while remaining:
        first = min(remaining)
        loop = [first]
        previous, current = None, first
        while True:
            choices = adjacency[current]
            nxt = choices[0] if choices[0] != previous else choices[1]
            if nxt == first:
                break
            if nxt in loop:
                raise ValueError("Self-connected cap boundary")
            loop.append(nxt)
            previous, current = current, nxt
        remaining.difference_update(loop)
        coords = vertices[loop]
        planar = np.column_stack([coords @ u, coords @ v])
        tris = np.array(loop)[triangulate_polygon(planar)]
        q = vertices[tris[0]]
        if np.dot(np.cross(q[1] - q[0], q[2] - q[0]), -normal) < 0:
            tris = tris[:, [0, 2, 1]]
        caps.append(tris)
        loops += 1
    cap_faces = np.concatenate(caps)
    final = vertices[np.concatenate([faces, cap_faces])]
    check = mesh_check(final)
    if check["boundary_edges"] or check["nonmanifold_edges"] or check["inconsistent_edge_winding"]:
        raise ValueError(f"Cap topology failed: {check}")
    return final, {"cap_triangles": len(cap_faces), "cap_loops": loops}


def mesh_check(t):
    v, f = indexed(t)
    directed, edges, ids, counts = edge_data(f)
    balance = np.bincount(ids, weights=np.where(directed[:, 0] < directed[:, 1], 1, -1))
    graph = coo_matrix((np.ones(len(edges)), (edges[:, 0], edges[:, 1])), shape=(len(v), len(v)))
    components, _ = connected_components(graph, directed=False)
    t = v[f]
    return {"triangles": len(f), "boundary_edges": int(sum(counts == 1)), "nonmanifold_edges": int(sum(counts > 2)),
            "inconsistent_edge_winding": int(sum((counts == 2) & (balance != 0))), "connected_shells": components,
            "bounds_mm": [v.min(0).tolist(), v.max(0).tolist()], "size_xyz_mm": np.ptp(v, axis=0).tolist(),
            "signed_volume_mm3": float(np.einsum("ij,ij->i", t[:, 0], np.cross(t[:, 1], t[:, 2])).sum() / 6)}


def write_stl(path, t):
    records = np.zeros(len(t), dtype=DTYPE)
    records["v"] = t
    n = np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0])
    n /= np.maximum(np.linalg.norm(n, axis=1)[:, None], 1e-20)
    records["normal"] = n
    path.write_bytes(b"Cicero intermediate reference; no dovetails".ljust(80, b"\0") + struct.pack("<I", len(t)) + records.tobytes())


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--audit-only", action="store_true")
    args = p.parse_args()
    manifest = OUT / "intermediate_exports_manifest.json"
    if args.audit_only:
        m = json.loads(manifest.read_text())
        for name, digest in m["dependencies"].items():
            if sha(ROOT / name) != digest:
                raise ValueError(f"Intermediate dependency changed: {name}")
        for name, digest in m["artifacts"].items():
            if sha(OUT / name) != digest:
                raise ValueError(f"Intermediate artifact changed: {name}")
        print("PASS: intermediate head/base export provenance")
        return
    source = OUT / "scaled_master.stl"
    config = DESIGN / "neck_interface.json"
    cfg = json.loads(config.read_text())
    scale_path = DESIGN / cfg["scale_config"]
    scale_cfg = json.loads(scale_path.read_text())
    scale = cfg["selected_tilt_degrees"]
    angle, yaw = np.radians([scale, cfg["selected_plane_yaw_degrees"]])
    n = np.array([np.sin(angle) * np.sin(yaw), -np.sin(angle) * np.cos(yaw), np.cos(angle)])
    factor = scale_cfg["target_ear_span_mm"] / np.linalg.norm(np.array(scale_cfg["ear_positive_x"]) - scale_cfg["ear_negative_x"])
    origin = (np.array(cfg["source_plane_origin"]) + scale_cfg["source_offset"]) * factor
    offset = float(n @ origin)
    t = read_stl(source)
    print(f"Source: {source}\nNeck plane: {n.tolist()} dot XYZ = {offset}\nOutput: {OUT}", flush=True)
    results = {}
    arrays = []
    for name, sign in [("head_intermediate", 1), ("base_intermediate", -1)]:
        print(f"Clipping/capping {name}", flush=True)
        cut, cap = capped_cut(t, n * sign, offset * sign)
        path = OUT / f"{name}.stl"
        write_stl(path, cut)
        actual = read_stl(path)
        check = mesh_check(actual)
        if any(check[k] for k in ["boundary_edges", "nonmanifold_edges", "inconsistent_edge_winding"]):
            raise ValueError(f"Installed artifact topology failed: {name}")
        results[name] = {**check, **cap, "sha256": sha(path), "scope": "Capped intermediate reference in assembly coordinates; no joints"}
        arrays.append(actual)
        print(f"{name}: {check}", flush=True)
    before = mesh_check(t)
    volume_error = abs(sum(r["signed_volume_mm3"] for r in results.values()) - before["signed_volume_mm3"])
    if volume_error > max(10., abs(before["signed_volume_mm3"]) * 1e-6):
        raise ValueError(f"Cut recombination volume mismatch: {volume_error}")
    fig, axes = plt.subplots(1, 2, figsize=(12, 9))
    for ax, cut, name in zip(axes, arrays, results):
        render(ax, cut, (0, 2), -1, name)
    fig.suptitle("Capped head/base intermediate references in assembly coordinates; no dovetails")
    fig.tight_layout()
    fig.savefig(OUT / "intermediate_head_base.png", dpi=140)
    plt.close(fig)
    report = {"scope": "Intermediate reference pair, not a complete printable manifest", "source": source.relative_to(ROOT).as_posix(),
              "neck_plane": {"normal": n.tolist(), "offset_mm": offset, "angle_degrees": scale}, "artifacts": results,
              "signed_volume_recombination_error_mm3": volume_error,
              "limits": ["Base retains three overlapping source shells; no solid union repair", "No dovetails, subdivision joints, supports, or print approval"]}
    report_path = OUT / "intermediate_exports_report.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    deps = [source, config, scale_path, Path(__file__), DESIGN / "analyze_splits.py", DESIGN / "measure_scale.py"]
    names = ["head_intermediate.stl", "base_intermediate.stl", "intermediate_head_base.png", report_path.name]
    manifest.write_text(json.dumps({"dependencies": {p.relative_to(ROOT).as_posix(): sha(p) for p in deps},
                                    "artifacts": {name: sha(OUT / name) for name in names}}, indent=2) + "\n")


if __name__ == "__main__":
    main()
