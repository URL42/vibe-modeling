# Cicero datacenter: detailed design and implementation plan

Status: requirements and proposed engineering sequence, 2026-10-18.
This document defines the design; the host
[future execution plan](../../plans/future/2026-10-18-22-35-10_cicero-datacenter-implementation.md)
governs later implementation approvals and checklists. The device inventory lives
only in [negatives.json](negatives.json). This is a new product, not a new revision
of `cicero_joined`.

## 1. Product requirements and scope

1. Retain the full-size scan and 228.6 mm ear-tip target. Preserve front facial
   features, ears, hair, drapery and overall silhouette as far as functional
   openings allow. Put ordinary peripheral access at the back, not through eyes
   or front facial detail. Exact rear-opening locations are not yet fixed.
2. Make the head and bust almost completely hollow, retaining only a defensible
   shell, necessary seam lands, supported mounts, local reinforcement, audio
   chambers and cable/air guides. Measure usable empty volume after these are
   included. Do not invent a hollow-percentage target before evaluating the scan.
3. Initially accommodate an AGX Xavier assembly based on the Gigachad reference
   and the user's Jetson Orin Nano Super in its existing simple slot-load tray.
   The Orin tray needs ventilation and rear-facing port access. Device variants,
   assembly dimensions and connector locations are still unknown.
4. Reserve an extensible architecture for several phones as AI servers. Phone
   models/count, cases, coolers and simultaneous heat/power loads are future inputs.
   Include them in layout studies now; do not promise a capacity before packing.
5. Provide rear device I/O, cable routing, power/network distribution space,
   accessible service paths and an intentional intake/exhaust topology.
6. Investigate a speaker coupled to the mouth and a microphone at each ear. Keep
   these spaces in the first layout, even if final electronics arrive later.
7. Print every fabrication leaf in a 220 mm cube on a broad actual flat cut face.
   No elevated sloping base held above a tiny contact by a large support scaffold.
   Local sculpted overhangs still need slicer-specific review.
8. Keep head and bust neck owners separate and continuous, enabling removal and
   service of logical subassemblies. Preserve integral male/female joints and
   downhill closed seats; no loose keys. Do not assume gravity prevents lift-off.
9. Allow later devices without redefining already accepted IDs. New additions
   update inventory, layout, dependencies, thermal budget, joinery and verification.

Authorized now: source/license import, reference review, registry and plan.
Not implemented now: shell offsets, actual negative tools, hardware choice,
placement, printable split geometry, electronics integration or thermal testing.

## 2. Source and engineering baseline

Use the byte-preserved scaled scan in `assets/`, not the joined assembly STL.
The latter includes fabrication interfaces that should not be hollowed blindly.
`source_manifest.json` records imported bounds/triangles, scale and source hashes.
The raw scan has inherited overlapping shells and has not passed a shell-offset
or structural audit. Evaluate source-shell union, surface quality, folds,
nonmanifold features and errors before constructing an interior surface.

Review the exact pinned local files recorded by the manifest:

- Gigachad `configs/rev_0001.json`, defaults and cutter modules: rectangular
  cavity, upper cooling shaft, fan-plate relief and fastener-hole pins. Its local
  depth extends toward -Y; Cicero's back is generally +Y. Define an explicit
  transform; never reuse its coordinates as if they already aligned with Cicero.
  Its historical `output/gigachad_xavier_void/mesh.scad` used a 2 mm voxel-remeshed
  head for difficult Booleans. Treat that as historical troubleshooting, not
  permission to coarsen Cicero's face/ears or reuse the old scene placement.
- RCA `rev_0002`, defaults and geometry: separated phone surfaces, supporting
  cage, cable-bend window, charging exit and rear fan/plenum. Reuse principles,
  not its external tower shape, wall thickness or asserted device capacity.
- `cicero_joined`: deeper face protecting the eye recesses, six-mm neck-owner
  reservation, oblique neck plane, face-up printing, integral pocket-loaded
  dovetails, closed stops, seam inventory and sampled assembly verification.
  Existing fit/strength/continuous-sweep limitations remain limitations.

Legacy dimensions in the registry are evidence for the old design only. Measure
actual kits/trays and consult exact manufacturer mechanical drawings during the
dimensioning phase. Record manufacturer/source revision, units, datum, tolerance,
measurement method, date and confidence. Conflicting drawings/physical dimensions
must be resolved explicitly before final cavities.

