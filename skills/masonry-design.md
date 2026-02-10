# Skill: Masonry Design

## Purpose

This skill covers structural masonry design per TMS 402/602 — Building Code Requirements and Specification for Masonry Structures. Masonry is commonly used in Washington State for commercial, institutional, and industrial buildings.

## Applicable Standards

- **TMS 402** — Building Code Requirements for Masonry Structures
- **TMS 602** — Specification for Masonry Structures
- **IBC Chapter 21** — Masonry
- **NCMA TEK Notes** — Practical design guidance for CMU

## Design Methods

TMS 402 provides:
- **Allowable Stress Design (ASD)** — Chapter 8
- **Strength Design (SD)** — Chapter 9
- **Empirical Design** — Chapter 5 (limited applications)
- **Prescriptive Design for Veneer** — Chapter 6

## Material Properties

### Concrete Masonry Units (CMU)
| f'm (psi) | Unit Strength (psi) | Mortar Type | Common Use |
|-----------|---------------------|-------------|------------|
| 1,500 | 1,900 | S or M | Standard structural |
| 2,000 | 2,800 | S or M | Higher-strength applications |
| 2,500 | 3,750 | S or M | Special applications |

### Mortar Types (ASTM C270)
| Type | Compressive Strength (psi) | Use |
|------|---------------------------|-----|
| M | 2,500 | Below grade, high lateral loads |
| S | 1,800 | General structural (most common) |
| N | 750 | Non-structural, above grade |

### Grout (ASTM C476)
- Minimum f'g = 2,000 psi (must be ≥ f'm)
- Fine grout: for cells ≤ 2" × 3" (less common)
- Coarse grout: for cells > 2" × 3" (typical for CMU)

### Reinforcement
- Grade 60 (fy = 60 ksi) standard
- Maximum bar size: #9 for 8" CMU, #11 for 12"+ CMU (practical)
- Lap splice per TMS 402 Section 9.3.3.4

## Wall Design — Strength Design

### Out-of-Plane Flexure (Section 9.3.5)
- For walls with axial load: check interaction using P-M interaction diagram
- Slender wall: if h/t > 30, use Section 9.3.5.4 (second-order effects)
- Mu = phi * As * fy * (d - a/2) where a = As*fy / (0.80*f'm*b)
- phi = 0.90 for flexure
- Check P-delta amplification for slender walls

### In-Plane Shear (Shear Walls) — Section 9.3.6
- Vn = An * [4.0 - 1.75(Mu/(Vu*dv))] * sqrt(f'm) + 0.25*Pu + 0.5*Av*fy*dv/s
- Maximum: An * (4 or 6) * sqrt(f'm) depending on Mu/(Vu*dv) ratio
- phi = 0.80 for shear
- Av_min = 0.0007*An (horizontal) and 0.0007*An (vertical) for SDC D+ (special reinforced)

### Axial Compression (Section 9.3.5.3)
- Pu ≤ phi * (0.80*f'm*(An - As) + fy*As) * (1 - (h/140r)^2) for h/r ≤ 99
- Buckling check for slender walls

## Reinforced Masonry Requirements by SDC

### SDC A and B — Ordinary Reinforced or Unreinforced
- Minimal prescriptive reinforcement

### SDC C — Intermediate Reinforced (Section 7.3.2.4)
- Vertical reinforcement at: corners, within 16" of openings, max 120" spacing
- Horizontal reinforcement: bond beams at top, bottom, floor/roof levels, max 120" spacing
- Minimum: #4 bars

### SDC D and E — Special Reinforced (Section 7.3.2.6)
- Vertical and horizontal reinforcement maximum spacing: 48"
- Minimum: sum(Av+Ah) ≥ 0.002*An with min 0.0007 in each direction
- Maximum spacing of reinforcement: 48" (both directions)
- All cells at corners, jambs, and intersections grouted
- Stack bond: additional requirements per Section 7.3.2.6

## Lintel and Bond Beam Design

### Lintels
- Design as reinforced masonry beam (simply supported typical)
- Bearing length: minimum 8" (4" per TMS 402, 8" recommended)
- Effective depth: to centroid of bottom reinforcement
- Minimum bearing: 4" each side of opening
- Check shear at d from face of support

### Bond Beams
- Continuous horizontal reinforced elements
- Required at: floor/roof bearing levels, top of wall, above/below openings
- Design for lateral load distribution, diaphragm anchorage, and continuity

## Reinforcement Detailing

### Cover Requirements
- 1-1/2" for bars in contact with soil
- 1-1/2" for #5 and smaller bars (not exposed)
- 2" for #6 and larger bars

### Spacing
- Minimum clear: max(1db, 1")
- Maximum for walls: 6t or 48" (SD seismic has more restrictive limits)

### Development Length (SD — Section 9.3.3.4)
- ld = 0.13*db^2*fy / (K*sqrt(f'm))
- Minimum ld = 12" or 6db (whichever is greater)

## Common Wall Assemblies

| CMU Size | Wall Thickness | Weight (fully grouted, psf) | Common Use |
|----------|---------------|----------------------------|------------|
| 6" | 5-5/8" | 50 | Non-bearing partitions, low retaining |
| 8" | 7-5/8" | 65 | Standard bearing/shear walls |
| 10" | 9-5/8" | 80 | Taller bearing/shear walls |
| 12" | 11-5/8" | 95 | Tall walls, heavy loads, retaining |

## Fire Ratings (IBC Table 721.1(2))

| Assembly | 1 Hour | 2 Hour | 3 Hour |
|----------|--------|--------|--------|
| 6" CMU (solid grouted) | Yes | No | No |
| 8" CMU (solid grouted) | Yes | Yes | No |
| 10" CMU (solid grouted) | Yes | Yes | Yes |
| 12" CMU (solid grouted) | Yes | Yes | Yes |

*Actual ratings depend on aggregate type, grouting, and equivalent thickness per IBC.*

## Common Errors to Avoid

- Using unreinforced masonry in SDC C or higher without justification
- Forgetting to check out-of-plane bending for in-plane shear walls (biaxial effects)
- Not grouting cells with reinforcement (all reinforced cells must be grouted)
- Insufficient lap splice length for reinforcement
- Not checking slenderness effects for tall walls (h/t > 30)
- Ignoring eccentricity of axial loads (ledger on one side, etc.)
- Inadequate anchorage of diaphragm to masonry walls

## Deliverable Checklist

- [ ] Wall design (in-plane shear, out-of-plane flexure, axial)
- [ ] Lintel design above openings
- [ ] Bond beam design
- [ ] Reinforcement schedule (vertical and horizontal)
- [ ] Grouting requirements
- [ ] Connection/anchorage to diaphragm
- [ ] Foundation design for masonry walls
