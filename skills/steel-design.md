# Skill: Structural Steel Design

## Purpose

This skill covers structural steel design per AISC 360 (Specification for Structural Steel Buildings) and AISC 341 (Seismic Provisions). Both LRFD and ASD methods are addressed, with LRFD preferred for new design.

## Applicable Standards

- **AISC 360** — Specification for Structural Steel Buildings
- **AISC 341** — Seismic Provisions for Structural Steel Buildings
- **AISC 358** — Prequalified Connections for Special and Intermediate Steel Moment Frames
- **AISC Steel Construction Manual** (15th Edition or current)
- **AWS D1.1** — Structural Welding Code — Steel
- **RCSC** — Specification for Structural Joints Using High-Strength Bolts

## Material Properties

### Common Structural Steels
| Designation | Fy (ksi) | Fu (ksi) | Common Use |
|-------------|----------|----------|------------|
| A36 | 36 | 58 | Plates, angles, channels |
| A572 Gr. 50 | 50 | 65 | W-shapes, HSS, plates |
| A992 | 50 | 65 | W-shapes (preferred) |
| A500 Gr. B | 46 (rect) / 42 (round) | 58 | HSS |
| A500 Gr. C | 50 (rect) / 46 (round) | 62 | HSS |
| A325 | — | 120 | Bolts (3/4" to 1-1/2") |
| A490 | — | 150 | Bolts (high-strength) |

### Weld Metal
- E70XX electrodes (Fu = 70 ksi) — standard for structural steel
- E80XX for higher-strength steels

## Beam Design

### Flexure (AISC 360 Chapter F)
- Mn depends on compactness and lateral bracing:
  - **Compact, Lb ≤ Lp:** Mn = Mp = Fy * Zx (full plastic moment)
  - **Compact, Lp < Lb ≤ Lr:** Mn = Mp - (Mp - 0.7*Fy*Sx)(Lb - Lp)/(Lr - Lp) (LTB inelastic)
  - **Lb > Lr:** Mn = Fcr * Sx (LTB elastic)
- LRFD: phi_b = 0.90; ASD: Omega_b = 1.67

### Shear (AISC 360 Chapter G)
- Vn = 0.6 * Fy * Aw * Cv1 (for unstiffened webs)
- Most W-shapes with h/tw ≤ 2.24*sqrt(E/Fy): Cv1 = 1.0, phi_v = 1.0
- LRFD: phi_v = 0.90 (or 1.0); ASD: Omega_v = 1.67 (or 1.50)

### Deflection
- Use unfactored (service) loads
- I required = 5wL^4 / (384*E*delta_allow) for uniform load
- Standard limits per IBC Table 1604.3

### Compact Section Check (Table B4.1b)
- Flange: bf/(2tf) ≤ 0.38*sqrt(E/Fy)
- Web: h/tw ≤ 3.76*sqrt(E/Fy)

## Column Design (AISC 360 Chapter E)

### Compression
- Determine KL/r for both axes (use larger)
- Fe = pi^2 * E / (KL/r)^2
- If KL/r ≤ 4.71*sqrt(E/Fy): Fcr = 0.658^(Fy/Fe) * Fy (inelastic)
- If KL/r > 4.71*sqrt(E/Fy): Fcr = 0.877 * Fe (elastic)
- Pn = Fcr * Ag
- LRFD: phi_c = 0.90; ASD: Omega_c = 1.67

### Effective Length
- Use alignment charts (AISC Commentary Fig. C-A-7.1/7.2) for K
- Braced frames: K ≤ 1.0 (typically K = 1.0)
- Unbraced frames: K > 1.0 (can be 1.5 to 2.0+)
- Direct analysis method (Chapter C) allows K = 1.0 with notional loads and reduced stiffness

### Combined Axial + Bending (Chapter H)
- Pr/(2Pc) + [Mrx/Mcx + Mry/Mcy] ≤ 1.0 when Pr/Pc < 0.2
- Pr/Pc + (8/9)[Mrx/Mcx + Mry/Mcy] ≤ 1.0 when Pr/Pc ≥ 0.2

