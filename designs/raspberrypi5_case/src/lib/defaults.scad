// ---------------------------------------------------------------------------
// defaults.scad - raspberrypi5_case
// Single source of truth for the case geometry. Every input parameter below is
// guarded with an is_undef fallback so the design renders even when a
// parameter is missing from a config file. All derived layout quantities are
// computed from the inputs; no part file hardcodes a size-derived constant.
//
// Coordinate frame (assembly coordinates, shared by all parts):
//   x: 0..envelope, left (Pi/PCB side) -> right
//   y: 0..envelope, front -> back (back is the fully open band)
//   z: 0..envelope+emblem_t, bottom -> top
//
// Layout (rev_0001, fixed 2026-10-08 per user review): the PCB
// (x 5..90, y 32..88) faces its TWO port edges into the open interior:
// the HDMI/power edge (y = 88) looks straight at the open back (32 mm of
// free space for plugs and cables), and the USB/Ethernet edge (x = 90)
// looks across the interior with 27 mm of clearance to the right wall,
// so both plug groups terminate inside the case and their cables leave
// through the open back. The PCB edge against the left wall (5 mm gap) is
// the port-FREE edge. All side walls are SOLID: there are no port
// cutouts in this design.
//
// Structural governance: AGENTS.md section 10. minimum_wall_thickness,
// minimum_structural_overlap, and minimum_internal_edge_width are asserted in
// the part sources; this file only computes and exposes the values.
// ---------------------------------------------------------------------------

// ---- Structural minima (config inputs) ----
minimum_wall_thickness = is_undef(minimum_wall_thickness) ? 3.0 : minimum_wall_thickness;
minimum_structural_overlap = is_undef(minimum_structural_overlap) ? 3.0 : minimum_structural_overlap;
minimum_internal_edge_width = is_undef(minimum_internal_edge_width) ? 3.0 : minimum_internal_edge_width;

// ---- Boolean hygiene ----
boolean_epsilon = is_undef(boolean_epsilon) ? 0.001 : boolean_epsilon;

// ---- Envelope ----
envelope = is_undef(envelope) ? 120.0 : envelope;

// ---- Shell section sizes ----
floor_t = is_undef(floor_t) ? 3.0 : floor_t;
wall_t = is_undef(wall_t) ? 3.0 : wall_t;
lid_slab_t = is_undef(lid_slab_t) ? 3.0 : lid_slab_t;
lid_band_h = is_undef(lid_band_h) ? 10.0 : lid_band_h;

// ---- M3 lid/base join (rim block scheme, rev_0001 fix 2026-10-08) ----
// The base carries short rim blocks at the four corners of the parting
// line (NOT full-height columns: the full-height columns were rejected in
// user review as breaking the interior layout). At each corner a
// m3_rim_size x m3_rim_size x m3_rim_h block sits at z 107-m3_rim_h .. 107,
// flush with the two outer faces; its 3 mm overlap into each adjacent wall
// is the positive-volume join, and the Ø m3_pilot_d bore through the block
// (depth = m3_rim_h, open end at the block bottom) receives the M3 screw
// from the lid's clearance bore. The lid side is unchanged (Ø3.4
// clearance bore + Ø7x4 counterbore over the stations).
m3_inset = is_undef(m3_inset) ? 10.0 : m3_inset;
// Ø14 locked: Ø11 would leave only a 2.0 mm ring between the Ø7 lid
// counterbore edge and the bore edge (sub-minimum); Ø14 leaves 3.5 mm.
m3_boss_d = is_undef(m3_boss_d) ? 14.0 : m3_boss_d;
// 15x15 block: 3 mm overlap into EACH adjacent wall (= the 3 mm wall
// thickness) leaves 15 - 3 = 12 mm into the interior of which 3.5 mm is
// ligament around the Ø3 pilot and 5.5 mm is thread engagement in the
// wall (asserted in base.scad). 15 is also the maximum block that keeps
// the block inner faces away from the PCB holes (see base.scad asserts).
m3_rim_size = is_undef(m3_rim_size) ? 15.0 : m3_rim_size;
// 10 mm: mirrors the lid band height (symmetric joint about the parting
// line) and equals the documented M3 thread engagement (asserted >= 10).
m3_rim_h = is_undef(m3_rim_h) ? 10.0 : m3_rim_h;
m3_clear_d = is_undef(m3_clear_d) ? 3.4 : m3_clear_d;
m3_pilot_d = is_undef(m3_pilot_d) ? 3.0 : m3_pilot_d;
m3_cbore_d = is_undef(m3_cbore_d) ? 7.0 : m3_cbore_d;
m3_cbore_depth = is_undef(m3_cbore_depth) ? 4.0 : m3_cbore_depth;

