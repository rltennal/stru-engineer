# Skill: Peer Review and QA/QC Procedures

## Purpose

This skill covers the peer review and quality assurance/quality control (QA/QC) processes used at RaBuilt Engineering. Peer review is both an internal process (self-review and checking) and an external service offered to clients and other firms.

## Internal QA/QC

### Three Levels of Review

**Level 1 — Self-Check (Designer)**
- Performed by the engineer who prepared the work
- Before submitting for independent review
- Checklist-based verification

**Level 2 — Independent Check (Checker)**
- Performed by a different engineer (or the Principal reviewing intern/PE work)
- Verify inputs, methodology, calculations, and conclusions
- Mark-up with initials and date

**Level 3 — Back-Check (Designer responds to checker)**
- Designer addresses all checker comments
- Confirm corrections or provide justification for original approach
- Final reconciliation before sealing

### Self-Check Procedures (Level 1)

Before submitting any calculation or report for review:

**General:**
- [ ] All assumptions stated and reasonable
- [ ] Design criteria complete and sourced
- [ ] Load combinations correct for design method (ASD vs. LRFD)
- [ ] Units consistent throughout
- [ ] All code references accurate and current
- [ ] Cross-references between calculations verified
- [ ] Summary tables match detailed calculations
- [ ] No "TODO" or placeholder items remaining

**Gravity System:**
- [ ] Tributary areas correct (sketch included)
- [ ] Dead loads itemized with sources
- [ ] Live load reductions applied correctly (or documented as not applicable)
- [ ] All members checked for flexure, shear, deflection
- [ ] D/C ratios reasonable (0.50-0.95 range)
- [ ] Bearing checks at all supports
- [ ] Reactions documented for connection design

**Lateral System:**
- [ ] Seismic parameters verified against USGS data
- [ ] Wind parameters verified against ASCE 7 maps
- [ ] SFRS selection documented with code reference
- [ ] Irregularity checks performed
- [ ] Base shear calculation complete with all checks (min Cs, etc.)
- [ ] Force distribution to vertical elements documented
- [ ] Drift checks at all stories
- [ ] Diaphragm design including collectors
- [ ] Overturning and hold-down design complete to foundation
- [ ] Redundancy factor determined

**Foundations:**
- [ ] Geotech report data cited with page/section references
- [ ] Service loads used for bearing check
- [ ] Factored loads used for concrete design
- [ ] One-way and two-way shear checked
- [ ] Reinforcement development length verified
- [ ] Retaining wall stability (OT, sliding, bearing) all satisfied

**Connections:**
- [ ] All failure modes checked
- [ ] Seismic overstrength applied where required
- [ ] Hardware specifications complete (manufacturer, model, fastener schedule)
- [ ] Constructability considered

### Independent Check Procedures (Level 2)

The checker should NOT just verify the designer's math step-by-step. The checker should:

1. **Verify scope:** Are all required elements addressed?
2. **Check design criteria:** Are inputs correct? Sources verified?
3. **Independent spot-checks:** Pick key elements and verify independently (not by tracing designer's steps)
4. **Reasonableness:** Do results make sense? Compare against rules of thumb and past experience.
5. **Code compliance:** Are all applicable code provisions addressed?
6. **Completeness:** Are connection forces, reactions, and boundary conditions all resolved?
7. **Constructability:** Can this be built as designed?
8. **Documentation:** Is the calc package clear enough that another engineer could follow it?

### Marking Convention
- Green check (✓): Verified, correct
- Yellow question (?): Needs clarification or minor issue
- Red X (✗): Error found, must be corrected
- Circle: Calculation spot-checked independently by checker

## External Peer Review Services

### Scope Definition
When retained for external peer review:

1. **Define scope clearly in writing** — what is being reviewed, what is NOT
2. **Establish basis:** review against specific code editions, loading criteria, etc.
3. **Define standard of review:**
   - Conceptual review: overall approach and system selection
   - Detailed review: verify specific calculations and code compliance
   - Comprehensive review: independent analysis to verify results
4. **Deliverable:** Written review letter with findings, categorized by severity

### Review Comment Categories

**Critical — Must be addressed before construction:**
- Code violation affecting safety
- Incorrect load path
- Missing design element
- Capacity below demand

**Major — Should be addressed:**
- Conservative or unconservative assumption that significantly affects design
- Incomplete documentation
- Missing code check that could govern

**Minor — Recommended to address:**
- Formatting or organizational issues
- Minor conservatism or clarification needed
- Improved presentation

**Informational:**
- Suggestions for future consideration
- Alternative approaches that may be more efficient
- Notes for the record

### Review Letter Format

```
RABUILT ENGINEERING
PEER REVIEW LETTER

TO: [Engineer of Record]
FROM: Ray Tennal, PE — RaBuilt Engineering
DATE: [Date]
RE: Peer Review — [Project Name]

SCOPE OF REVIEW:
[What was reviewed, document dates/revisions, criteria]

DOCUMENTS REVIEWED:
1. [Structural calculations dated ___]
2. [Structural drawings S1-S10 dated ___]
3. [Geotechnical report dated ___]

SUMMARY:
[Overall assessment — acceptable as-is, acceptable with corrections, requires revision]

FINDINGS:

1. [CRITICAL] [Description of finding]
   Reference: [Drawing/calc page, code section]
   Recommendation: [What should be done]

2. [MAJOR] [Description of finding]
   Reference: [Drawing/calc page, code section]
   Recommendation: [What should be done]

[Continue for all findings]

CONCLUSION:
[Overall assessment and conditions for acceptance]

[Signature block]
```

## Plan Review Response

When responding to building department plan review comments:

1. Read each comment carefully — understand what the reviewer is asking
2. Respond to every comment (do not skip any)
3. Format: restate comment, provide response with reference to revised sheet/calc page
4. Be professional and non-defensive
5. If you disagree with a comment, cite the specific code basis for your position
6. Provide revised sheets/calculations marked with revision clouds

### Response Format
```
PLAN REVIEW RESPONSE

Project: [Name]
Permit #: [Number]
Review Date: [Date]
Response Date: [Date]

Comment 1: [Restate reviewer's comment]
Response: [Your response with references to revised documents]

Comment 2: [Restate reviewer's comment]
Response: [Your response]

[Continue for all comments]

Revised documents attached:
- Structural calculations Rev. [X] dated [date]
- Structural drawings S1-S10 Rev. [X] dated [date]
```

## Common Review Findings

Based on typical plan review and peer review experience:

1. Missing or incomplete design criteria
2. Snow drift loads not addressed
3. Collector design missing or insufficient for Omega_0 forces
4. Hold-down load path incomplete (doesn't reach foundation)
5. Diaphragm design not documented
6. Deflection criteria not verified for critical elements
7. Foundation design not coordinated with geotech report
8. Connection forces not documented between elements
9. Seismic detailing requirements not shown on drawings
10. Inadequate documentation of engineering judgment decisions

## Deliverable Checklist

### For Internal QA/QC
- [ ] Self-check completed by designer
- [ ] Independent check completed by reviewer
- [ ] All review comments resolved (back-check)
- [ ] Final package assembled and stamped

### For External Peer Review
- [ ] Scope of review defined and agreed
- [ ] All provided documents reviewed
- [ ] Findings categorized and documented
- [ ] Review letter prepared and signed
- [ ] Follow-up on responses to critical/major findings
