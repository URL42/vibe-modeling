// ---------------------------------------------------------------------------
// base.scad - raspberrypi5_case part 1 (case base).
//
// Face features (assembly coordinates, x: left=Pi side -> right, y: front
// -> back, z: 0 -> parting line 107):
//   - Floor 120x120x3 (z 0..3) with the four Raspberry Pi PCB mounting
//     holes (Ø2.7, 58 x 49 pattern, (8.5, 35.5) corner; docs/
//     raspberry-pi-mounting.md, design README decision 6; M2.5 inserts are
//     ASSUMED, not modeled).
//   - Front (y 0..3), left (x 0..3), and right (x 117..120) walls, 3 mm,
//     z 0..107 — ALL SOLID, no cutouts. The bottom 3 mm of each wall is
//     embedded into the floor (positive-volume join, AGENTS.md section 10:
//     the shared face at z = 3 alone is not a structural join). The back
//     is fully OPEN (design README decision 4); the wall tops at z = 107
//     are the mating faces for the lid band (parting line, intentionally
//     split parts). Port access is through the open back only: the PCB's
//     HDMI/power edge faces it directly and the USB/Ethernet edge faces
//     the open interior (plug bodies and cable exits pass the 120 mm open
//     band; nothing is routed through a wall).
//   - Four rim blocks for the M3 lid/base join, one at each corner of the
//     parting line: 15x15x10 mm at z 97..107, flush with the two outer
//     faces (front-left: x 0..15, y 0..15, station (10,10)). Each block
//     overlaps 3 mm into each adjacent wall (positive-volume join; the
//     load path is rim block -> wall (3 mm) -> floor -> opposite wall, so
//     the part stays self-supporting even if a screw is stripped). Each
//     carries a Ø3.0 pilot bore across the full block height
//     (z 97..107; depth = block height = 10.0 mm, documented M3
//     engagement, exact-minimum boundary; the open end at the block
//     bottom faces the case interior) for the M3 screw driven down
//     through the lid's Ø3.4 clearance bore. The rim scheme replaces the full-height corner
//     columns rejected in user review (2026-10-08) as breaking the
//     interior layout.
//
// Provenance: designs/raspberrypi5_case/README.md (locked decisions 1..13),
// docs/raspberry-pi-mounting.md. No size-derived constants are hardcoded in
// this file; every quantity comes from lib/defaults.scad (config-driven).
//
// Structural governance: AGENTS.md section 10. minimum_wall_thickness,
// minimum_structural_overlap, and minimum_internal_edge_width (all 3.0 in
// rev_0001) are asserted below. The assert block re-derives every ligament
// at build time from the config values, so a parameter edit that violates
// the layout (sub-3 mm ligament, pilot-bore breakthrough, rim encroachment
// on a PCB hole) fails the build instead of producing an unverified part.
// ---------------------------------------------------------------------------

module base() {
    // ---- Governance minima -------------------------------------------
    assert(minimum_structural_overlap >= minimum_wall_thickness,
        str("minimum_structural_overlap ", minimum_structural_overlap,
            " < minimum_wall_thickness ", minimum_wall_thickness));
    assert(floor_t >= minimum_wall_thickness,
        str("floor_t ", floor_t, " < minimum wall thickness ", minimum_wall_thickness));
    assert(wall_t >= minimum_wall_thickness,
        str("wall_t ", wall_t, " < minimum wall thickness ", minimum_wall_thickness));
    assert(floor_t >= minimum_structural_overlap,
        str("floor/wall embed depth ", floor_t,
            " < minimum_structural_overlap ", minimum_structural_overlap));
    assert(parting_line_z() > floor_t,
        str("parting line z ", parting_line_z(), " must be above the floor top ", floor_t));

