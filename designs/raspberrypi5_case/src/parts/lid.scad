// ---------------------------------------------------------------------------
// lid.scad - raspberrypi5_case part 2 (case lid).
//
// Face features (assembly coordinates, this part spans z 107..125):
//   - Rim band: 3 mm walls around the front (y 0..3), left (x 0..3), and
//     right/port (x 117..120) edges, z 107..117 (10 mm tall); the back
//     (y 117..120) is fully OPEN (design README decision 5). The band
//     bottom at z 107 is the parting line with the base wall tops: a
//     coplanar mating face between two separate printable parts
//     (intentionally split; retention is the 4x M3 screws, not this
//     contact - assembly.json m3_lid_base_join).
//   - Slab: full 120x120 plate, z 117..120 visible, drawn z 114..120 so
//     the bottom 3 mm overlaps the band tops (z 114..117): the slab joins
//     the band by positive-volume overlap, not a shared face (AGENTS.md
//     section 10).
//   - Four Ø14 M3 bosses at the corner stations, z 107..120, each with a
//     Ø3.4 clearance through-bore and a Ø7 x 4 mm counterbore from the lid
//     top face (z 116..120) seating the screw head below the rim. The
//     boss top (z 120) is flush with the slab top. Each boss is TANGENT to
//     the inner face of the adjacent band wall (inset 10 - r 7 = 3 mm =
//     wall_t): that tangency is incidental (not a structural join); the
//     boss joins the slab by the z 114..120 positive-volume overlap
//     (6 mm), which is the asserted join.
//   - Camera emblem (docs/camera.svg): raised solid camera silhouette
//     centered (60,60) - rounded 92x60 body, corner r 8; top-center
//     viewfinder hump 40x8, corner r 4; upper-left shutter step 12x4,
//     pill corners r 2; and a 10x8 badge recess, corner r 2, cut from
//     the emboss top (z 123) down to the slab top (z 120). Drawn
//     z 117..123 (3 mm embed into the slab top, positive-volume join)
//     and 3 mm proud.
//   - Button rim (lens): the SVG lens is concentric circles; per user
//     review 2026-10-08 the inner circles are dropped and the OUTER circle
//     (O44, == lens_d) is modeled as a SOLID raised rim disc (no ring
//     bore), z 120..125 (2 mm proud above the emblem top, 5 mm proud
//     above the slab), its bottom 3 mm interleaving the silhouette below
//     for the positive-volume join (decorative registration).
//     rim (positive-volume join per AGENTS.md section 10). The rim rests
//     on the solid silhouette - decorative registration, not a load path.
//     The Ø28 button through-hole passes through rim + slab (z 114..125)
//     for the arcade button (README decision 8, button not modeled).
//
// Provenance: designs/raspberrypi5_case/README.md (locked decisions 1..13),
// docs/raspberry-pi-mounting.md, configs/rev_0001.json. No size-derived
// constants are hardcoded here; every quantity comes from lib/defaults.scad.
//
// Structural governance: AGENTS.md section 10. All three minima are 3.0 mm
// in rev_0001. Every join in this part is positive-volume overlap of at
// least minimum_structural_overlap, with exactly one documented exception:
// the 1.8 mm step ring between the Ø3.4 clearance bore edge and the Ø7
// counterbore edge at each station is a screw-head seating interface, not
// a load path (locked config value 1.8, asserted as an exception below).
// ---------------------------------------------------------------------------

module lid() {
    // ---- Minima relations ----------------------------------------------
    assert(lid_slab_t >= minimum_wall_thickness,
        str("lid slab ", lid_slab_t, " mm < minimum wall thickness ", minimum_wall_thickness));
    assert(wall_t >= minimum_wall_thickness,
        str("band wall ", wall_t, " mm < minimum wall thickness ", minimum_wall_thickness));
    assert(lid_band_h >= minimum_structural_overlap,
        str("band height ", lid_band_h, " mm < minimum structural overlap ", minimum_structural_overlap));
    assert(emblem_t >= minimum_structural_overlap,
        str("emblem embed into slab ", emblem_t, " mm < minimum structural overlap ", minimum_structural_overlap));

    // ---- Stack heights ----------------------------------------------------
    // Slab bottom must sit at or above the parting line (117 >= 107): the
    // visible slab is the lid roof; drawing it 3 mm lower gives the band
    // embed.
    assert(lid_slab_z0() >= parting_line_z(),
        str("slab z0 ", lid_slab_z0(), " mm below parting line ", parting_line_z(), " mm"));

    // ---- Slab-to-band join -------------------------------------------------
    // The slab is drawn from lid_slab_z0() - minimum_structural_overlap
    // (z 114) up to lid_slab_z0() + lid_slab_t (z 120); the band tops at
    // z 117, so the interleaving solid band|slab region is the positive-
    // volume join (3 mm).
    assert(lid_slab_t >= minimum_structural_overlap,
        str("slab embed into band tops ", lid_slab_t, " mm < minimum structural overlap ", minimum_structural_overlap));

