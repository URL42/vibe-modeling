// rev_0002: one flat 7 mm slab (z 113..120), no underside rim or bosses.
// Camera shape, outer lens rim and button bore are retained from rev_0001.
// Four 4 mm recesses leave 3 mm axial floors. The existing 1.8 mm radial
// head-seat annulus is a hardware detail; physical retention is unverified.
module lid() {
    assert(minimum_structural_overlap >= minimum_wall_thickness);
    assert(minimum_internal_edge_width >= minimum_wall_thickness);
    assert(lid_slab_t >= minimum_wall_thickness);
    assert(lid_slab_t >= minimum_structural_overlap);
    assert(lid_slab_z0() == parting_line_z());
    assert(m3_cbore_depth > 0 && m3_clear_d > 0 && m3_cbore_d > m3_clear_d);
    assert(lid_slab_t - m3_cbore_depth >= minimum_wall_thickness,
        str("screw-head recess floor ", lid_slab_t - m3_cbore_depth,
            " mm < minimum wall thickness ", minimum_wall_thickness));
    assert(m3_inset - m3_cbore_d / 2 >= minimum_internal_edge_width,
        "screw-head recess to slab edge is too narrow");
    assert(abs((m3_cbore_d - m3_clear_d) / 2 - 1.8) < 1e-9,
        "retained M3 seating detail: 1.8 mm radial annulus, 3 mm axial floor");
    assert(emblem_t >= minimum_structural_overlap);
    assert(emblem_center_x - emblem_body_w() / 2 >= minimum_internal_edge_width);
    assert(envelope - emblem_center_x - emblem_body_w() / 2 >= minimum_internal_edge_width);
    assert(emblem_body_h() / 2 - emblem_badge_h() / 2 - emblem_badge_dy()
           >= minimum_internal_edge_width);
    stations = [[m3_station_x0(), m3_station_y0()], [m3_station_x1(), m3_station_y0()],
                [m3_station_x0(), m3_station_y1()], [m3_station_x1(), m3_station_y1()]];
    badge = [emblem_center_x + emblem_badge_dx(), emblem_center_y + emblem_badge_dy()];
    // All subtraction pairs: recess/recess, recess/button, recess/badge,
    // badge/button. Concentric clearance/recess cuts form one stepped void.
    for (i = [0:len(stations)-1]) {
        c = stations[i];
        assert(norm(c - [emblem_center_x, emblem_center_y]) - m3_cbore_d / 2
               - button_hole_d / 2 >= minimum_internal_edge_width);
        badge_gap = [max(abs(c[0] - badge[0]) - emblem_badge_w() / 2, 0),
                     max(abs(c[1] - badge[1]) - emblem_badge_h() / 2, 0)];
        assert(norm(badge_gap) - m3_cbore_d / 2 >= minimum_internal_edge_width);
        if (i < len(stations)-1)
            for (j = [i+1:len(stations)-1])
                assert(norm(c - stations[j]) - m3_cbore_d >= minimum_internal_edge_width);
    }
    badge_button_gap = [max(abs(emblem_badge_dx()) - emblem_badge_w() / 2, 0),
                        max(abs(emblem_badge_dy()) - emblem_badge_h() / 2, 0)];
    assert(norm(badge_button_gap) - button_hole_d / 2 >= minimum_internal_edge_width);

    // ---- Camera emblem / button rim margins ----------------------------------
    // Button rim: solid disc (the SVG outer lens circle). Structural
    // quantity is the 3 mm embed into lid material; its wall to the Ø28
    // button hole must still meet the minimum internal edge width.
    assert(bezel_h + minimum_structural_overlap >= minimum_wall_thickness,
        str("button rim height ", bezel_h + minimum_structural_overlap, " mm < minimum wall thickness ", minimum_wall_thickness));
    assert((lens_d - button_hole_d) / 2 >= minimum_internal_edge_width,
        str("button hole to rim outer ", (lens_d - button_hole_d) / 2,
            " mm < minimum internal edge width ", minimum_internal_edge_width));
    // Camera silhouette margins on the lid top face, all >= minimum internal
    // edge width: body to slab front/rear (30 mm each), hump rear to slab
    // rear (24 mm), hump ends to body sides (26 mm), shutter step to slab
    // rear (27 mm), badge recess to the body left face (8 mm).
    assert(envelope - emblem_center_y - emblem_body_h() / 2 >= minimum_internal_edge_width,
        str("camera body to slab rear edge ", envelope - emblem_center_y - emblem_body_h() / 2,
            " mm < minimum internal edge width ", minimum_internal_edge_width));
    assert(emblem_center_y - emblem_body_h() / 2 >= minimum_internal_edge_width,
        str("camera body to slab front edge ", emblem_center_y - emblem_body_h() / 2,
            " mm < minimum internal edge width ", minimum_internal_edge_width));
    assert(envelope - emblem_center_y - emblem_hump_dy() - emblem_hump_h() / 2 >= minimum_internal_edge_width,
        str("viewfinder hump to slab rear edge ", envelope - emblem_center_y - emblem_hump_dy() - emblem_hump_h() / 2,
            " mm < minimum internal edge width ", minimum_internal_edge_width));
    assert(emblem_body_w() / 2 - emblem_hump_w() / 2 >= minimum_internal_edge_width,
        str("viewfinder hump to body side edges ", emblem_body_w() / 2 - emblem_hump_w() / 2,
            " mm < minimum internal edge width ", minimum_internal_edge_width));
    assert(envelope - emblem_center_y - emblem_shutter_dy() - emblem_shutter_h() / 2 >= minimum_internal_edge_width,
        str("shutter step to slab rear edge ", envelope - emblem_center_y - emblem_shutter_dy() - emblem_shutter_h() / 2,
            " mm < minimum internal edge width ", minimum_internal_edge_width));
    assert(emblem_body_w() / 2 - emblem_badge_w() / 2 + emblem_badge_dx() >= minimum_internal_edge_width,
        str("badge recess to body left face ", emblem_body_w() / 2 - emblem_badge_w() / 2 + emblem_badge_dx(),
            " mm < minimum internal edge width ", minimum_internal_edge_width));

