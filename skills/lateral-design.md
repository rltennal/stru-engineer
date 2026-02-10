# Skill: Lateral Force Resisting System Design

## Purpose

This skill covers the design of the lateral force resisting system (LFRS) for wind and seismic loads. The LFRS includes diaphragms, shear walls, braced frames, moment frames, collectors, and their connections — the complete lateral load path from point of application to the foundation.

## Lateral Load Path

```
Wind/Seismic Forces Applied to Building
        ↓
Cladding / Walls → Diaphragm (roof/floor)
        ↓
Diaphragm distributes to vertical LFRS elements
        ↓
Collectors / Drag Struts gather forces to vertical elements
        ↓
Shear Walls / Braced Frames / Moment Frames
        ↓
Foundation (resist overturning, sliding, uplift)
        ↓
Soil (passive pressure, friction, piles/piers)
```

## System Selection

### Seismic Force Resisting Systems (ASCE 7 Table 12.2-1)

| System | R | Cd | Omega_0 | Height Limit (SDC D) |
|--------|---|----|---------|--------------------|
| Special Steel MF | 8 | 5.5 | 3 | NL |
| Special Concrete MF | 8 | 5.5 | 3 | NL |
| Special CBF (steel) | 6 | 5 | 2 | 160 ft |
| Special RCW | 5-6 | 5 | 2.5 | 160 ft |
| Light-frame wood walls (wood panels) | 6.5 | 4 | 3 | 65 ft |
| Ordinary CBF (steel) | 3.25 | 3.25 | 2 | 35 ft (SDC D) |
| Ordinary Steel MF | 3.5 | 3 | 3 | NP (SDC D) |

### System Selection Considerations
- **Seismic Design Category** limits available systems
- **Building height** limits per ASCE 7 Table 12.2-1
- **Irregularities** may prohibit certain systems
- **Architectural constraints** — moment frames allow open bays, shear walls block openings
- **Economy** — braced frames typically most economical, moment frames most expensive
- **Redundancy** — more lateral elements = better performance and lower rho

## Diaphragm Design

### Rigid vs. Flexible Diaphragm
- **Flexible:** Wood structural panel, untopped steel deck → distribute loads by tributary area
- **Rigid:** Concrete-filled deck, concrete slab → distribute loads by relative stiffness
- **Semi-rigid:** Requires analysis considering both diaphragm stiffness and vertical element stiffness
- ASCE 7 Section 12.3.1 defines conditions for flexible diaphragm assumption

### Diaphragm Design Procedure
1. Determine lateral forces at each diaphragm level
2. Distribute to diaphragm based on rigid/flexible assumption
3. Analyze diaphragm as a deep beam (shear and moment)
4. Design sheathing nailing / concrete slab / deck for shear demand
5. Design chords for flexural tension/compression
6. Design collectors/drag struts to transfer forces to vertical elements
7. Check diaphragm deflection (ASCE 7 Section 12.12.2)

### Diaphragm Force (Fpx) — ASCE 7 Section 12.10.1
- Fpx = (sum of Fi from top to level x) / (sum of wi from top to level x) * wpx
- Minimum: Fpx = 0.2*SDS*Ie*wpx
- Maximum: Fpx = 0.4*SDS*Ie*wpx

### Wood Diaphragm Capacities
Per SDPWS Table 4.2A/4.2B:
- Depends on: panel type, thickness, nail size, nail spacing, framing width, blocking
- Blocked diaphragms have significantly higher capacity than unblocked
- Edge nailing spacing: 6", 4", 3", 2" — capacity increases as spacing decreases

## Shear Wall Design

### Wood Shear Walls (per SDPWS)
1. Determine shear demand at each story
2. Select sheathing type and nailing pattern from SDPWS Table 4.3A/4.3B
3. Check aspect ratio (SDPWS Table 4.3.4) — max 2:1 for wood structural panels
4. Design hold-downs for overturning (cumulative from top)
5. Design anchorage for sliding (base shear at wall base)
6. Check chord studs for combined axial + bending
7. For perforated shear walls, apply adjustment per SDPWS Section 4.3.3.5

### Steel Braced Frames
1. Determine brace forces from lateral analysis
2. Design brace members for tension and compression
3. Design gusset plate connections
4. Design beams and columns for frame forces (including Omega_0 forces at connections)
5. Check drift limits per ASCE 7 Table 12.12-1
6. For SCBF: check brace slenderness (KL/r ≤ 200), compact sections, special connection requirements per AISC 341

### Moment Frames
1. Model frame for lateral analysis
2. Design beams for combined gravity + lateral
3. Design columns: check strong-column/weak-beam (AISC 341 E3.4a)
4. Design connections (prequalified per AISC 358 or project-specific)
5. Check drift limits
6. Check P-Delta effects per ASCE 7 Section 12.8.7

## Drift Limits (ASCE 7 Table 12.12-1)

| Structure Type | Allowable Story Drift |
|---------------|----------------------|
| Risk Category I/II — other | 0.020 hsx |
| Risk Category III | 0.015 hsx |
| Risk Category IV | 0.010 hsx |
| Masonry cantilever shear walls | 0.010 hsx |
| Other masonry shear walls | 0.007 hsx |

- Drift = Cd * delta_xe / Ie
- delta_xe = elastic drift from analysis
- Check at each story, not just overall

## Overturning and Hold-Down Design

### Procedure
1. Calculate overturning moment at each level: M_OT = sum(Fi * hi)
2. Calculate restoring moment: M_R = 0.6D * (wall length / 2) — for ASD seismic
3. Net uplift at hold-down: T = (M_OT - M_R) / wall length
4. Cumulative uplift for multi-story: accumulate from top down
5. Select hold-down hardware for demand (Simpson, USP, or custom)
6. Design anchorage into foundation (anchor bolts, embedded straps)

### Continuous Rod Tie-Down Systems
- For multi-story wood buildings, continuous rod systems (e.g., Simpson Strong-Rod, ATS) preferred over discrete hold-downs at each level
- Accounts for cumulative overturning and shrinkage/compression
- Requires shrinkage compensation devices at each level

## Common Errors to Avoid

- Not checking both wind and seismic to determine which governs
- Forgetting accidental torsion (ASCE 7 Section 12.8.4.2)
- Not applying Omega_0 to collector forces where required
- Ignoring diaphragm flexibility effects on force distribution
- Not checking redundancy factor (rho) per ASCE 7 Section 12.3.4
- Missing out-of-plane anchorage of walls to diaphragms (ASCE 7 Section 12.11)
- Incomplete hold-down load path — uplift must be traced from top to foundation
- Not accounting for P-Delta effects in drift calculations

## Deliverable Checklist

- [ ] Lateral force calculation (ELF or MRSA)
- [ ] Force distribution to diaphragms and vertical elements
- [ ] Diaphragm design (shear, chords, collectors)
- [ ] Shear wall / braced frame / moment frame design
- [ ] Drift check at each story
- [ ] Overturning and hold-down design
- [ ] Foundation lateral force design
- [ ] Connection design for lateral force transfer
