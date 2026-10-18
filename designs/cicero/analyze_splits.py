"""Reproducible diagnostic mesh/neck/split study; produces no printable solids.

Requires the same NumPy/SciPy/Matplotlib environment as measure_scale.py.
Clipped triangles remain uncapped diagnostic surfaces. Candidate bounds include
split-plane triple intersections conservatively, so a reported fit never relies
on omitting a possible interior cap corner. No geometric repair is performed.
"""
import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial import ConvexHull, distance
from scipy.spatial.transform import Rotation

from measure_scale import DESIGN, OUT, ROOT, read_stl, render, sha

FILES = ["split_study_preview.png", "split_study_sections.png", "split_study_report.json"]
MANIFEST = OUT / "split_study_manifest.json"


def clip(triangles, normal, offset):
    """Keep n dot p >= offset, preserving winding and exact edge intersections."""
    signed = triangles @ normal - offset
    inside = signed >= 0
    full = triangles[inside.all(1)]
    crossing = triangles[inside.any(1) & ~inside.all(1)]
    added = []
    for tri in crossing:
        polygon = []
        for a, b in zip(tri, np.roll(tri, -1, axis=0)):
            da, db = a @ normal - offset, b @ normal - offset
            if da >= 0:
                polygon.append(a)
            if (da >= 0) != (db >= 0):
                polygon.append(a + (b - a) * (da / (da - db)))
        for j in range(1, len(polygon) - 1):
            added.append([polygon[0], polygon[j], polygon[j + 1]])
    return np.concatenate([full, np.asarray(added).reshape(-1, 3, 3)])


def area(t):
    return float(np.linalg.norm(np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0]), axis=1).sum() / 2)


def section(t, n, offset):
    signed = t @ n - offset
    selected = (signed.min(1) < 0) & (signed.max(1) > 0)
    segments = []
    for tri, d in zip(t[selected], signed[selected]):
        points = []
        for i, j in [(0, 1), (1, 2), (2, 0)]:
            if d[i] * d[j] < 0:
                points.append(tri[i] + (tri[j] - tri[i]) * d[i] / (d[i] - d[j]))
        if len(points) == 2:
            segments.append(points)
    return np.asarray(segments)


def topology(t):
    vertices, inverse = np.unique(t.reshape(-1, 3), axis=0, return_inverse=True)
    faces = inverse.reshape(-1, 3)
    directed = np.concatenate([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]])
    undirected, edge_index, counts = np.unique(np.sort(directed, axis=1), axis=0, return_counts=True, return_inverse=True)
    direction = np.where(directed[:, 0] < directed[:, 1], 1, -1)
    balance = np.bincount(edge_index, weights=direction)
    graph = coo_matrix((np.ones(len(undirected)), (undirected[:, 0], undirected[:, 1])), shape=(len(vertices), len(vertices)))
    number, labels = connected_components(graph, directed=False)
    shells = []
    for i in range(number):
        v = vertices[labels == i]
        tt = t[labels[faces[:, 0]] == i]
        shells.append({"id": i, "triangles": len(tt), "bounds_source": [v.min(0).tolist(), v.max(0).tolist()],
                       "signed_volume_source": float(np.einsum("ij,ij->i", tt[:, 0], np.cross(tt[:, 1], tt[:, 2])).sum() / 6)})
    # A point strictly inside multiple closed shells demonstrates volumetric overlap.
    # Independent ray directions reduce dependence on an accidental edge hit.
    point = np.array([5., 0, 10])
    overlap_tests = []
    for ray in [np.array([1., .371, .217]), np.array([-.313, 1., .239])]:
        e1, e2 = t[:, 1] - t[:, 0], t[:, 2] - t[:, 0]
        h = np.cross(np.broadcast_to(ray, e2.shape), e2)
        determinant = np.einsum("ij,ij->i", e1, h)
        valid = np.abs(determinant) > 1e-10
        reciprocal = np.zeros(len(t))
        reciprocal[valid] = 1 / determinant[valid]
        s = point - t[:, 0]
        u = reciprocal * np.einsum("ij,ij->i", s, h)
        q = np.cross(s, e1)
        v = reciprocal * (q @ ray)
        distance_along_ray = reciprocal * np.einsum("ij,ij->i", e2, q)
        hits = valid & (u >= 0) & (v >= 0) & (u + v <= 1) & (distance_along_ray > 1e-7)
        counts_per_shell = np.bincount(labels[faces[hits, 0]], minlength=number)
        overlap_tests.append({"ray": ray.tolist(), "hits_per_shell": counts_per_shell.tolist(),
                              "inside_shells": np.flatnonzero(counts_per_shell % 2).tolist()})
    return {"triangles": len(t), "vertices": len(vertices), "boundary_edges": int(sum(counts == 1)),
            "nonmanifold_edges": int(sum(counts > 2)), "inconsistent_edge_winding": int(sum((counts == 2) & (balance != 0))),
            "zero_area_triangles": int(sum(np.linalg.norm(np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0]), axis=1) < 1e-12)),
            "connected_shells": shells, "self_intersections": "not tested",
            "shell_overlap": {"point_source": point.tolist(), "ray_tests": overlap_tests,
                              "finding": "Point lies inside multiple shells; input is not a single resolved solid union"},
            "boolean_readiness": "unverified; edge checks alone do not verify a single solid"}


