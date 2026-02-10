"""
Wall designer orchestrator — ties all modules together.

Given a :class:`DesignCriteria`, the designer:
  1. Validates completeness of criteria.
  2. Assembles geometry, soil, water, surcharge, and seismic objects.
  3. Computes unfactored load resultants.
  4. Runs service-level stability checks (overturning, sliding, bearing).
  5. Computes factored demands at critical sections (stem base, heel, toe).
  6. Designs reinforcement per ACI 318-19.
  7. Returns a structured report.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

from retaining_wall.criteria import DesignCriteria
from retaining_wall.materials import Concrete, RebarSpec
from retaining_wall.geometry import WallGeometry
from retaining_wall.loads import (
    SoilParameters,
    WaterParameters,
    SurchargeLoad,
    SeismicParameters,
    LoadCase,
    compute_earth_pressure_resultant,
    compute_hydrostatic_resultant,
    compute_surcharge_resultant,
    compute_seismic_increment,
)
from retaining_wall.stability import StabilityResult, check_all_stability
from retaining_wall.structural import (
    SectionDesign,
    design_flexure,
    min_temp_shrinkage_steel,
    required_development_length,
    required_hook_development,
)


# ---------------------------------------------------------------------------
# Load combination helpers
# ---------------------------------------------------------------------------

# IBC/ASCE 7 load combinations relevant to retaining walls (strength level).
# For earth pressure (H), the critical combinations are typically:
#   1.2D + 1.6H
#   0.9D + 1.6H  (when D is stabilising and H is destabilising)

LOAD_FACTOR_H = 1.6   # lateral earth pressure
LOAD_FACTOR_D_MAX = 1.2
LOAD_FACTOR_D_MIN = 0.9


# ---------------------------------------------------------------------------
# Factored demand calculator
# ---------------------------------------------------------------------------

def _factored_stem_demands(
    wall: WallGeometry,
    soil: SoilParameters,
    water: WaterParameters,
    surcharge: SurchargeLoad,
    seismic: SeismicParameters,
) -> tuple[float, float]:
    """Compute factored Mu and Vu at the stem base (critical section).

    The stem is a vertical cantilever loaded by lateral earth pressure
    (triangular), surcharge (rectangular), water (triangular), and
    seismic increment.

    Returns (Mu_lbft, Vu_lb) per lineal foot of wall, both positive.
    """
    H = wall.stem.height_ft  # height of stem

    # --- Unfactored pressures ---
    # Active earth pressure at stem base
    ep = compute_earth_pressure_resultant(soil, H, wall.backfill_slope_deg)
    # Hydrostatic
    wp = compute_hydrostatic_resultant(water, H)
    # Surcharge
    sp = compute_surcharge_resultant(surcharge, soil, H)
    # Seismic
    eq = compute_seismic_increment(soil, seismic, H, wall.backfill_slope_deg)

    # --- Factor and sum ---
    # Use 1.6H for all lateral earth/water/surcharge loads
    Vu = LOAD_FACTOR_H * ep.H_lbft
    Mu = LOAD_FACTOR_H * ep.M_ot_lbft  # moment about stem base

    if wp is not None:
        Vu += LOAD_FACTOR_H * wp.H_lbft
        Mu += LOAD_FACTOR_H * wp.H_lbft * wp.arm_ft

    if sp is not None:
        Vu += LOAD_FACTOR_H * sp.H_lbft
        Mu += LOAD_FACTOR_H * sp.H_lbft * sp.arm_ft

    if eq is not None:
        # Seismic increment factored at 1.0 (per ASCE 7 seismic combinations)
        Vu += eq.H_lbft
        Mu += eq.H_lbft * eq.arm_ft

    return abs(Mu), abs(Vu)


def _factored_heel_demands(
    wall: WallGeometry,
    soil: SoilParameters,
) -> tuple[float, float]:
    """Compute factored Mu and Vu at the heel slab (critical section at stem face).

    The heel cantilevers from the stem.  Loading on the heel (top surface):
      - Soil weight (downward) — loads the heel
      - Base slab self-weight (downward)
    Net upward bearing pressure partially offsets these, but for the
    *maximum heel demand*, we use 1.2D + 1.6H (soil weight as H)
    and conservatively neglect upward bearing on the heel.

    The critical steel is on the *top* of the heel slab.
    """
    heel_L = wall.base.heel_ft
    if heel_L <= 0:
        return 0.0, 0.0

    t_slab_ft = wall.base.thickness_ft
    h_soil = wall.stem.height_ft  # soil above heel

    # Loads per foot of wall width, per foot of heel length
    w_soil = soil.gamma_pcf * h_soil      # psf on heel (soil column)
    w_slab = wall.base.thickness_in / 12.0 * 150.0  # slab self-weight (pcf assumed 150)

    # Factored: soil weight treated as H (earth pressure effect on heel)
    w_u = LOAD_FACTOR_H * w_soil + LOAD_FACTOR_D_MAX * w_slab

    # Cantilever from stem face
    Vu = w_u * heel_L
    Mu = w_u * heel_L ** 2 / 2.0

    return abs(Mu), abs(Vu)


def _factored_toe_demands(
    wall: WallGeometry,
    soil: SoilParameters,
    q_max_psf: float,
    q_min_psf: float,
) -> tuple[float, float]:
    """Compute factored Mu and Vu at the toe slab (critical section at stem face).

    The toe cantilevers from the stem in the opposite direction.  Loading:
      - Upward bearing pressure (trapezoidal/uniform, approximated as
        the average of q at toe edge and q at stem face)
      - Downward: slab self-weight + soil above toe (embedment)

    Critical steel is on the *bottom* of the toe slab.
    """
    toe_L = wall.base.toe_ft
    if toe_L <= 0:
        return 0.0, 0.0

    B = wall.base_width_ft
    # Bearing pressure at toe edge ≈ q_max, at stem face ≈ interpolated
    # Linear interpolation: q at distance x from toe = q_max - (q_max-q_min)*x/B
    q_at_stem = q_max_psf - (q_max_psf - q_min_psf) * toe_L / B
    q_avg = (q_max_psf + q_at_stem) / 2.0

    # Upward net pressure (bearing minus self-weight and overburden)
    w_slab = wall.base.thickness_in / 12.0 * 150.0
    w_soil_above = soil.gamma_pcf * wall.embedment_ft if wall.embedment_ft > 0 else 0.0

    # Net upward = bearing - slab weight - soil above toe
    # Factor bearing as 1.6 (it comes from H/earth), self-weight as 0.9 (stabilising)
    w_up = LOAD_FACTOR_H * q_avg
    w_down = LOAD_FACTOR_D_MIN * (w_slab + w_soil_above)
    w_net = w_up - w_down

    if w_net <= 0:
        return 0.0, 0.0

    Vu = w_net * toe_L
    Mu = w_net * toe_L ** 2 / 2.0

    return abs(Mu), abs(Vu)


# ---------------------------------------------------------------------------
# Design report
# ---------------------------------------------------------------------------

@dataclass
class DesignReport:
    """Complete design report for a cantilever retaining wall."""
    criteria: DesignCriteria
    wall: Optional[WallGeometry] = None
    load_cases: list[LoadCase] = field(default_factory=list)
    stability: list[StabilityResult] = field(default_factory=list)
    sections: list[SectionDesign] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    development_lengths: dict[str, float] = field(default_factory=dict)

    @property
    def all_ok(self) -> bool:
        if not self.stability or not self.sections:
            return False
        stab_ok = all(r.status == "OK" for r in self.stability)
        sect_ok = all(s.flexure_ok and s.shear_ok for s in self.sections)
        return stab_ok and sect_ok

    def summary(self) -> str:
        lines = [self.criteria.design_basis_narrative(), ""]

        if self.warnings:
            lines.append("WARNINGS:")
            for w in self.warnings:
                lines.append(f"  ⚠ {w}")
            lines.append("")

        if self.wall:
            lines.append(f"GEOMETRY:")
            lines.append(f"  Stem height = {self.wall.stem.height_ft:.1f} ft")
            lines.append(
                f"  Stem thickness = {self.wall.stem.thickness_top_in}″ (top) / "
                f"{self.wall.stem.thickness_bot_in}″ (base)"
            )
            lines.append(f"  Base width = {self.wall.base_width_ft:.2f} ft")
            lines.append(
                f"  Toe = {self.wall.base.toe_ft:.1f} ft, "
                f"Heel = {self.wall.base.heel_ft:.1f} ft, "
                f"Base thickness = {self.wall.base.thickness_in}″"
            )
            lines.append("")

        if self.load_cases:
            lines.append("UNFACTORED LOAD CASES:")
            for lc in self.load_cases:
                lines.append(
                    f"  {lc.label}: H={lc.H_lbft:.0f} lb/ft @ {lc.arm_ft:.2f} ft"
                )
            lines.append("")

        if self.stability:
            lines.append("SERVICE-LEVEL STABILITY:")
            for r in self.stability:
                lines.append(f"  {r}")
            lines.append("")

        if self.sections:
            lines.append("STRUCTURAL DESIGN (ACI 318-19):")
            for s in self.sections:
                lines.append(s.summary())
                lines.append("")

        if self.development_lengths:
            lines.append("DEVELOPMENT LENGTHS:")
            for loc, ld in self.development_lengths.items():
                lines.append(f"  {loc}: ld = {ld:.1f} in")
            lines.append("")

        overall = "ALL CHECKS PASS" if self.all_ok else "DESIGN INCOMPLETE OR NG"
        lines.append(f"OVERALL: {overall}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Designer
# ---------------------------------------------------------------------------

class WallDesigner:
    """Orchestrates the complete cantilever retaining wall design.

    Usage::

        criteria = DesignCriteria(
            retained_height_ft=10.0,
            base_heel_ft=5.0,
            backfill_gamma_pcf=120.0,
            backfill_phi_deg=30.0,
            ...
        )
        designer = WallDesigner(criteria)
        report = designer.run()
        print(report.summary())
    """

    def __init__(self, criteria: DesignCriteria) -> None:
        self.criteria = criteria

    def run(self) -> DesignReport:
        """Execute the full design sequence and return a report."""
        report = DesignReport(criteria=self.criteria)
        missing = self.criteria.validate()

        if missing:
            report.warnings.append(
                "Design criteria incomplete. The following are needed:"
            )
            report.warnings.extend(f"  - {m}" for m in missing)

        # Even with missing data, build what we can.
        try:
            wall = self.criteria.build_wall_geometry()
            report.wall = wall
        except ValueError as e:
            report.warnings.append(f"Cannot build geometry: {e}")
            return report

        concrete = self.criteria.build_concrete()
        cover = self.criteria.cover_in()

        # --- Loads ---
        try:
            soil = self.criteria.build_soil()
        except ValueError:
            report.warnings.append("Soil parameters missing — cannot compute loads.")
            return report

        water = self.criteria.build_water()
        surcharge = self.criteria.build_surcharge()
        seismic = self.criteria.build_seismic()

        total_H = wall.total_height_ft  # pressure height = stem + base slab

        ep = compute_earth_pressure_resultant(soil, total_H, wall.backfill_slope_deg)
        report.load_cases.append(ep)

        wp = compute_hydrostatic_resultant(water, total_H)
        if wp is not None:
            report.load_cases.append(wp)

        sp = compute_surcharge_resultant(surcharge, soil, total_H)
        if sp is not None:
            report.load_cases.append(sp)

        eq = compute_seismic_increment(soil, seismic, total_H, wall.backfill_slope_deg)
        if eq is not None:
            report.load_cases.append(eq)

        # --- Stability ---
        report.stability = check_all_stability(
            wall,
            soil,
            report.load_cases,
            fs_ot=self.criteria.fs_overturning,
            fs_sl=self.criteria.fs_sliding,
            gamma_conc=self.criteria.gamma_conc_pcf,
        )

        # --- Structural design ---
        # Determine fy based on expected bar size (start with #4 Gr.40)
        fy_stem = 40_000  # assume #4 first
        fy_base = 40_000

        # 1) Stem at base
        Mu_stem, Vu_stem = _factored_stem_demands(wall, soil, water, surcharge, seismic)
        # If demand is high, we may need #5 Gr.60
        stem_section = design_flexure(
            location="stem_base",
            h_in=wall.stem.thickness_bot_in,
            Mu_lbft=Mu_stem,
            Vu_lb=Vu_stem,
            fc=concrete,
            fy=fy_stem,
            cover_in=cover,
            max_bar_size=self.criteria.rebar_max_bar_size,
        )
        # If bar selection picked #5+, redo with fy=60,000
        if stem_section.bar and stem_section.bar.size_num >= 5:
            stem_section = design_flexure(
                location="stem_base",
                h_in=wall.stem.thickness_bot_in,
                Mu_lbft=Mu_stem,
                Vu_lb=Vu_stem,
                fc=concrete,
                fy=60_000,
                cover_in=cover,
                max_bar_size=self.criteria.rebar_max_bar_size,
            )
        report.sections.append(stem_section)

        # 2) Heel slab
        Mu_heel, Vu_heel = _factored_heel_demands(wall, soil)
        heel_section = design_flexure(
            location="heel (top steel)",
            h_in=wall.base.thickness_in,
            Mu_lbft=Mu_heel,
            Vu_lb=Vu_heel,
            fc=concrete,
            fy=fy_base,
            cover_in=cover,
            max_bar_size=self.criteria.rebar_max_bar_size,
        )
        if heel_section.bar and heel_section.bar.size_num >= 5:
            heel_section = design_flexure(
                location="heel (top steel)",
                h_in=wall.base.thickness_in,
                Mu_lbft=Mu_heel,
                Vu_lb=Vu_heel,
                fc=concrete,
                fy=60_000,
                cover_in=cover,
                max_bar_size=self.criteria.rebar_max_bar_size,
            )
        report.sections.append(heel_section)

        # 3) Toe slab
        # Need bearing pressures from stability check
        bearing_result = next(
            (r for r in report.stability if r.check == "Bearing"), None
        )
        q_max = bearing_result.demand if bearing_result else 0
        q_min = 0.0
        if bearing_result and bearing_result.notes:
            # Parse q_min from notes
            import re
            m = re.search(r"q_min=(\d+)", bearing_result.notes)
            if m:
                q_min = float(m.group(1))

        Mu_toe, Vu_toe = _factored_toe_demands(wall, soil, q_max, q_min)
        toe_section = design_flexure(
            location="toe (bottom steel)",
            h_in=wall.base.thickness_in,
            Mu_lbft=Mu_toe,
            Vu_lb=Vu_toe,
            fc=concrete,
            fy=fy_base,
            cover_in=cover,
            max_bar_size=self.criteria.rebar_max_bar_size,
        )
        if toe_section.bar and toe_section.bar.size_num >= 5:
            toe_section = design_flexure(
                location="toe (bottom steel)",
                h_in=wall.base.thickness_in,
                Mu_lbft=Mu_toe,
                Vu_lb=Vu_toe,
                fc=concrete,
                fy=60_000,
                cover_in=cover,
                max_bar_size=self.criteria.rebar_max_bar_size,
            )
        report.sections.append(toe_section)

        # --- Development lengths ---
        for section in report.sections:
            if section.bar:
                top_bar = "heel" in section.location or "top" in section.location
                ld = required_development_length(
                    section.bar, concrete, cover, top_bar=top_bar
                )
                ldh = required_hook_development(section.bar, concrete, cover)
                report.development_lengths[section.location] = ld
                report.development_lengths[f"{section.location} (hook)"] = ldh

        # --- Temperature / shrinkage steel reminder ---
        ts_stem = min_temp_shrinkage_steel(wall.stem.thickness_bot_in)
        ts_base = min_temp_shrinkage_steel(wall.base.thickness_in)
        report.warnings.append(
            f"T&S steel (ρ=0.0018): stem={ts_stem:.3f} in²/ft, "
            f"base={ts_base:.3f} in²/ft — provide in transverse direction."
        )

        return report
