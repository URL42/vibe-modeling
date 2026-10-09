// =============================================================================
// 6u_cyberdeck — design-owned rack constants and geometry-locking assertions
//
// Provenance (design-owned adapted copy — the reference SCAD is NEVER imported):
//   Spec        : ten-inch-rack-m3-printed-design-spec v2.0.0
//   Source      : references/engineering/ten_inch_rack/v2.0.0/
//   Bundle SHA256:
//     330051136930B54F0ABF91FF81EA217D0E6CAD2DBE6503375FFB219E59E0210D
//   Station ref : references/engineering/fasteners/m3_captive_nut_registration_seam_stations.md
//
// This file locks the derived geometry for the 6u_cyberdeck case (80 mm deep)
// with named dimensions and assert() statements, per host structural governance
// (AGENTS.md §10) and the split-prints playbook. A passing render does NOT prove
// these values; the asserts below are the proof.
//
// Three quantities are kept distinct (never conflated):
//   - fit clearance     : functional mating clearance
//   - structural overlap: positive-volume engagement >= minimum wall
//   - boolean epsilon   : computational tolerance only, never fit or structure
// =============================================================================

// --- Rack specification (v2.0.0) -------------------------------------------
U_PITCH                     = 44.45;   // spec: U_PITCH (mm)
RACK_FRONT_WIDTH_NOMINAL    = 254.000; // spec: RACK_FRONT_WIDTH_NOMINAL (mm)
RACK_CLEAR_OPENING_NOMINAL  = 222.250; // spec: RACK_CLEAR_OPENING_NOMINAL (mm)

// M3 hardware (spec)
M3_THREAD_D                 = 3.0;
M3_CLEARANCE_CLOSE_D        = 3.2;
M3_CLEARANCE_DEFAULT_D      = 3.4;
M3_CLEARANCE_COARSE_D       = 3.6;
M3_WASHER_OD                = 7.0;
M3_WASHER_T                 = 0.5;
M3_WASHER_SEAT_D            = 8.25;

// --- Structural floors (host raises MIN_PRIMARY_HOLE_RADIAL_MATERIAL) -------
MIN_WALL                    = 3.0;   // minimum wall thickness (mm)
MIN_STRUCTURAL_OVERLAP      = 3.0;   // >= MIN_WALL (host rule)
MIN_INTERNAL_EDGE           = 3.0;   // no ligament/edge thinner than this
BOOLEAN_EPSILON             = 0.02;  // computational only — NEVER fit/structure

// --- 6u_cyberdeck design inputs ---------------------------------------------
RACK_UNITS                  = 6;
RACK_DEPTH                  = 80.0;  // user-mandated (resolves spec rack_internal_depth)
RACK_FACE_WIDTH             = RACK_FRONT_WIDTH_NOMINAL; // 254.0

// --- Ring band: derived from M3 captive-nut station starting profile --------
// Each term is a structural/functional wall or depth; every wall term >= MIN_WALL.
RING_HEAD_RECESS_DEPTH      = 3.8;   // head-side recess depth (station profile)
RING_TONGUE_ROOT_OVERLAP    = MIN_STRUCTURAL_OVERLAP; // tongue root engagement
RING_SOCKET_TIP_CLEARANCE   = 1.0;   // socket tip fit clearance (distinct from structure)
RING_RECEIVER_CLOSED_END    = MIN_WALL; // receiver closed-end wall >= min wall
RING_NUT_POCKET_DEPTH       = 2.8;   // captive hex-nut pocket depth (station profile)

RING_BAND                   = RING_HEAD_RECESS_DEPTH
                            + RING_TONGUE_ROOT_OVERLAP
                            + RING_SOCKET_TIP_CLEARANCE
                            + RING_RECEIVER_CLOSED_END
                            + RING_NUT_POCKET_DEPTH;   // 3.8+3.0+1.0+3.0+2.8 = 13.6

// --- Locked outer envelope and opening --------------------------------------
OPENING_WIDTH               = RACK_CLEAR_OPENING_NOMINAL;              // 222.25
OPENING_HEIGHT              = RACK_UNITS * U_PITCH;                    // 6*44.45 = 266.7
OUTER_WIDTH                 = RACK_FACE_WIDTH;                         // 254.0
OUTER_DEPTH                 = RACK_DEPTH;                              // 80.0
// Opening centered on the face; the ring band fills each vertical side:
//   266.7 + 2*13.6 = 293.9  (asserted below as the locked envelope)
OUTER_HEIGHT                = OPENING_HEIGHT + 2 * RING_BAND;          // 293.9

