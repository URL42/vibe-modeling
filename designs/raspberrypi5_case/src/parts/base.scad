// rev_0004 base: 120x120 floor and three solid walls, open at the back.
// Wall tops are at parting_line_z() = 113. Four 15x15x3 mounting studs
// sit at z 110..113; each joins the adjacent side wall through its full
// 3 mm thickness. The front studs additionally join the front wall.
// Four underside mounting-head recesses are added in the 6 mm floor.
// PCB bores and head seats share the approved rev_0004 rotated positions.
// Physical screw retention and PCB/cable fit remain unverified.

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

    assert(minimum_internal_edge_width >= minimum_wall_thickness,
        "minimum internal material width must meet the wall minimum");
    assert(m3_rim_h >= minimum_wall_thickness,
        "stud throat is thinner than minimum_wall_thickness");
    assert(m3_rim_h == 3, "rev_0002 studs must be exactly 3 mm tall");
    assert(m3_inset - m3_pilot_d / 2 - wall_t >= minimum_internal_edge_width,
        "pilot cut approaches the block/wall overlap");

    // ---- M3 rim blocks (join scheme, rev_0002) --------------
    // Each 15x15x3 block sits at the corner, flush with the two outer
    // faces: the front-left block spans x 0..15, y 0..15, z 110..113 (derived).
    // The M3 station (inset 10) is the bore center, NOT the block center:
    // the bore is 10 - 1.5 = 8.5 mm from each outer face and
    // 15 - 10 - 1.5 = 3.5 mm from each inner face. Lid alignment (the
    // Ø3.4 clearance bore and Ø7 counterbore share the same station on
    // both parts) is preserved; the lid's own ligaments are asserted in
    // lid.scad. The station inset must stay within the block (8.5 >= 3.5
    // keeps the bore inside the block with >= 3 mm to stay inside the
    // parting-face footprint under a screwed lid).
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
    // Block height: exactly the 3 mm stud height at the parting line
    // (z 110..113 (derived)), equal to the pilot bore depth.
    assert(parting_line_z() - m3_rim_h > floor_t,
        str("rim would break the floor at z ", parting_line_z() - m3_rim_h));
    // Overlap into each adjacent wall: the block is flush with the outer
    // faces, so the overlap spans the FULL wall thickness in the
    // through-wall direction: wall_t (3.0 mm, exact-minimum
    // minimum_structural_overlap BOUNDARY, documented) x 15 mm along the
    // wall face x m3_rim_h rim height, a positive volume with each wall.
    // The load path rim block -> wall (3 mm) -> floor (6 mm in rev_0003, asserted
    // above as the floor/wall embed) keeps the base self-supporting even
    // if a thread pulls out of the rim material.
    assert(wall_t >= minimum_structural_overlap,
        str("rim-block/wall overlap depth (full wall thickness ", wall_t,
            ") < minimum_structural_overlap ", minimum_structural_overlap,
            " — the rim join would be sub-minimum"));
    assert(m3_rim_size > wall_t,
        str("rim block ", m3_rim_size, " does not project past the wall ",
            "inner face (", wall_t, ") — the interior overhang would vanish"));
    // User-requested 3 mm through-pilot depth: physical screw pullout and
    // tightening torque remain unverified; this is not a 10 mm engagement.
    assert(m3_pilot_depth() == m3_rim_h,
        str("pilot depth ", m3_pilot_depth(), " != rim height ", m3_rim_h,
            " — bore no longer spans the full block height"));

    assert(pi_x_off >= wall_t && pi_y_off >= wall_t
           && pi_x_off + pi_w <= envelope - wall_t
           && pi_y_off + pi_d <= envelope,
        "PCB case-frame outline exceeds the wall box/open rear");
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
    // Named case-frame connector channels. rev_0004 places USB/Ethernet
    // toward the open rear (17.5 mm to the PCB edge), with power/HDMI
    // toward the right interior (56 mm). These are board-edge gaps;
    // plug envelopes and cable bend radii still require physical review.
    assert(envelope - wall_t - (pi_x_off + pi_w) >= pi_max_connector_h + minimum_internal_edge_width,
        "PCB-to-right-wall channel is below the retained clearance guard");
    assert(envelope - (pi_y_off + pi_d) >= minimum_internal_edge_width,
        "PCB rear edge has insufficient clearance to the open boundary");
    // Rim-block bottom vs the Pi: the top rim blocks sit above
    // the tallest plug body (z <= floor + 16 = 22 in rev_0003) — a z-collision guard
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
    // with the rim-block scheme: the rim blocks sit at z 110..113 (derived)
    // and the holes at z 0..floor_t, so z separates them whenever x/y overlap.
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

    // ---- Underside Raspberry Pi mounting-head recesses -------------------
    assert(pi_mount_head_depth >= 0, "mounting-head depth must not be negative");
    if (pi_mount_head_depth > 0) {
        assert(pi_mount_head_d > pi_hole_d, "head recess must exceed through-bore diameter");
        assert(floor_t - pi_mount_head_depth >= minimum_wall_thickness,
            "mounting-head recess leaves less than the required floor thickness");
        // Preserve the wall/floor seam and its neighboring internal strip.
        for (h = holes) {
            assert(h[1] - pi_mount_head_d / 2 - wall_t >= minimum_internal_edge_width);
            assert(envelope - wall_t - h[1] - pi_mount_head_d / 2 >= minimum_internal_edge_width);
            assert(h[2] - pi_mount_head_d / 2 - wall_t >= minimum_internal_edge_width);
            assert(envelope - h[2] - pi_mount_head_d / 2 >= minimum_internal_edge_width);
        }
        // All six recess pairs are inventoried, not just exterior margins.
        for (i = [0:len(holes)-2])
            for (j = [i+1:len(holes)-1])
                assert(norm([holes[i][1]-holes[j][1], holes[i][2]-holes[j][2]])
                       - pi_mount_head_d >= minimum_internal_edge_width);
        // Concentric cuts form one stepped hardware void. Approved shoulder:
        // 1.15 mm radial seating face, supported by a full 3 mm axial floor.
    }

    // ---- Pilot floor-breakthrough guard --------------------------------
    // (depth == rim height is asserted in the M3 block above; the usual
    // >= 10 mm M3 engagement is a documented rev_0002 exception, 3 mm.)
    // The bore must not break through the floor. The bottom is parting_line_z() - m3_rim_h, far above the floor.
    assert(parting_line_z() - m3_pilot_depth() > floor_t,
        str("pilot bottom ", parting_line_z() - m3_pilot_depth(),
            " breaks through the floor"));

    // ---- Geometry --------------------------------------------------------
    // All features in assembly coordinates; the part spans z 0..parting_line_z().
    difference() {
        union() {
            // Floor, z 0..floor_t (6 mm in rev_0003).
            cube([envelope, envelope, floor_t]);
            // Front wall (y 0..3), left wall (x 0..3), right wall
            // (x 117..120), z 0..parting_line_z(): ALL SOLID, no port cutouts; port
            // access is through the open back only. The full floor_t embed
            // into the floor gives the positive-volume join (AGENTS.md
            // section 10). Back open.
            cube([envelope, wall_t, parting_line_z()]);
            cube([wall_t, envelope, parting_line_z()]);
            translate([envelope - wall_t, 0, 0])
                cube([wall_t, envelope, parting_line_z()]);
            // Four M3 rim blocks, z 110..113 (derived), each flush with the two outer
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
        // PCB/baseplate mounting bores, through the floor. Hardware not modeled.
        for (h = holes) {
            translate([h[1], h[2], -boolean_epsilon])
                cylinder($fn = 48, h = floor_t + 2 * boolean_epsilon, d = pi_hole_d);
        }
        if (pi_mount_head_depth > 0)
            for (h = holes) {
                // Outward epsilon only: seat ceiling remains exactly at depth.
                translate([h[1], h[2], -boolean_epsilon])
                    cylinder($fn = 48, h = pi_mount_head_depth + boolean_epsilon,
                             d = pi_mount_head_d);
            }
        // M3 pilot bores, through each rim block (z 110..113 (derived); depth = rim
        // height, open end at the block bottom).
        for (s = stations) {
            translate([s[1], s[2], parting_line_z() - m3_pilot_depth() - boolean_epsilon])
                cylinder($fn = 48, h = m3_pilot_depth() + 2 * boolean_epsilon, d = m3_pilot_d);
        }
    }
}
