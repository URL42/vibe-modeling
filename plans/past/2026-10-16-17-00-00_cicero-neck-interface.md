---
plan_id: 2026-10-16-17-00-00_cicero-neck-interface
title: Establish Cicero neck cut and dovetail interface first
summary: Refine the neck cut in the turned head's frame, study a sliding dovetail interface, before any further head/base partitioning.
status: past
created_at: 2026-10-16-17-00-00
---

# Establish Cicero neck cut and dovetail interface first

Key: `[ ]` pending task, `[x]` completed task, `[?]` needs validation, `[-]` closed task

Authority: user's explicit instruction to start with the neck cut/dovetail angle, then separate the head and base independently. This supersedes choosing a fixed whole-bust twelve-piece architecture. Preserve existing pending work, imported meshes, scale config, and unsplit master.

- [x] 1. Derive a head-aligned lateral/posterior frame from the ear landmarks; compare tilted neck planes, including a slightly lower origin to avoid clipping the chin. Record angle, origin, normal, anatomical uncertainty, and diagnostic sections.
- [x] 2. Define a preliminary pair of parallel head-owned dovetail rails and base-owned rear-open receivers with a common insertion direction, explicit root engagement/clearance/material dimensions, gravity-seating stop, and separate retention requirement. Measure section containment/margins through rail roots and receiving depth; report unverified outlet/sweep/strength limits.
- [-] 3. Head/base subdivision studies deferred following the user's correction: current work is only the neck cut and dovetail. Removed the new subdivision parameters/results from this study; retained older artifacts as diagnostic history only.
- [x] 4. Add reproducible design-local config/script, diagnostic PNGs and JSON evidence/provenance; extend the diagnostic audit's declared files, verify unchanged master geometry and source/config provenance, record results in README/journal, review artifacts and diff, and archive this focused study.

Expected changes: `designs/cicero/neck_interface.json`, `study_neck_interface.py`, design/output READMEs, minimal diagnostic audit extension, journal and plan/index. Outputs under `output/cicero/`: `neck_interface_angles.png`, `neck_interface_joint.png`, `neck_interface_report.json`, `neck_interface_manifest.json`. Generated geometry remains diagnostic only: no printable STL exports, source repair, production SCAD changes, immutable publication, or commit/push. Root/receiver support and joint exit checks remain unverified until actual Boolean cut solids and insertion sweeps are reviewed. Head/base subdivision studies must not cut a rail/receiver without an explicit ownership policy.

Verification: synthetic frame orthogonality and section/point-containment checks; source/config/master hashes; selected-point export ear span; section offsets and actual measured planar margins; positive/negative diagnostic provenance audits; documentation links; plan indexes and Git diff/status.