    // ---- M3 rim blocks (join scheme, rev_0001 fix 2026-10-08) ----------
    // Each 15x15x10 block sits at the corner, flush with the two outer
    // faces: the front-left block spans x 0..15, y 0..15, z 97..107.
    // The M3 station (inset 10) is the bore center, NOT the block center:
    // the bore is 10 - 1.5 = 8.5 mm from each outer face and
    // 15 - 10 - 1.5 = 3.5 mm from each inner face. Lid alignment (the
    // Ø3.4 clearance bore and Ø7 counterbore share the same station on
    // both parts) is preserved; the lid's own ligaments are asserted in
    // lid.scad. m3_boss_d still names the Ø14 circle used by both parts
    // (smallest circle keeping the Ø7 counterbore ring >= 3 mm). The
    // station inset must stay within the block (8.5 >= 3.5 keeps the
    // bore inside the block with >= 3 mm to stay inside the parting-face
    // footprint under a screwed lid).
    assert(m3_station_x0() == m3_inset && m3_station_y0() == m3_inset
           && m3_station_x1() == envelope - m3_inset
           && m3_station_y1() == envelope - m3_inset,
        str("station inset ", m3_inset, " does not match the rim-block corners"));
    assert(m3_rim_size - m3_inset - m3_pilot_d / 2 >= minimum_internal_edge_width,
        str("pilot bore to rim INNER faces ", m3_rim_size - m3_inset - m3_pilot_d / 2,
            " mm < minimum_internal_edge_width ", minimum_internal_edge_width,
            " — the Ø3 bore would leave a sub-3 mm ring at the block inner corner"));
    assert(m3_inset - m3_pilot_d / 2 >= minimum_internal_edge_width,
        str("pilot bore to OUTER faces ", m3_inset - m3_pilot_d / 2,
            " mm < minimum_internal_edge_width ", minimum_internal_edge_width));
    // Block height: exactly the parting-line band (z 97..107) and equal to
    // the lid band height for a symmetric joint.
    assert(m3_rim_h == lid_band_h,
        str("rim height ", m3_rim_h, " != lid band ", lid_band_h,
            " — asymmetric joint at the parting line"));
    assert(parting_line_z() - m3_rim_h > floor_t,
        str("rim would break the floor at z ", parting_line_z() - m3_rim_h));
    // Overlap into each adjacent wall: the block is flush with the outer
    // faces, so the overlap spans the FULL wall thickness in the
    // through-wall direction: wall_t (3.0 mm, exact-minimum
    // minimum_structural_overlap BOUNDARY, documented) x 15 mm along the
    // wall face x 10 mm rim height, a positive volume with each wall.
    // The load path rim block -> wall (3 mm) -> floor (3 mm, asserted
    // above as the floor/wall embed) keeps the base self-supporting even
    // if a thread pulls out of the rim material.
    assert(wall_t >= minimum_structural_overlap,
        str("rim-block/wall overlap depth (full wall thickness ", wall_t,
            ") < minimum_structural_overlap ", minimum_structural_overlap,
            " — the rim join would be sub-minimum"));
    assert(m3_rim_size > wall_t,
        str("rim block ", m3_rim_size, " does not project past the wall ",
            "inner face (", wall_t, ") — the interior overhang would vanish"));
    // Pilot bore: through the block (open end at the block bottom z 97
    // facing the case interior), depth = rim height (z 97..107), 10.0 mm
    // = documented M3 engagement (exact-minimum BOUNDARY, documented).
    // The bore bottom at z 97 is 94 mm above the floor top (floor
    // breakthrough guarded in the pilot section below).
    assert(m3_pilot_depth() >= 10,
        str("M3 pilot engagement ", m3_pilot_depth(), " mm < 10 mm"));
    assert(m3_pilot_depth() == m3_rim_h,
        str("pilot depth ", m3_pilot_depth(), " != rim height ", m3_rim_h,
            " — bore no longer spans the full block height"));
    // Lid coupling: the Ø3.4 clearance + Ø7 counterbore envelope (Ø14
    // boss circle on the lid) must fit the Ø14 base boss at the same
    // station (circle == circle by construction; the non-degenerate bound
    // keeps a future edit from misaligning the two parts).
    assert(m3_boss_d > m3_pilot_d,
        str("boss circle ", m3_boss_d, " does not contain the pilot bore ", m3_pilot_d));

