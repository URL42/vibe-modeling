# solarpunk_intelligence_breakout

Canonical source of truth for this design and the solarpunk series:
[`docs/solarpunk_series.md`](../../docs/solarpunk_series.md)

*Status: `rev_0001` built (2026-09-25); 1 STL + 17 PNG installed in
`output/solarpunk_intelligence_breakout/`, verified against hand-calculated
volume (95,958 mm³) and bounds (169 × 194 × 3 mm).*

## 1. Role

The intelligence breakout panel is a **blank companion backplane** for the
solarpunk intelligence hub. It shares the same plate envelope and hanging
interface as the main hub (169 × 194 × 3 mm, mirrored 20 × 5 mm hanging
slots), but carries no component mounting holes, raised outlines, labels, or
standoff collars. It provides open real estate for components that don't fit
on the main board layout.

## 2. Geometry

- **Plate:** 169 × 194 × 3 mm flat rectangular block. Origin at the
  bottom-left corner.
- **Hanging slots:** 8 × 20 × 5 mm rectangular through-slots, 4 per band,
  mirrored top and bottom (identical to `solarpunk_intelligence_hub`):
  - slot centers at x = 20, 63, 106, 149 mm (edges 10 mm from plate sides);
  - top band centered at y = 188.5 (3 mm gap to top edge);
  - bottom band centered at y = 5.5 (3 mm gap to bottom edge).
- **Zip-tie hole grid:** 8 × 9 = 72 Ø5 mm through-holes on a 20 mm
  center-to-center grid:
  - columns at x = 14.5, 34.5, 54.5, 74.5, 94.5, 114.5, 134.5, 154.5 (12 mm edge clearance to plate sides, symmetric);
  - rows at y = 17, 37, 57, 77, 97, 117, 137, 157, 177 (14.5 mm edge clearance, symmetric);
  - 6.5 mm separating material strip from the nearest slot band (governing internal-edge width).
  - intended for zip ties attaching components that don't fit the hub layout.
- **No** component mounting holes, outline rings, text labels, or standoff
  collars (the Ø5 grid is for zip ties, not threaded hardware).

## 3. Structural Minimums

| Parameter | Value |
|---|---|
| `minimum_wall_thickness` | 3.0 mm |
| `minimum_structural_overlap` | 3.0 mm (not applicable — no joins) |
| `minimum_internal_edge_width` | 6.5 mm (Ø5 hole edge to nearest slot edge, in y — the only separating strip because the hole overlaps the slot in x; 15 mm hole-to-hole ligament; 12/14.5 mm hole-to-plate-edge; 10 mm slot-to-plate-edge; 23 mm slot-to-slot) |

## 4. Relationship to Intelligence Hub

The breakout panel is intentionally a subset of the intelligence hub geometry:
same envelope, same hanging bands, no cutouts or markings beyond the slots.
This means it can be hung on the same rack hardware and sits flush with the
main hub when mounted adjacent.
