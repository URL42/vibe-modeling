# Cicero

Current complete candidate: [cicero_joined](../cicero_joined/README.md): six head and eleven bust pieces, all integral joints, and one head-to-bust connection. Earlier head-only and five-piece outputs are retired.

Documentation for the imported [Cicero model on MyMiniFactory](https://www.myminifactory.com/object/3d-print-cicero-55952).
The existing STL and 3MF files are in [output/cicero](../../output/cicero/README.md).
This design now includes an unsplit, uniformly scaled OpenSCAD measurement master
and a mutable `rev_0001` config. It establishes assembled size for the tilted-neck intermediate exports and the reference face-up study. Integral dovetails are implemented in the separate complete candidate.

## Initial scaled master — rev_0001

The chosen baseline is the original **508,792-triangle** `output/cicero/2.stl`,
preserved byte-for-byte as [assets/cicero_original.stl](assets/cicero_original.stl).
The supplied `simplified.stl` has 33,852 triangles and a different existing scale;
it is retained but is not the measurement baseline. No repair or decimation has
been applied to the chosen scan. Both the asset and its scaled derivative retain
the licensing notice below.

The initial interpretation of “ear tips” is the outer lateral ear rims, rather
than the highest points of the ears. Landmarks A and B are actual source-mesh
vertices, visually checked against both ear surfaces. They remain an initial
selection for user review before cuts or physical fit decisions.

| Measurement | Value |
| --- | --- |
| Source landmark A, negative-X ear | `[-14.551604271, -4.422200203, 45.658359528]` |
| Source landmark B, positive-X ear | `[9.461223602, 6.898849487, 45.459285736]` |
| Source straight-line A–B distance | 26.548478279 source units |
| Uniform scale | 8.610663014 mm per source unit |
| Target assembled ear span | 228.600000 mm / 9 inches |
| Measured exported ear span | 228.600191 mm |
| Complete assembled X width | **437.540745 mm** |
| Complete assembled Y depth | **342.233601 mm** |
| Complete assembled Z height | **568.999287 mm** |

STL has no intrinsic units. The landmark distance sets the conversion into
millimeters independently of any assumed source scale. The model retains the
scan's original orientation, with Z up and the face generally toward negative Y;
the head remains turned and tilted. The transform is
`p_mm = 8.610663014175309 * (p_source + [0.312078476, -0.123837471, 4.307562828])`.
It centers the full bounding box in XY and places its minimum Z at zero. Full
precision landmarks and translation are authoritative in the config. No rotation
or cuts have been applied.

Review the [ear landmark close-ups](../../output/cicero/source_ear_landmarks.png),
[dimensioned views](../../output/cicero/scaled_master_dimensions.png), and
[scaled STL](../../output/cicero/scaled_master.stl).
The [measurement record](../../output/cicero/scaled_master_measurements.json)
contains exact coordinates, bounds, transform, hashes, and export verification.
Axis-projected distances appear shorter than the true 3D ear-tip distance because
the head is turned. Full-bust width includes the shoulders and pedestal.

### Reproduce and audit

Run from the repository root with OpenSCAD, Python, NumPy, SciPy, and Matplotlib
available (all were available during this checkpoint):

```powershell
python scripts/scad_build.py --design cicero --config designs/cicero/configs/rev_0001.json
python designs/cicero/measure_scale.py --verify-export
python designs/cicero/measure_scale.py --audit-only
```

The first command builds one unsplit reference STL and all 17 standard PNGs.
The second verifies the source hash, landmark membership, all exported triangles,
bounds, and ear-tip distance to **0.002 mm**; stores the STL as compact binary
without changing its topology; and generates two measurement PNGs plus a JSON
record. The audit checks source, config, SCAD, measurement script, STL, and PNG
hashes, preserved import hashes, and the exact flat output set. This is a
design-local measurement audit, not a complete multipart `build_manifest.json`
audit. Source coordinate selection uncertainty is separate from export accuracy.

Expected/actual generated scope: **1 STL and 19 PNGs** (17 standard + 2 measurement),
plus one JSON measurement record, in `output/cicero/`. The three original model
files and licensing README remain alongside them. `rev_0001` is a mutable config;
no immutable revision has been published. The confirmed printer volume is 220 x 220 x 220 mm; the current head layout is below.

## Historical face-up study

The earlier five-piece unjoined layout established the rule: choose a broad real
cut face for the bed before optimizing in-plane rotation. It has been superseded
by [the complete integral-joint candidate](../cicero_joined/README.md).
Its generated print artifacts have been removed to prevent confusion.
The byte-preserved [fit reference](assets/face_up_fit_reference.json) and source
`face_up.json` / `face_up_split.py` retain the measured exploratory evidence.
Do not regenerate that study into the current print set.

The current source/reference output contains 30 files: three generated reference
STLs, 20 PNGs, three JSON evidence files, three original imports and its README.
The complete printable manifest is managed separately under `output/cicero_joined/`.
The uncut head/base intermediate pair remains available below.

## Intermediate head/base STL exports

- [Head](../../output/cicero/head_intermediate.stl): **235.987 x 253.611 x 290.194 mm**, one closed shell.
- [Base](../../output/cicero/base_intermediate.stl): **437.540 x 342.234 x 333.673 mm**, retaining three overlapping closed source shells; no repaired union.

Both are capped at the tilted neck cut, retain assembly coordinates, and contain
no dovetails. See the [pair preview](../../output/cicero/intermediate_head_base.png),
[verification report](../../output/cicero/intermediate_exports_report.json), and
[provenance manifest](../../output/cicero/intermediate_exports_manifest.json).
The whole head requires subdivision; the current demonstrated flat-bed layout
uses six joined head pieces, without claiming an absolute minimum. The complete
candidate also contains eleven bust pieces; the older five-piece fit is retired.

```powershell
python designs/cicero/export_intermediates.py
python designs/cicero/export_intermediates.py --audit-only
```

## Approved joint architecture requirements

See the [seam map and conceptual assembly sequence](joint_architecture.md),
[gravity-seated dovetail protocol](../../references/engineering/joints/gravity_seated_dovetails.md),
and [flat-bed slicing playbook](../../playbooks/how_to_slice_large_objects_for_flat_bed_printing.md).
Preserve one continuous neck interface on one printed head owner and one printed
bust owner, attached with a single gravity-seated connection wherever feasible.
The complete candidate reserves continuous neck owners on both sides and
implements that single connection; the retired five-piece study is historical.
Assemble head and bust separately, then attach them through that major interface.

## Working neck plane and joint requirements

The working neck cut is **16.699 degrees from horizontal**, rising rearward:
**`Z = 0.3 Y + 304.341422 mm`** in assembly coordinates. Its source-plane origin
is `[0, 0, 31]`, with normal proportional to `[0, -0.3, 1]`.
This is a visually inspected working choice, not a physically measured optimum.
Parameters remain in [neck_interface.json](neck_interface.json).

The historical two-rail concept in `neck_interface.json` is superseded by the
single-connection requirement. Preserve that config for reference provenance;
do not treat its draft dimensions as approved production geometry. The retained
intermediate pair contains no joints. The complete candidate has integral rails,
loading channels and closed stops with sampled installation verification. Full
continuous motion, global material widths, retention and strength remain unverified.

## Artifact cleanup

Superseded freely tilted head-fit candidates and earlier whole-bust/neck study
outputs have been removed. Their source scripts/configs remain for provenance;
historical findings remain in archived plans and the journal. Current artifact
links distinguish the retained master/intermediate pair from the complete joined product.
Avoid regenerating historical diagnostics into the current output for routine use.

## Intended product and required scale

Use this 3D scan of Cicero's head from a bust to create a life-size printed
holder for the owner's Steam Frame VR headset. This introduces a scan-derived
modeling process to the repository: preserve an imported mesh, measure anatomical
landmarks, scale it, and derive joined printable pieces.

- The required straight-line distance between the two ear tips in the assembled
  model is **9 inches = 228.6 mm**. This dimension defines the requested life-size
  scale; do not substitute overall mesh width or independently stretch one axis.
- Identify and record both ear-tip landmark coordinates on the selected source
  mesh before scaling. Apply one uniform scale factor:
  `scale_factor = 228.6 / measured_source_ear_tip_distance`.
- Record the input mesh hash, its assumed units and orientation, the landmarks,
  and the complete scale/rotation/translation transform. Verify the final ear-tip
  distance after splitting and reassembly.
- Preserve the recognizable scanned surface, particularly the ears and headset
  contact regions. Any mesh repair or simplification needs comparison with the
  chosen source, including its effect on the landmarks.

## Printer limits and required split strategy

- The confirmed printer volume is **220 mm × 220 mm × 220 mm**. Bed-edge safety
  margin, brim/support allowance, and printer/material settings remain to be
  established. Every piece must fit in its actual print orientation,
  including its dovetails and required print allowances.
- Separate the **head from the lower bust/base along a plane suited to the tilted
  neck**, with dovetail connections that allow the head to reattach securely.
  The neck is tilted, so this cut must not be assumed horizontal. Determine its
  angle and position during mesh inspection, and record the plane's origin and
  normal in assembly coordinates. Check the resulting neck material, dovetail
  access, and print orientations before fixing the plane.
- Also split **both the head and the base vertically**, with dovetails joining
  their respective pieces. The initial four-main-piece interpretation did not fit the confirmed printer volume.
  The complete candidate uses six head and eleven bust printable leaves.
- The assembled ear-tip span exceeds either bed axis by **8.6 mm**. The requested
  split strategy remains a requirement; actual fit must be checked from all
  transformed piece bounds rather than inferred from ear span alone.
- Plan every dovetail's insertion direction, access, engagement, fit clearance,
  end stop or retention, and assembly order. Crossing neck and vertical
  seams must not trap a piece or prevent the remaining joints from sliding home.

## Strength, fit, and acceptance requirements

The reassembled structure must support the headset and loads from placing and
removing it. Establish headset contact locations, strap clearance, protection
for delicate surfaces, and base stability against tipping. Headset dimensions,
mass, contact geometry, intended storage pose, and any padding are not yet
measured; the ear-tip target alone does not establish headset fit.

Before choosing dovetail dimensions, declare `minimum_wall_thickness`,
`minimum_structural_overlap`, and `minimum_internal_edge_width`. Verify each
key's attachment to its own printed piece, the surrounding receiving material,
and the assembled mechanical load path independently of sliding clearance.
Retain sufficient material at dovetail roots, socket walls, and seam crossings
after all cuts. Values and structural checks remain unverified.

Require full-scale dovetail fit coupons before a full print, then verify mesh
closure/connectivity, print orientation, supports, each piece's bounds, complete
assembly access, and recombination against the scaled unsplit master except
for declared joint clearances or intentional changes. Use the repository's
[split/reassembly workflow](../../playbooks/how_to_design_split_print_parts_and_verify_reassembly.md)
and [structural-join workflow](../../playbooks/how_to_design_and_verify_structural_openscad_joins.md).
Final multipart output requires authoritative parts and assembly contracts,
the complete manifest build/audit, and review of the exact installed artifacts.

## Current tool-stack assessment

OpenSCAD supports importing an STL, uniform scaling, and Boolean intersections,
differences, and unions. These primitives can derive split volumes and add
parametric dovetail geometry around the imported scan; see the official
[OpenSCAD language reference](https://openscad.org/cheatsheet/snapshot.html).
The repository already supplies multipart builds, artifact audits, assembly
reviews, and split/fit/structural verification workflows. This is a feasible
starting approach, subject to testing Boolean operations on the actual mesh.

The existing automation does not constitute a verified end-to-end scan workflow:

- Initial ear-tip selection, source choice, orientation, scaling, and measurement
  are now recorded by the config and `measure_scale.py`. Landmark interpretation
  remains subject to user review. The complete candidate implements imported-mesh
  clipping, integral joints and bounded local vertex-fan separation.
- Imported mesh dependency provenance needs attention: `scad_build_all.py`
  currently hashes only `.scad` files for its source-tree digest. Changing an
  imported STL would not change that digest. The initial single-master measurement
  record audits its input mesh separately. The complete candidate supplements the
  standard manifest with geometry/input/asset hashes and independent verification.
- The existing imported files and licensing README in `output/cicero/` must be
  preserved deliberately before using the complete build pipeline, whose flat
  output contract rejects undeclared extras. The complete product uses a separate
  output destination, preserved source assets and a source/license README.

The initial scale/import/export and complete integral-product manifest builds pass.
Scan clipping, source-shell union and joint generation use design-local Python
and Manifold, followed by the normal OpenSCAD pipeline. Installed mesh checks and
full assembly-review audits pass for the complete candidate. Physical coupons,
continuous sweeps, material widths and structural capacity still need validation.
Shared build automation has not been changed for this task.

## License and attribution

**Creative Commons Attribution-NonCommercial-ShareAlike (CC BY-NC-SA)**,
as specified by the repository owner for this import. See the
[Creative Commons license overview](https://creativecommons.org/share-your-work/cclicenses/)
and the original listing for the applicable license version and full terms.

Retain credit to the original creator, the source link, and the applicable
license notice when sharing these files. Identify any changes, use the material
only for noncommercial purposes, and share adaptations under the same license
as required by its terms. This notice applies to the imported model and its
adaptations, rather than establishing a repository-wide license.

The source page could not be retrieved during documentation (HTTP 403).
The creator's name and exact license version remain unverified; consult the
linked listing for those attribution details. No creator identity or license
version is inferred from other Cicero listings.

## Verification status

The initial scale master was reviewed using `configs/rev_0001.json`, the exported
STL, standard isometric/front/side renders, and annotated landmark/dimension
images. Export verification passed with a maximum triangle-vertex error of
0.000849 mm against the uniform transform, with all 508,792 triangles retained.
The inherited geometry has not passed a topology, structural, or fabrication
audit. No revision/configuration is approved for fabrication. The SCAD declares
3 mm future targets for `minimum_wall_thickness`, `minimum_structural_overlap`,
and `minimum_internal_edge_width`; these are not verified measurements of the
scan. Structural joins and minimum material width remain **unverified**. Integral fabrication joins exist only in the complete candidate linked above;
no headset fit or print readiness is claimed.
