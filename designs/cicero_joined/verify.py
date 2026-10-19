"""Verify actual integral features, seats, local travel and installed print poses."""
import sys
import json
import subprocess
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))
from build_geometry import md,sha,read_stl,mesh_check,write_json,frame_prism


def as_solid(t):
    v,ids=np.unique(t.reshape(-1,3),axis=0,return_inverse=True)
    return md.Manifold(md.Mesh64(v.astype(np.float64),ids.reshape(-1,3).astype(np.uint64),tolerance=1e-6))


def ray_data(triangles):
    ray=np.array([1.,.371,.217]);e1=triangles[:,1]-triangles[:,0];e2=triangles[:,2]-triangles[:,0]
    h=np.cross(np.broadcast_to(ray,e2.shape),e2);det=np.einsum('ij,ij->i',e1,h)
    inverse=np.zeros_like(det);valid=np.abs(det)>1e-10;inverse[valid]=1/det[valid]
    return triangles[:,0],e1,e2,h,inverse,valid,ray


def inside(data,point):
    origin,e1,e2,h,inverse,valid,ray=data
    s=point-origin;u=inverse*np.einsum('ij,ij->i',s,h);q=np.cross(s,e1)
    v=inverse*(q@ray);distance=inverse*np.einsum('ij,ij->i',e2,q)
    hit=valid&(u>=-1e-9)&(v>=-1e-9)&(u+v<=1+1e-9)&(distance>1e-7)
    # Count a triangulated planar face once if the ray happens to hit a shared edge.
    return len(np.unique(np.round(distance[hit],6)))%2==1


def exclude_contact(solid,normal,offset,relief=.02):
    # Diagnostic exclusion only, not a gap added to the manufactured geometry.
    return solid.trim_by_plane(normal,offset+relief)+solid.trim_by_plane(-normal,-offset+relief)


def assembly_samples(solids,data):
    stages=[]
    def stage(name,moving,fixed):stages.append((name,set(moving),set(fixed)))
    stage('head_lower_pair',['h_right_lower'],['h_left_lower'])
    stage('head_upper_pair',['h_right_upper'],['h_left_upper'])
    stage('head_lower_to_collar',['h_left_lower','h_right_lower'],['h_neck'])
    stage('head_upper_to_lower',['h_left_upper','h_right_upper'],['h_neck','h_left_lower','h_right_lower'])
    stage('head_face',['h_face'],[n for n in solids if n.startswith('h_') and n!='h_face'])
    for level,order in [('lower',['lf','rf','lb','rb']),('upper',['lf','mf','rf','lb','mb','rb'])]:
        fixed=['b_'+level+'_'+order[0]]
        for suffix in order[1:]:
            name='b_'+level+'_'+suffix;stage('bust_'+level+'_'+suffix,[name],fixed.copy());fixed.append(name)
    lower=[n for n in solids if n.startswith('b_lower_')]
    upper=[n for n in solids if n.startswith('b_upper_')]
    stage('bust_upper_to_lower',upper,lower)
    stage('bust_neck',['b_neck'],lower+upper)
    stage('head_to_complete_bust',[n for n in solids if n.startswith('h_')],[n for n in solids if n.startswith('b_')])
    results=[]
    for name,moving,fixed in stages:
        joints=[j for j in data['joints'] if (j['male'] in moving and j['female'] in fixed) or (j['female'] in moving and j['male'] in fixed)]
        assert joints,(name,'no joint across installation stage')
        direction=np.array(joints[0]['insertion_direction']);travel=joints[0]['travel_mm']
        assert all(np.linalg.norm(np.array(j['insertion_direction'])-direction)<1e-6 and j['travel_mm']==travel for j in joints),(name,'incompatible simultaneous motions')
        normals=[]
        for j in joints:
            # Into the moving owner from the fixed owner, independent of male ownership.
            n=np.array(j['normal_into_female'])*(1 if j['female'] in moving else -1)
            if not any(np.linalg.norm(n-old)<1e-6 for old in normals):normals.append(n)
        A=np.array(normals);approach=A.T@np.linalg.solve(A@A.T,np.full(len(A),10. if name=='head_to_complete_bust' else 8.))
        states=[approach*f-direction*travel for f in [1,.5,0]]+[ -direction*travel*f for f in [.75,.5,.25,0]]
        obstacles={}
        for mn in moving:
            for fn in fixed:
                ob=solids[fn]
                # Exclude only narrow intentional contact slabs, preserving
                # both fixed stock and every protruding male on either side.
                for j in joints:
                    if {mn,fn}!={j['male'],j['female']}:continue
                    n=np.array(j['seam_plane_normal']);d=j['seam_plane_offset_mm']
                    ob=exclude_contact(ob,n,d)
                    w=np.array(j['insertion_direction']);c=np.array(j['center_mm'])
                    sign=1 if j['moving_side']=='male' else -1
                    ob=exclude_contact(ob,w,float(c@w)+sign*j['profile_length_mm']/2)
                obstacles[mn,fn]=ob
        worst=0.;witness=None
        for index,translation in enumerate(states):
            for mn in moving:
                moving_solid=solids[mn].translate(translation)
                for fn in fixed:
                    overlap=(moving_solid^obstacles[mn,fn]).volume()
                    if overlap>worst:worst=overlap;witness=[index,mn,fn,translation.tolist()]
        print('Subassembly installation:',name,'worst mm3',worst,'witness',witness,flush=True)
        results.append(dict(stage=name,moving=sorted(moving),fixed=sorted(fixed),sampled_states=len(states),maximum_interference_mm3=worst,witness=witness))
        assert worst<1,(name,'whole-model installation collision',worst,witness)
    return results


