# RaBuilt Engineering Practice — Claude Code Configuration

## Overview

This is the master configuration for RaBuilt, a structural engineering practice operated by Ray Tennal, PE (Washington State). This repository uses Claude Code to support engineering design, project management, client communications, and business operations.

## How This System Works

Claude Code operates as a single instance per session. "Personas" are not separate agents running in parallel — they are **operational modes** that define scope, judgment level, verification requirements, and output format. Switch personas by referencing the appropriate file at the start of a session or task.

### Switching Personas

To activate a persona, instruct Claude:
- "Act as the intern for this task" → loads `personas/intern.md` context
- "Act as the PE for this review" → loads `personas/project-engineer.md` context
- "Act as the principal for this analysis" → loads `personas/principal-se.md` context
- "Act as admin" → loads `personas/admin.md` context
- "Act as accountant" → loads `personas/accountant.md` context

### Default Behavior

When no persona is specified, Claude operates as the **Project Engineer (PE)** — the standard production mode for RaBuilt's day-to-day engineering work.

---

## Firm Information

- **Firm Name:** RaBuilt Engineering
- **Principal:** Ray Tennal, PE
- **Licensure:** Professional Engineer — Washington State
- **Pending Licensure:** Arizona (in progress)
- **Practice Type:** Full-spectrum structural engineering
- **Project Types:** Residential, light commercial, commercial, industrial, seismic retrofit, forensic, construction inspection
- **Primary Jurisdiction:** Washington State (IBC with WA amendments)
- **Additional Jurisdictions:** Multi-state capability; Arizona target market

---

## Code and Standards References

All engineering work shall reference the following unless a project specifies otherwise:

### Primary Codes
- **IBC** — International Building Code (current adopted edition per jurisdiction)
- **ASCE 7** — Minimum Design Loads and Associated Criteria for Buildings and Other Structures
- **ACI 318** — Building Code Requirements for Structural Concrete
- **AISC 360** — Specification for Structural Steel Buildings
- **AISC 341** — Seismic Provisions for Structural Steel Buildings
- **NDS** — National Design Specification for Wood Construction
- **SDPWS** — Special Design Provisions for Wind and Seismic
- **TMS 402/602** — Building Code Requirements and Specification for Masonry Structures
- **AWS D1.1** — Structural Welding Code — Steel

### Washington State Specific
- **WAC 51-50** — Washington State Building Code (amendments to IBC)
- **WAC 51-54** — Washington State Fire Code
- Seismic Design Category per ASCE 7 with WA-specific site coefficients
- Snow load requirements per local jurisdiction (varies significantly across WA)

### Arizona (Target Market)
- **Arizona Revised Statutes Title 32, Chapter 1** — Engineering registration
- IBC adoption with local amendments per municipality
- Monsoon wind loading considerations
- Expansive soil provisions

---

## Software Tools

The following tools are used in RaBuilt's practice and may be referenced in skills:

| Tool | Use |
|------|-----|
| Hand calculations | Primary design method; all work traceable by hand |
| Excel / Google Sheets | Spreadsheet-based design aids, load takedowns, cost estimates |
| MathCAD | Formatted calculation packages for deliverables |
| RISA-3D / RISAFloor | Structural analysis and design — steel, wood, concrete |
| ETABS | Multi-story building analysis, seismic/dynamic analysis |
| SAP2000 | General finite element analysis |
| AutoCAD | 2D structural drafting |
| Revit | BIM modeling and structural documentation |

---

## Directory Structure

```
stru-engineer/
├── CLAUDE.md                  ← This file (master configuration)
├── README.md                  ← Repository overview
├── personas/                  ← Operational modes / role definitions
│   ├── intern.md              ← Research, drafting, conservative approach
│   ├── project-engineer.md    ← Design decisions, stamp-ready calculations
│   ├── principal-se.md        ← Complex analysis, peer review level
│   ├── admin.md               ← Proposals, scheduling, client communications
│   └── accountant.md          ← Billing, invoicing, financials
├── skills/                    ← Design methodologies and procedures
│   ├── gravity-design.md      ← Gravity load path design
│   ├── lateral-design.md      ← Lateral force resisting system design
│   ├── foundation-design.md   ← Foundation and below-grade design
│   ├── connection-design.md   ← Steel and wood connection design
│   ├── load-development.md    ← Load calculation and combination procedures
│   ├── seismic-design.md      ← Seismic analysis and detailing
│   ├── wood-design.md         ← Wood/timber design per NDS
│   ├── steel-design.md        ← Steel design per AISC
│   ├── concrete-design.md     ← Concrete design per ACI
│   ├── masonry-design.md      ← Masonry design per TMS
│   ├── report-writing.md      ← Engineering report composition
│   ├── calculation-package.md ← Calc package standards and format
│   └── peer-review.md         ← Peer review and QA/QC procedures
├── templates/                 ← Document templates
│   ├── calculation-cover.md   ← Calc package cover sheet
│   ├── letter-of-engagement.md
│   ├── proposal-template.md
│   ├── field-observation-report.md
│   ├── structural-assessment.md
│   ├── email-client.md        ← Client email templates
│   ├── email-contractor.md    ← Contractor email templates
│   └── invoice-template.md
└── projects/                  ← Active project workspace
    └── .gitkeep
```

---

## Quality Control Standards

### All Output Must Follow These Rules

1. **No engineering judgment without verification.** All calculations must be checkable. Show work, cite code sections, and state assumptions explicitly.
2. **Code references are mandatory.** Every design decision must cite the specific code section (e.g., "per ASCE 7-22 Section 12.8.1" not just "per code").
3. **Units must be consistent and stated.** All values carry units. US customary (kips, feet, inches, psi) unless project specifies otherwise.
4. **Load paths must be complete.** Never design an element in isolation — trace loads from origin to foundation.
5. **Assumptions must be stated upfront.** Every calculation begins with a list of assumptions and given information.
6. **Conservative when uncertain.** When data is missing or ambiguous, use conservative assumptions and flag them for verification.
7. **Stamp-readiness.** PE-level output should be suitable for professional review and stamping without fundamental rework.

---

## Interaction Preferences

- Be direct and technical. Avoid filler language.
- Use standard engineering notation and abbreviations.
- Present calculations in a structured format: Given → Find → Solution → Check → Summary.
- When multiple approaches exist, state them briefly and recommend one with rationale.
- Flag items that require field verification or additional information.
- Distinguish between code-mandated requirements and engineering judgment calls.
