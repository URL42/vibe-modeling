"""Study a head-aligned neck cut and preliminary parallel dovetail envelopes.

No repair, Boolean solids, printable exports, or fabrication approval. Local
section margins are evidence at sampled depths only, not full 3D wall checks.
"""
import argparse
import json
import math
import itertools
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from measure_scale import DESIGN, OUT, ROOT, read_stl, render, sha
from analyze_splits import section

ARTIFACTS = ["neck_interface_angles.png", "neck_interface_joint.png", "neck_interface_report.json"]
MANIFEST = OUT / "neck_interface_manifest.json"


def inside(points, segments):
    result = []
    a, b = segments[:, 0], segments[:, 1]
    for p in points:
        straddles = (a[:, 1] > p[1]) != (b[:, 1] > p[1])
        aa, bb = a[straddles], b[straddles]
        crossings = aa[:, 0] + (bb[:, 0] - aa[:, 0]) * (p[1] - aa[:, 1]) / (bb[:, 1] - aa[:, 1])
        result.append(bool(np.count_nonzero(crossings > p[0]) % 2))
    return np.array(result)


def point_segment_distance(points, segments):
    a, b = segments[:, 0], segments[:, 1]
    d = b - a
    vectors = points[:, None, :] - a[None, :, :]
    t = np.clip(np.einsum("pij,ij->pi", vectors, d) / np.maximum(np.sum(d * d, axis=1), 1e-20), 0, 1)
    return np.linalg.norm(vectors - t[:, :, None] * d, axis=2)


def footprint_check(segments, u_center, half_width, half_length):
    corners = np.array([[u_center - half_width, -half_length], [u_center + half_width, -half_length],
                        [u_center + half_width, half_length], [u_center - half_width, half_length]])
    edges = np.stack([corners, np.roll(corners, -1, axis=0)], axis=1)
    # Segment/edge intersections must also be rejected for concave boundaries.
    intersects = False
    for a, b in edges:
        e = b - a
        c, d = segments[:, 0], segments[:, 1] - segments[:, 0]
        det = e[0] * d[:, 1] - e[1] * d[:, 0]
        good = np.abs(det) > 1e-12
        q = c[good] - a
        t = (q[:, 0] * d[good, 1] - q[:, 1] * d[good, 0]) / det[good]
        s = (q[:, 0] * e[1] - q[:, 1] * e[0]) / det[good]
        intersects |= bool(np.any((t >= 0) & (t <= 1) & (s >= 0) & (s <= 1)))
    margin = min(float(point_segment_distance(corners, segments).min()),
                 float(point_segment_distance(segments.reshape(-1, 2), edges).min()))
    contained = bool(inside(corners, segments).all()) and not intersects
    return {"contained": contained, "planar_margin_mm": margin if contained else 0.0, "corners_local_mm": corners.tolist()}


def self_check():
    square = np.array([[[-10., -10], [10, -10]], [[10, -10], [10, 10]],
                       [[10, 10], [-10, 10]], [[-10, 10], [-10, -10]]])
    assert inside(np.array([[0., 0], [20, 0]]), square).tolist() == [True, False]
    check = footprint_check(square, 0, 2, 3)
    assert check["contained"] and abs(check["planar_margin_mm"] - 7) < 1e-10
    assert not footprint_check(square, 9, 2, 3)["contained"]
    print("PASS: section containment, crossing rejection, and exact planar clearance checks", flush=True)


