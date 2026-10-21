---
plan_id: 2026-10-04-11-35-16_create-6u-cyberdeck
title: Create 6u_cyberdeck 6U ten-inch-rack case (80 mm deep)
summary: Build and correct a standalone 6U ten-inch-rack case (254 x 293.9 x 80 mm outer, 222.25 x 266.7 mm opening) with four quadrant leaves, M3 seam stations, forward side joints at Y=40 and a four-point internal rear-center bridge; physical validation and publication remain pending.
status: current
created_at: 2026-10-04-11-35-16
---

# 6u_cyberdeck 6U Ten-Inch-Rack Case

Key: `[ ]` pending task, `[x]` completed task, `[?]` needs validation, `[-]` closed task

## User Instruction (verbatim)

> i want to create a new model which is a 6u ten-inch rack, 80mm deep.

Approved scope answers:

- **Location**: new standalone design `designs/6u_cyberdeck/` (fresh lineage; NOT a
  cyberdeck-2 config variant).
- **Folder name**: `6u_cyberdeck`.
- **Outer height (ring)**: sized to fit the attachment joints that hold the
  quadrants together, per
  `playbooks/how_to_design_split_print_parts_and_verify_reassembly.md` and the
  M3 captive-nut registration seam station reference.
- **Split strategy**: 4-leaf quadrant split (seams at X=0 and Z=0 on the front
  face), joined by M3 captive-nut registration seam stations in the band between
  the rack opening and the case edge.

## Provenance

- Rack spec: `ten-inch-rack-m3-printed-design-spec` **v2.0.0**
  (`references/engineering/ten_inch_rack/v2.0.0/`).
- Bundle manifest SHA-256:
  `330051136930B54F0ABF91FF81EA217D0E6CAD2DBE6503375FFB219E59E0210D`
  (`references/engineering/ten_inch_rack/v2.0.0/bundle_manifest.json`).
- Station reference:
  `references/engineering/fasteners/m3_captive_nut_registration_seam_stations.md`
  (starting profile only; physically unverified; design prints its own coupon).

## Resolved Inputs (lock at approval)

| Quantity | Value | Basis |
|---|---|---|
| U pitch | 44.45 | spec v2.0.0 `u_pitch` (NORMATIVE_EXTERNAL) |
| Clear opening (X) | 222.25 | spec `rack_clear_opening_nominal` (width is U-independent) |
| Clear opening (Z) | 266.7 | 6 x 44.45 |
| Face width (X) | 254.0 | spec `rack_front_width_nominal` |
| Depth (Y) | 80.0 | user mandate; resolves spec `rack_internal_depth` UNKNOWN — record as user-mandated resolution in `docs/` |
| Station radial envelope / top-bottom band | **13.6** | derived allowance below; side front rails are 15.875 |
| Outer envelope | 254.0 x 80.0 x 293.9 | 266.7 + 2 x 13.6 |
| `minimum_wall_thickness` | 3.0 | host baseline |
| `minimum_structural_overlap` | 3.0 | host baseline (>= wall) |
| `minimum_internal_edge_width` | 3.0 | host baseline |
| `boolean_epsilon` | 0.02 | spec baseline |
| Fastener | M3x0.5 only; ISO 7089 washer ID 3.2 / OD 7.0 / t 0.5; finished hole 3.2-3.6; washer seat 8.25 (8.0-8.5); no countersunk primary heads | spec v2.0.0 |

### Ring derivation (independent; assert in code)

Radial band must carry the station stack across the seam. From the M3 station
starting profile:

- head-side recess depth 3.8
- tongue root structural engagement 3.0 (>= `minimum_structural_overlap`)
- socket tip clearance 1.0
- receiver closed-end wall 3.0 (>= `minimum_wall_thickness`)
- nut pocket depth 2.8 (pocket depth, not a wall)

**13.6 = 3.8 + 3.0 + 1.0 + 3.0 + 2.8.** Per-leaf footprint then
141 x 160.95 x 80, fitting a 220 mm bed with >= 55 mm margin per axis; assert
per-piece bounds in code. Nut pocket circumdiameter = 5.9 / cos(30 deg) ~= 6.82.

### Unknowns / open items

- Station count and spacing per seam ribbon: design-specific, derived from the
  M3 station reference and the band's clearances (not copied from any prior
  design); propose 2 per ribbon (8 stations) as candidate to be verified at the
  station-layout gate.
