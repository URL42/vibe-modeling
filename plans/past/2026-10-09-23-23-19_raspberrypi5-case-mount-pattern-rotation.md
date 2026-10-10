---
plan_id: 2026-10-09-23-23-19_raspberrypi5-case-mount-pattern-rotation
title: Correct the Raspberry Pi base mounting pattern by 90 degrees
summary: Rotate the mounting holes and their underside recesses together while preserving the printing lid and its coupling.
status: past
created_at: 2026-10-09-23-23-19
---

# Correct the Raspberry Pi mounting orientation

Key: `[ ]` pending task, `[x]` completed task, `[?]` needs validation, `[-]` closed task

## Request, baseline and approved layout

User reports that the Raspberry Pi mounting pattern is off by 90 degrees.
Baseline commit f64f579, installed rev_0003.json; printing lid is rev_0002.
No existing active plan governs this correction.

User confirmed USB/Ethernet must face the open rear. Proposed atomic correction:
retain the PCB left edge at x5 (2 mm inside-wall gap), center its rotated
85 mm front-to-back length at y60, and use a 56 x 85 mm case-frame footprint
x5..61, y17.5..102.5. GPIO faces the left wall; USB-C/HDMI face the open
interior to the right. Transform board drawing coordinates (u,v) to case
(x,y) = (5+v,17.5+u). The mounting holes are not centered on the PCB;
rotating only their pitch about a fixed corner or their own center would
translate the board differently.

New centers: (8.5,21), (57.5,21), (8.5,79), (57.5,79) mm; pitch 49 x 58.
Move the four concentric underside recesses together with the through-bores.
User approved the exact placement and complete rebuild/regression checks with "yes".
The user-reported issue is a model orientation discrepancy. Printer/material,
printed base revision, observed fit measurements and hardware remain unknown;
no calibration compensation is proposed.

Official drawing checked during discovery:
https://datasheets.raspberrypi.com/rpi5/raspberry-pi-5-mechanical-drawing.pdf
Its 85 x 56 footprint, 58 x 49 mounting pitch and asymmetric end margin are
reference dimensions; physical board/baseplate fit remains unverified.

Freeze the lid source and exported geometry, envelope 120 mm, z113 mating
plane, four lid screw stations and z110..113 studs. Retain the approved 6 mm
floor, diameter-2.7 bores, diameter-5 x 3 mm underside recesses and 3 mm roofs.
Keep all earlier configs and captured printed-lid reference unchanged. Create
rev_0004.json; do not rewrite rev_0003. Product identities/hierarchy unchanged.

## Atomic execution checklist

- [x] 1. Confirm final rotation pivot/location and approve the matching atomic correction; promote to current.
- [x] 2. Correct the named PCB case-frame dimensions/offsets and derived centers; move bores and recesses together with assertion-protected exterior and pairwise margins.
- [x] 3. Create rev_0004.json, preserving printed-lid geometry and all coupling inputs.
- [x] 4. Extend installed-mesh verification to assert rotated pitch, exact approved centers, absence of obsolete holes, recess depth/diameter and retained roofs; preserve independent printed-lid comparison.
- [x] 5. Synchronize design README and revision-specific evidence with the changed mounting orientation and truthful PCB/hardware assumptions.
- [x] 6. Validate the assembly contract; initialize the new config with the complete builder and use the normal stale-design entrypoint.
- [x] 7. Audit and review the exact installed printable artifacts; verify sections, connectivity, winding, bounds and lid compatibility.
- [x] 8. Generate and review the full artifact-bound assembly set; audit all provenance and exact artifact counts.
- [x] 9. Finalize journal, documentation and plan lifecycle; regenerate/check indexes and review the intended diff.
- [x] 10. User authorized commit and push of the completed checkpoint on 2026-10-10.
- [-] 11. Immutable numbered publication remains outside this checkpoint.

## Files and validation

Expected files: defaults.scad and base.scad as needed, rev_0004.json, verifier,
design README/docs, corrected Pi 5 official link in docs/raspberry-pi-mounting.md, plan/indexes, journal and output/raspberrypi5_case/. Preserve
lid.scad/main.scad/parts.json and prior configs. Existing review sections use
derived mount-row coordinates and must follow the rotated layout. Keep the
same 19-view full assembly contract unless evidence requires a plan revision.

Complete printable build: 2 STL + 34 PNG. Supplement: 1 review-only STL + 19 PNG.
Final flat output: 3 STL + 53 PNG + two manifests = 58 files. No manual
OpenSCAD invocation or ad hoc artifact destinations.

For the proposed PCB placement, closest head-recess exterior margin
is 6 mm and nearest side-wall inner-face margin is 3 mm. Orthogonal recess
pair ligaments are 44/53 mm. Assert all six pairs and all exterior margins.
Wall/floor embed remains 6 mm; stud/wall overlap remains 3 mm. Seat roofs remain
3 mm, with the already-approved 1.15 mm radial base seating-face exception and
retained lid seat exception. Review final-STL sections and mount-row views;
closed meshes alone do not prove these dimensions.

