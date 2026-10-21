// Four independent rear-wall pads, one strictly inside each quadrant.
// Plate -> four M3x10 / washer clamps -> pad webs -> integral rear skin.
module rear_pads() {
  for(x=[-rear_fastener_offset,rear_fastener_offset],z=[-rear_fastener_offset,rear_fastener_offset])
    translate([x-rear_pad_size/2,rear_bridge_back_y,z-rear_pad_size/2])
      cube([rear_pad_size,case_depth-rear_bridge_back_y,rear_pad_size]);
}
module rear_hardware_cuts() {
  for(x=[-rear_fastener_offset,rear_fastener_offset],z=[-rear_fastener_offset,rear_fastener_offset])
    translate([x,0,z]) rotate([-90,0,0]) {
      translate([0,0,rear_bridge_back_y-boolean_epsilon])
        cylinder(d=m3_clearance_diameter,h=case_depth-rear_bridge_back_y+2*boolean_epsilon,$fn=48);
      translate([0,0,rear_nut_floor_y])
        cylinder(d=nut_pocket_circumscribed_diameter,h=rear_nut_depth+boolean_epsilon,$fn=6);
    }
}
module rear_bridge_body() {
  difference() {
    translate([-rear_bridge_size/2,rear_bridge_front_y,-rear_bridge_size/2])
      cube([rear_bridge_size,rear_bridge_thickness,rear_bridge_size]);
    for(x=[-rear_fastener_offset,rear_fastener_offset],z=[-rear_fastener_offset,rear_fastener_offset])
      translate([x,rear_bridge_front_y-boolean_epsilon,z]) rotate([-90,0,0])
        cylinder(d=m3_clearance_diameter,h=rear_bridge_thickness+2*boolean_epsilon,$fn=48);
  }
}
module rear_bridge_print() {
  translate([rear_bridge_size/2,rear_bridge_size/2,-rear_bridge_front_y])
    rotate([90,0,0]) rear_bridge_body();
}
