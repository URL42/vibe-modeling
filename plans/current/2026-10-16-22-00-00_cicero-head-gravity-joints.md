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
