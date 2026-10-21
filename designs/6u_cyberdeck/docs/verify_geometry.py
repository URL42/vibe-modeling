"""Read installed candidate STLs; independently check topology and joint sections.

No geometry is generated. Run after the normal build audit and full assembly review.
Results go to stdout; retain evidence in docs, never in the artifact directory.
"""
import hashlib
import json
from pathlib import Path
import sys
from collections import defaultdict
from math import cos, sin, pi

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from verify_raspberrypi5_case import Mesh, close, require

OUT = ROOT / "output/6u_cyberdeck"
NAMES = ["leaf_bottom_left", "leaf_bottom_right", "leaf_top_right", "leaf_top_left"]


def transformed(mesh, transform):
    result = Mesh.__new__(Mesh)
    result.path = mesh.path
    result.triangles = [[tuple(transform(v)) for v in tri] for tri in mesh.triangles]
    vertices = [v for tri in result.triangles for v in tri]
    result.bounds = [[f(v[a] for v in vertices) for a in range(3)] for f in (min, max)]
    return result


def merged_intervals(intervals):
    result = []
    for a, b in sorted(intervals):
        if result and a <= result[-1][1] + 0.002:
            result[-1][1] = max(result[-1][1], b)
        else:
            result.append([a, b])
    return result


def main():
    manifest = json.loads((OUT / "build_manifest.json").read_text(encoding="utf-8"))
    cfg = ROOT / manifest["config"]["path"]
    config = json.loads(cfg.read_text(encoding="utf-8"))
    revision = config["revision"]
    report = {"config_sha256": hashlib.sha256(cfg.read_bytes()).hexdigest(),
              "build_manifest_sha256": hashlib.sha256((OUT / "build_manifest.json").read_bytes()).hexdigest(),
              "parts": [], "sections": [], "readiness": "unverified: physical coupon and slicer required"}
    assembled = []
    for i, name in enumerate(NAMES):
        mesh = Mesh(OUT / (name + "_" + revision + ".stl"))
        result = mesh.topology()
        result["name"] = name
        result["sha256"] = hashlib.sha256(mesh.path.read_bytes()).hexdigest()
        require(all(hi - lo <= 210.002 for lo, hi in zip(*mesh.bounds)), "part exceeds reserved 220 mm volume")
        close(mesh.bounds[0][2], 0, "flat rear bed datum")
        close(mesh.bounds[1][2], 80, "height")
        report["parts"].append(result)
        tx = 127 if i in (0, 3) else 0
        tz = 146.95 if i in (0, 1) else 0
        assembled.append(transformed(mesh, lambda p: (p[0]-tx, 80-p[2], p[1]-tz)))

    def section(mesh, axis, fixed, expected, label):
        # Each section is bounded to the station under inspection. The same
        # infinite mesh line can also intersect the second depth station.
        lo, hi = ((-3,18),(-9,9),(0,13.6))[axis]
        actual = [(max(a,lo),min(b,hi)) for a,b in mesh.intervals(axis, fixed)
                  if min(b,hi)-max(a,lo)>0.001]
        require(len(actual) == len(expected), f"{label}: {actual} != {expected}")
        for pair, target in zip(actual, expected):
            for a, b in zip(pair, target):
                close(a, b, label)
        report["sections"].append({"label": label, "axis": axis, "fixed": fixed, "solid_intervals": actual})

    station_owners = [(3,2),(3,2),(0,1),(0,1),(0,3),(0,3),(1,2),(1,2)]
    for index, (tongue, receiver) in enumerate(station_owners):
        ribbon = index // 2
        depth = (config.get("side_front_station_y",18) if ribbon>=2 else 18) if index % 2 == 0 else 71
        def local(p):
            x, y, z = p
            if ribbon == 0: return (x, y-depth, 146.95-z)
            if ribbon == 1: return (x, y-depth, z+146.95)
            if ribbon == 2: return (z, y-depth, x+127)
            return (z, y-depth, 127-x)
        t = transformed(assembled[tongue], local)
        r = transformed(assembled[receiver], local)
        prefix = f"station {index}: "
        section(t, 2, (8, 2.5), [(3.8,6.8)], prefix+"tongue thickness at washer bearing")
        section(r, 2, (8, 2.5), [(6.8,10.8)], prefix+"receiver bearing wall below nut")
        section(t, 1, (8, 5), [(-5,-1.8),(1.8,5)], prefix+"tongue bore side ligaments")
        section(r, 1, (8, 5), [(-9,-6),(6,9)], prefix+"socket side shoulders")
        section(r, 0, (0, 5), [(15,18)], prefix+"socket closed end")
        # Root is inspected at start/mid/end of its 3 mm insertion-direction overlap.
        for u in (-2.9,-1.5,-0.1):
            section(t, 2, (u,0), [(0,13.6)], prefix+f"root overlap section u={u}")
        section(t, 2, (8,0), [], prefix+"tongue through bore")
        section(r, 2, (8,0), [], prefix+"receiver through bore and nut opening")

    # Both rack columns, every row: confirm front clearance and 3 mm nut floor
    # independently of any material farther back in the enclosure.
    for sign in (-1,1):
        for row in range(18):
            z = -127 + (row//3)*44.45 + (0,15.875,31.75)[row%3]
            owner = (0 if sign<0 else 1) if z<0 else (3 if sign<0 else 2)
            mesh = assembled[owner]
            axis = sign*118.2625
            hits = mesh.intervals(1,(axis,z))
            require(not any(a<5.799 and b>0.001 for a,b in hits), f"rack bore obstructed {sign}/{row}")
            # A point outside the round bore and inside the hex pocket.
            hits = mesh.intervals(1,(axis+2.2,z+0.11))
            front = [(a,b) for a,b in hits if a<5.8]
            require(len(front)==1, f"rack floor missing {sign}/{row}: {hits}")
            close(front[0][0],0,"rack floor exterior")
            close(front[0][1],3,"rack floor remaining thickness")
    report["rack_bores_checked"] = 36

    # This is deliberately deeper than the front bore/floor check above.
    # Sample the full declared service cylinder at center and concentric rings;
    # source bounds independently prove that side pads begin beyond its Y end.
    access_lines = 0
    for sign in (-1,1):
        for row in range(18):
            z = -127 + (row//3)*44.45 + (0,15.875,31.75)[row%3]
            owner = (0 if sign<0 else 1) if z<0 else (3 if sign<0 else 2)
            for radius in (0,2,4):
                for angle in range(16 if radius else 1):
                    x = sign*118.2625+radius*cos(angle*pi/8)
                    zz = z+radius*sin(angle*pi/8)
                    hits = assembled[owner].intervals(1,(x,zz))
                    require(not any(a < config['rail_service_end_y']-0.002 and b > 5.802 for a,b in hits),
                            f"rail service cylinder obstructed at {sign}/{row}, offset radius {radius}: {hits}")
                    access_lines += 1
    report["rail_service"] = {"diameter_mm":8,"y_interval_mm":[5.8,config['rail_service_end_y']],
                              "mesh_axis_lines":access_lines,"side_pad_front_y_mm":config['side_front_station_y']-9,
                              "side_pad_reserve_mm":config['side_front_station_y']-9-config['rail_service_end_y']}

    bridge = Mesh(OUT / ("rear_center_bridge_"+revision+".stl"))
    bridge_info = bridge.topology()
    bridge_info["name"] = "rear_center_bridge"
    bridge_info["sha256"] = hashlib.sha256(bridge.path.read_bytes()).hexdigest()
    for actual,expected in zip(bridge.bounds,((0,0,0),(48,48,3))):
        for a,b in zip(actual,expected):close(a,b,"bridge print bounds")
    bridge_world = transformed(bridge,lambda p:(p[0]-24,70.2+p[2],24-p[1]))
    report["parts"].append(bridge_info)

    def world_section(mesh,axis,fixed,expected,label,window=None):
        actual = mesh.intervals(axis,fixed)
        if window is not None:
            lo,hi=window
            actual=[(max(a,lo),min(b,hi)) for a,b in actual if min(b,hi)-max(a,lo)>0.001]
        require(len(actual)==len(expected),f"{label}: {actual} != {expected}")
        for pair,target in zip(actual,expected):
            for a,b in zip(pair,target):close(a,b,label)
        report["sections"].append({"label":label,"axis":axis,"fixed":fixed,"window":window,"solid_intervals":actual})

    for index,(sx,sz) in enumerate(((-1,-1),(1,-1),(1,1),(-1,1))):
        x,z=sx*12,sz*12
        # Radial offset outside the round passage but inside the hex pocket.
        world_section(bridge_world,1,(x+2.5,z+0.11),[(70.2,73.2)],f"rear clamp {index}: 3 mm bridge bearing")
        world_section(assembled[index],1,(x+2.5,z+0.11),[(73.2,77.2)],f"rear clamp {index}: 4 mm pad bearing web")
        world_section(assembled[index],1,(x+5*sz,z+5*sz),[(73.2,80)],f"rear clamp {index}: pad/rear skin continuous")
        world_section(bridge_world,1,(x,z),[],f"rear clamp {index}: bridge through passage")
        world_section(assembled[index],1,(x,z),[],f"rear clamp {index}: pad/nut through passage")
        world_section(assembled[index],0,(75.2,z),[(x-7,x-1.8),(x+1.8,x+7)],
                      f"rear clamp {index}: pad bore side ligaments",(x-7,x+7))
        nut_radius=5.9/cos(pi/6)/2
        world_section(assembled[index],0,(78.5,z),[(x-7,x-nut_radius),(x+nut_radius,x+7)],
                      f"rear clamp {index}: conservative nut-pocket edge lands",(x-7,x+7))
        for angle in range(16):
            xx=x+2*cos(angle*pi/8);zz=z+2*sin(angle*pi/8)
            hits=assembled[index].intervals(1,(xx,zz))
            require(not any(a<66.7 and b>16.7 for a,b in hits),f"rear driver path obstructed {index}: {hits}")
    world_section(bridge_world,0,(71.7,0),[(-24,24)],"rear bridge spans X center seam")
    world_section(bridge_world,2,(0,71.7),[(-24,24)],"rear bridge spans Z center seam")
    world_section(bridge_world,0,(71.7,12),[(-24,-13.8),(-10.2,10.2),(13.8,24)],"rear bridge bore-to-edge and bore-to-bore widths")
    insertion_lines=0
    for x in (-23.9,-0.13,0.13,23.9):
        for z in (-23.9,-0.13,0.13,23.9):
            owner=(0 if x<0 else 1) if z<0 else (3 if x<0 else 2)
            hits=assembled[owner].intervals(1,(x,z))
            require(not any(a<73.198 and b>0.002 for a,b in hits),f"rear bridge insertion path obstructed: {hits}")
            insertion_lines+=1
    report["rear_access"]={"driver_diameter_mm":4,"driver_y_interval_mm":[16.7,66.7],
                           "driver_lines":64,"plate_sweep_xy_cross_section_xz_mm":[[-24,24],[-24,24]],
                           "plate_insertion_mesh_lines":insertion_lines}
    report["rear_clamps_checked"] = 4
    report["rear_screw_stack_mm"] = {"plate":3,"washer":0.5,"bearing_web":4,"nut":2.4,
                                    "screw_length":10,"tip_y":79.7,"exterior_reserve":0.3}

    coupon_path = OUT / "seam_station_coupon.stl"
    require(coupon_path.exists(), "production-derived coupon export missing")
    coupon = Mesh(coupon_path)
    edges = defaultdict(list)
    for i,tri in enumerate(coupon.triangles):
        for j in range(3):
            edges[tuple(sorted((tri[j],tri[(j+1)%3])))].append(i)
    require(all(len(v)==2 for v in edges.values()), "coupon has nonmanifold/open edges")
    neighbors = defaultdict(set)
    for a,b in edges.values():
        neighbors[a].add(b); neighbors[b].add(a)
    unseen = set(range(len(coupon.triangles)))
    islands = []
    while unseen:
        todo = [unseen.pop()]; island = []
        while todo:
            i = todo.pop(); island.append(i)
            for j in neighbors[i]:
                if j in unseen: unseen.remove(j); todo.append(j)
        islands.append(island)
    require(len(islands)==2, f"coupon must have exactly two intentional pieces, got {len(islands)}")
    report["coupon_connected_pieces"] = len(islands)
    coupon_t = transformed(coupon,lambda p:(p[0]-3,9-p[2],p[1]))
    coupon_r = transformed(coupon,lambda p:(p[0]-31,9-p[2],p[1]))
    section(coupon_t,2,(8,2.5),[(3.8,6.8)],"coupon tongue matches production bearing")
    section(coupon_r,2,(8,2.5),[(6.8,10.8)],"coupon receiver matches production bearing")
    section(coupon_r,1,(8,5),[(-9,-6),(6,9)],"coupon socket matches production shoulders")

    master_path = OUT / "cyberdeck_6u_unsplit_master.stl"
    require(master_path.exists(), "full assembly review must install the independent master before final verification")
    if master_path.exists():
        master = Mesh(master_path)
        master_info = master.topology()
        # The source master represents the case, not its separate fastening plate.
        volume = sum(p["signed_volume_mm3"] for p in report["parts"][:4])
        delta = abs(volume-master_info["signed_volume_mm3"])
        require(delta < 0.1, f"split/master volume mismatch {delta}")
        report["split_master_volume_difference_mm3"] = delta
        comparisons = 0
        maximum_boundary_delta = 0
        # Independently translated ASCII STLs round coordinates differently.
        # Near-tangent section rays amplify that rounding: measured maximum
        # 0.002415 mm. This comparison allowance does not change material minima,
        # the 0.002 mm dimension checks above, fit clearances or Boolean epsilon.
        comparison_tolerance = 0.005
        # Independent recombination checks across all split planes, walls and stations.
        for y in (1.1,4.1,10.1,18.13,40.1,71.13,78.1):
            for z in (-145.4,-140.13,-134.8,-127.1,-8.13,-0.13,0.13,8.13,127.1,134.8,140.13,145.4):
                actual = merged_intervals([p for m in assembled for p in m.intervals(0,(y,z))])
                expected = master.intervals(0,(y,z))
                require(len(actual)==len(expected), f"recombination section mismatch y={y},z={z}: {actual} vs {expected}")
                for a,b in zip(actual,expected):
                    for v,w in zip(a,b):
                        difference = abs(v-w)
                        maximum_boundary_delta = max(maximum_boundary_delta,difference)
                        require(difference <= comparison_tolerance,
                                f"recombination boundary differs by {difference} mm")
                comparisons += 1
        report["recombination_sections_checked"] = comparisons
        report["recombination_boundary_tolerance_mm"] = comparison_tolerance
        report["maximum_recombination_boundary_difference_mm"] = maximum_boundary_delta
        report["unsplit_master"] = master_info
    report["result"] = "PASS: measured digital checks only"
    print(json.dumps(report,indent=2))


if __name__ == "__main__":
    main()
