"""Measure the original scan and verify its initial OpenSCAD scale-master export.

Requires NumPy, SciPy, and Matplotlib. No repair, simplification, or landmark detection.
Landmarks are explicit visually selected outer ear-rim mesh vertices in config.
"""
import argparse
import hashlib
import json
import re
import struct
import subprocess
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parents[2]
DESIGN = ROOT / "designs/cicero"
OUT = ROOT / "output/cicero"
DTYPE = np.dtype([("normal", "<f4", (3,)), ("v", "<f4", (3, 3)), ("attr", "<u2")])


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_stl(path):
    data = path.read_bytes()
    if len(data) >= 84:
        count = struct.unpack_from("<I", data, 80)[0]
        if len(data) == 84 + count * 50:
            return np.frombuffer(data, dtype=DTYPE, offset=84)["v"].astype(float)
    # OpenSCAD's default ASCII export; STL carries no intrinsic unit metadata.
    rows = re.findall(rb"\bvertex\s+([^\r\n]+)", data)
    if not rows or len(rows) % 3:
        raise ValueError(f"Invalid STL: {path}")
    return np.fromstring(b" ".join(rows).decode("ascii"), sep=" ").reshape(-1, 3, 3)


def render(ax, triangles, axes, sign, title, landmarks=None, labels=("A", "B")):
    i, j = axes
    k = 3 - i - j
    center = triangles.mean(axis=1)
    order = np.argsort(sign * center[:, k])
    normal = np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])
    normal /= np.maximum(np.linalg.norm(normal, axis=1)[:, None], 1e-20)
    shade = .25 + .7 * np.maximum(0, sign * normal[:, k])
    ax.add_collection(PolyCollection(triangles[order][:, :, [i, j]],
                      facecolors=plt.cm.Greys_r(shade[order]), edgecolors="none"))
    ax.autoscale()
    ax.set_aspect("equal")
    ax.set_xlabel("XYZ"[i])
    ax.set_ylabel("XYZ"[j])
    ax.set_title(title)
    ax.grid(alpha=.2)
    if landmarks is not None:
        ax.plot(landmarks[:, i], landmarks[:, j], "o-", color="crimson", lw=1.5, ms=5)
        for label, p in zip(labels, landmarks):
            ax.annotate(label, (p[i], p[j]), xytext=(7, 7), textcoords="offset points", color="crimson")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-export", action="store_true")
    parser.add_argument("--audit-only", action="store_true", help="Check the saved evidence hashes and exact file set without writing")
    args = parser.parse_args()
    if args.audit_only:
        record = json.loads((OUT / "scaled_master_measurements.json").read_text())
        for item in [record["source"], record["config"], record["export_verification"]]:
            if sha(ROOT / item["path"]) != item["sha256"]:
                raise ValueError(f"Evidence hash mismatch: {item['path']}")
        if sha(DESIGN / "src/main.scad") != record["scad_sha256"] or sha(Path(__file__)) != record["measurement_script_sha256"]:
            raise ValueError("Source or measurement script changed")
        for name, digest in record["generated_png_sha256"].items():
            if sha(OUT / name) != digest:
                raise ValueError(f"PNG hash mismatch: {name}")
        for name, digest in record["preserved_import_sha256"].items():
            if sha(OUT / name) != digest:
                raise ValueError(f"Imported file hash mismatch: {name}")
        expected = set(record["generated_png_sha256"]) | set(record["preserved_import_sha256"]) | {"README.md", "scaled_master.stl", "scaled_master_measurements.json"}
        study = OUT / "split_study_manifest.json"
        if study.exists():
            # Optional declared diagnostic extension; it does not turn this into
            # a complete printable-part manifest or an assembly approval.
            subprocess.run([sys.executable, str(DESIGN / "analyze_splits.py"), "--audit-only"], check=True)
            expected |= {"split_study_manifest.json", "split_study_report.json", "split_study_preview.png", "split_study_sections.png"}
        neck_study = OUT / "neck_interface_manifest.json"
        if neck_study.exists():
            subprocess.run([sys.executable, str(DESIGN / "study_neck_interface.py"), "--audit-only"], check=True)
            expected |= {"neck_interface_manifest.json", "neck_interface_report.json", "neck_interface_angles.png", "neck_interface_joint.png"}
        if (OUT / "intermediate_exports_manifest.json").exists():
            subprocess.run([sys.executable, str(DESIGN / "export_intermediates.py"), "--audit-only"], check=True)
            expected |= {"intermediate_exports_manifest.json", "intermediate_exports_report.json", "intermediate_head_base.png", "head_intermediate.stl", "base_intermediate.stl"}
        if (OUT / "head_fit_manifest.json").exists():
            subprocess.run([sys.executable, str(DESIGN / "fit_head.py"), "--audit-only"], check=True)
            expected |= {"head_fit_manifest.json", "head_fit_report.json", "head_fit_preview.png", "head_fit_top.stl", "head_fit_lower_left.stl", "head_fit_lower_right.stl"}
        if (OUT / "face_up_manifest.json").exists():
            subprocess.run([sys.executable, str(DESIGN / "face_up_split.py"), "--audit-only"], check=True)
            expected |= {"face_up_manifest.json", "face_up_report.json", "face_up_bed_review.png", "face_up_face_preview.png",
                         "face_up_face.stl", "face_up_rear_left_lower.stl", "face_up_rear_left_upper.stl",
                         "face_up_rear_right_lower.stl", "face_up_rear_right_upper.stl"}
        if {p.name for p in OUT.iterdir()} != expected or any(p.is_dir() for p in OUT.iterdir()):
            raise ValueError("Unexpected or missing output files")
        if len(record["generated_png_sha256"]) != 19 or record["export_verification"]["result"] != "passed":
            raise ValueError("Incomplete single-master evidence")
        print(f"PASS: single-master measurement audit; 1 generated STL, 19 PNGs; source/config/artifact hashes match. Output: {OUT}")
        return
    cfg_path = DESIGN / "configs/rev_0001.json"
    cfg = json.loads(cfg_path.read_text())
    source = DESIGN / "assets/cicero_original.stl"
    print(f"Source: {source}\nConfig: {cfg_path}\nOutput: {OUT}", flush=True)
    if sha(source) != cfg["source_sha256"]:
        raise ValueError("Source mesh hash does not match config")
    triangles = read_stl(source)
    vertices = triangles.reshape(-1, 3)
    ears = np.array([cfg["ear_negative_x"], cfg["ear_positive_x"]])
    for ear in ears:
        if np.min(np.linalg.norm(vertices - ear, axis=1)) > 1e-7:
            raise ValueError("Ear landmark is not a source vertex")
    distance = float(np.linalg.norm(ears[1] - ears[0]))
    scale = cfg["target_ear_span_mm"] / distance
    offset = np.array(cfg["source_offset"])
    scaled = (triangles + offset) * scale
    scaled_ears = (ears + offset) * scale
    bounds = np.array([scaled.min(axis=(0, 1)), scaled.max(axis=(0, 1))])
    matrix = np.eye(4) * scale
    matrix[:3, 3] = offset * scale
    matrix[3, 3] = 1
    report = {
        "scope": "Single unsplit scale reference; not a complete manifest build or fabrication approval",
        "source": {"path": source.relative_to(ROOT).as_posix(), "sha256": sha(source),
                   "triangles": len(triangles), "units": "STL unitless; retained source coordinates",
                   "bounds": [vertices.min(0).tolist(), vertices.max(0).tolist()]},
        "config": {"path": cfg_path.relative_to(ROOT).as_posix(), "sha256": sha(cfg_path)},
        "scad_sha256": sha(DESIGN / "src/main.scad"),
        "measurement_script_sha256": sha(Path(__file__)),
        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "preserved_import_sha256": {name: sha(OUT / name) for name in ["2.stl", "5352-tsaritsyno-museum-moscow-bust-5(1).3mf", "simplified.stl"]},
        "landmark_interpretation": "Initial visually selected outer lateral ear-rim points; user review pending",
        "source_ear_landmarks": ears.tolist(), "source_ear_span": distance,
        "target_ear_span_mm": cfg["target_ear_span_mm"], "uniform_scale": scale,
        "rotation_degrees": [0, 0, 0], "source_translation_before_scale": offset.tolist(),
        "source_to_assembled_matrix": matrix.tolist(), "scaled_ear_landmarks_mm": scaled_ears.tolist(),
        "scaled_ear_span_mm": float(np.linalg.norm(scaled_ears[1] - scaled_ears[0])),
        "assembled_bounds_mm": bounds.tolist(), "assembled_size_xyz_mm": (bounds[1] - bounds[0]).tolist(),
        "structural_joins": "unverified", "minimum_material_width": "unverified",
        "export_verification": "not requested",
    }
    OUT.mkdir(exist_ok=True)
    if args.verify_export:
        export = OUT / "scaled_master.stl"
        actual = read_stl(export)
        if actual.shape != scaled.shape:
            raise ValueError("Export triangle count changed")
        actual_bounds = np.array([actual.min(axis=(0, 1)), actual.max(axis=(0, 1))])
        # Compare triangles independent of winding and file ordering, not only bounds.
        tree = cKDTree(actual.mean(1))
        _, matches = tree.query(scaled.mean(1))
        from itertools import permutations
        error = np.full(len(scaled), np.inf)
        for perm in permutations(range(3)):
            error = np.minimum(error, np.max(np.linalg.norm(scaled - actual[matches][:, perm], axis=2), axis=1))
        max_error = float(error.max())
        if len(np.unique(matches)) != len(scaled) or max_error > .002:
            raise ValueError(f"Export triangles differ: {max_error} mm")
        if np.max(np.abs(actual_bounds - bounds)) > .002:
            raise ValueError("Export bounds differ")
        # Normalize ASCII once. Existing binary files remain byte-for-byte intact:
        # recomputing normals from rounded float32 vertices causes needless churn.
        raw = export.read_bytes()
        binary = len(raw) >= 84 and len(raw) == 84 + struct.unpack_from("<I", raw, 80)[0] * 50
        if not binary:
            records = np.zeros(len(actual), dtype=DTYPE)
            records["v"] = actual
            normals = np.cross(actual[:, 1] - actual[:, 0], actual[:, 2] - actual[:, 0])
            normals /= np.maximum(np.linalg.norm(normals, axis=1)[:, None], 1e-20)
            records["normal"] = normals
            export.write_bytes(b"Cicero uniformly scaled measurement master".ljust(80, b"\0") + struct.pack("<I", len(actual)) + records.tobytes())
        installed = read_stl(export)
        if np.max(np.abs(installed - actual)) > .0001:
            raise ValueError("Binary STL normalization exceeded tolerance")
        installed_vertices = installed.reshape(-1, 3)
        exported_ears = np.array([installed_vertices[np.argmin(np.linalg.norm(installed_vertices - ear, axis=1))] for ear in scaled_ears])
        actual_span = float(np.linalg.norm(exported_ears[1] - exported_ears[0]))
        if abs(actual_span - cfg["target_ear_span_mm"]) > .002:
            raise ValueError("Export ear-tip distance is outside tolerance")
        report["export_verification"] = {"result": "passed", "tolerance_mm": .002,
            "max_triangle_vertex_error_mm": max_error, "ear_span_mm": actual_span,
            "bounds_mm": [installed_vertices.min(0).tolist(), installed_vertices.max(0).tolist()],
            "triangles": len(installed), "path": export.relative_to(ROOT).as_posix(), "sha256": sha(export)}
    fig, axes = plt.subplots(1, 3, figsize=(16, 8))
    for ax, ij, sign, title in zip(axes, [(0, 2), (1, 2), (0, 1)], [-1, 1, 1],
                                  ["Front / XZ", "Side / YZ", "Top / XY"]):
        render(ax, scaled, ij, sign, title, scaled_ears)
    dims = bounds[1] - bounds[0]
    fig.suptitle(f"Cicero initial master: {dims[0]:.2f} × {dims[1]:.2f} × {dims[2]:.2f} mm (XYZ)\n"
                 f"3D distance A–B = {report['scaled_ear_span_mm']:.3f} mm; projections appear shorter")
    fig.tight_layout()
    fig.savefig(OUT / "scaled_master_dimensions.png", dpi=150)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(12, 9))
    center = triangles.mean(1)
    for index, (ax, sign) in enumerate(zip(axes, [-1, 1])):
        mask = (center[:, 2] > 35) & (center[:, 2] < 49) & (sign * center[:, 0] > 6)
        render(ax, triangles[mask], (1, 2), sign, f"Source ear {'AB'[index]}: lateral rim", ears[index:index+1], labels=("AB"[index],))
        ax.set_xlim((-12, 1) if sign < 0 else (-1, 10))
        ax.set_ylim(35, 49)
    fig.suptitle("Initial ear-rim landmark selection in source coordinates (unitless)")
    fig.tight_layout()
    fig.savefig(OUT / "source_ear_landmarks.png", dpi=150)
    plt.close(fig)
    standard_pngs = sorted(OUT.glob("scaled_master*.png"))
    standard_pngs = [p for p in standard_pngs if p.name != "scaled_master_dimensions.png"]
    if args.verify_export and (len(standard_pngs) != 17 or any(p.stat().st_size == 0 for p in standard_pngs)):
        raise ValueError(f"Expected 17 standard PNGs, got {len(standard_pngs)}")
    report["generated_png_sha256"] = {p.name: sha(p) for p in standard_pngs + [OUT / "scaled_master_dimensions.png", OUT / "source_ear_landmarks.png"]}
    destination = OUT / "scaled_master_measurements.json"
    destination.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Source ear distance: {distance:.9f}; uniform scale: {scale:.9f}")
    print(f"Assembled XYZ mm: {dims.tolist()}\nEvidence: {destination}", flush=True)


if __name__ == "__main__":
    main()
