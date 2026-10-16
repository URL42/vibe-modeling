# Parametric 3D Modeling Specification: Four-Hook VR Headset Wall Mount

## 1. Objective

Create an accurate, functional, 3D-printable reproduction of the wall-mounted VR headset and controller storage bracket shown in the reference photographs.

The final model should resemble a commercially manufactured, matte-black, one-piece bracket with four horizontally distributed, forward-projecting hooks.

**Model only the bracket.** Do not include the VR headset, controllers, cables, chargers, screws, wall anchors, packaging, or other items in the product photographs.

The bracket should be a single watertight solid, with smooth, rounded geometry and sufficient strength to support a VR headset and two controllers.

Prioritize dimensional accuracy, structural strength, ease of printing, and a close visual match to the reference.

## 2. Overall Dimensions

Manufacturer-specified dimensions:

| Dimension | Value |
|---|---|
| Total width | 275 mm |
| Maximum projection from wall | 93 mm |
| Backplate vertical height | 34 mm |

Estimated dimensions requiring reconstruction:

| Feature | Initial modeling value |
|---|---|
| Backplate thickness | 6 mm |
| Hook count | 4 |
| Hook width | 28 mm |
| Hook body vertical thickness | 10 mm |
| Hook end-lip height above arm | 18 mm |
| Hook end-lip thickness | 7–9 mm |
| Main edge fillet radius | 3 mm |
| Hook root fillet radius | 8–12 mm |
| Mounting hole count | 2 |
| Mounting hole through-diameter | 5 mm |

All estimated parameters must remain editable.

The advertised 34 mm height applies to the backplate. Position the hooks so that their tips remain approximately within the vertical extent of the backplate.

## 3. Coordinate System

Use millimeters.

Define:

- X-axis: Horizontal along the wall, left to right.
- Y-axis: Perpendicular to the wall, projecting outward.
- Z-axis: Vertical, upward.

The backplate occupies approximately:

- X = 0 to 275 mm
- Y = 0 to 6 mm
- Z = 0 to 34 mm

The flat rear mounting surface is at Y = 0.

The front face of the plate is at Y = 6.

All four hooks project forward in the positive Y direction, terminating at approximately Y = 93 mm.

The model should maintain this coordinate system so components can be generated parametrically.

## 4. Backplate Geometry

Create a long, narrow, rectangular mounting plate with rounded corners.

### Shape

The rear mounting surface must be completely flat so that the bracket seats firmly against a wall.

The front surface should have the smooth, subtly sculpted appearance of a molded or cast consumer-product bracket.

The plate should have:

- A nominal width of 275 mm.
- A nominal vertical height of 34 mm.
- A nominal thickness of 6 mm.
- Rounded perimeter corners with approximately 5 mm radius.
- Slightly rounded front-facing edges with approximately 2 mm fillets.

Avoid sharp rectangular transitions.

The front face should incorporate smooth reinforced areas around the four hook attachment points.

In the reference photographs, the geometry surrounding the hook roots forms a subtle continuous, wave-like reinforcing ridge across the backplate.

Reproduce that appearance with a series of smoothly blended raised transitions that connect the hook bases into the plate.

These reinforcements should be structural rather than merely decorative.

Do not add text, logos, textures, or ornamental features.

## 5. Hook Distribution

The bracket has exactly four cantilevered hooks, positioned in a single horizontal row.

All four hooks face in the same direction and are approximately identical.

Suggested hook center positions measured from the left edge:

| Hook | X center |
|---|---|
| Hook 1, left outer | 25 mm |
| Hook 2, left inner | 100 mm |
| Hook 3, right inner | 175 mm |
| Hook 4, right outer | 250 mm |

This gives nominal center-to-center spacing of 75 mm.

The four hooks should be parallel, symmetrically distributed, and aligned at the same vertical elevation.

The two center hooks support the head strap of a VR headset.

The two outer hooks can support the controllers by their wrist straps or compatible handles.

Do not add separate controller-shaped sockets or headset-shaped cradles. The original product achieves compatibility through four simple general-purpose hooks.

## 6. Detailed Hook Geometry

Each hook resembles a short, thick, rectangular cantilever arm with an upward-curved retention lip at its free end.

### Main arm

The main arm projects nearly horizontally outward from the front face of the backplate.

