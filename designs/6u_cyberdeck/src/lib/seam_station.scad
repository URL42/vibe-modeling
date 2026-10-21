// Local frame: u insertion, v depth, w inward from exterior skin.
// ISO 4762 M3x10 (5.5 x 3 head), ISO 7089 washer (7 x 0.5),
// ISO 4032 M3 nut (5.5 AF x 2.4). Candidate pockets require print calibration.
module station_frame(s) {
  r=s[0]; y=s[1];
  if(r==0) multmatrix([[1,0,0,0],[0,1,0,y],[0,0,-1,case_height/2],[0,0,0,1]]) children();
  if(r==1) multmatrix([[1,0,0,0],[0,1,0,y],[0,0,1,-case_height/2],[0,0,0,1]]) children();
  if(r==2) multmatrix([[0,0,1,-case_width/2],[0,1,0,y],[1,0,0,0],[0,0,0,1]]) children();
  if(r==3) multmatrix([[0,0,-1,case_width/2],[0,1,0,y],[1,0,0,0],[0,0,0,1]]) children();
}
module station_pad() {
  translate([-tongue_root_structural_overlap,-station_width/2,0])
    cube([receiver_length+tongue_root_structural_overlap,station_width,ring_band]);
}
module registration_tongue() {
  translate([-tongue_root_structural_overlap,-tongue_width/2,head_recess_depth])
    cube([tongue_root_structural_overlap+tongue_insertion_depth,tongue_width,tongue_thickness]);
}
module receiver_socket() {
  // The inner face is the load-bearing contact, nominally coincident with
  // the tongue inner face. Clearance is on the outer face, sides and tip.
  // No unsupported axial air gap is counted as a clamped load path.
  translate([0,-tongue_width/2-socket_side_clearance,head_recess_depth-socket_outer_clearance])
    cube([socket_length,tongue_width+2*socket_side_clearance,tongue_thickness+socket_outer_clearance]);
}
module m3_through_passage() {
  translate([fastener_offset,0,-boolean_epsilon])
    cylinder(d=m3_clearance_diameter,h=ring_band+2*boolean_epsilon,$fn=48);
}
module m3_head_recess() {
  translate([fastener_offset,0,-boolean_epsilon])
    cylinder(d=head_recess_diameter,h=head_recess_depth+boolean_epsilon,$fn=64);
}
module m3_captive_hex_nut_pocket() {
  translate([fastener_offset,0,ring_band-nut_pocket_depth])
    cylinder(d=nut_pocket_circumscribed_diameter,h=nut_pocket_depth+boolean_epsilon,$fn=6);
}
module receiver_cuts() {
  receiver_socket(); m3_through_passage(); m3_head_recess(); m3_captive_hex_nut_pocket();
}
module station_receiver() { difference() { station_pad(); receiver_cuts(); } }
module seam_station_coupon() {
  // Exact production local solids, separated for printing, bed = production rear face.
  // Tongue half includes the same pad root and 3 mm exterior-wall attachment.
  for(side=[0,1]) translate([side*28+3,0,station_width/2]) rotate([-90,0,0])
    if(side==0) difference() {
      union() {
        translate([-3,-station_width/2,0]) cube([3,station_width,ring_band]);
        registration_tongue();
      }
      m3_through_passage();
    } else intersection() {
      station_receiver();
      translate([0,-station_width/2,0]) cube([receiver_length,station_width,ring_band]);
    }
}
