"""
Schedule generator — auto-sizes heel length and produces a wall schedule.

Given a design criteria JSON, generates a retaining wall schedule for
multiple retained heights.  For each height/thickness combination:
  1. Iterates heel length to find the minimum that satisfies all three
     stability checks (overturning, sliding, bearing).
  2. Runs the full ACI 318-19 structural design on that geometry.
  3. Collects results into a tabular schedule.

Thickness rules:
  - Heights < 10 ft: stem and base limited to 8″ (constant section).
  - Heights >= 10 ft: provide options for 8″ and 10″ walls.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from retaining_wall.criteria import DesignCriteria, ExposureConditions
from retaining_wall.designer import WallDesigner, DesignReport


# ---------------------------------------------------------------------------
# Schedule entry
# ---------------------------------------------------------------------------

@dataclass
class ScheduleEntry:
    """One row in the wall schedule."""
    wall_mark: str
    retained_height_ft: float
    stem_top_in: float
    stem_bot_in: float
    base_thickness_in: float
    toe_ft: float
    heel_ft: float
    base_width_ft: float
    # Stability
    fs_overturning: Optional[float]
    fs_sliding: Optional[float]
    q_max_psf: Optional[float]
    q_allow_psf: Optional[float]
    bearing_status: str
    # Stem reinforcing
    stem_bar: str
    stem_spacing_in: Optional[float]
    stem_Mu: float
    stem_phi_Mn: float
    stem_Vu: float
    stem_phi_Vc: float
    # Heel reinforcing
    heel_bar: str
    heel_spacing_in: Optional[float]
    # Toe reinforcing
    toe_bar: str
    toe_spacing_in: Optional[float]
    # T&S steel
    ts_steel_in2ft: float
    # Development
    stem_ld_in: float
    stem_ldh_in: float
    # Status flags
    stability_ok: bool
    structural_ok: bool
    overall_ok: bool
    notes: str = ""


def _build_criteria_for_height(
    height_ft: float,
    heel_ft: float,
    stem_top_in: float,
    stem_bot_in: float,
    base_in: float,
    toe_ft: float,
    embedment_ft: float,
    slope_deg: float,
    criteria_base: dict,
) -> DesignCriteria:
    """Build a DesignCriteria object for a specific height/heel combination."""
    soil = criteria_base["soil"]
    water = criteria_base["water"]
    surcharge = criteria_base["surcharge"]
    seismic = criteria_base["seismic"]
    materials = criteria_base["materials"]
    exposure_data = criteria_base["exposure"]
    stab = criteria_base["stability_factors"]

    return DesignCriteria(
        retained_height_ft=height_ft,
        stem_thickness_top_in=stem_top_in,
        stem_thickness_bot_in=stem_bot_in,
        base_toe_ft=toe_ft,
        base_heel_ft=heel_ft,
        base_thickness_in=base_in,
        backfill_slope_deg=slope_deg,
        embedment_ft=embedment_ft,
        backfill_gamma_pcf=soil["backfill_gamma_pcf"],
        backfill_phi_deg=soil["backfill_phi_deg"],
        backfill_cohesion_psf=soil.get("cohesion_psf", 0),
        soil_condition=soil.get("condition", "active"),
        mu_sliding=soil.get("mu_sliding", 0.45),
        allowable_bearing_psf=soil.get("allowable_bearing_psf"),
        passive_permitted=soil.get("passive_permitted", False),
        passive_gamma_pcf=soil.get("passive_gamma_pcf"),
        passive_phi_deg=soil.get("passive_phi_deg"),
        gwl_depth_ft=water.get("gwl_depth_ft"),
        drainage_provided=water.get("drainage_provided", False),
        surcharge_psf=surcharge.get("uniform_psf", 0),
        sdc=seismic.get("sdc", ""),
        sds=seismic.get("sds", 0),
        sd1=seismic.get("sd1", 0),
        kh=seismic.get("kh", 0),
        kv=seismic.get("kv", 0),
        use_mononobe_okabe=seismic.get("use_mononobe_okabe", False),
        fc_psi=materials.get("fc_psi", 3000),
        gamma_conc_pcf=materials.get("gamma_conc_pcf", 150),
        rebar_max_bar_size=materials.get("rebar_max_bar_size", 6),
        exposure=ExposureConditions(
            freeze_thaw=exposure_data.get("freeze_thaw", ""),
            sulfate=exposure_data.get("sulfate", ""),
            corrosion=exposure_data.get("corrosion", ""),
        ),
        fs_overturning=stab.get("fs_overturning", 1.5),
        fs_sliding=stab.get("fs_sliding", 1.5),
    )


def _check_design_ok(report: DesignReport) -> bool:
    """Return True if all stability and structural checks pass."""
    stab_ok = all(
        r.status == "OK"
        for r in report.stability
        if r.status != "INCOMPLETE"
    )
    struct_ok = all(
        s.bar is not None and s.flexure_ok and s.shear_ok
        for s in report.sections
    )
    return stab_ok and struct_ok


def auto_size_heel(
    height_ft: float,
    stem_top_in: float,
    stem_bot_in: float,
    base_in: float,
    toe_ft: float,
    embedment_ft: float,
    slope_deg: float,
    criteria_base: dict,
    heel_min_ft: float = 1.5,
    heel_max_ft: float = 10.0,
    heel_step_ft: float = 0.25,
    toe_max_ft: float = 3.0,
    toe_step_ft: float = 0.5,
    allow_ftg_thickening: bool = True,
) -> tuple[float, float, float, DesignReport]:
    """Find the minimum heel/toe/footing that satisfies all checks.

    Sizing strategy (in order):
      1. Iterate heel length at the given toe and footing thickness.
      2. If no heel works, increase toe (more weight helps sliding).
      3. If still no solution, increase footing thickness by 2″ increments
         (improves heel shear capacity).

    Returns (heel_ft, toe_ft_used, base_in_used, report).
    """
    ftg_thicknesses = [base_in]
    if allow_ftg_thickening:
        # Try thicker footings in 2″ increments.
        # For taller walls (10–12 ft), allow footings up to ~1.5×H + 2″
        # so the heel slab has adequate shear/flexure capacity.
        max_ftg = max(int(stem_bot_in) + 6, int(height_ft * 2))
        max_ftg = min(max_ftg, 24)  # hard cap at 24″
        for t in range(int(base_in) + 2, max_ftg + 1, 2):
            if t >= 8:
                ftg_thicknesses.append(float(t))

    best_result = None  # (heel, toe, base_t, report)

    for base_t in ftg_thicknesses:
        toe_try = toe_ft
        while toe_try <= toe_max_ft:
            heel = heel_min_ft
            while heel <= heel_max_ft:
                criteria = _build_criteria_for_height(
                    height_ft, heel, stem_top_in, stem_bot_in, base_t,
                    toe_try, embedment_ft, slope_deg, criteria_base,
                )
                report = WallDesigner(criteria).run()
                best_result = (heel, toe_try, base_t, report)

                if _check_design_ok(report):
                    return heel, toe_try, base_t, report

                heel += heel_step_ft
            toe_try += toe_step_ft

    # Return the last attempt even if it doesn't fully pass
    return best_result


def _extract_schedule_entry(
    mark: str,
    height_ft: float,
    stem_top_in: float,
    stem_bot_in: float,
    base_in: float,
    heel_ft: float,
    report: DesignReport,
) -> ScheduleEntry:
    """Extract a ScheduleEntry from a completed DesignReport."""
    wall = report.wall

    # Stability results
    ot = next((r for r in report.stability if r.check == "Overturning"), None)
    sl = next((r for r in report.stability if r.check == "Sliding"), None)
    br = next((r for r in report.stability if r.check == "Bearing"), None)

    fs_ot = ot.fs if ot else None
    fs_sl = sl.fs if sl else None
    q_max = br.demand if br else None
    q_allow = br.capacity if br else None
    br_status = br.status if br else "N/A"

    # Section results
    stem_sec = next((s for s in report.sections if "stem" in s.location), None)
    heel_sec = next((s for s in report.sections if "heel" in s.location), None)
    toe_sec = next((s for s in report.sections if "toe" in s.location), None)

    def _bar_label(sec):
        return sec.bar.label if sec and sec.bar else "—"

    def _spacing(sec):
        return sec.spacing_in if sec and sec.spacing_in else None

    # T&S
    from retaining_wall.structural import min_temp_shrinkage_steel
    ts = min_temp_shrinkage_steel(stem_bot_in)

    # Development lengths
    stem_ld = report.development_lengths.get("stem_base", 0)
    stem_ldh = report.development_lengths.get("stem_base (hook)", 0)

    stab_ok = all(r.status == "OK" for r in report.stability if r.status != "INCOMPLETE")
    struct_ok = all(s.flexure_ok and s.shear_ok for s in report.sections if s.bar is not None)

    return ScheduleEntry(
        wall_mark=mark,
        retained_height_ft=height_ft,
        stem_top_in=stem_top_in,
        stem_bot_in=stem_bot_in,
        base_thickness_in=base_in,
        toe_ft=wall.base.toe_ft if wall else 0,
        heel_ft=heel_ft,
        base_width_ft=wall.base_width_ft if wall else 0,
        fs_overturning=fs_ot,
        fs_sliding=fs_sl,
        q_max_psf=q_max,
        q_allow_psf=q_allow,
        bearing_status=br_status,
        stem_bar=_bar_label(stem_sec),
        stem_spacing_in=_spacing(stem_sec),
        stem_Mu=stem_sec.Mu_lbft if stem_sec else 0,
        stem_phi_Mn=stem_sec.phi_Mn if stem_sec else 0,
        stem_Vu=stem_sec.Vu_lb if stem_sec else 0,
        stem_phi_Vc=stem_sec.phi_Vc if stem_sec else 0,
        heel_bar=_bar_label(heel_sec),
        heel_spacing_in=_spacing(heel_sec),
        toe_bar=_bar_label(toe_sec),
        toe_spacing_in=_spacing(toe_sec),
        ts_steel_in2ft=ts,
        stem_ld_in=stem_ld,
        stem_ldh_in=stem_ldh,
        stability_ok=stab_ok,
        structural_ok=struct_ok,
        overall_ok=stab_ok and struct_ok and all(
            s.bar is not None for s in report.sections
        ),
    )


# ---------------------------------------------------------------------------
# Generate full schedule
# ---------------------------------------------------------------------------

def generate_schedule(criteria_path: str | Path) -> tuple[list[ScheduleEntry], list[DesignReport]]:
    """Generate the retaining wall schedule from a criteria JSON file.

    Returns (schedule_entries, design_reports).
    """
    criteria_path = Path(criteria_path)
    with open(criteria_path) as f:
        data = json.load(f)

    sched_cfg = data["schedule"]
    heights = sched_cfg["heights_ft"]
    toe_ft = sched_cfg.get("toe_ft", 1.0)
    embedment_ft = sched_cfg.get("embedment_ft", 1.0)
    slope_deg = sched_cfg.get("backfill_slope_deg", 0)
    thick_rules = sched_cfg["thickness_rules"]

    entries: list[ScheduleEntry] = []
    reports: list[DesignReport] = []
    wall_num = 1

    for h in heights:
        if h < 10:
            # Single thickness option
            rule = thick_rules["below_10ft"]
            configs = [(rule["stem_top_in"], rule["stem_bot_in"], rule["base_in"], "")]
        else:
            # Multiple thickness options
            options = thick_rules["at_or_above_10ft"]
            configs = [
                (opt["stem_top_in"], opt["stem_bot_in"], opt["base_in"], opt.get("label", ""))
                for opt in options
            ]

        for stem_top, stem_bot, base_t, label in configs:
            mark = f"W{wall_num}"
            if label:
                mark = f"W{wall_num} ({label})"

            heel_ft, toe_used, base_used, report = auto_size_heel(
                height_ft=h,
                stem_top_in=stem_top,
                stem_bot_in=stem_bot,
                base_in=base_t,
                toe_ft=toe_ft,
                embedment_ft=embedment_ft,
                slope_deg=slope_deg,
                criteria_base=data,
            )

            entry = _extract_schedule_entry(
                mark, h, stem_top, stem_bot, base_used, heel_ft, report,
            )
            notes_parts = []
            if base_used > base_t:
                notes_parts.append(
                    f"Footing thickened to {base_used:.0f}\" "
                    f"(requested {base_t:.0f}\" insufficient for heel shear)"
                )
            if toe_used > toe_ft:
                notes_parts.append(f"Toe increased to {toe_used:.1f} ft for sliding")
            if not entry.overall_ok:
                notes_parts.append("DESIGN DOES NOT PASS")
            entry.notes = "; ".join(notes_parts)

            entries.append(entry)
            reports.append(report)
            wall_num += 1

    return entries, reports


# ---------------------------------------------------------------------------
# Formatted output
# ---------------------------------------------------------------------------

def format_schedule_table(entries: list[ScheduleEntry], project_data: dict) -> str:
    """Format the schedule entries into a readable text table."""
    proj = project_data.get("project", {})
    soil = project_data.get("soil", {})
    surcharge = project_data.get("surcharge", {})
    codes = project_data.get("codes", {})

    lines: list[str] = []
    lines.append("=" * 120)
    lines.append(f"RETAINING WALL SCHEDULE — {proj.get('name', 'Project')}")
    lines.append(f"Project No: {proj.get('number', '')}    Date: {proj.get('date', '')}")
    lines.append(f"Designer: {proj.get('designer', '')}")
    lines.append("=" * 120)
    lines.append("")
    lines.append("DESIGN BASIS:")
    lines.append(f"  Codes: {codes.get('building_code', '')} / {codes.get('concrete_code', '')}")
    lines.append(f"  {codes.get('residential_note', '')}")
    lines.append(f"  Backfill: gamma = {soil.get('backfill_gamma_pcf')} pcf, "
                 f"phi = {soil.get('backfill_phi_deg')} deg, "
                 f"condition = {soil.get('condition', 'active')}")
    lines.append(f"  Allowable bearing = {soil.get('allowable_bearing_psf')} psf   "
                 f"mu (sliding) = {soil.get('mu_sliding')}")
    lines.append(f"  Surcharge = {surcharge.get('uniform_psf', 0)} psf uniform")
    lines.append(f"  Drainage: {'Provided' if project_data.get('water', {}).get('drainage_provided') else 'NOT provided — check hydrostatic'}")
    lines.append(f"  f'c = {project_data.get('materials', {}).get('fc_psi', 3000)} psi, "
                 f"Rebar: #4 Gr.40 / #5 Gr.60, max bar = #{project_data.get('materials', {}).get('rebar_max_bar_size', 6)}")
    lines.append(f"  FS required: overturning >= 1.5, sliding >= 1.5")
    lines.append("")

    # Table header
    hdr1 = (
        f"{'Mark':<22s} {'H':>4s}  {'t_top':>5s} {'t_bot':>5s} {'t_ftg':>5s}  "
        f"{'Toe':>4s} {'Heel':>5s} {'B':>5s}   "
        f"{'FS_OT':>5s} {'FS_SL':>5s} {'q_max':>6s}  "
        f"{'Stem':>10s}  {'Heel':>10s}  {'Toe':>10s}  {'Status':>6s}"
    )
    hdr2 = (
        f"{'':.<22s} {'ft':>4s}  {'in':>5s} {'in':>5s} {'in':>5s}  "
        f"{'ft':>4s} {'ft':>5s} {'ft':>5s}   "
        f"{'':>5s} {'':>5s} {'psf':>6s}  "
        f"{'bar@sp':>10s}  {'bar@sp':>10s}  {'bar@sp':>10s}  {'':>6s}"
    )
    lines.append(hdr1)
    lines.append(hdr2)
    lines.append("-" * 120)

    for e in entries:
        stem_str = f"{e.stem_bar}@{e.stem_spacing_in:.0f}\"" if e.stem_spacing_in else "—"
        heel_str = f"{e.heel_bar}@{e.heel_spacing_in:.0f}\"" if e.heel_spacing_in else "—"
        toe_str = f"{e.toe_bar}@{e.toe_spacing_in:.0f}\"" if e.toe_spacing_in else "—"
        fs_ot_str = f"{e.fs_overturning:.2f}" if e.fs_overturning else "—"
        fs_sl_str = f"{e.fs_sliding:.2f}" if e.fs_sliding else "—"
        q_str = f"{e.q_max_psf:.0f}" if e.q_max_psf else "—"
        status = "OK" if e.overall_ok else "NG"

        row = (
            f"{e.wall_mark:<22s} {e.retained_height_ft:>4.0f}  "
            f"{e.stem_top_in:>5.0f} {e.stem_bot_in:>5.0f} {e.base_thickness_in:>5.0f}  "
            f"{e.toe_ft:>4.1f} {e.heel_ft:>5.2f} {e.base_width_ft:>5.2f}   "
            f"{fs_ot_str:>5s} {fs_sl_str:>5s} {q_str:>6s}  "
            f"{stem_str:>10s}  {heel_str:>10s}  {toe_str:>10s}  {status:>6s}"
        )
        lines.append(row)
        if e.notes:
            lines.append(f"    ** {e.notes}")

    lines.append("-" * 120)
    lines.append("")

    # Detail notes
    lines.append("NOTES:")
    lines.append("  1. Walls retaining <= 4 ft unbalanced backfill: per IRC prescriptive requirements.")
    lines.append("  2. All dimensions are nominal. Stem thickness = constant 8\" for walls < 10 ft.")
    lines.append("  3. For walls >= 10 ft, two options are shown: 8\" and 10\" stem/footing.")
    lines.append("  4. Heel length is auto-sized to satisfy stability (FS_OT >= 1.5, FS_SL >= 1.5, q <= q_allow).")
    lines.append("  5. Stem reinforcing is vertical steel on the earth-side face (tension side).")
    lines.append("  6. Heel reinforcing is top steel; toe reinforcing is bottom steel.")
    lines.append(f"  7. T&S steel (transverse): 0.0018 x Ag = 0.0018 x 12 x t  (provide in horizontal direction).")
    lines.append("  8. Cover = 2\" (cast against soil) per ACI 318-19 Table 20.6.1.3.1.")
    lines.append("  9. Verify all soil parameters with project geotechnical report before final design.")
    lines.append(" 10. Embedment = 1'-0\" assumed. Adjust based on frost depth and site conditions.")
    lines.append("")
    lines.append("=" * 120)

    return "\n".join(lines)


def format_detailed_report(entries: list[ScheduleEntry], reports: list[DesignReport]) -> str:
    """Generate detailed per-wall reports beneath the schedule."""
    lines: list[str] = []
    for entry, report in zip(entries, reports):
        lines.append("")
        lines.append("=" * 80)
        lines.append(f"DETAILED DESIGN — {entry.wall_mark}  "
                     f"(H = {entry.retained_height_ft:.0f} ft, "
                     f"t_stem = {entry.stem_bot_in:.0f}\", "
                     f"t_ftg = {entry.base_thickness_in:.0f}\")")
        lines.append("=" * 80)
        lines.append("")

        if report.wall:
            w = report.wall
            lines.append(f"GEOMETRY:")
            lines.append(f"  Stem: {w.stem.height_ft:.1f} ft tall, "
                         f"{w.stem.thickness_top_in:.0f}\" top / {w.stem.thickness_bot_in:.0f}\" base")
            lines.append(f"  Footing: {w.base_width_ft:.2f} ft total  "
                         f"(toe = {w.base.toe_ft:.1f} ft, "
                         f"stem = {w.stem.thickness_bot_in/12:.2f} ft, "
                         f"heel = {w.base.heel_ft:.2f} ft)")
            lines.append(f"  Footing thickness: {w.base.thickness_in:.0f}\"")
            lines.append(f"  Embedment: {w.embedment_ft:.1f} ft")
            lines.append("")

        if report.load_cases:
            lines.append("UNFACTORED LATERAL LOADS:")
            for lc in report.load_cases:
                lines.append(f"  {lc.label}: H = {lc.H_lbft:.0f} lb/ft "
                             f"@ {lc.arm_ft:.2f} ft above base")
            lines.append("")

        if report.stability:
            lines.append("STABILITY (service level):")
            for r in report.stability:
                lines.append(f"  {r}")
            lines.append("")

        if report.sections:
            lines.append("STRUCTURAL DESIGN (ACI 318-19 strength):")
            for s in report.sections:
                lines.append(s.summary())
                lines.append("")

        if report.development_lengths:
            lines.append("DEVELOPMENT LENGTHS:")
            for loc, ld in report.development_lengths.items():
                lines.append(f"  {loc}: {ld:.1f} in")
            lines.append("")

        status = "ALL CHECKS PASS" if entry.overall_ok else "DOES NOT PASS"
        lines.append(f"RESULT: {status}")
        if entry.notes:
            lines.append(f"  {entry.notes}")
        lines.append("")

    return "\n".join(lines)
