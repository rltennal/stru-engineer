"""
Geometry module — wall cross-section definitions.

Defines the L-shaped cantilever retaining wall geometry:
- Stem (vertical element)
- Base slab (heel + toe)
- Optional shear key

Follows the "heel-first philosophy" (Strategy A): bias geometry toward a
heel-dominant base to efficiently mobilize backfill weight for stability.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class StemGeometry:
    """Vertical stem of the cantilever wall.

    Parameters
    ----------
    height_ft : float
        Total stem height measured from top of base slab to top of wall (ft).
    thickness_top_in : float
        Stem thickness at the top (in). Minimum practical ≈ 8″.
    thickness_bot_in : float
        Stem thickness at the base (in). May equal top thickness for
        constant-section walls.
    """
    height_ft: float
    thickness_top_in: float = 8.0
    thickness_bot_in: float = 12.0

    def __post_init__(self) -> None:
        if self.height_ft <= 0:
            raise ValueError("stem height must be > 0")
        if self.thickness_top_in < 6:
            raise ValueError("stem top thickness unreasonably thin (< 6 in)")
        if self.thickness_bot_in < self.thickness_top_in:
            raise ValueError("stem base thickness must be ≥ top thickness")

    @property
    def height_in(self) -> float:
        return self.height_ft * 12.0

    @property
    def taper_per_ft(self) -> float:
        """Taper rate (in/ft) — 0 for constant section."""
        return (self.thickness_bot_in - self.thickness_top_in) / self.height_ft

    def thickness_at(self, dist_from_top_ft: float) -> float:
        """Stem thickness (in) at a given distance below the top."""
        return self.thickness_top_in + self.taper_per_ft * dist_from_top_ft

    @property
    def avg_thickness_in(self) -> float:
        return (self.thickness_top_in + self.thickness_bot_in) / 2.0

    def self_weight_per_ft(self, gamma_conc_pcf: float = 150.0) -> float:
        """Stem self-weight per lineal foot of wall (lb/ft).

        Treats the cross-section as a trapezoid.
        """
        avg_t_ft = self.avg_thickness_in / 12.0
        return gamma_conc_pcf * avg_t_ft * self.height_ft


@dataclass
class BaseSlabGeometry:
    """Base slab (footing) of the cantilever wall.

    Geometry is defined by toe length, heel length, and slab thickness.
    The stem sits at the junction of toe and heel.

    Parameters
    ----------
    toe_ft : float
        Toe projection from the front face of the stem (ft).
    heel_ft : float
        Heel projection from the back face of the stem (ft).
    thickness_in : float
        Base slab thickness (in). Minimum practical ≈ 10″–12″.
    """
    toe_ft: float = 1.0
    heel_ft: float = 4.0
    thickness_in: float = 12.0

    def __post_init__(self) -> None:
        if self.toe_ft < 0:
            raise ValueError("toe length must be ≥ 0")
        if self.heel_ft < 0:
            raise ValueError("heel length must be ≥ 0")
        if self.thickness_in < 8:
            raise ValueError("base slab thickness unreasonably thin (< 8 in)")

    @property
    def thickness_ft(self) -> float:
        return self.thickness_in / 12.0

    def total_width_ft(self, stem_thickness_bot_in: float) -> float:
        """Total base slab width (ft) including stem width at base."""
        return self.toe_ft + stem_thickness_bot_in / 12.0 + self.heel_ft

    def self_weight_per_ft(
        self, stem_thickness_bot_in: float, gamma_conc_pcf: float = 150.0
    ) -> float:
        """Base slab self-weight per lineal foot of wall (lb/ft)."""
        width = self.total_width_ft(stem_thickness_bot_in)
        return gamma_conc_pcf * width * self.thickness_ft

    def toe_moment_arm_ft(self, stem_thickness_bot_in: float) -> float:
        """Distance from toe edge to centroid of toe slab (ft)."""
        return self.toe_ft / 2.0

    def heel_moment_arm_ft(self, stem_thickness_bot_in: float) -> float:
        """Distance from toe edge to centroid of heel slab (ft)."""
        stem_w_ft = stem_thickness_bot_in / 12.0
        return self.toe_ft + stem_w_ft + self.heel_ft / 2.0


@dataclass
class ShearKey:
    """Optional shear key below the base slab (Strategy B).

    A shear key improves sliding resistance by engaging passive soil
    pressure at a greater depth. Treat as an alternate — not a default.

    Parameters
    ----------
    depth_in : float
        Key depth below bottom of base slab (in).
    width_in : float
        Key width (in).
    offset_from_toe_ft : float
        Horizontal distance from toe edge to centre of key (ft).
        Typically placed below the stem or slightly toward the heel.
    """
    depth_in: float = 12.0
    width_in: float = 12.0
    offset_from_toe_ft: Optional[float] = None  # set during assembly

    def __post_init__(self) -> None:
        if self.depth_in <= 0 or self.width_in <= 0:
            raise ValueError("shear key dimensions must be > 0")


@dataclass
class WallGeometry:
    """Complete wall geometry assembly.

    Combines stem, base slab, and optional shear key into a single object
    that downstream modules reference for dimensions and weight calculations.
    """
    stem: StemGeometry
    base: BaseSlabGeometry
    shear_key: Optional[ShearKey] = None
    backfill_slope_deg: float = 0.0  # slope angle of backfill behind wall (°)
    embedment_ft: float = 0.0        # depth of soil in front of wall (ft)

    # --- derived helpers ---------------------------------------------------

    @property
    def total_height_ft(self) -> float:
        """Total height from bottom of base slab to top of stem (ft)."""
        return self.stem.height_ft + self.base.thickness_ft

    @property
    def base_width_ft(self) -> float:
        """Total footing width (ft)."""
        return self.base.total_width_ft(self.stem.thickness_bot_in)

    @property
    def retained_height_ft(self) -> float:
        """Height of soil retained (top of base to top of stem)."""
        return self.stem.height_ft

    @property
    def stem_base_offset_ft(self) -> float:
        """Horizontal distance from toe edge to back face of stem (ft)."""
        return self.base.toe_ft + self.stem.thickness_bot_in / 12.0

    # --- weight helpers (concrete only) ------------------------------------

    def concrete_weights(self, gamma_conc_pcf: float = 150.0) -> dict[str, float]:
        """Return component concrete weights per lineal foot (lb/ft).

        Keys: 'stem', 'base', 'shear_key', 'total'.
        """
        w_stem = self.stem.self_weight_per_ft(gamma_conc_pcf)
        w_base = self.base.self_weight_per_ft(self.stem.thickness_bot_in, gamma_conc_pcf)
        w_key = 0.0
        if self.shear_key is not None:
            key = self.shear_key
            w_key = gamma_conc_pcf * (key.depth_in / 12.0) * (key.width_in / 12.0)
        return {
            "stem": w_stem,
            "base": w_base,
            "shear_key": w_key,
            "total": w_stem + w_base + w_key,
        }

    def moment_arms_from_toe(self, gamma_conc_pcf: float = 150.0) -> dict[str, float]:
        """Moment arms (ft) of each concrete component about the toe.

        Used in overturning/stability calculations.
        """
        # Stem centroid: toe_ft + stem_thickness/2 (approx for tapered)
        stem_arm = self.base.toe_ft + self.stem.avg_thickness_in / 24.0  # midpoint
        # Base slab centroid: half the total width
        base_arm = self.base_width_ft / 2.0
        # Shear key
        key_arm = 0.0
        if self.shear_key is not None:
            if self.shear_key.offset_from_toe_ft is not None:
                key_arm = self.shear_key.offset_from_toe_ft
            else:
                key_arm = self.stem_base_offset_ft - self.stem.thickness_bot_in / 24.0
        return {"stem": stem_arm, "base": base_arm, "shear_key": key_arm}