    // ---- PCB mounting holes (assume M2.5 inserts, design decision 6) --
    assert(pi_x_off >= wall_t && pi_y_off >= wall_t
           && envelope - pi_x_off - pi_w >= wall_t
           && envelope - pi_y_off - pi_d >= wall_t,
        str("PCB sits inside the wall box with margin: ",
            pi_x_off, " / ", pi_y_off, " / ",
            envelope - pi_x_off - pi_w, " / ", envelope - pi_y_off - pi_d));
    // Hole edges to the nearest floor-edge features (left/wall box for x,
    // front wall for y, back rim for y, right wall for x; the holes are
    // through-floor only, so z never separates them from the walls).
    assert(pi_hole_x0() - pi_hole_d / 2 - wall_t >= minimum_internal_edge_width,
        str("front-left hole to left wall ", pi_hole_x0() - pi_hole_d / 2 - wall_t));
    assert(pi_hole_y0() - pi_hole_d / 2 - wall_t >= minimum_internal_edge_width,
        str("front-left hole to front wall ", pi_hole_y0() - pi_hole_d / 2 - wall_t));
    assert(envelope - wall_t - pi_hole_x1() - pi_hole_d / 2 >= minimum_internal_edge_width,
        str("rear-right hole to right wall ", envelope - wall_t - pi_hole_x1() - pi_hole_d / 2));
    assert(envelope - pi_hole_y1() - pi_hole_d / 2 >= minimum_internal_edge_width,
        str("rear holes to back rim ", envelope - pi_hole_y1() - pi_hole_d / 2));
    // Hole-to-hole ligaments.
    assert(pi_hole_span_x - pi_hole_d >= minimum_internal_edge_width,
        str("hole-to-hole x ligament ", pi_hole_span_x - pi_hole_d));
    assert(pi_hole_span_y - pi_hole_d >= minimum_internal_edge_width,
        str("hole-to-hole y ligament ", pi_hole_span_y - pi_hole_d));
    // Port access (all side walls SOLID; access via the open back only):
    // the USB/Ethernet edge (x = pi_x_off + pi_w = 90) faces the right
    // wall (x = 117): the channel must clear the tallest standard
    // connector (16.0 mm, docs/raspberry-pi-mounting.md) with margin;
    // cables then exit under the 120 mm open-back band (physical check,
    // not modeled).
    assert(envelope - wall_t - (pi_x_off + pi_w) >= pi_max_connector_h + minimum_internal_edge_width,
        str("PCB-to-right-wall channel ", envelope - wall_t - (pi_x_off + pi_w),
            " mm < tallest connector ", pi_max_connector_h, " + ", minimum_internal_edge_width,
            " — the USB/Ethernet plugs would not seat"));
    // Rim-block bottom vs the Pi: the rim blocks (z 97..107) sit above
    // the tallest plug body (z <= floor + 16 = 19) — a z-collision guard
    // with named dimensions.
    assert(parting_line_z() - m3_rim_h >= floor_t + pi_max_connector_h + minimum_internal_edge_width,
        str("rim bottom z ", parting_line_z() - m3_rim_h,
            " is within ", pi_max_connector_h + minimum_internal_edge_width,
            " mm of the tallest connector top — the rim blocks would reach the Pi"));


    // Corner stations (M3 pilot-bore centers; used by the bore loop and
    // the rim-block corner placement below).
    stations = [
        ["front-left", m3_station_x0(), m3_station_y0()],
        ["front-right", m3_station_x1(), m3_station_y0()],
        ["back-left", m3_station_x0(), m3_station_y1()],
        ["back-right", m3_station_x1(), m3_station_y1()],
    ];

    // PCB mounting-hole centers (through-floor holes; used by the hole
    // geometry below). The old boss-vs-PCB-hole 16-pair loop is dropped
    // with the full-height boss scheme: the rim blocks sit at z 97..107
    // and the holes at z 0..3, so z separates them whenever x/y overlap.
    holes = [
        ["front-left", pi_hole_x0(), pi_hole_y0()],
        ["front-right", pi_hole_x1(), pi_hole_y0()],
        ["back-left", pi_hole_x0(), pi_hole_y1()],
        ["back-right", pi_hole_x1(), pi_hole_y1()],
    ];

