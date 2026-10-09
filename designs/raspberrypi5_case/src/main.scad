// main.scad — raspberrypi5_case part dispatch.
// Part ids (parts.json): 1 = base, 2 = lid; 90 = assembly review scene
// (review_dispatch_id in assembly.json; not a printable part).
// Config-driven per-part entries are injected by scripts/scad_build_all.py
// (part_id + part params), so this file hardcodes no config values.

include <lib/defaults.scad>;
include <parts/base.scad>;
include <parts/lid.scad>;
include <parts/assembly_review.scad>;

review_dispatch_id = 90;

_part_id = is_undef(part_id) ? 1 : part_id;

if (_part_id == 1) {
    // Part 1: case base (floor + front/left/right walls + M3 rim blocks).
    // Full Boolean geometry avoids OpenCSG axis-aligned hole occlusion.
    render(convexity = 10) base();
} else if (_part_id == 2) {
    // Part 2: case lid (flat slab + camera emblem + recessed M3 holes).
    render(convexity = 10) lid();
} else if (_part_id == review_dispatch_id) {
    // Product, exploded, isolation and section review scenes per assembly.json.
    assembly_review(is_undef(assembly_view_id) ? 0 : assembly_view_id,
                    is_undef(show_proxies) ? false : show_proxies);
} else {
    assert(false, str("Unknown part_id: ", _part_id));
}
