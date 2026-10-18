"""Face-first head references with a genuine cut face flat on the bed.

No arbitrary orientation optimizer. Every accepted print transform maps a
declared ownership-plane normal to +Z and its capped face to the bed.
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from scipy.optimize import minimize_scalar

from measure_scale import ROOT, DESIGN, OUT, read_stl, render, sha
from analyze_splits import clip, envelope
from export_intermediates import capped_cut, mesh_check, write_stl

PARTS = ["face_up_face", "face_up_rear_left_lower", "face_up_rear_left_upper",
         "face_up_rear_right_lower", "face_up_rear_right_upper"]
FILES = [name + ".stl" for name in PARTS] + ["face_up_bed_review.png", "face_up_face_preview.png", "face_up_report.json"]
MANIFEST = OUT / "face_up_manifest.json"


def flat_fit(points, planes, xy_limit, height_limit, triangles=None, prefer_contact=False):
    best = None
    for label, normal, offset in planes:
        norm = np.linalg.norm(normal)
        n, d = normal / norm, offset / norm
        touching = points[np.abs(points @ n - d) < .001]
        if len(touching) < 3:
            continue
        a = np.cross(n, [0., 0., 1.])
        if np.linalg.norm(a) < .1:
            a = np.cross(n, [1., 0., 0.])
        a /= np.linalg.norm(a)
        b = np.cross(n, a)
        xy = np.column_stack([points @ a, points @ b])
        xy = xy[ConvexHull(xy).vertices]
        try:
            contact_hull_area = float(ConvexHull(np.column_stack([touching @ a, touching @ b])).volume)
        except Exception:
            continue
        if contact_hull_area < 1:
            continue
        height = float(np.ptp(points @ n))
        def dimensions(angle):
            c, s = math.cos(angle), math.sin(angle)
            return np.ptp(xy @ np.array([[c, s], [-s, c]]), axis=0)
        angles = np.linspace(0, math.pi / 2, 181)
        values = [float(max(dimensions(x))) for x in angles]
        index = int(np.argmin(values))
        result = minimize_scalar(lambda x: float(max(dimensions(x))),
                                 bounds=(angles[max(0, index - 1)], angles[min(len(angles)-1, index + 1)]), method="bounded")
        angle = float(result.x)
        dx, dy = dimensions(angle)
        score = max(dx / xy_limit, dy / xy_limit, height / height_limit)
        c, s = math.cos(angle), math.sin(angle)
        matrix = np.array([c * a - s * b, s * a + c * b, n])
        assert np.allclose(matrix @ matrix.T, np.eye(3)) and np.linalg.det(matrix) > .99999
        candidate = {"bed_face": label, "bed_normal_assembly": n.tolist(), "bed_plane_offset_mm": d,
                     "in_plane_yaw_degrees": math.degrees(angle), "rotation_matrix": matrix.tolist(),
                     "size_xyz_mm": [float(dx), float(dy), height], "envelope_ratio": float(score),
                     "fits": bool(score <= 1), "contact_convex_hull_area_mm2": contact_hull_area}
        if triangles is not None:
            on = np.max(np.abs(triangles @ n - d), axis=1) < .001
            touching_triangles = triangles[on]
            candidate["actual_contact_area_mm2"] = float(np.linalg.norm(np.cross(touching_triangles[:,1]-touching_triangles[:,0],touching_triangles[:,2]-touching_triangles[:,0]),axis=1).sum()/2)
        if prefer_contact:
            rank = (candidate["fits"], candidate.get("actual_contact_area_mm2", 0.) if candidate["fits"] else -score)
            best_rank = None if best is None else (best["fits"], best.get("actual_contact_area_mm2", 0.) if best["fits"] else -best["envelope_ratio"])
            take = best is None or rank > best_rank
        else:
            take = best is None or score < best["envelope_ratio"]
        if take:
            best = candidate
    return best


def audit():
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for name, digest in m["dependencies"].items():
        if sha(ROOT / name) != digest:
            raise ValueError(f"Face-up dependency changed: {name}")
    if set(m["artifacts"]) != set(FILES):
        raise ValueError("Face-up artifact coverage mismatch")
    for name, digest in m["artifacts"].items():
        if sha(OUT / name) != digest:
            raise ValueError(f"Face-up artifact changed: {name}")
    print("PASS: flat-bed face-up reference artifacts and provenance", flush=True)


def self_check():
    cube = np.array([[x, y, z] for x in [0., 20.] for y in [0., 30.] for z in [0., 40.]])
    result = flat_fit(cube, [("bottom", np.array([0.,0.,1.]), 0.)], 210, 220)
    assert result["fits"] and result["bed_face"] == "bottom"
    r = np.array(result["rotation_matrix"])
    assert np.allclose(r @ [0.,0.,1.], [0.,0.,1.])
    assert abs(result["size_xyz_mm"][2] - 40) < 1e-8
    assert result["contact_convex_hull_area_mm2"] == 600
    print("PASS: fixed-cut-normal flat-bed orientation self-check", flush=True)


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
    config_path = DESIGN / "face_up.json"
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    source = ROOT / cfg["source"]
    t = read_stl(source)
    points = t.reshape(-1,3)
    before = mesh_check(t)
    scale_path = DESIGN / cfg["scale_config"]
    scaling = json.loads(scale_path.read_text())
    lateral = np.array(scaling["ear_positive_x"]) - scaling["ear_negative_x"]
    lateral[2] = 0
    lateral /= np.linalg.norm(lateral)
    anterior = np.cross(lateral, [0.,0.,1.])
    pitch = math.radians(cfg["face_pitch_degrees"])
    face_normal = anterior * math.cos(pitch) + np.array([0.,0.,1.]) * math.sin(pitch)
    xy_limit = cfg["printer_volume_mm"][0] - 2 * cfg["xy_margin_per_side_mm"] - cfg["footprint_numerical_reserve_mm"]
    height_limit = cfg["printer_volume_mm"][2]
    hull = ConvexHull(points)
    vertices = points[hull.vertices]
    edges = np.unique(np.sort(np.concatenate([hull.simplices[:,[0,1]],hull.simplices[:,[1,2]],hull.simplices[:,[2,0]]]),axis=1),axis=0)
    a, b = points[edges[:,0]], points[edges[:,1]]
    projection = vertices @ face_normal
    def face_points(offset):
        da, db = a @ face_normal - offset, b @ face_normal - offset
        crossing = da * db < 0
        q = a[crossing] + (b[crossing] - a[crossing]) * (da[crossing] / (da[crossing] - db[crossing]))[:,None]
        return np.concatenate([vertices[projection >= offset], q])
    lo, hi = float(projection.min()), float(projection.max() - 1.)
    print(f"Source: {source}\nOutput: {OUT}\nFinding deepest face plane at pitch {cfg['face_pitch_degrees']} degrees", flush=True)
    while hi - lo > cfg["face_plane_offset_resolution_mm"]:
        middle = (lo + hi) / 2
        f = flat_fit(face_points(middle), [("face_rear_cut",face_normal,middle)], xy_limit, height_limit)
        if f and f["fits"]:
            hi = middle
        else:
            lo = middle
    # Refine against the real non-convex scan surface. A clipped convex hull is
    # conservative and can stop before the actual face section reaches the bed limit.
    def actual_face_fit(offset):
        q = clip(t, face_normal, offset)
        return flat_fit(q.reshape(-1,3), [("face_rear_cut",face_normal,offset)],xy_limit,height_limit)
    while hi - 1 > float(projection.min()) and actual_face_fit(hi - 1)["fits"]:
        hi -= 1
    lo = hi - 1
    while hi - lo > cfg["face_plane_offset_resolution_mm"]:
        middle = (lo + hi) / 2
        if actual_face_fit(middle)["fits"]:
            hi = middle
        else:
            lo = middle
    face_d = hi
    face, _ = capped_cut(t, face_normal, face_d)
    rear, _ = capped_cut(t, -face_normal, -face_d)
    rear_points = rear.reshape(-1,3)
    midline = float((np.min(rear_points @ lateral) + np.max(rear_points @ lateral)) / 2)
    neck_cfg = json.loads((DESIGN / "neck_interface.json").read_text())
    neck_angle, neck_yaw = np.radians([neck_cfg["selected_tilt_degrees"], neck_cfg["selected_plane_yaw_degrees"]])
    neck_n = np.array([math.sin(neck_angle)*math.sin(neck_yaw), -math.sin(neck_angle)*math.cos(neck_yaw), math.cos(neck_angle)])
    factor = scaling["target_ear_span_mm"] / np.linalg.norm(np.array(scaling["ear_positive_x"]) - scaling["ear_negative_x"])
    neck_origin = (np.array(neck_cfg["source_plane_origin"]) + scaling["source_offset"]) * factor
    neck_d = float(neck_n @ neck_origin)
    halves = []
    for side, sign in [("left",-1), ("right",1)]:
        n, d = lateral * sign, midline * sign
        q, _ = capped_cut(rear, n, d)
        planes = [("face_rear_cut", -face_normal, -face_d), ("vertical_midline_cut", n, d), ("neck_cut", neck_n, neck_d)]
        fit = flat_fit(envelope(q,[(n,d) for _,n,d in planes]),planes,xy_limit,height_limit)
        halves.append((side,q,planes,fit))
        print(f"Rear {side} half, cut-flat only: {fit['size_xyz_mm']}, fits={fit['fits']}", flush=True)
    if all(h[3]["fits"] for h in halves):
        raise ValueError("Rear halves already fit; simplify PARTS before exporting unnecessary subdivisions")
    trials = []
    chosen = None
    for z in cfg["rear_height_candidates_mm"]:
        pieces = []
        for side,q,planes,_ in halves:
            for label,sign in [("lower",-1),("upper",1)]:
                n, d = np.array([0.,0.,float(sign)]), z * sign
                # Diagnostic bounds only while choosing height; cap after selection.
                region = clip(q,n,d)
                ps = planes + [("rear_height_cut",n,d)]
                fit = flat_fit(envelope(region,[(n,d) for _,n,d in ps]),ps,xy_limit,height_limit)
                pieces.append((f"face_up_rear_{side}_{label}",q,n,d,ps,fit))
        worst = max(p[-1]["envelope_ratio"] for p in pieces)
        trials.append({"rear_height_mm":z,"all_fit":all(p[-1]["fits"] for p in pieces),"worst_envelope_ratio":worst})
        print(f"Rear height {z}: all fit={trials[-1]['all_fit']}, worst ratio={worst:.4f}",flush=True)
        if trials[-1]["all_fit"] and (chosen is None or worst < chosen[0]):
            chosen=(worst,z,pieces)
    if chosen is None:
        raise ValueError("No rear height split fits with actual cut faces flat; do not introduce free tilt")
    _,rear_z,definitions = chosen
    face_fit=flat_fit(face.reshape(-1,3),[("face_rear_cut",face_normal,face_d)],xy_limit,height_limit)
    export_definitions=[("face_up_face",face,face_fit)]
    for name,q,n,d,planes,_ in definitions:
        actual,_=capped_cut(q,n,d)
        f=flat_fit(actual.reshape(-1,3),planes,xy_limit,height_limit,triangles=actual,prefer_contact=True)
        export_definitions.append((name,actual,f))
    results=[]
    fig,axes=plt.subplots(2,5,figsize=(20,9))
    face_print=None
    for column,(name,q,fit) in enumerate(export_definitions):
        if not fit or not fit["fits"]:
            raise ValueError(f"Final capped candidate fails flat-bed fit: {name}")
        matrix=np.array(fit["rotation_matrix"])
        rotated=q@matrix.T
        translation=np.array([cfg["xy_margin_per_side_mm"],cfg["xy_margin_per_side_mm"],0.])-rotated.min(axis=(0,1))
        posed=rotated+translation
        posed[np.abs(posed[:,:,2])<.0001,2]=0.
        path=OUT/(name+".stl")
        write_stl(path,posed)
        installed=read_stl(path)
        check=mesh_check(installed)
        if any(check[k] for k in ['boundary_edges','nonmanifold_edges','inconsistent_edge_winding']) or check['connected_shells']!=1:
            raise ValueError(f"Topology failed: {name}: {check}")
        bed=np.max(np.abs(installed[:,:,2]),axis=1)<.001
        tt=installed[bed]
        contact=float(np.linalg.norm(np.cross(tt[:,1]-tt[:,0],tt[:,2]-tt[:,0]),axis=1).sum()/2)
        if contact<cfg["minimum_planar_bed_contact_area_mm2"]:
            raise ValueError(f"Insufficient actual planar bed contact: {name}: {contact}")
        if np.any(np.array(check['bounds_mm'])[0]<-.001) or np.any(np.array(check['bounds_mm'])[1]>np.array(cfg['printer_volume_mm'])+.001):
            raise ValueError(f"Installed output exceeds build volume: {name}")
        results.append({"name":path.name,"fit":fit,"installed_mesh":check,"bed_contact_area_mm2":contact,
                        "assembly_to_print_rotation_matrix":matrix.tolist(),"assembly_to_print_translation_mm":translation.tolist(),
                        "assembly_volume_mm3":mesh_check(q)['signed_volume_mm3'],"sha256":sha(path)})
        render(axes[0,column],installed,(0,1),1,name.replace('face_up_',''))
        render(axes[1,column],installed,(0,2),-1,'Side / actual flat bed contact')
        for aa in axes[:,column]:aa.set_xlim(0,220);aa.set_ylim(0,220)
        axes[1,column].axhline(0,color='forestgreen',lw=3)
        if name=='face_up_face':face_print=installed
        print(f"{name}: XYZ {np.round(check['size_xyz_mm'],2).tolist()}, bed={fit['bed_face']}, contact={contact:.1f} mm2",flush=True)
    volume_error=abs(sum(p['assembly_volume_mm3'] for p in results)-before['signed_volume_mm3'])
    if volume_error>max(10.,abs(before['signed_volume_mm3'])*1e-6):raise ValueError('Flat-bed split volume conservation failed')
    fig.suptitle('Face-first intermediate pieces: top views and side views on the 220 mm bed\nEvery piece has a broad actual cut face at Z=0; only in-plane yaw was optimized. No arbitrary tilt or joints.')
    fig.tight_layout();fig.savefig(OUT/'face_up_bed_review.png',dpi=140);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,8))
    render(axes[0],face_print,(0,1),1,'Face pointing upward / top view')
    render(axes[1],face_print,(0,2),-1,'Face rear cut lies on the bed')
    axes[1].axhline(0,color='forestgreen',lw=3)
    fig.tight_layout();fig.savefig(OUT/'face_up_face_preview.png',dpi=140);plt.close(fig)
    report={"scope":cfg['scope'],"source_size_xyz_mm":before['size_xyz_mm'],"printer_volume_mm":cfg['printer_volume_mm'],
            "xy_margin_per_side_mm":cfg['xy_margin_per_side_mm'],"face_pitch_degrees":cfg['face_pitch_degrees'],
            "face_plane_normal":face_normal.tolist(),"face_plane_offset_mm":face_d,"face_thickness_mm":face_fit['size_xyz_mm'][2],
            "face_offset_search_resolution_mm":cfg['face_plane_offset_resolution_mm'],"deepest_face_cut_scope":"At the selected feature-preserving pitch, with fixed cut-face-down orientation and in-plane yaw only; refined using actual triangle/plane intersections to 0.01 mm",
            "rear_bed_face_selection":"Prefer the largest measured actual planar contact area among cut-flat orientations that fit",
            "rear_lateral_normal":lateral.tolist(),"rear_lateral_offset_mm":midline,"unsliced_rear_halves":[{'side':s,'fit':f} for s,_,_,f in halves],
            "rear_height_trials":trials,"selected_rear_height_mm":rear_z,"pieces":results,"volume_recombination_error_mm3":volume_error,
            "supersedes":"The earlier freely tilted three-piece bounding-box layout is rejected as a practical print recommendation",
            "limits":["Five is a demonstrated flat-bed layout, not a mathematical minimum","No dovetails, registration, slicer settings, or strength verification","Face features point upward; local sculpted overhangs may still need supports, unlike support under an entire sloping cut face"]}
    (OUT/'face_up_report.json').write_text(json.dumps(report,indent=2)+'\n')
    deps=[source,config_path,scale_path,DESIGN/'neck_interface.json',Path(__file__),DESIGN/'measure_scale.py',DESIGN/'analyze_splits.py',DESIGN/'export_intermediates.py']
    MANIFEST.write_text(json.dumps({'dependencies':{p.relative_to(ROOT).as_posix():sha(p) for p in deps},'artifacts':{name:sha(OUT/name) for name in FILES}},indent=2)+'\n')
    audit()


if __name__=='__main__':main()
