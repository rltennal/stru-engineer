# Skill: Gravity Load Path Design

## Purpose

This skill covers the design of the gravity load-resisting system — the complete path from applied load at the roof or floor level down through the structure to the foundation. Every structural element in the gravity system must be designed for strength and serviceability.

## Load Path Sequence

```
Applied Loads (D, L, S, Lr)
        ↓
Decking / Sheathing / Slab
        ↓
Joists / Beams / Girders (bending, shear, deflection)
        ↓
Columns / Posts / Studs (axial, combined if eccentric)
        ↓
Headers / Transfer Beams (where load path shifts)
        ↓
Bearing Walls / Columns to Foundation
        ↓
Foundation Walls / Footings / Piers
        ↓
Soil (bearing pressure ≤ allowable)
```

## Tributary Area Method

- **One-way systems:** Tributary width = half the span to adjacent supports on each side
- **Two-way systems:** Tributary area based on 45-degree lines from corners
- **Continuous members:** Use tributary width; analyze as continuous for moment/shear
- **Cantilevers:** Full tributary width applies; no reduction in tributary area

## Beam / Joist Design

### Design Procedure
1. Determine tributary width and calculate distributed load (w = q * tributary width)
2. Calculate reactions, shear, and moment (simple span, continuous, cantilever as appropriate)
3. Select trial member size
4. Check bending: Mu ≤ φMn (LRFD) or M ≤ Mn/Ω (ASD)
5. Check shear: Vu ≤ φVn (LRFD) or V ≤ Vn/Ω (ASD)
6. Check deflection at service loads:
   - L/360 for floors (live load)
   - L/240 for floors (total load)
   - L/240 for roofs (live load)
   - L/180 for roofs (total load)
   - Per IBC Table 1604.3 (verify project-specific requirements)
7. Check bearing at supports
8. Check web crippling/yielding at concentrated loads (steel)
9. Check lateral bracing requirements

### Rules of Thumb (for preliminary sizing)
- **Wood joists:** Span (inches) / 2 = depth (inches) approximately
- **Steel beams:** Span (feet) / 2 = depth (inches) approximately for floor loads
- **Steel beams:** Span (feet) × 1.0 to 1.5 = weight (plf) for typical floor loads
- **Concrete beams:** Span / 18 to Span / 12 = depth for continuous beams
- **Glulam:** Span / 15 to Span / 20 = depth

## Column Design

### Design Procedure
1. Calculate cumulative axial load from all supported levels
2. Determine effective length (KL) based on end conditions
3. Calculate slenderness ratio (KL/r for steel, Le/d for wood)
4. Check axial capacity considering buckling
5. For combined axial + bending (eccentric loads), use interaction equations
6. Check base plate bearing (steel columns)
7. Design anchor bolts

### Rules of Thumb
- **Wood posts:** 4x4 for single story, 6x6 for two stories, verify by calculation
- **Steel columns:** W-shape preferred for biaxial loading, HSS for concentric loads
- **Concrete columns:** Minimum dimension 10" (practical), reinforcement 1-4% of Ag typical

## Floor System Selection

| System | Typical Span Range | Applications |
|--------|-------------------|--------------|
| Wood I-joists | 12-30 ft | Residential, light commercial |
| Dimensional lumber | 8-20 ft | Residential |
| Open-web wood trusses | 20-40 ft | Residential, commercial |
| Steel bar joists | 20-60 ft | Commercial, industrial |
| W-shape beams | 20-40 ft | Commercial |
| Composite steel/concrete | 25-45 ft | Commercial, multi-story |
| PT concrete slab | 25-40 ft | Commercial, multi-story |
| Concrete slab + beam | 20-35 ft | Commercial |
| Precast plank | 20-40 ft | Commercial, parking |

## Special Considerations

### Load Path Discontinuities
- Transfer beams/girders where columns don't stack
- Cantilevered conditions creating uplift at back span
- Openings in diaphragms requiring trimmer framing
- Point loads from above on floor/roof framing below

### Deflection Compatibility
- Long-term deflection (creep) in wood — multiply immediate deflection by 1.5 to 2.0
- Deflection compatibility between adjacent elements of different stiffness
- Ponding on flat roofs — check per AISC Appendix 2 or IBC Section 1611

### Serviceability
- Floor vibration — particularly for long-span steel or wood systems
- Check natural frequency > 8-10 Hz for typical floors
- Excessive deflection causing distress in finishes, partitions, or cladding

## Deliverable Checklist

- [ ] Load takedown spreadsheet showing accumulation at each level
- [ ] Tributary area diagrams
- [ ] Member design calculations with code references
- [ ] Deflection checks at service loads
- [ ] Bearing checks at all supports
- [ ] Connection forces documented for connection design
- [ ] Member schedule / summary table
