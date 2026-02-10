"""Tests for the design criteria module."""

import pytest

from retaining_wall.criteria import DesignCriteria, ExposureConditions


class TestExposureConditions:
    def test_incomplete(self):
        e = ExposureConditions()
        assert not e.is_complete

    def test_complete(self):
        e = ExposureConditions(freeze_thaw="F1", sulfate="S0", corrosion="C1")
        assert e.is_complete

    def test_default_cover(self):
        e = ExposureConditions()
        assert e.required_cover_in() == 2.0

    def test_cover_with_corrosion(self):
        e = ExposureConditions(freeze_thaw="F0", sulfate="S0", corrosion="C1")
        assert e.required_cover_in() == 2.0


class TestDesignCriteria:
    def test_empty_criteria_validation(self):
        dc = DesignCriteria()
        missing = dc.validate()
        assert len(missing) > 0
        assert not dc.is_complete

    def test_complete_criteria(self):
        dc = DesignCriteria(
            retained_height_ft=10.0,
            base_heel_ft=5.0,
            backfill_gamma_pcf=120.0,
            backfill_phi_deg=30.0,
            allowable_bearing_psf=3000.0,
            drainage_provided=True,
            exposure=ExposureConditions(
                freeze_thaw="F0", sulfate="S0", corrosion="C0"
            ),
        )
        assert dc.is_complete
        assert len(dc.validate()) == 0

    def test_build_concrete(self):
        dc = DesignCriteria(fc_psi=4_000)
        c = dc.build_concrete()
        assert c.fc_psi == 4_000

    def test_build_wall_geometry(self):
        dc = DesignCriteria(
            retained_height_ft=10.0,
            base_heel_ft=5.0,
        )
        wall = dc.build_wall_geometry()
        assert wall.stem.height_ft == 10.0
        assert wall.base.heel_ft == 5.0

    def test_build_wall_requires_height(self):
        dc = DesignCriteria()
        with pytest.raises(ValueError):
            dc.build_wall_geometry()

    def test_build_soil(self):
        dc = DesignCriteria(
            backfill_gamma_pcf=120.0,
            backfill_phi_deg=30.0,
        )
        soil = dc.build_soil()
        assert soil.gamma_pcf == 120.0

    def test_build_soil_requires_params(self):
        dc = DesignCriteria()
        with pytest.raises(ValueError):
            dc.build_soil()

    def test_build_water_no_drainage(self):
        dc = DesignCriteria()
        water = dc.build_water()
        assert water.has_water_case

    def test_build_water_with_drainage(self):
        dc = DesignCriteria(drainage_provided=True)
        water = dc.build_water()
        assert not water.has_water_case

    def test_build_seismic_default(self):
        dc = DesignCriteria()
        seis = dc.build_seismic()
        assert not seis.is_active

    def test_build_shear_key(self):
        dc = DesignCriteria(
            retained_height_ft=10.0,
            base_heel_ft=5.0,
            use_shear_key=True,
        )
        wall = dc.build_wall_geometry()
        assert wall.shear_key is not None

    def test_design_basis_narrative(self):
        dc = DesignCriteria()
        text = dc.design_basis_narrative()
        assert "IBC 2021" in text
        assert "ACI 318-19" in text
        assert "INCOMPLETE" in text

    def test_design_basis_complete(self):
        dc = DesignCriteria(
            retained_height_ft=10.0,
            base_heel_ft=5.0,
            backfill_gamma_pcf=120.0,
            backfill_phi_deg=30.0,
            allowable_bearing_psf=3000.0,
            drainage_provided=True,
            exposure=ExposureConditions(
                freeze_thaw="F0", sulfate="S0", corrosion="C0"
            ),
        )
        text = dc.design_basis_narrative()
        assert "COMPLETE" in text
