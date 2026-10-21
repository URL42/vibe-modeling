> Historical rev_0001 record. The current shared source and manifest target rev_0003;
> this record does not approve or reproduce the corrected geometry. See [rev_0003 verification](rev_0003_verification.md).

# rack_internal_depth — UNKNOWN Resolution Record

- Spec: `ten-inch-rack-m3-printed-design-spec` v2.0.0
  (`references/engineering/ten_inch_rack/v2.0.0/`) declares
  `rack_internal_depth` = **null / UNKNOWN** and the reference validator
  confirms it "remains a required project input" (PASS, 2026-10-04).
- Resolution: **`rack_internal_depth` = 80.0 mm**, set by explicit user
  mandate ("6u ten-inch rack, 80mm deep") recorded verbatim in the governing
  plan `plans/current/2026-10-04-11-35-16_create-6u-cyberdeck.md`.
- Status: **resolved as user-mandated input** for rev_0001. This is a project
  input, not a spec conformance value; the spec's UNKNOWN is therefore
  resolved for this design. Other process, calibration and equipment-integration
  unknowns remain; this record alone does not authorize publication.
- Consequence: outer depth (Y) = 80.0 mm; per-leaf print bounds
  conservatively 141 x 160.95 x 80 mm after the 2026-10-18 tongue-reach check.
  Exterior depth is not usable cavity depth: the front ring occupies 5.8 mm and
  the rear skin 3 mm, leaving the shell interval Y=5.8..77 (71.2 mm) before
  hardware, joint and equipment/service keepouts.
