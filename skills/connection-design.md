# Skill: Connection Design

## Purpose

This skill covers the design of structural connections — the critical links that transfer forces between members. A structure is only as strong as its connections. This covers steel, wood, and concrete-to-steel connections.

## Principles

1. **Load path continuity.** Every force has a path; every path needs a connection.
2. **Ductility.** Connections should be at least as strong as the weaker member (seismic) or clearly designed for the demand.
3. **Constructability.** Design connections that can be fabricated and erected in the field.
4. **Clarity.** Connection details must be unambiguous on drawings.

## Steel Connections

### Simple Shear Connections

#### Single Plate (Shear Tab)
- Plate welded to column/girder, bolted to beam web
- Design checks: bolt shear, bolt bearing, plate shear yielding, plate shear rupture, plate block shear, weld, beam web bearing/coping
- Plate thickness: typically 1/4" to 1/2"
- Standard bolt gage: 3" from weld line
- Eccentricity: consider for bolt group design

#### Double Angle
- Two angles bolted or welded to beam web and to support
- Design checks: bolt shear (both legs), angle shear, bearing, block shear
- Typically L4x3-1/2 or L3-1/2x3-1/2

#### End Plate (Shear)
- Plate welded to beam end, bolted to support
- Similar checks to single plate

### Moment Connections

#### Extended End Plate (AISC 358)
- Prequalified for SMF and IMF
- Plate extends beyond beam flanges
- Bolts in tension transfer flange forces
- Design per AISC 358 Chapter 6

#### Directly Welded Flange
- CJP welds at beam flanges to column flange
- Web connection for shear (bolted or welded)
- Access holes required per AISC 360 J1.6
- Demand-critical welds per AISC 341

#### Bolted Flange Plate
- Plates welded to column, bolted to beam flanges
- Web connection for shear
- Prequalified per AISC 358 Chapter 7

### Brace Connections (Gusset Plates)

#### Design Procedure
1. Determine brace force (tension and compression)
2. Size gusset plate: Whitmore section for tension yielding/rupture
3. Check gusset compression (buckling): Thornton method — average of three corner lengths
4. Design weld or bolt group: brace to gusset
5. Design interface welds: gusset to beam, gusset to column
6. Check frame forces at gusset interfaces (beam shear, column axial)
7. For SCBF: design for expected brace strength (Ry*Fy*Ag in tension, 1.14*Ry*Fcre*Ag in compression)
8. Provide 2tp clearance for brace buckling (SCBF)

#### Whitmore Section
- Width: bw = 2*L*tan(30°) + w_connection (L = gusset length from first bolt to last bolt or weld length)
- Tension yielding: phi*Pn = 0.90 * Fy * bw * tp
- Tension rupture: phi*Pn = 0.75 * Fu * An (net of bolt holes)

#### Block Shear (AISC 360 J4.3)
- Rn = 0.60*Fu*Anv + Ubs*Fu*Ant ≤ 0.60*Fy*Agv + Ubs*Fu*Ant
- Check at all possible failure planes

### Bolt Group Analysis (Eccentrically Loaded)
- **In-plane eccentricity:** Instantaneous Center of Rotation method (AISC Manual Tables 7-7 through 7-14) or elastic method
- **Out-of-plane eccentricity (prying):** Check per AISC Manual Part 9

### Weld Design Summary

| Weld Type | Strength | Phi |
|-----------|----------|-----|
| Fillet (shear on throat) | 0.60*FEXX | 0.75 |
| CJP (tension/compression) | Same as base metal | 0.90 |
| CJP (shear) | 0.60*FEXX | 0.80 |
| PJP (compression) | Same as base metal | 0.90 |
| PJP (tension) | 0.60*FEXX | 0.75 |

## Wood Connections

### Dowel-Type Fasteners (NDS Chapter 12)

#### Yield Limit Equations
- NDS provides yield limit equations for 4 yield modes (single shear) and 4 modes (double shear)
- Lateral design value Z based on minimum from all modes
- Adjust: Z' = Z * (CD * CM * Ct * Cg * Cdelta * Ceg * Cdi * Ctn)

#### Bolt Design
- Minimum spacing (parallel to grain): 4D (tension), 3D (compression)
- Minimum end distance (parallel to grain): 7D (tension), 4D (compression)
- Minimum edge distance: depends on l/D ratio
- Group action factor (Cg) for rows of bolts: NDS Table 12.3.6

