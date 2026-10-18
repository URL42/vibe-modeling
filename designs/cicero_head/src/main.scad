// Generated from provenance-bound manifold assets.
part_id=1;
assembly_view_id=0;
minimum_wall_thickness=3; minimum_structural_overlap=4; minimum_internal_edge_width=3;
assert(minimum_structural_overlap>=minimum_wall_thickness);
assert(minimum_internal_edge_width>=minimum_wall_thickness);
module part_1() { import("../assets/face.stl",convexity=10); }
module assembled_1() { translate([166.20059569568826, -27.812845325237024, 397.13494167085383]) rotate([-104.775870570568, -47.088314064066104, -143.82437999063453]) part_1(); }
if(part_id==1) part_1();
module part_2() { import("../assets/neck_owner.stl",convexity=10); }
module assembled_2() { translate([20.187294734556957, 146.6578347932699, 360.0]) rotate([180.0, 0.0, -58.66851716807284]) part_2(); }
if(part_id==2) part_2();
module part_3() { import("../assets/rear_left_lower.stl",convexity=10); }
module assembled_3() { translate([-90.84506534136358, 119.01835506364557, 460.0]) rotate([180.0, 0.0, -24.812451501302647]) part_3(); }
if(part_id==3) part_3();
module part_4() { import("../assets/rear_right_lower.stl",convexity=10); }
module assembled_4() { translate([-58.15629433615034, 138.8592892745562, 460.0]) rotate([180.0, 0.0, -18.09889960908256]) part_4(); }
if(part_id==4) part_4();
module part_5() { import("../assets/rear_left_upper.stl",convexity=10); }
module assembled_5() { translate([51.13837199997619, -144.90183483079008, 506.14393352801983]) rotate([-90.0, -37.513364464547486, 115.24192808725385]) part_5(); }
if(part_id==5) part_5();
module part_6() { import("../assets/rear_right_upper.stl",convexity=10); }
module assembled_6() { translate([-72.45863328240897, 117.25701956313327, 468.6888034325353]) rotate([-90.0, -52.35569424448066, -64.75807191274613]) part_6(); }
if(part_id==6) part_6();
module part_7() { import("../assets/midline_key_lower.stl",convexity=10); }
module assembled_7() { translate([3.924763259055517, -61.17294902674918, 392.2198568797337]) rotate([-90.0, -71.55093026796465, -64.75825654229789]) part_7(); }
if(part_id==7) part_7();
module part_8() { import("../assets/midline_key_upper.stl",convexity=10); }
module assembled_8() { translate([44.328310041689235, -114.04215026929053, 502.23593923369833]) rotate([-90.00000000000003, -18.449031733085395, 115.24198779020082]) part_8(); }
if(part_id==8) part_8();
if(part_id==90) {
 if(assembly_view_id==1) import("../assets/exploded_reference.stl",convexity=10);
 else if(assembly_view_id==2) assembled_1();
 else if(assembly_view_id==3) import("../assets/rear_reference.stl",convexity=10);
 else import("../assets/assembled_reference.stl",convexity=10);
}
if(part_id==91) import("../assets/assembled_reference.stl",convexity=10);
