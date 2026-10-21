---
plan_id: 2026-10-18-23-59-27_6u-cyberdeck-4u-control-cover
title: Add a two-piece 4U control cover to the 6U cyberdeck
summary: Resolve legacy control interfaces and printer limits, then add a removable rail-mounted 4U panel with four logical control regions and two printable halves.
status: current
created_at: 2026-10-18-23-59-27
---

# Two-piece 4U control cover

Key: `[ ]` pending task, `[x]` completed task, `[?]` needs validation, `[-]` closed task

## Scope and approval

Approved extension of `plans/current/2026-10-04-11-35-16_create-6u-cyberdeck.md`.
User approved this cover implementation with "ok go ahead" on 2026-10-19.
Promoted before substantial edits. Original case-correction approval was separate.
User explicitly authorized committing everything and pushing on 2026-10-21.

The cover is a removable logical subassembly with two printable leaves split at
X=0 between the rails. Four logical control quadrants do not create four parts.
Bottom left and bottom right each center one joystick mounting pattern. Top left
has four arcade buttons in a 2x2 grid; top right has four in a diamond. Provide
integral M3 seam hardware stations near both ends of the center seam, with no
third printed joining piece. Mount the panel onto the existing front rail faces.

## Discovery and open inputs

- [x] Search present sources and available Git history for legacy control interfaces.
  Arcade defaults in `designs/cyberdeck/src/lib/defaults.scad` declare 28 mm
  mounting holes, 35 mm outer envelopes, 5 mm mounting margin and 40 mm spacing.
  Earlier config rev_0002 uses a 34 mm outer envelope. These are historical
  design assumptions, not measurements of the user's controls. No joystick
  pattern was found by joystick/thumbstick/stick searches or Git content history.
- [x] Calculate preliminary nominal bed fit: full face 254 x 177.8 mm, each half
  127 x 177.8 mm. A 14 mm seam projection gives 141 x 177.8 mm before supports,
  brim and any additional hardware features. This fits the existing assumed
  220 x 220 mm bed with 5 mm reserve per side, but is not a printer confirmation.
- [x] Resolve printer maximum dimensions: user confirmed 220 x 220 x 220 mm.
  Retain 5 mm per-side XY reserve, giving 210 x 210 mm usable before any
  additional adhesion allowance; verify final geometry against this budget.
- [x] Recover joystick cut pattern: early cyberdeck `_left_lid_aux_cut_pattern`
  uses a 30 mm center opening and four 3.4 mm holes on an 80 x 40 mm rectangle,
  X spanning 80 mm. User reports that the earlier printed pattern works.
  Hardware/body/wiring envelopes beyond this cut pattern remain unmeasured.
- [x] Confirm which 4U position is covered: user selected lower 4U, leaving upper
  2U open. This changes installation datums, not the four control-region layout.
- [?] Confirm button retention/body envelopes and allowable panel thickness;
  document any remaining assumptions explicitly.

### Follow-up legacy search

User identified the early cyberdeck as the joystick source. Inspected initial
commit `ad0447c` defaults and source, and searched all available Git history with
case-insensitive joystick/thumbstick/joy_stick/Sanwa content patterns. The only
joystick references recovered are the Cyberdeck-2 redesign plan introduced in
`a2fffec` and removed in `cd5867b`: it proposes a joystick and diamond buttons,
but explicitly lists the exact joystick mounting pattern as a missing input.
The subsequent geometry-based search found the numerical interface under the
generic auxiliary mounting/cable name in current retained early cyberdeck source:
`src/lib/defaults.scad` lines 205-214 and
`src/parts/cyberdeck.scad` module `_left_lid_aux_cut_pattern` around line 4216.
This supersedes the earlier keyword-search finding; no generic footprint is used.
Git history identifies commit `0d921ee` as the introduction of this auxiliary
pattern, confirming it predates the current rack design.

### Concrete implementation mapping