- Full M3 hardware declaration (exact screw, nut, washer, driver, swept
  tool-access envelope) — gate item G4; NEVER derive a recess from nominal
  "M3" alone.
- Fit tolerances: starting-profile clearances are unverified; production coupon
  required before final tolerance selection.

## Split-Prints Plan Binding (mandatory, per playbook)

- **Split planes**: front face at X=0 and Z=0, full depth (Y 0..80); rear
  closure follows the same quadrant ownership.
- **Ownership rules**: model the master assembly once in assembly coordinates;
  each printable leaf = master intersected with its strict ownership
  mask (quadrant plus assigned tongue extension, minus neighbouring owned tongues); no overlapping final solids, no coplanar slivers, no material
  duplicated or omitted across the seam.
- **Joining method**: M3 captive-nut registration seam stations in the radial
  band; tongue part owns registration tongue + root + M3 clearance passage;
  receiver part owns socket + passage + head-side recess + captive hex pocket;
  registration geometry is NOT a structural union; load path: tongue =
  registration/shear, M3 screw = clamp.
- **Print transforms**: each leaf flat on build bed, printed as modeled
  (band up / opening edge up); assert transformed bounds per piece fit the
  declared 220 mm bed with margin.
- **Assembled verification gates**: recombine vs unsplit master within
  tolerance; alignment/continuity/access/load-path checks; unexpected
  disconnected shells fail.

## Expected Files

- `designs/6u_cyberdeck/src/main.scad`
- `designs/6u_cyberdeck/src/lib/` (adapted rack helpers + station modules:
  `registration_tongue`, `receiver_socket`, `m3_through_passage`,
  `m3_head_recess`, `m3_captive_hex_nut_pocket`, `seam_station_coupon`;
  bundle v2.0.0 recorded in comments — reference SCAD is never imported
  directly)
- `designs/6u_cyberdeck/src/parts/<leaf>.scad` (4 leaves + master)
- `designs/6u_cyberdeck/configs/rev_0001.json` (flattened scalars incl.
  `rack_spec_version: v2.0.0`)
- `designs/6u_cyberdeck/parts.json`
- `designs/6u_cyberdeck/assembly.json`
- `designs/6u_cyberdeck/README.md` (links to the design; new standalone design,
  not solarpunk_)
- `designs/6u_cyberdeck/docs/` (resolved parameter manifest, conformance
  matrix, keepout inventory, depth-class report, fastener stack-up report,
  seam overlap + remaining ligament report, validation log, depth
  UNKNOWN resolution record)
- `output/6u_cyberdeck/` (complete manifest build, installed + audited)
- `revisions/6u_cyberdeck/rev_0001/` (immutable publication)

## Execution authorization and candidate definition (2026-10-18)

User authorized remaining execution: "ok finish the plan". This authorizes the
existing modeling/build/documentation items; physical printing and measurements
cannot be fabricated, and the existing explicit commit/push approval condition
still applies. Keep this plan current until those gates are resolved.

Baseline source-only checkpoint: `fc1ff8c`. Candidate: `rev_0001.json`; no immutable
revision destination exists. Rollback is to retain the mutable candidate/evidence,
not overwrite a published revision. Publication remains blocked by G7 and slicer
verification, irrespective of the ordering of G6/G7 below.

Hierarchy: product -> enclosure -> four quadrant leaves, IDs 1 bottom left,
2 bottom right, 3 top right, 4 top left. No additional logical components or
fabrication splits. Prohibited: separate rear lid, merged device modules, omitted
rack mounting columns. Ownership is quadrant shell plus explicitly owned crossing
tongues, with receiver sockets removing the corresponding volume from neighbours;
a bare quadrant intersection would truncate every registration tongue.

Station candidate: two per ribbon, eight total; Y=18 and 71. Ring depth 13.6
is the station radial envelope/top-bottom band. Front side bands are 15.875,
as independently fixed by 254 width and 222.25 opening. Socket tip clearance is
along insertion, not an axial gap in the clamp load path. Receiver bearing wall
is 4 mm. Exact hardware, clamp stack, cut pairs, supports and physical acceptance
criteria are in `designs/6u_cyberdeck/docs/verification.md`.