def main():
    assets_only='--assets-only' in sys.argv
    data=json.loads((HERE/'geometry_manifest.json').read_text())
    for path,digest in data['inputs'].items():assert sha(ROOT/path)==digest,('changed geometry input',path)
    for name,digest in data['assets'].items():assert sha(HERE/'assets'/name)==digest,('changed mesh asset',name)
    assert data['connector_only_leaves']==0
    assert len(data['parts'])==17 and len(data['joints'])==33
    out=ROOT/'output/cicero_joined'
    if not assets_only:
        subprocess.run([sys.executable,str(ROOT/'scripts/scad_build_all.py'),'--design','cicero_joined','--config','designs/cicero_joined/configs/rev_0001.json','--audit-only'],cwd=ROOT,check=True)
    solids={};rays={};posed_meshes={};part_checks={};cloud=[]
    for part in data['parts']:
        name=part['name'];asset=read_stl(HERE/'assets'/(name+'.stl'))
        t=asset if assets_only else read_stl(out/(name+'_rev_0001.stl'))
        check=mesh_check(t)
        assert check['connected_shells']==1 and not any(check[k] for k in ['boundary_edges','nonmanifold_edges','inconsistent_edge_winding']),(name,check)
        bounds=np.array(check['bounds_mm'])
        assert np.all(bounds[0]>=-.002) and np.all(bounds[1]<=[215.002,215.002,220.002]),(name,'build volume',bounds)
        on=np.max(np.abs(t[:,:,2]),axis=1)<.002;q=t[on]
        contact=float(np.linalg.norm(np.cross(q[:,1]-q[:,0],q[:,2]-q[:,0]),axis=1).sum()/2)
        assert contact>1000,(name,'no broad actual flat bed contact',contact)
        distances=cKDTree(asset.reshape(-1,3)).query(t.reshape(-1,3))[0]
        reverse=cKDTree(t.reshape(-1,3)).query(asset.reshape(-1,3))[0]
        deviation=max(float(distances.max()),float(reverse.max()))
        assert deviation<.002,(name,'asset/export vertex deviation',deviation)
        r=np.array(part['rotation']);tr=np.array(part['translation'])
        world=(asset-tr)@r
        solids[name]=as_solid(world);rays[name]=ray_data(world);cloud.append(world.reshape(-1,3));posed_meshes[name]=t
        part_checks[name]=dict(size_xyz_mm=check['size_xyz_mm'],bed_area_mm2=contact,shells=check['connected_shells'],maximum_export_vertex_deviation_mm=deviation)
        print('PASS printable:',name,np.round(check['size_xyz_mm'],2).tolist(),'bed',round(contact),flush=True)
    actual={tuple(sorted(contact['parts'])) for contact in data['actual_seam_contacts']}
    # The shallow face's two small cap contours locate the exposed eye regions
    # in an orthonormal face-plane frame. Check backing in the actual exported
    # face, after all connector cuts, rather than only trusting the new plane.
    n=np.array(data['parameters']['face_normal'])
    u=np.cross(n,[0,0,1]);u/=np.linalg.norm(u);w=np.cross(n,u)
    eye_backing=[]
    for center in [[-18.50448747,-422.09609932],[42.68749490,-431.18818001]]:
        points=[u*center[0]+w*center[1]+n*(data['parameters']['face_offset_mm']+depth) for depth in [.5,1.,2.,3.,4.]]
        assert all(inside(rays['h_face'],p) for p in points),('eye backing missing after joint cuts',center)
        eye_backing.append(dict(face_plane_coordinates_mm=center,depth_samples_mm=[.5,1.,2.,3.,4.],result='passed'))
    assert data['parameters']['face_uncut_rear_cap_contours']==1
    print('PASS: uninterrupted rear face cap and solid eye-region backing probes through 4 mm',flush=True)
    declared={tuple(sorted([j['male'],j['female']])) for j in data['joints']}
    assert actual==declared and len(actual)==len(data['joints']),'Missing or duplicate mating-pair joint'
    joint_checks=[]
    for j in data['joints']:
        c=np.array(j['center_mm']);u=np.array(j['profile_u']);v=np.array(j['normal_into_female']);w=np.array(j['insertion_direction'])
        L=j['profile_length_mm'];travel=j['travel_mm'];eng=j['engagement_mm'];throat=j['throat_mm'];flare=j['flare_mm']
        male=solids[j['male']];female=solids[j['female']];male_ray=rays[j['male']];female_ray=rays[j['female']]
        # Independent point-in-exported-solid checks prove the named feature
        # actually exists on each mating model, not merely in an inventory.
        for a in [-throat/4,0,throat/4]:
            for b in [-L/4,0,L/4]:
                p=c+u*a+w*b+v*eng*.5
                assert inside(male_ray,p),(j['id'],'missing integral male',p)
                assert not inside(female_ray,p),(j['id'],'missing receiver void',p)
                assert inside(male_ray,c+u*a+w*b-v*3),(j['id'],'missing root stock')
        male_moves=j['moving_side']=='male'
        stop_sign=1 if male_moves else -1
        stop=c+w*(stop_sign*(L/2+1.5))+v*eng*.5
        assert inside(female_ray,stop),(j['id'],'missing closed seat/stop')
        assert j['gravity_drop_mm']>0,(j['id'],'no downhill seating travel')
        profile=[[-throat/2,-6],[throat/2,-6],[throat/2,0],[flare/2,eng],[-flare/2,eng],[-throat/2,0]]
        probe=frame_prism(profile,L,c-w*L/2,u,v,w).trim_by_plane(v,float(c@v)+.02)
        obstacle=exclude_contact(female,w,float(c@w)+stop_sign*L/2)
        worst=0.;states=0
        sign=-1 if male_moves else 1
        # Test normal loading with both signs of the diagonal approach allowance
        # used by corner leaves, then the downward sliding seating stroke.
        for tangent in sorted(set([-j['loading_pocket_tangential_allowance_mm'],0,j['loading_pocket_tangential_allowance_mm']])):
            for fraction in [1,.75,.5,.25,0]:
                translation=-v*10*fraction+w*(sign*travel)+u*tangent*fraction
                worst=max(worst,(probe.translate(translation)^obstacle).volume());states+=1
        for fraction in [.8,.6,.4,.2,0]:
            translation=w*(sign*travel*fraction)
            worst=max(worst,(probe.translate(translation)^obstacle).volume());states+=1
        assert worst<.1,(j['id'],'connector installation collision mm3',worst)
        joint_checks.append(dict(id=j['id'],male=j['male'],female=j['female'],feature_presence='passed',closed_stop='passed',gravity_drop_mm=j['gravity_drop_mm'],sampled_connector_states=states,maximum_probe_interference_mm3=worst))
        print('PASS integral mating pair:',j['id'],'closed stop, presence, downhill travel; collision mm3',round(worst,6),flush=True)
    major=[j for j in data['joints'] if j['id']=='head_to_bust']
    assert len(major)==1 and {major[0]['male'],major[0]['female']}=={'h_neck','b_neck'}
    group_checks=assembly_samples(solids,data)
    scaling=json.loads((ROOT/'designs/cicero/configs/rev_0001.json').read_text())
    aa=np.array(scaling['ear_negative_x']);bb=np.array(scaling['ear_positive_x']);factor=228.6/np.linalg.norm(bb-aa)
    expected=(np.array([aa,bb])+scaling['source_offset'])*factor
    cloud=np.concatenate(cloud);distances,ids=cKDTree(cloud).query(expected)
    ear_span=float(np.linalg.norm(cloud[ids[1]]-cloud[ids[0]]))
    assert max(distances)<.003 and abs(ear_span-228.6)<.004,('ear span',ear_span,distances)
    print('PASS: 33/33 actual mating pairs have integral features and closed seats; single neck connection; ear span',ear_span,flush=True)
    if not assets_only:
        result=dict(config='designs/cicero_joined/configs/rev_0001.json',verification_script_sha256=sha(Path(__file__)),geometry_manifest_sha256=sha(HERE/'geometry_manifest.json'),build_manifest_sha256=sha(out/'build_manifest.json'),
                    parts=part_checks,joints=joint_checks,subassembly_installation_samples=group_checks,eye_backing_samples=eye_backing,actual_seams=len(actual),covered_seams=len(declared),connector_only_leaves=0,head_to_bust_connections=1,ear_span_mm=ear_span,
                    diagnostic_contact_exclusion_mm=.02,full_subassembly_swept_paths='unverified',physical_fit='unverified',structural_load_capacity='unverified',global_minimum_material_width='unverified')
        write_json(HERE/'verification.json',result)


if __name__=='__main__':main()
