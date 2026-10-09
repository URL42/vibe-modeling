# Raspberry Pi 5 case (120 mm cube)

A two-piece, 3D-printed enclosure for a single Raspberry Pi 5 (pattern-compatible
with the Raspberry Pi 4 Model B), sized to a 120 × 120 × 120 mm outer envelope.
The case is a base with walls plus a separate lid, joined by M3 screws. The back
of the case is fully open. The top face of the lid carries a raised camera
emblem with a centered arcade-button through-hole.

## Background

The dimensional basis for this design is
[`docs/raspberry-pi-mounting.md`](../../docs/raspberry-pi-mounting.md), which
consolidates Raspberry Pi's official Pi 4B / Pi 5 mechanical drawings with
practical fabrication recommendations:

- Both boards share the same 85.0 × 56.0 mm PCB footprint.
- Four 2.7 mm mounting holes on a 58 × 49 mm pitch, inset 3.5 mm from the
  top, bottom, and left PCB edges (hole centers at `(3.5, 3.5)`,
  `(61.5, 3.5)`, `(3.5, 52.5)`, `(61.5, 52.5)` mm PCB-relative). The pattern is
  **not centered** on the PCB — the Ethernet/USB connector end extends further.
- M2.5 hardware is the official fastener class; 5 mm diameter bosses with
  brass M2.5 inserts are the recommended printed fastener solution (screw-head
  clearance to the PCB edge is tight: ~1 mm for a 5 mm head at 3.5 mm inset).
- Tallest bare-Pi 5 connectors sit ~16–17 mm above the PCB (USB stack); the Pi 5
  additionally expects a fan assembly above the SoC.
- The Pi 5 drawing includes a separate 3 mm feature callout that is **not** a
  mounting hole — only the four 2.7 mm holes are attachment points.

The arcade-button hole dimensions are inherited from the cyberdeck design
(`designs/cyberdeck/src/lib/defaults.scad`):

- `chamber_arcade_button_mount_d` = **Ø28 mm** through-hole (the button mount bore).
- `chamber_arcade_button_outer_d` = Ø35 mm button outer envelope (cap clearance
  reference, not cut in this design).

## Design decisions

