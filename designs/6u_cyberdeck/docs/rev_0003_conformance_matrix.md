# rev_0003 rack-interface conformance

Config: `configs/rev_0003.json`; reference v2.0.0, bundle SHA256
`330051136930B54F0ABF91FF81EA217D0E6CAD2DBE6503375FFB219E59E0210D`.

PASS denotes the stated digital/declaration evidence, not fabrication readiness.
Every unresolved calibration, hardware, cable, load or slicer row blocks release.

## Interface cover_rail_attachment (lower-4U control cover)

| Requirement | Result | Evidence / reason |
|---|---|---|
| RACK-SCOPE-001 | PASS | M3x0.5 screws with ISO7089 washers and captive metal nuts; no countersinks; 80 mm case depth selected; dimensions in mm. |
| RACK-SCOPE-002 | PASS | M3x0.5 screws with ISO7089 washers and captive metal nuts; no countersinks; 80 mm case depth selected; dimensions in mm. |
| RACK-SCOPE-003 | PASS | M3x0.5 screws with ISO7089 washers and captive metal nuts; no countersinks; 80 mm case depth selected; dimensions in mm. |
| RACK-SCOPE-004 | PASS | M3x0.5 screws with ISO7089 washers and captive metal nuts; no countersinks; 80 mm case depth selected; dimensions in mm. |
| RACK-SCOPE-005 | PASS | M3x0.5 screws with ISO7089 washers and captive metal nuts; no countersinks; 80 mm case depth selected; dimensions in mm. |
| RACK-SCOPE-006 | PASS | M3x0.5 screws with ISO7089 washers and captive metal nuts; no countersinks; 80 mm case depth selected; dimensions in mm. |
| RACK-SCOPE-007 | PASS | M3x0.5 screws with ISO7089 washers and captive metal nuts; no countersinks; 80 mm case depth selected; dimensions in mm. |
| VOCAB-001 | PASS | 3 mm structural engagement is independent of 1 mm socket fit clearances and 0.02 mm Boolean epsilon. |
| VOCAB-002 | PASS | 3 mm structural engagement is independent of 1 mm socket fit clearances and 0.02 mm Boolean epsilon. |
| VOCAB-003 | PASS | Printed cover declared front_only, front anchored, occupied Y=-3..6.8 including bosses; complete device envelope remains unresolved. |
| VOCAB-004 | NOT_APPLICABLE | Cover is front_only; no full-depth equipment item. |
| VOCAB-005 | BLOCKED_UNKNOWN | Complete joystick/button body, connector and cable service envelopes unmeasured. |
| VOCAB-006 | PASS | Named face, joint, driver, nut-insertion and component keepouts documented in rev_0003_verification.md; component bounds explicitly unresolved. |
| RACK-GEO-001 | PASS | 4U nominal 177.8 mm; removable height177.2; four holes selected from canonical rail sequence at X=+/-118.2625, Z=-127/38.1; pitch unchanged. |
| RACK-GEO-002 | PASS | 4U nominal 177.8 mm; removable height177.2; four holes selected from canonical rail sequence at X=+/-118.2625, Z=-127/38.1; pitch unchanged. |
| RACK-GEO-003 | PASS | 4U nominal 177.8 mm; removable height177.2; four holes selected from canonical rail sequence at X=+/-118.2625, Z=-127/38.1; pitch unchanged. |
| RACK-GEO-004 | PASS | 4U nominal 177.8 mm; removable height177.2; four holes selected from canonical rail sequence at X=+/-118.2625, Z=-127/38.1; pitch unchanged. |
| RACK-GEO-005 | BLOCKED_UNKNOWN | Printed column-to-column tolerance and as-built calibration not measured; round-hole candidate is not commercial-rack fit evidence. |
| RACK-GEO-006 | BLOCKED_UNKNOWN | Complete joystick brackets and button terminal bodies unmeasured; checked 35 mm button envelopes alone do not prove full body width. |
| RACK-GEO-007 | NOT_APPLICABLE | Round holes selected; no horizontal or vertical slots. |
| RACK-GEO-008 | NOT_APPLICABLE | Round holes selected; no horizontal or vertical slots. |
| RACK-GEO-009 | NOT_APPLICABLE | Round holes selected; no horizontal or vertical slots. |
| RACK-GEO-010 | NOT_APPLICABLE | Round holes selected; no horizontal or vertical slots. |
| FAST-M3-001 | PASS | 3.6 mm nominal holes selected for independently printed cover/rail stack, with captive metal nuts; finished diameters await calibration. |
| FAST-M3-002 | PASS | 3.6 mm nominal holes selected for independently printed cover/rail stack, with captive metal nuts; finished diameters await calibration. |
| FAST-M3-003 | PASS | 3.6 mm nominal holes selected for independently printed cover/rail stack, with captive metal nuts; finished diameters await calibration. |
| FAST-M3-004 | NOT_APPLICABLE | No 3.2 mm controlled/post-machined datum holes. |
| FAST-M3-005 | BLOCKED_UNKNOWN | PLA process calibration and finished-hole measurements absent; nominal CAD diameter is not acceptance diameter. |
| FAST-M3-006 | BLOCKED_UNKNOWN | PLA process calibration and finished-hole measurements absent; nominal CAD diameter is not acceptance diameter. |
| FAST-M3-007 | PASS | Flat 3 mm face and 10 mm tongue support full 7 mm washer OD continuously; no front recess or embossed obstruction. |
| FAST-M3-008 | NOT_APPLICABLE | No mounting slots. |
| FAST-M3-009 | NOT_APPLICABLE | No cover screw-head counterbores; washer seats are flat face surfaces. |
| FAST-M3-010 | PASS | Socket-head M3 screws with flat washers, no countersinks. |
| FAST-M3-011 | PASS | M3x10 selected from seam 9.9 mm and rail 8.9 mm minimum stack; exact purchased hardware dimensions remain physical checks. |
| FAST-M3-012 | PASS | Through nut strategies, no blind inserts; seam screw tip W9.5 inside W9.8 boss. |
| FAST-M3-013 | BLOCKED_UNKNOWN | Nominal rail tips Y6.5 and seam tips Y6.5 declared; complete joystick/button wiring envelopes not measured. |
| FAST-M3-014 | PASS | 2.5 mm hex tool with declared 4 mm shaft envelope and 20 mm straight approach from negative Y; physical handle access remains a separate blocker. |
| DEPTH-001 | PASS | Inherited selected case depth80; independent front5.8/rear3 structural zones give positive ordinary interval Y5.8..77; cover uses declared front-interface exception. |
| DEPTH-002 | PASS | Inherited selected case depth80; independent front5.8/rear3 structural zones give positive ordinary interval Y5.8..77; cover uses declared front-interface exception. |
| DEPTH-003 | PASS | Inherited selected case depth80; independent front5.8/rear3 structural zones give positive ordinary interval Y5.8..77; cover uses declared front-interface exception. |
| DEPTH-004 | BLOCKED_UNKNOWN | Component connector, terminal, mating travel and cable-bend dimensions absent; no service volume silently counted as printed solid. |
| DEPTH-005 | BLOCKED_UNKNOWN | Component connector, terminal, mating travel and cable-bend dimensions absent; no service volume silently counted as printed solid. |
| DEPTH-006 | PASS | Cover class front_only; support_mode front_ears via four rail screws plus two mechanical center-seam stations. |
| DEPTH-007 | PASS | Cover class front_only; support_mode front_ears via four rail screws plus two mechanical center-seam stations. |
| DEPTH-008 | NOT_APPLICABLE | No partial, full or paired half-depth cover item. |
| DEPTH-009 | NOT_APPLICABLE | No partial, full or paired half-depth cover item. |
| DEPTH-010 | NOT_APPLICABLE | No partial, full or paired half-depth cover item. |
| DEPTH-011 | BLOCKED_UNKNOWN | Printed face/boss interval declared separately; complete controls service envelope unknown. |
| DEPTH-012 | NOT_APPLICABLE | No through-depth classified item; face holes are cuts, not equipment classifications. |
| DEPTH-013 | PASS | front_only depth class and front_ears support mode declared independently. |
| DEPTH-014 | PASS | front_only depth class and front_ears support mode declared independently. |
| DEPTH-015 | NOT_APPLICABLE | No front/rear half-depth pair. |
| DEPTH-016 | NOT_APPLICABLE | No front/rear half-depth pair. |
| DEPTH-017 | NOT_APPLICABLE | No shared cable zone declared; component wiring remains unresolved. |
| DEPTH-018 | BLOCKED_UNKNOWN | Printed cover has front removal sequence; wiring disconnect and complete control-body withdrawal await actual hardware. |
| CLR-001 | PASS | Purpose-named cover_fit_gap, socket side/tip gaps, independent Boolean epsilon and structural minima. |
| CLR-002 | PASS | Purpose-named cover_fit_gap, socket side/tip gaps, independent Boolean epsilon and structural minima. |
| CLR-003 | PASS | Purpose-named cover_fit_gap, socket side/tip gaps, independent Boolean epsilon and structural minima. |
| CLR-004 | PASS | Purpose-named cover_fit_gap, socket side/tip gaps, independent Boolean epsilon and structural minima. |
| CLR-005 | BLOCKED_UNKNOWN | Manufacturing deviation/shrinkage not measured; worst-case critical fit stack cannot yet be bounded. |
| CLR-006 | BLOCKED_UNKNOWN | Manufacturing deviation/shrinkage not measured; worst-case critical fit stack cannot yet be bounded. |
| CLR-007 | BLOCKED_UNKNOWN | Actual control wiring bend radius, connector body and mating/unmating travel absent. |
| CLR-008 | BLOCKED_UNKNOWN | Actual control wiring bend radius, connector body and mating/unmating travel absent. |
| CLR-009 | NOT_APPLICABLE | Passive faceplate has no requested fan/airflow interface; no thermal performance claimed. |
| CLR-010 | BLOCKED_UNKNOWN | Straight tool shaft approach declared; actual driver handle and physical hand access not verified. |
| CLR-011 | BLOCKED_UNKNOWN | Bare printed cover translation can clear rail plane; complete installed controls and wiring swept volume unresolved. |
| CLR-012 | PASS | Keepouts exclusive by default; no arbitrary payload may occupy the seam/fastener zones. |
| CLR-013 | NOT_APPLICABLE | No shared keepout ownership declared. |
| CLR-014 | PASS | 22 face-hole pairs, two seam bores, two nut pockets and socket entry/shoulder/end lands inventoried and asserted; measured final STL sections recorded. |
| CLR-015 | PASS | 22 face-hole pairs, two seam bores, two nut pockets and socket entry/shoulder/end lands inventoried and asserted; measured final STL sections recorded. |
| STRUCT-001 | BLOCKED_UNKNOWN | Digital root/land/overlap checks pass; slicer continuity, physical fit and PLA loaded assembly verification remain absent. |
| STRUCT-002 | PASS | 3 mm real root/face engagement; no epsilon or fit clearance counted as structural overlap. |
| STRUCT-003 | BLOCKED_UNKNOWN | Digital root/land/overlap checks pass; slicer continuity, physical fit and PLA loaded assembly verification remain absent. |
| STRUCT-004 | PASS | Host minimum3 exceeds reference2.5; smallest seam-hole side land3.2, face-hole edge land4.25 mm. |
| STRUCT-005 | PASS | All 7 mm washer seats supported continuously on front face/tongues; socket roof does not replace tongue bearing surface. |
| STRUCT-006 | BLOCKED_UNKNOWN | Digital root/land/overlap checks pass; slicer continuity, physical fit and PLA loaded assembly verification remain absent. |
| STRUCT-007 | BLOCKED_UNKNOWN | Digital root/land/overlap checks pass; slicer continuity, physical fit and PLA loaded assembly verification remain absent. |
| STRUCT-008 | PASS | Conservative face-hole pair minimum8.062 mm; seam tongue3.2 mm side land, receiver3 mm shoulders, 4 mm clamp web. |
| STRUCT-009 | NOT_APPLICABLE | No subtractive text, labels, cosmetic grooves or vents. |
| STRUCT-010 | PASS | Both cover leaves face-down; right socket roof needs bridge/support coupon and slicer verification. |

