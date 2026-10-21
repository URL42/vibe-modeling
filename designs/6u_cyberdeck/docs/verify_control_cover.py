"""Measure installed rev_0003 cover meshes; run after complete assembly review."""
import hashlib
import json
from math import hypot, cos, sin, pi
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT/'scripts'))
from verify_raspberrypi5_case import Mesh, require, close

OUT = ROOT/'output/6u_cyberdeck'


def main():
    manifest = json.loads((OUT/'build_manifest.json').read_text())
    cp = ROOT/manifest['config']['path']
    cfg = json.loads(cp.read_text())
    rev = cfg['revision']
    report = {'config':str(cp.relative_to(ROOT)),
              'verification_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'config_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),
              'build_manifest_sha256':hashlib.sha256((OUT/'build_manifest.json').read_bytes()).hexdigest(),
              'parts':[], 'sections':[], 'case_regression':{}}
    baseline=json.loads((Path(__file__).parent/'rev_0003_case_baseline.json').read_text())
    old_measurements=json.loads((Path(__file__).parent/'rev_0002_geometry_measurements.json').read_text())
    for name,digest in baseline.items():
        file=OUT/name.replace('.stl','_'+rev+'.stl')
        actual=hashlib.sha256(file.read_bytes()).hexdigest()
        before=next(p for p in old_measurements['parts'] if p['name']+'.stl'==name)
        info=Mesh(file).topology()
        require(info['triangles']==before['triangles'],'case triangle-count regression: '+name)
        require(info['bounds_mm']==before['bounds_mm'],'case bounds regression: '+name)
        require(abs(info['signed_volume_mm3']-before['signed_volume_mm3'])<0.000001,'case volume regression: '+name)
        # OpenSCAD CGAL may reorder ASCII triangle records across identical builds.
        # Artifact hashes remain authoritative per build; compare measured geometry
        # and rerun the independent case section suite rather than equating hashes.
        report['case_regression'][name]={'previous_sha256':digest,'current_sha256':actual,
            'identical_bytes':actual==digest,'triangle_count':info['triangles'],
            'volume_delta_mm3':info['signed_volume_mm3']-before['signed_volume_mm3'],
            'identical_bounds':True}
    height=177.2
    station=height/2-13
    meshes=[]
    for i,name in enumerate(['control_cover_left','control_cover_right']):
        m=Mesh(OUT/(name+'_'+rev+'.stl'))
        info=m.topology()
        info['name']=name
        info['sha256']=hashlib.sha256(m.path.read_bytes()).hexdigest()
        require(all(b-a<=210.002 for a,b in zip(*m.bounds)),'cover exceeds reserved bed')
        close(m.bounds[0][2],0,'face-down bed datum')
        close(m.bounds[1][0]-m.bounds[0][0],141 if i==0 else 127,'cover width with joints')
        close(m.bounds[1][1]-m.bounds[0][1],height,'cover height')
        close(m.bounds[1][2],3 if i==0 else 9.8,'cover print thickness')
        report['parts'].append(info)
        meshes.append(m)

    def sections(i,x,v,expected,label):
        # Local cover X,V,W -> print X+tx,half-V,W.
        found=meshes[i].intervals(2,(x+(127 if i==0 else 0),height/2-v))
        require(len(found)==len(expected),f'{label}: {found} != {expected}')
        for pair,target in zip(found,expected):
            for value,want in zip(pair,target): close(value,want,label)
        report['sections'].append({'label':label,'owner':i+6,'x':x,'v':v,'w_intervals':found})

    buttons=[(-63.5+dx,44.3+dv) for dx in [-20,20] for dv in [-20,20]]
    buttons += [(63.5+dx,44+dv) for dx,dv in [(0,25.5),(25.5,0),(0,-25.5),(-25.5,0)]]
    holes=[(x,v,14) for x,v in buttons]
    for x in [-63.5,63.5]:
        holes.append((x,-44.3,15))
        holes += [(x+dx,-44.3+dv,1.7) for dx in [-40,40] for dv in [-20,20]]
    holes += [(x,v,1.8) for x in [-118.2625,118.2625] for v in [-82.55,82.55]]
    minimum_edge=min(min(127-abs(x)-r,88.6-abs(v)-r,abs(x)-r) for x,v,r in holes)
    minimum_pair=min(hypot(x-a,v-b)-r-s for j,(x,v,r) in enumerate(holes) for a,b,s in holes[j+1:])
    require(minimum_edge>=3,'cover edge ligament')
    require(minimum_pair>=3,'cover pair ligament')
    # Center and off-center rays establish all 22 through-holes, surrounding
    # face material and thickness. Independent of source assertions.
    for j,(x,v,r) in enumerate(holes):
        i=int(x>0)
        px=x+(127 if i==0 else 0)
        # Measure both diameters from final STL void boundaries at the bore axis.
        for axis,center,fixed in [(0,px,(height/2-v,1.5)),(1,height/2-v,(px,1.5))]:
            material=meshes[i].intervals(axis,fixed)
            low=max((b for a,b in material if b<center),default=None)
            high=min((a for a,b in material if a>center),default=None)
            require(low is not None and high is not None,'unbounded face hole')
            close(low,center-r,f'hole {j} lower radius')
            close(high,center+r,f'hole {j} upper radius')
        for dx,dv in [(0,0),(r*.5,0),(0,r*.5)]:
            sections(i,x+dx,v+dv,[],f'hole {j} open')
        for dx,dv in [(r+0.4,0),(-r-0.4,0),(0,r+0.4),(0,-r-0.4)]:
            sections(i,x+dx,v+dv,[(0,3)],f'hole {j} surrounding face')
    for sign in [-1,1]:
        v=sign*station
        for dv in [-4.4,0.23,4.4]:
            sections(0,-1.5,v+dv,[(0,3)],'tongue root full overlap')
            sections(0,2,v+dv,[(0,3)],'tongue midpoint')
            sections(0,13.5,v+dv,[(0,3)],'tongue end')
        sections(0,8,v,[],'tongue screw bore')
        sections(1,8,v,[],'receiver screw bore')
        sections(1,8,v+2.3,[(3,7)],'receiver 4 mm clamp web')
        for dv in [-7.5,7.5]:
            for x in [0.4,8.1,17.5]:
                sections(1,x,v+dv,[(0,9.8)],'receiver shoulder and face overlap')
        sections(1,16.5,v+0.2,[(0,9.8)],'receiver closed end')
        # Distinct solids mate at W=3 with X=14 insertion, 1 mm lateral and tip gap.
        sections(1,14.5,v+0.2,[(3,9.8)],'closed socket tip clearance')
        sections(1,8,v+5.5,[(3,9.8)],'socket side clearance')
    # Spanning panel sections across both supports and cutouts. No residual strip
    # on sampled completed sections may fall below the 3 mm material minimum.
    line_count=0
    for i,m in enumerate(meshes):
        for v in [-85,-82.55,-77,-75.6,-70,-64.3,-44.3,-24.3,0,18.5,24.3,44.3,64.3,69.5,75.6,82.55,85]:
            intervals=m.intervals(0,(height/2-v,1.5))
            require(all(b-a>=2.998 for a,b in intervals),f'narrow panel strip owner {i+6}, v={v}: {intervals}')
            line_count+=1
    # Independently specified full-width analytical master, including intentional
    # socket gaps. Compare recombined leaves at four depths and reject duplicated
    # ownership. This also catches mirrored print/install quadrant mistakes.
    stations=[-station,station]
    sample_x=[-123+6.9*i for i in range(37)]+[-2,0.4,4,8,13.5,14.5,15.5,17.5,19]
    sample_v=[-86+6.7*i for i in range(26)]+[86]
    sample_v += [s+d for s in stations for d in [-10,-8.8,-7.5,-5.5,-4.4,-2.3,0.2,2.3,4.4,5.5,7.5,8.8,10]]
    master_samples=0
    for x in sample_x:
        for v in sample_v:
            if abs(x)>127 or abs(v)>88.6: continue
            if any(abs(x-a)<0.001 for a in [0,14,15,18]): continue
            if any(abs(abs(v-s)-a)<0.001 for s in stations for a in [5,6,9]): continue
            # Avoid polygon chord versus circle differences at tangency; the
            # exact bore diameters were checked separately above in both axes.
            if any(abs(hypot(x-a,v-b)-r)<0.03 for a,b,r in holes): continue
            if any(abs(hypot(x-8,v-s)-1.8)<0.03 for s in stations): continue
            intervals=[m.intervals(2,(x+(127 if i==0 else 0),88.6-v)) for i,m in enumerate(meshes)]
            require(all(min(b,d)-max(a,c)<=0.002 for a,b in intervals[0] for c,d in intervals[1]),'cover owners interpenetrate')
            for w in [1.5,3.5,6,8.5]:
                expected=abs(x)<=127 and abs(v)<=88.6 and w<3
                for s in stations:
                    dv=abs(v-s)
                    if 0<=x<=15 and dv<6 and w<3:
                        expected=x<14 and dv<5
                    if 0<=x<=18 and dv<9 and w>=3:
                        expected=True
                        if w>=7:
                            in_hex=all((x-8)*cos((30+60*k)*pi/180)+(v-s)*sin((30+60*k)*pi/180)<2.95 for k in range(6))
                            if in_hex: expected=False
                    if hypot(x-8,v-s)<1.8: expected=False
                if any(hypot(x-a,v-b)<r for a,b,r in holes): expected=False
                actual=any(a<w<b for owner in intervals for a,b in owner)
                require(actual==expected,f'cover/master mismatch x={x},v={v},w={w}')
                master_samples+=1
    report.update(through_holes=22,minimum_face_edge_ligament_mm=minimum_edge,
                  minimum_face_cut_pair_ligament_mm=minimum_pair,panel_span_sections=line_count,
                  seam_stations=2,rail_fasteners=4,button_envelope_clearance_mm=25.5*2**0.5-35,
                  analytical_master_samples=master_samples,
                  analytical_depths_mm=[1.5,3.5,6,8.5],
                  analytical_circle_boundary_exclusion_mm=0.03,
                  result='PASS: installed digital geometry only',
                  readiness='unverified: hardware bodies, physical fit, PLA load and slicer layers')
    assembly=Mesh(OUT/'cyberdeck_6u_assembled.stl')
    for actual,want in zip(assembly.bounds,[[-127,-3,-146.95],[127,80,146.95]]):
        for value,target in zip(actual,want): close(value,target,'installed full product bounds')
    for j,(x,v,r) in enumerate(holes):
        z=v-44.45
        line=assembly.intervals(1,(x,z))
        require(all(min(b,0)-max(a,-3)<=0.002 for a,b in line),f'installed hole {j} blocked by product')
        line=assembly.intervals(1,(x+r+0.4,z))
        require(any(a<=-2.998 and b>=-0.002 for a,b in line),f'installed face {j} transformed incorrectly')
    report['installed_product_hole_and_face_rays']=44
    report['assembly_review_manifest_sha256']=hashlib.sha256((OUT/'assembly_review_manifest.json').read_bytes()).hexdigest()
    # Coupon consists of two intentionally separate shells, individually audited.
    coupon=Mesh(OUT/'cover_seam_coupon.stl')
    # Production-derived pieces have an 8 mm gap, left max24/right min32.
    require(coupon.bounds[1][2]<=9.802,'coupon height')
    from collections import defaultdict
    edges=defaultdict(list)
    for i,tri in enumerate(coupon.triangles):
        for j in range(3): edges[tuple(sorted((tri[j],tri[(j+1)%3])))].append(i)
    require(all(len(fs)==2 for fs in edges.values()),'coupon open/nonmanifold')
    adj=defaultdict(set)
    for a,b in edges.values(): adj[a].add(b); adj[b].add(a)
    unseen=set(range(len(coupon.triangles)))
    count=0
    while unseen:
        stack=[unseen.pop()]; count+=1; component=[]
        while stack:
            tri_index=stack.pop(); component.append(coupon.triangles[tri_index])
            for n in adj[tri_index]:
                if n in unseen: unseen.remove(n); stack.append(n)
        leaf=Mesh.__new__(Mesh); leaf.path=coupon.path; leaf.triangles=component
        leaf.bounds=coupon.bounds; leaf.topology()
    require(count==2,'cover coupon must contain two separate printable pieces')
    for x in [25,28,31]:
        require(not coupon.intervals(2,(x,13.2)),'coupon pieces intersect')
    report['coupon_connected_pieces']=count
    report['coupon_sha256']=hashlib.sha256(coupon.path.read_bytes()).hexdigest()
    print(json.dumps(report,indent=2))


if __name__=='__main__': main()
