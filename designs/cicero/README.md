# Cicero

Documentation for the imported [Cicero model on MyMiniFactory](https://www.myminifactory.com/object/3d-print-cicero-55952).
The existing STL and 3MF files are in [output/cicero](../../output/cicero/README.md).
This design folder currently contains documentation only; no OpenSCAD source,
configuration, or verified build is provided.

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

- The available printer footprint is **220 mm × 220 mm**. Usable Z height,
  bed-edge safety margin, brim/support allowance, and printer/material settings
  remain to be established. Every piece must fit in its actual print orientation,
  including its dovetails and required print allowances.
- Separate the **head from the lower bust/base along a plane suited to the tilted
  neck**, with dovetail connections that allow the head to reattach securely.
  The neck is tilted, so this cut must not be assumed horizontal. Determine its
  angle and position during mesh inspection, and record the plane's origin and
  normal in assembly coordinates. Check the resulting neck material, dovetail
  access, and print orientations before fixing the plane.
- Also split **both the head and the base vertically**, with dovetails joining
  their respective pieces. A left/right split yielding four main pieces is a
  working interpretation, pending inspection; exact planes, positions, and final
  part count are not yet fixed.
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

- Ear-tip selection, source-mesh choice, orientation, measurement, and any repair
  still need a reproducible method. No Cicero-specific mesh inspection or
  dovetail generator has been implemented.
- Imported mesh dependency provenance needs attention: `scad_build_all.py`
  currently hashes only `.scad` files for its source-tree digest. Changing an
  imported STL would not change that digest. Record and audit input-mesh hashes
  before claiming complete provenance for a scan-derived build.
- The existing imported files and licensing README in `output/cicero/` must be
  preserved deliberately before using the complete build pipeline, whose flat
  output contract rejects undeclared extras. Choose a governed source-asset
  location and license-notice handling as part of implementation.

First inspect and measure the scan, then test a representative Boolean cut and
dovetail coupon with OpenSCAD. That evidence will determine whether mesh repair
or another mesh-processing tool is needed. Tool additions and build-automation
changes are future implementation work; this checkpoint documents requirements
and assesses feasibility only.

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

The imported geometry and its modification history have not been audited.
No revision/configuration has been reviewed for fabrication. Structural joins,
minimum wall thickness, and minimum internal material width are unverified for
the imported geometry.
