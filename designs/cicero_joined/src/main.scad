// Integral joints only; no connector-only printable leaves.
part_id=1; assembly_view_id=0;
minimum_wall_thickness=3; minimum_structural_overlap=6; minimum_internal_edge_width=3;
assert(minimum_structural_overlap>=minimum_wall_thickness);
if(part_id==1) import("../assets/h_face.stl",convexity=10);
if(part_id==2) import("../assets/h_neck.stl",convexity=10);
if(part_id==3) import("../assets/h_left_lower.stl",convexity=10);
if(part_id==4) import("../assets/h_right_lower.stl",convexity=10);
if(part_id==5) import("../assets/h_left_upper.stl",convexity=10);
if(part_id==6) import("../assets/h_right_upper.stl",convexity=10);
if(part_id==7) import("../assets/b_neck.stl",convexity=10);
if(part_id==8) import("../assets/b_lower_lf.stl",convexity=10);
if(part_id==9) import("../assets/b_lower_lb.stl",convexity=10);
if(part_id==10) import("../assets/b_lower_rf.stl",convexity=10);
if(part_id==11) import("../assets/b_lower_rb.stl",convexity=10);
if(part_id==12) import("../assets/b_upper_lf.stl",convexity=10);
if(part_id==13) import("../assets/b_upper_lb.stl",convexity=10);
if(part_id==14) import("../assets/b_upper_mf.stl",convexity=10);
if(part_id==15) import("../assets/b_upper_mb.stl",convexity=10);
if(part_id==16) import("../assets/b_upper_rf.stl",convexity=10);
if(part_id==17) import("../assets/b_upper_rb.stl",convexity=10);
if(part_id==90) {
 if(assembly_view_id==0) import("../assets/product_reference.stl",convexity=10);
 if(assembly_view_id==1) import("../assets/exploded_reference.stl",convexity=10);
 if(assembly_view_id==2) import("../assets/head_reference.stl",convexity=10);
 if(assembly_view_id==3) import("../assets/bust_reference.stl",convexity=10);
 if(assembly_view_id==4) import("../assets/neck_reference.stl",convexity=10);
 if(assembly_view_id==5) import("../assets/exposed_reference.stl",convexity=10);
 if(assembly_view_id==6) import("../assets/head_neck_socket_reference.stl",convexity=10);
 if(assembly_view_id==7) import("../assets/bust_neck_rail_reference.stl",convexity=10);
}
if(part_id==91) import("../assets/product_reference.stl",convexity=10);
if(part_id==92) import("../assets/head_reference.stl",convexity=10);
if(part_id==93) import("../assets/bust_reference.stl",convexity=10);
