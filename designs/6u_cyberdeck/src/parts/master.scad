// One continuous unsplit enclosure, with integral front ring and closed rear.
module shell_master() {
  difference() {
    translate([-case_width/2,0,-case_height/2]) cube([case_width,case_depth,case_height]);
    translate([-case_width/2+wall_thickness,front_thickness,-case_height/2+wall_thickness])
      cube([case_width-2*wall_thickness,case_depth-front_thickness-wall_thickness,case_height-2*wall_thickness]);
    translate([-opening_width/2,-boolean_epsilon,-opening_height/2])
      cube([opening_width,front_thickness+2*boolean_epsilon,opening_height]);
  }
}
module rack_cuts() {
  for(x=[-rail_x,rail_x],i=[0:17]) translate([x,0,rack_hole_z(i)]) rotate([-90,0,0]) {
    translate([0,0,-boolean_epsilon]) cylinder(d=m3_clearance_diameter,h=front_thickness+2*boolean_epsilon,$fn=48);
    translate([0,0,front_thickness-rack_nut_depth])
      cylinder(d=rack_nut_diameter,h=rack_nut_depth+boolean_epsilon,$fn=6);
  }
}
module receiver_master() {
  difference() {
    union() { shell_master(); rear_pads(); for(s=stations) station_frame(s) station_pad(); }
    rack_cuts();
    rear_hardware_cuts();
    for(s=stations) station_frame(s) receiver_cuts();
  }
}
module master_assembly() {
  union() {
    receiver_master();
    for(s=stations) station_frame(s) difference() { registration_tongue(); m3_through_passage(); }
  }
}
