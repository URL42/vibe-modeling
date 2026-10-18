# Cicero head assembly review record

Result: geometry candidate reviewed; fabrication approval pending.

- Design: cicero_head, head-only product/subassembly scope; bust excluded.
- Config: mutable configs/rev_0001.json; no immutable revision published.
- Reviewer: Codex; installed artifacts reviewed after complete manifest installation/audit.
- Canonical hierarchy: one head assembly, six body leaves and two separate spline keys; all present.
- Structural joins: unverified.
- Minimum internal edge/material width: unverified.

## Provenance

- Build manifest: `output/cicero_head/build_manifest.json`, SHA-256 `22808d8aa8859478675f1de19fbf959056fe777512ec4f3b3c099557587d9fbb`.
- Assembly review manifest: `output/cicero_head/assembly_review_manifest.json`, SHA-256 `375b66031ed39f2706613f7ae039b78d6bbfe4a832ec348abc1a94424299e01e`.
- SCAD entrypoint: `designs/cicero_head/src/main.scad`, SHA-256 `35dd91e54b62e6582c8d6c6967cdb710e12f69801ff5525e79c7005587daf696`.
- Config: `designs/cicero_head/configs/rev_0001.json`, SHA-256 `dabc83b4a432e895770149cd6fdf520a9261dacad8d1a3ef9d2d97737c244b01`.
- Parts contract: `designs/cicero_head/parts.json`, SHA-256 `b9a02399ac3ef0141c4bdd9c9385276d1b870717598802e05907de0760512fcb`.
- Assembly contract: `designs/cicero_head/assembly.json`, SHA-256 `8da5e41e9993f5fee124054aa45d744cc26ee30b8234886f73899a9fdd7aedd5`.
- Imported-asset provenance: `designs/cicero_head/asset_provenance.json`, SHA-256 `d8f4f0c0b68e6780b9db9423fde3b5fe793a4441b5255bf554004ba996ac59ed`.
- Geometry verification: `designs/cicero_head/verification.json`, SHA-256 `051e7ea7539e9b07dcffbfa36c047b1ab3a40cb4883f89a8f463264af83ff636`.

## Installed artifact findings

Reviewed installed face top/underside, neck-owner top/underside, rear leaves and
key views; then assembled front/isometric, exploded, face-socket and exposed-rear
views from the full artifact-bound assembly set. Features are present on both
mating sides, broad bed faces remain, face/eyes/nose/mouth/chin remain recognizable,
and the revised neck band is carried by the continuous neck owner. No visible
external floating structure or missing body region was found. Separate spline
keys and reference-assembly components are intentional, not fused print geometry.
Some straight-on bottom views have weak cavity contrast; oblique underside views
show the sockets and loading pockets. No proxies obscure the product.

Face sockets mate to the five rear male rails. Four horizontal seams use explicit
drop-in trapezoid-planform mortises, not undercut vertical captures. Two midline
splines close the left/right seams and enter before the face; the face subsequently
blocks their entry. Sampled installation sequence: collar, lower left/right,
upper left/right, two splines, normal approach then downward face seating.

## Independent installed-geometry evidence

- Eight printed leaves each closed, consistently wound, one shell; all fit the
  220 mm cube with provisional 5 mm XY margins on actual planar bed faces.
- Expected/actual printable build: 8 STL, 136 PNG. Supplementary full assembly:
  1 non-printable assembled reference STL, 10 PNG. Exact unified output: 9 STL,
  146 PNG, 2 manifests, 157 flat files; both audits pass.
- Config/SCAD/parts/assembly hashes and separate imported asset/helper/source
  dependencies pass. Generator backend pinned to manifold3d 3.3.2.
- Ear span: 228.600190924 mm. Full head assembly bounds approximately
  235.987 x 253.611 x 290.194 mm in assembly axes.
- Complete neck-cap footprint carried by neck_owner: planar symmetric area
  difference 0.014672911 mm2 against a 20191.686516 mm2 source cap.
- Body contact areas about 19696-28521 mm2; face about 21901 mm2 after pockets.
- Sampled motion maximum interference 0.000878023 mm3, below declared 1 mm3
  numerical threshold. Source assets match installed vertices within 0.002 mm.
  A 0.02 mm verification-only relief excludes intentional coplanar bearing
  contacts; this is not a gap added to printed geometry or a full sweep proof.

## Outstanding findings and disposition

Full continuous swept-envelope proof, whole-mesh recombination Boolean comparison,
minimum post-cut ligaments/sections, stop and root load capacity, physical fit,
slicer/profile/support review and anti-lift retention remain unverified. Current
posts and face can be deliberately lifted/disengaged; do not lift the product by
the face or claim handling retention without an explicit retainer/test. Production
coupons and headset/base stability/load measurements are still needed. Head-to-bust
connector is reserved on one owner but is not cut until a matching bust owner exists.

Primary visual assembly review: passed for candidate layout only. Interfaces:
blocked_unknown for final structural/physical acceptance. Approval state: pending.
Active plan retains these uncertain gates rather than claiming fabrication readiness.
