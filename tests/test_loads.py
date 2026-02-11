"""Tests for the loads module."""

import math
import pytest

from retaining_wall.loads import (
    SoilParameters,
    WaterParameters,
    SurchargeLoad,
    SurchargeType,
    SeismicParameters,
    LoadCase,
    rankine_Ka_sloped,
    compute_earth_pressure_resultant,
    compute_hydrostatic_resultant,
    compute_surcharge_resultant,
    compute_seismic_increment,
)


class TestSoilParameters:
    def test_Ka_30deg(self):
        s = SoilParameters(gamma_pcf=120.0, phi_deg=30.0)
        # Ka = tan²(45 - 15) = tan²(30°) = 1/3
        assert s.Ka == pytest.approx(1.0 / 3.0, rel=1e-3)

    def test_K0_30deg(self):
        s = SoilParameters(gamma_pcf=120.0, phi_deg=30.0, condition="at_rest")
        assert s.K0 == pytest.approx(0.5)
        assert s.K == pytest.approx(0.5)

    def test_Kp_30deg(self):
        s = SoilParameters(gamma_pcf=120.0, phi_deg=30.0)
        # Kp = tan²(45 + 15) = tan²(60°) = 3.0
        assert s.Kp == pytest.approx(3.0, rel=1e-3)

    def test_invalid_condition(self):
        with pytest.raises(ValueError):
            SoilParameters(gamma_pcf=120.0, phi_deg=30.0, condition="passive")


class TestRankineSloped:
    def test_level(self):
        Ka = rankine_Ka_sloped(30.0, 0.0)
        expected = math.tan(math.pi / 4 - math.radians(15)) ** 2
        assert Ka == pytest.approx(expected, rel=1e-3)

    def test_sloped(self):
        Ka = rankine_Ka_sloped(30.0, 10.0)
        assert Ka > rankine_Ka_sloped(30.0, 0.0)  # slope increases Ka

    def test_slope_exceeds_phi(self):
        with pytest.raises(ValueError):
            rankine_Ka_sloped(30.0, 35.0)


class TestWaterParameters:
    def test_no_water_with_drainage(self):
        w = WaterParameters(drainage_provided=True)
        assert not w.has_water_case

    def test_water_with_gwl(self):
        w = WaterParameters(gwl_depth_ft=5.0)
        assert w.has_water_case

    def test_water_without_drainage_or_gwl(self):
        w = WaterParameters(drainage_provided=False)
        assert w.has_water_case  # IBC requires consideration


class TestLoadCase:
    def test_overturning_moment(self):
        lc = LoadCase(label="test", H_lbft=1000.0, arm_ft=5.0)
        assert lc.M_ot_lbft == pytest.approx(5000.0)

    def test_resisting_moment(self):
        lc = LoadCase(label="test", H_lbft=0, arm_ft=0, V_lbft=500, v_arm_ft=3.0)
        assert lc.M_resist_lbft == pytest.approx(1500.0)


class TestEarthPressureResultant:
    def test_basic(self):
        soil = SoilParameters(gamma_pcf=120.0, phi_deg=30.0)
        lc = compute_earth_pressure_resultant(soil, 10.0)
        # P = 0.5 * (1/3) * 120 * 100 = 2000 lb/ft
        assert lc.H_lbft == pytest.approx(2000.0, rel=1e-2)
        assert lc.arm_ft == pytest.approx(10.0 / 3.0)

    def test_sloped_backfill(self):
        soil = SoilParameters(gamma_pcf=120.0, phi_deg=30.0)
        lc = compute_earth_pressure_resultant(soil, 10.0, backfill_slope_deg=10.0)
        assert lc.H_lbft > 0
        assert lc.V_lbft > 0  # inclined resultant has vertical component


class TestHydrostaticResultant:
    def test_with_water(self):
        water = WaterParameters(gwl_depth_ft=4.0)
        lc = compute_hydrostatic_resultant(water, 10.0)
        assert lc is not None
        # hw = 6 ft, Pw = 0.5 * 62.4 * 36 = 1123.2
        assert lc.H_lbft == pytest.approx(1123.2)

    def test_no_water(self):
        water = WaterParameters(drainage_provided=True)
        lc = compute_hydrostatic_resultant(water, 10.0)
        assert lc is None

    def test_gwl_below_base(self):
        water = WaterParameters(gwl_depth_ft=15.0)
        lc = compute_hydrostatic_resultant(water, 10.0)
        assert lc is None


class TestSurchargeResultant:
    def test_uniform(self):
        soil = SoilParameters(gamma_pcf=120.0, phi_deg=30.0)
        sur = SurchargeLoad(
            load_type=SurchargeType.UNIFORM, magnitude_psf=250.0
        )
        lc = compute_surcharge_resultant(sur, soil, 10.0)
        assert lc is not None
        # H = K * q * H = (1/3) * 250 * 10 = 833.3
        assert lc.H_lbft == pytest.approx(833.3, rel=1e-2)

    def test_zero_surcharge(self):
        soil = SoilParameters(gamma_pcf=120.0, phi_deg=30.0)
        sur = SurchargeLoad(magnitude_psf=0.0)
        lc = compute_surcharge_resultant(sur, soil, 10.0)
        assert lc is None


class TestSeismicIncrement:
    def test_no_seismic(self):
        soil = SoilParameters(gamma_pcf=120.0, phi_deg=30.0)
        seis = SeismicParameters()
        lc = compute_seismic_increment(soil, seis, 10.0)
        assert lc is None

    def test_with_seismic(self):
        soil = SoilParameters(gamma_pcf=120.0, phi_deg=30.0)
        seis = SeismicParameters(kh=0.15, kv=0.0, use_mononobe_okabe=True)
        lc = compute_seismic_increment(soil, seis, 10.0)
        assert lc is not None
        assert lc.H_lbft > 0
        assert lc.arm_ft == pytest.approx(6.0)  # 0.6 * H
