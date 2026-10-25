---
plan_id: 2026-10-24-11-00-00_fix-build-automation-review-findings
title: Fix build-automation review findings
summary: Correct revision numbering, make revision publication fail clean, bind design assets into build provenance, detect stale builds by audit, make provenance hashes line-ending independent, and restore passing audits for every multipart design.
status: past
created_at: 2026-10-24-11-00-00
---

# Fix build-automation review findings

Key: `[ ]` pending task, `[x]` completed task, `[?]` needs validation, `[-]` closed task

User approval: "plan approved. Use your judgement on the two decisions. I want this to be functional." (2026-10-24). Decisions taken: `--dry-run` becomes read-only; `cicero_joined` is rebuilt so its audit passes under the new asset binding.

Plan revisions approved during execution: "Normalize + migrate (Recommended)" for CRLF-dependent manifest hashes, and "Move to designs/<d>/slicer/ (Recommended)" for slicer projects inside governed outputs.

- [x] 1. Publish the staged candidate under its own revision number.
  - [x] 1.1 `scad_new_revision.py`: when `--base-config` is `configs/rev_N.json` and `revisions/<design>/rev_N/` does not exist, publish `rev_N` from that config without writing a new config.
  - [x] 1.2 Keep next-unused-number behavior when the base config's revision is already published; print which case applied.
  - [x] 1.3 Write `params.json` as a byte copy of the config so revision audits match hand-formatted candidates.
- [x] 2. Make revision publication fail clean.
  - [x] 2.1 Remove the config file and revision directory the command created when the build fails.
  - [x] 2.2 Make `--dry-run` write nothing.
- [x] 3. Bind design assets into complete-build provenance.
  - [x] 3.1 `scad_build_all.py`: record an `assets` hash when `designs/<design>/assets/` exists; audit fails when it is missing or differs.
  - [x] 3.2 Rebuild and audit `output/cicero_joined/` (printable set and full assembly review).
- [x] 4. Detect stale builds by audit instead of mtimes.
  - [x] 4.1 `rebuild_stale_designs.py`: rebuild when `scad_build_all.py --audit-only` fails.
- [x] 5. Fix the macOS `/private/var` path comparison in `tests/test_scad_unified_output.py`.
- [x] 6. Make provenance independent of checkout line endings (revision).
  - [x] 6.1 Hash and size text files (no NUL byte) with CRLF folded to LF in `scad_build_all.py`; reuse it in `scad_render_assembly_review.py`.
  - [x] 6.2 Migrate `output/*/build_manifest.json` and `output/*/assembly_review_manifest.json`, rewriting a hash only when the old hash is proven against the on-disk file in LF or CRLF form. `revisions/` manifests are immutable and left unchanged.
  - [x] 6.3 Rebuild `output/cyberdeck/` (rev_0030), whose recorded source hash matches no committed source version.
- [x] 7. Move hand-made slicer projects out of governed outputs (revision).
  - [x] 7.1 `git mv` the `.3mf` files of `ac_redirectors` and `cicero_joined` to `designs/<design>/slicer/`.
- [x] 8. Documentation and verification.
  - [x] 8.1 Update README, AGENTS.md, and the revision-publication playbook.
  - [x] 8.2 Add regression tests for items 1-4 and 6; run the full test suite.
  - [x] 8.3 Audit every multipart design; regenerate and check plan indexes; record the journal checkpoint.
  - [x] 8.4 Apply independent-review should-fix items: no out-of-order in-place publication, review-side asset check, hidden files excluded from asset hashes.