#### Nail Design
- Pre-drilling required for: hardwoods, near ends/edges, or large nails in small members
- Toe-nailing reduction: Ctn = 0.83
- End grain factor: Ceg = 0.67
- Diaphragm nail factor: Cdi = 1.1 (for diaphragm nails only)

### Metal Plate Connectors (Simpson Strong-Tie, USP)

#### Design Philosophy
- Manufacturer publishes allowable loads per ICC-ES evaluation report
- Verify: correct load direction, member species, fastener type, installation requirements
- Adjust for load duration (CD) — most published values are for normal duration
- Do NOT adjust for already-included factors (read evaluation report)

#### Common Hardware Connections

**Joist to Beam/Wall:**
- Joist hangers: face mount (LUS, HUS) or top-mount (HIT, MIT)
- Verify: joist depth, load capacity, nail/screw schedule, minimum bearing

**Hold-Downs:**
- Simpson HDU, HHDQ, PHD series
- Capacity ranges from 3,000 lbs to 25,000+ lbs
- Anchorage: embedded anchor bolt, expansion anchor, or epoxy anchor
- Pre-deflection: account for take-up in overturning calculations (1/8" to 1/4" typical)

**Straps and Ties:**
- Tension continuity across joints
- Simpson LSTA, MSTA, CMST
- Verify: embedment, nailing both sides, kink/bend effects on capacity

**Post Bases:**
- Simpson ABU, CBS, ABA
- Uplift and lateral capacity
- Standoff vs. concealed vs. surface-mount

## Concrete Anchorage (ACI 318 Chapter 17)

### Cast-in-Place Anchors

#### Tension
1. **Steel strength:** Nsa = Ase,N * futa (phi = 0.75)
2. **Concrete breakout:** Ncbg = (ANc/ANco) * psi_ed,N * psi_c,N * psi_cp,N * Nb (phi = 0.70 or 0.75)
   - Nb = kc * sqrt(f'c) * hef^1.5
   - Breakout cone: 35-degree from anchor head, projected area method
3. **Pullout:** Npn = psi_c,P * Np (phi = 0.70 or 0.75)
   - Np = 8*Abrg*f'c (headed bolt)
4. **Side-face blowout:** For anchors near an edge (ca1 < 0.4*hef)

#### Shear
1. **Steel strength:** Vsa = 0.6 * Ase,V * futa (phi = 0.65)
2. **Concrete breakout:** Vcbg = (AVc/AVco) * psi_ed,V * psi_c,V * psi_h,V * Vb
3. **Concrete pryout:** Vcp = kcp * Ncbg (phi = 0.70 or 0.75)

#### Combined Tension and Shear
- If Nua/(phi*Nn) ≤ 0.2: full shear strength
- If Vua/(phi*Vn) ≤ 0.2: full tension strength
- Otherwise: Nua/(phi*Nn) + Vua/(phi*Vn) ≤ 1.2

### Post-Installed Anchors
- Must comply with ACI 355.2 (mechanical) or ACI 355.4 (adhesive)
- Design per manufacturer ICC-ES evaluation report
- Adhesive anchors: additional sustained load requirements (ACI 318 17.5.2.2)
- Cracked vs. uncracked concrete factors

## Common Errors to Avoid

- Not checking all failure modes (steel, connection, member)
- Forgetting block shear in steel connections
- Not applying group action factor for multi-bolt wood connections
- Using manufacturer capacities without checking adjustment factors
- Ignoring prying action on bolts loaded in tension
- Not checking concrete anchorage breakout for anchors near edges
- Designing connections for less than required overstrength (Omega_0) in seismic
- Specifying connections that cannot be constructed in the field (access, clearance)
- Not coordinating connection forces between members

## Deliverable Checklist

- [ ] Connection forces clearly stated (type, magnitude, direction)
- [ ] All failure modes checked
- [ ] Bolt/nail/weld schedules
- [ ] Hardware specifications (manufacturer, model, evaluation report)
- [ ] Detail drawings showing dimensions, fasteners, edge distances
- [ ] Seismic requirements addressed (overstrength, ductile detailing)
- [ ] Constructability review
