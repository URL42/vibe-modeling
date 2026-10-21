# rev_0003 lower-4U control-cover verification

Mutable config: `configs/rev_0003.json`. No immutable revision published.
Digital installed-geometry, complete-build and assembly-review checks passed.
Physical fit/strength and slicer paths remain unverified.
See [artifact-bound review](rev_0003_assembly_review.md) and the retained
rev_0003_case_measurements.json / rev_0003_cover_measurements.json evidence.

## Interface provenance

User confirmed PLA, 0.4 mm nozzle, 0.2 mm layers and 220 x 220 x 220 mm build
volume, and chose the lower 4U. Use 5 mm per-side XY reserve (210 x 210 usable).

Joystick hole pattern is recovered from early cyberdeck commit `0d921ee`,
`designs/cyberdeck/src/lib/defaults.scad` and `_left_lid_aux_cut_pattern` in
`src/parts/cyberdeck.scad`. It was named auxiliary mounting/cable rather than
joystick: 30 mm center, four 3.4 mm holes, 80 mm across X by 40 mm along V.
The user reports the earlier printed pattern works. The present cover copies
these dimensions; it does not claim measured joystick body or travel envelopes.
Historical lid thickness is 5 mm, current cover thickness 3 mm: reselect joystick
screw lengths against the actual plate/washer/nut stack.

Arcade button defaults come from the same historical design: 28 mm hole, 35 mm
outer envelope, 40 mm spacing. Actual retention depth, terminals and maximum
panel thickness are not measured. Use those values as candidate interfaces.

## Geometry and ownership

Panel nominal 254 x 177.2 x 3 mm includes a 0.6 mm total 4U height allowance.
Installed X=-127..127, Y=-3..0, Z=-133.05..44.15, leaving upper 2U open.
Centered lower joystick origins: X=+/-63.5, Z=-88.75. Upper grid center
X=-63.5, Z=-0.15, 40 mm pitch. Diamond center X=63.5, Z=-0.45, cardinal offsets
25.5 mm. All four diamond flange circles remain in the upper quadrant.

IDs 1-5 keep existing case/bridge identities; ID6 `control_cover_left` owns both
14 mm crossing tongues, ID7 `control_cover_right` owns both receivers. Logical
cover subassembly has two leaves; quadrant divisions describe control positions.
Center seam X=0 is intentionally separate except for two fastened overlaps.

Print transform local (X,V,W) -> (X+127 for left or X for right,88.6-V,W).
Inverse installation is rotate -90 about X then translate (-127 or 0,-3,44.15).
Expected leaf bounds: left 141 x 177.2 x 3 mm; right 127 x 177.2 x 9.8 mm.
Broad visible faces lie at print Z=0. Socket roof spans up to 15 x 12 mm at
Z=3; test bridge/support behavior with the production-derived coupon. Coupon
owners are deliberately separated by 8 mm; it is an inspection export.

## Structural and fastener inventory

Minimum wall, root overlap and internal edge material are each 3 mm. Tongues
attach through full 3 mm face thickness and 3 mm X-root overlap at both seam
ends. Receiver shoulders are 3 mm wide; closed tips 3 mm. Receiver bosses
overlap their owner's face through 3 mm at both shoulders and closed end.
Tongue holes leave 3.2 mm side lands and 4.2 mm tip lands. A 4 mm bearing web
remains below each captive-nut pocket. Boss depth totals 9.8 mm.

Each clamp uses ISO4762 M3x10 (5.5 x 3 head), ISO7089 washer 7 OD x 0.5 and
ISO4032 nut 5.5 AF x 2.4. Socket: tongue width10, clear width12, insertion14,
closed cavity15, tongue/bearing contact W=3 with no axial air gap. Hole center
X=8; stations V=+/-75.6. Nut AF5.9, depth2.8, W=7..9.8. Screw starts at W=-0.5,
tip W=9.5, giving 0.1 mm beyond the nominal nut and 0.3 mm inside boss back.
Load path: left face -> integral tongue -> clamped bearing web/right boss ->
right face. Two stations resist relative rotation; strength requires PLA testing.

Four M3x10 rail screws/7x0.5 washers enter from front at X=+/-118.2625,
Z=-127 and 38.1. Cover3 + rail web3 + nut2.4 + washer0.5 = 8.9 mm. Screw tips
Y=6.5 clear the bounded rail service zone. Existing rail pockets AF5.6/depth2.8
are unchanged. Captive nuts are installed before closing the cover. Socket-head
driver approaches from negative Y; nuts insert from positive Y while cover is
on the bench. Joystick mounting screws are separate, lengths not yet selected.

