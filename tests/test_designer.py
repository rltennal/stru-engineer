"""Tests for the wall designer orchestrator."""

import pytest

from retaining_wall.criteria import DesignCriteria, ExposureConditions
from retaining_wall.designer import WallDesigner, DesignReport


def _complete_criteria() -> DesignCriteria:
    """Build a complete, realistic set of design criteria."""
    return DesignCriteria(
        retained_height_ft=10.0,
        stem_thickness_top_in=8.0,
        stem_thickness_bot_in=12.0,
        base_toe_ft=1.5,
        base_heel_ft=5.0,
        base_thickness_in=12.0,
        backfill_gamma_pcf=120.0,
        backfill_phi_deg=30.0,
        mu_sliding=0.45,
        allowable_bearing_psf=3000.0,
        drainage_provided=True,
        surcharge_psf=100.0,
        fc_psi=3_000,
        rebar_max_bar_size=6,
        exposure=ExposureConditions(
            freeze_thaw="F0", sulfate="S0", corrosion="C0"
        ),
    )


class TestWallDesigner:
    def test_full_run(self):
        criteria = _complete_criteria()
        designer = WallDesigner(criteria)
        report = designer.run()

        assert report.wall is not None
        assert len(report.stability) == 3
        assert len(report.sections) == 3  # stem, heel, toe
        assert len(report.development_lengths) > 0

    def test_stability_results(self):
        criteria = _complete_criteria()
        report = WallDesigner(criteria).run()
        checks = {r.check for r in report.stability}
        assert "Overturning" in checks
        assert "Sliding" in checks
        assert "Bearing" in checks

    def test_section_locations(self):
        criteria = _complete_criteria()
        report = WallDesigner(criteria).run()
        locations = {s.location for s in report.sections}
        assert "stem_base" in locations
        assert "heel (top steel)" in locations
        assert "toe (bottom steel)" in locations

    def test_sections_have_bars(self):
        criteria = _complete_criteria()
        report = WallDesigner(criteria).run()
        for section in report.sections:
            assert section.bar is not None, f"No bar selected for {section.location}"
            assert section.spacing_in is not None

    def test_summary_output(self):
        criteria = _complete_criteria()
        report = WallDesigner(criteria).run()
        text = report.summary()
        assert "GEOMETRY" in text
        assert "STABILITY" in text
        assert "STRUCTURAL DESIGN" in text
        assert "DEVELOPMENT LENGTHS" in text

    def test_incomplete_criteria(self):
        """Designer should still run (with warnings) when criteria are partial."""
        criteria = DesignCriteria(
            retained_height_ft=10.0,
            base_heel_ft=5.0,
            backfill_gamma_pcf=120.0,
            backfill_phi_deg=30.0,
        )
        report = WallDesigner(criteria).run()
        assert len(report.warnings) > 0
        assert report.wall is not None

    def test_missing_soil(self):
        """Designer should warn gracefully when soil data is absent."""
        criteria = DesignCriteria(retained_height_ft=10.0, base_heel_ft=5.0)
        report = WallDesigner(criteria).run()
        assert any("Soil" in w or "soil" in w for w in report.warnings)

    def test_with_seismic(self):
        criteria = _complete_criteria()
        criteria.kh = 0.15
        criteria.use_mononobe_okabe = True
        report = WallDesigner(criteria).run()
        seismic_cases = [lc for lc in report.load_cases if "seismic" in lc.label.lower()]
        assert len(seismic_cases) == 1

    def test_with_shear_key(self):
        criteria = _complete_criteria()
        criteria.use_shear_key = True
        report = WallDesigner(criteria).run()
        assert report.wall.shear_key is not None

    def test_report_all_ok_flag(self):
        criteria = _complete_criteria()
        report = WallDesigner(criteria).run()
        # Should be a boolean regardless of pass/fail
        assert isinstance(report.all_ok, bool)

    def test_with_water(self):
        criteria = _complete_criteria()
        criteria.drainage_provided = False
        criteria.gwl_depth_ft = 4.0
        report = WallDesigner(criteria).run()
        water_cases = [lc for lc in report.load_cases if "ydrostatic" in lc.label]
        assert len(water_cases) == 1