## 3. Canonical negative and keepout contract

Each registry family must eventually distinguish the following layers:

| Layer | Meaning | Boolean treatment |
| --- | --- | --- |
| Hardware reference | Physical assembled body, tray, heat sink, fan, feet, plugs, camera bump | Reference/proxy only |
| Fit cutter | Body envelope plus separately named manufacturing clearance | Subtract where a fitted cavity is intended |
| Interface cuts | Screw clearance, nut/head recesses, port openings, vent passages | Subtract only from their named owners |
| Installation/service envelope | Full insertion, withdrawal, connector bending and tool sweeps | Collision constraint; subtract only when access geometry requires it |
| Air/acoustic keepout | Intake, exhaust, speaker chamber or microphone duct | Reserve or model an intentional passage, not an indiscriminate exterior hole |
| Protected stock | Rails, bosses, lips, stops, seam lands, positive fan plate and load paths | Preserve/add with verified root attachment; never union into a cutter |

For every family record stable ID, device/variant, source, quantity, local datum,
orientation, dimensions, uncertainty, clearances, port face, mounting pattern,
cooling zones, connector/tool envelopes, retention, service direction, compatible
neighboring zones and required stock. Unknown values remain null/pending. An
undersized or zero-placeholder cutter must not pass as a completed negative.

Mounts need physical support, not just holes in a void. Draw the retained boss,
rail or plate and its supported path back to the shell/frame separately. Verify
material after all competing cavities and cable/vent cuts. Separate numerical
Boolean epsilon from fit clearance and structural overlap.

## 4. Device-specific work packages

### AGX Xavier

- Confirm the actual assembly: module/carrier, enclosure, heat sink/fan, feet and
  cabling. The old 110 x 220 x 110 cutter is not a measured board outline.
- Make individual body-fit, mounting, I/O/plug-bend, cooling and insertion tools.
  Include power/data leads, any antennas and removable media where applicable;
  the actual inventory determines which interfaces exist.
- Evaluate reuse of the upper shaft and nominal 80 mm fan concept. Record flow
  direction, fan body, screw/head/tool volumes and retained mounting plate. Recheck
  fan and rail ligament widths rather than inheriting the old geometry as safe.

### Orin Nano Super and slot-load tray

- Measure the user's tray with the installed board, heat sink/fan and any storage.
  Reserve the existing tray before proposing a replacement carrier mechanism.
- Define a slide axis, full entry opening, swept insertion/removal envelope,
  guide/support stock, end stop and accessible retention. Rear insertion is a
  candidate, not a frozen direction until clearance is demonstrated.
- Treat the user-described rear port face as the system-layout requirement;
  map the exact physical connectors and plugs on the selected carrier/tray.
- Keep intake/exhaust and any underside ventilation unobstructed by rails,
  neighboring phones, the neck joint or the rear panel. Show clearances in sections.

### Phone server bays and coolers

- Define a repeatable bay instance with independent position and device/case
  profile. Preserve camera bumps, buttons, charging plugs and cable-bend space.
- Carry forward RCA airflow stand-offs and accessible support principles. The
  old phone envelope and 18 x 88 slot are historical starting references only.
- Model cooler body, clamps, contact region, fan intake/exhaust, power lead and
  installation travel separately. The historical design proves only a forced-air
  pattern; do not assume it specifies a particular clip-on/Peltier cooler.
- Select phone count after showing hardware packing, total power, heat rejection
  and service access. Test replacing one phone without dismantling unrelated bays.
- Preserve room for future phones; do not fill every volume with fixed bosses.

### Shared rear services and future devices

- Start with a rear service-zone map, then actual individual port apertures,
  removable covers, connector strain relief and hand/tool clearances.
- Reserve optional hub/switch, power distribution, adapters and wiring as an
  unresolved infrastructure family; do not silently choose products or dimensions.
- Keep cable trunks out of slides, fan rotors, microphone paths and hot exhaust.
  Define cable disconnect access across the removable neck boundary, slack and
  strain relief; no cable may be trapped by a dovetail during head removal.
- Establish device masses and a base-to-neck load path. Heavy hardware should
  be supported by a deliberate internal frame/perimeter ribs, not facial skin.

## 5. Mostly hollow shell strategy

1. Establish outer-reference integrity and freeze protected facial regions.
2. Compare robust interior construction methods: local inset/offset of a cleaned
   union, or controlled interior envelopes where a global offset fails. Uniform
   scaling is not proof of uniform wall thickness on this asymmetric scan.
