"""Assess head fit and export a demonstrated three-piece intermediate layout.

No joints or slicer approval. A spherical direction grid plus a Lipschitz bound
certifies that the whole head is too wide for any orientation in a 220 mm cube.
Two-piece search is finite, not an impossibility proof for all possible cuts.
"""
import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull, distance
from scipy.spatial.transform import Rotation

from measure_scale import ROOT, DESIGN, OUT, read_stl, render, sha
from analyze_splits import orientation
from export_intermediates import capped_cut, mesh_check, write_stl

NAMES = ["head_fit_top.stl", "head_fit_lower_left.stl", "head_fit_lower_right.stl", "head_fit_preview.png", "head_fit_report.json"]


def width_certificate(points):
    diameter = float(distance.pdist(points).max())
    theta, phi = np.meshgrid(np.radians(np.arange(91)), np.radians(np.arange(360)), indexing="ij")
    directions = np.column_stack([np.sin(theta.ravel()) * np.cos(phi.ravel()),
                                  np.sin(theta.ravel()) * np.sin(phi.ravel()), np.cos(theta.ravel())])
    minimum = np.inf
    for start in range(0, len(directions), 128):
        widths = np.ptp(points @ directions[start:start+128].T, axis=0)
        minimum = min(minimum, float(widths.min()))
    # Every hemisphere direction is <=0.5 deg theta + 0.5 deg phi from a grid
    # sample; opposite directions have identical width. Width is the support
    # function of P-P, so its Lipschitz constant is the diameter of P.
    angular_radius = math.radians(1.)
    lower = minimum - diameter * 2 * math.sin(angular_radius / 2)
    return {"grid_directions": len(directions), "minimum_grid_width_mm": minimum,
            "diameter_mm": diameter, "covering_radius_upper_bound_degrees": 1.,
            "all_direction_width_lower_bound_mm": lower,
            "cannot_fit_220_cube_any_rotation": lower > 220,
            "proof": "Directional width changes by at most diameter*||n-m||. All directions are within one degree of the hemisphere grid up to sign. A cube requires three orthogonal widths <=220; here every width exceeds220."}


