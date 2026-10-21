module quadrant(id) {
  q=leaf_signs(id);
  translate([q[0]<0 ? -case_width/2 : 0,0,q[1]<0 ? -case_height/2 : 0])
    cube([case_width/2,case_depth,case_height/2]);
}
module leaf_body(id) {
  // Strict disjoint ownership: quadrant shell, plus its owned crossing tongues.
  // Receiver sockets remove those tongue volumes from the neighbouring owner.
  union() {
    intersection() { receiver_master(); quadrant(id); }
    for(s=stations) if(s[2]==id) station_frame(s)
      difference() { registration_tongue(); m3_through_passage(); }
  }
}
module leaf_print(id) {
  q=leaf_signs(id);
  translate([q[0]<0 ? case_width/2 : 0,q[1]<0 ? case_height/2 : 0,case_depth])
    rotate([-90,0,0]) leaf_body(id);
}
module colored_enclosure(explode=0) {
  colors=[[0.2,0.65,0.85],[0.95,0.55,0.2],[0.45,0.75,0.3],[0.75,0.35,0.65]];
  for(id=[1:4]) let(q=leaf_signs(id)) color(colors[id-1])
    translate([q[0]*explode,0,q[1]*explode]) installed_leaf(id);
}
module colored_product(explode=0) {
  colored_enclosure(explode);
  colored_cover(explode);
  color([0.8,0.7,0.2]) translate([0,-explode,0]) installed_bridge();
}
