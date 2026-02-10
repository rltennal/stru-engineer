"""
Structural design module — ACI 318-19 strength design for wall sections.

Covers the four critical sections of a cantilever retaining wall:
  1. Stem at base (flexure + shear)
  2. Heel slab at stem face (top steel critical)
  3. Toe slab at stem face (bottom steel critical)
  4. Shear key (shear + flexure + shear friction)

Material constraints are enforced via the materials module.

Key ACI 318-19 references:
  - Flexural strength: Chapter 22 (φMn ≥ Mu)
  - One-way shear: §22.5 (φVc ≥ Vu)
  - Min flexural reinforcement: §9.6.1 (beams/one-way slabs)
  - Temperature/shrinkage: §24.4 (ρ ≥ 0.0018 for deformed bars)
  - Development length: §25.4
  - Maximum spacing: §11.7.2 (lesser of 3h or 18″ for primary, 5h or 18″ for T&S)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

from retaining_wall.materials import Concrete, BarProperties, REBAR_DB, select_bar


# ---------------------------------------------------------------------------
# Section design result
# ---------------------------------------------------------------------------

@dataclass
class SectionDesign:
    """Result of designing a single rectangular section for flexure + shear.

    Attributes
    ----------
    location : str
        Where this section is in the wall (e.g. "stem_base").
    h_in : float
        Total section depth (in).
    b_in : float
        Section width (in per ft of wall = 12).
    cover_in : float
        Clear cover (in).
    d_in : float
        Effective depth (in).
    Mu_lbft : float
        Factored moment demand (lb·ft per ft of wall).
    Vu_lb : float
        Factored shear demand (lb per ft of wall).
    As_req : float
        Required flexural steel area (in²/ft).
    As_min : float
        Minimum flexural steel area (in²/ft).
    As_ts : float
        Temperature/shrinkage steel area (in²/ft).
    bar : BarProperties | None
        Selected bar.
    spacing_in : float | None
        Centre-to-centre spacing (in).
    phi_Mn : float
        Design flexural strength φMn (lb·ft per ft of wall).
    phi_Vc : float
        Design shear strength φVc (lb per ft of wall).
    shear_ok : bool
        True if φVc ≥ Vu.
    flexure_ok : bool
        True if φMn ≥ Mu.
    notes : str
        Any warnings or comments.
    """
    location: str
    h_in: float
    b_in: float = 12.0  # per foot of wall
    cover_in: float = 2.0
    d_in: float = 0.0
    Mu_lbft: float = 0.0
    Vu_lb: float = 0.0
    As_req: float = 0.0
    As_min: float = 0.0
    As_ts: float = 0.0
    bar: Optional[BarProperties] = None
    spacing_in: Optional[float] = None
    phi_Mn: float = 0.0
    phi_Vc: float = 0.0
    shear_ok: bool = False
    flexure_ok: bool = False
    notes: str = ""

    def summary(self) -> str:
        bar_label = self.bar.label if self.bar else "—"
        sp = f"{self.spacing_in:.1f}" if self.spacing_in else "—"
        return (
            f"[{self.location}]  h={self.h_in}″  d={self.d_in:.1f}″  "
            f"Mu={self.Mu_lbft:.0f} lb·ft  Vu={self.Vu_lb:.0f} lb\n"
            f"  As_req={self.As_req:.3f} in²/ft  → {bar_label} @ {sp}″ o.c.\n"
            f"  φMn={self.phi_Mn:.0f} lb·ft ({'OK' if self.flexure_ok else 'NG'})  "
            f"φVc={self.phi_Vc:.0f} lb ({'OK' if self.shear_ok else 'NG'})"
        )


# ---------------------------------------------------------------------------
# Flexural design
# ---------------------------------------------------------------------------

PHI_FLEXURE = 0.90  # ACI 318-19 Table 21.2.1 — tension-controlled
PHI_SHEAR = 0.75    # ACI 318-19 Table 21.2.1


def _as_required_flexure(
    Mu_lbin: float,
    fc: Concrete,
    fy: int,
    b: float,
    d: float,
    phi: float = PHI_FLEXURE,
) -> float:
    """Required flexural steel area (in²) for a rectangular section.

    Uses the quadratic from Whitney stress block:
        φMn = φ · As · fy · (d − a/2)
        a = As · fy / (0.85 · f'c · b)

    Solved for As given Mu.
    """
    Mu = abs(Mu_lbin)
    if Mu == 0:
        return 0.0

    fc_psi = fc.fc_psi
    # Rn = Mu / (φ · b · d²)
    Rn = Mu / (phi * b * d ** 2)
    # ρ = (0.85·f'c / fy) · (1 − √(1 − 2·Rn / (0.85·f'c)))
    inner = 1.0 - 2.0 * Rn / (0.85 * fc_psi)
    if inner < 0:
        raise ValueError(
            f"Section too small for Mu={Mu:.0f} lb·in "
            f"(h insufficient or f'c too low)."
        )
    rho = (0.85 * fc_psi / fy) * (1.0 - math.sqrt(inner))
    return rho * b * d


def _phi_Mn(
    As: float,
    fc: Concrete,
    fy: int,
    b: float,
    d: float,
    phi: float = PHI_FLEXURE,
) -> float:
    """Compute φMn (lb·in) for given As in a rectangular section."""
    a = As * fy / (0.85 * fc.fc_psi * b)
    return phi * As * fy * (d - a / 2.0)


def min_flexural_steel(fc: Concrete, fy: int, b: float, d: float) -> float:
    """ACI 318-19 §9.6.1.2 — minimum As for one-way slabs/beams.

    As_min = max(3√f'c / fy, 200/fy) · b · d
    """
    rho_min = max(3.0 * fc.sqrt_fc / fy, 200.0 / fy)
    return rho_min * b * d


def min_temp_shrinkage_steel(h: float, b: float = 12.0) -> float:
    """ACI 318-19 §24.4.3.2 — temperature/shrinkage reinforcement.

    As_ts = 0.0018 · Ag  for deformed bars (Grade 40 or 60).
    Returns in²/ft when b = 12.
    """
    return 0.0018 * b * h


def design_flexure(
    location: str,
    h_in: float,
    Mu_lbft: float,
    Vu_lb: float,
    fc: Concrete,
    fy: int,
    cover_in: float = 2.0,
    bar_dia_in: float = 0.5,
    max_bar_size: int = 6,
) -> SectionDesign:
    """Design a rectangular section for flexure and check shear.

    Parameters
    ----------
    location : str
        Section identifier (e.g. "stem_base", "heel", "toe").
    h_in : float
        Total section depth (in).
    Mu_lbft : float
        Factored moment demand (lb·ft/ft).
    Vu_lb : float
        Factored shear demand (lb/ft).
    fc : Concrete
    fy : int
        Yield strength of the tension bar (psi).
    cover_in : float
        Clear cover (in).
    bar_dia_in : float
        Assumed bar diameter for initial d estimate (in).
    max_bar_size : int
        Largest bar to consider.
    """
    b = 12.0  # per foot of wall
    d = h_in - cover_in - bar_dia_in / 2.0
    if d <= 0:
        return SectionDesign(
            location=location, h_in=h_in, cover_in=cover_in, d_in=d,
            Mu_lbft=Mu_lbft, Vu_lb=Vu_lb,
            notes="Effective depth d <= 0 — section too thin for cover.",
        )
    Mu_lbin = Mu_lbft * 12.0  # convert to lb·in

    # Required steel
    try:
        As_req = _as_required_flexure(Mu_lbin, fc, fy, b, d)
    except ValueError as exc:
        As_min_flex = min_flexural_steel(fc, fy, b, d)
        As_ts = min_temp_shrinkage_steel(h_in, b)
        return SectionDesign(
            location=location, h_in=h_in, cover_in=cover_in, d_in=d,
            Mu_lbft=Mu_lbft, Vu_lb=Vu_lb,
            As_req=0, As_min=As_min_flex, As_ts=As_ts,
            notes=f"Section too small: {exc}",
        )

    # Minimums
    As_min_flex = min_flexural_steel(fc, fy, b, d)
    As_ts = min_temp_shrinkage_steel(h_in, b)
    As_govern = max(As_req, As_min_flex, As_ts)

    # Bar selection
    try:
        bar, spacing = select_bar(As_govern, h_in, cover_in, max_bar_size=max_bar_size)
    except ValueError as exc:
        return SectionDesign(
            location=location,
            h_in=h_in,
            cover_in=cover_in,
            d_in=d,
            Mu_lbft=Mu_lbft,
            Vu_lb=Vu_lb,
            As_req=As_req,
            As_min=As_min_flex,
            As_ts=As_ts,
            notes=f"Bar selection failed: {exc}",
        )

    # Recompute d with actual bar
    d_actual = h_in - cover_in - bar.diameter_in / 2.0
    As_provided = bar.area_in2 * 12.0 / spacing

    # Capacity
    phi_mn = _phi_Mn(As_provided, fc, bar.fy_psi, b, d_actual) / 12.0  # lb·ft

    # Shear capacity: φVc = φ · 2λ√f'c · b · d  (ACI 318-19 §22.5.5.1)
    phi_vc = PHI_SHEAR * 2.0 * fc.lambda_factor * fc.sqrt_fc * b * d_actual

    return SectionDesign(
        location=location,
        h_in=h_in,
        cover_in=cover_in,
        d_in=d_actual,
        Mu_lbft=Mu_lbft,
        Vu_lb=Vu_lb,
        As_req=As_req,
        As_min=As_min_flex,
        As_ts=As_ts,
        bar=bar,
        spacing_in=spacing,
        phi_Mn=phi_mn,
        phi_Vc=phi_vc,
        shear_ok=phi_vc >= Vu_lb,
        flexure_ok=phi_mn >= Mu_lbft,
    )


# ---------------------------------------------------------------------------
# Development length
# ---------------------------------------------------------------------------

def required_development_length(
    bar: BarProperties,
    fc: Concrete,
    cover_in: float = 2.0,
    top_bar: bool = False,
    epoxy_coated: bool = False,
    lightweight: bool = False,
) -> float:
    """Simplified development length ld per ACI 318-19 §25.4.2.3.

    Uses the simplified equations (not the general equation with Ktr).

    Returns ld in inches.
    """
    fy = bar.fy_psi
    db = bar.diameter_in
    lam = 0.75 if lightweight else 1.0  # λ
    psi_t = 1.3 if top_bar else 1.0     # ψ_t (casting position)
    psi_e = 1.5 if epoxy_coated else 1.0  # ψ_e (coating)
    # ψ_t · ψ_e need not exceed 1.7
    psi_te = min(psi_t * psi_e, 1.7)

    sqrt_fc = fc.sqrt_fc

    # Simplified: for #6 and smaller with clear spacing ≥ db and cover ≥ db
    if bar.size_num <= 6:
        ld = (fy * psi_te / (25 * lam * sqrt_fc)) * db
    else:
        ld = (fy * psi_te / (20 * lam * sqrt_fc)) * db

    # Minimum 12 inches
    return max(ld, 12.0)


def required_hook_development(
    bar: BarProperties,
    fc: Concrete,
    cover_in: float = 2.0,
    lightweight: bool = False,
) -> float:
    """Standard hook development length ldh per ACI 318-19 §25.4.3.

    ldh = (fy · ψ_e · ψ_c · ψ_r / (55 · λ · √f'c)) · db
    Simplified with no epoxy coating and ψ_c = ψ_r = 1.0.

    Returns ldh in inches (≥ max(8db, 6″)).
    """
    fy = bar.fy_psi
    db = bar.diameter_in
    lam = 0.75 if lightweight else 1.0
    sqrt_fc = fc.sqrt_fc

    ldh = (fy / (55.0 * lam * sqrt_fc)) * db
    return max(ldh, 8 * db, 6.0)
