---
plan_id: 2026-10-16-13-40-00_cicero-license-readmes
title: Document Cicero source and licensing
summary: Add source attribution and user-specified CC BY-NC-SA licensing notices to the imported Cicero folders.
status: past
created_at: 2026-10-16-13-40-00
---

# Document Cicero source and licensing

Key: `[ ]` pending task, `[x]` completed task, `[?]` needs validation, `[-]` closed task

- [x] 1. Create `output/cicero/README.md` with the supplied MyMiniFactory source URL, CC BY-NC-SA notice, attribution verification status, and inventory of the existing imported files.
- [x] 2. Create `designs/cicero/README.md` with matching licensing details and relative links to the output folder; identify this as an imported model with no OpenSCAD source/config or verified build.
- [x] 3. Verify links, matching notices, and preservation of existing model files; leave license version and creator unspecified unless confirmed for the exact source object.
- [x] 4. Record the documentation checkpoint in `journal/2026-10-16.md`, archive this completed plan, regenerate/check indexes, and review the intended diff and Git status.

## Scope and approval

Authorized by the user's specific atomic instruction, reaffirmed after the unnecessary approval request. Completed and archived. Documentation only: preserve all existing STL/3MF files. No CAD generation, geometry edits, build claims, commit, or push. The user's requested output README is an explicit addition to the imported output folder, not a claim of manifest compliance.

## Source evidence

- User supplied source: https://www.myminifactory.com/object/3d-print-cicero-55952
- User specified CC BY-NC-SA. Direct page retrieval returned HTTP 403; the exact creator and license version have not been independently verified. Do not substitute metadata from another Cicero model.
- Existing files: `2.stl`, `5352-tsaritsyno-museum-moscow-bust-5(1).3mf`, and `simplified.stl`.

## Verification

Review both Markdown documents and relative links; compare existing model file hashes before/after. Run `python scripts/regenerate_plan_indexes.py --check --repo-root .`. Structural checks are not applicable to this documentation-only change.