// ---- Raspberry Pi PCB placement (docs/raspberry-pi-mounting.md) ----
pi_x_off = is_undef(pi_x_off) ? 5.0 : pi_x_off;
pi_y_off = is_undef(pi_y_off) ? 32.0 : pi_y_off;
pi_w = is_undef(pi_w) ? 85.0 : pi_w;
pi_d = is_undef(pi_d) ? 56.0 : pi_d;
pi_hole_span_x = is_undef(pi_hole_span_x) ? 58.0 : pi_hole_span_x;
pi_hole_span_y = is_undef(pi_hole_span_y) ? 49.0 : pi_hole_span_y;
pi_hole_inset = is_undef(pi_hole_inset) ? 3.5 : pi_hole_inset;
pi_hole_d = is_undef(pi_hole_d) ? 2.7 : pi_hole_d;
// Tallest standard connector on the Pi 5's edges (stacked USB-A pair,
// 16.0 mm, docs/raspberry-pi-mounting.md): used by base.scad's
// port-access channel assert and the rim-block z-collision guard.
pi_max_connector_h = is_undef(pi_max_connector_h) ? 16.0 : pi_max_connector_h;

// ---- Lid emblem (raised camera silhouette + solid button rim, docs/camera.svg) ----
// The camera icon follows docs/camera.svg per user review 2026-10-08: a
// rounded 46x30 camera body (corner r 4) with a top-center viewfinder
// hump (20x4, corner r 2), a small upper-left shutter step (6x2, corner
// r 2), and a small 6x4 badge recess (corner r 1) on the left body
// face, as a solid raised silhouette, centered on the lens center. The
// lens is the SVG's OUTER circle only ("forget the inner circle"),
// modeled as a solid raised button rim around the Ø28 arcade-button
// through-hole. All SVG unit counts are scaled by svg_unit() (derived
// below).
emblem_center_x = is_undef(emblem_center_x) ? 60.0 : emblem_center_x;
emblem_center_y = is_undef(emblem_center_y) ? 60.0 : emblem_center_y;
emblem_t = is_undef(emblem_t) ? 3.0 : emblem_t;
lens_d = is_undef(lens_d) ? 44.0 : lens_d;
bezel_h = is_undef(bezel_h) ? 2.0 : bezel_h;
button_hole_d = is_undef(button_hole_d) ? 28.0 : button_hole_d;

// ---- Maximum print dimension (sanity bound, not used for geometry) ----
maximum_print_dimension = is_undef(maximum_print_dimension) ? 300.0 : maximum_print_dimension;

// ===========================================================================
// Derived layout (computed from the config inputs above)
// ===========================================================================

// Parting line: top of base walls = bottom of lid rim band.
// Locked value: 120 - 3 (slab) - 10 (band) = 107.0
function parting_line_z() = envelope - lid_slab_t - lid_band_h; // 107.0

// Lid slab spans z = 117..120.
function lid_slab_z0() = envelope - lid_slab_t; // 117.0

// PCB hole centers in case coordinates. PCB origin (corner) is at
// (pi_x_off, pi_y_off, floor_t); hole centers are inset pi_hole_inset from
// the PCB corner and span pi_hole_span_x / pi_hole_span_y.
// Locked value: (8.5, 35.5), (66.5, 35.5), (8.5, 84.5), (66.5, 84.5).
function pi_hole_x0() = pi_x_off + pi_hole_inset; // 8.5
function pi_hole_y0() = pi_y_off + pi_hole_inset; // 35.5
function pi_hole_x1() = pi_x_off + pi_hole_inset + pi_hole_span_x; // 66.5
function pi_hole_y1() = pi_y_off + pi_hole_inset + pi_hole_span_y; // 84.5

// M3 stations: four corners inset m3_inset from the envelope edges.
// Locked value: (10, 10), (110, 10), (10, 110), (110, 110).
function m3_station_x0() = m3_inset; // 10.0
function m3_station_x1() = envelope - m3_inset; // 110.0
function m3_station_y0() = m3_inset; // 10.0
function m3_station_y1() = envelope - m3_inset; // 110.0

// Camera silhouette scale: the lens (button rim) O lens_d == the SVG's
// outer lens circle (r 11 SVG units), so svg_unit = lens_d/22 mm per SVG
// unit (2.0 at lens_d 44). The silhouette is centered on the lens center
// (the SVG lens sits at the body center); the icon "top" (viewfinder hump)
// faces the case back (+y).
function svg_unit() = lens_d / 22.0; // 2.0

// Camera body: SVG 46 x 30 units, corner r 4 units.
function emblem_body_w() = 46.0 * svg_unit(); // 92.0
function emblem_body_h() = 30.0 * svg_unit(); // 60.0
function emblem_body_corner_r() = 4.0 * svg_unit(); // 8.0