Suggested dimensions:

- Width along X: 28 mm.
- Vertical thickness along Z: approximately 10 mm.
- Overall reach from the wall: approximately 93 mm.
- Effective cantilever length beyond the backplate: approximately 87 mm.

The main horizontal support surface should be smooth and approximately level.

The top surface should be broad and gently rounded to avoid damaging fabric headset straps or controller wrist loops.

The underside should be smoothly blended into the backplate.

Use a shallow rectangular cross-section with slightly rounded edges rather than a circular rod.

The reference hooks have broad, flat support surfaces and relatively substantial rectangular profiles.

Avoid thin rods, sharp corners, narrow pegs, and delicate unsupported structures.

### Hook root

At the rear attachment point, the arm expands into a thickened structural root.

The connection should flow organically into the backplate rather than meeting it at a sharp 90-degree corner.

Use a concave structural fillet of approximately 8–12 mm radius where geometry permits.

The root should be slightly thicker than the middle and outer section of the arm.

A subtle taper is appropriate, with the arm gradually becoming thinner toward its outer end.

The transition should remain visually smooth and should not produce abrupt changes in thickness.

### Retention lip

At the front of each cantilever, create a raised vertical stop.

The lip prevents hanging equipment from sliding forward and falling off the bracket.

The lip should:

- Extend upward approximately 18 mm above the arm's upper support surface.
- Span essentially the full width of the hook.
- Have a nominal thickness of 7–9 mm in the projection direction.
- Blend smoothly into the horizontal arm.
- Have a broad, rounded upper end.
- Be approximately vertical, potentially leaning very slightly backward toward the wall.

The lip should form a shallow J-shaped or L-shaped profile when the hook is viewed from the side.

The tip should resemble a rounded, upright rectangular tab, not a ball, spike, claw, or sharply curved shepherd's hook.

The front face of the tab may be mostly flat, with rounded perimeter edges.

Use 2–4 mm fillets at the tip where possible.

### Side profile

Viewed from the side, each hook should have the following functional profile:

1. A reinforced root attached to the vertical backplate.
2. A long, approximately horizontal support arm.
3. A smooth upward bend near the free end.
4. A short, upright retention tab.

The support arm and retention tab are one continuous solid.

No articulated parts, fasteners, or inserts are used to attach the hooks.

## 7. Mounting Holes

The original bracket visibly contains two mounting holes through the long backplate.

Both holes are horizontally aligned near the vertical center of the backplate.

They are positioned between the two outer pairs of hooks.

Suggested coordinates:

- Left mounting hole: X = 55 mm, Z = 17 mm.
- Right mounting hole: X = 220 mm, Z = 17 mm.

Each mounting hole passes through the backplate along the Y-axis, perpendicular to the wall.

Suggested hole design:

- Through-hole diameter: 5 mm.
- Countersink diameter: approximately 9.5 mm.
- Countersink angle: 90 degrees.
- Fully open through the rear mounting surface.

The front opening should accept a conventional flat-head mounting screw so that the screw head sits approximately flush with the front surface.

Provide sufficient solid material around each hole.

The holes must not overlap any hook root or reinforcing fillet.

The rear mounting face must remain flat and unobstructed.

Do not model the mounting screws or anchors as part of the printed object.

## 8. Surface Treatment and Visual Appearance

The object has the appearance of a matte or satin black molded engineering component.

The design language should be:

- Minimalist.
- Functional.
- Symmetrical.
- Smoothly rounded.
- Slightly industrial.
- Substantial without appearing bulky.

The entire component should be modeled as a continuous solid with uniform dark material.

The original reference has an almost black, charcoal-gray appearance.

For visualization, use a dark gray material with low gloss and subtle specular highlights.

For printing, no surface texture is required.

Avoid decorative embossing, geometric patterns, perforations, honeycombing, exposed lattice structures, or logos.

The primary visual characteristics are the thin, elongated wall plate; the four identical forward-projecting arms; their upright retention lips; and the smoothly blended attachment roots.

## 9. Structural Design Requirements

This model is intended to be a functional 3D-printed bracket, not merely a decorative reproduction.

The four arms act as cantilevers. Their connection to the mounting plate must withstand the bending moments generated by equipment hanging near the ends of the hooks.

Therefore:

