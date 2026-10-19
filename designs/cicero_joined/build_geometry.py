"""Complete Cicero partition and integral dovetails. No connector-only leaves.

Uses the preserved scaled reference, manifold3d==3.3.2, and the existing mesh
inspection helpers. Generated printable assets feed the normal manifest build.
"""
import sys
import json
from pathlib import Path
import numpy as np
from scipy.spatial.transform import Rotation

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
# Limit only this native-Boolean worker to one allowed CPU. Declare Windows
# HANDLE signatures explicitly; ctypes' default int truncates 64-bit handles.
if sys.platform=='win32':
    import ctypes
    k=ctypes.windll.kernel32
    k.GetCurrentProcess.restype=ctypes.c_void_p
    k.GetProcessAffinityMask.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_size_t),ctypes.POINTER(ctypes.c_size_t)]
    k.SetProcessAffinityMask.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
    pm=ctypes.c_size_t();sm=ctypes.c_size_t();h=k.GetCurrentProcess()
    if k.GetProcessAffinityMask(h,ctypes.byref(pm),ctypes.byref(sm)):
        chosen=pm.value & -pm.value
        assert k.SetProcessAffinityMask(h,chosen),'Cannot isolate Boolean worker CPU'
        print('Boolean worker CPU mask:',chosen,flush=True)
sys.path.insert(0,str(ROOT/'designs/cicero_head'))
from generate import md,manifold,mesh,read_stl,write_stl,mesh_check,flat_fit,sha,write_json,frame_prism,box_frame


def norm(v):
    v=np.array(v,dtype=float)
    return v/np.linalg.norm(v)


