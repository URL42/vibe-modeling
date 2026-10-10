"""Measure the installed Raspberry Pi case STLs independently of SCAD assertions.

Run after the complete manifest audit. This reads artifacts without generating
temporary geometry. Line intersections are sections of the final triangle mesh.
Physical fastener retention, printer settings and cable fit are outside scope.
"""
import argparse
from collections import defaultdict
import json
import hashlib
from pathlib import Path

import scad_build_all as build
from validate_cad_assembly_contract import stl_vertices


TOL = 0.002  # STL coordinate rounding, not a structural allowance.


def require(condition, message):
    if not condition:
        raise SystemExit("FAIL: " + message)


def close(actual, expected, label):
    require(abs(actual - expected) <= TOL, f"{label}: {actual} != {expected}")


class Mesh:
    def __init__(self, path):
        self.path = path
        vertices = list(stl_vertices(path))
        require(len(vertices) % 3 == 0, "incomplete STL triangles")
        self.triangles = [vertices[i:i + 3] for i in range(0, len(vertices), 3)]
        self.bounds = [[f(v[a] for v in vertices) for a in range(3)] for f in (min, max)]

    def topology(self):
        edges = defaultdict(list)
        directed = defaultdict(list)
        volume = 0.0
        for i, tri in enumerate(self.triangles):
            for j in range(3):
                # STL repeats identical coordinates for shared vertices.
                key = tuple(sorted((tri[j], tri[(j + 1) % 3])))
                edges[key].append(i)
                directed[key].append((tri[j], tri[(j + 1) % 3]))
            a, b, c = tri
            volume += (a[0] * (b[1]*c[2] - b[2]*c[1])
                       + a[1] * (b[2]*c[0] - b[0]*c[2])
                       + a[2] * (b[0]*c[1] - b[1]*c[0])) / 6
        require(all(len(faces) == 2 for faces in edges.values()),
                f"{self.path.name}: nonmanifold/open triangle edges")
        require(all(pair[0] == (pair[1][1], pair[1][0]) for pair in directed.values()),
                f"{self.path.name}: inconsistent face winding")
        require(volume > 0, f"{self.path.name}: nonpositive signed volume")
        neighbors = defaultdict(set)
        for a, b in edges.values():
            neighbors[a].add(b)
            neighbors[b].add(a)
        unseen = set(range(len(self.triangles)))
        components = 0
        while unseen:
            components += 1
            todo = [unseen.pop()]
            while todo:
                for n in neighbors[todo.pop()]:
                    if n in unseen:
                        unseen.remove(n)
                        todo.append(n)
        require(components == 1, f"{self.path.name}: {components} disconnected shells")
        return {"triangles": len(self.triangles), "closed_shells": components,
                "bounds_mm": self.bounds, "signed_volume_mm3": volume, "consistent_winding": True}

    def intervals(self, axis, fixed):
        """Solid intervals on an infinite axis line, from triangle intersections."""
        other = [a for a in range(3) if a != axis]
        hits = []
        for tri in self.triangles:
            a, b, c = tri
            u, v = other
            det = (b[v] - c[v]) * (a[u] - c[u]) + (c[u] - b[u]) * (a[v] - c[v])
            if abs(det) < 1e-10:
                continue
            x, y = fixed
            w0 = ((b[v] - c[v]) * (x - c[u]) + (c[u] - b[u]) * (y - c[v])) / det
            w1 = ((c[v] - a[v]) * (x - c[u]) + (a[u] - c[u]) * (y - c[v])) / det
            w2 = 1 - w0 - w1
            if min(w0, w1, w2) >= -1e-8:
                hits.append(w0 * a[axis] + w1 * b[axis] + w2 * c[axis])
        unique = []
        for value in sorted(hits):
            if not unique or value - unique[-1] > 1e-5:
                unique.append(value)
        require(len(unique) % 2 == 0, f"ambiguous mesh section axis={axis}, fixed={fixed}: {unique}")
        return list(zip(unique[::2], unique[1::2]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--summary", action="store_true", help="Print concise results instead of all mesh sections")
    args = parser.parse_args()
    cp = Path(args.config).resolve()
    cfg = json.loads(cp.read_text(encoding="utf-8"))
    rev = cp.stem
    out = build.REPO_ROOT / "output/raspberrypi5_case"
    build.audit("raspberrypi5_case", rev, "current", cp,
                build.REPO_ROOT / "designs/raspberrypi5_case/parts.json",
                build.REPO_ROOT / "designs/raspberrypi5_case/src")
    base = Mesh(out / f"base_{rev}.stl")
    lid = Mesh(out / f"lid_{rev}.stl")
    e, t, h = cfg["envelope"], cfg["lid_slab_t"], cfg["m3_rim_h"]
    z, minimum = e - t, cfg["minimum_wall_thickness"]
    report = {"config": {"path": build.repo_relative(cp), "sha256": build.sha256_file(cp)},
              "build_manifest_sha256": build.sha256_file(out / "build_manifest.json"),
              "base": base.topology(), "lid": lid.topology(), "sections": []}
    for mesh, expected in [(base, [[0, 0, 0], [e, e, z]]),
                           (lid, [[0, 0, z], [e, e, e + cfg["emblem_t"] + cfg["bezel_h"]]])]:
        for row, target in zip(mesh.bounds, expected):
            for a, b in zip(row, target):
                close(a, b, f"{mesh.path.name} bounds")
        report[mesh.path.stem + "_sha256"] = build.sha256_file(mesh.path)
    close(e, 120, "approved nominal shell envelope")
    close(t, 7, "approved lid thickness")
    close(h, 3, "approved stud height")
    close(cfg["m3_cbore_depth"], 4, "retained head recess depth")

    def section(mesh, axis, fixed, expected, label):
        actual = mesh.intervals(axis, fixed)
        require(len(actual) == len(expected), f"{label}: {actual} != {expected}")
        for pair, target in zip(actual, expected):
            for a, b in zip(pair, target):
                close(a, b, label)
        report["sections"].append({"label": label, "axis": axis,
                                   "fixed_mm": fixed, "solid_intervals_mm": actual})

    # Flat lid underside away from decoration and screws.
    for x, y in [(20.13, 20.27), (60.13, 20.27), (100.13, 20.27),
                 (20.13, 100.27), (100.13, 100.27)]:
        section(lid, 2, (x, y), [(z, e)], "flat slab thickness/underside")

    # Post-subtraction stud throats and wall attachment sections at seam
    # start/mid/end. Rear studs engage the side wall only; there is no rear wall.
    size, wall, inset = cfg["m3_rim_size"], cfg["wall_t"], cfg["m3_inset"]
    for x0 in [0, e - size]:
        for y0 in [0, e - size]:
            for offset in [0.17, size / 2 + 0.13, size - 0.17]:
                x = wall / 2 if x0 == 0 else e - wall / 2
                section(base, 2, (x, y0 + offset), [(0, z)], "stud/side-wall seam continuity")
            x = x0 + (wall + 0.37 if x0 == 0 else size - wall - 0.37)
            y = y0 + size / 2 + 0.23
            section(base, 2, (x, y), [(0, cfg["floor_t"]), (z - h, z)], "3 mm stud throat")
    for offset in [0.17, e / 2 + 0.13, e - 0.17]:
        section(base, 2, (offset, wall / 2), [(0, z)], "front-wall support/floor seam")
    section(base, 0, (e / 2 + 0.13, z / 2 + 0.19),
            [(0, wall), (e-wall, e)], "side-wall thickness and clear interior")
    section(base, 1, (e / 2 + 0.13, z / 2 + 0.19), [(0, wall)],
            "front-wall thickness and open rear")
    # Empty back and interior: only the floor is present.
    section(base, 2, (e / 2 + 0.13, e - 0.27), [(0, cfg["floor_t"])], "open rear")

    for x in [inset, e - inset]:
        for y in [inset, e - inset]:
            pr = cfg["m3_pilot_d"] / 2
            lr, cr = cfg["m3_clear_d"] / 2, cfg["m3_cbore_d"] / 2
            # Axis sections expose both hole boundaries and the inner stud edge.
            section(base, 0, (y, z - h / 2),
                    [(0, inset-pr), (inset+pr, size), (e-size, e-inset-pr), (e-inset+pr, e)],
                    "pilot bores and both block ligaments")
            section(lid, 0, (y, e - cfg["m3_cbore_depth"] / 2),
                    [(0, inset-cr), (inset+cr, e-inset-cr), (e-inset+cr, e)], "counterbore diameter/alignment")
            section(lid, 0, (y, z + 0.23), [(0, inset-lr), (inset+lr, e-inset-lr), (e-inset+lr, e)], "clearance bore diameter/alignment")
            section(lid, 2, (x + (lr + cr) / 2, y),
                    [(z, e - cfg["m3_cbore_depth"])], "retained screw-head seat floor")
    floor = t - cfg["m3_cbore_depth"]
    required_floor = cfg.get("minimum_lid_recess_floor", minimum)
    require(floor + TOL >= required_floor, "recess floor below declared minimum")
    require(min(size - inset - cfg["m3_pilot_d"] / 2,
                inset - cfg["m3_cbore_d"] / 2) >= minimum, "fastener edge ligament")
    # rev_0003: approved four underside mounting-head recesses. The older
    # zero-depth configuration retains the original plain through-holes.
    head_depth = cfg.get("pi_mount_head_depth", 0)
    if rev == "rev_0004":
        close(head_depth, 3, "retained underside head-seat depth")
    if head_depth > 0:
        head_d = cfg["pi_mount_head_d"]
        close(cfg["floor_t"], 6, "approved thicker base floor")
        close(head_d, 5, "approved mounting-head diameter")
        close(head_depth, 3, "approved mounting-head depth")
        require(cfg["floor_t"] - head_depth >= minimum, "thin roof above base head recess")
        xs = [cfg["pi_x_off"] + cfg["pi_hole_inset"],
              cfg["pi_x_off"] + cfg["pi_hole_inset"] + cfg["pi_hole_span_x"]]
        ys = [cfg["pi_y_off"] + cfg["pi_hole_inset"],
              cfg["pi_y_off"] + cfg["pi_hole_inset"] + cfg["pi_hole_span_y"]]
        for x in xs:
            for y in ys:
                r = head_d / 2
                pr = cfg["pi_hole_d"] / 2
                section(base, 0, (y, head_depth / 2),
                        [(0, xs[0]-r), (xs[0]+r, xs[1]-r), (xs[1]+r, e)],
                        "underside head diameters and exterior ligaments")
                section(base, 1, (x, head_depth / 2),
                        [(0, ys[0]-r), (ys[0]+r, ys[1]-r), (ys[1]+r, e)],
                        "underside head diameters and pairwise ligaments")
                section(base, 0, (y, (head_depth + cfg["floor_t"]) / 2),
                        [(0, xs[0]-pr), (xs[0]+pr, xs[1]-pr), (xs[1]+pr, e)],
                        "retained diameter-2.7 mounting bores")
                section(base, 2, (x + (r + pr) / 2, y),
                        [(head_depth, cfg["floor_t"])], "3 mm floor above mounting-head seat")
                section(base, 2, (wall + 0.13, y), [(0, cfg["floor_t"])],
                        "uninterrupted floor beside side-wall seam")
        reference_path = build.REPO_ROOT / "designs/raspberrypi5_case/docs/rev_0002_lid_compatibility.json"
        reference = json.loads(reference_path.read_text(encoding="utf-8"))
        approved_layout = {}
        if rev == "rev_0004":
            approved_layout = {"pi_w": 56.0, "pi_d": 85.0, "pi_y_off": 17.5,
                               "pi_hole_span_x": 49.0, "pi_hole_span_y": 58.0}
            for key, value in approved_layout.items():
                require(cfg.get(key) == value, f"approved rotated PCB input changed: {key}")
            require(xs == [8.5, 57.5] and ys == [21.0, 79.0],
                    "mounting centers differ from approved official-drawing transform")
            for x, y in reference["mount_centers_mm"]:
                section(base, 2, (x, y), [(0, 6)], "obsolete mounting station restored to solid floor")
            report["rotated_mounting_pattern"] = {"result": "PASS", "pitch_mm": [49, 58],
                                                 "centers_mm": [[x,y] for x in xs for y in ys]}
        for key, value in reference["frozen_config"].items():
            if key in approved_layout:
                continue
            require(cfg.get(key) == value, f"printed-lid compatibility input changed: {key}")
        require(build.sha256_file(build.REPO_ROOT / "designs/raspberrypi5_case/src/parts/lid.scad")
                == reference["lid_source_sha256"], "printed lid source changed")
        canonical = sorted(tuple(sorted(tuple(round(c, 6) for c in v) for v in tri))
                           for tri in lid.triangles)
        geometry_hash = hashlib.sha256(json.dumps(canonical, separators=(',', ':')).encode()).hexdigest()
        require(geometry_hash == reference["lid_canonical_triangle_sha256"],
                "exported lid geometry differs from the printed rev_0002 reference")
        report["printed_lid_compatibility"] = {"result": "PASS", "reference": build.repo_relative(reference_path),
                                               "canonical_geometry_sha256": geometry_hash}
    # Floor PCB holes and button bore are measured from the final meshes.
    for x in [cfg["pi_x_off"] + cfg["pi_hole_inset"],
              cfg["pi_x_off"] + cfg["pi_hole_inset"] + cfg["pi_hole_span_x"]]:
        for y in [cfg["pi_y_off"] + cfg["pi_hole_inset"],
                  cfg["pi_y_off"] + cfg["pi_hole_inset"] + cfg["pi_hole_span_y"]]:
            section(base, 2, (x, y), [], "PCB mounting hole through-floor")
    cx, cy, br = cfg["emblem_center_x"], cfg["emblem_center_y"], cfg["button_hole_d"] / 2
    section(lid, 0, (cy, z + 0.19), [(0, cx - br), (cx + br, e)], "28 mm button bore")
    section(lid, 2, (cx + br + 0.31, cy), [(z, e + cfg["emblem_t"] + cfg["bezel_h"])],
            "lens/emblem/slab continuous load path")
    close(base.bounds[1][2], lid.bounds[0][2], "assembled parting faces")
    report["result"] = "PASS"
    report["recess_floor_mm"] = floor
    report["scope"] = "Digital mesh geometry; physical fit/retention and slicer validation remain unverified."
    if args.summary:
        print("PASS: installed STL geometry, closed-shell connectivity, "
              f"{len(report['sections'])} post-subtraction line sections, "
              f"{t:g} mm slab, {h:g} mm studs, {floor:g} mm recess floors")
        if head_depth > 0:
            print("PASS: four diameter-5 x 3 mm underside head recesses, 3 mm retained roofs; "
                  "printed rev_0002 lid geometry and coupling unchanged")
        if rev == "rev_0004":
            print("PASS: rotated 49 x 58 mm mounting pitch at approved centers; all four obsolete stations solid")
        print("Base bounds:", base.bounds, "Lid bounds:", lid.bounds)
        print("STL SHA-256:", report[base.path.stem + "_sha256"], report[lid.path.stem + "_sha256"])
    else:
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
