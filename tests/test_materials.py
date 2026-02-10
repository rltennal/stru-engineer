"""Tests for the materials module."""

import math
import pytest

from retaining_wall.materials import (
    Concrete,
    RebarSpec,
    REBAR_DB,
    BarProperties,
    select_bar,
)


class TestBarDatabase:
    def test_all_sizes_present(self):
        for size in (3, 4, 5, 6, 7, 8, 9, 10, 11):
            assert size in REBAR_DB

    def test_grade_40_for_4_and_smaller(self):
        for size in (3, 4):
            assert REBAR_DB[size].fy_psi == 40_000

    def test_grade_60_for_5_and_larger(self):
        for size in (5, 6, 7, 8, 9, 10, 11):
            assert REBAR_DB[size].fy_psi == 60_000

    def test_bar_areas(self):
        assert REBAR_DB[3].area_in2 == pytest.approx(0.11)
        assert REBAR_DB[4].area_in2 == pytest.approx(0.20)
        assert REBAR_DB[5].area_in2 == pytest.approx(0.31)

    def test_label(self):
        assert REBAR_DB[4].label == "#4"


class TestSelectBar:
    def test_selects_smallest_feasible_bar(self):
        bar, spacing = select_bar(0.20, 12.0, 2.0)
        assert bar.size_num == 3  # #3 @ ~6.5″ gives 0.20 in²/ft
        assert spacing <= 18.0

    def test_steps_up_when_needed(self):
        # Require 1.2 in²/ft — #3 @ 1.1″ has clear < 1″, forces step to #4
        bar, spacing = select_bar(1.2, 12.0, 2.0)
        assert bar.size_num >= 4

    def test_respects_max_bar_size(self):
        bar, spacing = select_bar(0.30, 12.0, 2.0, max_bar_size=4)
        assert bar.size_num <= 4

    def test_raises_on_impossible(self):
        with pytest.raises(ValueError):
            select_bar(5.0, 12.0, 2.0, max_bar_size=4)

    def test_raises_on_zero_as(self):
        with pytest.raises(ValueError):
            select_bar(0.0, 12.0, 2.0)


class TestConcrete:
    def test_defaults(self):
        c = Concrete()
        assert c.fc_psi == 3_000
        assert c.wc_pcf == 150.0

    def test_sqrt_fc(self):
        c = Concrete(fc_psi=3_000)
        assert c.sqrt_fc == pytest.approx(math.sqrt(3000))

    def test_beta1_3000(self):
        c = Concrete(fc_psi=3_000)
        assert c.beta1 == 0.85

    def test_beta1_5000(self):
        c = Concrete(fc_psi=5_000)
        assert c.beta1 == pytest.approx(0.80)

    def test_beta1_8000(self):
        c = Concrete(fc_psi=8_000)
        assert c.beta1 == 0.65

    def test_fr(self):
        c = Concrete(fc_psi=3_000)
        expected = 7.5 * 1.0 * math.sqrt(3000)
        assert c.fr == pytest.approx(expected)

    def test_Ec(self):
        c = Concrete(fc_psi=3_000, wc_pcf=150.0)
        expected = 33.0 * (150.0 ** 1.5) * math.sqrt(3000)
        assert c.Ec == pytest.approx(expected)


class TestRebarSpec:
    def test_defaults(self):
        spec = RebarSpec()
        assert spec.preferred_sizes == [3, 4]
        assert spec.max_bar_size == 6

    def test_is_preferred(self):
        spec = RebarSpec()
        assert spec.is_preferred(4)
        assert not spec.is_preferred(5)

    def test_is_allowed(self):
        spec = RebarSpec()
        assert spec.is_allowed(5)
        assert not spec.is_allowed(7)

    def test_fy(self):
        spec = RebarSpec()
        assert spec.fy(4) == 40_000
        assert spec.fy(5) == 60_000
