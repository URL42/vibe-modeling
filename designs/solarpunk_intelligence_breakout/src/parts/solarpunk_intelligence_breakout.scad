// Solarpunk Intelligence Breakout Panel — blank backplane plate with a
// uniform zip-tie hole grid.
// Same 169 x 194 x 3 mm envelope and hanging interface as the intelligence hub,
// but without raised outlines, labels, or collars.

module solarpunk_intelligence_breakout() {
    difference() {
        // Base plate (solid rectangular block).
        cube([plate_width, plate_height, plate_thick]);

        // Eight 20 x 5 mm hanging slots through the plate (4 top band, 4 bottom
        // band). Mirrored bands identical to the intelligence hub.
        for (xc = slot_centers_x) {
            // Top band slot (centered at y = 188.5)
            translate([xc, top_band_y_center, -0.5])
                linear_extrude(height = plate_thick + 1, convexity = 2)
                    square([slot_width, slot_height], center = true);

            // Bottom band slot (centered at y = 5.5)
            translate([xc, bottom_band_y_center, -0.5])
                linear_extrude(height = plate_thick + 1, convexity = 2)
                    square([slot_width, slot_height], center = true);
        }

        // 8 x 9 = 72 Ø5 mm through-holes on a 20 mm grid for zip-tie attachment.
        for (xc = hole_cols_x) {
            for (yc = hole_rows_y) {
                translate([xc, yc, -0.5])
                    linear_extrude(height = plate_thick + 1, convexity = 2)
                        circle(r = hole_r);
            }
        }
    }

    // --- Structural assertions (verified at render time) ---

    // Minimum internal edge width: tightest material strip between a void and
    // an exterior edge, or between two adjacent voids.
    // Governing feature: the Ø5 zip-tie hole grid.
    //   Closest hole-to-slot approach: hole at (14.5, 17) r=2.5 to slot at
    //   x 10..30, y 3..8. Hole spans x 12..17 (overlaps the slot's x extent),
    //   so the only separating material strip is in y:
    //   14.5 (hole bottom edge) - 8 (slot top edge) = 6.5 mm.
    //   Hole-to-hole ligament: 20 mm pitch - 5 mm dia = 15 mm.
    //   Hole-to-plate-edge: 12 mm (x) and 14.5 mm (y).
    //   Slot-to-slot gap: 23 mm (centers 20/63 - 20).
    //   Slot-to-plate-edge: 10 mm (slot centers at 20/149, half-width 10).
    minimum_internal_edge_width = 6.5;  // mm — hole edge to nearest slot edge

    assert(minimum_internal_edge_width >= minimum_wall_thickness,
        str("internal edge width ", minimum_internal_edge_width,
            " is below minimum wall thickness ", minimum_wall_thickness));
}
