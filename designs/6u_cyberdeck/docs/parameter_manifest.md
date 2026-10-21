> Historical rev_0001 record. The current shared source and manifest target rev_0003;
> this record does not approve or reproduce the corrected geometry. See [rev_0003 verification](rev_0003_verification.md).

# 6u_cyberdeck — Resolved Parameter Manifest (rev_0001)

Governing plan:
`plans/current/2026-10-04-11-35-16_create-6u-cyberdeck.md`

## Source Provenance

- Rack spec: `ten-inch-rack-m3-printed-design-spec` **v2.0.0**
  (`references/engineering/ten_inch_rack/v2.0.0/`).
- Bundle manifest SHA-256:
  `330051136930B54F0ABF91FF81EA217D0E6CAD2DBE6503375FFB219E59E0210D`
  (`references/engineering/ten_inch_rack/v2.0.0/bundle_manifest.json`).
- Reference validator: `python scripts/validate_ten_inch_rack_reference.py`
  — **PASS** (source hashes 4, document identity, 80 requirement IDs,
  20 companion constants, `rack_internal_depth` flagged as required project
  input) — run 2026-10-04.
- Station reference:
  `references/engineering/fasteners/m3_captive_nut_registration_seam_stations.md`
  (starting profile only; physically unverified).

## Resolved Parameters

| Quantity | Value | Basis |
|---|---|---|
| U pitch | 44.45 mm | spec v2.0.0 `u_pitch` (NORMATIVE_EXTERNAL) |
| Clear opening (X) | 222.25 mm | spec `rack_clear_opening_nominal` |
| Clear opening (Z) | 266.7 mm | 6 x 44.45 |
| Face width (X) | 254.0 mm | spec `rack_front_width_nominal` |
| Depth (Y) | 80.0 mm | user mandate — see depth resolution record |
| Top/bottom band and station radial envelope | 13.6 mm | Original dimensional allowance; actual clamp stack is head recess 3.8 + tongue 3.0 + bearing wall 4.0 + nut pocket 2.8. Socket tip clearance 1.0 is along insertion. |
| Side front rail band | 15.875 mm | (254.0 - 222.25) / 2; independent of station radial depth |
| Outer envelope | 254.0 x 80.0 x 293.9 mm | 266.7 + 2 x 13.6 (Z); face width; user depth |
| `minimum_wall_thickness` | 3.0 mm | host baseline |
| `minimum_structural_overlap` | 3.0 mm | host baseline (>= wall) |
| `minimum_internal_edge_width` | 3.0 mm | host baseline |
| `boolean_epsilon` | 0.02 mm | spec baseline |
| Fastener | M3x0.5 only | spec v2.0.0 |
| Washer (ISO 7089) | ID 3.2 / OD 7.0 / t 0.5 | spec v2.0.0 (required for primary mounts) |
| Finished hole dia | 3.2 close / 3.4 default / 3.6 stackup | spec v2.0.0 |
| Washer seat dia | 8.25 (range 8.0-8.5) | spec v2.0.0 |
| Countersunk primary heads | PROHIBITED | spec v2.0.0 |

### M3 Station Starting Profile (unverified; coupon gate G7 before freeze)

| Quantity | Starting value |
|---|---|
| `m3_clearance_diameter` | 3.6 mm |
| `head_recess_diameter` | 8.25 mm |
| `head_recess_depth` | 3.8 mm |
| `nut_across_flats` | 5.9 mm |
| `nut_pocket_circumscribed_diameter` | 5.9 / cos(30 deg) ~= 6.82 mm |
| `nut_pocket_depth` | 2.8 mm |
| `tongue_insertion_depth` | 14.0 mm |
| `tongue_root_structural_overlap` | >= 3.0 mm |
| `receiver_closed_end_thickness` | >= 3.0 mm |
| `socket_side_clearance` | 1.0 mm |
| `socket_tip_clearance` | 1.0 mm |
| `minimum_wall_thickness` | 3.0 mm |
| `minimum_structural_overlap` | 3.0 mm |
| `minimum_internal_edge_width` | 3.0 mm |

Fit clearance, structural engagement, and boolean epsilon are kept distinct
quantities per the station reference.

2026-10-18 candidate clarification: each tongue reaches 14 mm beyond its seam,
so conservative leaf print bounds are 141 x 160.95 x 80 mm, not the original
140.6 x 160.55 estimate based on the radial band. The dimensions still fit the
220 mm target with the originally required total free margin of at least 55 mm
per axis. The installed meshes provide the authoritative actual bounds.

The original starting profile is not a production tolerance freeze. See
`verification.md` and `geometry_measurements.json` for the implemented dimensions,
pending physical measurements, and exact candidate artifact evidence.
