# rev_0002 artifact-bound assembly review

## Findings first

- The two reported faults are corrected in the digital candidate: forward side
  station axes are Y=40, and a fifth printable part fastens all four rear-center
  corners through four independent M3 clamp points.
- Rail access passes the explicitly bounded diameter-8 envelope Y=5.8..28.
  It is not a full-depth equipment clearance claim; side connectors begin Y=31.
- No unexpected product shells, missing leaves, clipped/blank review images or
  unintended hardware openings were found in the reviewed installed artifacts.
- Physical PLA fit, actual printer/profile, clamp torque/retention, slicer paths,
  ring supports, plate-border cantilever behavior and payload remain unverified.
  These remain release blockers. No immutable revision or fabrication-ready claim.

## Provenance

- Candidate/config: rev_0002, designs/6u_cyberdeck/configs/rev_0002.json.
- Recorded Git: 25ee2c84a4bbbfa3a0880f2bc30b37756ff9dcb1, dirty working tree.
- Source SHA-256: `d680fe76896ee40de32e3623f04ffa4801a92f2579587f07f8c7e8cb7f00cc4b`.
- Config SHA-256: `462adbce37909e72b5dc47f0f3fd18059244148f306e444b223a46ed25052cb4`.
- parts.json SHA-256: `34d1ecde1805a8bd0e1eac511d65d2689923d4e98573ff68e18d4fe449b96ec8`.
- assembly.json SHA-256: `238c2f08fc33285a39090ef76eadda4738680cecad6ab35da4c77d4e915df928`.
- Build-manifest SHA-256: `747b894777523e4faf29944abcaa8d48452b9a6611100ed5304328af90d8387e`.
- Assembly-review-manifest SHA-256: `82f4a9034a2958c99761bf6678116a297d5e66ce1d21897cca29b40f49836b03`.
- Review manifest: output/6u_cyberdeck/assembly_review_manifest.json, full set.
- Reviewer: Codex; exact-artifact user approval remains pending.

## Canonical hierarchy

| Logical owner | Printable coverage | Role | Result |
|---|---|---|---|
| enclosure_assembly | IDs 1..4, one quadrant each | four case leaves with integral rear pads | PASS |
| rear_fastening_bridge | ID 5 rear_center_bridge | removable four-point center tie | PASS |

Both owners appear in isolation and in the product/exploded views. The seam
coupon is a declared two-piece test export, not part of the product hierarchy.
The unsplit source export represents the case alone; the bridge is independently
verified, not silently included in split/master case volume comparison.

## Interface findings

| Interface | Evidence | Result |
|---|---|---|
| top_seam | stations 0/1, unchanged Y=18/71, independent local root/bore/shoulder/end sections | PASS nominal |
| bottom_seam | stations 2/3, unchanged Y=18/71, independent local sections | PASS nominal |
| left_seam | stations 4/5, Y=40/71, moved forward joint and independent local sections | PASS nominal |
| right_seam | stations 6/7, Y=40/71, moved forward joint and independent local sections | PASS nominal |
| rack_front | 36 bores/floors; 1188 mesh-axis samples in declared service cylinders plus full source-bound separation proof | PASS bounded access |
| rear_center_clamp | four aligned independent pad/bridge clamps; separate owner transforms and bearing sections | PASS nominal |

| Rear clamp point | Quadrant | Verified local path |
|---|---|---|
| X=-12, Z=-12 | bottom left | 3 mm plate -> 4 mm web -> full rear skin |
| X=12, Z=-12 | bottom right | independently measured plate/web/skin/bore/pocket |
| X=12, Z=12 | top right | independently measured plate/web/skin/bore/pocket |
| X=-12, Z=12 | top left | independently measured plate/web/skin/bore/pocket |

These are fastened interfaces between separate prints. Coincident bearing faces
or sub-micron STL rounding gaps are not counted as positive structural unions;
M3 screws transfer clamp load. Positive structural pad/skin overlap remains
within each leaf. Final physical interface acceptance remains BLOCKED_UNKNOWN.

## Visual review and installation

Reviewed all 85 installed product PNGs, then all 27 installed supplementary PNGs.
The assembled/isolation/exploded views show the fifth part and relocated side
pads. Rear-center inside, pads-only, exterior nut access and normal-Z clamp
section expose both sides and the actual printed bearing material. No opaque
hardware proxy substitutes for geometry. Front/rear orthographic views are
silhouettes through the solid rear wall; oblique/isolation/section views carry
internal-detail evidence. CGAL renders do not retain owner colors at contacts.

Assembly remains columns along Z, then columns together along X. Install the
rear bridge from the front, seat it on four pads, insert nuts through the rear
and tighten from inside before equipment. Nominal plate insertion sweep is
clear by construction and 16 exported-mesh axis checks; four driver sweeps have
64 circumference checks. Exterior nut access is outside the measured case bounds.
Physical tool reach, torque and removability must still be tested.

## Independent geometry

- Five authoritative STLs: one closed connected positive-volume shell apiece.
- Case and assembled bounds: [-127,0,-146.95]..[127,80,146.95] mm.
- Bridge print bounds: nominal [0,0,0]..[48,48,3] mm, within 0.002 mm numeric
  comparison tolerance (one exported bed coordinate is -0.000000191 mm).
- Largest conservative leaf print bound remains 141 x 160.95 x 80 mm.
- All 36 rail holes and 3 mm pocket floors pass. Service diameter 8 mm from
  Y=5.8..28 is free; moved pad front Y=31 gives 3 mm reserve. This corrects the
  captured rev_0001 obstructions at Y=9..27 in rev_0002_regression_baseline.json.
- 114 station/coupon/rear-clamp/material sections pass, including
  all pad webs, 3 mm plate, pad bore/pocket lands and plate bore/edge ligaments.
- Four screws have nominal full 2.4 mm nut engagement; tip Y=79.7 leaves 0.3 mm
  within the unchanged rear exterior. No hidden axial air gap is clamped away.
- 84 split/master case sections pass at 0.005 mm comparison tolerance; max
  boundary delta 0.002414794 mm.
  Local dimensional checks retain 0.002 mm tolerance; neither is fit clearance
  or Boolean epsilon. No structural minimum was reduced.
- Case volume difference 0.064816381 mm3, below
  unchanged 0.1 mm3 limit. Separate bridge volume excluded explicitly.
- Existing production-derived station coupon remains exactly two closed pieces.

## Results and artifact contract

- Canonical decomposition, five-leaf coverage, nominal transforms and bounded
  rail/bridge installation checks: PASS digital.
- Structural joins/supports: unverified for fabrication; digital local minima pass.
- Minimum internal edge/material width: unverified for fabrication; digital checks pass.
- Physical interface acceptance: BLOCKED_UNKNOWN; user assembly approval: pending.
- Complete build and full review audits: PASS; config/source/authoritative STL
  provenance matches the same installed state.
- Expected/actual product: 5/5 STL + 85/85 PNG.
- Expected/actual supplementary: 3/3 STL + 27/27 PNG.
- Unified expected/actual: 8/8 STL + 112/112 PNG + 2 manifests = 122 flat files.
- No transient contact sheet, directory or SCAD source remains in final output.
- No immutable publication, commit or push performed.