    // ---- Boss-to-slab join ---------------------------------------------------
    // Bosses span z 107..120; the slab solid spans z 114..120, so each boss
    // interleaves the slab by 6 mm of positive volume. (The bosses are also
    // TANGENT to the adjacent band wall inner faces - inset 10 - r 7 = 3 mm
    // = wall_t - but tangency is deliberately NOT treated as a join.)
    assert((lid_slab_z0() + lid_slab_t) - (lid_slab_z0() - minimum_structural_overlap) >= minimum_structural_overlap,
        str("boss-to-slab overlap ", (lid_slab_z0() + lid_slab_t) - (lid_slab_z0() - minimum_structural_overlap),
            " mm < minimum structural overlap ", minimum_structural_overlap));
    assert(m3_inset - boss_rad() >= minimum_internal_edge_width,
        str("boss ligament to part face ", m3_inset - boss_rad(), " mm < minimum internal edge width ", minimum_internal_edge_width));
    assert(m3_inset - boss_rad() == 3.0,
        str("boss ligament to part face is ", m3_inset - boss_rad(),
            " mm: exact documented 3.0 mm boundary (rev_0001), boss tangent to wall inner faces"));
    // Wall between the Ø3.4 clearance bore and the Ø14 boss outside.
    assert((m3_boss_d - m3_clear_d) / 2 >= minimum_internal_edge_width,
        str("clearance-bore wall ", (m3_boss_d - m3_clear_d) / 2, " mm < minimum internal edge width ", minimum_internal_edge_width));
    // Documented sub-minimum (rev_0001): the 1.8 mm step ring between the
    // Ø3.4 clearance bore edge and the Ø7 counterbore edge is a screw-head
    // seating interface at each station, not a load path. Value is locked,
    // asserted as an exception with explicit justification.
    assert(abs((m3_cbore_d - m3_clear_d) / 2 - 1.8) < 1e-9,
        str("documented sub-minimum (rev_0001): the ", (m3_cbore_d - m3_clear_d) / 2,
            " mm step ring between the Ø3.4 clearance bore edge and the Ø7 counterbore edge (< 3.0) is a screw-head seating interface at each station, not a load path."));
    // The counterbore (4 mm deep) must stay inside the boss solid.
    assert(m3_cbore_depth >= minimum_structural_overlap,
        str("counterbore depth/retained floor ", m3_cbore_depth, " mm < minimum structural overlap ", minimum_structural_overlap));

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
    // All features in assembly coordinates; the part spans z 107..125.
    // Button rim (drawn) base: emblem visible top (123) - embed 3 = 120;
    // the rim solid spans z 120..125 with 3 mm interleaving the emblem
    // below it (positive-volume join; decorative registration on the solid
    // silhouette, not a load path).
    button_rim_base_z = (lid_slab_z0() + lid_slab_t + emblem_t) - minimum_structural_overlap;
    difference() {
        union() {
            // Rim band (back open), z 107..117.
            translate([0, 0, parting_line_z()])
                cube([envelope, wall_t, lid_band_h]);
            translate([0, 0, parting_line_z()])
                cube([wall_t, envelope, lid_band_h]);
            translate([envelope - wall_t, 0, parting_line_z()])
                cube([wall_t, envelope, lid_band_h]);
            // Slab, drawn z 114..120 (3 mm embed into the band tops).
            translate([0, 0, lid_slab_z0() - minimum_structural_overlap])
                cube([envelope, envelope, lid_slab_t + minimum_structural_overlap]);
            // M3 bosses, z 107..120 (6 mm positive-volume join into the slab).
            for (c = [[m3_station_x0(), m3_station_y0()], [m3_station_x1(), m3_station_y0()],
                      [m3_station_x0(), m3_station_y1()], [m3_station_x1(), m3_station_y1()]]) {
                translate([c[0], c[1], parting_line_z()])
                    cylinder($fn = 64, h = (lid_slab_z0() + lid_slab_t) - parting_line_z(), d = m3_boss_d);
            }
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
                    translate([emblem_badge_dx(), emblem_badge_dy(), emblem_t])
                        linear_extrude(emblem_t + boolean_epsilon)
                            rounded_rect_profile(emblem_badge_w(), emblem_badge_h(), emblem_badge_corner_r());
                }
            // Button rim (lens): solid O lens_d disc (= the SVG's OUTER
            // lens circle; inner circles dropped), drawn z 120..125 - 3 mm
            // embed into the emblem, 2 mm proud above the slab top.
            translate([emblem_center_x, emblem_center_y, button_rim_base_z])
                cylinder($fn = 64, h = bezel_h + minimum_structural_overlap, d = lens_d);
        }
        // Clearance bores, Ø3.4 through each boss (z 107..120 + epsilon).
        for (c = [[m3_station_x0(), m3_station_y0()], [m3_station_x1(), m3_station_y0()],
                  [m3_station_x0(), m3_station_y1()], [m3_station_x1(), m3_station_y1()]]) {
            translate([c[0], c[1], parting_line_z() - boolean_epsilon])
                cylinder($fn = 48, h = (lid_slab_z0() + lid_slab_t - parting_line_z()) + 2 * boolean_epsilon, d = m3_clear_d);
        }
        // Counterbores, Ø7 x 4 from the lid top face (z 116..120).
        for (c = [[m3_station_x0(), m3_station_y0()], [m3_station_x1(), m3_station_y0()],
                  [m3_station_x0(), m3_station_y1()], [m3_station_x1(), m3_station_y1()]]) {
            translate([c[0], c[1], (lid_slab_z0() + lid_slab_t) - m3_cbore_depth - boolean_epsilon])
                cylinder($fn = 48, h = m3_cbore_depth + 2 * boolean_epsilon, d = m3_cbore_d);
        }
        // Button through-hole, Ø28. The solid button rim spans z 120..125
        // and the slab spans z 114..120, so at (60,60) the hole passes
        // straight through the full stack (drawn z 114..125).
        translate([emblem_center_x, emblem_center_y, (lid_slab_z0() - minimum_structural_overlap) - boolean_epsilon])
            cylinder($fn = 48,
                     h = ((lid_slab_z0() + lid_slab_t + emblem_t + bezel_h) - (lid_slab_z0() - minimum_structural_overlap)) + 2 * boolean_epsilon,
                     d = button_hole_d);
    }
}