// Review-only scenes; printable leaves remain base (1) and lid (2).
// Both leaves use assembly coordinates; the screw interface is at
// parting_line_z(). No hardware proxies are modeled.
module assembly_review(view_id = 0, show_proxies = false) {
    assert(view_id >= 0 && view_id <= 9, "unsupported assembly view");
    if (view_id == 0) {
        union() { base(); lid(); }
    } else if (view_id == 1) {
        base();
        translate([0, 0, 30]) lid();
    } else if (view_id == 2) {
        base();
    } else if (view_id == 3) {
        lid();
    } else if (view_id >= 4 && view_id <= 7) {
        // Stud seam start/mid/end and screw centers, normal to x.
        section_x = view_id == 4 ? 0.17 : view_id == 5 ? m3_rim_size / 2 + 0.13
                    : view_id == 6 ? m3_rim_size - 0.17 : m3_inset;
        intersection() {
            union() { base(); lid(); }
            translate([section_x - 0.05, -1, -1])
                cube([0.1, envelope + 2, envelope + emblem_t + bezel_h + 2]);
        }
    } else if (view_id == 8) {
        // Both lid screw-head floors in their final post-cut state.
        intersection() {
            lid();
            translate([-1, m3_inset - 0.05, -1])
                cube([envelope + 2, 0.1, envelope + emblem_t + bezel_h + 2]);
        }
    } else {
        // Front wall/floor connection and both side-wall supports.
        intersection() {
            base();
            translate([-1, wall_t / 2 - 0.05, -1])
                cube([envelope + 2, 0.1, envelope + 2]);
        }
    }
}