def partition():
    head=manifold(read_stl(ROOT/'output/cicero/head_intermediate.stl'))
    base=manifold(read_stl(ROOT/'output/cicero/base_intermediate.stl'))
    base=md.Manifold.batch_boolean(base.decompose(),md.OpType.Add).simplify(.001)
    assert len(base.decompose())==1,'Bust source-shell union failed'
    r=json.loads((ROOT/'designs/cicero/assets/face_up_fit_reference.json').read_text())
    fn=np.array(r['face_plane_normal']);lat=np.array(r['rear_lateral_normal'])
    mid=r['rear_lateral_offset_mm'];nn=norm([0,-.3,1]);nd=291.5062138491311
    # Keep the deeper face plane: advancing it to clear the neck sliced through
    # the eye recesses. Reserve a six-mm neck band on the collar instead.
    fd=float(r['face_plane_offset_mm'])
    face,rear=head.split_by_plane(fn,fd)
    face,face_neck_band=face.split_by_plane(nn,nd+6.)
    q=norm([0,-.15,1]);hz0=360/np.linalg.norm([0,-.15,1]);hz1=460/np.linalg.norm([0,-.15,1])
    rest,collar=rear.split_by_plane(q,hz0)
    collar=(collar+face_neck_band).simplify(.001)
    # Coplanar recombination can emit closed zero-volume sheets. Preserve the
    # one volumetric owner; reject, rather than discard, any real extra island.
    collar_components=collar.decompose()
    volumetric=[c for c in collar_components if abs(c.volume())>1e-8]
    null_volume=sum(abs(c.volume()) for c in collar_components if abs(c.volume())<=1e-8)
    assert len(volumetric)==1 and null_volume<1e-6,('neck band recombination islands',len(volumetric),null_volume)
    collar=volumetric[0]
    right,left=rest.split_by_plane(lat,mid)
    lu,ll=left.split_by_plane(q,hz1);ru,rl=right.split_by_plane(q,hz1)
    pieces=dict(h_face=face,h_neck=collar,h_left_lower=ll,h_right_lower=rl,h_left_upper=lu,h_right_upper=ru)
    bn=nd-20
    band,_=base.split_by_plane(nn,bn)
    neck_candidates=[component for component in band.decompose() if abs(np.max(mesh(component)@nn)-nd)<.01]
    assert len(neck_candidates)==1,'Neck-bearing bust owner must be one connected source component'
    neck=neck_candidates[0]
    # Disconnected shoulder material in this height band belongs to the bust,
    # not to the neck plate. Preserve it instead of silently discarding it.
    body=(base-neck).simplify(.001)
    pieces['b_neck']=neck
    bz=150/np.linalg.norm([0,-.15,1])
    cells={}
    for level,sign in [('lower',-1),('upper',1)]:
        slab=body.trim_by_plane(q*sign,bz*sign)
        columns=[('l',-1000,0),('r',0,1000)] if level=='lower' else [('l',-1000,-109.8),('m',-109.8,109.8),('r',109.8,1000)]
        for col,xlo,xhi in columns:
            for row,ys in [('f',-1),('b',1)]:
                name='b_'+level+'_'+col+row
                pieces[name]=slab.trim_by_plane([1,0,0],xlo).trim_by_plane([-1,0,0],-xhi).trim_by_plane([0,ys,0],0)
                cells[name]=dict(level=level,xlo=xlo,xhi=xhi,row=row,ys=ys)
    edges=[]
    # Each record's normal points from its minus owner into its plus owner.
    def edge(id,minus,plus,n,d,moving,direction,group,tangent=0):
        edges.append(dict(id=id,minus=minus,plus=plus,normal=np.array(n,float),offset=float(d),
                          moving=set(moving),direction=norm(direction),group=group,tangent=tangent))
    down=np.array([0.,0.,-1.])
    fs=norm(down-fn*(down@fn));qs=norm(down-q*(down@q));ns=norm(down-nn*(down@nn))
    for name in ['h_neck','h_left_lower','h_right_lower','h_left_upper','h_right_upper']:
        edge('face__'+name,name,'h_face',fn,fd,['h_face'],fs,'face')
    for side in ['left','right']:
        lower='h_'+side+'_lower';upper='h_'+side+'_upper'
        edge('head_collar__'+side,'h_neck',lower,q,hz0,['h_left_lower','h_right_lower','h_left_upper','h_right_upper'],qs,'head_lower')
        edge('head_height__'+side,lower,upper,q,hz1,['h_left_upper','h_right_upper'],qs,'head_upper')
    for level in ['lower','upper']:
        edge('head_midline__'+level,'h_left_'+level,'h_right_'+level,lat,mid,['h_right_'+level],down,'head_midline_'+level)
    edge('head_to_bust','b_neck','h_neck',nn,nd,[k for k in pieces if k.startswith('h_')],ns,'head_to_bust')
    # Infer every bust adjacency from the exact cell intervals. No seam is
    # omitted merely because its joint would be inconvenient.
    for name,c in cells.items():
        if c['level']=='upper':
            # The neck slab's lower cap is inside the wide central column.
            nnverts=mesh(neck).reshape(-1,3)
            contact=nnverts[np.abs(nnverts@nn-bn)<.002]
            if np.any((contact[:,0]>c['xlo']+.01)&(contact[:,0]<c['xhi']-.01)&(contact[:,1]*c['ys']>.01)):
                edge('bust_neck__'+name,name,'b_neck',nn,bn,['b_neck'],ns,'bust_neck')
        for other,oc in cells.items():
            if name>=other:continue
            if c['level']==oc['level']:
                if c['row']==oc['row'] and abs(c['xhi']-oc['xlo'])<.001:
                    edge('bust_x__'+name+'__'+other,name,other,[1,0,0],c['xhi'],[other],down,'bust_vertical_'+c['level'],8)
                elif c['row']==oc['row'] and abs(oc['xhi']-c['xlo'])<.001:
                    edge('bust_x__'+other+'__'+name,other,name,[1,0,0],oc['xhi'],[name],down,'bust_vertical_'+c['level'],8)
                if c['xlo']==oc['xlo'] and c['xhi']==oc['xhi'] and c['row']!=oc['row']:
                    minus=name if c['row']=='f' else other;plus=other if c['row']=='f' else name
                    edge('bust_y__'+minus+'__'+plus,minus,plus,[0,1,0],0,[plus],down,'bust_vertical_'+c['level'],8)
            elif c['row']==oc['row'] and min(c['xhi'],oc['xhi'])>max(c['xlo'],oc['xlo'])+.01:
                lower=name if c['level']=='lower' else other;upper=other if c['level']=='lower' else name
                edge('bust_height__'+lower+'__'+upper,lower,upper,q,bz,[k for k in cells if cells[k]['level']=='upper'],qs,'bust_height')
    return pieces,edges,dict(face_normal=fn.tolist(),face_offset_mm=fd,ear_lateral=lat.tolist(),midline=mid,
                              height_normal=q.tolist(),neck_normal=nn.tolist(),neck_offset_mm=nd,
                              head_lower_offset_mm=hz0,head_upper_offset_mm=hz1,bust_height_offset_mm=bz,
                              bust_neck_offset_mm=bn,source_base_union_shells=len(base.decompose()),
                              face_neck_reserve_mm=6.,face_depth_increase_mm=31.559798942226173-fd,
                              collar_null_sheet_count=len(collar_components)-1,collar_null_sheet_total_volume_mm3=null_volume)


