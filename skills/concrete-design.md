# Skill: Reinforced Concrete Design

## Purpose

This skill covers reinforced concrete design per ACI 318 — Building Code Requirements for Structural Concrete. Concrete is used in foundations, retaining walls, elevated slabs, shear walls, and special moment frames.

## Applicable Standards

- **ACI 318** — Building Code Requirements for Structural Concrete
- **ACI 301** — Specifications for Structural Concrete
- **ACI 332** — Residential Code Requirements for Structural Concrete
- **CRSI Design Handbook** — Practical design reference

## Material Properties

### Common Concrete Strengths
| f'c (psi) | Common Use |
|-----------|------------|
| 3,000 | Residential footings, non-structural |
| 4,000 | Standard structural — beams, columns, slabs, walls |
| 5,000 | Higher-strength applications, post-tensioned |
| 6,000-8,000 | High-rise columns, precast |

### Reinforcing Steel
| Grade | fy (ksi) | Common Use |
|-------|----------|------------|
| Grade 40 | 40 | Older construction (rarely specified new) |
| Grade 60 | 60 | Standard for all applications |
| Grade 80 | 80 | Permitted for certain applications per ACI 318 |

### Key Material Properties
- Ec = 57,000 * sqrt(f'c) psi (normal weight concrete)
- fr = 7.5 * sqrt(f'c) psi (modulus of rupture)
- beta_1 = 0.85 for f'c ≤ 4,000 psi; decreases 0.05 per 1,000 psi above 4,000; minimum 0.65
- Normal weight concrete: 150 pcf (145 pcf without reinforcement)
- Lightweight concrete: 90-120 pcf (lambda factor applies)

## Beam Design (ACI 318 Chapter 9)

### Flexural Design
1. Determine Mu from factored load combinations
2. Assume tension-controlled section (phi = 0.90)
3. Mu = phi * As * fy * (d - a/2), where a = As*fy / (0.85*f'c*b)
4. Or use: Rn = Mu / (phi*b*d^2), then rho from Rn
5. Check: rho_min = max(3*sqrt(f'c)/fy, 200/fy) — ACI 318 Section 9.6.1.2
6. Check: rho_max for tension-controlled (c/dt ≤ 0.375 for Grade 60)
7. Select bar sizes and check spacing, cover requirements

### Shear Design
1. Determine Vu at critical section (d from face of support)
2. Vc = 2 * sqrt(f'c) * bw * d (simplified, ACI 318 Table 22.5.5.1)
3. If Vu > phi*Vc: provide stirrups. Vs = (Vu/phi) - Vc
4. Vs = Av * fy * d / s → solve for s
5. Maximum spacing: d/2 or 24" (d/4 or 12" when Vs > 4*sqrt(f'c)*bw*d)
6. Minimum stirrups: Av_min = max(0.75*sqrt(f'c)*bw*s/fy, 50*bw*s/fy)
7. Maximum Vs: 8*sqrt(f'c)*bw*d — if exceeded, increase section size

### Deflection
- Minimum thickness (Table 9.3.1.1): L/16 (simple), L/18.5 (one end cont.), L/21 (both ends cont.), L/8 (cantilever)
- If below minimum, calculate deflections using Ie (effective moment of inertia)
- Ie = Icr + (Ig - Icr)(Mcr/Ma)^3 ≤ Ig (Branson's equation)
- Long-term deflection multiplier: lambda_delta = xi / (1 + 50*rho') — xi from Table 24.2.4.1.3

## Slab Design

### One-Way Slabs (Chapter 7)
- Design as beam per unit width (12" strip)
- Minimum thickness per Table 7.3.1.1
- Minimum reinforcement: As_min = 0.0018*b*h (Grade 60)
- Maximum spacing: min(3h, 18")
- Temperature/shrinkage reinforcement required perpendicular to span

### Two-Way Slabs (Chapter 8)
- Direct Design Method (Section 8.10): limited to regular geometry, minimum 3 spans
- Equivalent Frame Method (Section 8.11): more general
- Total static moment: Mo = qu * L2 * Ln^2 / 8
- Distribute to column and middle strips per Tables 8.10.4.2 through 8.10.5.2
- Check punching shear at columns (Section 22.6.5): vu ≤ phi*vc at critical section d/2 from column face
- Punching shear: vc = minimum of 4*sqrt(f'c), (2 + 4/beta)*sqrt(f'c), (2 + alpha_s*d/bo)*sqrt(f'c)

## Column Design (Chapter 10)

### Short Column (no slenderness effects)
- Interaction diagram approach: plot phi*Pn vs. phi*Mn
- Use ACI interaction diagrams (CRSI or SP-17A) or software
- Minimum reinforcement: 1% Ag; Maximum: 8% Ag (practical max ~4%)
- Minimum column size: 10" (code), 12" (practical)
- Ties: #3 for longitudinal bars ≤ #10; #4 for #11, #14, #18
- Tie spacing: min(16db_longitudinal, 48db_tie, least column dimension)

### Slenderness Effects (Section 6.6)
- klu/r: if > 22 (braced) or > 22 (unbraced with check), slenderness must be considered
- Moment magnification method (Section 6.6.4) or P-Delta analysis
- Nonsway: Mc = delta_ns * M2, where delta_ns = Cm / (1 - Pu/(0.75*Pc)) ≥ 1.0
- Sway: delta_s amplification of sway moments

## Wall Design (Chapter 11)

### Bearing Walls
- Simplified method (Section 11.5.3): Pn = 0.55*f'c*Ag*(1 - (klc/32h)^2)
- Or design as column using interaction diagram

### Shear Walls (Section 18.10 for seismic)
- In-plane shear: Vn = Acv*(alpha_c*sqrt(f'c) + rho_t*fy)
- Boundary elements required when compressive stress > 0.2*f'c (simplified trigger)
- Boundary element detailing: confinement per Section 18.10.6

## Foundation Design

### Spread Footings (Chapter 13)
1. Size footing for allowable soil bearing (service loads): q = P/A ≤ q_allow
2. Design for factored loads (LRFD)
3. Check one-way shear at d from face of column
4. Check two-way (punching) shear at d/2 from face of column
5. Design flexural reinforcement: moment at face of column
6. Check development length of reinforcement
7. Minimum reinforcement: 0.0018*b*h (Grade 60)

### Continuous Footings
- Same design approach as spread footings, per unit length
- Check for bending in longitudinal direction if loads vary

### Retaining Walls
- Stability: sliding (FS ≥ 1.5), overturning (FS ≥ 2.0), bearing (q ≤ q_allow)
- Stem design: cantilever with lateral earth pressure
- Heel/toe design: soil pressure minus weight
- Key design if needed for sliding resistance

## Cover Requirements (Table 20.6.1.3.1)

| Condition | Cover |
|-----------|-------|
| Cast against earth | 3" |
| Exposed to weather (#6 and larger) | 2" |
| Exposed to weather (#5 and smaller) | 1-1/2" |
| Not exposed, slabs/walls (#14 and smaller) | 3/4" |
| Not exposed, beams/columns | 1-1/2" |

## Development Length (Chapter 25)

### Tension (Section 25.4.2.3 simplified)
- #6 and smaller: ld = (fy*psi_t*psi_e / (25*sqrt(f'c))) * db
- #7 and larger: ld = (fy*psi_t*psi_e / (20*sqrt(f'c))) * db
- Minimum ld = 12"

### Compression (Section 25.4.9)
- ldc = max((0.02*fy/sqrt(f'c))*db, 0.0003*fy*db, 8")

### Hooks (Section 25.4.3)
- ldh = (0.02*fy*psi_e / (sqrt(f'c))) * db
- Standard hook: 90-degree with 12db extension, or 180-degree with 4db extension

## Common Errors to Avoid

- Using service loads for concrete member design (must use factored loads for strength)
- Using factored loads for footing sizing on soil (must use service loads for bearing)
- Forgetting minimum reinforcement requirements
- Not checking development length at discontinuities
- Ignoring long-term deflection multiplier for sustained loads
- Not providing adequate concrete cover for exposure conditions
- Confusing one-way and two-way shear checks at footings/slabs
- Not checking punching shear at slab-column connections

## Deliverable Checklist

- [ ] Member design with reinforcement schedule
- [ ] Shear design with stirrup/tie spacing
- [ ] Deflection check (if not meeting minimum thickness)
- [ ] Development length verification
- [ ] Foundation bearing, shear, and flexure checks
- [ ] Reinforcement details and bar schedules
- [ ] Cover and spacing verification
