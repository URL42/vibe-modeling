# Raspberry Pi 4 vs. Raspberry Pi 5: Mechanical Dimensions, Mounting Patterns, and Clearances

The Raspberry Pi 4 Model B and Raspberry Pi 5 use the same PCB footprint and four-hole mounting pattern. This makes it possible to design a common mounting plate, bracket, or standoff system for both boards.

However, their component placement, connector geometry, and cooling requirements differ. A shared mounting system is straightforward; a fully enclosed, close-fitting case requires additional accommodation.

The following combines Raspberry Pi's official mechanical drawings with practical engineering recommendations for CAD modeling, 3D printing, and enclosure fabrication.

## 1. Core mechanical specifications

| Parameter | Raspberry Pi 4B | Raspberry Pi 5 |
| --- | --- | --- |
| PCB length | 85.0 mm | 85.0 mm |
| PCB width | 56.0 mm | 56.0 mm |
| Nominal PCB thickness | ~1.6 mm | ~1.6 mm |
| Mounting holes | 4 | 4 |
| Nominal mounting bore | 2.7 mm | 2.7 mm |
| Recommended screw | M2.5 | M2.5 |
| Hole pitch, X | 58.0 mm | 58.0 mm |
| Hole pitch, Y | 49.0 mm | 49.0 mm |
| Hole-center inset, left | 3.5 mm | 3.5 mm |
| Hole-center inset, top/bottom | 3.5 mm | 3.5 mm |
| Hole-center distance from right edge | 23.5 mm | 23.5 mm |
| PCB corner radius | 3.0 mm (specified) | Check CAD model |
| 40-pin GPIO header | Same physical footprint | Same physical footprint |
| Ethernet / USB port end | Similar footprint | Similar footprint |
| Cooling layout | Pi 4-specific | Pi 5-specific |

Nominal dimensions in millimeters. PCB thickness is a design assumption rather than a controlled tolerance from the two mechanical drawings.