def same_plane(a,b):
    return np.linalg.norm(a[0]-b[0])<1e-6 and abs(a[1]-b[1])<1e-5


def bed_options(pieces,edges):
    options={}
    for name,solid in pieces.items():
        planes=[]
        for e in edges:
            if name==e['minus']:p=(-e['normal'],-e['offset'])
            elif name==e['plus']:p=(e['normal'],e['offset'])
            else:continue
            if not any(same_plane(p,old) for old in planes):planes.append(p)
        t=mesh(solid);options[name]=[]
        for index,(n,d) in enumerate(planes):
            if np.min(t@n-d)<-.002:continue
            f=flat_fit(t.reshape(-1,3),[(str(index),n,d)],209.95,220,triangles=t)
            if not f or not f['fits'] or f.get('actual_contact_area_mm2',0)<1000:continue
            female_edges=set()
            for e in edges:
                if name==e['minus'] and same_plane((n,d),(-e['normal'],-e['offset'])):female_edges.add(e['id'])
                if name==e['plus'] and same_plane((n,d),(e['normal'],e['offset'])):female_edges.add(e['id'])
            options[name].append(dict(normal=n,offset=d,fit=f,female_edges=female_edges))
        print('Raw flat-bed options:',name,[(np.round(o['normal'],2).tolist(),np.round(o['fit']['size_xyz_mm'],2).tolist()) for o in options[name]],flush=True)
        assert options[name], 'No fitting broad cut face for '+name
    # Choose bed faces jointly: the two sides of one interface cannot both
    # require the female recess. Every chosen face stays free of protrusions.
    order=sorted(pieces,key=lambda name:len(options[name]));chosen={};owners={}
    # Wide central leaves print along X; neither X side may carry a protrusion
    # that would push their 219.6mm print height over the 220mm usable height.
    for e in edges:
        if abs(e['normal'][0])>.999 and e['group'].startswith('bust_vertical'):
            for name in [e['minus'],e['plus']]:
                if name.startswith('b_upper_m'):owners[e['id']]=name
    def search(i):
        if i==len(order):return True
        name=order[i]
        for option in sorted(options[name],key=lambda o:-o['fit']['actual_contact_area_mm2']):
            if any(e in owners and owners[e]!=name for e in option['female_edges']):continue
            chosen[name]=option
            old=owners.copy()
            for e in option['female_edges']:owners[e]=name
            if search(i+1):return True
            owners.clear();owners.update(old)
        chosen.pop(name,None)
        return False
    assert search(0),'No compatible integral-joint bed-face ownership; revise partitions'
    for e in edges:
        female=owners.get(e['id'])
        # Unconstrained joints prefer female on the moving/new subassembly.
        if female is None:female=e['plus'] if e['plus'] in e['moving'] else e['minus']
        e['female']=female;e['male']=e['minus'] if female==e['plus'] else e['plus']
    return chosen


