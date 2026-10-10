# Raspberry Pi 5 case

Two printable leaves: a base with a floor and three solid walls, plus a separate
flat lid fastened at four M3 stations. The back remains open for cables.
The nominal shell is 120 x 120 x 120 mm; the raised camera/lens reaches 125 mm.
The current mutable candidate is `configs/rev_0004.json`. Earlier configs are
preserved; the rev_0002 lid is already printing and remains geometry-identical.

## Approved update, 2026-10-09

The user requested removal of the lid underside rim and bosses and reduction of
the base studs from 10 mm to 3 mm. The user selected a **7 mm flat lid** so the
4 mm deep screw-head recesses retain 3 mm beneath them. No extra embedding slab,
rim, or bosses extend beneath the flat lid underside.

| Feature | rev_0004 geometry (lid retained from rev_0002) |
| --- | --- |
| Base floor | 120 x 120 x 6 mm, thickened inward |
| Pi mounting head recesses | Four diameter-5 x 3 mm deep underside recesses; 3 mm retained floor |
| Walls | Front/left/right, 3 mm thick, z 0..113; no side-wall cutouts |
| Base mounting studs | Four 15 x 15 x 3 mm blocks at z 110..113 |
| Stud attachment | Full 3 mm side-wall overlap; front studs also overlap the front wall |
| Pilot bores | Diameter 3 mm, through the 3 mm stud thickness |
| Lid | One 120 x 120 x 7 mm slab, z 113..120 |
| Screw stations | (10,10), (110,10), (10,110), (110,110) |
| Clearance bores | Diameter 3.4 mm, through the lid |
| Head recesses | Diameter 7 mm, 4 mm deep, z 116..120; retained axial floor 3 mm |
| Camera | Raised solid silhouette derived from [camera.svg](../../docs/camera.svg), retained from rev_0001 |
| Camera body | 92 x 60 mm, corner radius 8 mm, centered at (60,60), 3 mm proud |
| Camera details | 40 x 8 mm viewfinder hump, 12 x 4 mm shutter step, 10 x 8 mm blind badge recess |
| Lens/button rim | Outer circle only, diameter 44 mm, 2 mm above the emblem |
| Arcade-button bore | Diameter 28 mm through slab/emblem/rim; no inner lens-circle detail |

## PCB and hardware assumptions

The dimensional background is [Raspberry Pi mounting guidance](../../docs/raspberry-pi-mounting.md).
The rotated 56 x 85 mm PCB occupies x 5..61, y 17.5..102.5. Its four diameter-2.7 floor
holes are at (8.5,21), (57.5,21), (8.5,79), and (57.5,79).
The mounting surface is now z=6 rather than z=3; the 3 mm underside recesses
keep the same remaining mounting-floor thickness while admitting the screw heads.
A head must fit the approved diameter-5 x 3 mm envelope with suitable print
clearance; actual hardware fit has not been measured.
The PCB origin is 5 mm from the case outer x face, so the actual gap to the
3 mm left wall inner face is **2 mm**, not 5 mm. This retained layout was not
changed by this orientation correction. The port edges face the open interior/rear;
USB/Ethernet faces the open rear with a 17.5 mm board-edge gap; USB-C/HDMI
faces the right interior with a 56 mm board-edge gap. Plug/cable envelopes
remain physically unverified. The floor has
through-holes, without modeled PCB standoffs or insert pockets. PCB underside,
mounting hardware, fan stack, cable bend radii and electrical clearance require
physical verification.

The button bore is inherited from the cyberdeck's diameter-28 mounting bore;
the diameter-35 button outer envelope is a clearance reference, not modeled.
Four M3 screws insert from above and engage the printed pilots. Engagement is
only 3 mm, as requested; screw type, useful bite in a diameter-3 printed pilot,
torque and pullout strength are unverified. Do not infer retention from geometry.

## Base recess correction, 2026-10-09

The user approved a 6 mm floor and diameter-5 x 3 mm underside head recesses
because the previous flat bottom would rest on protruding mounting screw heads.
Only the base floor/head-seat geometry changes. The lid source and its parameters,
all four lid screw stations, 3 mm top studs and z113 mating plane are frozen.
The base outer bounds and lid placement do not change. No reprint of the lid is
required by this digital geometry update. Previous configs remain unchanged;
zero recess depth in older configs preserves the earlier base geometry.

## Mounting orientation correction, 2026-10-09

The user confirmed USB/Ethernet toward the open rear. rev_0004 changes the
case-frame mounting pitch from 58 x 49 to 49 x 58 mm and moves the four
concentric head recesses with their bores. The PCB keeps its x5 left edge and
is centered front-to-back in its rotated 56 x 85 mm footprint. Drawing
coordinates (u,v) transform to case (5+v,17.5+u); the hole rectangle is
asymmetric relative to the PCB, so simply swapping pitch at the old origin
would give the wrong placement. The four obsolete stations are solid floor.
Floor/head-seat dimensions, all lid geometry and the coupling remain unchanged.

