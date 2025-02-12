# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import os.path
import pytest
from selenium.webdriver import Keys, ActionChains

from locators.explore_model_locators import ExploreModelPageLocators
from locators.explore_page_locators import ExplorePageLocators
from pages.explore_model_page import ExploreModelDataPage
from pages.explore_page import ExplorePage

current_directory = os.getcwd()
relative_file_path = 'scraped_links.txt'
file_path = os.path.join(current_directory, relative_file_path)


class TestExploreModelPage:
    @pytest.mark.explore_page
    @pytest.mark.run(order=7)
    def test_explore_model(self, setup, login, logger):
        """
        The commented out code below is pending changes in the platform.
        """
        browser, wait, base_url = setup
        explore_model = ExploreModelDataPage(browser, wait, logger, base_url)
        lab_id = "37a3a2e8-a4b4-456b-8aff-4e23e87a5cbc"
        project_id = "8abcb1e3-b714-4267-a22c-3b3dc4be5306"
        explore_model.go_to_explore_model_page(lab_id, project_id)
        logger.info("Explore page is loaded")

        emodel_tab = explore_model.find_emodel_tab()
        logger.info("E-model data tab is found")
        cerebrum_title = explore_model.find_br_cerebrum_title()
        cerebrum_text = cerebrum_title.text
        logger.info(f"Found text: {cerebrum_text}")

        brain_region_search_field = explore_model.find_brain_region_search_field(timeout=25)
        assert brain_region_search_field.is_displayed()
        logger.info("Bran region panel search field is found")
        brain_region_search_field.send_keys(Keys.ENTER)
        logger.info("Clicked on the brain region search input field")
        find_input_file_and_wait = ExploreModelPageLocators.SEARCH_REGION
        explore_model.wait_for_long_load(find_input_file_and_wait)
        logger.info("Waiting for page to load")

        brain_region_search_field.send_keys("Isocortex")
        logger.info("Searching for 'Isocortex'")
        brain_region_search_field.send_keys(Keys.ENTER)

        brain_region_panel_close_btn = explore_model.brain_region_panel_close_btn()
        assert brain_region_panel_close_btn.is_displayed(), ("Brain region panel close button is "
                                                             "found")
        brain_region_panel_close_btn.click()
        logger.info("Brain region panel is toggled close")