// Viewfinder hump: SVG 20 x 4 units at the body top-center, corner r 2,
// SVG center (24, 9) with the lens at (24, 26). Case offset (0, +32) mm:
// the straight SVG mapping puts the hump base exactly on the body top
// edge (coplanar contact, not a join), so the hump is shifted 2 mm into
// the body for a positive-volume union (the decorative detail; the
// load-bearing join is the emboss-to-slab overlap, 3 mm minimum).
function emblem_hump_w() = 20.0 * svg_unit(); // 40.0
function emblem_hump_h() = 4.0 * svg_unit(); // 8.0
function emblem_hump_corner_r() = 2.0 * svg_unit(); // 4.0
function emblem_hump_dy() = (26 - 9) * svg_unit() - svg_unit(); // +32.0 (2 mm embed)

// Shutter step: SVG 6 x 2 units at the upper left, rounded top corners
// (r 2), SVG x 6..12, y 9..11, i.e. centered at (9, 10) with the lens at
// (24, 26). Case offset (-30, +31) mm: the straight SVG mapping puts the
// step base exactly on the body top edge (coplanar contact, not a join),
// so the step is shifted 1 mm into the body for a positive-volume union.
// The step spans case x 24..36, y 89..93 (10 mm from the body left face).
// Badge recess: SVG 5 x 4 units (corner r 1) at x 5..10, y 15..19, i.e.
// centered at (7.5, 17). Case offset (-33, +18) mm (straight mapping;
// the recess is a blind cut, not a unioned feature, so no embed is
// needed). Blind recess from the emboss top (z 123) down to the slab top
// (z 120), emblem_t deep (3 mm).
function emblem_shutter_w() = 6.0 * svg_unit(); // 12.0
function emblem_shutter_h() = 2.0 * svg_unit(); // 4.0
// The SVG strokes the icon with a 2-unit outline, which would read the
// step corner as r ~2 SVG units; that is impossible on a 2-unit-tall
// step (pill limit = 1 unit), so the step is modeled with the pill
// limit: fully semicircular ends (r = 1 SVG unit = 2 mm).
function emblem_shutter_corner_r() = 1.0 * svg_unit(); // 2.0 (pill)
function emblem_shutter_dx() = (9 - 24) * svg_unit(); // -30.0 (case x from lens center)
function emblem_shutter_dy() = (26 - 10) * svg_unit() - svg_unit() / 2; // +31.0 (1 mm embed)

function emblem_badge_w() = 5.0 * svg_unit(); // 10.0
function emblem_badge_h() = 4.0 * svg_unit(); // 8.0
function emblem_badge_corner_r() = 1.0 * svg_unit(); // 2.0
function emblem_badge_dx() = (7.5 - 24) * svg_unit(); // -33.0 (case x from lens center)
function emblem_badge_dy() = (26 - 17) * svg_unit(); // +18.0 (case y from lens center)

// Lens circle center: emblem center (button hole shares this center).
function lens_center_x() = emblem_center_x; // 60.0
function lens_center_y() = emblem_center_y; // 60.0

// Viewfinder: the top-center hump of the camera silhouette
// (docs/camera.svg) IS the viewfinder feature; the legacy finder_w /
// finder_h / finder_h_off / finder_v_off config keys are retained for
// config stability but are not used by any rev_0001 geometry.

// M3 screw pilot depth in the base rim blocks: a bore exactly
// m3_rim_h deep (z 97..107) — the full block height (open end at the
// block bottom), i.e. the documented 10 mm M3 thread engagement
// (asserted >= 10 in base.scad, exact-minimum boundary). The bore passes
// through the rim block only and no deeper; the lid's clearance bore over
// the same station passes 13 mm of lid material.
function m3_pilot_depth() = m3_rim_h; // 10.0

// Rim block size at each M3 corner: m3_rim_size x m3_rim_size x m3_rim_h,
// flush with the two outer faces, z 107-m3_rim_h .. 107. The 3 mm
// overlap into each adjacent wall is the positive-volume join
// (AGENTS.md section 10) and the load path rim block -> walls -> floor.
// base.scad / lid.scad assert every ligament and margin.
function boss_rad() = m3_boss_d / 2; // 7.0

// ===========================================================================
// Shared helper modules (hub pattern)
// ===========================================================================

// Rounded-rectangle profile in the xy plane, centered on the origin.
// corner_r = 0 degenerates to a plain rectangle.
module rounded_rect_profile(w, h, r) {
    assert(r <= min(w, h) / 2, str("rounded_rect_profile: r exceeds half-min-dimension"));
    if (r > 0) {
        offset(r = r) {
            square([w - 2 * r, h - 2 * r], center = true);
        }
    } else {
        square([w, h], center = true);
    }
}

// Part dispatch fallback (main.scad overrides via the build scripts).
part_id = is_undef(part_id) ? 1 : part_id;