def envelope(t, planes):
    points = t.reshape(-1, 3)
    lo, hi = points.min(0), points.max(0)
    extra = []
    # Plane intersections inside this region might be cap corners not present on
    # the clipped exterior. Retain them conservatively without assuming solid fill.
    for three in itertools.combinations(planes, 3):
        matrix = np.array([p[0] for p in three])
        if abs(np.linalg.det(matrix)) < 1e-9:
            continue
        p = np.linalg.solve(matrix, [p[1] for p in three])
        if np.all(p >= lo - 1e-6) and np.all(p <= hi + 1e-6) and all(p @ n >= d - 1e-6 for n, d in planes):
            extra.append(p)
    if extra:
        points = np.concatenate([points, extra])
    return points[ConvexHull(points).vertices]


def orientation(points, volume, seed, iterations):
    def dims(angles):
        matrix = Rotation.from_euler("xyz", angles, degrees=True).as_matrix()
        return np.ptp(points @ matrix.T, axis=0)
    def objective(angles):
        return float(np.max(dims(angles) / volume))
    result = differential_evolution(objective, [(-180, 180)] * 3, seed=seed, maxiter=iterations, popsize=10, tol=1e-5, polish=True)
    final = dims(result.x)
    return {"rotate_xyz_degrees": result.x.tolist(), "size_xyz_mm": final.tolist(),
            "envelope_ratio": float(np.max(final / volume)), "fits_studied_box": bool(np.all(final <= volume)),
            "method": "deterministic seeded orientation search; not a proof of optimality; bed contact/supports not checked"}


def self_check():
    tri = np.array([[[0., 0, 0], [2, 0, 0], [0, 2, 0]]])
    n = np.array([1., 0, 0])
    a, b = clip(tri, n, .75), clip(tri, -n, -.75)
    assert abs(area(a) + area(b) - area(tri)) < 1e-12
    assert np.all(a[:, :, 0] >= .75 - 1e-12)
    assert np.all(b[:, :, 0] <= .75 + 1e-12)
    seg = section(tri, n, .75)
    assert len(seg) == 1 and np.allclose(seg[:, :, 0], .75)
    r = Rotation.from_euler("z", 90, degrees=True).as_matrix()
    assert np.allclose(np.ptp(tri.reshape(-1, 3) @ r.T, axis=0), [2, 2, 0])
    print("PASS: synthetic clipping partition, section intersections, and rotation checks", flush=True)