| # | Decision | Rationale |
| --- | --- | --- |
| 1 | Outer envelope exactly 120 × 120 × 120 mm | User-specified cube size; comfortably fits the 85 × 56 mm PCB with room for ports and a lid. |
| 2 | Two printable parts: `base` + `lid` | User-specified. The base is the floor plus the front, left, and right walls up to the parting line; the lid is the top slab. |
| 3 | Lid fastened to the base with M3 screws | User-specified. Four M3 screw stations at the four corners of the parting line: Ø3.4 mm clearance bores in the lid rim, Ø3 mm pilot bores in the base rim bosses (screws drive into printed bosses; brass inserts optional later). Screw head seats are counterbored in the lid outer face so the heads sit flush. |
| 4 | Back of the case fully open, no rim at the back | User-approved (2026-10-08). The lid/base parting line runs across the front, left, and right walls only; the back is an open 120 mm tall band between the left and right walls. This gives full rear access for the Pi's HDMI/power edge and service. |
| 5 | Pi 5 mounted near one end wall with ~5 mm clearance | User-specified. The PCB is placed against the left end wall (5 mm gap to the wall, centered vertically), leaving the right end wall as the port wall and the open back. |
| 6 | Pi mounting holes through the base floor, no standoffs | The 85 × 56 mm PCB at ~1.6 mm thickness plus M2.5 insert bosses in the 3 mm floor keeps the SoC low, maximizing headroom under the lid for the Pi 5 fan/SoC stack. Four 2.7 mm holes through the 3 mm floor; brass M2.5 inserts assumed (not modeled as geometry). |
| 7 | Port wall (right end wall) cutouts | Vertical through-cutouts for the Pi 5 edge connectors: 1× RJ45 Ethernet, 2× USB-A, 1× USB-C (power), 2× micro-HDMI. Cutout dimensions are approximate envelope boxes based on connector body sizes — functional cable-through fit is unverified and flagged for physical check. |
| 8 | Lid: raised camera emblem, ~50 × 40 mm plate, ~3 mm proud of the lid surface | User-approved size choice (2026-10-08): compact emblem rather than a full-face plate. Rounded-rectangle body plate with a central lens ring (lens circle + raised lens bezel) and a small viewfinder block in the upper corner. The emblem reads as a camera diagram raised from the lid surface. |
| 9 | Arcade button hole centered inside the camera lens | User-specified. One Ø28 mm through-hole (cyberdeck `chamber_arcade_button_mount_d`) centered on the lens center, passing through both the raised emblem and the lid slab below. No counterbore for a button cap (user-approved: straight through only). The emblem lens geometry is sized so the Ø28 mm hole sits visually inside the lens ring. |
| 10 | Wall and floor thickness 3 mm | `minimum_wall_thickness` = `minimum_structural_overlap` = `minimum_internal_edge_width` = 3 mm, asserted in source (AGENTS.md §10). |
| 11 | Parting line at 3/4 height, not at the top | With a fully open back, the lid is a top slab that wraps the front/left/right walls only; the parting line sits where the lid rim begins. The lid rim extends 10 mm above the rim line over each wall (the visible lid band), and the base walls rise to the parting line. (Exact split height to be confirmed during blockout; default target: lid band ≈ 10 mm above the wall tops.) |
| 12 | No fans or internal components modeled | This design is a case: empty interior, PCB mounting, port access. No hardware proxies in the parts manifest. |
| 13 | Multi-part design under full manifest governance | `parts.json` (base, lid), `assembly.json` (product assembly = the two parts + the parting-line M3 interface), complete `scad_build_all.py` build + `--audit-only` pass + artifact-bound assembly review are all mandatory before the design is considered complete. |

### Coordinate convention

- `x`: left (Pi mount side) → right (port wall side), `x = 0..120`.
- `y`: front → back, `y = 0..120`.
- `z`: bottom (`z = 0`) → top (`z = 120`).
- The PCB plane is horizontal at `z = 3 mm` (top of the 3 mm floor); the PCB
  occupies `x = 5..90` (5 mm clearance to the left wall, centered on the
  85 mm length), `y = 32..88` (centered in the 56 mm depth), with the
  GPIO header facing the open back.
- M3 lid screw stations: four corners inset 10 mm from the outer faces at the
  parting line.
- Lid emblem center: `(60, 60)`, raised plate 50 × 40 mm, lens center at the
  same point, Ø28 mm button hole through it.

## Structural governance (AGENTS.md §10)

- `minimum_wall_thickness` = 3 mm (all walls, floor, lid slab).
- `minimum_structural_overlap` = 3 mm: lid rim bosses and base rim bosses are
  distinct parts joined by M3 screws (intentionally separated parts — the screw
  interface is the connection; no boolean contact between them).
- `minimum_internal_edge_width` = 3 mm: all port-wall ligaments around
  cutouts are asserted ≥ 3 mm in source; any sub-3 mm feature must be a
  documented, asserted exception in the design README.
- The arcade button hole, PCB holes, and M3 bores are all asserted to retain
  ≥ 3 mm material to every open edge or to other bores.
- A successful render or manifold STL does **not** count as verification; the
  structural-joins and artifact-governance playbooks apply at the review gate.

## Roadmap checklist (execution)

State: pending as of 2026-10-08.

- [ ] 1. Scaffolding
  - [ ] 1.1 Create plan (from `templates/task_execution_plan.md`), promote to `plans/current/` before edits
  - [ ] 1.2 Create `designs/raspberrypi5_case/{src/main.scad, src/lib/defaults.scad, src/parts/base.scad, src/parts/lid.scad, src/parts/assembly_review.scad}`
  - [ ] 1.3 `defaults.scad` with all dimensions as `is_undef`-fallback parameters (envelope, wall/floor thickness, PCB placement, port cutout set, emblem geometry, M3 stations, structural minima)
  - [ ] 1.4 `main.scad` part_id dispatch: 1 → base, 2 → lid, 90 → assembly review scene
  - [ ] 1.5 `configs/rev_0001.json`
