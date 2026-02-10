# Skill: Wood / Timber Design

## Purpose

This skill covers structural wood design per the National Design Specification (NDS) and Special Design Provisions for Wind and Seismic (SDPWS). Wood construction is prevalent in Washington State residential and light commercial projects.

## Applicable Standards

- **NDS** — National Design Specification for Wood Construction (AWC)
- **NDS Supplement** — Design Values for Wood Construction
- **SDPWS** — Special Design Provisions for Wind and Seismic
- **IBC Chapter 23** — Wood
- **AWC PWF** — Permanent Wood Foundation (if applicable)

## Design Method

NDS provides both ASD and LRFD procedures. ASD is traditional and most common in wood design.

### ASD Adjustment Factors

Reference design values from NDS Supplement are adjusted:

| Factor | Symbol | Applies To | Reference |
|--------|--------|-----------|-----------|
| Load Duration | CD | All except E, Emin | Table 2.3.2 |
| Wet Service | CM | All | Supplement tables |
| Temperature | Ct | All | Table 2.3.3 |
| Beam Stability | CL | Fb | Section 3.3.3 |
| Size | CF | Fb, Ft, Fc (sawn lumber) | Supplement tables |
| Flat Use | Cfu | Fb | Supplement tables |
| Incising | Ci | All | Table 4.3.8 |
| Repetitive Member | Cr | Fb (sawn lumber) | Section 4.3.9 |
| Column Stability | CP | Fc | Section 3.7.1 |
| Buckling Stiffness | CT | Emin (trusses) | Section 4.4.2 |
| Bearing Area | Cb | Fc_perp | Section 3.10.4 |
| Volume | CV | Fb (glulam) | Section 5.3.6 |
| Curvature | Cc | Fb (glulam) | Section 5.4.4 |

### Common Load Duration Factors (CD)
- Dead load: 0.90
- Dead + Live (occupancy): 1.00
- Dead + Live (floor) + Snow: 1.15
- Dead + Wind or Seismic: 1.60
- Impact: 2.00

## Beam Design

### Flexure
- fb = M / S ≤ F'b = Fb * (CD * CM * Ct * CL * CF * Cfu * Ci * Cr)
- For glulam: F'b = Fb * (CD * CM * Ct * CV or CL * Cc * CI)
- CL and CV not applied simultaneously for glulam — use lesser

### Shear
- fv = VQ / Ib = (3V) / (2A) for rectangular sections
- fv ≤ F'v = Fv * (CD * CM * Ct * Ci)
- Shear at supports: reduce V by loads within d of support (NDS Section 3.4.3)

### Deflection
- Use E' = E * (CM * Ct * Ci) for deflection calculations
- Long-term deflection: multiply by 1.5 (seasoned lumber) or 2.0 (green lumber) per NDS Table 3.5.2
- Creep factor for sustained loads — significant for wood

### Bearing
- fc_perp = P / A_bearing ≤ F'c_perp = Fc_perp * (CM * Ct * Ci * Cb)
- Cb = (Lb + 0.375) / Lb for bearings < 6" and not at end of member
- Minimum bearing length: 1.5" on wood, 3" on concrete/masonry (recommended)

## Column Design

### Axial Compression
- fc = P / A ≤ F'c = Fc * (CD * CM * Ct * CF * Ci * CP)
- CP = (1 + (FcE/F*c)) / (2c) - sqrt[((1 + (FcE/F*c)) / (2c))^2 - (FcE/F*c) / c]
- FcE = 0.822 * E'min / (Le/d)^2
- c = 0.8 for sawn lumber, 0.9 for glulam
- F*c = Fc adjusted by all factors except CP
- Le/d ≤ 50

### Effective Length
- Le = Ke * L (Ke depends on end conditions)
- Pin-pin: Ke = 1.0
- Fixed-free: Ke = 2.1
- Check both axes; design for governing slenderness