// --- Per-leaf print bounds (quadrant split at X=0 and Z=0, full depth) ------
// A leaf owns one quadrant of the face. Its print bounds are the half-envelope
// on each axis plus the ring band that the leaf's seam stations carry.
LEAF_X                      = (OUTER_WIDTH  / 2.0) + RING_BAND;        // 127.0  + 13.6 = 140.6
LEAF_Z                      = (OUTER_HEIGHT / 2.0) + RING_BAND;        // 146.95 + 13.6 = 160.55
LEAF_Y                      = OUTER_DEPTH;                             // 80.0 (full depth)

PRINT_BED                   = 220.0;   // per-leaf build bed (mm)
BED_MARGIN_MIN              = 55.0;    // required free margin per axis (mm)

// =============================================================================
// Assertions — the proof. All must pass at render for the design to be valid.
// =============================================================================
module assert_6u_geometry() {
    // G2.1 — Ring band = 13.6, and every structural wall term >= minimum wall.
    assert(RING_HEAD_RECESS_DEPTH    >= 0.0, "ring: head recess depth positive");
    assert(RING_TONGUE_ROOT_OVERLAP >= MIN_WALL, "ring: tongue root overlap >= min wall");
    assert(RING_SOCKET_TIP_CLEARANCE >= 0.0, "ring: socket tip clearance non-negative");
    assert(RING_RECEIVER_CLOSED_END >= MIN_WALL, "ring: receiver closed-end >= min wall");
    assert(RING_NUT_POCKET_DEPTH    >= 0.0, "ring: nut pocket depth positive");
    assert(abs(RING_BAND - 13.6) < BOOLEAN_EPSILON,
        "ring band must equal 13.6 (3.8+3.0+1.0+3.0+2.8)");
    assert(RING_TONGUE_ROOT_OVERLAP >= MIN_STRUCTURAL_OVERLAP,
        "ring: tongue root engagement >= min structural overlap");
    assert(RING_RECEIVER_CLOSED_END >= MIN_WALL,
        "ring: receiver closed-end wall >= min wall");

    // G2.2 — Outer envelope and clear opening.
    assert(abs(OUTER_WIDTH  - 254.0)  < BOOLEAN_EPSILON, "outer width must be 254.0");
    assert(abs(OUTER_DEPTH  - 80.0)   < BOOLEAN_EPSILON, "outer depth must be 80.0");
    assert(abs(OUTER_HEIGHT - 293.9)  < BOOLEAN_EPSILON, "outer height must be 293.9");
    assert(abs(OPENING_WIDTH  - 222.25) < BOOLEAN_EPSILON, "opening width must be 222.25");
    assert(abs(OPENING_HEIGHT - 266.7)  < BOOLEAN_EPSILON, "opening height must be 266.7 (6*44.45)");
    assert(OPENING_WIDTH  < OUTER_WIDTH,  "opening width inside face width");
    assert(OPENING_HEIGHT < OUTER_HEIGHT, "opening height inside face height");
    assert(OPENING_HEIGHT == RACK_UNITS * U_PITCH, "opening height is 6 U pitches");

    // Structural floors are mutually consistent.
    assert(MIN_STRUCTURAL_OVERLAP >= MIN_WALL, "min overlap >= min wall");
    assert(MIN_INTERNAL_EDGE    >= MIN_WALL, "min internal edge >= min wall");
    assert(M3_WASHER_SEAT_D    > M3_WASHER_OD, "washer seat OD exceeds washer OD");

    // G2.3 — Each leaf's print bounds fit the 220 mm bed with margin.
    assert(LEAF_X < PRINT_BED, "leaf X within bed");
    assert(LEAF_Y < PRINT_BED, "leaf Y within bed");
    assert(LEAF_Z < PRINT_BED, "leaf Z within bed");
    assert((PRINT_BED - LEAF_X) >= BED_MARGIN_MIN, "leaf X bed margin >= 55");
    assert((PRINT_BED - LEAF_Y) >= BED_MARGIN_MIN, "leaf Y bed margin >= 55");
    assert((PRINT_BED - LEAF_Z) >= BED_MARGIN_MIN, "leaf Z bed margin >= 55");
}
assert_6u_geometry();