Manifest mapping: no former printable set -> four named product leaves. Expected
normal build: 4 STL + 68 PNG. `assembly.json` declares 22 full-review PNG and
3 supplementary STL (assembled product, unsplit master, production-derived coupon),
for final union 7 STL + 90 PNG + 2 manifests. Coupon is an intentional retained
inspection export; its two pieces are separate from the product hierarchy.

Review: installed complete artifacts first, then artifact-bound full review;
front/rear/left/right/top/bottom/isometric/exploded, enclosure and every leaf,
coupon and eight station sections. Independent installed-mesh checks cover bounds,
closed connectivity, bore/shoulder/root/end sections, 36 rack bores, and split/master
volume and section equivalence. Any source/config/manifest/interface change
invalidates prior affected review. Preserve physical/assembly approval as pending
where evidence is unavailable; never infer them from a successful artifact audit.

No immutable publication or commit/push until applicable gates and authorization
are satisfied. Unrelated Cicero work observed during execution is outside scope.

## Checklist

### G1 — Provenance and inputs

- [x] Run `python scripts/validate_ten_inch_rack_reference.py`; pass.
- [x] Record spec v2.0.0 + bundle manifest SHA-256 in plan and in
      `designs/6u_cyberdeck/docs/` parameter manifest.
- [x] Record `rack_internal_depth` = 80.0 user-mandated resolution in
      `docs/` (resolves the spec UNKNOWN blocking publication).

### G2 — Lock derived geometry

- [x] Assert ring = 13.6 derivation in code; all wall terms >= 3.0 asserted.
- [x] Assert outer envelope 254.0 x 80.0 x 293.9 and opening 222.25 x 266.7.
- [x] Assert each leaf's transformed print bounds fit the 220 mm bed with
      margin.

### G3 — Model master + leaves

- [x] Model master assembly once in assembly coordinates; derive 4 leaves by
      strict ownership volumes (X=0, Z=0 split planes, full depth).
- [x] Classify every cross-seam feature with an ownership policy
      (`continuous_across_seam` / `<leaf>_owned` / `separate_bridge` /
      `intentionally_terminated`) in `docs/`.
- [x] No overlapping final solids, coplanar slivers, or missing material at
      the seams; no unexpected disconnected shells.

### G4 — Station layout and hardware declaration

- [x] Verify and fix station count + spacing per seam ribbon (candidate: 2 per
      ribbon, 8 total); each station inventory and role documented in
      `docs/`.
- [x] Full hardware declaration: exact screw type/dia/head/length, nut
      AF/thickness/orientation, `head_side`/`nut_side`, washer OD/thickness,
      driver type + swept tool-access envelope, material/nozzle/layer basis.
- [x] Every named station quantity (the 14 from the reference) present as
      named dimensions with `assert()`; fit clearance / structural engagement
      / boolean epsilon kept distinct.
- [x] Sections normal to the seam through every station type; pairwise
      cut-to-cut and cut-to-edge ligament checks after all subtractions.
- [x] Head-side / nut-side / assembly views with installation and tool paths
      verified in `docs/`.

### G5 — Structural verification

- [x] Positive-volume structural engagement >= 3.0 for tongue root and
      receiver attachment after all cuts; overlap survives `difference()`.
- [x] Every ligament between any fastener cut and edge/socket/other cut
      >= 3.0 on shortest solid-material path; report in `docs/`.
- [x] Fastener cuts create no sub-minimum ligaments; remaining load path
      >= 3.0 at every join.

### G6 — Build, audit, review

- [x] Complete manifest build via `python scripts/scad_build_all.py`;
      atomically installed to `output/6u_cyberdeck/`.
- [x] `python scripts/scad_build_all.py --audit-only` passes.
- [x] `python scripts/validate_cad_assembly_contract.py` passes on
      `assembly.json`; assembly review manifest records build-manifest hash
      and every authoritative STL hash.
- [x] Review installed STL + PNG artifacts (complete build, audit, artifact
      review, then artifact-bound assembly review — in that order).
- [ ] Publish immutable `revisions/6u_cyberdeck/rev_0001/`.

### G7 — Fit coupon (pre-release gate)

- [ ] Production-derived `seam_station_coupon` printed in intended
      material/orientation/nozzle/layer/walls; measure insertion force,
      actual clearance, nut retention, head seating, driver access, clamp
      behavior, failure location; record in `docs/` validation log.
