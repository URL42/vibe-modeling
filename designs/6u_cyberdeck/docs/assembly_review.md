> Historical rev_0001 record. The current shared source and manifest target rev_0003;
> this record does not approve or reproduce the corrected geometry. See [rev_0003 verification](rev_0003_verification.md).

# rev_0001 multipart assembly review

## Findings first

- Release is BLOCKED_UNKNOWN: printed PLA coupon/calibration and actual slicer
  layer/support evidence do not exist. Do not publish an immutable revision or
  call the design fabrication-ready.
- Front-ring overhangs need support or validated bridging; socket/sideways bore/
  nut-pocket paths need layer review. No physical load rating is established.
- Digital decomposition, four-leaf coverage, nominal transforms, inspected
  sections and artifact provenance passed. No unexpected shells, missing leaves,
  unintended openings or truncated registration tongues were found.
- Physical clearances, captive-nut retention, tightening torque and material
  strength remain unverified. Zero nominal separation at the bearing face is
  intentional; outer-face, side and tip clearances are separate dimensions.

## Provenance

- Design: 6u_cyberdeck; candidate rev_0001.
- Config: designs/6u_cyberdeck/configs/rev_0001.json.
- Primary assembly: product_assembly; review set: full; reviewer: Codex.
- Recorded Git checkpoint: 25ee2c84a4bbbfa3a0880f2bc30b37756ff9dcb1; working tree dirty.
- Source SHA-256: `1c9885f1c73ae10ec16a095b85d9ba22f3b7db233b8e279401af6838fbe4ee62`.
- Config SHA-256: `6b0a07e115b08c82fdb3fd95357a4a99c956592c6919220d499882060176e21e`.
- parts.json SHA-256: `7acf2539c18a47f7917120392577557930dcd79d8f87a8bf9ae8f6c6ffd34d22`.
- assembly.json SHA-256: `edd7b95d65c7105983cc1be92345f175831d770e2b0ff9f5c5d3ed452fa7a371`.
- Build-manifest SHA-256: `a714689713241b89d7762b448481a45a80c3bd62a56ed42de3a84e0e5068b98f`.
- Assembly-review-manifest SHA-256: `acaf343d2e4bdf3b14472ce67492014c8ea28bced8094796cf771c0aa942d5f3`.
- Review manifest: output/6u_cyberdeck/assembly_review_manifest.json.

## Canonical hierarchy

| Logical subassembly | Printable leaves | Expected role | Present | Result |
|---|---|---|---:|---|
| enclosure_assembly | bottom left, bottom right, top right, top left | one closed-rear rack case | 4 | PASS |

No extra rear lid, electronics module or positive reference proxy is present.
The coupon is an inspection/test export with two intentionally separate pieces;
assembled and unsplit-master STLs are comparison artifacts, not product leaves.

## Interface findings

| Interface ID | Both sides / transform | Gap/collision and engagement evidence | Result |
|---|---|---|---|
| top_seam | correct | stations 0/1; 14 mm insertion, 1 mm side/tip gaps; root/bearing sections | PASS digital; physical BLOCKED_UNKNOWN |
| bottom_seam | correct | stations 2/3; same nominal dimensions, independent mesh sections | PASS digital; physical BLOCKED_UNKNOWN |
| left_seam | correct | stations 4/5; same nominal dimensions, independent mesh sections | PASS digital; physical BLOCKED_UNKNOWN |
| right_seam | correct | stations 6/7; same nominal dimensions, independent mesh sections | PASS digital; physical BLOCKED_UNKNOWN |
| rack_front | correct | both X columns, all 36 through passages and 3 mm pocket floors measured | PASS nominal; physical fit BLOCKED_UNKNOWN |

## Visual findings

Reviewed all 68 installed product PNGs and all 22 installed assembly PNGs,
including isometric/exploded, four leaf isolations, enclosure isolation, coupon,
and eight normal station sections. No blank or clipped artifact was found.
Orthographic front/rear are silhouette views because the solid rear is behind
all front openings; oblique/isolation views and independent sections provide
front interface detail. No opaque proxy obscures printable geometry.

Separate owner STLs and the exploded view expose the four quadrant boundaries;
CGAL assembled views merge contacting surfaces and do not preserve owner colors.
Rear panels and perimeter walls align. All observed openings match the declared
rack, socket, bore, head-recess and nut-pocket inventory. There are no floating
positive shells in a product leaf. Slicer support continuity remains unverified.

Nominal assembly: join each vertical column along Z, then slide the right column
onto the two left-column X tongues; install nuts and screws before equipment.
Reverse for removal. Straight driver and nut insertion sweeps are declared in
verification.md; physical service/tool fit remains a coupon gate.

## Independent installed geometry

- Every product leaf is one closed connected positive-volume shell with consistent
  winding and Z=0 bed datum. Bounds are in geometry_measurements.json.
- Combined and unsplit bounds: [-127,0,-146.95]..[127,80,146.95] mm.
- Coupon: [0,0,0]..[49,13.6,18] mm; exactly two closed connected pieces.
- 36 rack bores and their 3 mm front bearing webs checked.
- 83 bounded station/coupon sections checked, including roots at
  start/mid/end, tongue side ligaments, receiver shoulders, closed ends and bores.
- Recombined/unsplit volume difference: 0.065525421 mm3,
  below the 0.1 mm3 comparison limit.
- 84 independent recombination sections checked;
  maximum boundary difference 0.002414794 mm.
  Near-tangent ASCII-STL rounding exceeded the initial 0.002 mm comparison threshold;
  a complete diagnostic census found maximum 0.002415 mm. The recorded 0.005 mm
  recombination-only tolerance accounts for this; local material checks retain
  their original 0.002 mm numeric tolerance. No geometry or structural minimum
  was changed to pass a measurement.

## Results

- Canonical decomposition / printable coverage / nominal transforms: PASS.
- Primary assembly digital review: PASS; user approval state: pending.
- Interfaces: PASS nominal geometry; physical acceptance: BLOCKED_UNKNOWN.
- Structural supports/joins: unverified for fabrication (slicer/physical gates).
- Minimum internal edge/material width: unverified for fabrication; local digital
  minima and post-subtraction sections passed at the declared 3 mm floor.
- Artifact/provenance audits: PASS, source/config and all authoritative STL hashes.
- Expected/actual product artifacts: 4/4 STL and 68/68 PNG.
- Expected/actual supplementary review: 3/3 STL and 22/22 PNG.
- Unified expected/actual output: 7/7 STL, 90/90 PNG, two manifests, 99 files;
  flat directory, no transient source, stage or contact-sheet file remains.
- Immutable publication: blocked; no numbered revision directory created.
