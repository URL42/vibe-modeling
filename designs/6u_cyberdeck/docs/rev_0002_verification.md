# rev_0002 correction and verification record

Config: designs/6u_cyberdeck/configs/rev_0002.json. Approved correction: relocate
forward side joints to Y=40 and fasten all four rear-center corners through a
separate interior plate. Preserve 254 x 293.9 x 80 exterior, four quadrant IDs,
3 mm structural minima, and PLA/0.4 nozzle/0.2 layers. Physical/slicer gates remain
open. rev_0001 acceptance is superseded for rail access and rear-center support.

## Failure and regression coverage

The rev_0001 bore test only inspected Y=0..5.8. It missed material behind the
rail holes and did not verify a rear-center clamp. The corrected test checks a
cylinder of diameter 8 at all 36 rack axes, behind the rails through Y=28, plus
all four bridge-to-quadrant load paths. Source bounds additionally prove the
complete service cylinders avoid walls/pads: X extremes +/-122.2625 stay inside
cavity walls +/-124; Z extremes +/-131 stay inside +/-143.95; forward side pads
begin Y=31, leaving 3 mm beyond the reserved service interval. The nearer
rail holes at Z=+/-6.35 must be included. No full-depth equipment sweep is claimed.

## Rear-center joint and supports

One separate bridge, 48 x 48 x 3 mm, lies at X/Z=-24..24, Y=70.2..73.2. Four
14 x 14 mm pads center at X/Z=(+/-12,+/-12), Y=73.2..80, fully within their own
quadrants. They penetrate the full rear skin Y=77..80, giving 3 mm overlap around
hardware voids. Each plate span is supported by two distinct clamped pad contacts
on both sides of each center seam; four total clamps provide independent load
paths into all four quadrants. No unfastened rear butt seam is counted as fused
material. Plate/pad contact at Y=73.2 is a fastened bearing interface, not a union.

Rear-entry hex pockets use AF=5.9 (circumdiameter=5.9/cos30), Y=77.2..80. The
pad bearing web is 4 mm; the plate is 3 mm. M3 passage diameter 3.6. Nut pocket
to conservative pad edge margin is 7 - 5.9/cos30/2 = 3.5936 mm. Pocket to center
split plane has at least 12 - 5.9/cos30/2 = 8.5936 mm. Adjacent pad edges are
10 mm apart. Plate bore-to-edge margin is 24 - 12 - 1.8 = 10.2 mm; bore-pair
ligament 24 - 3.6 = 20.4 mm. No cosmetic cuts or other voids approach this region.

Hardware: ISO 4762 M3x10 (5.5 head diameter x 3 height, 2.5 hex bit), ISO 7089
M3 washer (3.2 ID, 7 OD, 0.5 thick), ISO 4032 M3 nut (5.5 AF x 2.4). Washer
sits at Y=69.7..70.2, head at Y=66.7..69.7, shank Y=69.7..79.7. Nut bears at
Y=77.2 and occupies 77.2..79.6, giving full nominal thread engagement, 0.1 mm tip
protrusion past nut, 0.3 mm reserve to rear exterior. Shorter 8 mm screw fails
nut engagement; 12 mm projects outside and is rejected. No countersinks or head
recesses weaken the plate. Contact annulus fully supports each 7 mm washer.

Four interior driver approach cylinders, diameter 4 mm for 50 mm toward -Y
from the heads, fit the empty case; insert the bridge and tighten before equipment.
Four rear nut-insertion cylinders, diameter 8 mm for 15 mm toward +Y, are outside
the rear face. Plate installation is straight from the open front at its fixed
X/Z footprint; perimeter pads lie far outside that footprint. Equipment/service
integration and actual tool/profile variation remain unverified. Unscrew the four
center screws and withdraw the plate through the front before separating leaves.

## Perimeter stations and printability

