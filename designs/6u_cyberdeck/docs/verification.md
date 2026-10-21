> Historical rev_0001 record. The current shared source and manifest target rev_0003;
> this record does not approve or reproduce the corrected geometry. See [rev_0003 verification](rev_0003_verification.md).

# rev_0001 engineering and verification record

Config: `designs/6u_cyberdeck/configs/rev_0001.json`. Baseline: `fc1ff8c`, initial
dimension locks and no case geometry. Governing plan remains current at
`plans/current/2026-10-04-11-35-16_create-6u-cyberdeck.md`.

## Hardware and clamp path

Proposed seam hardware, eight sets: ISO 4762 M3x0.5 x 10 socket-head screw
(5.5 mm head diameter, 3 mm head height, 2.5 mm hex key), ISO 7089 M3 washer
(3.2 ID, 7 OD, 0.5 thick), ISO 4032 M3 nut (5.5 AF, 2.4 thick). Check purchased
hardware against these envelopes before printing. Pocket AF=5.9, depth=2.8;
head/washer recess diameter=8.25, depth=3.8. No countersinks.

Local coordinates: u is insertion from the seam into the receiver, v is case
depth relative to station center, w is inward from the case exterior. Tongue
root u=-3..0; insertion u=0..14; socket u=0..15; closed end u=15..18. Tongue
width=10, socket width=12, pad width=18, leaving 3 mm side shoulders. Tongue
w=3.8..6.8; socket w=3.6..6.8. The extra 0.2 mm clearance is on the exterior
side only. The tongue's inner face bears directly on the receiver at w=6.8;
there is no axial air gap that must collapse before clamping.

The receiver bearing wall is w=6.8..10.8 (4 mm). Nut pocket is w=10.8..13.6.
Washer underside w=3.8, washer top w=3.3; screw head occupies w=0.3..3.3.
The 10 mm shank reaches w=13.3. Nut occupies w=10.8..13.2, giving full nominal
2.4 mm engagement and 0.1 mm tip protrusion beyond the nut, still 0.3 mm inside
the pad's inner mouth. Shorter 8 mm screws give only 0.5 mm nut engagement and
are rejected. A 12 mm screw projects 1.7 mm beyond the pad and is rejected.
Load path: screw -> washer -> tongue -> receiver bearing wall -> nut -> screw;
tongue registers and transfers shear, while the screw clamps separate leaves.

Driver sweep: straight 2.5 mm hex bit inside a diameter-4 mm cylinder, extending
50 mm radially outward from each screw. Head/washer insertion uses the diameter
8.25 recess. Nut insertion is radially outward from the chamber into the pad's
inner mouth, requiring an unobstructed diameter-8 x 15 mm local service cylinder.
Install nuts and screws before equipment. No hand-tightening torque or load rating
is claimed; nut antirotation and torque resistance need coupon measurements.

Rack mounting uses 36 M3 clearance passages at X=+/-118.2625 and the canonical
18-hole sequence Z=-127 + floor(i/3)*44.45 + [0,15.875,31.75][i%3]. The rack
origin is centered on this 6U opening. Flat external washer support has no shallow
recess, preserving the full 3 mm bearing web ahead of each 2.8 mm pocket. Rail
pockets use AF=5.6, circumdiameter=6.4663; this closer-fit candidate preserves
3.1168 mm to the central split. Physical nut fit is not established. Rack screw
length depends on the installed device ear; it must be selected from the 3 mm
bearing web, washer, ear thickness and 2.4 mm nut engagement, with tip keepouts.

## Station inventory and ownership

| Station | Ribbon | Axis Y | Tongue owner | Receiver owner |
|---|---|---:|---|---|
| 0 | top | 18 | top left | top right |
| 1 | top | 71 | top left | top right |
| 2 | bottom | 18 | bottom left | bottom right |
| 3 | bottom | 71 | bottom left | bottom right |
| 4 | left | 18 | bottom left | top left |
| 5 | left | 71 | bottom left | top left |
| 6 | right | 18 | bottom right | top right |
| 7 | right | 71 | bottom right | top right |