- [ ] Select final fit tolerances from coupon data (do not freeze
      starting-profile values before this gate).

### G8 — Governance closure

- [x] Update `README.md`, `AGENTS.md` (design listing), journal checkpoint.
- [ ] Commit + push `output/6u_cyberdeck/` and
      `revisions/6u_cyberdeck/rev_0001/` per 2026-09-14 artifact directive
      (only with explicit approval).
- [x] Completion summary per AGENTS.md section 12 (plan path, structural
      joins status, min internal edge status, exact revision/config, build
      scope, destination, STL/PNG counts, audit + provenance results).

## Verification

- Plan index regenerates clean:
  `python scripts/regenerate_plan_indexes.py --check --repo-root .`.
- All `assert()` statements in source pass at render.
- Manifest audit passes on the installed output.
- `designs/6u_cyberdeck/docs/` evidence complete for every required output in
  the spec `required_outputs` list.
- No `UNKNOWN` remains unresolved for the published revision.

## 2026-10-18 digital checkpoint

The user's remaining-plan execution authorization is recorded above. G3 ownership,
G4 candidate hardware/layout/named dimensions, and G5 local geometric minima are
implemented. Installed first-build independent mesh checks passed for four closed
connected leaves, 36 rack passages and ten bounded sections per station, including
root start/mid/end, receiver bearing wall, side shoulders and closed end. These
checkboxes describe digital geometry, not slicer, physical fit or strength approval.
Final-source rebuild is in progress after correcting coupon bed orientation and
conservative tongue print-bound assertions.

Discovered blocker: `scripts/scad_render_assembly_review.py` currently stages under
`.tmp/scad/<design>/`, contrary to canonical root AGENTS.md. Requested a narrowly
scoped plan extension to move its managed stage under `output/<design>/` and run
existing regression tests. Approval is pending; no shared automation edits made.
Do not run the conflicting renderer or publish an immutable revision until fixed.
Physical coupon/calibration, slicer evidence and commit/push approval remain open.

## Approved G6 staging extension (2026-10-18)

User reply: "Approve the staging-path fix". Also selected PLA, 0.4 mm nozzle and
"-.2mm layers", interpreted as positive 0.2 mm layer height. Four walls remain
an unverified candidate setting; printer/profile and measurements remain unknown.

- [x] Move only the assembly renderer's managed stage to the canonical current
      design output; preserve exact-set audits, rollback, cleanup and CLI/schema.
- [x] Add a regression covering the managed stage location and cleanup on render
      failure; run existing assembly, unified-output and build-view tests.
- [x] Synchronize the applicable staging instructions in the iteration, complete
      build and automation-modification playbooks; document the correction.
- [x] Run the complete artifact-bound full assembly review and both audits on
      6u_cyberdeck rev_0001; independently compare split leaves with unsplit master.

Affected automation: scripts/scad_render_assembly_review.py only. Existing
scad_build.py/scad_build_all.py/scad_new_revision.py CLIs, schema and destinations
remain unchanged. Review staging may be ignored only while the command is active;
final output must be flat. Rollback must restore old review files and preserve
printable artifacts; tests use temporary roots/paths with spaces. Representative
new-design complete build/dry run and audit provide production integration checks.


Staging extension implemented; 15 relevant regression tests passed. Review views
now use inverse-transformed installed leaf STLs, rather than repeating source
Booleans, while the independent unsplit-master export stays source-derived.
This changes review implementation, not product geometry or hierarchy. Complete
rebuild is required to bind the final source state. PLA, 0.4 mm nozzle and 0.2 mm
layers are now the recorded user-selected fabrication basis. Support/bridging and
physical fit evidence remain pending; no fabrication-readiness claim is made.


## Final current checkpoint (2026-10-18)

G1-G5 digital work is complete; G6 complete build/audit, installed-artifact review
and artifact-bound full assembly review are complete. The approved staging fix
and all four extension items are complete; 15 regression tests pass. Earlier
in-progress/blocker notes above are historical and superseded by this checkpoint.
G8 documentation, journal and summary record are complete. No lifecycle move:
this plan remains current for required follow-up execution.

