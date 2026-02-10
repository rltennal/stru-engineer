# Skill: Foundation and Below-Grade Design

## Purpose

This skill covers foundation design including spread footings, continuous footings, mat foundations, piles/piers, retaining walls, and below-grade structures. Foundation design interfaces directly with geotechnical engineering — the geotechnical report is a critical input document.

## Applicable Standards

- **ACI 318** — Structural concrete design for footings and foundation walls
- **IBC Chapter 18** — Soils and Foundations
- **IBC Section 1809** — Shallow Foundations
- **IBC Section 1810** — Deep Foundations
- **ASCE 7** — Load combinations (service for soil bearing, factored for concrete design)

## Geotechnical Report — Key Information

Every foundation design begins with the geotechnical report. Extract:

| Parameter | Typical Symbol | Use |
|-----------|---------------|-----|
| Allowable bearing pressure | q_allow (psf/ksf) | Footing sizing |
| Lateral earth pressure (active) | Ka * gamma * H | Retaining wall design |
| Lateral earth pressure (passive) | Kp * gamma * H | Sliding resistance |
| Coefficient of friction | mu | Sliding resistance |
| Soil unit weight | gamma (pcf) | Lateral pressure, overburden |
| Groundwater elevation | — | Hydrostatic pressure, buoyancy |
| Frost depth | — | Minimum footing depth |
| Liquefaction potential | — | Seismic design |
| Soil type / site class | — | ASCE 7 seismic parameters |
| Lateral pile/pier capacity | — | Deep foundation design |
| Vertical pile/pier capacity | — | Deep foundation design |
| Modulus of subgrade reaction | ks | Mat foundation design |

**Washington State Notes:**
- Frost depth: 12-18" in lowlands, deeper in eastern WA and mountains
- Glacial till common in Puget Sound region — generally good bearing
- Alluvial soils near rivers — potential liquefaction in seismic events
- Expansive soils less common in WA than Arizona (flag for AZ projects)

## Spread Footing Design

### Sizing (Service Loads)
1. Determine service loads (D, L, S, etc.) — unfactored
2. Calculate required area: A_req = P_service / q_allow
3. For eccentric loads: q_max = P/A + M/S ≤ q_allow (check q_min ≥ 0 for no tension)
4. For biaxial eccentricity: check kern rule — e ≤ L/6 in both directions for full bearing

