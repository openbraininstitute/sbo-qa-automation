# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import os.path
import pytest
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys, ActionChains

from locators.explore_model_locators import ExploreModelPageLocators
from locators.explore_page_locators import ExplorePageLocators
from pages.explore_model_page import ExploreModelDataPage
from pages.explore_page import ExplorePage



class TestExploreModelPage:
    @pytest.mark.explore_page
    @pytest.mark.run(order=7)
    def test_explore_model(self, setup, login, logger, test_config):
        browser, wait, base_url, lab_id, project_id = setup
        explore_model = ExploreModelDataPage(browser, wait, logger, base_url)
        print(f"DEBUG: Using lab_id={lab_id}, project_id={project_id}")

        explore_model.go_to_explore_model_page(lab_id, project_id)
        logger.info("Explore page is loaded")

        emodel_tab = explore_model.find_emodel_tab()
        assert emodel_tab.is_displayed(), "E-model tab is not displayed"
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

        search_for_resources = explore_model.find_search_for_resources()
        assert search_for_resources.is_displayed(), "Search resources field is not found"
        search_for_resources.click()
        searched_emodel = "cadpyr"
        for char in searched_emodel:
            search_for_resources.send_keys(char)
            time.sleep(0.1)
        logger.info("Searching for 'cadpyr'")
        lv_searched_emodel = explore_model.find_lv_selected_resource()
        assert lv_searched_emodel.is_displayed(), "The selected emodel is not found"
        logger.info("Selected resource found")
        lv_searched_emodel.click()

        try:
            ai_assistant_panel_close = explore_model.find_ai_assistant_panel_close()
            if ai_assistant_panel_close and ai_assistant_panel_close.is_displayed():
                logger.info("Panel is open. Clicking to close it.")
                ai_assistant_panel_close.click()
            else:
                logger.info("Panel is already closed. No action needed.")
        except NoSuchElementException:
            logger.info("No close button found. Assuming panel is already closed.")

        dv_name_label = explore_model.find_dv_name_label()
        assert dv_name_label.is_displayed(), "'Name' label is missing"
        logger.info("Found 'Name' label")

        dv_name_value = explore_model.find_dv_name_value()
        assert dv_name_value.is_displayed(), "Name value is missing"
        logger.info("Found name value")

        description_label_element = explore_model.find_dv_description_label()
        assert description_label_element.is_displayed(), "Description label is not displayed"
        assert description_label_element.text.strip() == "DESCRIPTION", f"Expected label 'Description', but found: {description_label_element.text.strip()}"

        description_value_element = explore_model.find_dv_description_value()
        assert description_value_element.is_displayed(), "Description value is not displayed"
        description_text = description_value_element.text.strip()
        assert description_text != "", "Description value is empty"
        logger.info(f"Found Description value: {description_text}")

        dv_config_tab = explore_model.find_dv_configuration_tab()
        assert dv_config_tab.is_displayed(), "Emodel detail view confiugration tab is not displayed"
        logger.info("Detail view configuration tab is found")

        dv_analysis_tab = explore_model.find_dv_analysis_tab()
        assert dv_analysis_tab.is_displayed(), "Emodel detail view analysis tab is not displayed"
        logger.info("Detail view analysis tab is found")

        dv_simulation_tab = explore_model.find_dv_simulation_tab()
        assert dv_simulation_tab.is_displayed(), "Emodel detail view simulation tab is not displayed"
        logger.info("Detail view simulation tab is found")
        time.sleep(5)
        expected_morph_titles = ["PREVIEW", "NAME", "DESCRIPTION", "BRAIN LOCATION", "M-TYPE",
                                 "CONTRIBUTOR"]

        header_texts = explore_model.dv_get_table_headers()
        assert len(header_texts) == len(expected_morph_titles), (
            f"Expected {len(expected_morph_titles)} columns, but found {len(header_texts)}: {header_texts}"
        )

        assert header_texts == expected_morph_titles, (
            f"Expected headers {expected_morph_titles}, but found {header_texts}"
        )
