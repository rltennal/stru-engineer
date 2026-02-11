"""Tests for the structural design module."""

import math
import pytest

from retaining_wall.materials import Concrete, REBAR_DB
from retaining_wall.structural import (
    design_flexure,
    min_temp_shrinkage_steel,
    min_flexural_steel,
    required_development_length,
    required_hook_development,
    PHI_FLEXURE,
    PHI_SHEAR,
)


class TestMinTempShrinkageSteel:
    def test_12in_slab(self):
        # 0.0018 * 12 * 12 = 0.2592
        assert min_temp_shrinkage_steel(12.0) == pytest.approx(0.2592)

    def test_8in_wall(self):
        assert min_temp_shrinkage_steel(8.0) == pytest.approx(0.1728)


class TestMinFlexuralSteel:
    def test_grade_40(self):
        fc = Concrete(fc_psi=3_000)
        As_min = min_flexural_steel(fc, 40_000, 12.0, 9.5)
        # max(3*sqrt(3000)/40000, 200/40000) * 12 * 9.5
        rho1 = 3 * math.sqrt(3000) / 40_000
        rho2 = 200 / 40_000
        expected = max(rho1, rho2) * 12.0 * 9.5
        assert As_min == pytest.approx(expected)

    def test_grade_60(self):
        fc = Concrete(fc_psi=3_000)
        As_min = min_flexural_steel(fc, 60_000, 12.0, 9.5)
        rho1 = 3 * math.sqrt(3000) / 60_000
        rho2 = 200 / 60_000
        expected = max(rho1, rho2) * 12.0 * 9.5
        assert As_min == pytest.approx(expected)


class TestDesignFlexure:
    def test_basic_stem(self):
        fc = Concrete(fc_psi=3_000)
        result = design_flexure(
            location="stem_base",
            h_in=12.0,
            Mu_lbft=5000.0,
            Vu_lb=1500.0,
            fc=fc,
            fy=40_000,
            cover_in=2.0,
        )
        assert result.bar is not None
        assert result.As_req > 0
        assert result.phi_Mn > 0
        assert result.phi_Vc > 0

    def test_flexure_adequacy(self):
        fc = Concrete(fc_psi=3_000)
        result = design_flexure(
            location="test",
            h_in=12.0,
            Mu_lbft=3000.0,
            Vu_lb=1000.0,
            fc=fc,
            fy=40_000,
            cover_in=2.0,
        )
        assert result.flexure_ok
        assert result.phi_Mn >= 3000.0

    def test_shear_check(self):
        fc = Concrete(fc_psi=3_000)
        # Low shear demand — should pass
        result = design_flexure(
            location="test",
            h_in=12.0,
            Mu_lbft=2000.0,
            Vu_lb=500.0,
            fc=fc,
            fy=40_000,
            cover_in=2.0,
        )
        assert result.shear_ok

    def test_zero_moment(self):
        fc = Concrete(fc_psi=3_000)
        result = design_flexure(
            location="test",
            h_in=12.0,
            Mu_lbft=0.0,
            Vu_lb=0.0,
            fc=fc,
            fy=40_000,
            cover_in=2.0,
        )
        # Still provides minimum steel
        assert result.bar is not None
        assert result.As_req == 0.0
        assert result.As_min > 0

    def test_summary_format(self):
        fc = Concrete(fc_psi=3_000)
        result = design_flexure(
            location="stem_base",
            h_in=12.0,
            Mu_lbft=3000.0,
            Vu_lb=1000.0,
            fc=fc,
            fy=40_000,
        )
        text = result.summary()
        assert "stem_base" in text


class TestDevelopmentLength:
    def test_bar_4(self):
        bar = REBAR_DB[4]
        fc = Concrete(fc_psi=3_000)
        ld = required_development_length(bar, fc)
        assert ld >= 12.0  # minimum
        assert ld > 0

    def test_top_bar_factor(self):
        bar = REBAR_DB[4]
        fc = Concrete(fc_psi=3_000)
        ld_bot = required_development_length(bar, fc, top_bar=False)
        ld_top = required_development_length(bar, fc, top_bar=True)
        assert ld_top > ld_bot

    def test_hook_development(self):
        bar = REBAR_DB[4]
        fc = Concrete(fc_psi=3_000)
        ldh = required_hook_development(bar, fc)
        assert ldh >= 6.0
        assert ldh >= 8 * bar.diameter_in
