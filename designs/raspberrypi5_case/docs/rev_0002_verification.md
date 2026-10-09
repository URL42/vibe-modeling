# rev_0002 digital verification - 2026-10-09

## Findings and scope

The user-approved flat lid and shorter studs are complete. The nominal shell
remains 120 x 120 x 120 mm, with the icon reaching z=125. The lid has no underside
rim or bosses. All reviewed geometry belongs to `configs/rev_0002.json` and the
working tree at build time, based on commit `fc1ff8cd9f9da9913bb44c7e8a844ea16e073481`.
The complete build and assembly manifests record the actual Git/input hashes.

The first OpenCSG orthographic previews hid through-holes even though the STL
sections and isometric previews proved them. `main.scad` printable dispatches
now use `render(convexity=10)`. The complete manifest was rebuilt through the
normal stale-design entrypoint and all 34 installed PNGs were reviewed again.
Orthographic views show footprints and through-apertures; vertical emboss/recess
surfaces can have identical shading from directly above, so depth is verified
with isometric views, sections and final-mesh measurements. No individual output
was manually patched. The original rev_0001 config remains unchanged.

## Machine measurements from installed STLs

The reproducible check is:

```powershell
python scripts/verify_raspberrypi5_case.py --config designs/raspberrypi5_case/configs/rev_0002.json --summary
```

The checker first audits the complete installed artifact set and provenance.
It reads final ASCII/binary STL triangles, verifies closed shared-edge topology,
consistent winding, positive signed volume and exactly one connected shell per
printable part. Its 49 post-subtraction line sections measure final material
intervals independently of the SCAD parameter assertions. A 0.002 mm comparison
tolerance accounts for STL coordinate rounding; it is not structural engagement.
Negative checks confirmed rejection of a removed triangle/open shell and a
6 mm measurement where a 7 mm slab was expected.

| Check | Final exported measurement | Result |
| --- | --- | --- |
| Base bounds | (0,0,0)..(120,120,113) mm | passed |
| Lid bounds | (0,0,113)..(120,120,125) mm | passed |
| Flat slab | z 113..120 at five distributed samples; global minimum z=113 | passed |
| Four stud throats | z 110..113; 3 mm tall | passed |
| Stud-side-wall seam | Continuous final material at start/mid/end of all four attachments | passed |
| Walls and floor | 3 mm walls/floor, continuous front/side support and clear interior | passed |
| Pilot bores | Diameter 3 mm at x/y 10/110, full stud-depth holes | passed |
| Pilot inner-edge ligament | 3.5 mm to the block inner faces; 5.5 mm to side-wall inner face | passed |
| Lid clearance bores | Diameter 3.4 mm, centers aligned to all pilot stations | passed |
| Head recesses | Diameter 7 mm, depth 4 mm, retained floor z 113..116 = 3 mm | passed |
| Recess exterior ligament | 6.5 mm | passed |
| PCB mounting holes | Four through-floor openings at (8.5,35.5), (66.5,35.5), (8.5,84.5), (66.5,84.5) | passed |
| PCB-hole to left inner wall | 4.15 mm construction margin | passed |
| Button bore | Diameter 28 mm at (60,60), through the full 12 mm central stack | passed |
| Lens material to bore | 8 mm radial width | passed |
| Lens/emblem/slab | Continuous final interval z 113..125 adjacent to the bore | passed |
| Assembly interface | Base top = lid bottom = z113; aligned screw centers; no positive-volume base/lid collision | passed |
| Shell connectivity/winding | One closed, consistently oriented shell per printable leaf | passed |

## Join and subtraction inventories

- Wall/floor: every wall is embedded into the complete 3 mm floor. Front/side
  wall corners have 3 mm full-thickness overlap. Side walls attach along the
  floor; front corners provide the other support boundary.
- Front studs: full side-wall and front-wall overlap; rear studs: full side-wall
  overlap only (there is no rear wall). Each attachment has 3 mm engagement,
  15 mm along the side seam and a 3 mm vertical throat after the pilot cuts.
- Camera body/hump/shutter: each independently embeds 3 mm into the slab. Their
  incidental shallow profile overlaps do not supply structural support. Lens:
  3 mm embed into the emblem. Badge cutter stops at the slab top.