    // ---- Rim block vs rim block (6 pairs) -------------------------------
    // Separate features, not a load path, but keep the minimum anyway.
    // Box-to-box gaps between the 15x15 blocks: orthogonal pairs 90 mm,
    // diagonal pairs sqrt(90^2 + 90^2) ~= 127.28 mm.
    blocks = [
        [0, 0],
        [envelope - m3_rim_size, 0],
        [0, envelope - m3_rim_size],
        [envelope - m3_rim_size, envelope - m3_rim_size],
    ];
    for (i = [0:len(blocks) - 2]) {
        for (j = [i + 1:len(blocks) - 1]) {
            a = blocks[i];
            b = blocks[j];
            gx = (b[0] >= a[0] + m3_rim_size) ? b[0] - (a[0] + m3_rim_size)
                 : (a[0] >= b[0] + m3_rim_size) ? a[0] - (b[0] + m3_rim_size) : 0;
            gy = (b[1] >= a[1] + m3_rim_size) ? b[1] - (a[1] + m3_rim_size)
                 : (a[1] >= b[1] + m3_rim_size) ? a[1] - (b[1] + m3_rim_size) : 0;
            lig = (gx == 0) ? gy : (gy == 0) ? gx : sqrt(gx * gx + gy * gy);
            assert(lig >= minimum_internal_edge_width,
                str("rim blocks ", i, "-", j, ": ", lig,
                    " mm < minimum_internal_edge_width ", minimum_internal_edge_width));
        }
    }

    // ---- Pilot floor-breakthrough guard --------------------------------
    // (>= 10 mm engagement and depth == rim height are asserted in the M3
    // block above.) The bore must not break through the floor: bottom
    // z 97 >> floor top 3.
    assert(parting_line_z() - m3_pilot_depth() > floor_t,
        str("pilot bottom ", parting_line_z() - m3_pilot_depth(),
            " breaks through the floor"));

    // ---- Geometry --------------------------------------------------------
    // All features in assembly coordinates; the part spans z 0..107.
    difference() {
        union() {
            // Floor, z 0..3.
            cube([envelope, envelope, floor_t]);
            // Front wall (y 0..3), left wall (x 0..3), right wall
            // (x 117..120), z 0..107: ALL SOLID, no port cutouts; port
            // access is through the open back only. The bottom 3 mm embed
            // into the floor gives the positive-volume join (AGENTS.md
            // section 10). Back open.
            cube([envelope, wall_t, parting_line_z()]);
            cube([wall_t, envelope, parting_line_z()]);
            translate([envelope - wall_t, 0, 0])
                cube([wall_t, envelope, parting_line_z()]);
            // Four M3 rim blocks, z 97..107, each flush with the two outer
            // faces at its corner; the overlap into each adjacent wall
            // spans the full wall thickness (positive-volume join, asserted
            // above).
            for (c = [[0, 0], [envelope - m3_rim_size, 0],
                       [0, envelope - m3_rim_size],
                       [envelope - m3_rim_size, envelope - m3_rim_size]]) {
                translate([c[0], c[1], parting_line_z() - m3_rim_h])
                    cube([m3_rim_size, m3_rim_size, m3_rim_h]);
            }
        }
        // PCB mounting holes, through the floor (M2.5 inserts assumed).
        for (h = holes) {
            translate([h[1], h[2], -boolean_epsilon])
                cylinder($fn = 48, h = floor_t + 2 * boolean_epsilon, d = pi_hole_d);
        }
        // M3 pilot bores, through each rim block (z 97..107; depth = rim
        // height, open end at the block bottom).
        for (s = stations) {
            translate([s[1], s[2], parting_line_z() - m3_pilot_depth() - boolean_epsilon])
                cylinder($fn = 48, h = m3_pilot_depth() + 2 * boolean_epsilon, d = m3_pilot_d);
        }
    }
}