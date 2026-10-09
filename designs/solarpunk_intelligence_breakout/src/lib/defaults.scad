// Structural and layout defaults for the Solarpunk Intelligence Breakout Panel.
// Blank backplane: same plate envelope and hanging interface as the intelligence
// hub, but without component holes, outlines, labels, or standoff collars.

// --- Structural minimums (asserted at render) ---
minimum_wall_thickness = 3.0;
minimum_structural_overlap = 3.0;
assert(minimum_structural_overlap >= minimum_wall_thickness,
    "structural overlap must be at least wall thickness");

// --- Plate envelope (matches solarpunk_intelligence_hub) ---
plate_width  = 169;  // mm, x-axis extent
plate_height = 194;  // mm, y-axis extent
plate_thick  = 3;    // mm, z-axis thickness
plate_origin = [0, 0, 0];  // bottom-left corner

// --- Hanging slots (mirrored top / bottom bands, identical to hub) ---
// 8 x 20 x 5 mm rectangular through-slots, 4 per band.
slot_width   = 20;   // mm, along x
slot_height  = 5;    // mm, along y
slot_centers_x = [20, 63, 106, 149];  // 4 stations, edges 10 mm from plate sides

// Top band: slot spans y = 186..191 (center y = 188.5); top edge 3 mm from plate top
top_band_y_center = 188.5;

// Bottom band: slot spans y = 3..8 (center y = 5.5); bottom edge 3 mm from plate bottom
bottom_band_y_center = 5.5;

// Each band is an 11 mm zone: 3 mm gap + 5 mm slot + 3 mm gap.
assert(top_band_y_center + slot_height/2 == plate_height - 3,
    "top band should leave 3 mm gap to top edge");
assert(bottom_band_y_center - slot_height/2 == 3,
    "bottom band should start 3 mm from bottom edge");

// --- Zip-tie hole grid (8 cols x 9 rows, 20 mm pitch, Ø5 through) ---
hole_dia   = 5;   // mm, through-hole diameter
hole_r     = hole_dia / 2;
hole_pitch = 20;  // mm, center-to-center spacing

// Columns: 8 stations symmetrically centered on the 169 mm plate.
// Edge clearance = 12 mm on both sides.
// Centers: 14.5 / 34.5 / 54.5 / 74.5 / 94.5 / 114.5 / 134.5 / 154.5 mm.
hole_cols_x = [14.5, 34.5, 54.5, 74.5, 94.5, 114.5, 134.5, 154.5];
assert(len(hole_cols_x) == 8, "hole grid expects 8 columns");
assert(hole_cols_x[0] - hole_r == 12, "leftmost hole edge should be 12 mm from plate left");
assert(plate_width - (hole_cols_x[7] + hole_r) == 12, "rightmost hole edge should be 12 mm from plate right");
for (i = [1:7])
    assert(hole_cols_x[i] - hole_cols_x[i-1] == hole_pitch,
        "hole columns should be 20 mm apart");

// Rows: 9 stations symmetrically centered on the 194 mm plate.
// Edge clearance = 14.5 mm on both sides.
// Centers: 17 / 37 / 57 / 77 / 97 / 117 / 137 / 157 / 177 mm.
hole_rows_y = [17, 37, 57, 77, 97, 117, 137, 157, 177];
assert(len(hole_rows_y) == 9, "hole grid expects 9 rows");
assert(hole_rows_y[0] - hole_r == 14.5, "bottom row edge should be 14.5 mm from plate bottom");
assert(plate_height - (hole_rows_y[8] + hole_r) == 14.5, "top row edge should be 14.5 mm from plate top");
for (i = [1:8])
    assert(hole_rows_y[i] - hole_rows_y[i-1] == hole_pitch,
        "hole rows should be 20 mm apart");

// Clearance to slot bands.
// The bottom row (center y = 17, edge y = 14.5) overlaps in x with the slot
// at x 10..30 (the hole at x = 14.5 spans x 12..17, slot spans x 10..30).
// The only separating material strip is in y: 14.5 - 8 = 6.5 mm.
// This is the governing internal-edge-width figure for this part.
assert(hole_rows_y[0] - hole_r - (bottom_band_y_center + slot_height/2) == 6.5,
    "bottom row-to-slot y gap should be 6.5 mm (governing internal edge width)");
assert((top_band_y_center - slot_height/2) - (hole_rows_y[8] + hole_r) == 6.5,
    "top row-to-slot y gap should be 6.5 mm (governing internal edge width)");