def plane_section(solid,n,d,u,w):
    t=mesh(solid)
    cap=t[np.max(np.abs(t@n-d),axis=1)<.002]
    if not len(cap):return md.CrossSection()
    return md.CrossSection(np.stack([cap@u,cap@w],axis=2).tolist(),md.FillRule.NonZero)


def add_joints(original,edges):
    solids=original.copy();records=[];guards=[]
    # The large neck connection is placed first, then the head interfaces.
    ordered=sorted(edges,key=lambda e:(e['id']!='head_to_bust',not e['id'].startswith('face__'),e['id']))
    for e in ordered:
        major=e['id']=='head_to_bust'
        length,travel,throat,flare,engagement=(32.,34.,24.,32.,8.) if major else (18.,20.,10.,16.,6.)
        if e['id'].startswith('face__'):length,travel,throat,flare,engagement=16.,18.,8.,12.,5.
        # The shoulder rises beside the neck cap. A short loading stroke keeps
        # the continuous neck owner clear of that original exterior surface.
        # Retain the full throat, flare, engagement and root dimensions.
        if e['group']=='bust_neck':length,travel=8.,10.
        root=6.;clearance=.35
        v=e['normal'] if e['male']==e['minus'] else -e['normal']
        d=e['offset'] if e['male']==e['minus'] else -e['offset']
        w=e['direction'];u=np.cross(v,w);u/=np.linalg.norm(u)
        assert abs(v@w)<1e-7 and np.linalg.det(np.column_stack([u,v,w]))>.999
        male_moves=e['male'] in e['moving']
        load_sign=-1 if male_moves else 1
        male_profile=[[-throat/2,-root],[throat/2,-root],[throat/2,0],[flare/2,engagement],[-flare/2,engagement],[-throat/2,0]]
        socket_profile=[[-throat/2-clearance,-.5],[throat/2+clearance,-.5],
                        [throat/2+clearance,0],[flare/2+clearance,engagement+clearance],
                        [-flare/2-clearance,engagement+clearance],[-throat/2-clearance,0]]
        pocket_width=flare+2*clearance+2*e['tangent']
        fw=pocket_width+6.2;fl=length+travel+6.2;shift=load_sign*travel/2
        # Intersect actual opposing planar contact polygons; convex bounding
        # rectangles alone would accept holes or tiny sculpted edge contacts.
        contact=plane_section(original[e['minus']],e['normal'],e['offset'],u,w)^plane_section(original[e['plus']],e['normal'],e['offset'],u,w)
        if contact.is_empty():raise ValueError('Missing actual seam '+e['id'])
        bounds=contact.bounds();umin,wmin,umax,wmax=bounds
        grid=[]
        for a in np.linspace(umin+fw/2,umax-fw/2,37 if e['id'].startswith('face__') else 15):
            for b in np.linspace(wmin+fl/2-shift,wmax-fl/2-shift,43 if e['id'].startswith('face__') else 19):
                rectangle=md.CrossSection.square([fw,fl],True).translate([a,b+shift])
                if (rectangle-contact).area()>.002:continue
                score=((a-(umin+umax)/2)/(umax-umin))**2+((b+shift-(wmin+wmax)/2)/(wmax-wmin))**2
                grid.append((score,a,b))
        found=None;diagnostic=[1e99,None]
        for _,a,b in sorted(grid):
            c=u*a+w*b+v*d
            mg=box_frame(c-v*(root+3.15)/2,u,v,w,[flare+6.2,root+3.05,length+6.2])
            fg=box_frame(c+w*shift+v*(engagement+clearance+3.15)/2,u,v,w,[fw,engagement+clearance+3.05,fl])
            # Insets of 0.05mm avoid exact coplanar-contact degeneracy; they do
            # not change geometry. All other stock margins are at least 3mm.
            merror=(mg-solids[e['male']]).volume()
            if merror>.05:continue
            ferror=(fg-solids[e['female']]).volume()
            if merror+ferror<diagnostic[0]:diagnostic=[merror+ferror,c.tolist()]
            if ferror>.05:continue
            found=(c,mg,fg,merror,ferror);break
        if found is None:
            raise ValueError(f"No 3mm-stock integral dovetail fits seam {e['id']}; contact={contact.area():.1f}, bounds={bounds}, footprint={fw}x{fl}, candidates={len(grid)}, best={diagnostic}")
        c,mg,fg,merror,ferror=found
        male=frame_prism(male_profile,length,c-w*length/2,u,v,w)
        low=-length/2-travel-.3 if male_moves else -length/2
        slot=frame_prism(socket_profile,length+travel+.3,c+w*low,u,v,w)
        pocket=box_frame(c+w*(load_sign*travel)+v*((engagement+clearance-.5)/2),u,v,w,
                         [pocket_width,engagement+clearance+.5,length+.6])
        void=slot+pocket
        solids[e['male']]=solids[e['male']]+male
        solids[e['female']]=solids[e['female']]-void
        guards.append((e['id'],e['male'],e['female'],mg,fg,void))
        record=dict(id=e['id'],male=e['male'],female=e['female'],group=e['group'],
                    center_mm=c.tolist(),normal_into_female=v.tolist(),profile_u=u.tolist(),
                    insertion_direction=w.tolist(),moving_owners=sorted(e['moving']),
                    moving_side='male' if male_moves else 'female',travel_mm=travel,
                    profile_length_mm=length,throat_mm=throat,flare_mm=flare,engagement_mm=engagement,
                    root_overlap_mm=root,clearance_mm=clearance,minimum_stock_margin_mm=3,construction_stock_guard_mm=3.1,
                    loading_pocket_tangential_allowance_mm=e['tangent'],contact_area_mm2=contact.area(),
                    gravity_drop_mm=travel*(-w[2]),stop='closed channel end at lowest installed position',
                    initial_male_guard_error_mm3=merror,initial_female_guard_error_mm3=ferror,
                    seam_plane_normal=e['normal'].tolist(),seam_plane_offset_mm=e['offset'])
        records.append(record)
        print('Integral joint:',e['id'],e['male'],'->',e['female'],'at',np.round(c,1).tolist(),flush=True)
    # Material at creation was checked against the already modified owner.
    # Audit every later subtraction directly against earlier stock guards.
    # This avoids an ill-conditioned coincident Boolean between a socket and
    # its own complement while checking the same algebraic material contract.
    for i,(id,mname,fname,mg,fg,own_void) in enumerate(guards):
        for oid,omale,ofemale,omg,ofg,other_void in guards[i+1:]:
            if ofemale==mname:
                error=(mg^other_void).volume()
                assert error<.05,('later socket damages earlier rail root',id,oid,error)
            if ofemale==fname:
                error=(fg^other_void).volume()
                assert error<.05,('later socket damages earlier stop/wall guard',id,oid,error)
    return solids,records


