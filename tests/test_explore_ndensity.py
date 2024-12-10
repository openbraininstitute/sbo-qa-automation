# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

import os
import time
import pytest

from locators.explore_ndensity_locators import ExploreNDensityPageLocators
from pages.explore_ndensity import ExploreNeuronDensityPage

# Skip module if `SKIP_TESTS` environment variable is set
if os.getenv("SKIP_TESTS") == "1":
    pytest.skip("Skipping Morphology tests temporarily.", allow_module_level=True)


class TestExploreNeuronDensity:
    @pytest.mark.build_page
    @pytest.mark.run(order=5)
    def test_explore_neuron_density_page(self, setup, login, logger):
        browser, wait = setup
        explore_ndensity = ExploreNeuronDensityPage(browser, wait)
        explore_ndensity.go_to_explore_neuron_density_page()
        # explore_ndensity_tab = explore_ndensity.find_ndensity_tab()
        explore_ndensity.element_visibility(ExploreNDensityPageLocators.NDENSITY_TAB,
                                            timeout=60)
        logger.info("Neuron density tab is displayed")

        column_locators = [
            ExploreNDensityPageLocators.LV_BRAIN_REGION,
            ExploreNDensityPageLocators.LV_MTYPE,
            ExploreNDensityPageLocators.LV_ETYPE,
            ExploreNDensityPageLocators.LV_DENSITY,
            ExploreNDensityPageLocators.LV_NMEASUREMENTS,
            ExploreNDensityPageLocators.LV_NAME,
            ExploreNDensityPageLocators.LV_SPECIES,
            ExploreNDensityPageLocators.LV_AGE,
            ExploreNDensityPageLocators.LV_CONTRIBUTORS
        ]
        column_headers = explore_ndensity.find_column_headers(column_locators)

        found_column_headers = [element.text for element in column_headers]
        logger.info(f"Found n.density list view column headers: {found_column_headers}")
        for header in column_headers:
            assert header.is_displayed(), f"Column header {header} is not displayed."
        logger.info("Found 'List view' column headers")

        registration_date = explore_ndensity.find_registration_date()
        assert registration_date is not None, "The registration date is not visible"
        logger.info("The Registration date column header is in the DOM")

        cerebrum_brp = explore_ndensity.find_cerebrum_brp()
        assert cerebrum_brp.is_displayed()
        logger.info("Cerebrum is found")
        lv_br_row1 = explore_ndensity.lv_br_row1()
        browser.execute_script("arguments[0].scrollIntoView(true);", lv_br_row1)
        browser.execute_script("arguments[0].click();", lv_br_row1)
        logger.info("Clicked on a resource to see detail view")

        dv_name = explore_ndensity.find_dv_name()
        logger.info("Detail view is displayed")

        title_locators = [
            ExploreNDensityPageLocators.DV_DESC_TITLE,
            ExploreNDensityPageLocators.DV_DENSITY_TITLE,
            ExploreNDensityPageLocators.DV_AGE_TITLE,
            ExploreNDensityPageLocators.DV_BRAIN_REG_TITLE,
            ExploreNDensityPageLocators.DV_CONTRIBUTORS_TITLE,
            ExploreNDensityPageLocators.DV_LICENSE_TITLE,
            ExploreNDensityPageLocators.DV_NUM_MEAS_TITLE,
            ExploreNDensityPageLocators.DV_ETYPE_TITLE,
            ExploreNDensityPageLocators.DV_MTYPE_TITLE,
            ExploreNDensityPageLocators.DV_SPECIES_TITLE,
            ExploreNDensityPageLocators.DV_REG_DATE_TITLE
        ]

        title_headers = explore_ndensity.find_dv_title_header(title_locators)
        for title in title_headers:
            assert title.is_displayed(), f"DV title header {title} is not displayed"
        logger.info("Found 'Detail view' title headers")
