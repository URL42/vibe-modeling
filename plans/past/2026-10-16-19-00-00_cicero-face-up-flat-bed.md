---
plan_id: 2026-10-16-19-00-00_cicero-face-up-flat-bed
title: Develop a face-first head split with flat cut faces on the bed
summary: Find the deepest face-up section and divide the rear head only as needed using broad planar bed contact rather than arbitrary tilted orientations.
status: past
created_at: 2026-10-16-19-00-00
---

# Develop a face-first head split with flat cut faces on the bed

Key: `[ ]` pending task, `[x]` completed task, `[?]` needs validation, `[-]` closed task

Authority: user approved the face-first strategy with “go ahead”. Each candidate must print with an actual cut plane horizontal on the build plate; optimize only rotation within that plane. Prior arbitrary-tilt head-fit results are superseded as a practical printing recommendation. Preserve all pending work/imports and the established scale/neck cut.

- [x] 1. Search face-plane position and anatomically reasonable pitch, retaining the face as one connected section. Move the cut rearward only while its flat-bed footprint and height fit the confirmed 220 mm cube; use a separately declared provisional 5 mm XY margin and inspect facial feature preservation.
- [x] 2. Test rear left/right halves on their actual flat cut faces. Add top/bottom cuts only where the bed/height constraints require them. Do not claim a globally minimal layout or support-free sculpted surfaces.
- [x] 3. Export the face and required rear regions as intermediate reference STLs stored with their chosen cut faces flat at Z=0; verify actual bounds, planar contact, closure/winding, connected shells, recombination, and source/config/artifact provenance. No dovetails or final assembly approval in this geometry-fit checkpoint.
- [x] 4. Produce an assembly/bed-contact review PNG and quantitative JSON/provenance record; update current READMEs/journal, mark rejected tilted recommendations accurately, extend the diagnostic output audit, verify indexes/diff/status, and archive completed study.

Expected files: design-local face-first script/config; named face/rear intermediate STLs, review PNG(s), findings/provenance JSON under flat `output/cicero/`; audit extension and documentation. New artifacts are diagnostics and fit witnesses, not a complete printable multipart release. Structural joins/material widths, final connectors, support settings and physical validation remain unverified. No commit/push.

## Outcome

Five intermediate pieces demonstrated: one complete face and four rear regions after a rear-only Z=460 mm cut. All are exported on broad actual cut faces at Z=0; no arbitrary tilt. Face 209.95 x 209.95 x 49.09 mm; all rear regions fit the 210 mm XY study envelope and 220 mm height with >20,500 mm2 bed contact. Reference geometry only; joining/support/physical verification remains future work.
