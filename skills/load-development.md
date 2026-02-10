# Skill: Load Development and Combinations

## Purpose

This skill covers the determination of all design loads and their combinations for structural design per ASCE 7 and IBC. Load development is the foundation of every structural design — errors here propagate through every subsequent calculation.

## Applicable Standards

- ASCE 7 — Minimum Design Loads and Associated Criteria
- IBC Chapter 16 — Structural Design
- WAC 51-50 — Washington State amendments

## Load Types

### Dead Load (D)
- Self-weight of structural elements
- Superimposed dead loads (roofing, MEP, finishes, partitions)
- Permanent equipment

**Common Values (verify for specific project):**

| Component | Typical Load (psf) |
|-----------|-------------------|
| Concrete slab (per inch) | 12.5 |
| Steel deck (20 ga composite) | 2-3 |
| Lightweight concrete (per inch) | 8-9 |
| Roofing (built-up) | 5-7 |
| Suspended ceiling + MEP | 5-10 |
| Partition allowance (office) | 15-20 (per ASCE 7 4.3.2) |
| Wood framing (floor) | 8-12 |
| Wood framing (roof) | 5-8 |

### Live Load (L)
Per ASCE 7 Table 4.3-1:

| Occupancy | LL (psf) |
|-----------|----------|
| Residential | 40 |
| Office | 50 |
| Corridors (above first floor) | 80 |
| Corridors (first floor) | 100 |
| Light storage | 125 |
| Heavy storage | 250 |
| Assembly (fixed seats) | 60 |
| Assembly (movable seats) | 100 |
| Retail (first floor) | 100 |
| Retail (upper floors) | 75 |
| Garages (passenger) | 40 |

**Live Load Reduction (ASCE 7 Section 4.7):**
- L = L_0 * (0.25 + 15/sqrt(K_LL * A_T))
- Minimum: 50% for members supporting one floor, 40% for two or more floors
- No reduction for loads > 100 psf, assembly areas, garages, or roofs

### Roof Live Load (Lr)
Per ASCE 7 Section 4.8:
- Lr = 20*R1*R2
- R1: tributary area factor
- R2: slope factor
- Range: 12 to 20 psf

### Snow Load (S)
Per ASCE 7 Chapter 7:
- pf = 0.7 * Ce * Ct * Is * pg
- pg = ground snow load (from ASCE 7 maps or local jurisdiction)
- Ce = exposure factor (Table 7.3-1)
- Ct = thermal factor (Table 7.3-2)
- Is = importance factor (Table 1.5-2)

**Washington State Notes:**
- Ground snow loads vary dramatically — from 20 psf in lowlands to 200+ psf in mountains
- Many jurisdictions publish local snow load maps that supersede ASCE 7
- Check with local building department for site-specific requirements
- Drift loads on lower roofs, projections, and roof obstructions per Section 7.7-7.9
- Rain-on-snow surcharge per Section 7.10 where pg <= 20 psf

### Wind Load (W)
Per ASCE 7 Chapters 26-30:
- V = basic wind speed from ASCE 7 maps (by Risk Category)
- Kd = wind directionality factor (Table 26.6-1)
- Kz = velocity pressure exposure coefficient (Table 26.10-1)
- Kzt = topographic factor (Section 26.8)
- Ke = ground elevation factor (Table 26.9-1)
- qz = 0.00256 * Kz * Kzt * Kd * Ke * V^2

**Washington State Notes:**
- Western WA generally governed by seismic, not wind
- Eastern WA and gorge areas may have higher wind loads
- Topographic effects significant in hilly terrain per Section 26.8

### Seismic Load (E)
Per ASCE 7 Chapters 11-23:
- Determine SS, S1 from USGS seismic hazard maps (site-specific)
- Site class from geotechnical report (default D if unknown)
- SDS = (2/3) * Fa * SS
- SD1 = (2/3) * Fv * S1
- Seismic Design Category from Tables 11.6-1 and 11.6-2
- Select SFRS and determine R, Cd, Omega_0

**Washington State Notes:**
- Western WA is high seismic (SDC D typical for most sites)
- Seattle/Puget Sound region: SS typically 1.0-1.5g, S1 typically 0.4-0.6g
- Eastern WA: lower seismic but not negligible
- Liquefaction potential in alluvial soils — check geotech report

## Load Combinations

### LRFD (ASCE 7 Section 2.3.1)
1. 1.4D
2. 1.2D + 1.6L + 0.5(Lr or S or R)
3. 1.2D + 1.6(Lr or S or R) + (L or 0.5W)
4. 1.2D + 1.0W + L + 0.5(Lr or S or R)
5. 1.2D + 1.0E + L + 0.2S
6. 0.9D + 1.0W
7. 0.9D + 1.0E

### ASD (ASCE 7 Section 2.4.1)
1. D
2. D + L
3. D + (Lr or S or R)
4. D + 0.75L + 0.75(Lr or S or R)
5. D + (0.6W or 0.7E)
6a. D + 0.75L + 0.75(0.6W) + 0.75(Lr or S or R)
6b. D + 0.75L + 0.75(0.7E) + 0.75S
7. 0.6D + 0.6W
8. 0.6D + 0.7E

### Special Seismic Combinations (ASCE 7 Section 12.4.3)
- Including overstrength: Em = Omega_0 * QE
- Including vertical seismic: Ev = 0.2*SDS*D
- Required for collectors, diaphragm connections to vertical elements, etc.

## Procedure

1. **Establish building geometry** — plan dimensions, heights, roof slopes
2. **Determine Risk Category** (ASCE 7 Table 1.5-1) and importance factors
3. **Calculate dead loads** — itemize all components, document sources
4. **Determine live loads** — from ASCE 7 Table 4.3-1, apply reductions where permitted
5. **Calculate snow loads** — ground snow from jurisdiction, apply exposure/thermal/importance
6. **Calculate wind loads** — determine exposure, basic wind speed, pressure coefficients
7. **Determine seismic parameters** — SS, S1, site class, SDS, SD1, SDC, SFRS, R/Cd/Omega_0
8. **Assemble load combinations** — ASD or LRFD per project basis
9. **Identify governing combinations** for each element type
10. **Document all sources and assumptions**

## Common Errors to Avoid

- Forgetting to include partition loads in dead load (ASCE 7 4.3.2 — 15 psf minimum for office)
- Applying live load reduction to areas where it is not permitted
- Using wrong Risk Category for importance factor
- Not checking both minimum and maximum snow load cases (balanced vs. unbalanced)
- Ignoring drift loads at roof level changes
- Using wrong exposure category for wind
- Not including vertical seismic effect (Ev) in seismic combinations
- Mixing ASD and LRFD load factors in the same design
