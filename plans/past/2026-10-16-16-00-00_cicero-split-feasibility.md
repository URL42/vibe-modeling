---
plan_id: 2026-10-16-16-00-00_cicero-split-feasibility
title: Investigate Cicero split and dovetail feasibility
summary: Audit the scaled scan, preview a tilted neck separation, and measure candidate split footprints before defining printable dovetail parts.
status: past
created_at: 2026-10-16-16-00-00
---

# Investigate Cicero split and dovetail feasibility

Key: `[ ]` pending task, `[x]` completed task, `[?]` needs validation, `[-]` closed task

Authority: user approved the presented next steps with “go ahead”; use existing ear landmarks as the working scale. Preserve the pending initial-scale work and all imports. Existing baseline: `configs/rev_0001.json`, unchanged unsplit master. Printer footprint 220 × 220 mm; user confirmed usable volume 220 ? 220 ? 220 mm; material/nozzle settings remain unknown.

- [x] 1. Record reproducible mesh edge, winding, degeneracy, and shell checks, with explicit limits on self-intersection/Boolean claims.
- [x] 2. Analyze neck sections to select and annotate an oblique candidate separation in source and assembly coordinates. Generate diagnostic views, not approved fabrication parts.
- [x] 3. Clip scan triangles against candidate neck and vertical ownership planes analytically, including plane intersection vertices; search print orientations and report XY footprints and Z requirements for the four-piece concept and any necessary additional subdivisions. This is fit analysis without dovetails/support allowances, not a completed multipart build.
- [x] 4. Define feasible dovetail insertion directions/assembly sequence and coupon questions if supported by findings. If geometry, printer limits, or source topology prevent final joint design, document the concrete issue and required next plan instead of exporting misleading printable pieces or a guessed coupon.
- [x] 5. Add design-local reproducible analysis/evidence commands and retained diagnostic artifacts to the single-master audit contract; verify preservation/provenance, update README/journal, review diagnostics, and archive this investigation when no analysis execution remains.

Expected files: `designs/cicero/analyze_splits.py`, `designs/cicero/split_study.json`, additions to the existing measurement audit for diagnostic evidence, design/output READMEs and root README if commands/workflow change, today's journal, plan/index; diagnostic PNG/JSON only under `output/cicero/`. No production source/config/scale changes, mesh repair, cut STL exports, printable manifest, or immutable release at this investigation checkpoint. Production dovetails/coupons depend on a justified split and confirmed printer envelope. Any future multipart geometry must first satisfy parts/assembly contracts and the normal complete-build pipeline.

Verification: exact hash preservation of imports and unchanged initial-master triangle geometry (normal encoding was refreshed by the existing verifier before its byte-preservation correction); source/config/script/analysis/evidence hashes; mesh topology checks; polygon clipping partition area conservation; synthetic plane clipping/rotation checks; diagnostic image review; positive and negative evidence audit tests; plan-index validation and intended diff review. Structural joins/material widths remain unverified.

## Outcome

Investigation complete. Four-piece candidate fails the cube-diagonal bound; a twelve-main-piece candidate fits the conservative envelope before joints/supports. Source shells overlap. Production layout preference requested; production solid union, assembly/parts contracts, dovetail sweeps, and derived coupons are future work after selecting that materially different architecture. No production geometry was changed.