Official references: Raspberry Pi official mechanical drawings for the [Raspberry Pi 4 Model B](https://pip.raspberrypi.com/documentation/hardware/raspberrypi4/CM4_datasheet.pdf) and the [Raspberry Pi 5](https://datasheets.raspberrypi.com/rpi5/raspberry-pi-5-mechanical-drawing.pdf) (pip-assets.raspberrypi.com). Raspberry Pi also provides a documentation page with DXF and STEP resources. The Pi 5 STEP model is especially useful for confirming three-dimensional collisions between connectors, coolers, and enclosure walls.

## 2. Exact mounting-hole coordinates

Use the following coordinate system for either board:

- Origin `(0, 0)` at the upper-left PCB corner, viewed from above, with the GPIO header along the top.
- X increases to the right, toward Ethernet/USB.
- Y increases downward, toward the HDMI/power connector edge.
- All measurements refer to the centerline of each mounting hole.

| Hole | X (mm) | Y (mm) |
| --- | --- | --- |
| A — upper left | 3.5 | 3.5 |
| B — upper right | 61.5 | 3.5 |
| C — lower left | 3.5 | 52.5 |
| D — lower right | 61.5 | 52.5 |

The hole-pattern rectangle is therefore 58 × 49 mm, but it is not centered on the 85 × 56 mm PCB.

This distinction is important: there is considerably more PCB extending to the right of the mounting holes, where the Ethernet and USB connectors are located.

For a CAD sketch, the four hole-center coordinates above are sufficient to create the common mounting pattern.

## 4. Mounting hardware and mechanical clearances

Both models are designed around M2.5 mounting hardware.

| Component | Recommended size |
| --- | --- |
| Fastener thread | M2.5 × 0.45 |
| PCB hole nominal diameter | 2.7 mm |
| Clearance hole in a mounting bracket | 2.8–3.0 mm |
| Printed plastic pilot for threaded M2.5 screw | Depends on material and screw |
| Typical standoff diameter | 5–6 mm |
| Standoff height beneath PCB | 5–6 mm |
| Typical screw-head diameter | 4.5–5.0 mm |
| Recommended fastening points | All four |

These are practical fabrication recommendations, not all official Raspberry Pi dimensions.

### Critical consideration: screw-head and boss clearance

The mounting holes lie only 3.5 mm from the nearest top, bottom, or left edge.

For example, a 5 mm diameter screw head has a radius of 2.5 mm, leaving approximately 1 mm of geometric clearance to the PCB edge when centered.

A 6 mm diameter standoff similarly leaves only 0.5 mm.

For a 3D printed mounting structure, use 5 mm diameter bosses with brass M2.5 inserts or nuts, provided the underside component layout allows them.

Avoid large washers or oversized standoffs that could contact solder joints, surface-mounted components, or nearby connector hardware.

## 5. Vertical clearances

There are three separate height requirements: underside clearance, clearance above the bare PCB, and additional clearance for cooling.

### Recommended enclosure heights

| Clearance | Pi 4B | Pi 5 |
| --- | --- | --- |
| Beneath PCB, minimal | 3 mm | 3 mm |
| Beneath PCB, preferred | 5–6 mm | 5–6 mm |
| Above PCB, bare board only | 18–20 mm | 18–20 mm |
| Above PCB with low-profile cooling | 22–30 mm | 22–30 mm |
| Above PCB with substantial active cooling | 30–45+ mm | 30–45+ mm |

Engineering allowances, not exact device dimensions. Cooler height must be measured from the selected heatsink/fan assembly.

### Raspberry Pi 4: Component heights

The official Pi 4 drawing gives several useful Z-height values.

| Component | Nominal Z-height above PCB |
| --- | --- |
| Ethernet jack | 13.5 mm |
| Stacked USB connectors | 16.0 mm |
| 40-pin GPIO header | 8.5 mm |
| SoC package | 2.4 mm |
| USB-C power connector | 3.2 mm |
| Micro-HDMI connectors | 3.0 mm |
| 3.5 mm A/V jack | 6.0 mm |
| Camera/display ribbon connectors | 5.5 mm |

The tallest standard connectors are the stacked USB ports at approximately 16 mm above the PCB.

Consequently, an enclosure ceiling approximately 20 mm above the PCB is adequate as a starting point for the bare Pi 4, although it may not leave much room for cooling.

### Raspberry Pi 5: Cooling and additional interfaces

The Pi 5 introduces several mechanical differences that matter when designing a common enclosure:

- A dedicated fan connector.
- A PCIe FPC connector, potentially requiring space for a cable and M.2 adapter.
- Two compact camera/display ribbon connectors with different placement from the Pi 4.
- A power button.
- A different layout around the SoC and power-management components.

The official mechanical drawing also identifies the positions of the principal edge connectors and the secondary board features.

The Pi 5 typically benefits from active cooling, especially under sustained CPU workloads. This means the cooling assembly, rather than the bare PCB, will often determine the minimum enclosure height.

## 6. Edge clearances and connector accessibility

A reliable enclosure design needs to account for the physical connector body as well as the cables plugged into it.

| Area | Suggested free space | Purpose |
| --- | --- | --- |
| PCB long edges without ports | 2–3 mm | Manufacturing and assembly tolerance |
| Connector end of PCB | 3–5 mm before cutouts | Prevent interference with housings |
| USB-A / Ethernet exit | 25–40 mm | Typical straight cable/plug clearance |
| USB-C power exit | 15–25 mm | Depends on cable and plug |
| Micro-HDMI exit | 20–35 mm | Depends on connector |
| FPC ribbon connector | Depends on cable | Avoid tight folds or kinks |
| Fan intake | 5–10+ mm | Reduce inlet obstruction |

These spaces describe a practical layout envelope, not minimum manufacturer-mandated distances.

For a very compact enclosure, right-angle power and HDMI connectors can substantially reduce cable-exit clearance. For modular or serviceable enclosures, allow more space.

## 7. Designing a universal Pi 4 / Pi 5 mounting plate

If the goal is a common mounting solution, the best strategy is to make only the shared features dimensionally fixed: the PCB outline, mounting holes, and PCB elevation.

### Suggested universal mounting geometry

| Feature | Value |
| --- | --- |
| Plate footprint | 95 × 66 mm (5 mm nominal margin around the PCB) |
| Mounting pitch | 58 × 49 mm (compatible with both boards) |
| Standoff height | 6 mm above plate surface |
| Boss diameter | 5 mm (verify underside clearance) |

For this proposed 95 × 66 mm plate, with the 85 × 56 mm board centered, the coordinates become:

| Mounting hole | X (mm) | Y (mm) |
| --- | --- | --- |
| Upper left | 8.5 | 8.5 |
| Upper right | 66.5 | 8.5 |
| Lower left | 8.5 | 57.5 |
| Lower right | 66.5 | 57.5 |

These are plate-relative coordinates, not PCB-relative coordinates.

### Example OpenSCAD parameters

```openscad
// Raspberry Pi 4B / Raspberry Pi 5
// Universal mounting plate

pcb_x = 85;
pcb_y = 56;

hole_d = 2.7;
hole_pitch_x = 58;
hole_pitch_y = 49;

hole_inset_x = 3.5;
hole_inset_y = 3.5;

plate_margin = 5;
plate_x = pcb_x + 2 * plate_margin;
plate_y = pcb_y + 2 * plate_margin;

plate_thickness = 3;
standoff_height = 6;
standoff_diameter = 5;

mounting_holes = [
    [3.5, 3.5],
    [61.5, 3.5],
    [3.5, 52.5],
    [61.5, 52.5]
];

// Plate-relative hole coordinates
for (p = mounting_holes) {
    echo([
        p[0] + plate_margin,
        p[1] + plate_margin
    ]);
}
```

## 8. Important caveats for fabrication

A few factors become particularly significant with close-fitting printed enclosures:

1. Dimensional tolerances: Raspberry Pi explicitly warns that its mechanical drawings are approximate reference drawings, not production manufacturing data. Design clearance rather than relying on perfectly exact dimensions.
2. PCB hole diameter vs. other holes: The Pi 5 drawing includes a separate 3 mm diameter callout for a feature that is not one of the four principal mounting holes. Do not mistake every circular feature for an attachment point.
3. Cooling and airflow: Mounting several Raspberry Pis close together requires attention to airflow direction, exhaust recirculation, and vertical spacing.
4. HAT compatibility: A standard HAT may share the mounting pattern but require taller standoffs and additional clearance for the GPIO connector.
5. Cable routing: The mounting plate can be universal, but connector cutouts and cable-routing geometries should be specific to each board.

**Bottom line:** For both the Raspberry Pi 4 Model B and Raspberry Pi 5, use an 85 × 56 mm PCB envelope and four 2.7 mm mounting holes centered at `(3.5, 3.5)`, `(61.5, 3.5)`, `(3.5, 52.5)`, and `(61.5, 52.5)` mm. A 6 mm standoff and a 5 mm diameter mounting boss are reasonable starting choices.

That gives you one reusable mounting pattern for either generation while keeping the enclosure, cooling, and cable-routing details independently configurable.
