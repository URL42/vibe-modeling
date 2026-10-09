---
plan_id: 2026-10-09-19-00-00_raspberrypi5-case-base-mount-recesses
title: Add Raspberry Pi base mounting screw-head recesses without changing the printed lid
summary: Thicken the floor inward and add four underside mounting-head recesses while freezing the rev_0002 lid and lid/base coupling.
status: past
created_at: 2026-10-09-19-00-00
---

# Base mounting recesses with frozen lid coupling

Key: `[ ]` pending task, `[x]` completed task, `[?]` needs validation, `[-]` closed task

## Request and approval boundary

User: "printing has already started for the lid, so don't change anything that
would affect coupling"; add underside head insets around the current Raspberry
Pi baseplate mounting points and make the base thicker.

Baseline commit: f684d15. Printed lid reference: rev_0002.json and installed
lid_rev_0002.stl. Proposed rev_0003 candidate: 6 mm floor thickened inward,
four diameter-5 x 3 mm deep underside recesses. Leave 3 mm material above each
recess; keep diameter-2.7 through-bores and centers (8.5,35.5), (66.5,35.5),
(8.5,84.5), (66.5,84.5). User approved the exact strategy on 2026-10-09:
"Approve Ø5 × 3 mm recesses and 6 mm floor.". Screw-head physical fit must not be declared passed without a known
head envelope or physical measurement. The example diameter-5 recess assumes
heads smaller than 5 mm; wider heads need different recess dimensions.

Freeze: lid.scad bytes and all lid geometry inputs, nominal 120 mm envelope,
lid slab 7 mm, mating plane z113, base studs z110..113, 15x15x3 stud size,
four lid screw stations, pilot/clearance diameters and lid recesses. Floor
thickening raises the internal mounting surface by 3 mm; it does not move the
base underside, walls' outer extents, lid, or coupling. Preserve prior configs.
Product hierarchy and part identities are unchanged.

## Execution and artifacts

- [x] 1. Approve and activate this atomic plan after mounting-head dimensions are resolved.
- [x] 2. Add named floor-recess parameters, guards and four underside cuts in base.scad; create rev_0003.json.
- [x] 3. Extend installed-STL verifier for four head recesses, retained floors and exact rev_0002 lid/coupling regression.
- [x] 4. Add assembly underside/isolation and through-mount section views; validate the contract.
- [x] 5. Sync design README and rev_0003 verification note, retaining the rev_0002 historical record.
- [x] 6. Initialize rev_0003 through scad_build_all.py, then run the normal stale-design entrypoint and installed artifact audit.
- [x] 7. Review installed printable geometry; verify recess depths/diameters, flat underside, final ligaments, connected shell and unchanged lid/coupling.
- [x] 8. Generate/review the full artifact-bound assembly set; audit the flat exact union and input hashes.
- [x] 9. Finalize evidence, journal and plan/index lifecycle; review diff and propose task-scoped commit.
- [x] 10. Obtain explicit approval for the reviewed task-scoped commit and push; user approved with "yes go ahead".
- [-] 11. Immutable numbered publication remains outside this approved checkpoint.

Expected files: this plan/indexes, defaults.scad/base.scad/assembly_review.scad,
assembly.json, configs/rev_0003.json, design README/docs, independent verifier,
journal, and complete output/raspberrypi5_case/ artifacts. Do not edit lid.scad.
The baseline printable set is 2 STL + 34 PNG. Existing supplement is 1 STL +
16 PNG; declare the exact added underside and mount-section view counts before
building. All mutable artifacts remain in output/raspberrypi5_case/. No manual
OpenSCAD invocation or unrelated builds/automation changes.

Structural evidence: 6 mm wall/floor embed and unchanged 3 mm stud/wall overlaps; retained floor above
head recess >=3 mm; every new recess exterior and pairwise ligament >=3 mm.
Cuts must not enter the wall attachment zone. Verify using construction guards,
final STL line sections at all four mounts and their nearest outer edges,
connectivity/winding, underside/isometric images and mount sections. Compare
the new lid's final exported geometry against the printed rev_0002 reference
independently of source/config declarations; STL byte hash alone is insufficient
because triangle order can change between builds. Physical screw fit, hardware
length, slicing and load response remain unverified unless measured.

