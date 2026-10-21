# 6U cyberdeck rack case

Current mutable candidate: **rev_0003**. Standalone 254 x 293.9 x 80 mm case,
222.25 x 266.7 mm front opening, four quadrant leaves and a removable internal
rear-center fastening bridge. It is not a cyberdeck-2 variant. A removable lower-4U control cover adds two printable halves, two joystick
patterns and eight arcade-button holes. Control hardware is not included. Physical PLA fit/strength and slicer review remain
unverified; do not treat this candidate as fabrication-ready.

## Current lower-4U control cover

The 254 x 177.2 x 3 mm cover sits on the front rails at Y=-3..0, spanning
Z=-133.05..44.15, with the upper 2U open. Four logical regions share two
printable leaves: upper left 2x2 buttons on 40 mm pitch, upper right diamond
buttons at cardinal offsets 25.5 mm (36.062 mm adjacent pitch), and one
centered joystick in each lower region. Button holes are 28 mm with a checked
35 mm body/flange envelope. Diamond envelope gap is 1.062 mm and its top
flange clears the panel edge by 1.6 mm.

Joystick cuts reuse the early cyberdeck `_left_lid_aux_cut_pattern`: 30 mm
center opening plus four 3.4 mm through-holes on an 80 x 40 mm rectangle.
The user reports the earlier print works; its generic auxiliary/cable naming
initially hid it from keyword searches. Full joystick bodies, travel, terminals
and mounting screw lengths remain unmeasured. The historical lid is 5 mm thick;
this 3 mm cover may require different joystick screw lengths.

M3 seam stations lie at cover X=8, local V=+/-75.6, with 14 mm left-owned
tongues and right-owned sockets/bosses. Clamping screws enter from the visible
face; captive nuts enter from the rear before installation onto the rails. Four
M3 rail screws use X=+/-118.2625, Z=-127/38.1 and the existing rail nuts.
The cover is supported at two rail screws per side and two center-seam clamps;
verify PLA load/deflection physically before operation. No third cover connector
is printed. Build the case first, assemble the two cover halves on the bench,
attach controls and wiring, then fasten the cover onto the rails.

Both cover halves export face-down: left 141 x 177.2 x 3 mm, right
127 x 177.2 x 9.8 mm including its integral rear bosses. Confirmed printer
volume is 220 x 220 x 220 mm; a 5 mm per-side XY reserve leaves 210 x 210 mm.
The right socket roof needs a bridge/support test. The production-derived
cover_seam_coupon export contains two intentionally separate small pieces.
Physical fit, complete component envelopes and slicer paths remain unverified.

## Case corrections retained from rev_0002

- Move the two forward side connector axes from Y=18 to Y=40, at side depth
  midline. Pads now start at Y=31. Keep the four top/bottom stations and rear
  side stations in their original positions.
- Reserve an 8 mm diameter hardware/nut/tool access envelope behind every rail
  bore from Y=5.8 to Y=28, with 3 mm before the nearest side pad. This is a bounded
  rail-access zone, not an unobstructed 80 mm equipment insertion claim.
- Add one 48 x 48 x 3 mm interior bridge at the rear center, with four M3 clamps,
  one integral pad per quadrant. This directly fastens the four meeting corners.
  All printed geometry and nominal hardware tips remain within Y=0..80.

## Product and printable parts

Product -> enclosure (four leaves) + rear fastening bridge + removable control cover
(two leaves). parts.json is
canonical: IDs 1 bottom left, 2 bottom right, 3 top right, 4 top left, 5 rear center
bridge, 6 control_cover_left, 7 control_cover_right. Preserve these identities. Do not merge the plate into a quadrant or
remove one clamp without a revised plan. The four rear corner pads are integral
to their quadrant owners; only the bridge crosses both rear seams.

Master shell geometry is modeled once, with strict quadrant ownership plus
explicitly owned crossing tongues and corresponding receiver sockets. Assemble
left and right columns along Z, then slide the right column onto the left-column
X tongues. Clamp the perimeter stations; place the rear bridge from the open
front, insert four nuts through the exterior rear pockets and tighten the bridge
screws from inside. Install equipment afterwards. Disassemble in reverse order.

All four leaves export rear-face-down, with broad planar rear bed contact, on a
220 mm bed with 5 mm per-side reserve. Conservative largest footprint is
141 x 160.95 mm, height 80 mm. The bridge exports flat at 48 x 48 x 3 mm. Its
inverse print transform and every owner are declared in assembly.json.

Minimum wall, structural overlap and shortest internal material width are each
3 mm. Front rails are 5.8 mm, rear/perimeter skin 3 mm; top/bottom ring bands
13.6 mm, side bands 15.875 mm. Exterior depth is 80 mm; ordinary shell interval
is Y=5.8..77 before local joints and hardware. The rear bridge/pads occupy the
central Y=70.2..80 region; screw heads reach forward to Y=66.7. Equipment, cable,
service and load capacity must be verified separately.

## Hardware and process

Seam and rear-center screws: ISO 4762 M3x10, 5.5 x 3 mm socket head and 2.5 mm
hex bit, ISO 7089 M3 washer (7 OD x 0.5), ISO 4032 M3 nut (5.5 AF x 2.4). Verify
purchased dimensions. Rear-center clamp: 3 mm plate + 0.5 washer + 4 mm pad web
+ 2.4 nut = 9.9 mm; 10 mm screw tip lies at Y=79.7, 0.3 mm inside the exterior.
Cover seam/rail screws also use M3x10 with washers; rail screw tips reach Y=6.5,
inside the existing service zone. Joystick screw lengths depend on its unmeasured
mounting plate stack. No countersinks.

User-selected PLA, 0.4 mm nozzle and 0.2 mm layers. Four walls remain a proposed
test setting; printer volume is confirmed at 220 mm per axis; profile and calibration measurements are unknown.
The front ring overhangs the perimeter skin by 10.6 mm at top/bottom and 12.875 mm
on the sides. Validate supports/bridging, socket and sideways-hole layer paths,
and rear-pad undersides; remove supports through the opening without trapping
material in sockets. Do not infer strength from watertight meshes.

See [rev_0003 verification](docs/rev_0003_verification.md) for hardware, cut-pair,
support, service and physical test records. Earlier unnumbered records describe
historical rev_0001; its config is retained, but shared source has since changed.
No immutable revision has been published.

## Build and review

The installed manifest selects configs/rev_0003.json. The standard automatic
pipeline is `python scripts/rebuild_stale_designs.py --all`; use the exact config
for audits and supplementary review:

```powershell
python scripts/scad_build_all.py --design 6u_cyberdeck --config designs/6u_cyberdeck/configs/rev_0003.json --audit-only
python scripts/validate_cad_assembly_contract.py --design 6u_cyberdeck
python scripts/scad_render_assembly_review.py --design 6u_cyberdeck --config designs/6u_cyberdeck/configs/rev_0003.json --set full
python designs/6u_cyberdeck/docs/verify_geometry.py
python designs/6u_cyberdeck/docs/verify_control_cover.py
```

Complete product build: 7 STL + 119 PNG. Full supplementary review: 4 STL + 34 PNG.
Unified expected set: 11 STL + 153 PNG + 2 manifests = 166 flat files under
output/6u_cyberdeck/. Assembly, unsplit case and both two-piece seam coupon
exports are inspection/test artifacts, not additional product leaves.

Current artifact review: [rev_0003 review](docs/rev_0003_assembly_review.md),
[verification](docs/rev_0003_verification.md) and
[interface conformance](docs/rev_0003_conformance_matrix.md).
The rev_0002 records remain historical; current shared source includes the cover.
