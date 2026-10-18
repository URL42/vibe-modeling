"""Generate joined head assets from the preserved scan; all units are mm.

Requires numpy/scipy/matplotlib and manifold3d==3.3.2 installed under
.tmp/cicero-head-tools-v332. Run from repository root. Asset Booleans precede the
normal OpenSCAD manifest build; they are not a replacement for that build.
"""
import sys
import json
from pathlib import Path
import numpy as np
from scipy.spatial.transform import Rotation

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / '.tmp/cicero-head-tools-v332'))
sys.path.insert(0, str(ROOT / 'designs/cicero'))
if sys.platform=='win32':
    import ctypes
    k=ctypes.windll.kernel32
    pm=ctypes.c_size_t();sm=ctypes.c_size_t();handle=k.GetCurrentProcess()
    if k.GetProcessAffinityMask(handle,ctypes.byref(pm),ctypes.byref(sm)):
        k.SetProcessAffinityMask(handle,ctypes.c_size_t(pm.value & -pm.value))
import manifold3d as md
from measure_scale import read_stl, sha
from export_intermediates import indexed, write_stl, mesh_check
from face_up_split import flat_fit


def mesh(solid):
    m = solid.to_mesh()
    return np.asarray(m.vert_properties)[:, :3][np.asarray(m.tri_verts)].astype(float)


def manifold(t):
    v, f = indexed(t)
    result = md.Manifold(md.Mesh(v.astype(np.float32), f.astype(np.uint32)))
    assert str(result.status()).endswith('NoError'), result.status()
    return result


def frame_prism(polygon, length, origin, u, v, w):
    # u,v,w form a right-handed orthonormal frame.
    matrix = np.column_stack([u, v, w, origin])
    return md.Manifold.extrude(md.CrossSection([polygon]), length).transform(matrix)


def box_frame(center, u, v, w, lengths):
    matrix = np.column_stack([u, v, w, center])
    return md.Manifold.cube(lengths, True).transform(matrix)


def missing(shape, owner):
    return (shape - owner).volume()


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')