    // ---- Geometry ------------------------------------------------------------
    // All features in assembly coordinates; the part spans z 113..125.
    // Button rim (drawn) base: emblem visible top (123) - embed 3 = 120;
    // the rim solid spans z 120..125 with 3 mm interleaving the emblem
    // below it (positive-volume join; decorative registration on the solid
    // silhouette, not a load path).
    button_rim_base_z = (lid_slab_z0() + lid_slab_t + emblem_t) - minimum_structural_overlap;
    difference() {
        union() {
            // Single plate; no extra band-embedding material below it.
            translate([0, 0, lid_slab_z0()])
                cube([envelope, envelope, lid_slab_t]);
            // Camera silhouette (docs/camera.svg), drawn z 117..123
            // (3 mm embed into the slab): rounded body, top-center
            // viewfinder hump, upper-left shutter step, left-face badge
            // recess (cut down to the slab top).
            translate([emblem_center_x, emblem_center_y, (lid_slab_z0() + lid_slab_t) - minimum_structural_overlap])
                difference() {
                    linear_extrude(emblem_t + minimum_structural_overlap) {
                        rounded_rect_profile(emblem_body_w(), emblem_body_h(), emblem_body_corner_r());
                        translate([0, emblem_hump_dy()])
                            rounded_rect_profile(emblem_hump_w(), emblem_hump_h(), emblem_hump_corner_r());
                        translate([emblem_shutter_dx(), emblem_shutter_dy()])
                            rounded_rect_profile(emblem_shutter_w(), emblem_shutter_h(), emblem_shutter_corner_r());
                    }
                    translate([emblem_badge_dx(), emblem_badge_dy(), minimum_structural_overlap])
                        linear_extrude(emblem_t + boolean_epsilon)
                            rounded_rect_profile(emblem_badge_w(), emblem_badge_h(), emblem_badge_corner_r());
                }
            // Button rim (lens): solid O lens_d disc (= the SVG's OUTER
            // lens circle; inner circles dropped), drawn z 120..125 - 3 mm
            // embed into the emblem, 2 mm proud above the emblem top.
            translate([emblem_center_x, emblem_center_y, button_rim_base_z])
                cylinder($fn = 64, h = bezel_h + minimum_structural_overlap, d = lens_d);
        }
        // Clearance bores through the 7 mm flat slab (z 113..120).
        for (c = [[m3_station_x0(), m3_station_y0()], [m3_station_x1(), m3_station_y0()],
                  [m3_station_x0(), m3_station_y1()], [m3_station_x1(), m3_station_y1()]]) {
            translate([c[0], c[1], parting_line_z() - boolean_epsilon])
                cylinder($fn = 48, h = (lid_slab_z0() + lid_slab_t - parting_line_z()) + 2 * boolean_epsilon, d = m3_clear_d);
        }
        // Counterbores, Ø7 x 4 from the lid top face (z 116..120).
        for (c = [[m3_station_x0(), m3_station_y0()], [m3_station_x1(), m3_station_y0()],
                  [m3_station_x0(), m3_station_y1()], [m3_station_x1(), m3_station_y1()]]) {
            translate([c[0], c[1], (lid_slab_z0() + lid_slab_t) - m3_cbore_depth])
                cylinder($fn = 48, h = m3_cbore_depth + boolean_epsilon, d = m3_cbore_d);
        }
        // Button through-hole, Ø28. The solid button rim spans z 120..125
        // and the slab spans z 113..120, so at (60,60) the hole passes
        // straight through the full stack (drawn z 113..125).
        translate([emblem_center_x, emblem_center_y, lid_slab_z0() - boolean_epsilon])
            cylinder($fn = 48,
                     h = ((lid_slab_z0() + lid_slab_t + emblem_t + bezel_h) - lid_slab_z0()) + 2 * boolean_epsilon,
                     d = button_hole_d);
    }
}
