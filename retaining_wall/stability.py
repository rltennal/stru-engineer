"""
Stability module — overturning, sliding, and bearing checks at service level.

Per IBC 2021 practice:
  - FS_overturning ≥ 1.5
  - FS_sliding     ≥ 1.5
  - Bearing pressure within allowable (from geotech report)

All checks use *service-level* (unfactored) loads: 1.0 D + 1.0 H.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional

from retaining_wall.geometry import WallGeometry
from retaining_wall.loads import (
    LoadCase,
    SoilParameters,
    WaterParameters,
    compute_earth_pressure_resultant,
    compute_hydrostatic_resultant,
)


@dataclass
class StabilityResult:
    """Result of a single stability check.

    Attributes
    ----------
    check : str
        Name of the check (e.g. "overturning", "sliding", "bearing").
    fs : float | None
        Computed factor of safety. None if data is insufficient.
    fs_required : float
        Required minimum factor of safety.
    demand : float
        Driving/destabilising quantity (moment, force, or pressure).
    capacity : float
        Resisting quantity.
    status : str
        'OK', 'NG', or 'INCOMPLETE' (missing data).
    notes : str
        Explanatory notes or warnings.
    """
    check: str
    fs: Optional[float]
    fs_required: float
    demand: float
    capacity: float
    status: str
    notes: str = ""

    def __str__(self) -> str:
        fs_str = f"{self.fs:.2f}" if self.fs is not None else "N/A"
        return (
            f"{self.check}: FS = {fs_str} "
            f"(req'd {self.fs_required:.2f}) → {self.status}"
            + (f"  [{self.notes}]" if self.notes else "")
        )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _resisting_forces_and_moments(
    wall: WallGeometry,
    soil: SoilParameters,
    gamma_conc: float = 150.0,
) -> tuple[float, float]:
    """Compute total resisting vertical force (lb/ft) and resisting moment
    about the toe (lb·ft/ft) from concrete self-weight and soil over the heel.

    Returns (V_resist, M_resist).
    """
    # Concrete weights and arms
    weights = wall.concrete_weights(gamma_conc)
    arms = wall.moment_arms_from_toe(gamma_conc)

    V_conc = weights["total"]
    M_conc = (
        weights["stem"] * arms["stem"]
        + weights["base"] * arms["base"]
        + weights["shear_key"] * arms["shear_key"]
    )

    # Soil weight over the heel
    heel_width = wall.base.heel_ft
    soil_height = wall.stem.height_ft  # soil height above base slab over heel
    V_soil = soil.gamma_pcf * heel_width * soil_height
    # Moment arm: centroid of heel soil block from toe
    soil_arm = (
        wall.base.toe_ft
        + wall.stem.thickness_bot_in / 12.0
        + heel_width / 2.0
    )
    M_soil = V_soil * soil_arm

    # Soil weight over the toe (embedment)
    if wall.embedment_ft > 0:
        V_toe_soil = soil.gamma_pcf * wall.base.toe_ft * wall.embedment_ft
        toe_soil_arm = wall.base.toe_ft / 2.0
        V_conc += V_toe_soil
        M_conc += V_toe_soil * toe_soil_arm

    return V_conc + V_soil, M_conc + M_soil


# ---------------------------------------------------------------------------
# Overturning check
# ---------------------------------------------------------------------------

def check_overturning(
    wall: WallGeometry,
    soil: SoilParameters,
    load_cases: list[LoadCase],
    fs_required: float = 1.5,
    gamma_conc: float = 150.0,
) -> StabilityResult:
    """Check overturning stability about the toe.

    FS_OT = M_resist / M_overturn  ≥  fs_required

    Parameters
    ----------
    wall : WallGeometry
    soil : SoilParameters
    load_cases : list[LoadCase]
        All lateral (and vertical) load resultants.
    fs_required : float
        Required minimum FS (default 1.5).
    gamma_conc : float
        Concrete unit weight (pcf).
    """
    _, M_resist = _resisting_forces_and_moments(wall, soil, gamma_conc)

    # Add resisting moments from any vertical load-case components
    for lc in load_cases:
        if lc.V_lbft > 0:
            M_resist += lc.M_resist_lbft

    M_ot = sum(lc.M_ot_lbft for lc in load_cases)

    if M_ot <= 0:
        return StabilityResult(
            check="Overturning",
            fs=None,
            fs_required=fs_required,
            demand=M_ot,
            capacity=M_resist,
            status="INCOMPLETE",
            notes="No overturning moment — check load input.",
        )

    fs = M_resist / M_ot
    status = "OK" if fs >= fs_required else "NG"
    return StabilityResult(
        check="Overturning",
        fs=fs,
        fs_required=fs_required,
        demand=M_ot,
        capacity=M_resist,
        status=status,
    )


# ---------------------------------------------------------------------------
# Sliding check
# ---------------------------------------------------------------------------

def check_sliding(
    wall: WallGeometry,
    soil: SoilParameters,
    load_cases: list[LoadCase],
    fs_required: float = 1.5,
    gamma_conc: float = 150.0,
) -> StabilityResult:
    """Check sliding stability along the base.

    FS_SL = (μ·V_total + Pp) / H_total  ≥  fs_required

    Passive resistance is included only if ``soil.passive_permitted``.
    """
    V_total, _ = _resisting_forces_and_moments(wall, soil, gamma_conc)

    # Add vertical components of lateral loads
    for lc in load_cases:
        V_total += lc.V_lbft

    # Base friction
    friction = soil.mu_sliding * V_total

    # Passive resistance (if permitted)
    Pp = 0.0
    if soil.passive_permitted and wall.embedment_ft > 0:
        p_gamma = soil.passive_gamma_pcf or soil.gamma_pcf
        p_phi = soil.passive_phi_deg or soil.phi_deg
        Kp = math.tan(math.pi / 4 + math.radians(p_phi) / 2) ** 2
        Pp = 0.5 * Kp * p_gamma * wall.embedment_ft ** 2

    H_total = sum(lc.H_lbft for lc in load_cases)

    if H_total <= 0:
        return StabilityResult(
            check="Sliding",
            fs=None,
            fs_required=fs_required,
            demand=H_total,
            capacity=friction + Pp,
            status="INCOMPLETE",
            notes="No driving horizontal force — check load input.",
        )

    fs = (friction + Pp) / H_total
    status = "OK" if fs >= fs_required else "NG"
    notes = ""
    if Pp > 0:
        notes = f"Includes passive Pp={Pp:.0f} lb/ft"
    return StabilityResult(
        check="Sliding",
        fs=fs,
        fs_required=fs_required,
        demand=H_total,
        capacity=friction + Pp,
        status=status,
        notes=notes,
    )


# ---------------------------------------------------------------------------
# Bearing check
# ---------------------------------------------------------------------------

def check_bearing(
    wall: WallGeometry,
    soil: SoilParameters,
    load_cases: list[LoadCase],
    gamma_conc: float = 150.0,
) -> StabilityResult:
    """Check bearing pressure at the base.

    Computes the eccentricity of the resultant and the maximum bearing
    pressure (trapezoidal or triangular distribution).

    Returns 'INCOMPLETE' if ``soil.allowable_bearing_psf`` is not provided.
    """
    V_total, M_resist = _resisting_forces_and_moments(wall, soil, gamma_conc)

    for lc in load_cases:
        V_total += lc.V_lbft
        M_resist += lc.M_resist_lbft

    M_ot = sum(lc.M_ot_lbft for lc in load_cases)

    B = wall.base_width_ft  # total base width
    M_net = M_resist - M_ot  # net moment about toe
    if V_total <= 0:
        return StabilityResult(
            check="Bearing",
            fs=None,
            fs_required=1.0,
            demand=0,
            capacity=0,
            status="INCOMPLETE",
            notes="No vertical load — check input.",
        )

    x_bar = M_net / V_total  # distance from toe to resultant
    e = B / 2.0 - x_bar  # eccentricity from centreline

    # Bearing pressure
    if abs(e) <= B / 6.0:
        # Resultant within middle third → trapezoidal
        q_max = V_total / B * (1 + 6 * e / B)
        q_min = V_total / B * (1 - 6 * e / B)
    else:
        # Resultant outside middle third → triangular
        q_max = 2 * V_total / (3 * x_bar) if x_bar > 0 else float("inf")
        q_min = 0.0

    if soil.allowable_bearing_psf is None:
        return StabilityResult(
            check="Bearing",
            fs=None,
            fs_required=1.0,
            demand=q_max,
            capacity=0,
            status="INCOMPLETE",
            notes=(
                f"q_max = {q_max:.0f} psf, q_min = {q_min:.0f} psf, "
                f"e = {e:.2f} ft. Allowable bearing not yet provided."
            ),
        )

    fs = soil.allowable_bearing_psf / q_max if q_max > 0 else float("inf")
    status = "OK" if q_max <= soil.allowable_bearing_psf else "NG"
    return StabilityResult(
        check="Bearing",
        fs=fs,
        fs_required=1.0,
        demand=q_max,
        capacity=soil.allowable_bearing_psf,
        status=status,
        notes=f"q_max={q_max:.0f} psf, q_min={q_min:.0f} psf, e={e:.2f} ft",
    )


# ---------------------------------------------------------------------------
# Convenience wrapper
# ---------------------------------------------------------------------------

def check_all_stability(
    wall: WallGeometry,
    soil: SoilParameters,
    load_cases: list[LoadCase],
    fs_ot: float = 1.5,
    fs_sl: float = 1.5,
    gamma_conc: float = 150.0,
) -> list[StabilityResult]:
    """Run all three service-level stability checks and return results."""
    return [
        check_overturning(wall, soil, load_cases, fs_ot, gamma_conc),
        check_sliding(wall, soil, load_cases, fs_sl, gamma_conc),
        check_bearing(wall, soil, load_cases, gamma_conc),
    ]
