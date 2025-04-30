# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import os
import time
import pytest

from locators.explore_ndensity_locators import ExploreNDensityPageLocators
from pages.explore_ndensity import ExploreNeuronDensityPage


class TestExploreNeuronDensity:
    @pytest.mark.build_page
    @pytest.mark.run(order=5)
    def test_explore_neuron_density_page(self, setup, login, logger, test_config):
        """Checking the titles of the Neuron Density Tab"""
        browser, wait, base_url, lab_id, project_id = setup
        explore_ndensity = ExploreNeuronDensityPage(browser, wait, base_url)
        explore_ndensity.go_to_explore_neuron_density_page(lab_id, project_id)
        explore_ndensity.wait_for_ndensity_tab(timeout=60)
        logger.info(f"Neuron density tab is displayed, {browser.current_url}")

        ai_assistant_panel = explore_ndensity.find_ai_assistant_panel()
        logger.info("Found Ai Assistant Panel")
        ai_assistant_panel_close = explore_ndensity.find_ai_assistant_panel_close()
        ai_assistant_panel_close.click()
        logger.info("Found the AI assistant close button and clicked")

        brain_regions_panel_btn = explore_ndensity.find_brain_regions_panel_btn()
        assert brain_regions_panel_btn.is_displayed(), "Button to close Brain regions panel is not found"
        brain_regions_panel_btn.click()
        logger.info("Brain regions panel is closed")


        column_locators = [
            ExploreNDensityPageLocators.LV_BRAIN_REGION,
            ExploreNDensityPageLocators.LV_MTYPE,
            ExploreNDensityPageLocators.LV_ETYPE,
            ExploreNDensityPageLocators.LV_DENSITY,
            ExploreNDensityPageLocators.LV_NMEASUREMENTS,
            ExploreNDensityPageLocators.LV_NAME,
            ExploreNDensityPageLocators.LV_SPECIES,
            ExploreNDensityPageLocators.LV_AGE,
            ExploreNDensityPageLocators.LV_CONTRIBUTORS,
            ExploreNDensityPageLocators.LV_REGISTRATION_DATE
        ]
        column_headers = explore_ndensity.find_column_headers(column_locators)

        found_column_headers = [element.text for element in column_headers]
        logger.info(f"Found n.density list view column headers: {found_column_headers}")
        for header in column_headers:
            assert header.is_displayed(), f"Column header {header} is not displayed."
        logger.info("Found 'List view' column headers")

        lv_registration_date = explore_ndensity.find_registration_date()
        assert lv_registration_date is not None, "The registration date is not visible"
        logger.info("'Registration date' column header is in the DOM")
        lv_contributors_header = explore_ndensity.find_lv_contributor_header()
        logger.info("'Contributors' column header is found in the List view")

        cerebrum_brp = explore_ndensity.find_cerebrum_brp()
        assert cerebrum_brp.is_displayed()
        logger.info("Cerebrum is found")
        lv_br_row1 = explore_ndensity.lv_br_row1()
        browser.execute_script("arguments[0].scrollIntoView(true);", lv_br_row1)
        browser.execute_script("arguments[0].click();", lv_br_row1)
        logger.info("Clicked on a resource to see detail view")

        dv_name = explore_ndensity.find_dv_name_title()
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

        value_locators = [
            ExploreNDensityPageLocators.DV_DESC_VALUE,
            ExploreNDensityPageLocators.DV_CONTRIBUTORS_VALUE,
            ExploreNDensityPageLocators.DV_REG_DATE_VALUE,
            ExploreNDensityPageLocators.DV_BRAIN_REG_VALUE,
            ExploreNDensityPageLocators.DV_SPECIES_VALUE,
            ExploreNDensityPageLocators.DV_LICENSE_VALUE,
            ExploreNDensityPageLocators.DV_MTYPE_VALUE,
            # ExploreNDensityPageLocators.DV_AGE_VALUE,
            ExploreNDensityPageLocators.DV_ETYPE_VALUE,
            ExploreNDensityPageLocators.DV_DENSITY_VALUE,
            ExploreNDensityPageLocators.DV_NUM_MEAS_VALUE,
        ]

        for locator in value_locators:
            element = explore_ndensity.find_element(locator)
            text = element.text.strip()
            logger.info(f"Found value for {locator}: '{text}'")
            assert text, f"Element {locator} is empty or missing text"
