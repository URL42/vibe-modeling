---
plan_id: 2026-10-16-15-00-00_cicero-initial-scale
title: Establish the initial Cicero scale master
summary: Measure scan ear landmarks and build an unsplit 228.6 mm ear-span reference master with assembled bounds.
status: past
created_at: 2026-10-16-15-00-00
---

# Establish the initial Cicero scale master

Key: `[ ]` pending task, `[x]` completed task, `[?]` needs validation, `[-]` closed task

Authorized by the user's explicit atomic instruction to set up the initial scaled model; no redundant approval required per their clarification. Baseline: `f3ab27af2b71378703b933484b576199d2443545`. This is a single unsplit measurement reference, not a fabricated multipart product or immutable release.

- [x] 1. Preserve the original high-resolution STL as a licensed design asset; visually identify and record outer ear-rim landmarks and the source hash.
- [x] 2. Add `src/main.scad`, candidate `configs/rev_0001.json`, and a design-local measurement/verification script. Uniformly scale the ear-tip Euclidean distance to 228.6 mm, center XY and ground Z without rotation or cuts.
- [x] 3. Build one STL and 17 standard PNGs with `scripts/scad_build.py`; generate two annotated measurement PNGs and a JSON evidence record in `output/cicero/`. Verify exported landmark coordinates/bounds and source/config/artifact hashes. Preserve imported files and README. Binary STL normalization after export is permitted to avoid inflated ASCII storage, with geometry verified afterward.
- [x] 4. Update both READMEs and today's journal with selected landmarks, resulting assembled size, evidence and unverified fabrication limits. Review installed views, full intended diff/status, check indexes, and archive the completed plan.

No dovetails, mesh repair, decimation, split-plane decisions, automation-wide changes, numbered publication, commit, or push. Retain exact source triangles. Record physical landmark interpretation as an initial selection requiring user review, rather than claiming the scan has certified anatomical dimensions. Structural joins/material widths remain unverified on this inherited mesh.

Expected generated set: 1 scaled STL, 17 standard PNGs, 2 measurement PNGs and 1 JSON evidence record, in addition to the preserved original 3 model files and README. Remove temporary inspection PNGs on success. No `parts.json`: this is a single reference master, not the future multipart implementation.