- All hook roots must have generous reinforcement.
- Avoid sharp internal corners.
- Avoid thin cross-sections near attachment points.
- Preserve continuous material through the hook-to-backplate interface.
- Maintain a solid load path from each hook into the mounting plate.
- Preserve sufficient material around mounting holes.
- Avoid hollow decorative shells unless explicitly designed and validated for strength.

Where visual fidelity conflicts with print strength, make modest structural improvements while preserving the external appearance.

The model must not depend on adhesives, glued-on hooks, or separate mechanical fasteners to attach the arms.

Use a single solid body as the default design.

Do not assume any specific rated load without engineering validation.

## 10. 3D Printing Requirements

Target FDM/FFF printing.

Recommended material: PETG, PETG-CF, or another tough engineering filament with suitable layer adhesion.

PLA may be used for an initial dimensional prototype, but avoid treating an untested PLA prototype as a permanently rated load-bearing wall fixture.

Geometry should be compatible with a 0.4 mm nozzle.

Prefer:

- At least 3 mm of continuous structural material in critical areas, preferably more.
- Rounded overhang transitions.
- Generous fillets.
- No unnecessarily thin features.
- Watertight, manifold mesh geometry.
- No intersecting or disconnected solids.
- No zero-thickness surfaces.

The rear mounting surface must remain planar.

The mounting holes must be printable, unobstructed, and accurately dimensioned.

Consider the expected FDM layer orientation when evaluating the strength of the cantilever roots. If the bracket is printed with the rear plate against the build surface, the hooks extend upward during printing, but the resulting layer interfaces may become a structural weakness under bending loads.

Prefer a mechanically favorable print orientation or adjust the design and reinforcement accordingly.

Do not claim the part is safe for a particular load without testing.

## 11. Optional Split-Print Configuration

The primary output must be a one-piece, 275 mm-wide bracket.

A printer with a sufficiently large build volume is required for the one-piece configuration.

As an optional secondary configuration, provide a version divided into two approximately equal sections for smaller printers.

If a split model is generated:

- The split occurs between the two center hooks.
- Each half contains two hooks.
- The halves must interlock with a mechanically meaningful alignment joint.
- Do not rely on a simple glued butt joint for structural support.
- Add adequate independent wall fastening to each section.
- Preserve the appearance of the original continuous bracket when assembled.

The split configuration must not replace the primary one-piece model.

## 12. Modeling Workflow

Construct the component using an editable parametric workflow.

Suggested sequence:

1. Create the rectangular 275 × 34 × 6 mm backplate.
2. Round the backplate's perimeter corners.
3. Define the four hook centerlines.
4. Construct one cantilever arm with a rounded rectangular section.
5. Add its raised front retention lip.
6. Blend the lip and arm into a single continuous form.
7. Add the reinforced hook root.
8. Replicate the hook at the remaining three positions.
9. Union all four hooks with the backplate.
10. Add smooth reinforcing transitions along the front face.
11. Subtract the two countersunk mounting holes.
12. Apply cosmetic edge fillets.
13. Check the overall bounding dimensions.
14. Validate the resulting solid for 3D printing.

Where supported, use parameter-driven features rather than manually sculpted geometry.

## 13. Deliverables

Generate:

1. An editable parametric CAD model with named dimensions.
2. A single watertight 3D printable solid.
3. An STL export in millimeters.
4. A STEP export, if supported.
5. A dimensioned isometric preview.
6. Front, top, side, and rear orthographic previews.

If possible, identify which dimensions were taken from the photographs and which were estimated.

Do not silently substitute estimated dimensions for manufacturer-specified dimensions.

## 14. Geometric Validation

Before finalizing, verify:

- Overall bracket width = 275 mm.
- Backplate height = 34 mm.
- Maximum wall-to-tip projection ≈ 93 mm.
- Exactly four hooks are present.
- All four hooks are parallel and forward-facing.
- All hooks have upward-facing retention lips.
- The bracket has two usable wall-mounting holes.
- The back surface is flat.
- The object is a single connected solid.
- The exported mesh is watertight.
- No headset, controller, cable, or fastener geometry is included.

The finished part should be immediately recognizable as the simple four-hook VR headset wall mount in the supplied reference photographs.

The visual objective is high fidelity to the reference object; the functional objective is a robust, printable storage bracket rather than a purely cosmetic 3D model.