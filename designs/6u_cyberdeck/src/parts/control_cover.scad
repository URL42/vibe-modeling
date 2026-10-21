// Local frame: X left/right, V bottom/top, W front-to-back; front face W=0.
// Installed: (X,Y,Z)=(X,W-cover_thickness,V+cover_center_z).
cover_height = 4*44.45-cover_fit_gap;
cover_center_z = -opening_height/2+2*44.45;
cover_station_v = cover_height/2-13;
cover_boss_depth = cover_thickness+4+nut_pocket_depth;
function cover_buttons() = concat(
  [for(x=[-20,20],v=[-20,20]) [-case_width/4+x,cover_height/4+v]],
  [for(p=[[0,25.5],[25.5,0],[0,-25.5],[-25.5,0]])
    [case_width/4+p[0],44+p[1]]]);
function cover_joysticks() = [[-case_width/4,-cover_height/4],[case_width/4,-cover_height/4]];
function cover_holes() = concat(
  [for(p=cover_buttons()) [p[0],p[1],cover_button_hole_d/2]],
  [for(p=cover_joysticks()) [p[0],p[1],cover_joystick_center_d/2]],
  [for(p=cover_joysticks(),sx=[-1,1],sv=[-1,1])
    [p[0]+sx*cover_joystick_pitch_x/2,p[1]+sv*cover_joystick_pitch_v/2,cover_joystick_bolt_d/2]],
  [for(x=[-rail_x,rail_x],i=[0,11]) [x,rack_hole_z(i)-cover_center_z,m3_clearance_diameter/2]]);
module assert_cover() {
  assert(cover_thickness>=minimum_wall_thickness);
  assert(cover_thickness>=minimum_structural_overlap);
  assert(cover_boss_depth-nut_pocket_depth-cover_thickness>=minimum_wall_thickness);
  assert(9-nut_pocket_circumscribed_diameter/2>=minimum_internal_edge_width);
  assert(10/2-m3_clearance_diameter/2>=minimum_internal_edge_width);
  assert(14-8-m3_clearance_diameter/2>=minimum_internal_edge_width);
  assert(case_width/2+14+2*print_margin<=print_bed);
  assert(cover_height+2*print_margin<=print_bed);
  assert(cover_boss_depth<=220);
  hs=cover_holes();
  for(i=[0:len(hs)-1]) {
    h=hs[i];
    assert(case_width/2-abs(h[0])-h[2]>=minimum_internal_edge_width,"cover outside edge");
    assert(cover_height/2-abs(h[1])-h[2]>=minimum_internal_edge_width,"cover top/bottom edge");
    assert(abs(h[0])-h[2]>=minimum_internal_edge_width,"cover seam edge");
    for(j=[0:len(hs)-1]) if(j>i)
      assert(norm([h[0]-hs[j][0],h[1]-hs[j][1]])-h[2]-hs[j][2]>=minimum_internal_edge_width,"cover cut-pair ligament");
    // Conservative complete boss rectangle clearance from every panel cut.
    for(v=[-cover_station_v,cover_station_v])
      assert(norm([max(0,-h[0],h[0]-18),max(0,abs(h[1]-v)-9)])-h[2]>=minimum_internal_edge_width,"cut vs seam station");
  }
  bs=cover_buttons();
  for(i=[0:len(bs)-1]) {
    b=bs[i];
    assert(opening_width/2-abs(b[0])-cover_button_envelope_d/2>=1,"button body vs rail");
    assert(cover_height/2-abs(b[1])-cover_button_envelope_d/2>=1,"button flange vs edge");
    for(j=[0:len(bs)-1]) if(j>i)
      assert(norm(b-bs[j])-cover_button_envelope_d>=1,"button envelope spacing");
  }
}
assert_cover();
module cover_hole_cuts() {
  for(h=cover_holes()) translate([h[0],h[1],-boolean_epsilon])
    cylinder(r=h[2],h=cover_boss_depth+2*boolean_epsilon,$fn=96);
}
module cover_station(id,v) {
  translate([0,v,0]) difference() {
    if(id==6) translate([-3,-5,0]) cube([17,10,cover_thickness]);
    else translate([0,-9,0]) cube([18,18,cover_boss_depth]);
    if(id==7) {
      // Side entry in X; exact bearing depth, 1 mm tip/side clearance.
      translate([-boolean_epsilon,-6,-boolean_epsilon]) cube([15+boolean_epsilon,12,cover_thickness+boolean_epsilon]);
      translate([8,0,cover_boss_depth-nut_pocket_depth])
        cylinder(d=nut_pocket_circumscribed_diameter,h=nut_pocket_depth+boolean_epsilon,$fn=6);
    }
    translate([8,0,-boolean_epsilon]) cylinder(d=m3_clearance_diameter,h=cover_boss_depth+2*boolean_epsilon,$fn=64);
  }
}
module cover_body(id) {
  difference() {
    union() {
      difference() {
        translate([id==6 ? -case_width/2 : 0,-cover_height/2,0]) cube([case_width/2,cover_height,cover_thickness]);
        if(id==7) for(v=[-cover_station_v,cover_station_v])
          translate([-boolean_epsilon,v-6,-boolean_epsilon]) cube([15+boolean_epsilon,12,cover_thickness+2*boolean_epsilon]);
      }
      for(v=[-cover_station_v,cover_station_v]) cover_station(id,v);
    }
    cover_hole_cuts();
  }
}
module cover_print(id) {
  translate([id==6 ? case_width/2 : 0,cover_height/2,0]) mirror([0,1,0]) cover_body(id);
}
module cover_coupon() {
  // Two deliberately separate production-derived station owners, face down.
  for(id=[6,7]) translate([id==6 ? 10 : 32,13-cover_station_v,0])
    intersection() { cover_body(id); translate([id==6 ? -10 : 0,cover_station_v-12,0]) cube([id==6 ? 24 : 21,24,cover_boss_depth]); }
}