Reviewed config: designs/6u_cyberdeck/configs/rev_0001.json. Complete build and full
review installed into output/6u_cyberdeck/ and both audits passed. Expected/actual
product = 4/4 STL + 68/68 PNG; review = 3/3 STL + 22/22 PNG. Unified = 7/7 STL +
90/90 PNG + two manifests = 99 files, no directories or transient source. Config,
source and authoritative STL provenance match. Independent measurements pass four
closed connected product shells, 36 rack passages/pocket floors, 83 station/coupon
sections, two closed coupon pieces and 84 recombination sections. Split/master
volume difference 0.065525421 mm3; maximum section-boundary difference 0.002414794
mm under the documented 0.005 mm mesh-comparison tolerance. Local material checks
keep their original 0.002 mm numeric tolerance; no geometry/minimum was relaxed.

Evidence: designs/6u_cyberdeck/docs/assembly_review.md,
designs/6u_cyberdeck/docs/geometry_measurements.json and verification.md.
Structural joins: unverified for fabrication. Minimum internal edge/material
width: unverified for fabrication. Local digital minima/sections pass; actual
PLA/profile calibration, slicer paths/support strategy and G7 physical coupon
measurements remain required. User assembly approval is pending exact-artifact
review. Do not freeze final tolerances or publish an immutable revision yet.

Still open: G7 physical test/tolerance selection, slicer verification, G6 immutable
publication, and G8 explicit commit/push approval. No commit or push performed.
Suggested candidate checkpoint commit: Build the four-part 6U cyberdeck candidate.
No pending downtime reports beyond the directory README. Preserve unrelated
Cicero design/plans/journal changes and the unrelated b_neck 3MF artifact.


## Proposed correction checkpoint: rail access and rear center (pending approval)

User reported that the two forward side stations obstruct the rail openings and
that the four rear-panel corners have no fastened connection at their meeting
point. The earlier nominal assembly acceptance does not cover these findings:
rail access and rear-center load transfer are now failed/incomplete. The existing
artifact hashes remain historical evidence, not acceptance of the reported faults.

Diagnosis: side forward station axes are at Y=18 with pads Y=9..27. Their X/Z
projection overlaps rack-column hardware access. The rear center X=0/Z=0 is only
a pair of unfastened butt seams; perimeter stations do not directly clamp the
four meeting corners. Prior bore checks tested the front rail thickness, not a
complete installation/service sweep; add that missing regression explicitly.

Proposed atomic strategy, subject to user approval:

- [x] Move the two forward SIDE station axes from Y=18 to Y=40 (the side's
      front-to-rear midline). Leave top/bottom and rear stations in place. Verify
      actual rack screw/nut/driver access sweeps, not only distance between cuts;
      document the reserved service depth and any equipment-integration limits.
- [x] Add one removable interior rear-center bridge plate, initially 48 x 48 x
      3 mm, with four M3 fasteners: one supported pad on each rear quadrant.
      Keep the 254 x 293.9 x 80 mm exterior envelope. Derive the plate offset,
      integral pad depth, nut capture and screw length from the full stack so
      neither heads nor tips protrude beyond the case. Maintain 3 mm overlap,
      floor/throat and shortest material width after all cuts. Final exact pad
      positions/stack are to be verified, not accepted from this sketch.
- [x] Change the authoritative set from four leaves (IDs 1..4) to those same
      four identities plus rear_center_bridge (ID 5). Declare the bridge as a
      separate logical fastening component and show it in isolation/exploded
      views. Require explicit approval of this fifth-part decomposition.
- [x] Create candidate configs/rev_0002.json; retain rev_0001 config and evidence
      as historical, but do not claim the previous shared-source hash remains
      reproducible after source changes. Do not publish any immutable revision
      while physical/slicer requirements remain unresolved.
- [x] Update affected geometry/defaults/dispatch, parts.json, assembly.json,
      design README, verification/conformance/review records, measurement script,
      root navigation, this plan and append-only journal. Preserve unrelated work.
- [x] Build/audit all five product parts through the scoped automatic pipeline,
      review installed STLs/PNGs, then regenerate/audit full artifact-bound review.
      Expected normal output: 5 STL + 85 PNG. Derive supplementary counts from
      the revised assembly contract before building; final output must be flat.
- [x] Independently verify five product shells/bounds/bed contact, side-station
      locations and full rail hardware sweeps, all four rear-center clamp paths,
      boss/plate cut ligaments, installation/tool access and assembly/removal
      sequence. Update split/master comparison to account explicitly for the
      separate bridge. Retain PLA/0.4 mm nozzle/0.2 mm layer physical gates.

