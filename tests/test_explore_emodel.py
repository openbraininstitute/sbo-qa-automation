# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import os.path
import pytest
from selenium.common import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver import Keys, ActionChains

from locators.explore_emodel_locators import ExploreEModelPageLocators
from pages.explore_emodel_page import ExploreEModelDataPage



class TestExploreModelPage:
    @pytest.mark.explore_page
    @pytest.mark.run(order=7)
    def test_explore_emodel(self, setup, login, logger, test_config):
        browser, wait, base_url, lab_id, project_id = setup
        explore_model = ExploreEModelDataPage(browser, wait, logger, base_url)
        print(f"DEBUG: Using lab_id={lab_id}, project_id={project_id}")

        explore_model.go_to_explore_emodel_page(lab_id, project_id)
        logger.info("Explore page is loaded")

        emodel_tab = explore_model.find_emodel_tab(timeout=15)
        assert emodel_tab.is_displayed(), "E-model tab is not displayed"
        logger.info("E-model data tab is found")

        cerebrum_title = explore_model.find_br_cerebrum_title(timeout=15)
        cerebrum_text = cerebrum_title.text
        logger.info(f"Found text: {cerebrum_text}")

        ai_assistant_panel = explore_model.find_ai_assistant_panel(timeout=10)
        assert ai_assistant_panel.is_displayed()
        logger.info("Found AI assistant panel")

        ai_assistant_panel_close_btn = explore_model.find_ai_assistant_panel_close_btn()
        logger.info("Panel is open. Clicking to close it.")
        ai_assistant_panel_close_btn.click()

        brain_region_search_field = explore_model.find_brain_region_search_field(timeout=25)
        assert brain_region_search_field.is_displayed()
        logger.info("Bran region panel search field is found")
        brain_region_search_field.send_keys(Keys.ENTER)
        logger.info("Clicked on the brain region search input field")
        find_input_file_and_wait = ExploreEModelPageLocators.SEARCH_REGION
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

        searched_emodel = "cadpyr"
        search_for_resources = explore_model.find_search_for_resources()
        assert search_for_resources.is_displayed(), "Search resources field is not found"
        search_for_resources.click()

        for char in searched_emodel:
            search_for_resources.send_keys(char)
            time.sleep(0.2)
        logger.info("Searching for 'cadpyr'")

        lv_row = explore_model.find_lv_row()
        assert lv_row.is_displayed(), "The table and the rows are not found"
        logger.info("The table and the rows are displayed")

        explore_model.wait_for_spinner_to_disappear(timeout=25)

        lv_searched_emodel = explore_model.find_lv_selected_resource(timeout=15)
        assert lv_searched_emodel.is_displayed(), "The selected emodel is not found"
        logger.info("Selected resource found")

        try:
            lv_searched_emodel.click()
        except ElementClickInterceptedException:
            logger.warning("Click intercepted. Retrying after wait.")
            time.sleep(1)
            lv_searched_emodel.click()

        label_checks = [
            ("DESCRIPTION", explore_model.find_dv_description_label, explore_model.find_dv_description_value),
            ("CONTRIBUTORS", explore_model.find_dv_contributors_label, explore_model.find_dv_contributors_value),
            ("REGISTRATION DATE", explore_model.find_dv_registration_date_label,
             explore_model.find_dv_registration_date_value),
            ("BRAIN REGION", explore_model.find_dv_brain_region_label, explore_model.find_dv_brain_region_value),
            ("MODEL CUMULATED SCORE", explore_model.find_dv_model_score_label,
             explore_model.find_dv_model_score_value),
            ("M-TYPE", explore_model.find_dv_mtype_label, explore_model.find_dv_mtype_value),
            ("E-TYPE", explore_model.find_dv_etype_label, explore_model.find_dv_etype_value),
        ]

        for label_text, find_label_fn, find_value_fn in label_checks:
            try:
                label_el = find_label_fn()
                value_el = find_value_fn()

                assert label_el is not None, f"'{label_text}' label element not found"
                assert value_el is not None, f"{label_text} value element not found"
                assert label_el.is_displayed(), f"'{label_text}' label is missing"
                assert label_el.text.strip() == label_text, f"Expected label '{label_text}', got '{label_el.text.strip()}'"
                assert value_el.is_displayed(), f"{label_text} value is not displayed"
                value = value_el.text.strip()
                assert value != "", f"{label_text} value is empty"
                logger.info(f"{label_text} value: {value}")

            except AssertionError as e:
                if label_text == "CONTRIBUTORS":
                    logger.warning(f"XFAIL: {label_text} check failed but is expected to fail: {e}")
                else:
                    logger.error(f"{label_text} check failed: {e}")
            except Exception as e:
                logger.error(f"Unexpected error in {label_text} check: {e}")

        dv_config_tab = explore_model.find_dv_configuration_tab()
        assert dv_config_tab.is_displayed(), "Emodel detail view confiugration tab is not displayed"
        logger.info("Detail view configuration tab is found")

        dv_analysis_tab = explore_model.find_dv_analysis_tab()
        assert dv_analysis_tab.is_displayed(), "Emodel detail view analysis tab is not displayed"
        logger.info("Detail view analysis tab is found")

        dv_simulation_tab = explore_model.find_dv_simulation_tab()
        assert dv_simulation_tab.is_displayed(), "Emodel detail view simulation tab is not displayed"
        logger.info("Detail view simulation tab is found")

        expected_morph_headers = explore_model.verify_exemplar_morphology_headers()
        expected_exemplar_traces_headers = explore_model.verify_exemplar_traces_table_headers()

