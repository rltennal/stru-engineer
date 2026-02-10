# Skill: Calculation Package Standards

## Purpose

This skill defines the standard format, content, and quality requirements for structural calculation packages produced by RaBuilt Engineering. The calculation package is the primary record of engineering design decisions and must be complete, traceable, and stamp-ready.

## Package Structure

```
CALCULATION PACKAGE
Project: [Name]
Project Number: [###]
Date: [Date]
Designed By: [Name, Title]
Checked By: [Name, Title]

TABLE OF CONTENTS

1. Cover Sheet
2. Design Criteria
3. Load Development
4. Gravity System Design
   4.1 Roof Framing
   4.2 Floor Framing
   4.3 Columns / Bearing Walls
5. Lateral System Design
   5.1 Seismic / Wind Parameters
   5.2 Lateral Force Calculation
   5.3 Force Distribution
   5.4 Diaphragm Design
   5.5 Shear Wall / Frame Design
   5.6 Overturning / Hold-Down Design
6. Foundation Design
7. Connection Design
8. Special Conditions
9. Member / Hardware Schedules
10. Appendices (software output, manufacturer data, geotech excerpts)
```

## Cover Sheet Requirements

```
RABUILT ENGINEERING
STRUCTURAL CALCULATIONS

PROJECT: [Name]
PROJECT NUMBER: [###]
LOCATION: [Address, City, State]
CLIENT: [Name]

DESCRIPTION: [Brief project description]

DESIGNED BY: _________________ DATE: _______
CHECKED BY: _________________ DATE: _______
APPROVED BY: _________________ DATE: _______

REVISION LOG:
| Rev | Date | Description | By |
|-----|------|------------|-----|
```

## Design Criteria Section

Every calc package begins with a comprehensive design criteria section:

```
DESIGN CRITERIA

APPLICABLE CODES:
- Building Code: IBC [year] with [jurisdiction] amendments
- Load Standard: ASCE 7-[year]
- Concrete: ACI 318-[year]
- Steel: AISC 360-[year], AISC 341-[year] (if seismic)
- Wood: NDS [year], SDPWS [year]
- Masonry: TMS 402/602-[year]
- Existing Buildings: IEBC [year] (if applicable)

DESIGN METHOD: [ ] ASD  [ ] LRFD  (identify per material)

RISK CATEGORY: [I / II / III / IV]
IMPORTANCE FACTOR: Ie = [value]

LOADS:
Dead:
- Roof: [itemize] = ___ psf
- Floor: [itemize] = ___ psf
- Walls: [material, weight]

Live:
- Floor: ___ psf (occupancy: ___)
- Roof: Lr = ___ psf
- Reducible: [Y/N], basis: ___

Snow:
- pg = ___ psf (source: ___)
- pf = ___ psf (calculated)
- Drift: [applicable locations]

Wind:
- V = ___ mph (Risk Cat. ___)
- Exposure: ___
- Kzt = ___

Seismic:
- SS = ___ g, S1 = ___ g (source: USGS for lat/long)
- Site Class: ___ (source: geotech report dated ___)
- SDS = ___, SD1 = ___
- SDC: ___
- SFRS: ___
- R = ___, Cd = ___, Omega_0 = ___

SOIL:
- Allowable Bearing: ___ psf/ksf (source: geotech report)
- Lateral: Ka = ___, Kp = ___
- Friction: mu = ___

MATERIAL PROPERTIES:
- Concrete: f'c = ___ psi (normal/lightweight)
- Reinforcing: fy = ___ ksi (Grade ___)
- Structural Steel: Fy = ___ ksi (A992/A572/A36)
- Wood: Species = ___, Grade = ___
- Masonry: f'm = ___ psi, Type ___ mortar

DEFLECTION LIMITS:
- Floor LL: L/___
- Floor TL: L/___
- Roof LL: L/___
- Roof TL: L/___
- Lateral drift: H/___
```

## Calculation Format

Each calculation follows the Given → Find → Solution → Check → Summary format:

```
SUBJECT: [Member or element being designed]
REFERENCE: [Drawing sheet, detail, grid location]

GIVEN:
- [Loads, geometry, material, support conditions]

FIND:
- [What is being determined — member size, reinforcement, capacity, etc.]

SOLUTION:
[Step-by-step calculations]
[Code reference at each design decision]
[Clear equation → substitution → result format]

Example:
Mu = wu * L^2 / 8
   = 1.82 klf * (24 ft)^2 / 8
   = 131 k-ft

Required Zx = Mu / (phi * Fy)
            = 131 k-ft * 12 / (0.90 * 50 ksi)
            = 34.9 in^3

Select W16x31 (Zx = 54.0 in^3)

D/C = 131 / (0.90 * 50 * 54.0 / 12) = 0.65  OK

CHECK:
[Independent verification, order-of-magnitude check, or alternative method]

SUMMARY:
[Final selection, key design values, D/C ratio]
USE: W16x31 (D/C = 0.65)
```

## Quality Standards

### Traceability
- Every number must be traceable to a source (code, geotech report, drawing, calculation)
- No "magic numbers" — if a value is used, its origin is documented
- Cross-reference between calculations (e.g., "beam reaction from page 12")

### Units
- US customary: kips, feet, inches, psi, ksi, psf, plf, klf
- Units must be carried through calculations
- Convert units explicitly (not in your head)

### Notation
- Use standard structural engineering notation
- Define non-standard symbols on first use
- Subscripts: u = factored (ultimate), n = nominal, a = allowable, s = service

### Checking
- Every calculation should be independently checkable
- Checker initials and date on each page
- Checker marks: checkmark for verified, "?" for questioned, "X" for error found
- Red/green pen convention (or digital equivalent)

### Software Output
- Software output supplements hand calculations; does not replace them
- Include input summary, model description, and key results
- Verify software results with hand calculation spot-checks
- Note software name and version

## Revision Control

- Revisions marked clearly with revision cloud on drawings, revision number in calcs
- Superseded pages clearly marked "SUPERSEDED" (not discarded)
- Revision log on cover sheet updated
- When revisions affect previously approved work, re-check affected calculations

## Page Numbering and Organization

- Sequential page numbers: Page X of Y
- Each major section can restart numbering (1.1, 1.2, etc.) or use continuous
- Table of contents with page references
- Tab dividers for physical packages (or bookmarks for digital)

## Common Errors to Avoid

- Missing design criteria section
- Calculations that cannot be followed by another engineer
- No cross-references between related calculations
- Missing units on intermediate results
- Software output without verification or context
- No summary of final member sizes
- Missing connection forces (what does the gravity design need from the connection designer?)
- Revision without updating table of contents

## Deliverable Checklist

- [ ] Cover sheet complete with all project information
- [ ] Design criteria comprehensive with all sources cited
- [ ] Load development complete with tributary area diagrams
- [ ] All members designed with D/C ratios
- [ ] Deflection checks complete
- [ ] Connection forces tabulated
- [ ] Foundation design coordinated with geotech report
- [ ] Hardware schedules (hold-downs, hangers, connectors)
- [ ] Member schedules (beams, columns, walls)
- [ ] Software output included with verification
- [ ] Table of contents accurate
- [ ] All pages numbered
- [ ] Checked and signed by checker
- [ ] Ready for PE stamp and signature
