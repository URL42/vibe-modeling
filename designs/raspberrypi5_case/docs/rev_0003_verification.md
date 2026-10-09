# rev_0003 base mounting recess verification

Approved configuration: `configs/rev_0003.json`, 2026-10-09. Baseline: commit
`f684d15`, rev_0002 printed lid. This candidate changes the base floor from
3 to 6 mm inward and adds four diameter-5 x 3 mm deep underside head recesses.
The existing diameter-2.7 bores and centers remain (8.5,35.5), (66.5,35.5),
(8.5,84.5), (66.5,84.5). Recess ceilings are z3, mounting surface z6.

## Frozen printed-lid interface

`rev_0002_lid_compatibility.json` captures the baseline lid source hash,
canonical sorted-triangle geometry hash and every frozen configuration input.
Only floor thickness, status and the new base recess parameters differ.
Lid source bytes, lid geometry, 7 mm slab, four screw stations, z113 seating
plane and the 15 x 15 x 3 mm studs at z110..113 must match the baseline.
Previous configs remain intact; a default recess depth of zero preserves them.

## Structural dimensions and scope

Minimum wall, structural overlap and internal material width are 3 mm.
Wall/floor embed is now 6 mm; stud/wall attachment remains 3 mm throughout.
The new recesses leave 3 mm floor above each seat, 6 mm to the closest exterior
x face and 3 mm to the adjacent side-wall inner face. All six recess pairs are
guarded; orthogonal head-to-head ligaments are 53 and 44 mm. Recesses cannot
enter the wall seam. The concentric stepped void has an approved 1.15 mm radial
seating face supported by 3 mm axial floor. This hardware seating detail is an
explicit exception to the radial-strip rule, alongside the retained lid's
1.8 mm radial seat. Remaining structural ligaments must meet the 3 mm minimum.

The floor rises 3 mm inside the base. PCB, fastener length, physical head fit,
supports, slicing and mechanical strength have not been physically tested.
No claim of printer-specific fabrication readiness is made.

## Artifact and validation record

Digital printable-leaf verification passed: two closed consistently wound,
positive-volume connected shells, exact base bounds (0,0,0)..(120,120,113),
lid bounds (0,0,113)..(120,120,125), and all 69 final-STL line sections.
The measurements confirm each 5 mm recess diameter, 3 mm depth, 3 mm seat roof,
original 2.7 mm through-bores, flat underside and unchanged coupling stations.
Negative checks reject incorrect 2/4 mm recess depths and an opened shell.
The canonical exported lid triangle hash equals the printed rev_0002 reference:
`36281ee5052ce08af6e37fa510e84be303be2fedb1597a69591725c9751b3a6c`.
Lid source hash and every frozen input also match. Installed printable images
were reviewed in all 34 views; orthographic shading alone cannot show seat depth,
so final-mesh sections and underside/isometric views supply the depth evidence.
Structural joins: passed. Minimum internal material width: passed with the
explicit hardware seating-face exceptions above.

The final complete/supplementary audit and installed assembly image findings
are recorded in the 2026-10-09 journal checkpoint. Their exact input hashes and
artifact hashes are in `build_manifest.json` and `assembly_review_manifest.json`.
The build Git baseline is f684d15 with task changes present; this candidate is
mutable output, not an immutable numbered revision or a pushed deliverable.
Complete printable set: 2 STL and 34 PNG. Supplementary full assembly
set: 1 review-only STL and 19 PNG, including underside isolation and sections
through both mount rows. Final flat output: 3 STL, 53 PNG, two manifests
(58 files) in `output/raspberrypi5_case/`.

Reproduction checks: installed build audit, two closed oriented connected meshes,
69 final-mesh line sections, exact printed-lid geometry/input comparison,
review of installed printable images, then artifact-bound assembly review
and both manifest audits. Source assertions protect floor roofs, wall joins,
all exterior margins and all six recess pairs.
