---
plan_id: 2026-10-16-21-00-00_gravity-dovetails-and-flat-bed-slicing
title: Document gravity-seated dovetails and flat-bed slicing
summary: Establish reusable joint and slicing workflows and map Cicero seam ownership before production geometry.
status: past
created_at: 2026-10-16-21-00-00
---

# Document gravity-seated dovetails and flat-bed slicing

Key: `[ ]` pending task, `[x]` completed task, `[?]` needs validation, `[-]` closed task

Authority: user approved the proposed first checkpoint (written protocol plus Cicero seam/assembly diagram before jointed STLs), including one continuous major interface on one printable owner per side wherever feasible. No redundant approval prompt. Later production geometry is intended follow-up; this checkpoint does not assert it is built.

- [x] 1. Inspect current seam planes/neck contact ownership; distinguish measured current constraints from proposed printable ownership.
- [x] 2. Write a reusable gravity-seated dovetail protocol and large-object flat-bed slicing playbook, integrated into existing structural, split, motion, orientation and decomposition workflows and indexes.
- [x] 3. Document Cicero seam inventory, conceptual assembly diagram/sequence, single-owner neck interface requirement and unresolved feasibility gates. Preserve current geometry/configs/artifact bytes and mark prior two-rail neck proposal superseded.
- [x] 4. Verify document links, policy consistency, retained artifact provenance and indexes; append journal, review diff/status and archive this documentation checkpoint.

Expected files: references/engineering/joints/gravity_seated_dovetails.md; playbooks/how_to_slice_large_objects_for_flat_bed_printing.md; linked existing playbooks; AGENTS.md and README.md; designs/cicero/README.md and joint_architecture.md; plan/indexes and journal. No CAD export, manifest publication, commit or push. Joint dimensions, physical friction/strength, single-owner cut feasibility and final assembly insertion paths remain unverified until later geometry/coupon evidence.

## Outcome

Documentation checkpoint complete. Existing reference geometry/configs unchanged; no fabrication approval. Next production work must demonstrate single-owner neck-bearing leaves, base subdivision and compatible gravity-seated insertion paths before generating jointed outputs. Horizontal in-plane rear seams need a verified alternative mechanism or revised cuts.