Independent geometry checks must compare the final lid to the stored printed
rev_0002 canonical triangle hash, verify lid source bytes and frozen coupling
inputs, assert exact rotated centers/pitch and confirm the old through-hole
locations have returned to solid floor. Physical Pi/baseplate placement,
hardware fit, connector/cable access, slicing and strength remain unverified
without measured physical evidence. Do not claim fabrication readiness.

## Verifier regression scope

Preserve the captured printed-lid reference unchanged. In rev_0004 only, permit
the five approved PCB layout fields (pi_w, pi_d, pi_y_off, pi_hole_span_x,
pi_hole_span_y) to differ from the earlier broad freeze; explicitly assert
56,85,17.5,49,58 and the four approved centers independently. All other frozen
inputs and lid source/mesh must still match. Keep rev_0003 verification behavior.
Measure original mounting positions as solid 6 mm floor, not leftover bores.
Audit the base top coupling, every recess roof, wall seam and all cut pairs.

## Initial digital geometry gate

Complete rev_0004 installed build/audit passed 2 STL/34 PNG. Independent mesh
verification passed all 73 sections, exact approved centers and 49 x 58 pitch,
closed/wound connected leaves and unchanged bounds. Old positions are solid
6 mm floor; four head recesses retain diameter 5, depth 3 and 3 mm roofs.
Canonical lid hash matches the printing reference. Earlier configs, lid source,
main dispatch, part/assembly contracts and baseline reference match HEAD.
A negative check rejects the old 58 mm across-case pitch. Structural joins and
minimum internal material width: passed with retained seat-face exceptions.

## Final installed printable review

Normal stale-design entrypoint installed rev_0004 after documentation updates.
Final complete audit passed 2 STL/34 PNG. Repeated final-mesh verification passed
all 73 sections and printed-lid canonical equality. Reviewed all 34 exact
installed printable PNGs before starting the full supplementary assembly set.
Base shows only the new rectangular pattern; no obsolete holes, lid changes,
new part identities or altered upper stations appear. Physical fit unverified.

## Final artifact-bound review and local checkpoint

Reviewed all 19 exact installed assembly PNGs after the complete printable
build/audit and printable artifact review. PASS: canonical product decomposition,
printable-leaf coverage, unchanged placement/assembly sequence, declared geometric
lid/base interface, intended z113 seating contact, gaps/collisions, modeled
supports and cross-seam continuity, explained openings and source/artifact
provenance. Both mount-row sections show the stepped seats; underside views
show only the approved 49 x 58 pattern. No displaced lid stations, new lid
features or obsolete Pi holes appear. Physical hardware fit/retention,
slicing, cable envelopes and strength remain BLOCKED_UNKNOWN for fabrication
readiness; digital correction does not constitute physical-fit evidence.

Final complete and assembly audits passed: 2 printable STL/34 PNG plus 1
review-only STL/19 PNG, exactly 3 STL/53 PNG/two manifests = 58 flat files.
Config/source/parts/assembly and current printable-build bindings match all
recorded artifact hashes. Final STL verifier passed 73 line sections, exact
approved centers/pitch, four restored stations, seat dimensions/roofs, bounds,
closed consistent shells and exact printed-lid canonical geometry comparison.
Structural joins: passed. Minimum internal material width: passed with retained
approved hardware-seat exceptions. No inspection or staging files remain.
Normal stale scan reports rev_0004 CURRENT; other designs stayed unchanged.

Implementation items 1..9 complete; item 10 closed until new Git/publication
authorization. Archive to past; regenerate/check indexes and review the task
diff. Proposed commit: `Correct Raspberry Pi mounting pattern orientation`.
No commit, push or immutable publication made. No pending downtime reports.

## Git checkpoint authorization

User authorized committing and pushing the complete verified rev_0004 checkpoint
with "commit everything and push" on 2026-10-10. Approved message: `Correct
Raspberry Pi mounting pattern orientation`. This includes all staged source,
documentation, journal, plan and governed mutable output artifacts. Immutable
numbered publication remains outside the authorization.

build_manifest.json SHA-256: f0c7d08c238570ed034de11d17a20b45f0067a4b7a723315f2d7f7e5cdd1a7cf.

assembly_review_manifest.json SHA-256: 0decdc7bcce48d47aba38cc5873d8b7792edeb513a94f34d8ecd0d98eabfac3b.

Config SHA-256: 57074aea42ac1294d289ffe6b1b21090d81d8c62f722bd7ab1627b311fc7bd31.
Source SHA-256: 66d26b64ecb741e95cca5ed29828dbed414d0463f41af119cfbf811e7706baff.
