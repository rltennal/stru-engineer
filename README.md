# RaBuilt Engineering — Claude Code Practice Management

Structural engineering practice management system powered by Claude Code. This repository contains personas, skills, and templates for operating a one-person structural engineering firm.

## Quick Start

1. Open this directory in Claude Code
2. Claude reads `CLAUDE.md` automatically for configuration
3. Activate a persona: *"Act as the PE for this task"*
4. Reference skills: *"Use the seismic design skill for this analysis"*
5. Use templates: *"Draft a proposal using the proposal template"*

## Structure

```
├── CLAUDE.md              Master configuration — roles, standards, quality rules
├── personas/              Operational modes (hats Claude wears)
│   ├── intern.md          Research, drafting, conservative — all flagged for review
│   ├── project-engineer.md  Design decisions, stamp-ready output (DEFAULT)
│   ├── principal-se.md    Complex analysis, peer review, final authority
│   ├── admin.md           Proposals, scheduling, client communications
│   └── accountant.md      Billing, invoicing, financial tracking
├── skills/                Engineering methodology references
│   ├── load-development.md    Load calculation and combinations (ASCE 7)
│   ├── gravity-design.md      Gravity load path design
│   ├── lateral-design.md      Lateral force resisting system design
│   ├── seismic-design.md      Seismic analysis and detailing
│   ├── wood-design.md         Wood/timber design (NDS/SDPWS)
│   ├── steel-design.md        Steel design (AISC 360/341)
│   ├── concrete-design.md     Reinforced concrete design (ACI 318)
│   ├── masonry-design.md      Masonry design (TMS 402)
│   ├── foundation-design.md   Foundation and below-grade design
│   ├── connection-design.md   Steel, wood, and anchorage connections
│   ├── report-writing.md      Engineering report composition
│   ├── calculation-package.md Calc package standards and format
│   └── peer-review.md         QA/QC and peer review procedures
├── templates/             Document templates
│   ├── calculation-cover.md
│   ├── letter-of-engagement.md
│   ├── proposal-template.md
│   ├── field-observation-report.md
│   ├── structural-assessment.md
│   ├── email-client.md
│   ├── email-contractor.md
│   └── invoice-template.md
└── projects/              Active project workspace
```

## Personas

| Persona | When to Use |
|---------|-------------|
| **Intern** | Research, preliminary calcs, drafting — everything flagged for PE review |
| **Project Engineer** | Day-to-day design work, stamp-ready calcs, client communication (default) |
| **Principal SE** | Complex analysis, peer review, final approval, forensic work |
| **Admin** | Proposals, contracts, scheduling, project tracking, marketing |
| **Accountant** | Invoicing, AR tracking, expense management, tax prep support |

## Firm Details

- **Principal:** Ray Tennal, PE
- **Licensure:** Washington State PE (Arizona in progress)
- **Practice:** Full-spectrum structural — residential through commercial/industrial
- **Primary Codes:** IBC, ASCE 7, ACI 318, AISC 360/341, NDS/SDPWS, TMS 402