### Combined Axial + Bending (NDS Section 3.9)
- (fc/F'c)^2 + fb1/(F'b1(1 - fc/FcE1)) + fb2/(F'b2(1 - fc/FcE2 - (fb1/FbE)^2)) ≤ 1.0

## Common Sawn Lumber Species Groups

### Douglas Fir-Larch (most common in Pacific NW)
| Grade | Fb (psi) | Ft (psi) | Fv (psi) | Fc (psi) | E (psi) | Emin (psi) |
|-------|----------|----------|----------|----------|---------|------------|
| Select Structural (2x) | 1,500 | 1,000 | 180 | 1,700 | 1,900,000 | 690,000 |
| No. 1 (2x) | 1,000 | 675 | 180 | 1,500 | 1,700,000 | 620,000 |
| No. 2 (2x) | 900 | 575 | 180 | 1,350 | 1,600,000 | 580,000 |
| Stud | 675 | 450 | 180 | 850 | 1,400,000 | 510,000 |

*Values shown for dimension lumber ≤ 4" wide. Verify in NDS Supplement for specific sizes.*

### Engineered Wood Products
- **LVL:** Fb = 2,600-3,100 psi, E = 1,900,000-2,000,000 psi (manufacturer specific)
- **PSL:** Fb = 2,400-2,900 psi, E = 2,000,000 psi
- **Glulam (24F-V4 DF):** Fb+ = 2,400 psi, Fb- = 1,450 psi, Fv = 265 psi, E = 1,800,000 psi

## Shear Wall Design (SDPWS)

### Segmented Shear Wall
- Capacity from SDPWS Table 4.3A (wood structural panels)
- Depends on: panel type, thickness, nail size, nail spacing, stud spacing
- Aspect ratio: h/w ≤ 2:1 for full capacity (3.5:1 with reduction for wind only)

### Perforated Shear Wall (SDPWS Section 4.3.3.5)
- Allows design of wall with openings without requiring full-height segments
- Shear capacity adjustment factor Co from Table 4.3.3.5
- Each wall pier height/width must be ≤ 2:1
- Hold-downs required at ends of perforated wall only

### Diaphragm Design (SDPWS)
- Capacity from SDPWS Table 4.2A (blocked) or 4.2B (unblocked)
- Blocked diaphragms required for higher shear demands
- High-load diaphragms: consider 3" edge nailing with 10d nails

## Connection Design

### Fastener Types
- **Nails:** Common wire nails, sinker nails. Reference lateral values per NDS Table 12.3.1
- **Bolts:** Per NDS Section 12.3. Yield limit equations for single/double shear
- **Lag Screws:** Per NDS Section 12.3. Consider both lateral and withdrawal
- **Wood Screws:** Per NDS Section 12.3
- **Split Rings / Shear Plates:** For heavy timber connections per NDS Chapter 13
- **Metal Connector Plates:** Per manufacturer (Simpson, USP, MiTek)

### Simpson Strong-Tie Common Hardware
- **Joist hangers:** LUS, HUS,?"" series — verify for loading and member size
- **Hold-downs:** HDU, HHDQ, PHD series — verify for uplift demand
- **Straps:** LSTA, MSTA, CMST series — verify for tension demand
- **Post bases:** ABU, CBS, ABA series — verify for post size and loading
- **Angles:** A35, L-series — verify for load and configuration

## Washington State Considerations

- Douglas Fir-Larch is the predominant species available in the Pacific Northwest
- Moisture conditions: generally dry service for interior, verify for exposed or below-grade
- Preservative treatment required for soil contact, exterior exposed applications
- Check for incising effects on design values when preservative-treated lumber is incised
- Snow loads — wood roof systems in mountain areas need careful deflection/ponding checks

## Common Errors to Avoid

- Forgetting to apply CD (load duration factor) — this is the most common wood design error
- Using wrong CF for actual member size
- Not checking CL (beam stability) for unbraced compression edge
- Ignoring long-term creep deflection for sustained loads
- Using full nail capacity when edge distance or spacing is insufficient
- Not reducing shear wall capacity for aspect ratio > 2:1
- Mixing manufacturer-specific EWP values with generic NDS values
- Not checking net section at connections (bolt holes, notches)

## Deliverable Checklist

- [ ] Member design with all NDS adjustment factors documented
- [ ] Deflection check including long-term effects
- [ ] Connection design with fastener schedules
- [ ] Shear wall design with nailing schedule
- [ ] Hold-down schedule with hardware specifications
- [ ] Diaphragm nailing schedule
- [ ] Bearing checks at all supports
