# Cicero complete-product assembly review

Result: geometry/artifact checkpoint passed; fabrication approval **pending**.
Physical fit, structural strength, global minimum widths and continuous swept
clearance remain unverified. No loose connectors, missing subassemblies or bare
neck are accepted as a complete product.

- Design: cicero_joined
- Candidate: mutable `configs/rev_0001.json`; no immutable revision published.
- Product: cicero, containing logical head and bust subassemblies.
- Reviewer: Codex, installed artifacts and independent mesh checks.
- Review set: full (25 views, three nonprintable geometry exports).
- SCAD source: `designs/cicero_joined/src/main.scad`; SHA-256 `28e00edc1691f3733f3cca5ceed1b1f6ffb6b558d97c0020de4410bfd02145c7`.
- Config: `designs/cicero_joined/configs/rev_0001.json`; SHA-256 `e69427fed878b63ff08d4fd5babd7e1693f6f8949f3aa2f67e4dae02465fea2a`.
- Parts manifest: `designs/cicero_joined/parts.json`; SHA-256 `4301bc74ab82d30fb7a43bed5540bd89d4c881c17b8f6bbf0db1c6094c0f3187`.
- Assembly contract: `designs/cicero_joined/assembly.json`; SHA-256 `2bf83109df66e6c15e78ffe90d0a810c5b93e971d9abf72667a94b5d634d1494`.
- Geometry provenance: `designs/cicero_joined/geometry_manifest.json`; SHA-256 `dab354bdabf66ba3274a75d5040986ba25bdf70add7b98d622f5b9555f843385`.
- Installed build manifest: `output/cicero_joined/build_manifest.json`; SHA-256 `178bc0c37b7aad28416a40cd8e81d8da5b87bca79293909bfed1720ae8a6e6e2`.
- Assembly review manifest: `output/cicero_joined/assembly_review_manifest.json`; SHA-256 `d27eddae4406ca77787c14a0bf3757965f5d9b4b6678d8a6fab67f56eb21a6d7`.
- Independent verification: `designs/cicero_joined/verification.json`; SHA-256 `47ae0fcd152ef1fd0508eae890caf4fa608b88bcf6b25f3cc20d3a52451076a1`.

## Hierarchy and interfaces

| Assembly | Printable owners | Result |
| --- | --- | --- |
| Head | face, neck collar, left/right lower, left/right upper | six present |
| Bust | four lower, six upper, continuous neck plate | eleven present |
| Complete product | head plus bust | seventeen present; zero connector-only leaves |

The independently discovered 33 shared-cap mating pairs equal the declared
33 integral joints. Every joint passes feature-presence, own-root stock probes,
receiver-void probes and closed-stop probes on geometry matched to the installed
exports. All connector loading/slide samples pass. Sixteen full-part/subassembly
installation stages pass sampled collision checks (seven states each), including
whole-head installation on the completed bust. Worst sampled whole-model overlap
is 0.009958 mm3, below the 1 mm3 diagnostic threshold; connector limit is 0.1 mm3.
Only 0.02 mm contact-plane slabs are excluded diagnostically; no print gap is
introduced by that exclusion. These samples do not prove a continuous sweep.

The single major connection is b_neck male to h_neck female. Its 32 mm long,
32 mm flared, 8 mm engagement rail has 34 mm travel and a closed seat. Both
interface owners are continuous printed bodies. Two shorter internal bust-neck
rails avoid the rising shoulder: 8 mm length, 10 mm travel, unchanged 10/16/6 mm
throat/flare/engagement and 6 mm root. Earlier 20 mm travel collided with original
shoulder material and was rejected rather than hidden with a larger tolerance.

## Installed visual review

Reviewed installed face and neck part views, complete isometric, exploded,
bust-neck rail and head-neck socket views. The face remains intact and points up
in its print pose. The complete reference contains head and full draped bust;
the exploded reference exposes the intended body subdivisions and integral
features. No separate key or unintended isolated printable component is present.
The major male and matching socket are visible in their dedicated views;
assembled views naturally hide captured features. Some generic orthographic
views obscure the small joints and cannot alone establish their presence.
Numerical joint probes and topology checks supplement that visual limitation.

All seventeen installed STL leaves are closed, consistently wound single shells,
match their generated assets within 0.002 mm, and have actual flat bed contact
above 1000 mm2. All transformed bounds fit the 220 mm cube with at least 5 mm XY
margin; the central upper bust pieces reach 219.6 mm Z. No bounding-box tilt is
used to elevate a broad base. Local overhang supports still need slicer review.

The assembled scan span is 437.54 x 342.234 x 568.999 mm. Ear span is
228.600190 mm. Original intermediate source geometry and imported dependencies
are separately hash-bound by geometry provenance and independent verification.
Inherited overlapping bust shells are unioned; local duplicate vertex fans are
separated by no more than 0.008 mm on three leaves, recorded in provenance.
Assembly-reference exports are concatenated inspection geometry, not printable
unions and not substitutes for individual topology checks.

## Audit and remaining gates

Expected and actual complete output: 17 printable STL / 289 part PNG, plus
3 reference STL / 25 assembly PNG, two manifests: **336 flat files**.
Normal build audit, unified exact-set audit, full assembly review audit,
source/config/imported-asset provenance and original reference audit pass.

- Canonical decomposition: passed.
- Primary geometry/visual assembly review: passed for this engineering checkpoint.
- Interface presence and sampled installation: passed.
- Structural joins/load capacity: unverified.
- Minimum internal edge/material width: unverified globally; conservative local
  3.1 mm stock guards and later-subtraction inventories passed generation.
- Continuous swept clearance, anti-lift retention, slicer support review,
  calibrated production-derived coupons and headset stability: unverified.
- Fabrication approval: pending. No commit or push performed.

## Face correction and multi-angle review: 2026-10-18

The earlier face was too shallow: its rear cut exposed eye recesses. The current
plane offset is 25.61125149 mm, 5.94854745 mm deeper. Installed print dimensions
are 209.747 x 209.747 x 49.094 mm; the broad rear cut remains on the bed.
The unjointed cap has one contour; the installed rear view has no eye openings.
Independent post-joint probes at both old eye-contour centers find solid material
at 0.5, 1, 2, 3 and 4 mm from the rear plane. This is local backing evidence,
not a global thickness assertion. Face features remain on one piece.

A six-mm neck band now belongs wholly to the collar, including the local region
beneath the face. The face/collar pair has compound contact (main rear plane and
band-top plane), with its existing integral joint on the main plane. All sixteen
sampled assembly stages still pass. Single neck ownership and one major dovetail
are preserved. Recombining the collar produces 66 numerical zero-volume sheets,
with total absolute volume 4.104e-13 mm3; these are removed with a 1e-6 mm3 total
limit and exactly one volumetric-owner assertion. No real island is discarded.

Reviewed all ten new separate exploded views: head and bust/base each from
front-left, front-right, back-left, back-right and underside. They expose both
sides of the fabrication cuts across complementary views; individual views can
occlude some rear pieces. These reference poses do not prescribe print angles
or represent the installation swept paths. All six head and eleven bust leaves
are accounted for. Normal/unified/assembly audits pass: 20 STL, 314 PNG and two
manifests, 336 flat files. Config remains mutable rev_0001. Structural strength,
global minimum material widths, continuous sweeps and physical fit remain
unverified. No new fabrication approval is given.