def audit():
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for path, digest in m["dependencies"].items():
        if sha(ROOT / path) != digest:
            raise ValueError(f"Neck-study dependency changed: {path}")
    if set(m["artifacts"]) != set(ARTIFACTS):
        raise ValueError("Neck-study coverage mismatch")
    for name, digest in m["artifacts"].items():
        if sha(OUT / name) != digest:
            raise ValueError(f"Neck-study artifact changed: {name}")
    print("PASS: neck-interface diagnostic artifacts and provenance", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-only", action="store_true")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.audit_only:
        audit()
        return
    self_check()
    if args.self_check:
        return
    config_path = DESIGN / "neck_interface.json"
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    scale_path = DESIGN / cfg["scale_config"]
    scaling = json.loads(scale_path.read_text(encoding="utf-8"))
    source = DESIGN / "assets/cicero_original.stl"
    if sha(source) != scaling["source_sha256"]:
        raise ValueError("Source mesh hash mismatch")
    measurement_path = OUT / "scaled_master_measurements.json"
    measured = json.loads(measurement_path.read_text(encoding="utf-8"))
    if sha(OUT / "scaled_master.stl") != measured["export_verification"]["sha256"]:
        raise ValueError("Scale-master hash mismatch")
    print(f"Source/config: {source}\n{config_path}\nOutput: {OUT}", flush=True)
    t = read_stl(OUT / "scaled_master.stl")
    ears = np.array(scaling["ear_positive_x"]) - scaling["ear_negative_x"]
    u = np.r_[ears[:2] / np.linalg.norm(ears[:2]), 0.]
    posterior = np.cross([0., 0, 1.], u)
    anatomical = np.array([u, posterior, [0., 0, 1.]])
    assert np.allclose(anatomical @ anatomical.T, np.eye(3))
    scale = measured["uniform_scale"]
    origin = (np.array(cfg["source_plane_origin"]) + scaling["source_offset"]) * scale
    local = (t - origin) @ anatomical.T
    j = cfg["joint"]
    assert j["root_overlap_mm"] >= j["minimum_structural_overlap_mm"] >= j["minimum_wall_thickness_mm"]
    assert j["minimum_internal_edge_width_mm"] >= j["minimum_wall_thickness_mm"]
    assert j["throat_width_mm"] >= j["minimum_wall_thickness_mm"]
    flank_slope = (j["flared_width_mm"] - j["throat_width_mm"]) / (2 * j["engagement_depth_mm"])
    comparisons = []
    selected = None
    head_yaw = math.degrees(math.atan2(u[1], u[0]))
    yaws = [head_yaw if y == "head" else float(y) for y in cfg["comparison_yaws_degrees"]]
    for angle, yaw in itertools.product(cfg["comparison_tilts_degrees"], yaws):
        a = math.radians(angle)
        plane_posterior = np.array([-math.sin(math.radians(yaw)), math.cos(math.radians(yaw)), 0.])
        n = np.array([0., 0, 1.]) * math.cos(a) - plane_posterior * math.sin(a)
        joint_u = u - np.dot(u, n) * n
        joint_u /= np.linalg.norm(joint_u)
        v = np.cross(n, joint_u)
        frame = np.array([joint_u, v, n])
        shift_u, shift_v = j["joint_center_shift_in_plane_uv_mm"]
        joint_origin = origin + joint_u * shift_u + v * shift_v
        assert np.allclose(frame @ frame.T, np.eye(3))
        offset = float(n @ origin)
        seg = section(t, n, offset)
        planar = (seg - origin) @ frame.T
        record = {"tilt_degrees": angle, "yaw_degrees": yaw, "normal_assembly": n.tolist(), "offset_mm": offset,
                  "section_size_uv_mm": np.ptp(planar[:, :, :2].reshape(-1, 2), axis=0).tolist()}
        checks = []
        for depth in [-j["engagement_depth_mm"] - j["floor_clearance_mm"], -4., 0., 2., j["root_overlap_mm"]]:
            s = section(t, n, offset + depth)
            s2 = ((s - joint_origin) @ frame.T)[:, :, :2]
            if depth <= 0:
                width = j["throat_width_mm"] / 2 + (-depth) * flank_slope + j["flank_clearance_normal_mm"] * math.sqrt(1 + flank_slope ** 2)
            else:
                width = j["throat_width_mm"] / 2
            for center in j["rail_centers_local_u_mm"]:
                check = footprint_check(s2, center, width, j["rail_length_mm"] / 2)
                check.update({"depth_n_mm": depth, "rail_u_mm": center, "half_width_mm": width})
                checks.append(check)
        record["sampled_footprint_checks"] = checks
        record["all_sampled_margins_at_least_minimum"] = all(c["contained"] and c["planar_margin_mm"] >= j["minimum_internal_edge_width_mm"] for c in checks)
        record["minimum_sampled_margin_mm"] = min(c["planar_margin_mm"] for c in checks)
        comparisons.append(record)
        print(f"Tilt {angle:.3f}, yaw {yaw:.2f}: section {np.round(record['section_size_uv_mm'], 2).tolist()}, min sampled footprint margin {record['minimum_sampled_margin_mm']:.2f} mm", flush=True)
        if abs(angle - cfg["selected_tilt_degrees"]) < 1e-8 and abs(yaw - cfg["selected_plane_yaw_degrees"]) < 1e-8:
            selected = (record, n, v, frame, offset, joint_origin)
    if selected is None:
        raise ValueError("Selected angle missing from comparison list")
    chosen, n, v, frame, offset, joint_origin = selected
    fig, axes = plt.subplots(1, 3, figsize=(16, 8))
    neck_region = local[(local[:, :, 2].min(1) < 150) & (local[:, :, 2].max(1) > -110)]
    render(axes[0], neck_region, (1, 2), 1, "Head-posterior tilt comparisons / sagittal view")
    for angle in cfg["comparison_tilts_degrees"]:
        vv = np.array([-120., 120.])
        axes[0].plot(vv, math.tan(math.radians(angle)) * vv, label=f"{angle:.1f} deg", lw=1)
    axes[0].set_xlim(-165, 135)
    axes[0].set_ylim(-95, 100)
    n_anatomical = n @ anatomical.T
    vv = np.array([-120., 120.])
    axes[0].plot(vv, -n_anatomical[1] / n_anatomical[2] * vv, color="crimson", lw=2, label="Selected scan-posterior")
    axes[0].legend(fontsize=8, loc="upper left")
    for aa, ij, sg, title in zip(axes[1:], [(0, 2), (1, 2)], [-1, 1], ["Selected cut: anatomical front", "Selected cut: anatomical side"]):
        render(aa, neck_region, ij, sg, title)
        s = (section(t, n, offset) - origin) @ anatomical.T
        for ss in s:
            aa.plot(ss[:, ij[0]], ss[:, ij[1]], color="crimson", lw=.9)
        aa.set_ylim(-105, 125)
    fig.suptitle(f"Neck-first working plane: {cfg['selected_tilt_degrees']:.2f} deg, scan-posterior direction (yaw {cfg['selected_plane_yaw_degrees']:g} deg)\nSource origin {cfg['source_plane_origin']}; head yaw {head_yaw:.2f} deg; diagnostic, not a fabrication approval")
    fig.tight_layout()
    fig.savefig(OUT / ARTIFACTS[0], dpi=140)
    plt.close(fig)
    fig, axes = plt.subplots(1, 3, figsize=(16, 7))
    for aa, depth in zip(axes[:2], [0., -j["engagement_depth_mm"] - j["floor_clearance_mm"]]):
        s = ((section(t, n, offset + depth) - joint_origin) @ frame.T)[:, :, :2]
        for ss in s:
            aa.plot(ss[:, 0], ss[:, 1], "k-", lw=.7)
        for center in j["rail_centers_local_u_mm"]:
            half = j["throat_width_mm"] / 2 + (-depth) * flank_slope + j["flank_clearance_normal_mm"] * math.sqrt(1 + flank_slope ** 2) if depth <= 0 else j["throat_width_mm"] / 2
            xx = [center - half, center + half, center + half, center - half, center - half]
            yy = [-30, -30, 30, 30, -30]
            aa.plot(xx, yy, color="royalblue")
            aa.annotate("insertion", xy=(center, -12), xytext=(center, 65), arrowprops={"arrowstyle": "->", "color": "royalblue"}, ha="center", fontsize=8)
        aa.axvline(0, color="orange", ls="--", label="Rail-pair center")
        aa.set_title(f"Neck cross-section N={depth:g} mm")
        aa.set_aspect("equal")
        aa.set_xlabel("U lateral (mm)")
        aa.set_ylabel("V in-plane posterior (mm)")
        aa.grid(alpha=.2)
    aa = axes[2]
    width0, width1 = j["throat_width_mm"] / 2, j["flared_width_mm"] / 2
    depth = j["engagement_depth_mm"]
    for center in j["rail_centers_local_u_mm"]:
        aa.fill([center-width0, center+width0, center+width0, center+width1, center-width1, center-width0],
                [j["root_overlap_mm"], j["root_overlap_mm"], 0, -depth, -depth, 0], color="royalblue", alpha=.5)
    aa.axhline(0, color="black")
    aa.set_aspect("equal")
    aa.set_title("Draft male rails: U/N section\n24 mm throat / 32 mm flare / 8 mm engagement")
    aa.set_xlabel("U lateral (mm)")
    aa.set_ylabel("N above neck plane (mm)")
    aa.grid(alpha=.2)
    fig.suptitle("Head-owned rails / base-owned rear-open sockets: preliminary envelopes only\nBlue footprints omit the rear access channels, front stop, and rear retainer, all still to be modeled")
    fig.tight_layout()
    fig.savefig(OUT / ARTIFACTS[1], dpi=140)
    plt.close(fig)
    source_normal = n
    source_offset = float(n @ cfg["source_plane_origin"])
    report = {"scope": cfg["scope"], "selection_status": cfg["selection_status"],
              "head_yaw_degrees": head_yaw, "origin_assembly_mm": origin.tolist(), "joint_origin_assembly_mm": joint_origin.tolist(),
              "source_plane": {"origin": cfg["source_plane_origin"], "normal_unit": source_normal.tolist(), "offset": source_offset},
              "assembly_plane": {"normal_unit": n.tolist(), "offset_mm": offset},
              "local_to_assembly_basis_columns": frame.T.tolist(), "angle_comparisons": comparisons,
              "selected_comparison": chosen, "joint": j,
              "dovetail_flank_angle_from_normal_degrees": math.degrees(math.atan(flank_slope)),
              "receiver_pair_material_inventory": {
                  "nominal_web_at_socket_floor_mm": abs(j["rail_centers_local_u_mm"][1] - j["rail_centers_local_u_mm"][0]) -
                      (j["throat_width_mm"] + 2 * ((j["engagement_depth_mm"] + j["floor_clearance_mm"]) * flank_slope +
                       j["flank_clearance_normal_mm"] * math.sqrt(1 + flank_slope ** 2))),
                  "status": "Nominal local cross-section only; receiver outlet and full shortest 3D ligament remain unverified"},
              "insertion_unit_vector": (-v).tolist(),
              "ownership": "Both male rails belong to the head; both receivers belong to the base. Head/base subdivisions are deferred until this neck interface is established.",
              "sequence": "Slide the head anterior along both parallel rails into the base; seat against a front stop and install a rear retainer. Subdivision sequence is outside this study.",
              "limits": ["No whole-interface clearance sweep, rear-mouth/throat/retainer material verification, production solids, or strength test",
                         "Section margins are exact planar distances at sampled depths only; 3D shortest material widths remain unverified",
                         "Head/base subdivision and printer-envelope studies are outside this focused neck-interface study",
                         "Source overlapping shells still require validated union; head/base assemblies are conceptual, not printable leaves"]}
    (OUT / ARTIFACTS[2]).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    deps = [source, scale_path, config_path, Path(__file__), DESIGN / "measure_scale.py", DESIGN / "analyze_splits.py", OUT / "scaled_master.stl", measurement_path]
    MANIFEST.write_text(json.dumps({"scope": cfg["scope"], "dependencies": {p.relative_to(ROOT).as_posix(): sha(p) for p in deps},
                                   "artifacts": {name: sha(OUT / name) for name in ARTIFACTS}}, indent=2) + "\n", encoding="utf-8")
    audit()


if __name__ == "__main__":
    main()