Top/bottom stations keep Y=18/71; side stations now Y=40/71. Forward side pads
span Y=31..49, rear pads 62..80, leaving a 13 mm gap; their socket faces are
Y=34..46 and 65..77. All existing tongue/root/receiver and cut-margin dimensions
are unchanged. Sections and connectivity must be rechecked for the exact config.

Rear-face-down leaves preserve broad actual bed contact. New pads grow from the
rear skin; their edges, horizontal bores and nut-pocket roofs need slicer review.
The flat bridge is a separate 48 x 48 x 3 mm print. Front-ring overhangs and
perimeter socket supports remain open slicer gates. All physical coupon, PLA fit,
retention, torque, load and actual printer-profile fields from the initial record
remain UNKNOWN. The existing seam coupon proves only local station geometry;
rear-center clamps require their own measured assembly test before release.

## Evidence required before acceptance

- Five installed closed connected product shells, transformed bounds and bed faces.
- 36 rail bores/floors plus complete declared hardware-access envelope checks.
- All eight station types/locations and four rear-center clamps, shortest post-cut
  material widths, plate spans and tool/installation access.
- Case-only split/master volume and section comparison, excluding the separate
  bridge from case volume. Explicitly verify the bridge independently.
- Complete build, installed artifact review, then artifact-bound full assembly
  review and both audits. Expected 5 STL + 85 PNG product, 3 STL + 27 PNG review;
  unified 8 STL + 112 PNG + 2 manifests = 122 flat files.
- Structural joins and material width remain unverified for fabrication until
  required slicer/physical evidence passes. No immutable publication/commit/push.


## Captured failing baseline

Before replacement, measured the exact installed rev_0001 top-left/right leaf
STLs at both X=+/-118.2625, Z=6.35. Behind the open rail bore, solid material
occupied Y=9..17.284874 and 18.715126..27, confirming both blocked rail access
zones. Retained input STL hashes and intervals in rev_0002_regression_baseline.json.
The new regression requires the full declared Y=5.8..28 service envelope clear,
not merely an unobstructed front bore.


## Reference and physical boundaries

Rack reference remains ten-inch-rack-m3-printed-design-spec v2.0.0, bundle manifest
SHA-256 330051136930B54F0ABF91FF81EA217D0E6CAD2DBE6503375FFB219E59E0210D.
The design-owned rack helpers and constants remain inside the hashed source tree;
no code imports the immutable reference package. Current conformance rows are in
rev_0002_conformance_matrix.md; calibration/equipment-related blockers remain.

Total hardware is twelve M3x10 screw/washer/nut sets: eight perimeter and four
rear-center. Rack attachment hardware is additional and device-dependent.
Bridge center spans have paired pad supports at +/-12 on both axes. The outer
5 mm border beyond each pad footprint is a short handling overhang with a 3 mm
throat; it has no rated external load, and its cantilever behavior remains part
of the unverified physical load case. The 3 mm rear panels, perimeter members,
front-ring overhangs, pad roots and clamp regions also retain slicer/physical
verification gates. No load capacity or validated clamp torque is asserted.


## Final digital evidence

Complete build and full assembly-review audits passed. Actual counts match all
expected counts: 5 STL + 85 PNG product; 3 STL + 27 PNG review; combined 8 STL +
112 PNG + two manifests = 122 flat files at output/6u_cyberdeck/. Config/source
and all five authoritative STL hashes match. Five shells, 36 rail bores/floors,
1188 rail-access rays, four rear clamps, 64 rear driver rays, 16 plate insertion
rays, 114 material/joint/coupon sections and 84 case recombination
sections passed. Source/part geometry, plate isolation and both rear clamp sides
were reviewed from the installed artifacts. Case/master volume difference is
0.064816381 mm3.

See [artifact-bound review](rev_0002_assembly_review.md),
[measurements](rev_0002_geometry_measurements.json) and
[conformance matrix](rev_0002_conformance_matrix.md).
Structural joins and minimum material width remain unverified for fabrication;
physical PLA calibration, actual slicer/support paths and user exact-artifact
review remain open. No immutable publication, commit or push.