- [ ] 2. Base part
  - [ ] 2.1 Floor slab 120 × 120 × 3 mm with four 2.7 mm PCB mounting holes at the 58 × 49 mm pattern (PCB-relative centers `(3.5, 3.5)`, `(61.5, 3.5)`, `(3.5, 52.5)`, `(61.5, 52.5)`, PCB at `x = 5..90`, `y = 32..88`)
  - [ ] 2.2 Front/left/right walls to the parting line; back fully open
  - [ ] 2.3 Port-wall cutouts: RJ45, 2× USB-A, USB-C, 2× micro-HDMI (envelope boxes, ligaments asserted ≥ 3 mm)
  - [ ] 2.4 M3 boss stations at the four rim corners (Ø3.0 pilot bores)
  - [ ] 2.5 Build-time `assert()` block: minima, ligaments, hole-edge margins
- [ ] 3. Lid part
  - [ ] 3.1 Top slab 120 × 120 × 3 mm plus front/left/right rim band to the parting line; back open
  - [ ] 3.2 Raised camera emblem: ~50 × 40 × 3 mm rounded-rect plate centered at `(60, 60)`, lens ring + bezel, viewfinder block
  - [ ] 3.3 Ø28 mm arcade-button through-hole at the lens center, through emblem + slab
  - [ ] 3.4 M3 clearance bores (Ø3.4) at the four rim corners with flush head counterbores in the outer face
  - [ ] 3.5 Build-time `assert()` block: emblem margins, button-hole ligaments, bore margins
- [ ] 4. Manifest and assembly governance
  - [ ] 4.1 `parts.json` (part 1 base, part 2 lid)
  - [ ] 4.2 `assembly.json` (product assembly, M3 lid-base interface, front + isometric views)
  - [ ] 4.3 `assembly_review.scad` scene (part_id 90)
  - [ ] 4.4 Pass `scripts/validate_cad_assembly_contract.py`
- [ ] 5. Build and verify
  - [ ] 5.1 `scad_build.py --dry-run` for `rev_0001.json`
  - [ ] 5.2 Complete build: `scad_build_all.py --design raspberrypi5_case --config designs/raspberrypi5_case/configs/rev_0001.json`
  - [ ] 5.3 `scad_build_all.py --audit-only` pass on `output/raspberrypi5_case/`
  - [ ] 5.4 Review installed STL + PNG artifacts
  - [ ] 5.5 Artifact-bound assembly review manifest
  - [ ] 5.6 Structural review per playbook: joins, ligaments, connectivity, no unexpected shells
- [ ] 6. Documentation
  - [ ] 6.1 Finish this README with the executed geometry, verification record, and provenance hashes
  - [ ] 6.2 Root `README.md`: add design to the list
  - [ ] 6.3 `docs/raspberry-pi-mounting.md`: add backlink to this design
  - [ ] 6.4 Journal checkpoint for the work date
- [ ] 7. Git
  - [ ] 7.1 Status review, task-scoped commit message, commit on approval
  - [ ] 7.2 Push (artifacts included) on approval

## Open items / unverified

- Port cutout exact dimensions are envelope estimates; physical cable/plug fit is unverified until a real connector is tested.
- M3 screws drive into printed plastic bosses — brass inserts in the lid/base rim are a future improvement, not included.
- Pi 5 fan/cooling stack height above the SoC is not modeled; headroom under the lid is generous but unverified against a specific cooler part number.
- Print orientation, supports, and target printer build volume: 120 mm cube fits common 220–256 mm build volumes; orientation/support review pending.
