include <lib/rack_lock.scad>
include <lib/defaults.scad>
include <lib/seam_station.scad>
include <parts/master.scad>
include <parts/rear_bridge.scad>
include <parts/leaves.scad>
include <parts/control_cover.scad>
include <parts/assembly_review.scad>
module installed_leaf(id) {
  // Resolve imports in this entrypoint, relative to src/main.scad.
  // The review manifest binds these exact installed meshes before rendering.
  names=["leaf_bottom_left","leaf_bottom_right","leaf_top_right","leaf_top_left"];
  q=leaf_signs(id);
  tx=q[0]<0 ? case_width/2 : 0;
  tz=q[1]<0 ? case_height/2 : 0;
  translate([-tx,case_depth,-tz]) rotate([90,0,0])
    import(str("../../../output/6u_cyberdeck/",names[id-1],"_",revision,".stl"),convexity=10);
}
module installed_bridge() {
  translate([-rear_bridge_size/2,rear_bridge_front_y,rear_bridge_size/2]) rotate([-90,0,0])
    import(str("../../../output/6u_cyberdeck/rear_center_bridge_",revision,".stl"),convexity=10);
}
module installed_cover(id) {
  translate([id==6 ? -case_width/2 : 0,-cover_thickness,cover_center_z+cover_height/2])
    rotate([-90,0,0])
    import(str("../../../output/6u_cyberdeck/control_cover_",id==6 ? "left" : "right","_",revision,".stl"),convexity=10);
}
module colored_cover(explode=0) {
  for(id=[6,7]) color(id==6 ? [0.18,0.6,0.7] : [0.9,0.55,0.18])
    translate([id==6 ? -explode : explode,-explode,0]) installed_cover(id);
}
if(part_id>=1 && part_id<=4) leaf_print(part_id);
else if(part_id==5) rear_bridge_print();
else if(part_id==6 || part_id==7) cover_print(part_id);
else if(part_id==94) cover_coupon();
else if(part_id==90) assembly_review(assembly_view_id);
else if(part_id==91) colored_product();
else if(part_id==92) seam_station_coupon();
else if(part_id==93) master_assembly();
else assert(false,"Unknown part_id");