## Structural contract and hierarchy

`minimum_wall_thickness`, `minimum_structural_overlap`, and
`minimum_internal_edge_width` are 3 mm. Wall/floor and front/side-wall joints
have full-thickness positive-volume overlap (6 mm wall/floor embed in rev_0003). Each stud joins its side wall with
3 x 15 x 3 mm overlap, and retains a 3 mm thick throat and 3.5 mm to the pilot
bore at the inner block edge. Pilot cuts remain 5.5 mm from the wall inner face.
The new underside recesses leave 6 mm to the nearest exterior x face and 3 mm
to the side-wall inner face; hole-to-hole head-recess ligaments are 44 and 53 mm.
Their approved hardware seating shoulder is 1.15 mm radially, with a full 3 mm
axial floor above it. This is a seating-face detail exception, not a reduced
wall/floor throat. The lid head recesses retain 6.5 mm to an exterior edge and a 3 mm axial floor.
The unchanged hardware seating annulus is **1.8 mm radially** between the
3.4 mm bore and 7 mm recess; this retained seating detail is explicitly
excepted from the generic radial-strip rule, while its axial floor is 3 mm.
The 28 mm button bore has 8 mm of material to the diameter-44 lens edge.

The camera body's hump and shutter each embed directly into the lid slab by
3 mm; their incidental 2/1 mm overlaps with the body profile are decorative
registration, not their structural support. The lens embeds 3 mm into the
emblem. The badge recess stops at the slab top. Pairwise recess/button/badge
subtraction assertions protect remaining ligaments.

`product_assembly` contains the logical `case_joint`, which owns exactly two
printable leaves (`base`, `lid`). The lid/base interface is
`intentionally_terminated`: aligned coplanar seating faces at z=113, retained by
screws. It is not a Boolean structural join. Walls are supported by the floor
and front-wall corners; rear studs are local wall-supported overhangs. The lid
spans between the front and side seating surfaces/four screw stations; digital
geometry checks do not constitute a mechanical load test.

## Build and verification

The installed manifest selects the config for the normal VS Code task:

```powershell
python scripts/rebuild_stale_designs.py --all
```

For the first build that switches from a prior config to rev_0004, initialize the
installed config selection with the complete manifest builder:

```powershell
python scripts/scad_build_all.py --design raspberrypi5_case --config designs/raspberrypi5_case/configs/rev_0004.json
python scripts/scad_build_all.py --design raspberrypi5_case --config designs/raspberrypi5_case/configs/rev_0004.json --audit-only
python scripts/verify_raspberrypi5_case.py --config designs/raspberrypi5_case/configs/rev_0004.json
python scripts/scad_render_assembly_review.py --design raspberrypi5_case --config designs/raspberrypi5_case/configs/rev_0004.json --set full
python scripts/scad_render_assembly_review.py --design raspberrypi5_case --config designs/raspberrypi5_case/configs/rev_0004.json --set full --audit-only
```

Review installed printable artifacts before generating assembly evidence.
The complete printable set contains 2 STL + 34 PNG. The supplementary full set
contains 1 combined assembly STL + 19 PNG: six orthographic views, isometric,
exploded, both leaf isolations, stud seam start/mid/end, fastener section,
lid-head-floor section, wall/floor section, base underside isolation, and
sections through both Raspberry Pi mounting-hole rows. Final output is the flat union:
3 STL + 53 PNG and the two manifests in `output/raspberrypi5_case/`.
The combined STL is review-only, not a third printable part.

Exact digital findings, measurements and artifact provenance are recorded in
[rev_0004 verification](docs/rev_0004_verification.md). The prior
[rev_0003 record](docs/rev_0003_verification.md) and
[rev_0002 record](docs/rev_0002_verification.md) remain historical.
Compatibility is measured against [the printed lid reference](docs/rev_0002_lid_compatibility.json). Immutable revision
publication and committing/pushing this checkpoint require separate approval.

## Print and physical validation

Orient the lid with its flat underside on the bed, translated down by 113 mm;
its printable bounding box is 120 x 120 x 12 mm including the raised icon.
Orient the base floor-down; bounding box is 120 x 120 x 113 mm. Rear and front
studs overhang the interior by 12 mm and may need supports. The old lid band
and bosses have been removed, so the lid has no corresponding underside
support demand. Printer/material, brim margins, actual slicing and physical
fit/strength remain unverified. This digital checkpoint is not a claim that a
specific printer/profile or fastener combination is fabrication-ready.
