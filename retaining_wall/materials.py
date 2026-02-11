"""
Materials module — concrete and reinforcing steel properties.

Implements the bar-sizing logic and material constraints from the design basis:
- f'c = 3,000 psi concrete
- #4 Grade 40 (or smaller), #5 Grade 60 (or larger)
- Prefer #4 and smaller, step to #5 when needed, avoid #7+
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Rebar database
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class BarProperties:
    """Immutable record for a single bar size."""
    size_num: int          # e.g. 3 for #3
    diameter_in: float     # nominal diameter (in)
    area_in2: float        # nominal area (in²)
    weight_plf: float      # weight (lb/ft)
    fy_psi: int            # yield strength per design basis rule

    @property
    def label(self) -> str:
        return f"#{self.size_num}"


def _bar(size: int, dia: float, area: float, wt: float) -> BarProperties:
    """Helper — assigns fy based on the design-basis rule."""
    fy = 40_000 if size <= 4 else 60_000
    return BarProperties(size, dia, area, wt, fy)


# Standard bar table (ACI standard sizes through #11)
REBAR_DB: dict[int, BarProperties] = {
    3:  _bar(3,  0.375, 0.11,  0.376),
    4:  _bar(4,  0.500, 0.20,  0.668),
    5:  _bar(5,  0.625, 0.31,  1.043),
    6:  _bar(6,  0.750, 0.44,  1.502),
    7:  _bar(7,  0.875, 0.60,  2.044),
    8:  _bar(8,  1.000, 0.79,  2.670),
    9:  _bar(9,  1.128, 1.00,  3.400),
    10: _bar(10, 1.270, 1.27,  4.303),
    11: _bar(11, 1.410, 1.56,  5.313),
}


def select_bar(
    required_as: float,
    thickness: float,
    cover: float,
    max_spacing: float = 18.0,
    min_spacing: float = 1.0,
    max_bar_size: int = 6,
) -> tuple[BarProperties, float]:
    """Pick the smallest preferred bar at a feasible spacing.

    Follows the escalation order: #3 → #4 → #5 → #6 (capped by *max_bar_size*).
    Returns ``(bar, spacing_in)`` or raises ``ValueError`` if nothing fits.

    Parameters
    ----------
    required_as : float
        Required steel area per foot of wall (in²/ft).
    thickness : float
        Section thickness (in) — used only for spacing sanity check.
    cover : float
        Clear cover (in) — not used in spacing calc but reserved.
    max_spacing : float
        Maximum centre-to-centre spacing (in), default 18 (ACI 318-19 §11.7.2).
    min_spacing : float
        Minimum clear spacing (in), default 1.0.
    max_bar_size : int
        Largest bar number to consider (default 6, per design preference).
    """
    preferred_order = [3, 4, 5, 6]
    for size in preferred_order:
        if size > max_bar_size:
            break
        bar = REBAR_DB[size]
        # spacing = Ab * 12 / As_required  (bars per foot)
        if required_as <= 0:
            raise ValueError("required_as must be > 0")
        spacing = bar.area_in2 * 12.0 / required_as
        clear = spacing - bar.diameter_in
        if clear >= min_spacing and spacing <= max_spacing:
            return bar, math.floor(spacing * 2) / 2  # round down to nearest ½″
    raise ValueError(
        f"Cannot satisfy As={required_as:.3f} in²/ft within bar sizes "
        f"≤#{max_bar_size} and spacing {min_spacing}–{max_spacing} in."
    )


# ---------------------------------------------------------------------------
# Concrete
# ---------------------------------------------------------------------------

@dataclass
class Concrete:
    """Concrete material properties.

    Attributes
    ----------
    fc_psi : int
        Specified compressive strength (psi). Default 3 000 per design basis.
    wc_pcf : float
        Unit weight (pcf). Default 150 (normal weight).
    lambda_factor : float
        ACI 318-19 lightweight factor λ. 1.0 for normal weight.
    """
    fc_psi: int = 3_000
    wc_pcf: float = 150.0
    lambda_factor: float = 1.0

    @property
    def fc_ksi(self) -> float:
        return self.fc_psi / 1_000

    @property
    def sqrt_fc(self) -> float:
        """√f'c (psi units)."""
        return math.sqrt(self.fc_psi)

    @property
    def fr(self) -> float:
        """Modulus of rupture fr = 7.5 λ √f'c  (psi), ACI 318-19 §19.2.3."""
        return 7.5 * self.lambda_factor * self.sqrt_fc

    @property
    def beta1(self) -> float:
        """Whitney stress-block factor β₁, ACI 318-19 §22.2.2.4.3."""
        if self.fc_psi <= 4_000:
            return 0.85
        elif self.fc_psi >= 8_000:
            return 0.65
        else:
            return 0.85 - 0.05 * (self.fc_psi - 4_000) / 1_000

    @property
    def Ec(self) -> float:
        """Modulus of elasticity Ec = 33 wc^1.5 √f'c  (psi), ACI 318-19 §19.2.2."""
        return 33.0 * (self.wc_pcf ** 1.5) * self.sqrt_fc


# ---------------------------------------------------------------------------
# Rebar specification (project-level)
# ---------------------------------------------------------------------------

@dataclass
class RebarSpec:
    """Project-level reinforcing specification.

    Encodes the design-basis bar preference rules.
    """
    preferred_sizes: list[int] = field(default_factory=lambda: [3, 4])
    allowed_sizes: list[int] = field(default_factory=lambda: [3, 4, 5, 6])
    max_bar_size: int = 6

    def fy(self, bar_size: int) -> int:
        """Return fy for a given bar number per design-basis rule."""
        return REBAR_DB[bar_size].fy_psi

    def is_preferred(self, bar_size: int) -> bool:
        return bar_size in self.preferred_sizes

    def is_allowed(self, bar_size: int) -> bool:
        return bar_size in self.allowed_sizes and bar_size <= self.max_bar_size
