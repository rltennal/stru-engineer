"""
Loads module — lateral earth pressure, hydrostatic, surcharge, seismic.

Computes unfactored (service-level) load resultants acting on the wall.
These feed into both:
  - Stability checks (service-level FS)
  - Structural design (after applying load factors)

Earth pressure theory uses Rankine (default) or Coulomb.  Seismic uses
Mononobe-Okabe when the seismic flag is active.

All functions return forces **per lineal foot of wall** (lb/ft) and
moment arms measured from a stated datum.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Soil parameters
# ---------------------------------------------------------------------------

@dataclass
class SoilParameters:
    """Geotechnical input for a single soil stratum.

    Parameters
    ----------
    gamma_pcf : float
        Total unit weight (pcf).
    phi_deg : float
        Angle of internal friction (degrees).
    cohesion_psf : float
        Cohesion (psf). Default 0 (granular).
    condition : str
        'active' or 'at_rest'. IBC/ACI lateral-pressure basis.
    mu_sliding : float
        Base-soil friction coefficient for sliding resistance.
        Typical 0.35–0.55 for granular soils.
    allowable_bearing_psf : float | None
        Allowable bearing pressure (psf). None = not yet provided.
    passive_permitted : bool
        Whether passive resistance in front of the wall may be used.
    passive_gamma_pcf : float | None
        Unit weight of soil providing passive resistance (pcf).
    passive_phi_deg : float | None
        Friction angle of passive soil (degrees).
    """
    gamma_pcf: float
    phi_deg: float
    cohesion_psf: float = 0.0
    condition: str = "active"
    mu_sliding: float = 0.45
    allowable_bearing_psf: Optional[float] = None
    passive_permitted: bool = False
    passive_gamma_pcf: Optional[float] = None
    passive_phi_deg: Optional[float] = None

    def __post_init__(self) -> None:
        if self.condition not in ("active", "at_rest"):
            raise ValueError("condition must be 'active' or 'at_rest'")

    @property
    def phi_rad(self) -> float:
        return math.radians(self.phi_deg)

    @property
    def Ka(self) -> float:
        """Rankine active earth pressure coefficient (level backfill)."""
        return math.tan(math.pi / 4 - self.phi_rad / 2) ** 2

    @property
    def K0(self) -> float:
        """At-rest earth pressure coefficient (Jaky)."""
        return 1.0 - math.sin(self.phi_rad)

    @property
    def K(self) -> float:
        """Return the applicable lateral pressure coefficient."""
        return self.K0 if self.condition == "at_rest" else self.Ka

    @property
    def Kp(self) -> float:
        """Rankine passive earth pressure coefficient."""
        return math.tan(math.pi / 4 + self.phi_rad / 2) ** 2


def rankine_Ka_sloped(phi_deg: float, beta_deg: float) -> float:
    """Rankine Ka for a sloping backfill surface.

    Parameters
    ----------
    phi_deg : float
        Friction angle of backfill (degrees).
    beta_deg : float
        Backfill slope angle (degrees). Must be < phi_deg.
    """
    phi = math.radians(phi_deg)
    beta = math.radians(beta_deg)
    if beta >= phi:
        raise ValueError("backfill slope must be < friction angle")
    cos_b = math.cos(beta)
    return cos_b * (cos_b - math.sqrt(cos_b**2 - math.cos(phi)**2)) / (
        cos_b + math.sqrt(cos_b**2 - math.cos(phi)**2)
    )


# ---------------------------------------------------------------------------
# Water parameters
# ---------------------------------------------------------------------------

@dataclass
class WaterParameters:
    """Hydrostatic pressure parameters.

    IBC requires consideration of water pressure unless drainage and
    groundwater conditions explicitly eliminate it.

    Parameters
    ----------
    gwl_depth_ft : float | None
        Depth to groundwater below top of retained soil (ft).
        None = no water (must be justified by drainage design).
    gamma_water_pcf : float
        Unit weight of water (pcf). Default 62.4.
    drainage_provided : bool
        Whether positive drainage is designed behind the wall.
    """
    gwl_depth_ft: Optional[float] = None
    gamma_water_pcf: float = 62.4
    drainage_provided: bool = False

    @property
    def has_water_case(self) -> bool:
        """True if hydrostatic load must be considered."""
        if self.gwl_depth_ft is not None:
            return True
        # Even without explicit GWL, if drainage is NOT provided, a water
        # case should be carried as a design checklist item per IBC.
        return not self.drainage_provided


# ---------------------------------------------------------------------------
# Surcharge
# ---------------------------------------------------------------------------

class SurchargeType(Enum):
    UNIFORM = "uniform"
    STRIP = "strip"
    POINT = "point"
    LINE = "line"


@dataclass
class SurchargeLoad:
    """Surcharge loading on or near the retained soil.

    Parameters
    ----------
    load_type : SurchargeType
        Type of surcharge (uniform, strip, point, line).
    magnitude_psf : float
        Intensity (psf for uniform/strip, plf for line, lb for point).
    offset_ft : float
        Distance from back face of wall to surcharge (ft).
    width_ft : float
        Width of strip load (ft). Only used for strip type.
    """
    load_type: SurchargeType = SurchargeType.UNIFORM
    magnitude_psf: float = 0.0
    offset_ft: float = 0.0
    width_ft: float = 0.0


# ---------------------------------------------------------------------------
# Seismic parameters (placeholder)
# ---------------------------------------------------------------------------

@dataclass
class SeismicParameters:
    """Seismic design parameters.

    Placeholder — populated when SDC and site coefficients are known.
    """
    sdc: str = ""            # seismic design category (A–F)
    sds: float = 0.0         # design spectral acceleration (short period)
    sd1: float = 0.0         # design spectral acceleration (1-sec)
    kh: float = 0.0          # horizontal seismic coefficient for M-O
    kv: float = 0.0          # vertical seismic coefficient for M-O
    use_mononobe_okabe: bool = False

    @property
    def is_active(self) -> bool:
        return self.use_mononobe_okabe and self.kh > 0


# ---------------------------------------------------------------------------
# Load resultant calculators
# ---------------------------------------------------------------------------

@dataclass
class LoadCase:
    """A single lateral load resultant acting on the wall.

    Attributes
    ----------
    label : str
        Human-readable name (e.g., "Active earth pressure").
    H_lbft : float
        Horizontal force per lineal foot of wall (lb/ft).
        Positive = pushing wall toward toe (overturning direction).
    arm_ft : float
        Height of resultant above base of footing (ft).
    V_lbft : float
        Vertical component of load (lb/ft). Positive = downward.
    v_arm_ft : float
        Moment arm of vertical component from toe (ft).
    """
    label: str
    H_lbft: float
    arm_ft: float
    V_lbft: float = 0.0
    v_arm_ft: float = 0.0

    @property
    def M_ot_lbft(self) -> float:
        """Overturning moment about the toe (lb·ft/ft)."""
        return self.H_lbft * self.arm_ft

    @property
    def M_resist_lbft(self) -> float:
        """Resisting moment from vertical component about the toe (lb·ft/ft)."""
        return self.V_lbft * self.v_arm_ft


def compute_earth_pressure_resultant(
    soil: SoilParameters,
    height_ft: float,
    backfill_slope_deg: float = 0.0,
) -> LoadCase:
    """Compute the Rankine lateral earth pressure resultant.

    For a triangular distribution on a wall of height *height_ft*:
        P = 0.5 · K · γ · H²
    Resultant acts at H/3 from the base.

    Parameters
    ----------
    soil : SoilParameters
    height_ft : float
        Total height over which pressure acts (ft).
    backfill_slope_deg : float
        Slope of backfill (degrees). 0 = level.
    """
    if backfill_slope_deg > 0:
        Ka = rankine_Ka_sloped(soil.phi_deg, backfill_slope_deg)
    else:
        Ka = soil.K  # uses active or at-rest per soil.condition

    P = 0.5 * Ka * soil.gamma_pcf * height_ft ** 2
    arm = height_ft / 3.0

    # For sloped backfill, resultant is inclined at β from horizontal.
    beta_rad = math.radians(backfill_slope_deg)
    H = P * math.cos(beta_rad)
    V = P * math.sin(beta_rad)

    return LoadCase(
        label=f"Earth pressure ({soil.condition}, β={backfill_slope_deg}°)",
        H_lbft=H,
        arm_ft=arm,
        V_lbft=V,
    )


def compute_hydrostatic_resultant(
    water: WaterParameters,
    wall_height_ft: float,
) -> Optional[LoadCase]:
    """Compute hydrostatic pressure resultant if water is present.

    Returns None if no water case applies.

    Triangular distribution from GWL to base:
        Pw = 0.5 · γw · hw²
    """
    if not water.has_water_case:
        return None
    if water.gwl_depth_ft is None:
        # No explicit GWL but water case flagged (no drainage).
        # Return a zero-magnitude placeholder so the checklist carries it.
        return LoadCase(label="Hydrostatic (TBD — no GWL data)", H_lbft=0.0, arm_ft=0.0)

    hw = wall_height_ft - water.gwl_depth_ft
    if hw <= 0:
        return None

    Pw = 0.5 * water.gamma_water_pcf * hw ** 2
    arm = hw / 3.0
    return LoadCase(label="Hydrostatic pressure", H_lbft=Pw, arm_ft=arm)


def compute_surcharge_resultant(
    surcharge: SurchargeLoad,
    soil: SoilParameters,
    wall_height_ft: float,
) -> Optional[LoadCase]:
    """Convert a surcharge into an equivalent lateral resultant.

    Only uniform surcharge is implemented in this template.  Strip/point/line
    follow Boussinesq or simplified chart methods and require additional
    geometry data.
    """
    if surcharge.magnitude_psf == 0:
        return None

    if surcharge.load_type == SurchargeType.UNIFORM:
        # Uniform surcharge → rectangular lateral pressure = K · q
        K = soil.K
        q = surcharge.magnitude_psf
        H_total = K * q * wall_height_ft
        arm = wall_height_ft / 2.0
        return LoadCase(
            label=f"Uniform surcharge ({q} psf)",
            H_lbft=H_total,
            arm_ft=arm,
        )

    # Placeholder for other surcharge types
    return LoadCase(
        label=f"Surcharge ({surcharge.load_type.value}) — not yet computed",
        H_lbft=0.0,
        arm_ft=0.0,
    )


def compute_seismic_increment(
    soil: SoilParameters,
    seismic: SeismicParameters,
    wall_height_ft: float,
    backfill_slope_deg: float = 0.0,
) -> Optional[LoadCase]:
    """Mononobe-Okabe dynamic earth pressure increment.

    Returns the *incremental* force ΔP_AE above the static active pressure.
    Returns None if seismic is not active.
    """
    if not seismic.is_active:
        return None

    phi = math.radians(soil.phi_deg)
    beta = math.radians(backfill_slope_deg)
    kh = seismic.kh
    kv = seismic.kv
    theta = math.atan(kh / (1.0 - kv))

    # M-O coefficient (vertical wall face, δ=0 simplified)
    num = math.cos(phi - theta) ** 2
    denom_inner = math.sqrt(math.sin(phi) * math.sin(phi - theta - beta))
    denom = math.cos(theta) * (1.0 + denom_inner) ** 2
    if denom == 0:
        return None
    KAE = num / denom

    # Static Ka for subtraction
    Ka_static = soil.Ka
    delta_K = max(KAE - Ka_static, 0.0)

    P_dyn = 0.5 * delta_K * soil.gamma_pcf * (1.0 - kv) * wall_height_ft ** 2
    # Dynamic increment typically applied at 0.6H from base (Seed & Whitman)
    arm = 0.6 * wall_height_ft

    return LoadCase(
        label="Seismic M-O increment",
        H_lbft=P_dyn,
        arm_ft=arm,
    )
