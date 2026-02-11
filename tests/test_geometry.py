"""Tests for the geometry module."""

import pytest

from retaining_wall.geometry import (
    StemGeometry,
    BaseSlabGeometry,
    ShearKey,
    WallGeometry,
)


class TestStemGeometry:
    def test_basic(self):
        s = StemGeometry(height_ft=10.0, thickness_top_in=8.0, thickness_bot_in=12.0)
        assert s.height_in == 120.0
        assert s.avg_thickness_in == 10.0

    def test_taper(self):
        s = StemGeometry(height_ft=10.0, thickness_top_in=8.0, thickness_bot_in=12.0)
        assert s.taper_per_ft == pytest.approx(0.4)
        assert s.thickness_at(5.0) == pytest.approx(10.0)

    def test_constant_section(self):
        s = StemGeometry(height_ft=8.0, thickness_top_in=10.0, thickness_bot_in=10.0)
        assert s.taper_per_ft == 0.0

    def test_self_weight(self):
        s = StemGeometry(height_ft=10.0, thickness_top_in=12.0, thickness_bot_in=12.0)
        # 150 pcf * (12/12 ft) * 10 ft = 1500 lb/ft
        assert s.self_weight_per_ft(150.0) == pytest.approx(1500.0)

    def test_rejects_zero_height(self):
        with pytest.raises(ValueError):
            StemGeometry(height_ft=0.0)

    def test_rejects_thin_top(self):
        with pytest.raises(ValueError):
            StemGeometry(height_ft=10.0, thickness_top_in=4.0)

    def test_rejects_bot_thinner_than_top(self):
        with pytest.raises(ValueError):
            StemGeometry(height_ft=10.0, thickness_top_in=12.0, thickness_bot_in=10.0)


class TestBaseSlabGeometry:
    def test_total_width(self):
        b = BaseSlabGeometry(toe_ft=2.0, heel_ft=5.0, thickness_in=12.0)
        # stem_bot = 12″ = 1 ft → total = 2 + 1 + 5 = 8 ft
        assert b.total_width_ft(12.0) == pytest.approx(8.0)

    def test_self_weight(self):
        b = BaseSlabGeometry(toe_ft=2.0, heel_ft=5.0, thickness_in=12.0)
        # width=8 ft, thickness=1 ft, 150 pcf → 1200 lb/ft
        assert b.self_weight_per_ft(12.0, 150.0) == pytest.approx(1200.0)

    def test_rejects_negative_toe(self):
        with pytest.raises(ValueError):
            BaseSlabGeometry(toe_ft=-1.0)

    def test_rejects_thin_slab(self):
        with pytest.raises(ValueError):
            BaseSlabGeometry(thickness_in=6.0)


class TestShearKey:
    def test_creation(self):
        k = ShearKey(depth_in=12.0, width_in=10.0)
        assert k.depth_in == 12.0

    def test_rejects_zero_depth(self):
        with pytest.raises(ValueError):
            ShearKey(depth_in=0.0)


class TestWallGeometry:
    def _make_wall(self):
        stem = StemGeometry(height_ft=10.0, thickness_top_in=8.0, thickness_bot_in=12.0)
        base = BaseSlabGeometry(toe_ft=1.5, heel_ft=5.0, thickness_in=12.0)
        return WallGeometry(stem=stem, base=base)

    def test_total_height(self):
        w = self._make_wall()
        assert w.total_height_ft == pytest.approx(11.0)

    def test_base_width(self):
        w = self._make_wall()
        # 1.5 + 1.0 + 5.0 = 7.5
        assert w.base_width_ft == pytest.approx(7.5)

    def test_concrete_weights(self):
        w = self._make_wall()
        cw = w.concrete_weights(150.0)
        assert cw["stem"] > 0
        assert cw["base"] > 0
        assert cw["shear_key"] == 0.0
        assert cw["total"] == pytest.approx(cw["stem"] + cw["base"])

    def test_with_shear_key(self):
        stem = StemGeometry(height_ft=10.0)
        base = BaseSlabGeometry(toe_ft=1.5, heel_ft=5.0)
        key = ShearKey(depth_in=12.0, width_in=12.0)
        w = WallGeometry(stem=stem, base=base, shear_key=key)
        cw = w.concrete_weights(150.0)
        assert cw["shear_key"] > 0
