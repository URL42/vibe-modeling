---
plan_id: 2026-10-18-22-35-10_cicero-datacenter-implementation
title: Implement the hollow Cicero datacenter
summary: Build measured device negatives, pack hardware, hollow the scan and develop void-aware integral joints with thermal and acoustic access.
status: future
created_at: 2026-10-18-22-35-10
---

# Implement the hollow Cicero datacenter

Key: `[ ]` pending task, `[x]` completed task, `[?]` needs validation, `[-]` closed task

Status: proposed future work, not approved for execution by the definition task.
Canonical engineering plan: [design PLAN.md](../../designs/cicero_datacenter/PLAN.md).
Canonical device-negative IDs: [negatives.json](../../designs/cicero_datacenter/negatives.json).
Imported scan/scale/license: [design README](../../designs/cicero_datacenter/README.md).

- [ ] 1. Establish measured dimensional contracts.
  - [ ] 1.1 Identify AGX Xavier assembly and measure body, cooler, mounts and plugs.
  - [ ] 1.2 Measure the actual Orin Nano Super assembly and existing slot-load tray;
    establish slide axis, rear port mapping, ventilation and retention.
  - [ ] 1.3 Select initial phone/case/cooler profiles without promising a capacity;
    record insertion, charging, camera and airflow envelopes.
  - [ ] 1.4 Identify candidate speaker, left/right microphones and supporting audio
    electronics; record acoustic ports and mounting/service envelopes.
  - [ ] 1.5 Record material/profile/fit targets and power, thermal and mass budgets.
- [ ] 2. Create reusable negative/reference families, starting with AGX Xavier.
  - [ ] 2.1 Parameterize AGX body, mounts, rear I/O and cooling separately; audit
    cutter polarity and positive fan-plate/root stock inherited conceptually.
  - [ ] 2.2 Parameterize the Orin tray fit, docking, ports and ventilation.
  - [ ] 2.3 Parameterize repeatable phone/cooler/cable families and instance IDs.
  - [ ] 2.4 Parameterize audio and shared cable/air/rear-service/expansion families.
  - [ ] 2.5 Produce and measure production-derived fit/interface coupons for risky
    families; retain unknown families as pending, never zero-sized placeholders.
- [ ] 3. Review an internal packing blockout before committing enclosure cuts.
  - [ ] 3.1 Place hardware and full entry/removal/plug/tool sweeps in full-size scan.
  - [ ] 3.2 Map rear services, continuous cooling paths, power/network and cables.
  - [ ] 3.3 Reserve mouth/ear acoustic paths and useful future expansion space.
  - [ ] 3.4 Establish supported hardware load paths, base stability and candidate
    phone capacity with explicit clearance and thermal qualifications.
- [ ] 4. Develop mostly hollow shell and protected structural stock.
  - [ ] 4.1 Audit/regularize scan shells and evaluate a robust interior method.
  - [ ] 4.2 Define shell, supported frame/ribs, mounting stations and protected
    perimeter seam/neck stock; preserve facial detail and eye backing.
  - [ ] 4.3 Measure shortest post-cut thickness, void-pair ligaments, connectivity,
    cavity usability and expansion/airflow volume; reject unsupported islands.
- [ ] 5. Approve canonical print decomposition and void-aware joint architecture.
  - [ ] 5.1 Keep one continuous open-center neck owner per side; test one localized
    reinforced major dovetail before proposing multiple perimeter stations.
  - [ ] 5.2 Reposition integral joints outside hardware, air, cable and audio
    envelopes; verify rail/socket/stop roots and complete supported load paths.
  - [ ] 5.3 Reconsider old cuts/leaf count, preserve broad flat bed contact, and
    prove each final part including joints fits the 220 mm printer cube.
  - [ ] 5.4 Prove installation/removal graph and full subassembly swept clearances
    with hardware/cables present; resolve accessible anti-lift/service retention.
  - [ ] 5.5 Declare actual printable identities and logical head/bust/hardware
    ownership in parts.json/assembly.json; review artifact count changes.
- [ ] 6. Build and review exact governed artifacts.
  - [ ] 6.1 Complete normal manifest build/install/audit at output/cicero_datacenter.
  - [ ] 6.2 Inspect installed individual STLs/PNGs, topology, fit and support needs.
  - [ ] 6.3 Generate artifact-bound complete and separate exploded head/bust views,
    shell/joint sections and hardware-exposed assembly review; audit input hashes.
- [ ] 7. Validate physical operation and publish only verified claims.
  - [ ] 7.1 Test fit, loaded roots/stops, retention and safe assembly/removal on
    production-derived coupons and partial prints in the intended orientation.
  - [ ] 7.2 Measure running-device temperatures, airflow and service access.
  - [ ] 7.3 Test mouth speaker, ear pickup, fan noise, vibration and audio feedback.
  - [ ] 7.4 Check whole-product stability and revise affected geometry/evidence.
  - [ ] 7.5 Publish an immutable verified revision, update docs/journal and seek
    explicit commit/push authorization for that completed checkpoint.

Expected future files: design negative library/source, dimension/config records,
hardware references, coupons, parts/assembly contracts, generated current/revision
artifacts, provenance and review records, canonical inventory updates and journal.
Exact part/config/export names and counts require approved decomposition.

Dependencies: actual device/tray/cooler/audio dimensions, desired initial phone
count, material/profile, load/thermal budgets and access preferences. Shared
build-automation changes are outside this plan unless separately justified.

Acceptance gates: see PLAN.md sections 5-9. Targets are 3 mm minimum wall/internal
material and 6 mm root overlap, increased where necessary. Every void must preserve
required stock; every print must fit on a real flat bed face; every installed
artifact must have matching source/config/import provenance. Digital fit is not
physical, structural, thermal or acoustic approval.