Two depth-separated clamps per seam give a 53 mm moment arm. This is a geometric
layout choice, not proof of an enclosure payload capacity. The front pad spans
Y=9..27; rear pad Y=62..80. Socket bounds Y=12..24 and 65..77 leave 6.2 mm from
the front rail's rear pocket face; the rear socket stops before the 3 mm rear wall.
The rear pad merges through the entire rear skin. Front and rear stations remain
disjoint, with a 35 mm pad gap along depth.

## Structural and subtraction inventory

Continuous shell: side/top/bottom walls 3 mm, rear skin 3 mm, front rail 5.8 mm.
All corners are formed by one hollowed outer box; the full 3 mm wall thickness
continues into intersecting front/rear skins and neighbouring perimeter walls.
Each perimeter panel spans front-to-rear with those two integral supports. Each
front/rear quadrant panel has adjacent perimeter-wall support at its exterior
edges; its cut edges require the fastened seams to complete the assembly. No
unfastened butt seam is claimed as a structural union.

Pad roots penetrate their owner's exterior skin through its full 3 mm thickness;
tongue roots overlap the pad u=-3..0 by 3 mm. Socket subtraction starts at u=0,
and the head cut starts no closer than u=3.875, so neither removes the root.
Receiver side shoulders are 3 mm wide and its closed end 3 mm long. The receiver
bearing wall after the nut/socket cuts is 4 mm. These are local geometric minima,
not physical material-strength verification.

| Cut pair / edge | Nominal minimum mm | Meaning |
|---|---:|---|
| Tongue bore to width edge | 3.2 | 5 - 1.8 |
| Tongue bore to insertion tip | 4.2 | 14 - 8 - 1.8 |
| Head recess to seam mouth | 3.875 | 8 - 4.125 |
| Head recess to pad depth edge | 4.875 | 9 - 4.125 |
| Socket to pad depth edge | 3 | 9 - 6 |
| Socket tip to closed end | 3 | 18 - 15 |
| Socket inner face to nut floor | 4 | 10.8 - 6.8 |
| Nut pocket to pad depth edge | 5.5936 | 9 - 5.9/cos(30)/2 |
| Front rack pocket to front station socket | 6.2 | 12 - 5.8, projected Y |
| Adjacent rack nut cuts | 6.2337 | 12.7 - 5.6/cos(30) |
| Rack nut pocket to central quadrant seam | 3.1168 | 6.35 - 5.6/cos(30)/2 |
| Rack nut pocket to opening edge | 3.9043 | 7.1375 - 5.6/cos(30)/2 |
| Rack nut pocket to outer edge | 5.5043 | 8.7375 - 5.6/cos(30)/2 |

Head recess/socket and bore/nut pocket intersections are intentional connected
hardware cavities. Their bearing faces and surrounding shoulders are inventoried
above rather than falsely counted as material between disjoint cuts. Other
approaching pairs are the adjacent rack rows, front rack pockets vs station slots,
and front/rear station sets; all have named checks. Top/bottom stations are far
from rack columns. Opposite side/ribbon sets do not intersect each other.

## Depth, service and keepouts

Case class: full shell, anchored at Y=0; equipment support is device-specific.
Front structural reserved depth=5.8; rear=3; geometric available interval=5.8..77.
No electronics, mass/center of gravity, connectors, cable bends or fan clearances
were specified. Equipment integration and payload capacity remain BLOCKED_UNKNOWN.
The open front alone does not establish a usable insertion/service envelope.

Named keepouts: rack_front_hardware (36 individual hole/pocket axes and device
dependent screw/washer/driver volumes); station_pad_0..7 (local pad envelopes);
station_driver_0..7 (outward bit sweeps); station_nut_access_0..7 (inward access
cylinders); rear_skin Y=77..80; front_ring Y=0..5.8 outside the clear opening.
There are no opaque hardware/equipment proxies in printable or review geometry.

## Physical coupon gate

`seam_station_coupon.stl` is derived from the exact production station modules,
with two intentionally separated printable pieces. It tests socket entry, tongue
fit, nut retention, head/washer seating, driver reach and clamping. Print using
the same rear-facing local bed orientation and process as the production leaves.
Candidate: PLA, 0.4 mm nozzle, 0.2 mm layers, four walls; actual printer/profile
and measured manufacturing deviations remain UNKNOWN.