No geometry, config, manifest or generated artifact changes are authorized by
this proposed extension until approval. User approval is required by root
AGENTS.md section 3 for materially revised work and by the decomposition
playbook for adding a fabrication part/interface owner. No commit/push requested.


### Correction authorization

User approved the proposed correction with "go ahead". Execute the correction
checklist above as an approved current-plan extension. Candidate rev_0002 adds
part 5 rear_center_bridge; product -> enclosure (four leaves) + rear fastening
bridge is the approved hierarchy. Retain the 80 mm exterior, with the bridge and
heads inside the case. Proposed resolved bridge stack: 48 x 48 x 3 plate at
Y=70.2..73.2; four integral 14 x 14 pads at X/Z=+/-12, Y=73.2..80; rear-entry
2.8 mm nut pockets at Y=77.2..80; 4 mm bearing web. M3x10 + 0.5 washer + 2.4 nut
leaves tip Y=79.7. Confirm all by exported geometry. Rear plate load path crosses
both center seams through four independent clamps. Rail rear-access envelope:
diameter 8 mm from Y=5.8..28; moved side pads start Y=31, giving 3 mm reserve.
This declares a bounded hardware service envelope, not clearance for unspecified
full-depth equipment. Add isolation/inside/rear-center section views; derive and
record full review counts in assembly.json before building.

Correction artifact contract before build: five product parts, 5 STL + 85 PNG;
27 full review PNG + three supplementary STL. Unified exact set: 8 STL + 112 PNG
+ two manifests = 122 files. assembly.json validator passed (3 assemblies, 5 parts,
6 interfaces, 27 views). rev_0001 source/config evidence is labeled historical.


### Correction completion checkpoint (rev_0002)

All seven approved digital correction checklist items are complete. Forward side
stations are at Y=40 with pads beginning Y=31; all 36 declared diameter-8 rail
service cylinders pass Y=5.8..28 (1188 independent mesh-axis samples plus source
bounds). Four rear-center corners now have independently checked pad/plate M3
clamps through the separate fifth printable part. Five closed connected product
shells, 114 station/material/coupon sections, 64 rear driver and 16 plate insertion
checks pass. 84 case split/master sections pass; case volume difference is
0.064816381 mm3 under the unchanged 0.1 mm3 limit. Bridge volume is deliberately
excluded from the unsplit-case comparison and checked independently.

Complete build and full artifact-bound review installed into output/6u_cyberdeck/;
both audits and config/source/authoritative STL provenance pass. Expected/actual
product: 5/5 STL + 85/85 PNG; supplementary: 3/3 STL + 27/27 PNG; unified 8/8 STL +
112/112 PNG + two manifests = 122 flat files. All installed product/review image
classes reviewed, including plate isolation, rear pads without plate, rear nut
access and normal-Z clamp section. Temporary contact sheets removed.

Exact reviewed config: designs/6u_cyberdeck/configs/rev_0002.json. Evidence:
designs/6u_cyberdeck/docs/rev_0002_verification.md,
rev_0002_assembly_review.md, rev_0002_geometry_measurements.json and the captured
rev_0001 obstruction in rev_0002_regression_baseline.json. Earlier rev_0001 final
checkpoint is historical and does not describe the corrected current artifacts.

Structural joins: unverified for fabrication; local digital checks pass.
Minimum internal edge/material width: unverified for fabrication; local digital
checks pass. Keep this governing plan current for physical PLA/slicer/calibration
and user exact-artifact review, final tolerance selection, immutable publication
and explicit commit/push approval. No immutable revision, commit or push performed.
Suggested checkpoint commit: Clear 6U rack access and fasten the rear center.

## Lower-4U Control-Cover Extension

- User approved the separate atomic plan `plans/current/2026-10-18-23-59-27_6u-cyberdeck-4u-control-cover.md` with "ok go ahead". That plan governs rev_0003 addition of two removable control-cover leaves; this parent retains the case/physical/publication work. IDs 1-5 remain stable; IDs 6-7 are the cover. The legacy joystick pattern was recovered under the early cyberdeck auxiliary lid cuts (30 mm center, 80 x 40 mm rectangle of 3.4 mm mounting holes).