3. Set provisional `minimum_wall_thickness = 3 mm`,
   `minimum_internal_edge_width = 3 mm`, `minimum_structural_overlap = 6 mm`.
   These are planning targets, not a verified shell; raise them at loaded stations.
4. Design the nominal cavity while explicitly masking protected stock. Prefer
   short local load paths/perimeter reinforcement rather than a central solid core.
5. Measure shortest shell thickness around eyes, ears, lips, neck, folds and every
   opening. Preserve backing behind both eyes after all cuts. Reject thin islands,
   trapped slivers and unintended exterior breakthroughs.
6. Record gross cavity volume, usable hardware volume, reserved airflow/cables,
   structural stock and remaining expansion volume separately. Volume alone does
   not establish whether a device can actually enter or be serviced.
7. Check hardware weight, center of gravity and tipping in assembled and partially
   serviced states. A mostly hollow bust changes the original load assumptions.

## 6. Void-aware joinery and fabrication strategy

The existing solid model's 33 joints cannot simply survive a large interior
subtraction. Its neck male and rail roots depend on solid stock. Start with its
geometry/process rules but regenerate ownership, joint stations and load paths.

1. Build a **protected-stock map** before subtracting hardware cavities. Include
   shell-edge seam lands, dovetail roots, socket walls, closed stops, mounting
   stations and their supporting connections. Map all nearby pairs of voids.
2. Reserve a continuous **perimeter neck collar on one head owner and one bust
   owner**, with an open center for electronics, cooling and cabling if feasible.
   These are continuous rings/arches, not solid plates capping the cavity.
3. First test one localized integral gravity-seated head-to-bust dovetail on a
   reinforced perimeter station. Evaluate bearing lands, torsion, shell ovalizing,
   bending, lift-off and the complete head/neck load path. One continuous owner
   per side remains a requirement, not proof one small rail is strong enough.
4. If one station cannot support the loads without consuming required space,
   present measured failure and alternatives. Multiple compatible perimeter
   stations on the same two owners need explicit architecture review; never split
   the neck into a many-to-many set or add loose keys silently.
5. Relocate internal head/bust joints to usable perimeter lands outside device,
   airflow, cable and acoustic envelopes. Local ribs must connect to verified
   supports; every spanning rail needs two supports or a verified cantilever case.
   Avoid deep flanges or cross-cavity beams that defeat the hollow-volume goal.
6. Preserve downhill installation and closed low stops, with provisionally
   female-down/male-up ownership where compatible. Broad print faces and
   installation access take precedence over that ownership preference.
7. Reconsider the seventeen-leaf partition after shell and hardware blockout.
   Thin shell edges may lose broad first-layer contact. Use flat perimeter lands
   and design-supported seam flanges; do not substitute an arbitrarily tilted
   shell or a support scaffold beneath a large elevated base.
8. Check the existing deeper face/collar band and compound contact against the
   mouth speaker cavity. Keep eye backing and face integrity; reroute adjacent
   joint stations instead of letting audio cuts sever the collar or rail roots.
9. Rebuild an actual seam-contact inventory. Every fabrication mating pair needs
   integral capture/alignment and a valid access path; a service panel may require
   a separately reviewed retention mechanism. Enumerate fasteners if selected.
10. Verify the entire assembly sequence with hardware, plugged cables, frame and
    covers present. Check full loading and sliding sweeps, final seating, reverse
    removal and hand/tool access. A connector-only motion test is insufficient.
11. Design independent anti-lift/service retention as needed. Require reachable
    removal and coupons; gravity seats are not automatically secure in handling.

Acceptance: no cutter removes required root/stop stock, shortest post-cut material
meets minima, all intended load paths remain connected, interiors stay usable,
and every final print including joints fits its declared bed/support allowances.

## 7. Mouth speaker and ear microphones

Treat the speaker and two microphones as separate replaceable assemblies. Exact
transducers, amplifier, codec/interface, supply and cable routing are unknown.

- Speaker: reserve behind-mouth body, mounting rim/fasteners, wiring and a sealed
  or deliberately vented acoustic chamber as required by the eventual driver.
  Explore a small discreet mouth aperture/duct that preserves the lips. A driver
  somewhere in the hollow head does not demonstrate sound emerges at the mouth.