Preserve IDs 1-5; add ID 6 `control_cover_left` and ID 7 `control_cover_right`.
Normal build changes from 5 STL / 85 PNG to 7 STL / 119 PNG (17 PNG per leaf).
Use 3 mm face thickness, 177.2 mm panel height (0.6 mm total fit gap), center at
case Z=-44.45, face Y=-3 and underside Y=0. Two tongue/receiver clamps use
M3x10 screws, 7 x 0.5 washers and 5.5 AF x 2.4 nuts, near both seam ends;
four rail attachments use M3x10 with washers and existing rail captive nuts.
Integral receiver bosses total 9.8 mm depth from front, with 3 mm face overlap,
3 mm tongue and 4 mm bearing web ahead of a 2.8 mm rear-entry nut pocket.
Print both faces down; right socket roof needs a production-derived bridge coupon
and slicer review. Joystick fasteners and full device bodies remain unverified.

## Approved implementation checklist

- [x] Freeze a new rev_0003 config with rack datums, panel fit gap, PLA,
  0.4 mm nozzle, 0.2 mm layers, minimum wall and overlap parameters.
- [x] Add a control-cover subassembly and two authoritative leaf identities to
  the existing design manifests, preserving the five case/bridge identities.
- [x] Model rail fastener clearances, two integral center-seam clamp stations,
  and production-derived seam coupon geometry without adding a third cover leaf.
- [x] Center both recovered lower joystick cut patterns and place the upper
  grid/diamond; check declared 35 mm button envelopes, 28 mm holes and pattern
  placement against rails, seam stations and case geometry.
- [?] Verify complete joystick brackets/bodies, button retention/terminals,
  wiring, shaft travel, hand access and actual joystick screw lengths when
  measured hardware is available. Historical working holes do not establish
  these new assembly envelopes or PLA stiffness.
- [x] Assert face cut-pair ligaments, edge margins, root overlap and mechanical
  support paths; measure final STL joints and declared nominal screw stacks.
- [?] Verify actual driver handles, purchased screw/nut dimensions and complete
  device installation/removal envelopes physically; bench assembly sequence is
  documented, but complete hardware and wiring dimensions remain unknown.
- [x] Verify actual transformed print bounds of both complete cover leaves,
  including joints and underside bosses, against confirmed printer limits.
- [x] Run the governed complete manifest pipeline, installed artifact audit,
  installed artifact visual review and provenance-bound assembly review.
- [x] Extend geometry verification for controls, seams, rail attachment and
  intentional separate leaves; record exact config and source provenance.
- [x] Update design README, revision evidence, root navigation if relevant,
  plan indexes and today's append-only journal. Keep physical fit/strength and
  slicer behavior unverified until demonstrated; publish no immutable revision
  before the corresponding gates and approval.

## Expected files and verification

Expected changes: `designs/6u_cyberdeck/{src,configs,parts.json,assembly.json,README.md,docs}`,
`output/6u_cyberdeck/`, this plan, plan indexes, journal and relevant root docs.
Read-only references: historical cyberdeck control sources and rack specification.
No changes inside `agentic-pipelines/` or to unrelated Cicero work.

Use the host iteration, decomposition, manifest, structural joins, fastener,
clearance, split/reassembly, print-orientation, assembly-review and provenance
playbooks. Require complete manifest counts derived from updated contracts,
passing artifact/config/source hashes, flat output and no surviving staging.
Digital geometry checks do not establish PLA strength or physical control fit.

## Digital checkpoint result (2026-10-20)

Approved modeling and digital artifact work completed for rev_0003. Complete
normal 7 STL /119 PNG plus full review4 STL /34 PNG, unified11 STL /153 PNG /
2 manifests,166 flat files. Both audits, contract/geometry validation and
reference validation passed; installed config/source/STL provenance matches.
All119 normal and34 assembly PNG reviewed. Cover196 material sections,34 span
sections,9528 analytical master samples,44 installed product rays and two-shell
coupon pass; case114 sections,36 bores,1188 service rays and84 recombination
sections pass. STL byte ordering changes are recorded separately from measured
case/bridge geometric equivalence. No source geometry changed during assembly
review. No staging directories or probe/contact-sheet files remain.

Plan remains current for the `[?]` physical/hardware gates and eventual immutable
publication, with the case parent plan. No commit/push authorized or performed.
Proposed commit message: `Add split 4U control cover to 6U cyberdeck`.

## Repository checkpoint authorization (2026-10-21)

- [x] User explicitly approved committing all current tracked/untracked work and pushing: "commit everything and push". This includes the verified rev_0003 artifacts, shared staging fix, journals, Cicero definition/reference and user slicer projects. Physical validation remains open; this Git checkpoint does not approve fabrication or immutable revision publication.