def audit_seam_coverage(original,edges):
    """Discover opposing cap contacts independently of the edge-name inventory."""
    planes=[]
    for e in edges:
        n=e['normal'];d=e['offset']
        if not any(same_plane((n,d),p) or same_plane((-n,-d),p) for p in planes):planes.append((n,d))
    # The collar's reserved neck band adds a second contact face for the same
    # face/collar mating pair, not a new independently moving seam or loose key.
    planes.append((norm([0,-.3,1]),291.5062138491311+6.))
    actual=set();area_records=[]
    for n,d in planes:
        w=norm(np.cross(n,[1,0,0]) if abs(n[0])<.9 else np.cross(n,[0,1,0]))
        u=np.cross(n,w)
        sections={}
        for name,solid in original.items():
            section=plane_section(solid,n,d,u,w)
            if section.area()>1:sections[name]=section
        names=sorted(sections)
        for i,a in enumerate(names):
            for b in names[i+1:]:
                area=(sections[a]^sections[b]).area()
                if area>1:
                    actual.add(tuple(sorted([a,b])))
                    area_records.append(dict(parts=[a,b],plane_normal=n.tolist(),plane_offset_mm=d,contact_area_mm2=area))
    declared={tuple(sorted([e['minus'],e['plus']])) for e in edges}
    assert actual==declared,('Seam inventory differs from actual contact geometry',actual-declared,declared-actual)
    assert len(edges)==len(declared),'Duplicate interfaces for one mating pair'
    print('PASS: independently discovered',len(actual),'mating pairs, each with one integral joint',flush=True)
    return area_records


