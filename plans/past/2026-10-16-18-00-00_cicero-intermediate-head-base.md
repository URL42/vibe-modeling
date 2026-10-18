---
plan_id: 2026-10-16-18-00-00_cicero-intermediate-head-base
title: Export Cicero intermediate head and base and assess head splits
summary: Export capped intermediate head/base reference meshes at the neck plane and test the smallest feasible head split count without claiming unproven minimality.
status: past
created_at: 2026-10-16-18-00-00
---

# Export Cicero intermediate head and base and assess head splits

Key: `[ ]` pending task, `[x]` completed task, `[?]` needs validation, `[-]` closed task

Authority: explicit user request for a pair of intermediate STL artifacts and an assessment of whole-head fit and minimum printable head pieces. Preserve current neck plane, original imports, and all pending work. This supersedes further angle-only study. No redundant approval required for this specific instruction.

- [x] 1. Add a reproducible mesh clipping/capping exporter and write `output/cicero/head_intermediate.stl` and `base_intermediate.stl` in unchanged assembly coordinates at the established 16.699-degree neck plane. Label these intermediate reference meshes, with no dovetails or final printable-leaf claims; preserve and report existing base shell overlaps.
- [x] 2. Verify cap closure/winding, component counts, cut-plane location, recombination by exterior area and signed-volume conservation, bounds, and source/config/artifact hashes. Generate a review PNG and report.
- [x] 3. Test whole-head and increasing small split counts against 220 mm nominal cube and separate print allowances. Prioritize one and two pieces, then three/four if needed. Report concrete fit witnesses and distinguish smallest demonstrated layout from a mathematical minimum; do not claim physical print readiness without joints/supports/material verification.
- [x] 4. Extend diagnostic evidence audits for the exact retained intermediate exports/report/preview; update README/journal and superseded neck-study plan, verify indexes, review installed artifacts and intended diff/status, and archive completed work.

Expected new files: design-local exporter and fit-study script/config as needed; intermediate/reference STL pair, geometry/fit report, provenance JSON, review PNG under flat `output/cicero/`; no production geometry/manifests or immutable release. Any additional candidate head STL exports must be explicitly named in the report/audit and remain intermediate references. No commit/push. Structural joins and minimum material widths remain unverified; no joints are added in this step.