- Stepped screw void: bore/recess are concentric portions of the same hardware
  void. The **existing 1.8 mm radial seating annulus** is the documented hardware
  detail exception; the new axial floor beneath it is a full 3 mm. This is not a
  blanket exception for other material widths.
- Base cut neighborhoods: PCB-hole pairs have large pitch ligaments; stud pilots
  are separated vertically from floor holes. Pilot-to-wall attachment margins
  and block inner-edge margins are explicitly guarded.
- Lid cut neighborhoods: all six head-recess pairs, each head recess against
  the button/badge, and badge against button are asserted. Badge/body margins
  are at least 8 mm. The structural minimum remains 3 mm.

Structural joins: **passed for the defined digital geometry**. Minimum internal
edge/material width: **passed with the retained hardware-seat exception**.
Coplanar lid/base contact is deliberately not counted as a fused structural join.
Stud overhang strength, lid span under load and the screw interface require
physical material/load verification before fabrication-readiness approval.

## Assembly review

Hierarchy: `product_assembly -> case_joint -> base + lid`. Exactly two printable
leaves; the combined STL is review-only. Component count, isolation ownership,
identity transforms and top-down installation/removal are correct. No part was
merged or added. The interface remains `intentionally_terminated`, at z113.

The full installed set was reviewed: front/rear/left/right/top/bottom/isometric,
exploded, both printable isolations, stud attachment start/mid/end, fastener
section, lid recess section and wall/floor section. Views contain no proxies.
The exploded view exposes all four studs and both mating faces; the lid can be
lowered straight down after positioning and removed upward after unscrewing.
No unexplained openings, floating printable shells, truncation or interference
were found. Section cuts through bores can show separated 2D islands; these are
diagnostic intersections, not extra printable components. The full assembly
bounds are (0,0,0)..(120,120,125) mm. The floor under the arcade-button hole is
intentional; the hole pierces the lid, not the base.

Canonical hierarchy/coverage, transforms, digital interface alignment, visual
review and source/artifact provenance: **passed**. Agent digital review is
complete; user milestone acceptance and physical validation are pending.

## Artifact counts and provenance

Build scope: **complete manifest**, canonical mutable destination
`output/raspberrypi5_case/`. Expected/actual printable counts: **2 STL / 34 PNG**.
Expected/actual supplementary counts: **1 STL / 16 PNG**. Expected/actual flat
union: **3 STL / 50 PNG / 2 manifests = 55 files**. No probe source or staging
remains in the completed output. Both manifest audits pass; config/source/parts/
assembly/artifact hashes agree. The assembly review binds the exact complete
build-manifest hash and both authoritative printable STL hashes. Refer to the
installed manifests for build timestamps and hashes rather than duplicating
changeable manifest timestamps in this source note.

- Source SCAD tree SHA-256: `55403f9be4f2911f2cce380d58915b5619ccd3de515960a5ac4139a5e885bc23`
- Config SHA-256: `cffa570f71d27a44f223613f63ab89d022458a1aea67e5f34bacfdae0b769e96`
- parts.json SHA-256: `e4e0d3dd85f90a75a45dbef937dc1d0c699ac9904e5ccb3366cae7662931b610`
- assembly.json SHA-256: `2e0c9acfdfbd1a970fe5203bb426b79d2f9f89b4a06172f88c2f725b127a5ee2`

Final validation is rerun after documentation sync through the normal stale
pipeline, followed by installed-artifact review and fresh full assembly review.
This note is bound to the source/config/contract hashes above; the installed
manifests remain authoritative for all final STL/PNG hashes.

## Physical limitations

- Lid: underside down on the bed, translate z by -113; 120 x 120 x 12 mm bounds.
- Base: floor down, 120 x 120 x 113 mm bounds. The 12 mm stud projections into
  the interior may require supports. Specific printer/material/nozzle/layers,
  adhesion margins, slicing, support removal and layer-load response: unverified.
- M3 screw specification, grip, torque and pullout in 3 mm printed pilots:
  unverified. A diameter-3 pilot alone does not prove self-tapping retention.
- PCB underside/mounting hardware, port cables/bend radii, fan stack and button
  hardware fit: unverified. The retained PCB origin is 5 mm from the outer x
  face, hence 2 mm from the left inner wall; this update did not move it.
- No physical print/coupon has been tested, and no immutable revision published.

No claim of fabrication readiness or mechanical load qualification is made.
