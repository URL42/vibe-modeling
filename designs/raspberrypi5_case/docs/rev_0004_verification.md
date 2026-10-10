# rev_0004 mounting orientation verification

Approved on 2026-10-09 after the user reported a 90-degree pattern error and
confirmed USB/Ethernet must face the open rear. Baseline commit `f64f579` and
config rev_0003; the printed lid remains rev_0002. Candidate: `configs/rev_0004.json`.

## Layout and unchanged geometry

The PCB is 56 mm across the case and 85 mm front-to-back, at x5..61,
y17.5..102.5. GPIO faces left; USB-C/HDMI face the right interior. The
[official drawing](https://datasheets.raspberrypi.com/rpi5/raspberry-pi-5-mechanical-drawing.pdf)
coordinates (u,v) transform to case (5+v,17.5+u). Approved hole centers:
(8.5,21), (57.5,21), (8.5,79), (57.5,79); pitch 49 x 58 mm. The hole
rectangle is asymmetric relative to the board outline. Rotate the placement
and its head seats together, rather than swapping pitch at the previous origin.

Retained: 6 mm inward-thickened floor, diameter-2.7 through-bores, four
diameter-5 x 3 mm underside head seats and 3 mm supporting roofs. Prior configs
and printed-lid reference are unchanged. Lid source bytes, canonical exported
mesh, all lid inputs, four coupling stations, z113 plane and z110..113 studs
must match the printed reference. Only the five approved PCB layout inputs
are exempted from the earlier broad input freeze, and those are independently
asserted to their exact approved values.

## Structural inventory and scope

Named minimum wall, overlap and internal material width: 3 mm. Floor/wall embed
6 mm, stud/wall overlap 3 mm, nearest new recess exterior margin 6 mm,
side-wall inner-face margin 3 mm, pairwise recess ligaments 44/53 mm.
All six pairs and every outer margin are asserted. Concentric bore/head cuts
form one stepped void. The retained approved base seat face is 1.15 mm radially,
with 3 mm axial support; the printed lid seat remains its documented 1.8 mm
radial exception. These seating details do not reduce a wall/floor throat.
No new join or printable leaf is introduced.

The PCB rear board-edge gap is 17.5 mm; right board-edge gap is 56 mm and
left inner-wall gap 2 mm. Plug envelopes, cable bends, baseplate placement,
head fit, slicing, supports, strength and physical fit remain unverified.
The user observation identifies model orientation, not a measured printer
calibration defect. No printer/material/profile or physical measurement is
known. This is digital geometry verification, not fabrication-ready approval.

## Artifact and verification record

Installed geometry verification passed all 73 line sections in the complete
rev_0004 build. Each leaf is one closed, consistently wound, positive-volume
connected shell. Base bounds: (0,0,0)..(120,120,113); lid bounds:
(0,0,113)..(120,120,125). Exact approved centers and 49 x 58 pitch passed;
all four obsolete stations measure solid z0..6 floor. All four recesses
measure diameter 5, depth 3 and retained roof 3 mm. The exported lid canonical
triangle hash equals the printed rev_0002 reference; source bytes and every
remaining frozen input match. A negative check rejects the old 58 mm
across-case pitch. Earlier configs and captured reference match HEAD.
Structural joins: passed. Minimum internal material width: passed with the
explicitly approved hardware seating-face exceptions documented above.

The revision-specific regression inventory is:
73 final-STL line sections (including four restored obsolete stations), closed
oriented connected printable shells, exact bounds, approved centers/pitch,
recess diameter/depth/roofs and independent printed-lid canonical comparison.
Final obsolete locations (8.5,35.5), (66.5,35.5), (8.5,84.5), (66.5,84.5)
must be solid 6 mm floor. Review installed printable images before generating
the full artifact-bound assembly set.

Complete printable set: 2 STL + 34 PNG. Full supplementary set: 1 review-only
STL + 19 PNG. Final exact flat output: 3 STL + 53 PNG + two manifests (58 files)
in `output/raspberrypi5_case/`. Commands are in the design README. Exact input,
printable-build binding and artifact hashes belong to the installed manifests;
final measured geometry, assembly findings and audit outcomes are recorded in
the [2026-10-09 journal](../../../journal/2026-10-09.md) and governing plan.
The printed-lid canonical comparison target is
`36281ee5052ce08af6e37fa510e84be303be2fedb1597a69591725c9751b3a6c`. Mutable config/output is not immutable numbered publication.