## Connection Design

### Bolted Connections
**Bolt Strength (per bolt):**
- Shear: Rn = Fnv * Ab (phi = 0.75)
  - A325-N: Fnv = 54 ksi; A325-X: Fnv = 68 ksi
  - A490-N: Fnv = 68 ksi; A490-X: Fnv = 84 ksi
- Tension: Rn = Fnt * Ab (phi = 0.75)
  - A325: Fnt = 90 ksi; A490: Fnt = 113 ksi
- Bearing: Rn = 2.4*d*t*Fu (phi = 0.75) — deformation at service a consideration
- Slip-critical: Rn = mu * Du * hf * Tb * ns (phi = 1.0 for serviceability, 0.85 for strength)

**Bolt Spacing and Edge Distance:**
- Minimum spacing: 2-2/3 d (preferred 3d)
- Minimum edge distance: Table J3.4
- Maximum edge distance: 12t or 6"

### Welded Connections
**Fillet Welds:**
- Rn = 0.60 * FEXX * (0.707 * w * L) — weld metal strength
- Check base metal: Rn = 0.60 * Fy * t * L (shear yielding) or 0.45 * Fu * t * L (shear rupture)
- Minimum fillet weld size: Table J2.4
- Maximum fillet weld size: t - 1/16" for material ≥ 1/4"

**Complete Joint Penetration (CJP):**
- Develops full strength of connected material
- Required for certain seismic connections

### Common Connection Types
- **Simple shear:** Single plate (shear tab), double angle, end plate
- **Moment:** Extended end plate, directly welded flange, bolted flange plate
- **Brace gusset:** Whitmore section, block shear, buckling checks

## Seismic Steel Design (AISC 341)

### Member Requirements
- **Highly Ductile Members** (SCBF braces, SMF beams): lambda_hd per Table D1.1
- **Moderately Ductile Members** (IMF, OCBF): lambda_md per Table D1.1
- Protected zones: no attachments, penetrations, or modifications

### SCBF Requirements (Section F2)
- Brace KL/r ≤ 200
- Brace sections: compact per highly ductile limits
- Connection: designed for expected brace strength in tension (Ry*Fy*Ag) and compression
- Beam and column: designed for capacity-limited forces
- Gusset plates: 2tp linear clearance for brace buckling

### SMF Requirements (Section E3)
- Strong column / weak beam: sum(Mpc) ≥ sum(1.0*Mpr) at joints
- Connections: prequalified per AISC 358 or qualified by testing
- Panel zone: check for shear per Section E3.6e
- Column splices: designed for amplified forces

## Rules of Thumb

- **Beam depth:** Span (ft) / 2 = depth (in.) for floor beams
- **Beam weight:** 1.0-1.5 × span (ft) = weight (plf) for typical floor loads
- **Column W-shape:** W10 or W12 for most buildings up to 5 stories
- **Base plate:** Column depth + 4-6" each direction
- **Bolt quantity (shear):** Load (kips) / 15 per A325-N 3/4" bolt (rough)

## Common Errors to Avoid

- Not checking LTB for unbraced beam segments
- Using K = 1.0 for unbraced frame columns without direct analysis
- Forgetting to check block shear at connections
- Not checking prying action on bolts in tension
- Using A36 design values for A992 material (conservative but not optimal)
- Not applying Ry factor for expected yield strength in seismic connections
- Forgetting web crippling and yielding checks at concentrated loads
- Inadequate column base plate design

## Deliverable Checklist

- [ ] Member design with demand/capacity ratios
- [ ] Connection design with complete load path
- [ ] Deflection checks at service loads
- [ ] Drift check (if lateral system)
- [ ] Seismic detailing requirements (if SDC C or higher)
- [ ] Member schedule with sizes, grades, and orientation
- [ ] Connection schedule with bolt/weld specifications
