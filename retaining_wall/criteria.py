"""
Design criteria module — project-level input template.

This is the single entry point where all project-specific data is defined.
Every field has an explicit placeholder state so the designer knows exactly
what remains to be provided before a design can be finalised.

Corresponds to section 5 of the design basis:
  Geometry, Soil, Water, Surcharge, Seismic, Material exposure.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from retaining_wall.materials import Concrete, RebarSpec
from retaining_wall.geometry import StemGeometry, BaseSlabGeometry, ShearKey, WallGeometry
from retaining_wall.loads import SoilParameters, WaterParameters, SurchargeLoad, SeismicParameters


# ---------------------------------------------------------------------------
# Exposure / durability placeholders
# ---------------------------------------------------------------------------

@dataclass
class ExposureConditions:
    """ACI 318-19 exposure class assignments (placeholders until known).

    Exposure classes drive minimum f'c, maximum w/c, and minimum cover.
    """
    # Freeze-thaw: F0, F1, F2, F3
    freeze_thaw: str = ""
    # Sulfate: S0, S1, S2, S3
    sulfate: str = ""
    # Corrosion (reinforcement): C0, C1, C2
    corrosion: str = ""
    # Water permeability: W0, W1, W2
    water_perm: str = ""
    # Weathering: see IBC Table 1904.2.3
    weathering: str = ""

    @property
    def is_complete(self) -> bool:
        return all([self.freeze_thaw, self.sulfate, self.corrosion])

    def required_cover_in(self) -> float:
        """Minimum clear cover (in) based on exposure.

        Defaults to 2″ for soil contact (ACI 318-19 Table 20.6.1.3.1)
        if exposure is not fully defined.
        """
        if not self.is_complete:
            return 2.0  # conservative default for cast against soil
        # Simplified lookup — extend as needed
        if self.corrosion in ("C1", "C2"):
            return 2.0
        return 1.5


# ---------------------------------------------------------------------------
# Design criteria (master input)
# ---------------------------------------------------------------------------

@dataclass
class DesignCriteria:
    """Complete set of project design criteria for a cantilever retaining wall.

    Every field that requires project-specific data has a default of None or
    a neutral placeholder.  Call :meth:`validate` to get a list of what is
    still missing.
    """

    # --- Geometry ---
    retained_height_ft: Optional[float] = None
    stem_thickness_top_in: float = 8.0
    stem_thickness_bot_in: float = 12.0
    base_toe_ft: float = 1.0
    base_heel_ft: Optional[float] = None  # placeholder — size for stability
    base_thickness_in: float = 12.0
    backfill_slope_deg: float = 0.0
    embedment_ft: float = 0.0
    wall_length_ft: Optional[float] = None  # total wall length (for quantity take-off)

    # --- Shear key (Strategy B — optional) ---
    use_shear_key: bool = False
    shear_key_depth_in: float = 12.0
    shear_key_width_in: float = 12.0

    # --- Soil ---
    backfill_gamma_pcf: Optional[float] = None
    backfill_phi_deg: Optional[float] = None
    backfill_cohesion_psf: float = 0.0
    soil_condition: str = "active"
    mu_sliding: float = 0.45
    allowable_bearing_psf: Optional[float] = None
    passive_permitted: bool = False
    passive_gamma_pcf: Optional[float] = None
    passive_phi_deg: Optional[float] = None

    # --- Water ---
    gwl_depth_ft: Optional[float] = None
    drainage_provided: bool = False

    # --- Surcharge ---
    surcharge_psf: float = 0.0

    # --- Seismic ---
    sdc: str = ""
    sds: float = 0.0
    sd1: float = 0.0
    kh: float = 0.0
    kv: float = 0.0
    use_mononobe_okabe: bool = False

    # --- Materials ---
    fc_psi: int = 3_000
    gamma_conc_pcf: float = 150.0
    rebar_max_bar_size: int = 6

    # --- Exposure ---
    exposure: ExposureConditions = field(default_factory=ExposureConditions)

    # --- Stability FS ---
    fs_overturning: float = 1.5
    fs_sliding: float = 1.5

    # -----------------------------------------------------------------------
    # Validation
    # -----------------------------------------------------------------------

    def validate(self) -> list[str]:
        """Return a list of missing or incomplete criteria.

        An empty list means the criteria set is complete enough to run
        a full design.
        """
        missing: list[str] = []
        if self.retained_height_ft is None:
            missing.append("retained_height_ft — wall retained height (ft)")
        if self.base_heel_ft is None:
            missing.append("base_heel_ft — heel projection (ft)")
        if self.backfill_gamma_pcf is None:
            missing.append("backfill_gamma_pcf — backfill unit weight (pcf)")
        if self.backfill_phi_deg is None:
            missing.append("backfill_phi_deg — backfill friction angle (°)")
        if self.allowable_bearing_psf is None:
            missing.append("allowable_bearing_psf — allowable bearing (psf)")
        if not self.drainage_provided and self.gwl_depth_ft is None:
            missing.append(
                "gwl_depth_ft or drainage_provided — "
                "water case undetermined (IBC requires consideration)"
            )
        if not self.exposure.is_complete:
            missing.append("exposure classes — needed for cover and durability")
        return missing

    @property
    def is_complete(self) -> bool:
        return len(self.validate()) == 0

    # -----------------------------------------------------------------------
    # Object builders
    # -----------------------------------------------------------------------

    def build_concrete(self) -> Concrete:
        return Concrete(fc_psi=self.fc_psi, wc_pcf=self.gamma_conc_pcf)

    def build_rebar_spec(self) -> RebarSpec:
        return RebarSpec(max_bar_size=self.rebar_max_bar_size)

    def build_wall_geometry(self) -> WallGeometry:
        """Build a WallGeometry from the criteria.

        Raises ValueError if minimum geometry fields are not set.
        """
        if self.retained_height_ft is None:
            raise ValueError("retained_height_ft is required")
        heel = self.base_heel_ft if self.base_heel_ft is not None else 0.0

        stem = StemGeometry(
            height_ft=self.retained_height_ft,
            thickness_top_in=self.stem_thickness_top_in,
            thickness_bot_in=self.stem_thickness_bot_in,
        )
        base = BaseSlabGeometry(
            toe_ft=self.base_toe_ft,
            heel_ft=heel,
            thickness_in=self.base_thickness_in,
        )
        shear_key = None
        if self.use_shear_key:
            shear_key = ShearKey(
                depth_in=self.shear_key_depth_in,
                width_in=self.shear_key_width_in,
            )
        return WallGeometry(
            stem=stem,
            base=base,
            shear_key=shear_key,
            backfill_slope_deg=self.backfill_slope_deg,
            embedment_ft=self.embedment_ft,
        )

    def build_soil(self) -> SoilParameters:
        if self.backfill_gamma_pcf is None or self.backfill_phi_deg is None:
            raise ValueError("soil parameters are required")
        return SoilParameters(
            gamma_pcf=self.backfill_gamma_pcf,
            phi_deg=self.backfill_phi_deg,
            cohesion_psf=self.backfill_cohesion_psf,
            condition=self.soil_condition,
            mu_sliding=self.mu_sliding,
            allowable_bearing_psf=self.allowable_bearing_psf,
            passive_permitted=self.passive_permitted,
            passive_gamma_pcf=self.passive_gamma_pcf,
            passive_phi_deg=self.passive_phi_deg,
        )

    def build_water(self) -> WaterParameters:
        return WaterParameters(
            gwl_depth_ft=self.gwl_depth_ft,
            drainage_provided=self.drainage_provided,
        )

    def build_surcharge(self) -> SurchargeLoad:
        return SurchargeLoad(magnitude_psf=self.surcharge_psf)

    def build_seismic(self) -> SeismicParameters:
        return SeismicParameters(
            sdc=self.sdc,
            sds=self.sds,
            sd1=self.sd1,
            kh=self.kh,
            kv=self.kv,
            use_mononobe_okabe=self.use_mononobe_okabe,
        )

    def cover_in(self) -> float:
        """Minimum clear cover (in) for design."""
        return self.exposure.required_cover_in()

    # -----------------------------------------------------------------------
    # Design basis narrative
    # -----------------------------------------------------------------------

    def design_basis_narrative(self) -> str:
        """Generate the Section 6 design basis narrative text."""
        missing = self.validate()
        status = "COMPLETE" if not missing else "INCOMPLETE — see placeholders below"

        lines = [
            "=" * 72,
            "CANTILEVER RETAINING WALL — DESIGN BASIS",
            "=" * 72,
            "",
            f"Status: {status}",
            "",
            "Wall system: Cast-in-place reinforced concrete L-shaped cantilever",
            "retaining wall (stem + base slab with heel and toe).",
            "",
            "Codes: IBC 2021, ACI 318-19.",
            "",
            "Stability: Service-level checks per IBC practice:",
            f"  FS_overturning ≥ {self.fs_overturning}",
            f"  FS_sliding     ≥ {self.fs_sliding}",
            f"  Bearing        ≤ allowable ({self.allowable_bearing_psf or 'TBD'} psf)",
            "",
            "Structural strength: ACI 318-19 strength design (flexure, one-way",
            "shear, detailing). Min T&S reinforcement ρ ≥ 0.0018.",
            "",
            f"Materials: f'c = {self.fc_psi} psi.  Rebar: #4 Gr.40 or smaller,",
            f"  #5 Gr.60 or larger; max bar = #{self.rebar_max_bar_size}.",
            "",
        ]

        if missing:
            lines.append("MISSING CRITERIA (must be provided before final design):")
            for m in missing:
                lines.append(f"  • {m}")
            lines.append("")

        lines.append("=" * 72)
        return "\n".join(lines)
