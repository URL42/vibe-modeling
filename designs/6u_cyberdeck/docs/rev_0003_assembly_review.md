# rev_0003 multipart assembly review

Digital geometry and artifact review passed. Fabrication readiness is unverified:
actual control bodies/wiring, PLA load/fit and slicer layer paths remain open.
User assembly approval is pending. No immutable revision, commit or push.

- Design: 6u_cyberdeck
- Candidate: `configs/rev_0003.json`
- Product: `product_assembly`
- Source SHA256: `5142d3d16bf4127ff0ccb4fbed132970ea0c030a890b89ac8f8fb08d3ecef303`
- Config SHA256: `bbe19ed52adb9e22aca33bd34bdfd0c2ae20813ff6a08cb228dccdb062d64ad3`
- Parts manifest SHA256: `e627d8d0a1a64743c22ae3463aecc4569f210044ce2999bb0ed9210243d6051e`
- Assembly contract SHA256: `5d523d62760fb806d68ac40ccfcf69a8d2e9f97a9b97f5a4b89d945ce28dde18`
- Build manifest SHA256: `f254bc29145a27cfa82cf7c8af40131a3f2ec59c7ce62539cb1b3eff7645ad4e`
- Assembly-review manifest SHA256: `f6a58ae4c1133d0e7975440719db3ba77d98659f022755dccf199a1d5391be67`
- Git snapshot: `25ee2c84a4bbbfa3a0880f2bc30b37756ff9dcb1`, dirty working tree
- Review: full, 34 installed PNG and 4 supplemental STL, Codex
- Review manifest: `output/6u_cyberdeck/assembly_review_manifest.json`

## Canonical hierarchy

| Subassembly | Printable leaves | Role | Result |
|---|---|---|---|
| enclosure_assembly | IDs1-4, four case quadrants | Retained enclosure | passed |
| rear_fastening_bridge | ID5, rear_center_bridge | Four-corner rear clamp | passed |
| control_cover | ID6 left, ID7 right | Removable lower-4U two-piece cover | passed |

All seven normal meshes have one closed positive-volume shell and consistent
winding. Coupons intentionally contain two separate components apiece and do
not add product leaves. No reference hardware is included in printable meshes.

## Interface findings

Results below refer to printed geometry; full device/service qualification is
separately blocked by the conformance matrix's explicit unknowns.

| Interface | Evidence | Findings | Digital result |
|---|---|---|---|
| top_seam | station_0/1_section, case sections | Both owners engaged, retained geometry | passed |
| bottom_seam | station_2/3_section, case sections | Both owners engaged, retained geometry | passed |
| left_seam | station_4/5_section, rail service rays | Forward joint Y40 leaves service access | passed |
| right_seam | station_6/7_section, rail service rays | Forward joint Y40 leaves service access | passed |
| rack_front | 36 bores, 1188 service rays, enclosure isolation | Both columns and nonuniform U sequence preserved | passed |
| rear_center_clamp | rear-center views, 4 clamp checks | Bridge meets four integral pad owners | passed |
| cover_center_seam | cover lower/upper sections, 196 material sections | Two captive-nut clamps, left-owned tongues, no duplicated volume | passed |
| cover_rail_attachment | installed product rays, cover front/back, isometric | Four bores align with rails; lower4U transform correct | passed |

## Visual findings

Reviewed all 119 installed normal PNG via seven temporary contact sheets, then
removed them before assembly generation. Reviewed all 34 installed assembly PNG
via three temporary contact sheets, and inspected full-size isometric, full front
and rear, isolated cover front and a cover clamp section. Temporary sheets were
removed before final audits.

No missing/duplicate printable leaves, truncated features, unintended floating
shells or unexplained cuts found. The panel has a grid in the upper left, diamond
in the upper right and centered joystick patterns in both lower regions.
Front-facing cover is face Y=-3, rear Y0, below the open upper2U.

Straight-on full-case front images look flat because the gold rear wall is
visible behind the holes with the same material shading. This is a render
visibility limitation, not filled control holes: isolated cover front/back images
show all holes, isometric shows installed position, and 44 independent installed
rays verify clear bores and surrounding face. Rear-view isolation mirrors the
left/right layout as expected. Thin clamp sections through a bolt axis split the
material at the intentionally open coaxial bore; they do not indicate a missing
bearing web. Offset sections measure the 4 mm web.

No opaque proxies obscure printable geometry. Each cover half has two rail
support positions and the center seam is joined at two ends; PLA stiffness and
loaded support adequacy still require testing. Right receiver roof bridging and
all case overhangs require slicer/coupon review. Complete hardware-body and
wiring removal paths remain unknown. Bench assembly and front module withdrawal
sequence are documented in rev_0003_verification.md.

## Independent geometry evidence

- Cover face: 254 x177.2 x3 mm, lower4U, 0.6 mm total height allowance.
- Left leaf: 141 x177.2 x3 mm; right:127 x177.2 x9.8 mm. Both fit confirmed
  220 mm printer with 5 mm per-side XY reserve.
- Full printed product bounds: X +/-127, Y=-3..80, Z +/-146.95.
- Cover: 196 material sections, 22 face-hole diameters checked in
  both axes, 34 panel-span sections, 9528
  analytical master/depth samples and 44
  installed product rays. No overlapping cover-owner volume detected at samples.
- Conservative face edge ligament: 4.250 mm;
  face-hole pair ligament: 8.062446 mm;
  tongue side land3.2, receiver shoulders/closed end3, clamp web4 mm.
- Cover coupon: 53 x24 x9.8 mm bounding set, two separately closed positive
  shells, production-derived cuts and 8 mm placement gap.
- Case rerun: 114 material sections,36 rack bores,1188 rail
  service rays,4 rear clamps,64 rear-driver rays,16 bridge-insertion rays and
  84 recombination sections.
- Case split/master volume difference: 0.064816381 mm3;
  boundary maximum: 0.002414794 mm.
  Existing case/bridge bounds, triangle counts and volumes match rev_0002. Byte
  hashes differ because OpenSCAD reorders ASCII facets; per-build hashes audit.

Machine-readable evidence: rev_0003_cover_measurements.json and
rev_0003_case_measurements.json. Rack interfaces have independent 80-row tables
in rev_0003_conformance_matrix.md. Both coupons still need physical testing.

## Artifact and readiness results

Complete normal build expected/actual: 7 STL /119 PNG. Supplementary full review
expected/actual:4 STL /34 PNG. Unified expected/actual:11 STL /153 PNG /2
manifests,166 flat files at `output/6u_cyberdeck/`, no directories or SCAD source.
Normal audit, assembly audit and contract/geometry validation passed. Config,
parts, source and installed STL provenance match; assembly review binds the exact
normal build-manifest hash and all seven authoritative STL hashes.

- Canonical product decomposition: passed.
- Primary assembly review: passed (digital printed geometry).
- Printed interfaces: passed; complete device/service interfaces: blocked_unknown.
- Structural joins/supports: unverified for fabrication; digital checks passed.
- Minimum internal edge/material width: unverified for fabrication; digital checks passed.
- Slicer/physical coupon and loaded PLA checks: unverified.
- Artifact/provenance audit: passed.
- User assembly approval: pending.