- Ears: reserve left and right capsules/boards and short controlled acoustic
  passages to the corresponding ear surface. Show actual port direction, grilles,
  mounting isolation and wiring. Do not cut large holes through thin ear rims.
- Separate microphone passages and speaker pressure from fan ducts/large open
  cavities. Use mounting/gasket/damping stock where supported by the chosen
  components. Verify any speaker baffle is attached and does not bridge the
  hardware opening accidentally.
- Validate speech intelligibility, microphone pickup, left/right operation,
  fan/flow/vibration noise and speaker feedback in running conditions. Echo
  cancellation may need electronics/software; no geometric plan guarantees it.

## 8. Implementation phases and review gates

| Phase | Work | Evidence required to advance |
| --- | --- | --- |
| 0: definition (this checkpoint) | Licensed full-size reference, legacy review, inventory, plan | Source/copy hashes, explicit unknowns and no fabricated hardware claims |
| 1: dimension contracts | Measure AGX, Orin/tray, proposed phone/cooler and audio candidates | Dimensioned local frames; physical vs fitting vs service/air envelopes |
| 2: reusable negative library | Parameterize AGX first, then Orin/tray, then repeatable phone/cooler and audio families | Isolated cutter/proxy views, polarity and units audit, production-derived fit coupons |
| 3: packing blockout | Lay out devices, rear services, airflow, power and future expansion | Noncolliding assembled and insertion envelopes; phone capacity still conditional |
| 4: hollow shell and frame | Construct/measure shell, supports, neck aperture and protected stock | Thickness sections, connectivity, usable-volume and support/load-path records |
| 5: split/joint architecture | Reposition cuts, integral seam stations and neck connection | Canonical product/subassembly/printable-leaf ownership; assembly/removal graph |
| 6: governed digital review | Complete manifest build/install/audit, installed artifacts, then full assembly review | Exact artifacts and hashes; exposed interiors, all-angle exploded head/bust, sectional joints |
| 7: physical validation | Coupons, local shell prints, device insertion, running thermal/audio tests | Measured fit, temperatures/noise, strength, retention, stability and service results |
| 8: revision/publication | Resolve findings, freeze config, publish immutable artifact set | Release audits and explicit commit/push authorization |

No specific phone count or component placement is fixed by the order above.
Dimensions need not all arrive at once: implement independent registry families
without pretending unknown families are completed. Every newly added device
invalidates affected packing, airflow, load, assembly and artifact evidence.

## 9. Required artifacts during implementation

- Parametric negative library and hardware-reference exports, with explicit
  classification; cutters must never appear as printable positive parts.
- Config/versioned dimensional evidence, fit clearances, measurement and source
  citations, including actual plug/cable bend dimensions and service envelopes.
- Future `parts.json` and `assembly.json` declaring logical head, bust, devices,
  supports and printable leaves. Final names/counts await approved decomposition.
- Complete outputs only at `output/cicero_datacenter/`; numbered immutable
  snapshots only at `revisions/cicero_datacenter/rev_000N/`. Stage/probe sources
  remain governed and must not remain in completed flat output.
- Normal manifest pipeline before artifact-bound assembly review; installed STLs
  and PNGs, source/config/input/asset hashes, review manifests and findings records.
- Full, separate exploded head/bust views from multiple angles, shell-thickness
  sections, local neck/joint sections, hardware-exposed views and airflow/access
  overlays. Protect original scanned/reference assets and inherited license.

## 10. Missing inputs and decisions

These are recorded blockers for later affected geometry, not a request to stop
the current planning/import work:

- Exact AGX Xavier kit/enclosure/cooler and mounting/I/O measurements.
- Orin carrier/tray model, assembled dimensions, slide direction and rear plugs.
- Initial phone models, cases, count, cooling devices and replacement access.
- Power/network infrastructure, expected masses, heat loads and intended runtime.
- Speaker driver, microphone boards/interface, audio targets and grille preferences.
- Material, nozzle, brim/support margins and coupon-derived fit tolerances.
- Rear-door strategy, preferred maintenance access, anti-lift retention and neck
  cable disconnects. Whether VR-headset support is also required is optional/TBD.
- Acceptable visible mouth/ear alterations, rear openings and fan noise.
- Minimum useful expansion reserve and whether hardware can occupy neck space.

Current status: structural joins **unverified**, minimum material width
**unverified**, thermal/acoustic performance **unverified**, printable artifacts
**not created**. This plan does not declare the enclosure fabrication-ready.