Total enclosure/cover hardware is 18 M3x10 screws, 18 ISO7089 washers and 18
ISO4032 nuts: eight perimeter seams, four rear bridge clamps, two cover seam
clamps and four cover rail attachments. Only the four selected rail pockets
need nuts for this cover; unused rail positions remain available. Add the eight
joystick mounting screws and their actual retention hardware separately.

Panel supports: two clamped rail screws on each X side and two clamped seam
stations at X=8 near its ends. The face provides continuous material around all
control holes to those supports. Case body source geometry is unchanged: compare
five installed STL triangle counts, bounds and volumes against rev_0002 measured
evidence and rerun previous case section/regression checks on this installed
config. Captured rev_0002 byte hashes are retained, but OpenSCAD can reorder ASCII
triangle records across identical builds. Different byte hashes therefore do not
alone prove changed geometry; each build's own artifact hashes must still audit.

Cut inventory: 8 button holes, 2 joystick center holes, 8 joystick bolt holes,
4 rail holes and 2 seam holes; 2 socket entries and 2 nut pockets. Source asserts
all pairs of the 22 face holes, all outer/seam margins, all face-hole to boss
clearances, button envelope spacing/rail clearance, tongue and receiver lands.
Independent STL sections check centers and surrounding face on every hole,
roots/start/mid/end, shoulder overlaps, clamp webs and panel support sections.
Both hole diameters are measured at each bore axis. An independent analytical
full-width master compares the recombined cover leaves at W=1.5/3.5/6/8.5,
including intentional socket fit gaps and hex nut pockets, and rejects positive
overlap between owners. Sampling avoids exact solid boundaries and locations
within 0.03 mm of circular tangencies to exclude polygon-chord ambiguity; exact
axis diameters and critical land sections are checked separately. This sampling
exclusion does not reduce any 3 mm structural or material acceptance threshold.

## Resolved depth and keepout inventory

Cover item: `control_cover`, depth_class `front_only`, anchor `front`, support_mode
`front_ears`. Printed depth is 9.8 mm including bosses, occupied Y=-3..6.8.
Its explicit front-interface exception is distinct from the case's ordinary
equipment interval Y=5.8..77. It is not classified as full or half-depth.

| Named zone | Bounds / purpose | Evidence |
|---|---|---|
| cover_face_solid | X +/-127, Y=-3..0, Z=-133.05..44.15 | Two installed cover leaves; holes intentional |
| cover_joint_solid | X=0..18, Y=0..6.8, Z=-120.05/31.15 +/-9 | Integral receivers; within case opening |
| cover_front_driver | 4 mm diameter shaft at six clamp axes, 20 mm straight approach Y=-26.5..-6.5 | Declared tool shaft; real handle/hand envelope unknown |
| cover_nut_insertion | Rear-entry seam nut pockets, W=9.8..29.8, 6.813 mm diameter conservative envelope | Assemble on bench before controls/rail mounting |
| cover_control_body | Joystick/button rear bodies, terminals and wiring | BLOCKED_UNKNOWN: actual depths and travel absent |
| cover_removal | Bare cover translated toward negative Y by at least 7 mm before lift | Printed bosses clear rail plane; complete control/wire sweep unknown |

Zones are exclusive unless occupied by their named owner. No shared cable or
airflow keepout is claimed. Front/rear fit, terminal projection, connector travel
and cable bend remain distinct unknowns for actual controls. Conformance rows
are evaluated separately for `cover_rail_attachment` and retained `rack_front`
in [rev_0003 matrix](rev_0003_conformance_matrix.md).

## Installation and remaining gates

Assemble the case and rear bridge. On a bench, insert receiver nuts, slide the
right cover onto both left tongues, add both M3 clamps and tighten without
distorting PLA. Mount controls with their actual hardware and connect wiring.
Offer the assembled cover straight onto the lower-4U rail faces and install
four rail screws. Remove as a complete module before separating the halves.

Button external envelopes clear neighboring buttons by at least 1.062 mm, the
right rail opening by at least 4.625 mm and top edge by 1.6 mm. Rear bosses are
inside X=0..18, Y=0..6.8 and the rack opening; existing case seam stations are
outside this central region. Their installation is from the open front.
Joystick bodies, complete button retention/terminal shapes, wiring bend radii,
shaft travel, joystick plate screw/head/washer envelopes, hand clearance,
button usability, PLA stiffness and slicer layers remain unverified. Do not
describe this mutable candidate as print-ready or fabrication-ready.

## Artifact gate

Expected complete normal build: 7 STL / 119 PNG. Expected full supplementary
review: 4 STL / 34 PNG. Unified flat set: 11 STL / 153 PNG / 2 manifests, 166 files.
Complete build and audit must precede installed artifact review, followed by
assembly review and both final audits. Hash-bound independent measurement JSON
is stored in this docs directory, outside the authoritative flat output.