Acceptance: insertion by hand without cracking or forced deflection; both datum
faces seat; 7 mm washer supported all around; nut inserts and does not rotate
during tightening; chosen screw fully engages nut without protruding into the
keepout; driver reaches head; no cracked or yielded root/receiver. Record actual
clearance, insertion force, torque, deformation, failure location and test setup.
Do not freeze production tolerances without those measurements. Rail nut-pocket
fit and finished hole size also need calibration/post-machining evidence.

| Physical validation field | Recorded value |
|---|---|
| Material / nozzle / layer height | User-selected PLA / 0.4 mm / 0.2 mm |
| Actual printer and saved slicer profile | UNKNOWN |
| Wall count / infill / supports / temperatures | UNKNOWN; four walls proposed |
| Measured tongue width / thickness / insertion length | UNKNOWN |
| Measured socket width / depth / tip clearance | UNKNOWN |
| Insertion force and seated datum alignment | UNKNOWN |
| Nut fit / retention / rotation resistance | UNKNOWN |
| Head and washer seating / driver reach | UNKNOWN |
| Applied tightening torque / clamping response | UNKNOWN |
| Root or receiver deformation / failure location | UNKNOWN |
| Finished rack bore / rail nut-pocket fit | UNKNOWN |
| Slicer paths through roots, shoulders and front-ring supports | UNKNOWN |

Worst-case fit requires measured errors from both members. For example, the
nominal 1 mm per-side socket clearance becomes `1 - (tongue_width_error +
socket_width_error)/2` under adverse width deviations; the nominal outer-face
0.2 mm gap becomes `0.2 - tongue_thickness_error - socket_depth_error` under
adverse radial deviations. Those error bounds are unknown, so neither a minimum
physical gap nor maximum interference is claimed. Verify the actual bearing
faces and minimum printed material widths before selecting production tolerances.

## Evidence and remaining gates

Reference validation and assembly-contract validation passed on 2026-10-18.
Mesh, section, build, provenance and image-review results are recorded separately
after the installed complete build. Readiness remains unverified until those
records and physical/slicer gates pass. No immutable publication is permitted
while a required physical or assembly gate is BLOCKED_UNKNOWN.

## Review implementation and printability scope

Assembly review imports the exact installed leaf STLs and applies the inverse
print transform. Source/config/parts hashes and authoritative STL hashes are
bound by the normal review manifest. The unsplit-master export remains an
independent source-derived comparison. No hardware/equipment proxy is imported.
A complete build and audit must precede review; opening review dispatch without
installed matching artifacts is unsupported.

Rear-face-down printing leaves 10.6 mm top/bottom and 12.875 mm side front-ring
cantilevers above the perimeter skin. A slicer must explicitly support or validate
these spans and verify support removal through the opening. Local socket bridges,
sideways bores, nut pockets and tongue roots also need layer-path review. No
support-free or production-strength claim is made for the selected PLA profile.

The shared review-stage correction retains its CLI/schema, exact-file audits,
rollback and cleanup. Fifteen regression tests passed: six unified-output tests
(including paths with spaces and injected render-failure cleanup), eight assembly
contract tests, and one build-view preset test. Staging now stays under the
canonical output and is removed before ordinary final audits.


Review imports live in `src/main.scad` so their relative location is explicit.
The [OpenSCAD import documentation](https://files.openscad.org/documentation/manual/The_OpenSCAD_Language.html#import)
explains that include/import path context affects relative file resolution.
The final normal build is repeated after review-source edits; a prior build is
never treated as matching a newly edited source hash.


## Final digital checkpoint, 2026-10-18

Complete-manifest and full assembly-review audits passed at output/6u_cyberdeck/:
4 product STL + 68 product PNG, plus 3 supplementary STL + 22 review PNG;
combined 7 STL + 90 PNG + 2 manifests = 99 flat files. Config and source provenance
and every authoritative STL hash match. Independent measurement passed 36 rack
bores, 83 station/coupon sections and 84 split/master comparison sections; the
volume difference is 0.065525421 mm3. Coupon contains exactly two closed pieces.
See assembly_review.md for hashes, findings, numeric-comparison tolerance and
approval state, and geometry_measurements.json for raw measured intervals.

Structural joins: unverified for fabrication. Minimum internal edge/material
width: unverified for fabrication. Local digital topology/section/margin checks
passed; slicer/physical gates remain open. No immutable revision, commit or push.