## Captured printed-lid baseline

- rev_0002 lid source SHA-256: 928ffe3e167d5b46630afc1108bf2e3119359a1933d91778270b6193db554e6c.
- Canonical triangle hash (sorted vertex triples rounded to six decimals, JSON
  with compact separators, SHA-256): 36281ee5052ce08af6e37fa510e84be303be2fedb1597a69591725c9751b3a6c.
- Lid bounds: (0,0,113)..(120,120,125) mm. Mating plane z113.
- Four printed-lid screw stations: (10,10), (110,10), (10,110), (110,110).
- No CAD geometry or installed artifact has been changed during planning.

## Approved artifact inventory

Printable: 2 STL + 34 PNG. Supplement: 1 combined STL + 19 PNG (the existing
16 plus base underside isolation and sections through both mounting-hole rows).
Final union: 3 STL + 53 PNG + 2 manifests = 58 files in output/raspberrypi5_case/.
The hardware seat shoulder is 1.15 mm radially around the diameter-2.7 bore;
this user-approved seating detail has a full 3 mm axial supporting floor.
Record it explicitly alongside the unchanged lid seat detail exception.
Printed-lid reference metadata: designs/raspberrypi5_case/docs/rev_0002_lid_compatibility.json.

## Installed printable gate

Complete manifest installed through the normal stale-design entrypoint with
rev_0003.json. Audit passed 2 STL/34 PNG; all installed printable views reviewed.
Final exported meshes passed 69 line sections, manifold/connectivity/winding,
base bounds (0,0,0)..(120,120,113), lid bounds (0,0,113)..(120,120,125).
Canonical lid mesh equals the printed reference; source and all coupling inputs
match. Negative checks reject wrong head-seat depths and an open mesh.
Previous configs, lid.scad, main.scad and parts.json match HEAD.
Structural joins: passed. Minimum internal material width: passed with the
approved base/lid hardware seating-face exceptions. Physical fit is unverified.

## Final artifact-bound assembly review and checkpoint

PASS: canonical decomposition and printable coverage (two logical assemblies,
two printable leaves), unchanged transforms/assembly sequence, declared
lid/base geometric interface, intentional z113 contact and collision-free
placement, stud/wall and floor/wall seam continuity, modeled structural
supports, explained openings and source/artifact provenance. Reviewed the exact
installed 19 assembly PNGs, including both stepped mount sections and underside
isolation. No extra parts, displaced stations or new lid features appeared.
Physical hardware retention/fit, slicing and mechanical strength remain
BLOCKED_UNKNOWN for fabrication readiness; they do not invalidate the measured
base-only digital correction. User fabrication/release approval has not been
requested or inferred. No immutable revision was published.

Complete build and full supplement audits passed the exact flat union of
3 STL + 53 PNG + two manifests = 58 files. All input/artifact hashes match.
The normal stale-design scan reports raspberrypi5_case CURRENT at rev_0003;
other designs remained untouched. Temporary inspection/staging files removed.
Documentation and journal synchronized; indexes regenerated and checked.
No pending downtime reports. Local implementation items 1..9 complete; item 10
closed pending separate Git/publication authorization. Proposed task commit:
`Add Raspberry Pi base mounting screw-head recesses`. No commit or push made.

build_manifest.json SHA-256: fb2d5c844d6129cf1da47c1a9fb4e01675882f337a40708f35abb1d304351d50.

assembly_review_manifest.json SHA-256: 15d3523202cbdc4a19967aa65c395657cc30ffd017c291cfb6427ecc46ae2af0.

## Git checkpoint authorization

User approved the proposed commit and push with "yes go ahead". Approved message:
`Add Raspberry Pi base mounting screw-head recesses`. Scope: completed rev_0003
source/config, verification/compatibility records, design README, verifier,
archived plan/index, journal and all governed mutable output artifacts. The
printed lid remains unchanged. Immutable numbered publication is not included.
