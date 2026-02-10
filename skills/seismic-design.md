# Skill: Seismic Analysis and Design

## Purpose

This skill covers seismic analysis and design procedures per ASCE 7 Chapters 11-23. Given Washington State's high seismicity (SDC D typical in western WA), seismic design is a core competency for RaBuilt Engineering.

## Seismic Design Procedure Overview

```
1. Determine Site Seismicity (SS, S1) → USGS Seismic Hazard Maps
2. Determine Site Class → Geotechnical Report (default D)
3. Calculate Design Spectral Parameters (SDS, SD1)
4. Determine Risk Category and Importance Factor (Ie)
5. Determine Seismic Design Category (SDC)
6. Select Seismic Force Resisting System (SFRS)
7. Determine R, Cd, Omega_0
8. Check for Irregularities
9. Select Analysis Procedure
10. Calculate Base Shear and Distribute Forces
11. Design SFRS Elements
12. Check Drift
13. Design Diaphragms, Collectors, and Connections
14. Detail for Ductility
```

## Seismic Hazard Parameters

### Determining SS and S1
- Use USGS Unified Hazard Tool (https://earthquake.usgs.gov/hazards/)
- Input: latitude/longitude of project site
- Risk-targeted MCE ground motions: SS (0.2s), S1 (1.0s)

### Washington State Typical Values

| Location | SS (g) | S1 (g) | Typical SDC |
|----------|--------|--------|-------------|
| Seattle | 1.2-1.5 | 0.4-0.6 | D |
| Tacoma | 1.2-1.5 | 0.4-0.6 | D |
| Olympia | 1.0-1.4 | 0.4-0.5 | D |
| Bellingham | 1.0-1.3 | 0.4-0.5 | D |
| Spokane | 0.3-0.5 | 0.1-0.2 | B-C |
| Yakima | 0.4-0.6 | 0.1-0.3 | C-D |
| Vancouver | 0.8-1.2 | 0.3-0.5 | D |

### Site Coefficients
- Fa = f(Site Class, SS) — Table 11.4-1
- Fv = f(Site Class, S1) — Table 11.4-2
- **Site Class F** requires site-specific ground motion analysis

### Design Parameters
- SMS = Fa * SS
- SM1 = Fv * S1
- SDS = (2/3) * SMS
- SD1 = (2/3) * SM1

## Equivalent Lateral Force Procedure (ASCE 7 Section 12.8)

### Applicability
Permitted for all structures in SDC B and C. For SDC D-F, limited to:
- Risk Category I/II with T < 3.5*Ts and no structural irregularities
- Light-frame construction
- Structures up to 160 ft with certain conditions (Table 12.6-1)

### Base Shear
- V = Cs * W
- Cs = SDS / (R/Ie)
- Cs need not exceed SD1 / (T * R/Ie) for T ≤ TL
- Cs shall not be less than 0.044*SDS*Ie ≥ 0.01
- For S1 ≥ 0.6g: Cs ≥ 0.5*S1 / (R/Ie)

### Period Determination
- Ta = Ct * hn^x (approximate period per Table 12.8-2)
  - Steel MRF: Ct = 0.028, x = 0.8
  - Concrete MRF: Ct = 0.016, x = 0.9
  - Steel EBF/BF: Ct = 0.03, x = 0.75
  - All other: Ct = 0.02, x = 0.75
- T = Cu * Ta (upper limit on computed period, Table 12.8-1)

### Vertical Distribution
- Fx = Cvx * V
- Cvx = (wx * hx^k) / sum(wi * hi^k)
- k = 1 for T ≤ 0.5s, k = 2 for T ≥ 2.5s, interpolate between

## Modal Response Spectrum Analysis (ASCE 7 Section 12.9)

### When Required
- Structures with T ≥ 3.5*Ts in SDC D-F
- Irregular structures where ELF is not permitted

### Procedure
1. Develop structural model with mass and stiffness
2. Perform eigenvalue analysis — extract modes until 90% mass participation
3. Apply design response spectrum (Section 11.4.6)
4. Combine modal responses — CQC method (preferred) or SRSS
5. Scale results: V_dynamic ≥ 100% of V_ELF (Section 12.9.1.4.1)
6. Apply accidental torsion
7. Check drift using Cd * delta / Ie

## Irregularities

### Horizontal Irregularities (Table 12.3-1)
1. **Torsional** — Max drift > 1.2 * average drift at story
2. **Extreme Torsional** — Max drift > 1.4 * average drift
3. **Reentrant Corner** — Projection > 15% of plan dimension
4. **Diaphragm Discontinuity** — Opening > 50% of area, or stiffness change > 50%
5. **Nonparallel Systems** — LFRS not parallel to major axes

### Vertical Irregularities (Table 12.3-2)
1. **Stiffness (Soft Story)** — Story stiffness < 70% of story above or < 80% of average of 3 stories above
2. **Extreme Soft Story** — < 60% or < 70% of average
3. **Weight (Mass)** — Mass > 150% of adjacent story
4. **In-Plane Discontinuity** — Offset in LFRS element > length of element
5. **Weak Story** — Story strength < 80% of story above

### Consequences
- Certain irregularities prohibit ELF procedure
- Extreme soft story and weak story prohibited in SDC E/F
- Irregularities trigger additional analysis and detailing requirements
- Redundancy factor rho may be affected

## Redundancy Factor (rho) — Section 12.3.4

- rho = 1.0 for SDC B and C
- rho = 1.3 for SDC D-F unless conditions of Section 12.3.4.2 are met
- Conditions for rho = 1.0 in SDC D-F:
  - Loss of moment resistance at beam-to-column connection at both ends of a single beam does not result in more than 33% reduction in story strength or extreme torsional irregularity
  - Or: at least two bays of SFRS in each direction at each story

## Seismic Detailing Requirements

### Wood (NDS/SDPWS)
- Shear wall aspect ratio limits
- Nailing requirements at panel edges
- Hold-down and anchorage requirements
- Blocking and framing connector requirements

### Steel (AISC 341)
- Member compactness requirements (highly ductile, moderately ductile)
- Connection requirements (prequalified or tested)
- Brace slenderness limits for SCBF
- Column splice design including overstrength
- Protected zone limitations

### Concrete (ACI 318 Chapter 18)
- Confinement reinforcement in columns and boundary elements
- Beam and column proportioning
- Joint shear requirements
- Development length modifications
- Shear wall boundary element triggers

## Non-Structural Component Design (Section 13)

- Fp = (0.4*ap*SDS*Wp / (Rp/Ip)) * (1 + 2*z/h)
- Not less than 0.3*SDS*Ip*Wp
- Not more than 1.6*SDS*Ip*Wp
- Applies to mechanical, electrical, architectural components, and their supports/attachments

## Common Errors to Avoid

- Using wrong Risk Category for Ie determination
- Not checking both SDS-based and SD1-based Cs equations
- Forgetting minimum Cs check (0.044*SDS*Ie ≥ 0.01)
- Not checking minimum Cs for S1 ≥ 0.6g (applicable in much of western WA)
- Applying ELF when MRSA is required due to irregularity
- Not applying accidental torsion
- Using elastic drift instead of amplified drift (Cd * delta_xe / Ie)
- Incomplete redundancy factor analysis
- Not applying Omega_0 to collectors and their connections
- Forgetting non-structural component anchorage requirements

## Deliverable Checklist

- [ ] Seismic parameter determination (SS, S1, Site Class, SDS, SD1, SDC)
- [ ] SFRS selection with R, Cd, Omega_0
- [ ] Irregularity check
- [ ] Base shear calculation
- [ ] Vertical force distribution
- [ ] Lateral analysis (ELF or MRSA)
- [ ] SFRS member design
- [ ] Drift check at each story
- [ ] Diaphragm design including Fpx
- [ ] Collector design with Omega_0
- [ ] Hold-down and anchorage design
- [ ] Foundation seismic design
- [ ] Non-structural component anchorage (if in scope)
