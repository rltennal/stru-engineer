"""Tests for the stability module."""

import pytest

from retaining_wall.geometry import StemGeometry, BaseSlabGeometry, WallGeometry
from retaining_wall.loads import SoilParameters, LoadCase, compute_earth_pressure_resultant
from retaining_wall.stability import (
    check_overturning,
    check_sliding,
    check_bearing,
    check_all_stability,
)


def _make_test_wall():
    """Standard test wall: 10 ft stem, 7.5 ft base."""
    stem = StemGeometry(height_ft=10.0, thickness_top_in=8.0, thickness_bot_in=12.0)
    base = BaseSlabGeometry(toe_ft=1.5, heel_ft=5.0, thickness_in=12.0)
    return WallGeometry(stem=stem, base=base)


def _make_test_soil():
    return SoilParameters(
        gamma_pcf=120.0,
        phi_deg=30.0,
        mu_sliding=0.45,
        allowable_bearing_psf=3000.0,
    )


class TestOverturning:
    def test_basic_pass(self):
        wall = _make_test_wall()
        soil = _make_test_soil()
        ep = compute_earth_pressure_resultant(soil, wall.total_height_ft)
        result = check_overturning(wall, soil, [ep])
        assert result.fs is not None
        assert result.fs > 1.0  # should pass for reasonable wall
        assert result.status in ("OK", "NG")

    def test_no_loads(self):
        wall = _make_test_wall()
        soil = _make_test_soil()
        result = check_overturning(wall, soil, [])
        assert result.status == "INCOMPLETE"


class TestSliding:
    def test_basic(self):
        wall = _make_test_wall()
        soil = _make_test_soil()
        ep = compute_earth_pressure_resultant(soil, wall.total_height_ft)
        result = check_sliding(wall, soil, [ep])
        assert result.fs is not None
        assert result.status in ("OK", "NG")

    def test_no_loads(self):
        wall = _make_test_wall()
        soil = _make_test_soil()
        result = check_sliding(wall, soil, [])
        assert result.status == "INCOMPLETE"

    def test_with_passive(self):
        wall = _make_test_wall()
        wall.embedment_ft = 2.0
        soil = SoilParameters(
            gamma_pcf=120.0,
            phi_deg=30.0,
            mu_sliding=0.45,
            passive_permitted=True,
            passive_gamma_pcf=120.0,
            passive_phi_deg=30.0,
        )
        ep = compute_earth_pressure_resultant(soil, wall.total_height_ft)
        result = check_sliding(wall, soil, [ep])
        assert "passive" in result.notes.lower() or result.notes == ""


class TestBearing:
    def test_with_allowable(self):
        wall = _make_test_wall()
        soil = _make_test_soil()
        ep = compute_earth_pressure_resultant(soil, wall.total_height_ft)
        result = check_bearing(wall, soil, [ep])
        assert result.status in ("OK", "NG")
        assert "q_max" in result.notes

    def test_without_allowable(self):
        wall = _make_test_wall()
        soil = SoilParameters(gamma_pcf=120.0, phi_deg=30.0)
        ep = compute_earth_pressure_resultant(soil, wall.total_height_ft)
        result = check_bearing(wall, soil, [ep])
        assert result.status == "INCOMPLETE"


class TestCheckAll:
    def test_returns_three_results(self):
        wall = _make_test_wall()
        soil = _make_test_soil()
        ep = compute_earth_pressure_resultant(soil, wall.total_height_ft)
        results = check_all_stability(wall, soil, [ep])
        assert len(results) == 3
        checks = {r.check for r in results}
        assert checks == {"Overturning", "Sliding", "Bearing"}
