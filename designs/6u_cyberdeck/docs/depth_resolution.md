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
  resolved for this design and no `UNKNOWN` remains unresolved for the
  published revision.
- Consequence: outer depth (Y) = 80.0 mm; per-leaf print bounds
  140.6 x 160.55 x 80 mm.
