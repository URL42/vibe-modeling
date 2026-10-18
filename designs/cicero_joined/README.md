# Cicero: complete integral-joint candidate

Current complete product: **6 head pieces and 11 bust pieces**, with **33 integral
male/female dovetails and no separate keys**. This supersedes the rejected
`cicero_head` candidate and earlier unjoined face-fit exports.

The life-size Steam Frame headset holder retains a target **228.6 mm (nine-inch)
ear-tip span**. Assembled scan bounds are approximately 437.54 x 342.23 x
569.00 mm. Printer envelope: **220 x 220 x 220 mm**. This is a mutable engineering
candidate, not fabrication-approved; headset fit, tipping and load capacity remain
unverified.

## Printable parts

Use the individual `*_rev_0001.stl` files in [the complete output](../../output/cicero_joined/).
They already include print transforms. Keep their broad cut faces at Z=0;
do not tilt them onto tiny contacts. The face points upward. Local sculpted
overhangs and joint bridges still require slicer review.

| Part | Print dimensions XYZ (mm) | Actual bed contact (mm2) |
| --- | --- | --- |
| h_face | 200.95 x 200.95 x 43.15 | 19877 |
| h_neck | 205.63 x 205.63 x 69.20 | 18293 |
| h_left_lower | 201.10 x 201.10 x 98.89 | 19969 |
| h_right_lower | 201.30 x 201.30 x 104.89 | 15438 |
| h_left_upper | 201.23 x 201.23 x 116.53 | 19859 |
| h_right_upper | 199.51 x 199.51 x 108.63 | 20233 |
| b_neck | 162.65 x 162.65 x 28.00 | 17723 |
| b_lower_lf | 185.94 x 199.03 x 171.12 | 25138 |
| b_lower_lb | 142.20 x 169.94 x 173.53 | 20514 |
| b_lower_rf | 187.20 x 150.00 x 168.97 | 27261 |
| b_lower_rb | 190.06 x 172.96 x 168.13 | 19401 |
| b_upper_lf | 134.91 x 134.91 x 92.01 | 7259 |
| b_upper_lb | 150.69 x 150.69 x 123.22 | 4302 |
| b_upper_mf | 152.70 x 152.70 x 219.60 | 10874 |
| b_upper_mb | 171.12 x 163.50 x 219.60 | 14944 |
| b_upper_rf | 144.70 x 144.70 x 137.53 | 7934 |
| b_upper_rb | 139.88 x 126.70 x 140.57 | 10081 |

See [geometry_manifest.json](geometry_manifest.json) for exact transforms, bounds, bed contacts, source hashes and every joint.

## Cuts and joint ownership

The neck plane is Z = 0.3Y + 304.341422 mm (16.70 degrees from horizontal).
Head and bust each retain a continuous printed neck owner: `h_neck` and
`b_neck`. **One** 32 mm-long, 32 mm-wide flared dovetail joins those owners,
with 8 mm engagement, 6 mm root overlap and 34 mm downhill travel.
The head owns the downward-facing recess; the bust owns the upward male.

The face cut retains the entire facial region. Rear head height cuts use
Z = 0.15Y + 360 and Z = 0.15Y + 460 mm, permitting downhill in-plane seating.
The neck-bearing collar is one piece; rear lower and upper sections are each
split left/right. The bust has four lower, six upper and one neck piece.
Its main height plane is Z = 0.15Y + 150 mm. The central upper column is
219.6 mm wide and prints with that dimension vertical; both column-edge
connections are recessed to preserve the 220 mm height limit.

Every actual mating pair has a joint: 11 internal head, 21 internal bust,
and one head-to-bust connection. `actual_seam_contacts` is discovered from
shared cap polygons independently of the declared joint inventory.
Male/female ownership also preserves a broad flat print face; female-down
is a preference subordinate to material, entry access and bed contact.

All channels have a closed end at their lowest installed travel. Loading uses
normal approach through a widened pocket followed by downhill sliding into
capture. Clearances are provisional 0.35 mm profile-coordinate offsets,
not calibrated normal flank clearances. The two bust-neck rails use 8 mm length
and 10 mm travel to avoid the rising shoulder; their throat/flare/engagement
remain 10/16/6 mm. This does not establish a load rating.

## Assembly sequence under verification

1. Join right to left lower rear head; repeat for upper rear head.
2. Seat the lower rear pair onto `h_neck`, then the upper rear pair onto it.
3. Load and slide the face onto the completed rear head.
4. Assemble lower bust in order lf, rf, lb, rb. Assemble upper bust in order
   lf, mf, rf, lb, mb, rb. Corner pieces use diagonal normal loading.
5. Seat the entire upper bust onto the lower bust; install `b_neck`.
6. Load the complete head onto the single bust-neck male, then slide downhill
   to the closed stop. Anti-lift retention remains an unresolved design decision.

Orders describe assembly coordinates, not print poses. Sampled whole-piece
collision checks must pass before accepting these steps; samples do not prove
continuous swept clearance or physical fit.

See the hash-bound [installed assembly review](assembly_review.md) and
[independent verification](verification.json) for current results. All sixteen
sampled installation stages pass; continuous sweeps remain unverified.

## Reproduce and audit

Geometry generation uses NumPy, SciPy and manifold3d **3.3.2** from
`.tmp/cicero-head-tools-v332` (the historical helper imports that pinned location).
The worker constrains its own native Boolean process to one available CPU.
Source helpers and original intermediate meshes are explicit hashed dependencies.

```powershell
python designs/cicero_joined/build_geometry.py
python designs/cicero_joined/verify.py --assets-only
python scripts/validate_cad_assembly_contract.py --design cicero_joined
python scripts/scad_build_all.py --design cicero_joined --config designs/cicero_joined/configs/rev_0001.json
python designs/cicero_joined/verify.py
python scripts/scad_render_assembly_review.py --design cicero_joined --config designs/cicero_joined/configs/rev_0001.json --set full
```

The normal pipeline installs 17 printable STL / 289 PNG; full assembly review adds
3 nonprintable reference STL / 15 PNG. Total: **20 STL, 304 PNG and two manifests**.
Reference assembly meshes are inspection artifacts, never additional print parts.
`verification.json` binds independent mesh/joint/assembly samples to installed
build and geometry hashes; the standard SCAD digest alone does not cover imports.

The overlapping source bust shells are unioned before partition. Inherited
coincident vertex fans on three leaves are separated by at most 0.008 mm for
position-only STL topology; originals remain unchanged. Per-part repair counts
and displacement are recorded. All leaves must remain closed, consistently
wound single shells after the OpenSCAD export round trip.

Targets: minimum wall/internal material width 3 mm; male root overlap 6 mm.
Generation checks conservative 3.1 mm local stock guards and pairwise later void
interference. Global shortest material paths, continuous swept motion,
structural capacity, anti-lift retention, material/profile calibration, slicer
supports and physical coupons remain **unverified**. Gravity seating alone
neither guarantees friction-free settling nor prevents upward removal.

## Source and license

Adapted from [Cicero on MyMiniFactory](https://www.myminifactory.com/object/3d-print-cicero-55952).
**CC BY-NC-SA**, as specified by the repository owner. Preserve original creator
credit, this source link, the applicable license and change notices; share
adaptations noncommercially under the same applicable license. Creator name and
exact license version remain unverified because the source listing returned 403.
No version or creator is invented. Changes: uniform scaling, source-shell union,
flat-bed partitioning, integral dovetails and small STL vertex-fan separation.
See [original import documentation](../cicero/README.md) for source provenance.
