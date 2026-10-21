# cicero_datacenter

A new, mostly hollow, full-size Cicero bust containing Jetson computers and,
eventually, multiple phone-based AI servers. Rear openings provide peripheral
connections, ventilation and service access. Explore a mouth speaker and
microphones at both ears while preserving the recognizable sculpture.

This is a **definition and reference-import checkpoint**. No hollow shell,
device negatives, mounts or printable parts have been generated or approved.
The existing `cicero_joined` design remains independent and unchanged.

## Canonical documents

- [PLAN.md](PLAN.md): detailed requirements, internal architecture, void-aware
  joinery strategy, implementation phases, unknowns and acceptance gates.
- [negatives.json](negatives.json): **canonical negative/keepout inventory**.
  Stable IDs identify everything that must be dimensioned and modeled. A null
  dimension means unknown, never zero clearance. Add future devices here first.
- [source_manifest.json](source_manifest.json): full-size asset identity, actual
  imported bounds, scale, inherited landmarks and hashes of reviewed references.
- [LICENSE.md](LICENSE.md): inherited CC BY-NC-SA notice and attribution limitations.

## Imported full-size model

[assets/cicero_full_size_reference.stl](assets/cicero_full_size_reference.stl)
is a byte-for-byte copy of the uncut scaled master, not the joined-part assembly.
It contains 508,792 triangles; its imported bounds are approximately
**437.54 x 342.234 x 568.999 mm**. Ear-tip target: **228.6 mm (nine inches)**.
Preserve this outer scale; do not shrink the bust to fit the hardware or printer.
This solid reference is not a printable enclosure or a validated shell.

Printer envelope remains **220 x 220 x 220 mm**. Select broad real flat bed faces
before optimizing in-plane rotation. Keep any brim/support allowances explicit.

## Initial negative families

| Family | Canonical IDs | Starting intent |
| --- | --- | --- |
| Hollow interior | `interior_core` | Mostly empty interior; preserve shell, joint lands and supported mounts |
| Jetson AGX Xavier | `agx_xavier`, `agx_mount_interface`, `agx_rear_io`, `agx_cooling` | Adapt the Gigachad cavity/shaft reference after actual hardware measurements |
| Jetson Orin Nano Super | `orin_nano_super_tray`, `orin_tray_docking`, `orin_rear_io`, `orin_ventilation` | Accommodate the user's existing simple slot-load tray, rear ports and cooling |
| Phone AI servers | `phone_server_slot`, `phone_cooler`, `phone_cabling` | Repeatable serviceable phone bays with cooler, camera-bump and cable space |
| Shared infrastructure | `shared_airflow`, `rear_service_ports`, `power_network_hub`, `cable_trunk`, `rear_service_access` | Rear connectors, service doors, cable bends and cooling paths |
| Audio | `mouth_speaker`, `ear_microphone_left`, `ear_microphone_right`, `audio_electronics` | Speaker behind mouth; microphone and isolated acoustic path at each ear |
| Growth | `future_expansion` | Additional devices/empty reserve; final capacity remains unknown |

All actual new device dimensions, part numbers, positions and phone count remain
to be established. The user's Orin tray/port arrangement is a design input, not
a verified claim about every carrier-board variant. Audio is a requested
feasibility objective; components and acoustic performance are not selected.

## What the historical references actually establish

The [Gigachad cutter](../gigachad_xavier_void/src/parts/gigachad_xavier_void.scad)
uses a **110 x 220 x 110 mm** main prism plus an **80 x 205 x 100 mm** upper
shaft. Its nominal 80 mm fan example uses 71.5 mm hole pitch, 4.4 mm cutter pins
and a 3 mm fan plate. These are **legacy cutter parameters**, not verified AGX
dimensions or a proven mounting/thermal solution. A relief in that cutter leaves
positive fan-plate stock; indiscriminate subtraction would destroy that stock.

The [RCA phone tower](../old_rca_building/README.md) provides phone-support rails,
airflow gaps, a cable-bend opening and a fan/plenum pattern. Legacy defaults use
a 163.6 x 78.1 x 8.9 mm phone envelope, a nominal 40 mm fan and an 18 x 88 mm
slot cross-section. Do not adopt its old 2 mm wall or phone dimensions as verified
new enclosure requirements. The reviewed implementation is fan-driven airflow;
specific clip-on/thermoelectric phone coolers still need identification.

## Joinery direction

Retain integral dovetails, closed gravity seats, broad planar print bases and
separate continuous head/bust neck owners from
[cicero_joined](../cicero_joined/README.md). Replace its solid-volume rail/root
assumptions with **perimeter seam lands and locally supported joint stations**.
Keep a continuous central electronics/cable/air passage through the neck if
feasible. First test one localized head-to-bust connection on that perimeter;
do not put a solid plate across the entire interior or blindly subtract a void
through the current neck rail. Multiple perimeter joints require a documented
architecture decision and compatible motion, not silent many-to-many ownership.

Provisional minima for future geometry: shell wall and shortest internal material
width **3 mm**, structural overlap **6 mm**; increase locally as loads demand.
These are targets, not verified measurements. Empty-space fraction, final neck
opening, seam positions, part count and device capacity require layout evidence.
The existing seventeen leaves and thirty-three joint locations are a baseline
to reconsider, not a committed decomposition for the hollow design.

## Lifecycle and verification

The [future implementation plan](../../plans/future/2026-10-18-22-35-10_cicero-datacenter-implementation.md)
is proposed, not authorization to perform all later phases. This checkpoint only
imports and documents. There is no `parts.json`, `assembly.json`, executable SCAD
or output directory yet; adding dummy printable declarations would misrepresent
the current state. Establish those contracts when the first modeled blockout has
real printable owners, before its complete build and assembly review.

Structural joins: **unverified**. Minimum internal material width: **unverified**.
No headset-holder requirement is automatically inherited by this separate product;
whether it should also hold the VR headset is an open optional requirement.
