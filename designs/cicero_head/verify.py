"""Audit imported dependencies and installed head geometry/installation states."""
import json
import sys
from pathlib import Path
# Isolate this verification process to one allowed CPU before loading the native
# Boolean library. Parallel near-coplanar Boolean queries stalled on this host.
if sys.platform=='win32':
    import ctypes
    k=ctypes.windll.kernel32
    process_mask=ctypes.c_size_t();system_mask=ctypes.c_size_t()
    handle=k.GetCurrentProcess()
    if k.GetProcessAffinityMask(handle,ctypes.byref(process_mask),ctypes.byref(system_mask)):
        chosen=process_mask.value & -process_mask.value
        if k.SetProcessAffinityMask(handle,ctypes.c_size_t(chosen)):
            print('Native verification CPU affinity:',chosen,flush=True)
import numpy as np
from scipy.spatial import cKDTree

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))
from generate import md, mesh, sha, read_stl, mesh_check, write_json

def manifold(t):
    v,ids=np.unique(t.reshape(-1,3),axis=0,return_inverse=True)
    f=ids.reshape(-1,3)
    return md.Manifold(md.Mesh64(v.astype(np.float64),f.astype(np.uint64),tolerance=1e-6))



def main():
    p=json.loads((HERE/'asset_provenance.json').read_text())
    for name,digest in p['inputs'].items():
        assert sha(ROOT/name)==digest,('changed input',name)
    for name,digest in p['assets'].items():
        assert sha(HERE/name)==digest,('changed imported asset',name)
    out=ROOT/'output/cicero_head'
    import subprocess
    subprocess.run([sys.executable,str(ROOT/'scripts/scad_build_all.py'),'--design','cicero_head','--config','designs/cicero_head/configs/rev_0001.json','--audit-only'],cwd=ROOT,check=True)
    solids={};checks={}
    for part in p['parts']:
        name=part['name'];file=out/(name+'_rev_0001.stl')
        t=read_stl(file);check=mesh_check(t)
        assert check['connected_shells']==1 and not any(check[k] for k in ['boundary_edges','nonmanifold_edges','inconsistent_edge_winding']),(name,check)
        bounds=np.array(check['bounds_mm'])
        assert np.all(bounds[0]>=-.002) and np.all(bounds[1]<=[215.002,215.002,220.002]),(name,bounds)
        on=np.max(np.abs(t[:,:,2]),axis=1)<.002
        q=t[on]
        contact=float(np.linalg.norm(np.cross(q[:,1]-q[:,0],q[:,2]-q[:,0]),axis=1).sum()/2)
        assert contact>(10 if name.startswith('midline_key') else 1000),(name,contact)
        r=np.array(part['assembly_to_print_rotation']);tr=np.array(part['assembly_to_print_translation'])
        assembled=(t-tr)@r
        solid=manifold(assembled)
        source=read_stl(HERE/'assets'/(name+'.stl'))
        # OpenSCAD may retriangulate coplanar faces; compare vertex clouds,
        # closure, signed volume and surface area independently.
        asset=manifold((source-tr)@r)
        sv=np.unique(source.reshape(-1,3),axis=0)
        distances=cKDTree(sv).query(t.reshape(-1,3))[0]
        reverse=cKDTree(t.reshape(-1,3)).query(sv)[0]
        nearest=max(float(distances.max()),float(reverse.max()))
        assert nearest<.002 and abs(solid.volume()-asset.volume())<asset.surface_area()*.002 and abs(solid.surface_area()-asset.surface_area())<asset.surface_area()*1e-4,(name,'import/export vertex or integrated surface deviation',nearest)
        solids[name]=asset
        checks[name]=dict(mesh=check,bed_contact_area_mm2=contact,maximum_vertex_deviation_mm=nearest,asset_volume_difference_mm3=abs(solid.volume()-asset.volume()))
        print('PASS installed leaf:',name,np.round(check['size_xyz_mm'],2).tolist(),'bed mm2',round(contact,1),flush=True)
    # Sample motion on source assets independently matched to installed geometry.
    # This is sampled evidence, not a continuous swept-solid proof.
    motions=[]
    sequence=['neck_owner','rear_left_lower','rear_right_lower','rear_left_upper','rear_right_upper','midline_key_lower','midline_key_upper','face']
    fixed=[]
    s=np.array(p['joints'][0]['insertion_direction'])
    n=np.array(json.loads((ROOT/'output/cicero/face_up_report.json').read_text())['face_plane_normal'])
    d=json.loads((ROOT/'output/cicero/face_up_report.json').read_text())['face_plane_offset_mm']
    # Contact-plane relief is a verification-only exclusion of 0.02mm at
    # intentional bearing planes; printed geometry is unchanged. This avoids
    # degenerate native Booleans on coincident contacts, not moving interference.
    lateral=np.array(json.loads((ROOT/'output/cicero/face_up_report.json').read_text())['rear_lateral_normal'])
    mid=json.loads((ROOT/'output/cicero/face_up_report.json').read_text())['rear_lateral_offset_mm']
    obstacles={}
    for name,solid in solids.items():
        ob=solid
        if name.startswith('rear_left'):ob=ob.trim_by_plane(-lateral,-mid+.02)
        if name.startswith('rear_right'):ob=ob.trim_by_plane(lateral,mid+.02)
        if name=='neck_owner':ob=ob.trim_by_plane([0,0,-1],-360+.02)
        if name.endswith('_lower'):ob=ob.trim_by_plane([0,0,-1],-460+.02)
        obstacles[name]=ob
    face_obstacles={name:solid.trim_by_plane(n,d+.02) for name,solid in obstacles.items() if name!='face'}
    neck_normal=np.array([0.,-.3,1.]);neck_normal/=np.linalg.norm(neck_normal)
    face_obstacles['neck_owner']=face_obstacles['neck_owner'].trim_by_plane(-neck_normal,-291.5062138491311-6+.02)
    for name in sequence:
        if name=='neck_owner':fixed.append(name);continue
        if name=='face':
            states=[n*distance-s*24 for distance in np.linspace(8,0,3)]
            states += [-s*distance for distance in np.linspace(24,0,7)]
        elif name.startswith('midline_key'):
            j=next(j for j in p['joints'] if j.get('key')==name)
            direction=np.array(j['insertion_direction'])
            states=[-direction*distance for distance in np.linspace(40,0,6)]
        else:states=[-s*distance for distance in np.linspace(18,0,4)]
        worst=0;witness=None
        for index,translation in enumerate(states):
            moving=solids[name].translate(translation)
            for other in fixed:
                obstacle=face_obstacles[other] if name=='face' else obstacles[other]
                overlap=(moving^obstacle).volume()
                if overlap>worst:worst=overlap;witness=[index,other,translation.tolist()]
            if name=='face': print('Face motion sample',index,'of',len(states),'worst mm3',worst,flush=True)
        motions.append(dict(moving=name,samples=len(states),worst_overlap_mm3=worst,witness=witness))
        print('Installation samples:',name,'worst overlap mm3',worst,'witness',witness,flush=True)
        fixed.append(name)
    # Verify preserved neck surface vertices without a near-coincident Boolean
    # between serialized meshes. Such Booleans are numerically ill-conditioned.
    master_t=read_stl(ROOT/'output/cicero/head_intermediate.stl')
    normal=np.array([0.,-.3,1.]);normal/=np.linalg.norm(normal)
    offset=291.5062138491311
    cap=master_t[np.max(np.abs(master_t@normal-offset),axis=1)<.002]
    neck_triangles=mesh(solids['neck_owner'])
    neck_cap=neck_triangles[np.max(np.abs(neck_triangles@normal-offset),axis=1)<.002]
    u=np.array([1.,0.,0.]);v=np.cross(normal,u)
    def cap_section(triangles):
        projected=np.stack([triangles@u,triangles@v],axis=2)
        return md.CrossSection(projected.tolist(),md.FillRule.NonZero)
    before=cap_section(cap);after=cap_section(neck_cap)
    neck_error=(before-after).area()+(after-before).area()
    print('Neck cap symmetric area difference mm2:',neck_error,'source area mm2:',before.area(),flush=True)
    assert neck_error<.1,('neck interface changed',neck_error)
    scaling=json.loads((ROOT/'designs/cicero/configs/rev_0001.json').read_text())
    aa=np.array(scaling['ear_negative_x']);bb=np.array(scaling['ear_positive_x'])
    factor=scaling['target_ear_span_mm']/np.linalg.norm(bb-aa)
    expected=(np.array([aa,bb])+scaling['source_offset'])*factor
    cloud=np.concatenate([mesh(obj).reshape(-1,3) for obj in solids.values()])
    distances,ids=cKDTree(cloud).query(expected)
    ear_span=float(np.linalg.norm(cloud[ids[1]]-cloud[ids[0]]))
    assert np.max(distances)<.003 and abs(ear_span-228.6)<.004,('ear landmark preservation',distances,ear_span)
    print('Reassembled ear span mm:',ear_span,flush=True)
    outside=None;removed=None
    result=dict(verification_script_sha256=sha(Path(__file__)),config='designs/cicero_head/configs/rev_0001.json',build_manifest_sha256=sha(out/'build_manifest.json'),
                asset_provenance_sha256=sha(HERE/'asset_provenance.json'),leaves=checks,installation_samples=motions,motion_geometry='source assets independently matched to installed STL within 0.002mm; face obstacles trimmed to rail protrusions >0.02mm beyond seam to avoid coplanar contact degeneracy',
                ear_span_mm=ear_span,ear_landmark_errors_mm=distances.tolist(),verification_contact_plane_exclusion_mm=.02,excess_outside_master_mm3=outside,intentional_removed_volume_mm3=removed,
                single_neck_owner_cap_symmetric_area_difference_mm2=neck_error,
                recombination_boolean='unverified; near-coincident serialized mesh Booleans avoided',full_continuous_sweeps='unverified',structural_joins='unverified',minimum_internal_material_width='unverified')
    write_json(HERE/'verification.json',result)
    failures=[m for m in motions if m['worst_overlap_mm3']>1]
    # Up to 1 mm3 is an explicit conservative serialization/contact-sliver
    # allowance after the independently checked 0.002mm import/export tolerance.
    assert not failures,('installation collisions',failures)
    print('PASS: installed geometry, imported dependency provenance, flat contact, single neck owner, sampled assembly paths',flush=True)


if __name__=='__main__':main()