### Concrete Design (Factored Loads)
1. Calculate factored soil pressure: q_u = P_u / A_footing
2. **One-way shear:** Check at d from face of column
   - Vu = q_u * B * (L/2 - c/2 - d)
   - phi*Vc = phi * 2 * sqrt(f'c) * B * d
3. **Two-way (punching) shear:** Check at d/2 from face of column
   - Vu = P_u - q_u * (c1 + d)(c2 + d)
   - phi*Vc = phi * min(4, 2 + 4/beta, 2 + alpha_s*d/bo) * sqrt(f'c) * bo * d
4. **Flexure:** Design reinforcement at face of column
   - Mu = q_u * B * (L/2 - c/2)^2 / 2
   - Select As per flexural design procedure
5. **Minimum reinforcement:** As_min = 0.0018 * B * h (Grade 60)
6. **Development length:** Verify bar development from critical section to footing edge

### Footing Rules of Thumb
- Minimum depth: 6" for residential footings per IBC (12" practical)
- Typical residential: 16-24" wide continuous, 8-10" deep
- Column footings: 12-24" deep, sized for bearing
- Projection beyond column: approximately equal in all directions (square preferred)

## Continuous (Strip) Footing Design

- Design per unit length (1-ft strip)
- Same bearing, shear, and flexure checks as spread footing
- Longitudinal reinforcement for point load variation
- Check for combined gravity + lateral overturning from shear walls above

## Retaining Wall Design

### Loading
1. **Active earth pressure:** Pa = 0.5 * Ka * gamma_s * H^2
   - Ka = (1 - sin(phi)) / (1 + sin(phi)) for Rankine
   - Or per geotechnical report (often gives equivalent fluid pressure)
2. **Surcharge:** p_s = Ka * q (uniform surcharge at surface)
3. **Hydrostatic pressure:** if no drainage behind wall (avoid this condition)
4. **Seismic earth pressure:** Mononobe-Okabe method or per ASCE 7

### Stability Checks (Service Loads)
1. **Overturning:** FS = M_resisting / M_overturning ≥ 2.0
   - M_resisting = weight of wall, soil on heel, surcharge * moment arm
   - M_overturning = Pa * H/3 + Ps * H/2
2. **Sliding:** FS = (mu * N + Pp) / Ph ≥ 1.5
   - mu = coefficient of friction (typically 0.35-0.50)
   - Pp = passive pressure on toe (often neglected or reduced by 50%)
   - Add key if FS inadequate
3. **Bearing:** q_max ≤ q_allow
   - Eccentricity from resultant: e = B/2 - (M_net / V)
   - If e ≤ B/6: q = V/B * (1 ± 6e/B)
   - If e > B/6: q_max = 2V / (3*(B/2 - e)) — partial bearing

### Stem Design
- Cantilever from base: design for lateral earth pressure
- Maximum moment at base of stem: M = Pa * H/3 + Ps * H/2
- Shear at base of stem: V = Pa + Ps
- Reinforce tension side (earth-side for cantilever retaining wall)

### Heel and Toe Design
- **Heel:** Net downward pressure (soil weight + surcharge) minus upward soil bearing
- **Toe:** Upward soil bearing pressure minus self-weight
- Design each as cantilever from face of stem

### Wall Drainage
- Always provide drainage behind retaining walls
- Specify: drainage mat or gravel, perforated pipe at base, weep holes
- If no drainage: design for full hydrostatic pressure (not recommended)

## Deep Foundations (Piles / Drilled Shafts)

### When Required
- Shallow bearing inadequate (soft soils, fill, expansive soils)
- Lateral loads require deep embedment
- Uplift resistance needed
- Liquefaction mitigation
- Scour conditions

### Design Considerations
- Vertical capacity: end bearing + skin friction (per geotech report)
- Lateral capacity: p-y analysis or geotech-provided values
- Group effects: pile spacing ≥ 3 diameters for full capacity
- Pile cap design: strut-and-tie or sectional method
- Minimum piles per column: 2 (unless single pile with ductile connection)

## Anchor Bolt Design

### Cast-in-Place Anchors (ACI 318 Chapter 17)
- Tension: steel strength, concrete breakout, pullout, side-face blowout
- Shear: steel strength, concrete breakout, concrete pryout
- Combined tension and shear: interaction equation
- Edge distances and embedment per Chapter 17

### Common Anchor Bolt Specifications
- Standard plate washers on anchor bolts
- Minimum embedment: 7 bolt diameters (rule of thumb)
- Minimum edge distance: 6 bolt diameters (or per ACI 318 Ch. 17)
- Template or setting plan required for field placement

## Frost Protection

- Washington State: minimum 12" below grade in most jurisdictions
- Eastern WA: 18-24" or deeper depending on elevation
- Arizona: typically 12" (frost not typically controlling; expansive soils may govern depth)
- Frost-protected shallow foundations: per IRC R403.3 (alternative for heated buildings)

## Common Errors to Avoid

- Using factored loads for soil bearing checks (use service loads)
- Using service loads for concrete footing design (use factored loads)
- Not checking both one-way and two-way shear in footings
- Forgetting to include soil weight on heel in retaining wall stability
- Not providing adequate drainage behind retaining walls
- Ignoring seismic lateral earth pressure in SDC D+
- Not verifying development length of dowels into footing
- Sizing footing for gravity only and not checking overturning from lateral loads
- Not coordinating footing elevation with geotechnical bearing stratum

## Deliverable Checklist

- [ ] Geotechnical data summary
- [ ] Footing sizing for bearing (service loads)
- [ ] One-way and two-way shear checks (factored loads)
- [ ] Flexural reinforcement design
- [ ] Retaining wall stability (overturning, sliding, bearing)
- [ ] Retaining wall stem, heel, toe design
- [ ] Anchor bolt design
- [ ] Foundation plan with dimensions, reinforcement, and embedment
- [ ] Drainage provisions for retaining walls