## Interface rack_front (retained 6U case rails)

The following rows are scoped only to the retained case interface, independently
from the cover rows above. Geometry measurements are rerun on rev_0003 installed
leaves; case bounds/triangle counts/volumes are compared against rev_0002.
The historical empty-case payload exclusions do not apply to the cover or controls.

| Requirement | Result | Evidence / reason |
|---|---|---|
| RACK-SCOPE-001 | PASS | M3/washer/captive-nut declaration; millimetres; selected depth; no countersinks or other thread families. |
| RACK-SCOPE-002 | PASS | M3/washer/captive-nut declaration; millimetres; selected depth; no countersinks or other thread families. |
| RACK-SCOPE-003 | PASS | M3/washer/captive-nut declaration; millimetres; selected depth; no countersinks or other thread families. |
| RACK-SCOPE-004 | PASS | M3/washer/captive-nut declaration; millimetres; selected depth; no countersinks or other thread families. |
| RACK-SCOPE-005 | PASS | M3/washer/captive-nut declaration; millimetres; selected depth; no countersinks or other thread families. |
| RACK-SCOPE-006 | PASS | M3/washer/captive-nut declaration; millimetres; selected depth; no countersinks or other thread families. |
| RACK-SCOPE-007 | PASS | M3/washer/captive-nut declaration; millimetres; selected depth; no countersinks or other thread families. |
| VOCAB-001 | PASS | Structural overlap 3 mm is separate from named socket clearances. |
| VOCAB-002 | PASS | Boolean epsilon 0.02 is computational only. |
| VOCAB-003 | PASS | Full shell class explicitly declared, not inferred from size. |
| VOCAB-004 | NOT_APPLICABLE | Empty enclosure scope: no installed equipment, half-depth pair, cables, airflow device or removable equipment module. Future integration needs independent verification. |
| VOCAB-005 | NOT_APPLICABLE | Empty enclosure scope: no installed equipment, half-depth pair, cables, airflow device or removable equipment module. Future integration needs independent verification. |
| VOCAB-006 | PASS | Named keepout inventory in rev_0003_verification.md. |
| RACK-GEO-001 | PASS | 36 installed passages on canonical 44.45 / 15.875 / 15.875 / 12.7 pattern, X=+/-118.2625. |
| RACK-GEO-002 | PASS | 36 installed passages on canonical 44.45 / 15.875 / 15.875 / 12.7 pattern, X=+/-118.2625. |
| RACK-GEO-003 | PASS | 36 installed passages on canonical 44.45 / 15.875 / 15.875 / 12.7 pattern, X=+/-118.2625. |
| RACK-GEO-004 | PASS | 36 installed passages on canonical 44.45 / 15.875 / 15.875 / 12.7 pattern, X=+/-118.2625. |
| RACK-GEO-005 | BLOCKED_UNKNOWN | Printer/material calibration and commercial-rack fit have not been measured. |
| RACK-GEO-006 | BLOCKED_UNKNOWN | Actual equipment width and service envelope are unspecified. |
| RACK-GEO-007 | NOT_APPLICABLE | No mounting slots in this candidate; round holes selected. |
| RACK-GEO-008 | NOT_APPLICABLE | No mounting slots in this candidate; round holes selected. |
| RACK-GEO-009 | NOT_APPLICABLE | No mounting slots in this candidate; round holes selected. |
| RACK-GEO-010 | NOT_APPLICABLE | No mounting slots in this candidate; round holes selected. |
| FAST-M3-001 | PASS | Clearance passages plus explicitly declared captive nuts. |
| FAST-M3-002 | BLOCKED_UNKNOWN | 3.6 mm candidate is deliberately selected for the independent-part stack; finished diameter needs calibration. |
| FAST-M3-003 | PASS | 3.6 mm nominal for alignment with independently printed equipment ears; finished hole calibration pending. |
| FAST-M3-004 | NOT_APPLICABLE | No 3.2 mm close-fit holes selected. |
| FAST-M3-005 | PASS | As-printed size explicitly unverified; coupon/calibration required. |
| FAST-M3-006 | BLOCKED_UNKNOWN | No measured printer/material profile or executed post-machining evidence. |
| FAST-M3-007 | PASS | Flat external rail and tongue bearing faces support the entire 7 mm washer annulus. |
| FAST-M3-008 | NOT_APPLICABLE | No slots. |
| FAST-M3-009 | PASS | Head recess and washer contact surface are declared separately. |
| FAST-M3-010 | PASS | No countersinks. |
| FAST-M3-011 | BLOCKED_UNKNOWN | Seam and rear-center screw stacks resolved; rack screw length still depends on unspecified device-ear thickness. |
| FAST-M3-012 | NOT_APPLICABLE | No blind threaded inserts; captive nut strategy. |
| FAST-M3-013 | BLOCKED_UNKNOWN | Seam tip contained nominally; installed equipment and hand-service checks require real hardware. |
| FAST-M3-014 | PASS | 4 x 50 mm bit sweeps declared for eight seam and four rear-center clamps; install before equipment. |
| DEPTH-001 | PASS | User-selected 80 mm exterior depth; usable depth is separately derived. |
| DEPTH-002 | PASS | 71.2 mm positive shell interval before local keepouts. |
| DEPTH-003 | PASS | Front 5.8 mm and rear 3 mm independently modeled. |
| DEPTH-004 | PASS | Equipment connector/service integration explicitly excluded from claimed clear cavity. |
| DEPTH-005 | NOT_APPLICABLE | Empty enclosure scope: no installed equipment, half-depth pair, cables, airflow device or removable equipment module. Future integration needs independent verification. |
| DEPTH-006 | NOT_APPLICABLE | Empty enclosure scope: no installed equipment, half-depth pair, cables, airflow device or removable equipment module. Future integration needs independent verification. |
| DEPTH-007 | NOT_APPLICABLE | Empty enclosure scope: no installed equipment, half-depth pair, cables, airflow device or removable equipment module. Future integration needs independent verification. |
| DEPTH-008 | NOT_APPLICABLE | Empty enclosure scope: no installed equipment, half-depth pair, cables, airflow device or removable equipment module. Future integration needs independent verification. |
| DEPTH-009 | NOT_APPLICABLE | Empty enclosure scope: no installed equipment, half-depth pair, cables, airflow device or removable equipment module. Future integration needs independent verification. |
| DEPTH-010 | NOT_APPLICABLE | Empty enclosure scope: no installed equipment, half-depth pair, cables, airflow device or removable equipment module. Future integration needs independent verification. |
| DEPTH-011 | NOT_APPLICABLE | Empty enclosure scope: no installed equipment, half-depth pair, cables, airflow device or removable equipment module. Future integration needs independent verification. |
| DEPTH-012 | NOT_APPLICABLE | Empty enclosure scope: no installed equipment, half-depth pair, cables, airflow device or removable equipment module. Future integration needs independent verification. |
| DEPTH-013 | NOT_APPLICABLE | Empty enclosure scope: no installed equipment, half-depth pair, cables, airflow device or removable equipment module. Future integration needs independent verification. |
| DEPTH-014 | NOT_APPLICABLE | Empty enclosure scope: no installed equipment, half-depth pair, cables, airflow device or removable equipment module. Future integration needs independent verification. |
| DEPTH-015 | NOT_APPLICABLE | Empty enclosure scope: no installed equipment, half-depth pair, cables, airflow device or removable equipment module. Future integration needs independent verification. |
| DEPTH-016 | NOT_APPLICABLE | Empty enclosure scope: no installed equipment, half-depth pair, cables, airflow device or removable equipment module. Future integration needs independent verification. |
| DEPTH-017 | NOT_APPLICABLE | Empty enclosure scope: no installed equipment, half-depth pair, cables, airflow device or removable equipment module. Future integration needs independent verification. |
| DEPTH-018 | NOT_APPLICABLE | Empty enclosure scope: no installed equipment, half-depth pair, cables, airflow device or removable equipment module. Future integration needs independent verification. |
| CLR-001 | PASS | Purpose-named socket side/tip/outer clearances. |
| CLR-002 | PASS | No generic clearance variable. |
| CLR-003 | PASS | Clearances distinct from boolean_epsilon. |
| CLR-004 | PASS | Structural minima are independent assertions. |
| CLR-005 | BLOCKED_UNKNOWN | Manufacturing deviations of both prints are unknown. |
| CLR-006 | BLOCKED_UNKNOWN | Worst-case fit/interference cannot be bounded without measured process deviations. |
| CLR-007 | NOT_APPLICABLE | Empty enclosure scope: no installed equipment, half-depth pair, cables, airflow device or removable equipment module. Future integration needs independent verification. |
| CLR-008 | NOT_APPLICABLE | Empty enclosure scope: no installed equipment, half-depth pair, cables, airflow device or removable equipment module. Future integration needs independent verification. |
| CLR-009 | NOT_APPLICABLE | Empty enclosure scope: no installed equipment, half-depth pair, cables, airflow device or removable equipment module. Future integration needs independent verification. |
| CLR-010 | BLOCKED_UNKNOWN | Seam access declared geometrically; physical tool body and equipment service integration await test. |
| CLR-011 | NOT_APPLICABLE | Empty enclosure scope: no installed equipment, half-depth pair, cables, airflow device or removable equipment module. Future integration needs independent verification. |
| CLR-012 | PASS | Declared keepouts are exclusive. |
| CLR-013 | NOT_APPLICABLE | No shared keepouts. |
| CLR-014 | PASS | Station and rack subtraction inventory in rev_0003_verification.md. |
| CLR-015 | PASS | Projected adjacent-cut pairs inventoried and local shoulders measured. |
| STRUCT-001 | BLOCKED_UNKNOWN | Local digital roots/sections checked; slicer paths and physical validation outstanding. |
| STRUCT-002 | PASS | No fit gap or epsilon counted toward overlap. |
| STRUCT-003 | BLOCKED_UNKNOWN | Digital margin checks recorded; complete physical material-width confirmation remains pending. |
| STRUCT-004 | PASS | Host raises minimum to 3 mm; bore/pocket edge calculations in rev_0003_verification.md. |
| STRUCT-005 | PASS | Washer surfaces have no unsupported bridges. |
| STRUCT-006 | BLOCKED_UNKNOWN | Digital root sections checked; no slicer/physical full-seam verification. |
| STRUCT-007 | BLOCKED_UNKNOWN | Nominal continuous 3 mm shell overlap; slicer continuity evidence outstanding. |
| STRUCT-008 | PASS | Socket/nut, socket/edge, rack adjacent-cut and seam margins inventoried. |
| STRUCT-009 | NOT_APPLICABLE | No cosmetic subtractive features. |
| STRUCT-010 | PASS | Rear-face-down orientation declared per leaf. |