def emit(solids,records,beds,parameters,coverage):
    from export_intermediates import indexed,edge_data
    assets=HERE/'assets';parts=[];repairs=[]
    for i,(name,solid) in enumerate(solids.items(),1):
        bed=beds[name];n=bed['normal'];d=bed['offset']
        solid=solid.simplify(.001)
        mm=solid.to_mesh64()
        vertices=np.asarray(mm.vert_properties)[:,:3].copy()
        faces=np.asarray(mm.tri_verts).astype(int)
        assert not len(mm.merge_from_vert),'Unexpected property-vertex aliases; canonicalize before encoding'
        t=vertices[faces]
        assert np.min(t@n-d)>-.002,('protrusion below chosen bed face',name)
        fit=flat_fit(t.reshape(-1,3),[('actual_cut_face',n,d)],209.95,220,triangles=t)
        assert fit and fit['fits'],('joined part no longer fits flat',name,fit)
        assert fit['actual_contact_area_mm2']>1000,(name,'insufficient actual bed contact')
        r=np.array(fit['rotation_matrix']);tr=np.array([5.,5.,0.])-(t@r.T).min(axis=(0,1))
        posed_vertices=vertices@r.T+tr
        _,group,counts=np.unique(posed_vertices.astype(np.float32),axis=0,return_inverse=True,return_counts=True)
        # Preserve Manifold's distinct topological vertex fans when STL's
        # position-only encoding would weld coincident skin sheets. Separate
        # only duplicate fans by 0.004mm; no global mesh healing/removal.
        normals=np.zeros_like(vertices)
        triangle_normals=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0])
        for column in range(3):np.add.at(normals,faces[:,column],triangle_normals)
        for duplicate in np.flatnonzero(counts>1):
            ids=np.flatnonzero(group==duplicate)
            for rank,index in enumerate(ids[1:],1):
                direction=normals[index]@r.T
                if abs(posed_vertices[index,2])<.001:direction[2]=0
                if np.linalg.norm(direction)<1e-10:direction=np.array([1.,.37,0.])
                displacement=norm(direction)*(.004*rank)
                posed_vertices[index]+=displacement
                repairs.append(dict(part=name,assembly_vertex_mm=vertices[index].tolist(),maximum_displacement_mm=float(np.linalg.norm(displacement)),reason='separate coincident topological skin fans for position-only STL encoding'))
        posed=posed_vertices[faces];posed[np.abs(posed[:,:,2])<.0001,2]=0
        path=assets/(name+'.stl');write_stl(path,posed)
        check=mesh_check(read_stl(path))
        assert check['connected_shells']==1 and not any(check[k] for k in ['boundary_edges','nonmanifold_edges','inconsistent_edge_winding']),(name,check)
        parts.append(dict(part_id=i,name=name,fit=fit,mesh=check,rotation=r.tolist(),translation=tr.tolist(),
                          inverse_translation=(-r.T@tr).tolist(),inverse_rotation=Rotation.from_matrix(r.T).as_euler('xyz',degrees=True).tolist()))
        print('Printable:',name,np.round(check['size_xyz_mm'],2).tolist(),'contact',round(fit['actual_contact_area_mm2']),flush=True)
    meshes={}
    for p in parts:
        name=p['name'];r=np.array(p['rotation']);tr=np.array(p['translation'])
        meshes[name]=(read_stl(assets/(name+'.stl'))-tr)@r
    # Before connector recesses, the face's rear cut must be one uninterrupted
    # cap contour: the rejected shallow plane exposed both eye recesses here.
    raw_face=partition()[0]['h_face']
    fn=np.array(parameters['face_normal']);u=norm(np.cross(fn,[0,0,1]));w=np.cross(fn,u)
    contours=plane_section(raw_face,fn,parameters['face_offset_mm'],u,w).to_polygons()
    assert len(contours)==1,('face rear cap exposes sculpted recesses',len(contours))
    parameters['face_uncut_rear_cap_contours']=len(contours)
    references=dict(product_reference=list(meshes),head_reference=[n for n in meshes if n.startswith('h_')],bust_reference=[n for n in meshes if n.startswith('b_')])
    for name,names in references.items():write_stl(assets/(name+'.stl'),np.concatenate([meshes[n] for n in names]))
    exploded=[]
    for name,t in meshes.items():
        centroid=t.reshape(-1,3).mean(0);shift=np.array([centroid[0]*.35,centroid[1]*.35,(centroid[2]-250)*.25])
        if name=='h_face':shift+=np.array(parameters['face_normal'])*90
        if name.startswith('h_'):shift[2]+=80
        exploded.append(t+shift)
    write_stl(assets/'exploded_reference.stl',np.concatenate(exploded))
    for prefix,label in [('h_','head'),('b_','bust')]:
        names=[n for n in meshes if n.startswith(prefix)]
        center=np.concatenate([meshes[n].reshape(-1,3) for n in names]).mean(0)
        separated=[]
        for name in names:
            t=meshes[name];shift=(t.reshape(-1,3).mean(0)-center)*np.array([.7,.7,.5])
            if name=='h_face':shift+=np.array(parameters['face_normal'])*100
            separated.append(t+shift)
        write_stl(assets/(label+'_exploded_reference.stl'),np.concatenate(separated))
    neck_names=['h_neck','b_neck'];write_stl(assets/'neck_reference.stl',np.concatenate([meshes[n] for n in neck_names]))
    write_stl(assets/'head_neck_socket_reference.stl',meshes['h_neck'])
    write_stl(assets/'bust_neck_rail_reference.stl',meshes['b_neck'])
    exposed=[n for n in meshes if n!='h_face'];write_stl(assets/'exposed_reference.stl',np.concatenate([meshes[n] for n in exposed]))
    lines=['// Integral joints only; no connector-only printable leaves.','part_id=1; assembly_view_id=0;',
           'minimum_wall_thickness=3; minimum_structural_overlap=6; minimum_internal_edge_width=3;',
           'assert(minimum_structural_overlap>=minimum_wall_thickness);']
    for p in parts:lines.append(f'if(part_id=={p["part_id"]}) import("../assets/{p["name"]}.stl",convexity=10);')
    refs=['product_reference','exploded_reference','head_reference','bust_reference','neck_reference','exposed_reference','head_neck_socket_reference','bust_neck_rail_reference','head_exploded_reference','bust_exploded_reference']
    lines.append('if(part_id==90) {')
    for i,name in enumerate(refs):lines.append(f' if(assembly_view_id=={i}) import("../assets/{name}.stl",convexity=10);')
    lines.append('}')
    for i,name in enumerate(refs[:1]+refs[2:4],91):lines.append(f'if(part_id=={i}) import("../assets/{name}.stl",convexity=10);')
    (HERE/'src/main.scad').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    write_json(HERE/'parts.json',dict(schema_version=1,parts=[dict(part_id=p['part_id'],name=p['name']) for p in parts]))
    members=lambda prefix:[dict(part_id=p['part_id'],transform=dict(translate=p['inverse_translation'],rotate=p['inverse_rotation'])) for p in parts if p['name'].startswith(prefix)]
    assemblies=[dict(assembly_id='cicero',role='product',members=[dict(assembly_id=a,transform=dict(translate=[0,0,0],rotate=[0,0,0])) for a in ['head','bust']]),
                dict(assembly_id='head',role='head',members=members('h_')),dict(assembly_id='bust',role='bust',members=members('b_'))]
    views=[]
    def view(name,vid,rot):views.append(dict(name=name,projection='o',camera=[0,0,280,*rot,1000],assembly_view=refs[vid],assembly_view_id=vid,show_proxies=False))
    for name,rot in [('front',[90,0,0]),('back',[90,0,180]),('left',[90,0,270]),('right',[90,0,90]),('isometric',[55,0,25]),('top',[0,0,0]),('bottom',[180,0,0])]:view(name,0,rot)
    for name,vid,rot in [('exploded',1,[55,0,25]),('head',2,[55,0,25]),('bust',3,[55,0,25]),('neck_front',4,[55,0,25]),('neck_back',4,[125,0,205]),('exposed',5,[55,0,25]),('head_neck_socket',6,[125,0,205]),('bust_neck_rail',7,[55,0,25])]:view(name,vid,rot)
    for label,vid in [('head',8),('bust',9)]:
        for angle,rot in [('front_left',[55,0,335]),('front_right',[55,0,25]),('back_left',[55,0,205]),('back_right',[55,0,155]),('underside',[125,0,25])]:
            view(label+'_exploded_'+angle,vid,rot)
    interfaces=[dict(interface_id=j['id'],owner_assembly='cicero' if j['id']=='head_to_bust' else ('head' if j['male'].startswith('h_') else 'bust'),type='integral_sliding_dovetail',split_policy='continuous_across_seam',local_frame=dict(translate=j['center_mm'],rotate=[0,0,0]),engages_parts=[j['male'],j['female']]) for j in records]
    write_json(HERE/'assembly.json',dict(schema_version=1,primary_assembly='cicero',review_dispatch_id=90,assemblies=assemblies,interfaces=interfaces,views=views,
        view_sets=dict(compact=['front','back','left','right','isometric','head','bust','neck_front','exposed'],full=[v['name'] for v in views]),
        geometry_exports=[dict(name='cicero_assembled_reference',dispatch_id=91,minimum_span=[437,342,568]),dict(name='head_assembled_reference',dispatch_id=92,minimum_span=[235,253,290]),dict(name='bust_assembled_reference',dispatch_id=93,minimum_span=[437,342,333])]))
    source_files=[Path(__file__),ROOT/'designs/cicero_head/generate.py',ROOT/'designs/cicero/face_up_split.py',ROOT/'designs/cicero/measure_scale.py',ROOT/'designs/cicero/export_intermediates.py',ROOT/'designs/cicero/analyze_splits.py',ROOT/'output/cicero/head_intermediate.stl',ROOT/'output/cicero/base_intermediate.stl',ROOT/'designs/cicero/assets/face_up_fit_reference.json']
    write_json(HERE/'geometry_manifest.json',dict(inputs={p.relative_to(ROOT).as_posix():sha(p) for p in source_files},assets={p.name:sha(p) for p in sorted(assets.glob('*.stl'))},
        parameters=parameters,parts=parts,joints=records,actual_seam_contacts=coverage,local_skin_contact_repairs=repairs,printable_count=len(parts),seam_count=len(records),connector_only_leaves=0,
        verification_status=dict(joint_stock_guards='passed at generation; installed recheck required',structural_strength='unverified',physical_fit='unverified',continuous_sweeps='unverified')))


def main():
    pieces,edges,parameters=partition()
    beds=bed_options(pieces,edges)
    if '--study-only' in sys.argv:
        print('PASS: all raw regions fit; compatible all-integral bed ownership exists')
        for name,bed in beds.items():print('BED:',name,bed['normal'].tolist(),bed['female_edges'])
        return
    coverage=audit_seam_coverage(pieces,edges)
    solids,joints=add_joints(pieces,edges)
    emit(solids,joints,beds,parameters,coverage)
    print('PASS: complete integral geometry and all declared seams; no separate connectors',flush=True)


if __name__=='__main__':main()
