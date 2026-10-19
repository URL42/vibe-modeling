# Playbook: Slice Large Objects for Flat-Bed Printing

*Status: Stable workflow; each design needs its own geometry and physical verification.*

## Objective

Partition oversized objects into useful build-volume sections with broad real
cut faces on the bed, preserved major interfaces and an installable joint scheme.

## Prerequisites

Read the [split/reassembly](how_to_design_split_print_parts_and_verify_reassembly.md),
[product decomposition](how_to_define_and_verify_canonical_product_decomposition.md),
[orientation](how_to_verify_print_orientation_supports_and_build_volume.md), and
[structural joins](how_to_design_and_verify_structural_openscad_joins.md) workflows.
For gravity-seated seams use the [dovetail protocol](../references/engineering/joints/gravity_seated_dovetails.md).
Have an approved scope, preserved source, usable printer XYZ limits and declared
provisional margins where brim, material or profile details are not yet known.

## Procedure

1. Preserve the original mesh and license/source notice. Record source hash,
   units or unit conversion, shell count, orientation and any overlapping shells.
   Do not confuse a closed shell with a valid union of overlapping components.
   Repair/decimation needs a documented comparison; never silently replace the source.
2. Define scale from explicit landmarks or functional measurements, using one
   uniform factor when preserving a scan. Record landmark coordinates, interpretation,
   transform and selection uncertainty. Verify the exported measurement separately
   from source-landmark uncertainty. Preserve important surface/contact regions.
3. Define product, logical subassemblies and tentative printable leaves. Reserve
   one continuous major attachment on one printable owner per side where feasible,
   before secondary cuts. Record interface support material and insertion access.
4. Choose an anatomically/functionally appropriate major cut; do not assume a
   tilted neck or angled body has a horizontal separation. Record unit plane
   normal and offset in assembly coordinates and inspect real sections.
5. For each candidate leaf, choose a **broad actual planar cut face first**.
   Transform its inward normal to print +Z and its face to Z=0. Optimize in-plane
   yaw/XY placement only while evaluating that face. Try other actual flat faces
   if necessary. Reject arbitrary tilted fits that leave a large flat cut face
   elevated above the plate with only a small contact point and a support scaffold.
6. Measure transformed triangle bounds, actual coplanar contact area and contact
   shape after all cuts. A bounding rectangle or convex-hull contact area can
   overstate real contact across cavities; report actual material. Check stability,
   center-of-mass projection, fragmented first layers and remaining lands after sockets.
7. Maximize useful depth behind a protected feature section while preserving its
   broad flat bed face and fitting the usable envelope. Refine candidate offsets
   against actual mesh/plane intersections; a convex hull is a conservative search
   aid, not proof of the deepest feasible nonconvex section. Declare resolution
   and numerical reserve; inspect features rather than trusting bounds alone.
   Inspect the rear cap for breakthroughs into protected recesses such as eyes.
   Recheck backing after connector cuts. If a major-interface reservation forces
   an excessively shallow feature section, reserve a local band on its interface
   owner and verify the resulting compound contact and installation path; retain
   broad real bed contact rather than sacrificing the protected feature.
8. Test the remainder on its real cut faces. Add only the cuts needed for fit,
   stable contact, load paths or assembly. A rear-only height slice can preserve
   a face section intact. Do not retain a low piece count at the cost of large
   elevated bases or fragmented major interfaces. Report a demonstrated count;
   finite searches do not prove a global minimum or universal impossibility.
9. Reserve footprint/height for brims, supports, males, entry lips, stops, keys
   and retainers. Recalculate actual final STL envelopes in print coordinates.
   Broad flat contact avoids the cut-face scaffold; sculpted overhangs may still
   require local support. Verify access/removal and layer-direction strength.
10. Inventory seams and assign exact ownership, entry paths and assembly order.
    Apply the gravity-seated protocol where selected. Revisit cuts if they divide
    a major interface or block the final installation. Do not add connectors to
    an incompatible cutting layout simply because body-only fit passed.
11. Cap and validate each region: closure, winding, intentional/unexpected shells,
    surface preservation, declared ownership and recombination against the master.
    Use full geometry differences/sections as appropriate; summed volume alone
    can hide equal-volume gaps and overlaps. Exclude declared joint clearances
    and intentional modifications explicitly from comparison expectations.
12. Complete the normal manifest build/install/audit before an artifact-bound
    assembly review for production blockout/detail/release gates. Review exact
    installed STLs/PNGs, section joins and inspect slicer layers; use coupons.
    Label design-local diagnostic exports as intermediate references, not complete
    printable releases. Preserve source/import dependency hashes beyond SCAD text.
13. Keep one unambiguous current output under `output/<design>/`. Remove superseded
    candidates through an authorized exact-file cleanup after checking current
    dependencies. Preserve originals and immutable revisions. Update links/counts,
    audit the exact flat file set and retain history in plans/journal, not competing
    current candidates. Remove staging and temporary SCAD before completion.

## Verification

Record per leaf: source/region identity, assembly-to-print transform, actual bed
plane/contact area, final XYZ bounds, margins/allowances, topology and support
assumptions. Record per seam: owners, material checks, stop/retention and installation
path. Validate reassembly, source/config/artifact hashes, exact artifact counts and
assembly review provenance. Keep mathematical impossibility proofs distinct from
failed sampled trials, and geometric fit distinct from fabrication readiness.

For existing Cicero reference artifacts, from repository root:

```powershell
python designs/cicero/measure_scale.py --audit-only
```

That command audits only the design-local reference set. It does not validate new
joint geometry, replace the complete multipart pipeline, or generalize to other
designs. Follow the [manifest build workflow](how_to_build_install_and_audit_manifest_driven_openscad_designs.md)
for production outputs.

## Plan Binding

The plan identifies protected features/major interface owners, usable volume,
flat-face policy, margins, cut-search scope, joint ownership and verification.
An explicit user-approved strategy authorizes matching checklist work without a
redundant approval request. Record failed candidates and revise materially
incompatible ownership through the governing plan rather than silently changing it.

## Lifecycle Compliance

Prompt -> Select/Create Plan -> Approval -> Execute approved items -> Update
plan/docs -> Verify -> Journal checkpoint -> Commit only when authorized.

## Cicero lessons and limits

Cicero demonstrated a uniformly scaled 228.6 mm ear span and an oblique neck cut,
then a whole-face section with four rear regions resting on actual cut faces in
a 220 mm cube. Free-tilt bounding-box fits were rejected. Its 5 mm XY margin,
0.01 mm search resolution and 0.05 mm numerical reserve are study-specific,
not universal fabrication tolerances. Current body-only fit does not establish
connector fit, source-shell union, strength, support-free sculpted features or
single-owner neck architecture. See the [Cicero architecture](../designs/cicero/joint_architecture.md).
