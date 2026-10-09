---
plan_id: 2026-10-05-09-00-00_raspberrypi5-case-flat-lid-3mm-studs
title: Raspberry Pi 5 Case - Flat 7 mm Lid and 3 mm Mounting Studs
summary: Reduce the lid to a single flat screw-plate slab (drop the bottom rim band and bosses) and shrink the base mounting studs to 3 mm thick at the parting line.
status: past
created_at: 2026-10-05-09-00-00
---

## Context

User directive (verbatim): *"the rim and studs on the bottom of the lid are useless and
make it essentially impossible to print. remove them so its just a single layer with the
screw holes, insets for the heads, and the camera icon/bore hole for the arcade button.
also the mounting studs at the top of the base are 10mm thick. there is no reason for them
to be more than 3mm thick. make them 3mm thick, and keep them at the top.."*

## Execution authority and corrected constraints

The original thread approved this update with "yes". On 2026-10-09 the user
renewed execution authority: "finish the work and test the results to validate".
Existing partial edits in defaults.scad/base.scad belong to this task.
Baseline: committed rev_0001 config and installed rev_0001 outputs. Preserve
rev_0001.json; develop a mutable rev_0002 candidate in output/raspberrypi5_case/.
No immutable publication, commit, or push is authorized by this execution request.

The earlier plan incorrectly called z 114..120 a 3 mm slab and combined a
3 mm slab with a 4 mm counterbore. On 2026-10-09 the user selected "7mm":
use a 7 mm flat slab, retaining 4 mm recesses and 3 mm beneath the heads.
Nominal shell top remains z=120; parting line is z=113; studs occupy z=110..113.
The existing 1.8 mm radial head-seat annulus is a retained hardware detail;
its axial floor is now a full 3 mm and the outer recess ligament is 6.5 mm.
The physical M3 retention/torque and exact screw specification remain unverified.

Product hierarchy remains product_assembly -> case_joint -> base + lid.
Do not merge these printable leaves or add fabrication splits. The screw-only
interface is intentionally_terminated; it is not a Boolean structural join.
Base studs remain 15 x 15 x 3 mm, at the top of the base, with 3 mm pilot depth.
The camera silhouette, outer lens rim, and 28 mm button bore are retained.

## Files and verification

Expected edits: design defaults/base/lid/main/assembly_review source,
configs/rev_0002.json, assembly.json, design README, design docs verification
record and independent STL verification script, root README design entry,
this plan/indexes, today's journal, and governed output artifacts.

Complete printable pipeline: 2 STL + 34 PNG in output/raspberrypi5_case/.
Supplement with a full artifact-bound assembly set: front/rear/left/right/top/
bottom/isometric, exploded, leaf isolation, and sections at stud attachment
seam start/midpoint/end and fasteners. Supplement counts: 1 combined assembly STL + 16 PNG. Final union: 3 STL + 50 PNG and two manifests.
Review real installed printable files before supplementary assembly rendering.
Measure exact STL bounds, shell connectivity, void sizes/locations, stud height,
seam/throat sections, lid recess floor, and aligned interface/collision state.
Record physical screw retention, cable fit and printer/slicer validation as
unverified; do not infer these from manifoldness.

The automatic stale rebuild follows the installed manifest's rev_0001 config.
A first explicit governed scad_build_all.py build of rev_0002 is necessary to
select the new config, as directed by rebuild_stale_designs.py for config
selection. Thereafter run the normal stale-rebuild entrypoint and both audits.
No manual OpenSCAD invocation or build-automation edits are in scope.

## Checklist

Key: `[ ]` pending task, `[x]` completed task, `[?]` needs validation, `[-]` closed task

- [x] 1. Repair interrupted source and complete requested geometry.
  - [x] 1.1 Restore the malformed base.scad expression found during discovery.
  - [x] 1.2 Resolve lid/recess contradiction with the user and record dimensions.
  - [x] 1.3 Complete base stud/assertion repairs and flat-lid source.
  - [x] 1.4 Create rev_0002 config and update derived defaults/comments.
- [x] 2. Synchronize assembly and documentation.
  - [x] 2.1 Update interface frame and full/compact views and source dispatch.
  - [x] 2.2 Replace stale design README statements and add root design entry.
- [x] 3. Build and validate exact artifacts.
  - [x] 3.1 Validate contract; dry-run and install complete rev_0002 build.
  - [x] 3.2 Audit and inspect the installed printable STL/PNG artifacts.
  - [x] 3.3 Run independent STL measurement, connectivity and section checks.
  - [x] 3.4 Render full supplementary assembly set and inspect installed views.
  - [x] 3.5 Pass both manifest audits and normal stale-rebuild check.
  - [x] 3.6 Record evidence, provenance, and physical verification limitations.
- [x] 4. Close the local execution checkpoint.
  - [x] 4.1 Update checklist; archive execution plan when no local work remains.
  - [x] 4.2 Regenerate/check plan indexes and append journal checkpoint.
  - [x] 4.3 Review intended diff, final status, pending reports and commit proposal.
  - [x] 4.4 Receive explicit approval for the completed Git checkpoint (user: "go ahead").

## Artifact-review finding and scoped correction

The first complete build/audit and independent mesh verification passed, but
installed top/bottom orthographic previews hid holes. Three checks distinguished
this from bad geometry or stale outputs: manifest hashes matched, exact mesh
line sections proved through-holes, and installed below-isometric views exposed
the same holes. The normal PNG builder uses OpenCSG previews; the scoped design
main.scad now wraps its printable dispatches with render(convexity=10), forcing
full Boolean evaluation for every existing preset without modifying automation.
Rebuild the complete set and re-review orthographic artifacts before assembly.

## Verified local results

- User selected 7 mm lid; nominal top remains z120 and mating plane z113.
- Complete rev_0002 pipeline and normal stale-design entrypoint passed; no other
  design was rebuilt. Expected/actual printable set: 2 STL + 34 PNG.
- Reviewed all installed printable views, including corrected through-aperture
  orthographic views. Independent mesh check passed 49 final-solid sections,
  closed-shell/winding/volume checks and exact bounds/bores/recess-floor checks.
- Final full assembly set passed: 1 combined STL + 16 PNG. Re-rendered and reviewed the
  final set after source comment/documentation synchronization, bound to the
  final installed build. Both manifest audits passed.
- Digital structural joins passed. Minimum material width passed with the
  retained 1.8 mm radial hardware-seat exception (3 mm axial floor).
- Physical screw retention, hardware/cable fit, mechanical load testing and
  slicing remain unverified; no immutable publication or fabrication claim.
- Verification record: designs/raspberrypi5_case/docs/rev_0002_verification.md.

## Local execution checkpoint closed

All local execution and verification items are complete. Final exact union:
3 STL, 50 PNG and 2 manifests (55 files); complete and supplementary audits pass.
At local closeout, commit/push approval was pending. The user subsequently
approved the proposed commit and push with "go ahead" on 2026-10-09. The
checkpoint includes source, config, docs, journal and generated artifacts.
Immutable revision publication remains outside this approved checkpoint.
Suggested commit: `Finish Raspberry Pi 5 case flat lid and 3 mm studs`.
No pending downtime reports exist.

## Git checkpoint authorization

User approval on 2026-10-09: "go ahead", in response to the explicit proposal to
commit and push `Finish Raspberry Pi 5 case flat lid and 3 mm studs`.
Stage only the task files and complete generated artifact set; commit and push
main to origin. No geometry or source changes accompany this Git checkpoint.