def search_two(points):
    hull = ConvexHull(points)
    vertices = points[hull.vertices]
    edges = np.unique(np.sort(np.concatenate([hull.simplices[:, [0, 1]], hull.simplices[:, [1, 2]], hull.simplices[:, [2, 0]]]), axis=1), axis=0)
    a, b = points[edges[:, 0]], points[edges[:, 1]]
    normals = [(1,1,1),(1,-1,1),(-1,1,1),(-1,-1,1),(1,0,1),(-1,0,1),(0,1,1),(0,-1,1),
               (1,1,0),(1,-1,0),(1,2,1),(-1,2,1),(1,-2,1),(-1,-2,1),(2,1,1),(-2,1,1),(2,-1,1),(-2,-1,1)]
    best = None
    trials = []
    for raw, fraction in itertools.product(normals, [.45, .5, .55]):
        normal = np.array(raw, dtype=float)
        normal /= np.linalg.norm(normal)
        projection = vertices @ normal
        offset = float(projection.min() + np.ptp(projection) * fraction)
        da, db = a @ normal - offset, b @ normal - offset
        crossing = da * db < 0
        intersection = a[crossing] + (b[crossing] - a[crossing]) * (da[crossing] / (da[crossing] - db[crossing]))[:, None]
        fits = []
        for sign in [-1, 1]:
            q = np.concatenate([vertices[sign * (projection - offset) >= 0], intersection])
            q = q[ConvexHull(q).vertices]
            fits.append(orientation(q, np.array([220.,220.,220.]), 55952, 45))
        score = max(f["envelope_ratio"] for f in fits)
        trial = {"normal": normal.tolist(), "offset_mm": offset, "fraction": fraction, "fits": fits, "worst_envelope_ratio": score}
        trials.append(trial)
        if best is None or score < best["worst_envelope_ratio"]:
            best = trial
            print(f"Two-piece search best worst ratio: {score:.6f}", flush=True)
    return {"cuts_tested": len(trials), "best": best, "any_pair_fit_nominal_cube": any(t["worst_envelope_ratio"] <= 1 for t in trials),
            "trials": trials, "limit": "Finite planar direction/offset and orientation search; cannot exclude all two-piece layouts or nonplanar cuts"}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--audit-only", action="store_true")
    args = p.parse_args()
    manifest_path = OUT / "head_fit_manifest.json"
    if args.audit_only:
        m = json.loads(manifest_path.read_text())
        for name, digest in m["dependencies"].items():
            if sha(ROOT / name) != digest:
                raise ValueError(f"Head-fit dependency changed: {name}")
        if set(m["artifacts"]) != set(NAMES):
            raise ValueError("Head-fit coverage mismatch")
        for name, digest in m["artifacts"].items():
            if sha(OUT / name) != digest:
                raise ValueError(f"Head-fit artifact changed: {name}")
        print("PASS: intermediate head-fit artifacts and provenance")
        return
    source = OUT / "head_intermediate.stl"
    t = read_stl(source)
    original = mesh_check(t)
    points = t.reshape(-1,3)
    hull_points = points[ConvexHull(points).vertices]
    print(f"Source: {source}\nOutput: {OUT}\nMeasuring whole-head fit", flush=True)
    certificate = width_certificate(hull_points)
    print(f"Certified all-direction width lower bound: {certificate['all_direction_width_lower_bound_mm']:.4f} mm", flush=True)
    two = search_two(hull_points)
    print("Exporting three-piece fit witness at Z=460 and lower X=0", flush=True)
    top, _ = capped_cut(t, np.array([0.,0.,1.]), 460.)
    lower, _ = capped_cut(t, np.array([0.,0.,-1.]), -460.)
    left, _ = capped_cut(lower, np.array([-1.,0.,0.]), 0.)
    right, _ = capped_cut(lower, np.array([1.,0.,0.]), 0.)
    results = []
    fig, axes = plt.subplots(1,3,figsize=(15,8))
    for name, q, ax in zip(NAMES[:3], [top,left,right], axes):
        vertices = q.reshape(-1,3)
        pts = vertices[ConvexHull(vertices).vertices]
        fit = orientation(pts, np.array([210.,210.,220.]), 55952, 110)
        if not fit["fits_studied_box"]:
            raise ValueError(f"Candidate does not fit working envelope: {name}: {fit}")
        matrix = Rotation.from_euler("xyz", fit["rotate_xyz_degrees"], degrees=True).as_matrix()
        rotated = q @ matrix.T
        translation = np.array([5.,5.,0.]) - rotated.min(axis=(0,1))
        print_q = rotated + translation
        destination = OUT / name
        write_stl(destination, print_q)
        installed = read_stl(destination)
        check = mesh_check(installed)
        if any(check[k] for k in ["boundary_edges","nonmanifold_edges","inconsistent_edge_winding"]) or check["connected_shells"] != 1:
            raise ValueError(f"Exported head piece topology failed: {name}: {check}")
        bounds = np.array(check["bounds_mm"])
        if np.any(bounds[0] < -.001) or np.any(bounds[1] > 220.001):
            raise ValueError("Installed piece exceeds cube")
        results.append({"name": name, "fit": fit, "installed_mesh": check,
                        "assembly_to_print_rotation_matrix": matrix.tolist(), "assembly_to_print_translation_mm": translation.tolist(),
                        "source_region_volume_mm3": mesh_check(q)["signed_volume_mm3"], "sha256": sha(destination)})
        render(ax, installed, (0,2), -1, name.replace(".stl", ""))
        ax.set_xlim(0,220)
        ax.set_ylim(0,220)
        print(f"{name}: installed XYZ {np.round(check['size_xyz_mm'],3).tolist()}", flush=True)
    volume_error = abs(sum(r["source_region_volume_mm3"] for r in results) - original["signed_volume_mm3"])
    if volume_error > max(10., original["signed_volume_mm3"] * 1e-6):
        raise ValueError("Head-piece volume recombination failed")
    fig.suptitle("Three intermediate head pieces in stored print transforms; 220 mm cube\nBodies have 5 mm minimum XY bed margin; supports, joining features, and slicer settings unverified")
    fig.tight_layout()
    fig.savefig(OUT / "head_fit_preview.png",dpi=140)
    plt.close(fig)
    report = {"source": source.relative_to(ROOT).as_posix(), "source_size_xyz_mm": original["size_xyz_mm"],
              "whole_head_width_certificate": certificate, "two_piece_search": two,
              "smallest_demonstrated_body_fit_count": 3, "absolute_minimum_piece_count": "Unproven: whole head excluded, tested two-piece layouts failed, three-piece witness fits",
              "layout": "One top cap above assembly Z=460; lower region split at X=0; each artifact stored in its own print transform",
              "pieces": results, "volume_recombination_error_mm3": volume_error,
              "limits": ["Intermediate reference cuts without dovetails or seam alignment features", "Tilted print orientations require slicer support/bed-contact review; 5mm XY margin is provisional", "Envelope fit and closed topology are not fabrication readiness"]}
    (OUT / "head_fit_report.json").write_text(json.dumps(report,indent=2)+"\n")
    deps = [source, Path(__file__), DESIGN/"export_intermediates.py",DESIGN/"analyze_splits.py",DESIGN/"measure_scale.py"]
    manifest_path.write_text(json.dumps({"dependencies": {p.relative_to(ROOT).as_posix():sha(p) for p in deps},
                                         "artifacts": {name:sha(OUT/name) for name in NAMES}},indent=2)+"\n")


if __name__ == "__main__":
    main()
