---
plan_id: 2026-10-04-11-35-16_create-6u-cyberdeck
title: Create 6u_cyberdeck 6U ten-inch-rack case (80 mm deep)
summary: Build a new standalone 6U ten-inch-rack case (254 x 293.9 x 80 mm outer, 222.25 x 266.7 mm clear opening) split into four printable quadrant leaves joined by M3 captive-nut registration seam stations; ring band 13.6 mm independently derived from the M3 station starting profile.
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
| Ring band (both axes, radial) | **13.6** | derived below |
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
140.6 x 160.55 x 80, fitting a 220 mm bed with >= 55 mm margin per axis; assert
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
  each printable leaf = master intersected with its strict quadrant ownership
  volume; no overlapping final solids, no coplanar slivers, no material
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

- [ ] Model master assembly once in assembly coordinates; derive 4 leaves by
      strict ownership volumes (X=0, Z=0 split planes, full depth).
- [ ] Classify every cross-seam feature with an ownership policy
      (`continuous_across_seam` / `<leaf>_owned` / `separate_bridge` /
      `intentionally_terminated`) in `docs/`.
- [ ] No overlapping final solids, coplanar slivers, or missing material at
      the seams; no unexpected disconnected shells.

### G4 — Station layout and hardware declaration

- [ ] Verify and fix station count + spacing per seam ribbon (candidate: 2 per
      ribbon, 8 total); each station inventory and role documented in
      `docs/`.
- [ ] Full hardware declaration: exact screw type/dia/head/length, nut
      AF/thickness/orientation, `head_side`/`nut_side`, washer OD/thickness,
      driver type + swept tool-access envelope, material/nozzle/layer basis.
- [ ] Every named station quantity (the 14 from the reference) present as
      named dimensions with `assert()`; fit clearance / structural engagement
      / boolean epsilon kept distinct.
- [ ] Sections normal to the seam through every station type; pairwise
      cut-to-cut and cut-to-edge ligament checks after all subtractions.
- [ ] Head-side / nut-side / assembly views with installation and tool paths
      verified in `docs/`.

### G5 — Structural verification

- [ ] Positive-volume structural engagement >= 3.0 for tongue root and
      receiver attachment after all cuts; overlap survives `difference()`.
- [ ] Every ligament between any fastener cut and edge/socket/other cut
      >= 3.0 on shortest solid-material path; report in `docs/`.
- [ ] Fastener cuts create no sub-minimum ligaments; remaining load path
      >= 3.0 at every join.

### G6 — Build, audit, review

- [ ] Complete manifest build via `python scripts/scad_build_all.py`;
      atomically installed to `output/6u_cyberdeck/`.
- [ ] `python scripts/scad_build_all.py --audit-only` passes.
- [ ] `python scripts/validate_cad_assembly_contract.py` passes on
      `assembly.json`; assembly review manifest records build-manifest hash
      and every authoritative STL hash.
- [ ] Review installed STL + PNG artifacts (complete build, audit, artifact
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

- [ ] Update `README.md`, `AGENTS.md` (design listing), journal checkpoint.
- [ ] Commit + push `output/6u_cyberdeck/` and
      `revisions/6u_cyberdeck/rev_0001/` per 2026-09-14 artifact directive
      (only with explicit approval).
- [ ] Completion summary per AGENTS.md section 12 (plan path, structural
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
