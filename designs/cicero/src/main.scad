// Unsplit measurement master. Imported scan is not fabrication-verified.
part_id = 1;
target_ear_span_mm = 228.6;
ear_negative_x = [-14.551604270935059, -4.4222002029418945, 45.65835952758789];
ear_positive_x = [9.461223602294922, 6.8988494873046875, 45.459285736083984];
source_offset = [0.31207847595214844, -0.12383747100830078, 4.307562828063965];

// Future structural design targets, NOT measurements of the inherited scan.
minimum_wall_thickness = 3;
minimum_structural_overlap = 3;
minimum_internal_edge_width = 3;
assert(minimum_structural_overlap >= minimum_wall_thickness);
assert(minimum_internal_edge_width >= minimum_wall_thickness);
assert(part_id == 1, "Only the unsplit measurement master exists.");
assert(target_ear_span_mm > 0);
source_ear_span = norm(ear_positive_x - ear_negative_x);
assert(source_ear_span > 0);
uniform_scale = target_ear_span_mm / source_ear_span;
echo(source_ear_span=source_ear_span, uniform_scale=uniform_scale,
     target_ear_span_mm=target_ear_span_mm);

scale([uniform_scale, uniform_scale, uniform_scale])
    translate(source_offset)
        import("../assets/cicero_original.stl", convexity=10);