def audit():
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for name, digest in m["dependencies"].items():
        if sha(ROOT / name) != digest:
            raise ValueError(f"Study dependency changed: {name}")
    for name, digest in m["artifacts"].items():
        if sha(OUT / name) != digest:
            raise ValueError(f"Study artifact changed: {name}")
    if set(m["artifacts"]) != set(FILES):
        raise ValueError("Study artifact coverage mismatch")
    print("PASS: diagnostic split-study provenance and artifacts", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-only", action="store_true")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return
    if args.audit_only:
        audit()
        return
    self_check()
    cfg_path = DESIGN / "split_study.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    scale_path = DESIGN / cfg["scale_config"]
    scale_cfg = json.loads(scale_path.read_text(encoding="utf-8"))
    source = DESIGN / "assets/cicero_original.stl"
    if sha(source) != scale_cfg["source_sha256"]:
        raise ValueError("Source hash mismatch")
    source_t = read_stl(source)
    print(f"Source: {source}\nStudy: {cfg_path}\nOutput: {OUT}", flush=True)
    mesh = topology(source_t)
    print(f"Mesh: {len(mesh['connected_shells'])} shells; boundary edges {mesh['boundary_edges']}; nonmanifold edges {mesh['nonmanifold_edges']}", flush=True)
    measurement = json.loads((OUT / "scaled_master_measurements.json").read_text(encoding="utf-8"))
    scale = measurement["uniform_scale"]
    offset = np.array(scale_cfg["source_offset"])
    t = read_stl(OUT / "scaled_master.stl")
    normal = np.array(cfg["neck_plane_source"]["normal_unnormalized"], dtype=float)
    source_d = float(normal @ cfg["neck_plane_source"]["origin"])
    d = scale * (source_d + normal @ offset)
    norm = float(np.linalg.norm(normal))
    neck = (normal, d)
    head = clip(t, normal, d)
    base = clip(t, -normal, -d)
    area_error = abs(area(head) + area(base) - area(t))
    if area_error > max(1e-6, area(t) * 1e-10):
        raise ValueError("Head/base exterior surface partition failed")
    volume = np.array(cfg["printer_volume_mm"], dtype=float)
    working = volume - [2 * cfg["study_xy_margin_per_side_mm"], 2 * cfg["study_xy_margin_per_side_mm"], 0]
    candidates = {}
    definitions = [
        ("four_pieces", {"head": [0], "base": [0]}, []),
        ("eight_pieces_vertical_quarters", {"head": [0, 1], "base": [0, 1]}, []),
        ("twelve_pieces_base_height_split", {"head": [0, 1], "base": [0, 1]}, ["base"]),
        ("twelve_pieces_head_halves_height_split", {"head": [0], "base": [0, 1]}, ["base", "head"]),
        ("sixteen_pieces_head_and_base_height_split", {"head": [0, 1], "base": [0, 1]}, ["base", "head"]),
    ]
    cached = {}
    for name, axes, height_split in definitions:
        print(f"Studying {name} with 220 mm nominal cube and {working.tolist()} study envelope", flush=True)
        pieces = []
        partition_area = 0.
        for group, initial, first in [("head", head, neck), ("base", base, (-normal, -d))]:
            subsets = [(initial, [first], group)]
            for axis in axes[group]:
                next_subsets = []
                for tt, planes, label in subsets:
                    for sign, suffix in [(-1, "minus"), (1, "plus")]:
                        n = np.eye(3)[axis] * sign
                        dd = float(cfg[f"vertical_plane_{'xy'[axis]}_mm"]) * sign
                        next_subsets.append((clip(tt, n, dd), planes + [(n, dd)], f"{label}_{'xy'[axis]}_{suffix}"))
                subsets = next_subsets
            if group in height_split:
                next_subsets = []
                for tt, planes, label in subsets:
                    for sign, suffix in [(-1, "lower"), (1, "upper")]:
                        n = np.array([0., 0, sign])
                        dd = cfg[f"{group}_additional_height_mm"] * sign
                        next_subsets.append((clip(tt, n, dd), planes + [(n, dd)], f"{label}_{suffix}"))
                subsets = next_subsets
            for tt, planes, label in subsets:
                if not len(tt):
                    continue
                partition_area += area(tt)
                if label in cached:
                    pieces.append(cached[label])
                    continue
                hull = envelope(tt, planes)
                # Diameter witness from actual exterior vertices, not conservative cap points.
                exterior = tt.reshape(-1, 3)
                actual_hull = exterior[ConvexHull(exterior).vertices]
                pairs = distance.pdist(actual_hull)
                max_index = int(np.argmax(pairs))
                diameter = float(pairs[max_index])
                # Recover pair indices without allocating a square distance matrix.
                count = len(actual_hull)
                start = 0
                for i in range(count - 1):
                    row_len = count - i - 1
                    if max_index < start + row_len:
                        j = i + 1 + max_index - start
                        witness = actual_hull[[i, j]].tolist()
                        break
                    start += row_len
                nominal_impossible = diameter > float(np.linalg.norm(volume)) + 1e-6
                fit = orientation(hull, working, cfg["orientation_search_seed"], cfg["orientation_search_iterations"])
                pieces.append({"name": label, "assembly_axes_size_mm": np.ptp(hull, axis=0).tolist(),
                               "diameter_witness_mm": diameter, "witness_points_mm": witness,
                               "cannot_fit_nominal_cube_by_diameter": nominal_impossible, "orientation_study": fit,
                               "ownership_halfspaces": [{"normal": n.tolist(), "offset": dd} for n, dd in planes]})
                cached[label] = pieces[-1]
                print(f"  {label}: best searched XYZ {np.round(fit['size_xyz_mm'], 2).tolist()}, fits working box={fit['fits_studied_box']}, impossible by diameter={nominal_impossible}", flush=True)
        partition_error = abs(partition_area - area(t))
        if partition_error > max(1e-6, area(t) * 1e-10):
            raise ValueError(f"Exterior partition area mismatch: {name}")
        candidates[name] = {"pieces": pieces, "partition_area_error_mm2": partition_error,
                            "all_fit_studied_box": all(p["orientation_study"]["fits_studied_box"] for p in pieces)}
    # Diagnostic only: distinguish clipped exterior regions on the original scan.
    fig, ax = plt.subplots(2, 2, figsize=(14, 15))
    for aa, ij, sg, title in zip(ax[0], [(0, 2), (1, 2)], [-1, 1], ["Neck candidate: front / XZ", "Neck candidate: side / YZ"]):
        render(aa, t, ij, sg, title)
        seg = section(t, normal, d)
        for s in seg:
            aa.plot(s[:, ij[0]], s[:, ij[1]], color="crimson", lw=.8)
        if ij == (0, 2):
            aa.axvline(0, color="royalblue", lw=1, label="Vertical X = 0")
        aa.set_xlabel('XYZ'[ij[0]] + " (mm)")
        aa.set_ylabel('XYZ'[ij[1]] + " (mm)")
    for aa, ij, sg, title in zip(ax[1], [(0, 2), (1, 2)], [-1, 1], ["12-piece candidate: front / XZ", "12-piece candidate: side / YZ"]):
        render(aa, t, ij, sg, title)
        for group_t, nn, dd, color in [(t, normal, d, "crimson"),
                                      (t, np.array([1., 0, 0]), 0., "royalblue"),
                                      (base, np.array([0., 1, 0]), 0., "darkorange"),
                                      (base, np.array([0., 0, 1]), cfg["base_additional_height_mm"], "forestgreen"),
                                      (head, np.array([0., 0, 1]), cfg["head_additional_height_mm"], "purple")]:
            for s in section(group_t, nn, dd):
                aa.plot(s[:, ij[0]], s[:, ij[1]], color=color, lw=.8)
        aa.set_xlabel('XYZ'[ij[0]] + " (mm)")
        aa.set_ylabel('XYZ'[ij[1]] + " (mm)")
    tilt = math.degrees(math.acos(normal[2] / norm))
    fig.suptitle(f"Candidate neck plane normal {normal.tolist()}, offset {d:.2f}; tilt {tilt:.2f} degrees\n"
                 "Diagnostic projected sections (including hidden surfaces); no printable parts or joints\n"
                 "Red: neck; blue: X split; orange: base Y split; green: base height; purple: head height")
    fig.tight_layout()
    fig.savefig(OUT / FILES[0], dpi=140)
    plt.close(fig)
    fig, axes = plt.subplots(1, 3, figsize=(15, 6))
    tangent_y = np.cross(normal / norm, [1., 0, 0])
    origin_mm = (np.array(cfg["neck_plane_source"]["origin"]) + offset) * scale
    for aa, delta in zip(axes, [-5., 0., 5.]):
        seg = section(t, normal, d + delta * norm)
        for s in seg:
            pp = s - origin_mm
            aa.plot(pp[:, 0], pp @ tangent_y, color="black", lw=.7)
        aa.set_aspect('equal')
        aa.grid(alpha=.2)
        aa.set_title(f"Neck section: normal offset {delta:+.0f} mm")
        aa.set_xlabel("Local X (mm)")
        aa.set_ylabel("Local in-plane Y (mm)")
    fig.suptitle("Unmodified scan neck sections; no dovetail or material-width verification")
    fig.tight_layout()
    fig.savefig(OUT / FILES[1], dpi=140)
    plt.close(fig)
    report = {"scope": cfg["scope"], "scale_config": str(scale_path.relative_to(ROOT)), "mesh_audit": mesh,
              "printer_volume_mm": volume.tolist(), "study_envelope_mm": working.tolist(),
              "allowance_status": cfg["margin_status"], "neck_candidate": {
                  "normal_unit": (normal / norm).tolist(), "origin_assembled_mm": origin_mm.tolist(),
                  "plane_offset_unit_normal_mm": d / norm, "tilt_degrees": tilt,
                  "plane_equation": f"{normal.tolist()} dot XYZ = {d} (mm)", "status": "candidate; not anatomically or structurally approved"},
              "partition_surface_area_error_mm2": area_error, "candidates": candidates,
              "limits": ["No capped cut solids, joints, collision sweeps, supports, or physical fit verified",
                         "Fits use conservative clipped surface envelopes plus possible split-plane cap corners",
                         "Orientation search success is an envelope result only; failure is not an impossibility proof unless diameter witness exceeds cube diagonal",
                         "Self intersections are untested and overlapping shells are not unioned; do not assume Boolean readiness"]}
    (OUT / FILES[2]).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    dependencies = [source, scale_path, cfg_path, Path(__file__), DESIGN / "measure_scale.py", OUT / "scaled_master.stl", OUT / "scaled_master_measurements.json"]
    manifest = {"scope": cfg["scope"], "dependencies": {p.relative_to(ROOT).as_posix(): sha(p) for p in dependencies},
                "artifacts": {name: sha(OUT / name) for name in FILES}}
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    audit()


if __name__ == "__main__":
    main()
