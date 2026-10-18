# Gravity-seated dovetail protocol

Status: design protocol; dimensions and physical performance require design-specific verification.

## Purpose and coordinate frames

Join split prints with an accessible sliding dovetail that settles against a
closed lower stop under gravity in its normal assembled pose. A catch means a
positive end stop here, not an elastic snap latch. A retainer is a separate
feature that prevents unintended withdrawal. Keep these functions distinct.

Declare assembly coordinates with Z up and gravity direction `g = [0, 0, -1]`.
Declare a unit insertion direction `s` from entry to seated position for the
moving component, with the receiving component held fixed. For straight sliding
motion require `dot(s, g) > 0`; record travel `L` and vertical drop
`L * dot(s, g)`. Evaluate removal, seating and load transfer in assembly space,
not the rotated print pose. If both parts move, evaluate the moving assembly's
center-of-mass descent explicitly rather than reusing the fixed-receiver test.

A positive drop is necessary, not sufficient, for reliable gravity seating:
friction, surface finish, angular error and side loading may prevent it. A shallow
slope needs a physical coupon; do not claim automatic settling from slope alone.
The lowest stop is the end of the travel path at minimum assembled height, not
an arbitrary lowest point on the sculpted surface.

## Ownership and installation rules

| Seam | Preferred ownership | Required installation check |
| --- | --- | --- |
| Stacked pieces | Upward male on lower owner; downward-facing recess on upper owner where feasible | Prove an actual entry path. A conventional undercut sliding dovetail cannot be pushed normally through its narrow mouth. |
| Vertical seam | Either owner may carry the socket; choose for material and print orientation | Open entry above, closed stop below, and downward relative sliding travel. |
| Oblique seam | Prefer female-down/male-up where compatible with the chosen path | In-plane travel descends toward a closed low stop; check normal separation capture and tipping. |
| Horizontal seam | Ownership preference still applies | In-plane motion has zero gravity drop. Use a deliberately modeled accessible entry/compound seating mechanism or another verified joint; do not call an ordinary horizontal rail gravity-seated. |

Female-down/male-up is a preference in assembled coordinates, not a substitute
for accessible rail-end entry, adequate material or a valid installation path.
A proposed vertical drop-in, keyhole, tapered plug or compound-motion connection
must be modeled and verified as that mechanism; it is not automatically equivalent
to an end-entry dovetail. Any entry relief must retain capture at the final seat.

For major divisions (head/body, lid/chassis, removable module), preserve one
continuous interface on **one printed owner per side** whenever feasible. Prefer
one dovetail connection between those owners. Place secondary fabrication cuts
away from its rail, socket, stop and supporting load path. Do not substitute
several small mating interfaces distributed among multiple leaves merely because
the final exterior aligns. One interface owner is a requirement to verify, not
proof of strength. If volume or access prevents it, document evidence and review
a specific alternative before splitting the major interface.

## Joint record required before modeling

For each seam record:

- Stable interface ID, logical subassemblies, exact printable owners and assembly frame.
- Seam plane, unit insertion direction, moving/fixed owner, entry location,
  travel, vertical drop, seated position, closed stop and removal access.
- Male root, neck/throat, flank angle, engagement length/depth, receiving wall,
  stop thickness/root attachment, entry lead-in and separately dimensioned
  flank/floor/end clearances. Express whether clearance is per flank or total.
- Explicit `minimum_wall_thickness`, `minimum_structural_overlap` (at least wall
  thickness) and `minimum_internal_edge_width`; measure all shortest post-cut
  ligaments, including socket-to-socket, socket-to-stop and socket-to-exterior.
- Weight/bearing surface, transverse capture, torsion and overturning resistance,
  anti-lift retention, service-removal requirements and load assumptions.
- Actual print transform, broad planar bed face, remaining bed contact after
  recesses, added connector envelope, layer direction and support accessibility.
- Assembly predecessor steps, installation swept envelope and coupon evidence.

No universal rail size, angle, clearance or load rating is established here.
Distinguish the male's structural root overlap into its own body from sliding
engagement with a separate female part: mating parts require clearance, not
positive-volume union with each other. Both rail and stop need verified attachment
to their own owner. Count numerical epsilon separately from structural overlap.

## Execution sequence

1. Freeze the logical hierarchy and reserve major interface owners before
   choosing secondary cuts. Inventory every seam and every approaching feature.
2. Choose entry-to-stop motion in the final pose; check descent and access for
   every intermediate assembly state. Parallel rails need compatible travel and
   tolerance; intersecting directions can trap the last piece.
3. Locate continuous load-bearing lands and the closed lower stop. A stop must
   physically terminate travel, survive its bearing/shear loads and remain
   printable; an uncapped groove or a drawing of a stop is insufficient.
4. Start with straight, clearance-controlled sliding surfaces and a positive
   seat. Treat a terminal taper/wedge as an optional coupon-tested variation,
   with explicit seating depth, release behavior and splitting-force checks.
   Gravity seating does not by itself eliminate play.
5. Model mating geometry from shared parameters. Add intentional male-root and
   stop-root overlap into their owners; perform all sockets, reliefs and cuts;
   then repeat full-seam sections, pairwise void checks and connectivity tests.
6. Check insertion/removal swept solids at start, midpoint, end and changes in
   direction. Check realistic hand/tool access and full subassembly motion,
   not only a loose connector. Use integral mating features by default. Separate keys require explicit user
   approval plus verified seating/retention. Cicero prohibits loose keys.
7. Export production-derived coupons in the actual layer orientation. Test
   clearance, seating under intended loading, wobble, pull-off, stop durability,
   repeated removal and retainer access using the intended material/profile.
8. Build the complete governed product set; audit installed artifacts, then
   review the matching assembly and exact joint sections. Recheck bounds after
   every protrusion, recess, stop, retainer or orientation change.

## Acceptance and failure behavior

Pass only with exact source/config/artifact provenance, verified root/stop material,
collision-free assembly, retained planar bed contact, fitting final envelopes,
slicer review and applicable coupon/load evidence. Separate geometric, structural
and physical statuses; untested friction or strength remains unverified.

If a joint requires lifting against gravity to seat, loses its lower stop,
traps a final piece, subdivides a protected major interface, or forces a large
cut face into an elevated supported orientation, revise the ownership/cut/path.
Do not silently waive a requirement to retain an earlier piece count.

## Governing workflows

Use the [split/reassembly](../../../playbooks/how_to_design_split_print_parts_and_verify_reassembly.md),
[structural joins](../../../playbooks/how_to_design_and_verify_structural_openscad_joins.md),
[moving parts](../../../playbooks/how_to_design_and_verify_mating_sliding_and_moving_parts.md),
[fit coupons](../../../playbooks/how_to_create_fit_test_coupons_and_partial_prints.md),
and [flat-bed slicing](../../../playbooks/how_to_slice_large_objects_for_flat_bed_printing.md)
workflows. Implementation follows approved plan items; this protocol alone does
not authorize a new hierarchy or claim a print-ready design.
