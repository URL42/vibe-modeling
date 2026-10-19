---
plan_id: 2026-10-16-22-00-00_cicero-head-gravity-joints
title: Implement gravity-seated joints for the Cicero head
summary: Resolve a continuous neck owner, add installable head joints, and verify flat-bed outputs.
status: current
created_at: 2026-10-16-22-00-00
---

# Implement gravity-seated joints for the Cicero head

Key: `[ ]` pending task, `[x]` completed task, `[?]` needs validation, `[-]` closed task

Authority: user instructs implementation on the head after approving the protocol. Preserve originals/current reference provenance. Latest user correction explicitly rejects separate keys and requires completion of neck/bust connections. Integral mating features only; add bust leaves and a single head-to-bust connection. No commit or push.

- [x] 1. Establish printable single-owner neck-bearing head region and revised head cuts preserving the face-up section.
- [?] 2. Implement shared gravity-seated joints and complete verification.
  - [x] 2.1 Implement face sliding dovetails, explicit horizontal drop-in sockets and two midline splines with seated stops and gravity-directed travel.
  - [x] 2.2 Verify closed single-shell exports, flat-bed contact/envelopes, sampled installation states, ear landmarks and single-owner neck cap.
  - [?] 2.3 Complete shortest post-cut material/structural sections, full continuous swept envelopes, anti-lift retention decision, slicer review and production-derived physical coupons. Existing candidate remains unverified for fabrication; these checks are not claimed complete.
- [x] 3. Declare head parts/assembly and config; build/audit complete installed outputs and review installed parts/assembly. Preserve source dependencies and reference output.
- [x] 4. Update design documentation/journal, verification evidence and plan lifecycle/indexes. Physical coupons/strength remain unverified until printed.

Expected files: design-local head source/config/manifest/contracts and verification, head STLs/PNGs and provenance in governed output, documentation and journal. A separately named cicero_head subassembly design/output may isolate the complete head artifact set from existing cicero imported/reference artifacts. First demonstrate geometry before choosing exact part count. Printer 220 mm cube, 5 mm provisional XY margin, true broad flat cut face down. No silent downgrade to freely tilted prints or divided neck ownership.

## Superseded head-only evidence

Eight printable leaves: six body regions plus two keys. The whole neck cap is on
one owner through a 6 mm neck-plane band; a 121 mm2 face-owned sliver discovered
during verification was corrected before the accepted build. Body contact faces
remain flat; all parts fit 210 mm XY / 220 mm Z. Assembled ear span 228.600191 mm;
neck-cap symmetric area difference 0.014673 mm2. Complete output/audits pass with
9 STL (8 printable + 1 assembled reference), 146 PNG and 2 manifests, 157 files.
Geometry/build/review checkpoint delivered; plan remains current because structural,
continuous motion and physical verification are unresolved. No commit or push.

## User correction: integral joints and complete product

Separate connector keys are rejected. The prior head-only candidate is superseded
as the target architecture, not fabrication-approved. Continue under the user's
explicit correction; do not request redundant approval.

- [x] 5. Replace separate midline keys with integral male/female joints and choose unaffected broad bed faces; inventory every head cut and actual mating pair.
- [x] 6. Split the bust with one continuous upper neck owner, add integral joints to every actual bust seam and one head-to-bust dovetail on its single owners.
- [x] 7. Build one complete product manifest/assembly with separately identified head and bust subassemblies, no connector-only printable leaves; verify actual bed contact, installation states, seam coverage and all artifact provenance. Clearly supersede the earlier output sets.
- [x] 8. Update protocol/design docs/journal and review exact installed artifacts. Keep physical fit, strength and unresolved material checks explicit.

Expected additional scope: a complete product design/output under cicero_joined,
including direct integral geometry, all head/bust printable leaves, hierarchy,
seam inventory and a single neck connection. Preserve original imported/reference
artifacts; mark the prior cicero_head candidate superseded rather than imply its
bare neck or omitted bust is complete.

## Complete integral-product checkpoint (2026-10-17)

The rejected key-based output is removed and its manifests are renamed historical
so automatic rebuilding cannot restore it. The current candidate is
`designs/cicero_joined/configs/rev_0001.json`: 17 body leaves (6 head, 11 bust),
33 actual mating pairs, no connector-only leaves, and one head-to-bust dovetail.
The face owns no neck sliver; each side of the major interface is continuous.
The two internal bust-neck rails use 10 mm travel / 8 mm length after whole-model
sampling found a shoulder collision at the earlier 20 mm travel. Width, depth,
root and stock targets are retained. All asset-level sampled assembly stages pass.
The complete standard build installs 17 STL / 289 PNG and passes its audit.
Exact installed verification and the new full assembly review pass: 20 STL,
304 PNG and two manifests (326 flat files). Sixteen whole-model assembly stages
pass sampled collision checks; maximum diagnostic overlap is 0.009958 mm3.
The installed ear span is 228.600188 mm. See cicero_joined/assembly_review.md.
Continuous sweeps, global material paths, anti-lift retention and physical fit/load
remain open under item 2.3. No commit or push is authorized.

## User-directed face correction and exploded views (2026-10-18)

Authority: user reports eye recesses open at the back and requests deeper face
plus separate multi-angle exploded head/bust views. Execute this atomic correction.

- [x] 9. Restore deeper face plane, reserve neck-bearing band on collar; verify
  uninterrupted pre-joint rear face cap, flat-bed fit, all joints and assembly paths.
- [x] 10. Add five exploded angles each for head and bust, complete governed build,
  installed verification and artifact-bound review; update docs and journal.

Expected: cicero_joined generator/assets/contracts, current output, verification,
README/review record and today's journal. Preserve single neck owners, integral
joints and original scan; no commit/push. Mutable config rev_0001 remains current.

Items 9-10 verified complete: deeper face has an uninterrupted rear cap and
installed solid eye-backing probes through 4 mm. All 17 leaves / 33 mating pairs /
16 sampled installation stages pass; ear span 228.600190 mm. Ten separate exploded
views visually reviewed, five each for head and bust. Complete current totals:
20 STL / 314 PNG / 2 manifests, 336 flat files; all artifact/provenance audits pass.
Earlier evidence above is historical. Item 2.3 remains open; no commit or push.

## Commit and push authorization (2026-10-18)

User explicitly keeps the neck pieces separate and authorizes committing every
repository change and pushing all local commits. Include generated artifacts.
The assembled product STL exceeds 100 MiB; track that exact artifact with Git LFS,
leaving its working-tree bytes and provenance hashes unchanged. Record LFS checkout
requirements. Items 9-10 remain complete; unresolved physical/structural work
under item 2.3 keeps this plan current. No geometry changes in this checkpoint.