def main():
    cfg = json.loads((HERE / 'head_parameters.json').read_text())
    report = json.loads((ROOT / 'output/cicero/face_up_report.json').read_text())
    source = ROOT / 'output/cicero/head_intermediate.stl'
    head = manifold(read_stl(source))
    n = np.array(report['face_plane_normal'])
    d = report['face_plane_offset_mm']
    lateral = np.array(report['rear_lateral_normal'])
    mid = report['rear_lateral_offset_mm']
    down = np.array([0., 0., -1.])
    s = down - n * (down @ n)
    s /= np.linalg.norm(s)
    face, rear = head.split_by_plane(n, d)
    neck_n=np.array([0.,-.3,1.]);neck_n/=np.linalg.norm(neck_n)
    neck_d=291.5062138491311
    face, face_neck_band=face.split_by_plane(neck_n,neck_d+cfg['continuous_neck_band_mm'])
    neck_band=head.trim_by_plane(-neck_n,-neck_d-cfg['continuous_neck_band_mm'])
    rear=(rear+neck_band).simplify(.001)

    z0, z1 = cfg['collar_height_mm'], cfg['upper_split_height_mm']
    remaining, collar = rear.split_by_plane([0, 0, 1], z0)
    right, left = remaining.split_by_plane(lateral, mid)
    lu, ll = left.split_by_plane([0, 0, 1], z1)
    ru, rl = right.split_by_plane([0, 0, 1], z1)
    original = dict(face=face, neck_owner=collar, rear_left_lower=ll,
                    rear_right_lower=rl, rear_left_upper=lu, rear_right_upper=ru)
    solids = original.copy()
    joints = []
    guards = []
    print('Source:', source, 'triangles:', head.num_tri(), flush=True)

    # Face receives five short dovetails through internal loading pockets.
    # The moving FACE descends s relative to the completed rear assembly.
    # Rear males therefore move -s relative to the socket and meet its closed
    # upper end. The stop limits the face at its lowest installed position.
    # u x n = -s (upstream extrusion).
    u = -lateral
    w = np.cross(u, n)
    assert np.dot(w, -s) > .999
    used_lanes = []
    for name in list(original)[1:]:
        own = original[name]
        verts = mesh(own).reshape(-1, 3)
        near = verts[np.abs(verts @ n - d) < .002]
        lo, hi = near @ u, near @ s
        centers = {'neck_owner':[18.98,-86.72,343.26],
                   'rear_left_lower':[4.59,-102.44,389.09],
                   'rear_right_lower':[36.53,-86.42,384.17],
                   'rear_left_upper':[2.10,-120.62,476.35],
                   'rear_right_upper':[59.56,-93.54,476.39]}
        c=np.array(centers[name]);
        if name=='neck_owner':c+=lateral*.75
        c+=n*(d-c@n)
        root = box_frame(c-n*3.025,u,n,w,[20,5.95,30])
        female_guard=box_frame(c+n*5.05+s*12,u,n,w,[22,10,58])
        guard_error=missing(root,own)+missing(female_guard,face)
        if guard_error>1:raise ValueError('Joint placement guard error '+name+str(guard_error))
        used_lanes.append(float(c @ u))
        # Rail root -4..0, 10mm throat, 16mm captured head at depth6.
        poly = [[-5,-4],[5,-4],[5,0],[8,6],[-8,6],[-5,0]]
        male = frame_prism(poly, 24, c-w*12, u,n,w)
        socket_poly = [[-5.3,-.5],[5.3,-.5],[5.3,0],[8.4,6.35],[-8.4,6.35],[-5.3,0]]
        # Socket extends 24mm DOWN from the final male to loading pocket.
        channel = frame_prism(socket_poly, 48.3, c-w*36.3, u,n,w)
        loading = box_frame(c-w*24+n*2.8,u,n,w,[17,7.1,24.6])
        socket = channel + loading
        solids[name] = solids[name] + male
        solids['face'] = solids['face'] - socket
        guards.append((name, root, female_guard))
        joints.append(dict(id='face_'+name, type='loading-pocket sliding dovetail',
                           male=name, female='face', center_mm=c.tolist(),
                           moving='face', insertion_direction=s.tolist(), travel_mm=24,
                           stop='closed socket upper end limits downward face travel',
                           root_overlap_mm=4, engagement_mm=6,
                           retention='24mm reverse lift then normal withdrawal; no separate anti-lift latch yet'))
        print('Face rail:',name,np.round(c,2).tolist(),flush=True)

    # Horizontal divisions use explicit drop-in dovetail-planform mortises.
    # They resist shear/twist, are NOT normal-separation-capturing slide rails.
    # All moving upper leaves descend along the same s as face rails.
    # Upper male is directed down; lower socket has closed bottom seat.
    for lower, upper, height in [('neck_owner','rear_left_lower',z0),
                                 ('neck_owner','rear_right_lower',z0),
                                 ('rear_left_lower','rear_left_upper',z1),
                                 ('rear_right_lower','rear_right_upper',z1)]:
        a,b=original[lower],original[upper]
        up=-s
        x=lateral
        y=np.cross(up,x)
        pts=mesh(b).reshape(-1,3)
        near=pts[np.abs(pts[:,2]-height)<.002]
        best=None
        for xx in np.arange((near@x).min()+15,(near@x).max()-14,6):
            for yy in np.arange((near@y).min()+15,(near@y).max()-14,6):
                # height fixes the remaining coordinate along up.
                c=x*xx+y*yy
                c += up*((height-c[2])/up[2])
                lower_guard=box_frame(c+s*7,x,y,up,[26,26,14])
                upper_guard=box_frame(c-s*5,x,y,up,[26,26,10])
                lower_guard=lower_guard.trim_by_plane([0,0,-1],-height+.05)
                upper_guard=upper_guard.trim_by_plane([0,0,1],height+.05)
                if missing(lower_guard,a)<.1 and missing(upper_guard,b)<.1:
                    best=c;break
            if best is not None:break
        if best is None:raise ValueError('No safe post at '+lower+'/'+upper)
        c=best
        # Trapezoidal planform provides keyed rotation; vertical withdrawal
        # remains possible. Explicitly label this instead of claiming undercut.
        poly=[[-7,-8],[7,-8],[10,8],[-10,8]]
        male=frame_prism(poly,18,c+s*12,x,y,up)
        cp=[[-7.4,-8.4],[7.4,-8.4],[10.5,8.4],[-10.5,8.4]]
        socket=frame_prism(cp,16.8,c+s*12.4,x,y,up)
        solids[upper]=solids[upper]+male
        solids[lower]=solids[lower]-socket
        joints.append(dict(id=lower+'__'+upper,type='drop-in dovetail-planform mortise',
                           male=upper,female=lower,center_mm=c.tolist(),moving=upper,
                           insertion_direction=s.tolist(),travel_mm=12,
                           stop='closed lower socket floor; shoulder bearing',
                           normal_capture=False,retention='gravity only; lift-off remains possible',
                           root_overlap_along_post_mm=6,minimum_normal_root_overlap_mm=4.5,clearance_mm=.4))
        print('Drop-in post:',lower,upper,np.round(c,2).tolist(),flush=True)

    # Midline double-dovetail keys enter from the exposed face seam BEFORE
    # the face is installed. Their axes slope rearward/downward in final pose.
    # Both body halves remain recessed at the chosen midline print faces.
    v=lateral
    key_direction=-n + down*.55
    key_direction-=v*(key_direction@v)
    key_direction/=np.linalg.norm(key_direction)
    ku=np.cross(v,key_direction);ku/=np.linalg.norm(ku)
    for suffix,lname,rname,height in [('lower','rear_left_lower','rear_right_lower',(z0+z1)/2),
                                       ('upper','rear_left_upper','rear_right_upper',495)]:
        # Anchor on intersection of face and lateral planes at chosen Z.
        c=np.linalg.solve(np.array([n,lateral,[0,0,1]]),[d,mid,height])
        # Profile spans both owners across lateral seam; 6mm neck, 12mm flares.
        poly=[[-3,-.1],[-6,-7],[6,-7],[3,-.1],[3,.1],[6,7],[-6,7],[-3,.1]]
        # u=ku,v=lateral,w=key_direction must be RH.
        assert np.linalg.det(np.column_stack([ku,v,key_direction]))>.99
        key=frame_prism(poly,32,c,ku,v,key_direction)
        # Clearance via a cross-section offset in the same profile frame.
        section=md.CrossSection([poly]).offset(.3)
        socket=md.Manifold.extrude(section,32.3).transform(np.column_stack([ku,v,key_direction,c]))
        # Extend entry out through the face-side opening, leaving the rear/down
        # end closed. Root/support guards around socket must stay inside rear.
        entry=md.Manifold.extrude(section,12).transform(np.column_stack([ku,v,key_direction,c-key_direction*12]))
        whole=socket+entry
        rear_guard=box_frame(c+key_direction*18,ku,v,key_direction,[20,22,36])
        rear_guard=rear_guard.trim_by_plane(-n,-d+.05)
        if missing(rear_guard,remaining)>.1:
            raise ValueError('Insufficient material for midline key '+suffix)
        solids[lname]=solids[lname]-whole
        solids[rname]=solids[rname]-whole
        # Clip the front end to the original rear region, keeping the exterior
        # and the face seating plane; key itself is a separate printable leaf.
        key=key.trim_by_plane(-n,-d)
        solids['midline_key_'+suffix]=key
        joints.append(dict(id='midline_'+suffix,type='separate double-dovetail spline',
                           owners=[lname,rname],key='midline_key_'+suffix,
                           insertion_direction=key_direction.tolist(),travel_mm=32,
                           stop='closed rear/down channel end',clearance_mm=.3,
                           retention='entry blocked by subsequently installed face'))
        print('Midline key:',suffix,flush=True)

    # Final actual cut faces: face rear, collar/lower upper caps, upper midline,
    # keys on a prism side. Added protrusions must not change these datums.
    defs={
      'face':[('face_rear',n,d)],
      'neck_owner':[('collar_top',np.array([0.,0.,-1.]),-z0)],
      'rear_left_lower':[('lower_top',np.array([0.,0.,-1.]),-z1)],
      'rear_right_lower':[('lower_top',np.array([0.,0.,-1.]),-z1)],
      'rear_left_upper':[('midline',-lateral,-mid)],
      'rear_right_upper':[('midline',lateral,mid)]}
    parts=[]
    assetdir=HERE/'assets';assetdir.mkdir(exist_ok=True)
    for i,(name,solid) in enumerate(solids.items(),1):
        t=mesh(solid)
        if name.startswith('midline_key'):
            # Use the largest real planar triangle face and test all available
            # prism normals; no free-tilt orientation search.
            normals=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);normals/=np.linalg.norm(normals,axis=1)[:,None]
            planes=[]
            for nn in np.unique(np.round(normals,5),axis=0):
                nn=-nn/np.linalg.norm(nn);dd=float((t.reshape(-1,3)@nn).min())
                planes.append(('key_planar_side',nn,dd))
        else:planes=defs[name]
        fit=flat_fit(t.reshape(-1,3),planes,209.95,220,triangles=t,prefer_contact=True)
        if fit is None or not fit['fits']:
            raise ValueError('Final joined leaf fails broad-cut-flat fit: '+name+': '+str(fit))
        R=np.array(fit['rotation_matrix']);translation=np.array([5.,5.,0.])-(t@R.T).min(axis=(0,1))
        posed=t@R.T+translation
        posed[np.abs(posed[:,:,2])<.0001,2]=0
        write_stl(assetdir/(name+'.stl'),posed)
        check=mesh_check(read_stl(assetdir/(name+'.stl')))
        assert check['connected_shells']==1 and not any(check[k] for k in ['boundary_edges','nonmanifold_edges','inconsistent_edge_winding']),(name,check)
        inverse_translation=-R.T@translation
        euler=Rotation.from_matrix(R.T).as_euler('xyz',degrees=True).tolist()
        parts.append(dict(part_id=i,name=name,fit=fit,mesh=check,
                          assembly_to_print_rotation=R.tolist(),assembly_to_print_translation=translation.tolist(),
                          inverse_translation=inverse_translation.tolist(),inverse_rotation=euler,
                          asset_sha256=sha(assetdir/(name+'.stl'))))
        print('Installed asset:',name,np.round(check['size_xyz_mm'],2),flush=True)
    # Exact pairwise final collisions, excluding intended clearance-separated keys.
    collisions=[]
    # Raw pairwise Booleans at intentional coplanar contacts are numerically
    # unstable on this host. verify.py checks explicit installation states with
    # a declared contact-plane relief instead; do not claim a raw Boolean pass.
    from importlib.metadata import version
    assert version('manifold3d')=='3.3.2','Pinned manifold3d==3.3.2 required'
    inputs=[ROOT/'designs/cicero/measure_scale.py',ROOT/'designs/cicero/export_intermediates.py',ROOT/'designs/cicero/face_up_split.py',ROOT/'designs/cicero/analyze_splits.py',source,ROOT/'output/cicero/face_up_report.json',HERE/'head_parameters.json',Path(__file__)]
    write_json(HERE/'asset_provenance.json',dict(inputs={p.relative_to(ROOT).as_posix():sha(p) for p in inputs},
        assets={('assets/'+p['name']+'.stl'):p['asset_sha256'] for p in parts},parts=parts,joints=joints,
        boolean_backend='manifold3d==3.3.2',raw_coplanar_collision_check='unverified; see installation verification',neck_owner='neck_owner',
        unverified=['physical friction/clearance','anti-lift retention on face/posts','load capacity','slicer supports']))
    write_json(HERE/'parts.json',dict(schema_version=1,parts=[dict(part_id=p['part_id'],name=p['name']) for p in parts]))
    # Non-printable assembly references concatenate the exact printable assets
    # transformed back into assembly coordinates; no Boolean fusion is implied.
    assembled_triangles=[];exploded_triangles=[];rear_triangles=[]
    for p in parts:
        r=np.array(p['assembly_to_print_rotation']);tr=np.array(p['assembly_to_print_translation'])
        tt=(read_stl(assetdir/(p['name']+'.stl'))-tr)@r
        assembled_triangles.append(tt)
        name=p['name']
        if name!='face':rear_triangles.append(tt)
        shift=(n*70 if name=='face' else np.array([0.,0.,-45.]) if name=='neck_owner'
               else -lateral*40 if 'left_lower' in name else lateral*40 if 'right_lower' in name
               else -lateral*40+np.array([0.,0.,45.]) if 'left_upper' in name
               else lateral*40+np.array([0.,0.,45.]) if 'right_upper' in name else n*60)
        exploded_triangles.append(tt+shift)
    for fname,tt in [('assembled_reference',assembled_triangles),('exploded_reference',exploded_triangles),('rear_reference',rear_triangles)]:
        write_stl(assetdir/(fname+'.stl'),np.concatenate(tt))
    provenance=json.loads((HERE/'asset_provenance.json').read_text())
    provenance['assets'].update({('assets/'+fname+'.stl'):sha(assetdir/(fname+'.stl')) for fname in ['assembled_reference','exploded_reference','rear_reference']})
    provenance['reference_meshes']='Non-printable concatenations of printable leaf geometry; intentionally separate components, not a fused production solid.'
    write_json(HERE/'asset_provenance.json',provenance)
    # SCAD assembly dispatch uses the exact inverse printable transform.
    lines=['// Generated from provenance-bound manifold assets.','part_id=1;','assembly_view_id=0;',
           'minimum_wall_thickness=3; minimum_structural_overlap=4; minimum_internal_edge_width=3;',
           'assert(minimum_structural_overlap>=minimum_wall_thickness);',
           'assert(minimum_internal_edge_width>=minimum_wall_thickness);']
    for p in parts:
        i=p['part_id'];name=p['name'];it=p['inverse_translation'];er=p['inverse_rotation']
        lines += [f'module part_{i}() {{ import("../assets/{name}.stl",convexity=10); }}',
                  f'module assembled_{i}() {{ translate({json.dumps(it)}) rotate({json.dumps(er)}) part_{i}(); }}',
                  f'if(part_id=={i}) part_{i}();']
    lines+=['if(part_id==90) {',
            ' if(assembly_view_id==1) import("../assets/exploded_reference.stl",convexity=10);',
            ' else if(assembly_view_id==2) assembled_1();',
            ' else if(assembly_view_id==3) import("../assets/rear_reference.stl",convexity=10);',
            ' else import("../assets/assembled_reference.stl",convexity=10);','}',
            'if(part_id==91) import("../assets/assembled_reference.stl",convexity=10);']
    (HERE/'src/main.scad').write_text('\n'.join(lines)+'\n')
    contract=dict(schema_version=1,primary_assembly='head',review_dispatch_id=90,
        assemblies=[dict(assembly_id='head',role='product',members=[dict(part_id=p['part_id'],transform=dict(translate=p['inverse_translation'],rotate=p['inverse_rotation'])) for p in parts])],
        interfaces=[dict(interface_id=j['id'],owner_assembly='head',type='sliding_joint',split_policy='separate_bridge' if 'key' in j else 'continuous_across_seam',local_frame=dict(translate=[0,0,0],rotate=[0,0,0]),engages_parts=j.get('owners',[j.get('male'),j.get('female')])+([j['key']] if 'key' in j else [])) for j in joints],
        views=[dict(name=name,projection='o',camera=cam,assembly_view='head',assembly_view_id=0,show_proxies=False) for name,cam in [('front',[0,0,430,90,0,0,700]),('back',[0,0,430,90,0,180,700]),('left',[0,0,430,90,0,270,700]),('right',[0,0,430,90,0,90,700]),('isometric',[0,0,430,55,0,25,700])]],
        view_sets=dict(compact=['front','back','left','right','isometric'],full=['front','back','left','right','isometric']),geometry_exports=[dict(name='head_assembled_reference',dispatch_id=91,minimum_span=[235,253,290])])
    extras=[('top',0,[0,0,430,0,0,0,700]),('bottom',0,[0,0,430,180,0,0,700]),('exploded',1,[0,0,430,55,0,25,900]),('face_joint',2,[0,0,430,55,0,205,700]),('rear_joints',3,[0,0,430,55,0,25,700])]
    contract['views'] += [dict(name=nm,projection='o',camera=cam,assembly_view=nm,assembly_view_id=vid,show_proxies=False) for nm,vid,cam in extras]
    contract['view_sets']['full'] += [nm for nm,_,_ in extras]
    write_json(HERE/'assembly.json',contract)
    print('PASS: generated assets, closed single-shell leaves and flat-bed fit; installation verification required',flush=True)


if __name__=='__main__':main()
