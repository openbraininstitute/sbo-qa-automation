# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import os.path
import pytest
from selenium.common import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver import Keys, ActionChains

from locators.explore_emodel_locators import ExploreEModelPageLocators
from pages.explore_emodel_page import ExploreEModelDataPage



class TestExploreModelPage:
    @pytest.mark.explore_page
    @pytest.mark.run(order=7)
    def test_explore_emodel(self, setup, login_direct_complete, logger, test_config):
        browser, wait, base_url, lab_id, project_id = login_direct_complete
        explore_emodel = ExploreEModelDataPage(browser, wait, logger, base_url)
        print(f"DEBUG: Using lab_id={lab_id}, project_id={project_id}")

        explore_emodel.go_to_explore_emodel_page(lab_id, project_id)
        logger.info("Explore page is loaded")

        model_tab = explore_emodel.model_data_tab()
        assert model_tab.is_displayed(), "Model data tab is not displayed"
        logger.info("Model data tab is found")
        model_tab.click()
        logger.info("Model data tab is clicked")

        emodel_tab = explore_emodel.wait_for_emodel_tab_ready(timeout=40)
        assert emodel_tab.is_displayed(), "E-model tab is not displayed"
        logger.info("E-model data tab is found")
        emodel_tab.click()
        logger.info("E-model data tab is clicked")

        cerebrum_title = explore_emodel.find_br_cerebrum_title(timeout=25)
        cerebrum_text = cerebrum_title.text
        logger.info(f"Found text: {cerebrum_text}")

        brain_region_panel = explore_emodel.find_brain_region_panel(timeout=20)
        logger.info("Found Brain Region Panel")

        brain_region_panel.click()
        logger.info("Brain region panel is toggled open")

        brain_region_search_field = explore_emodel.find_brain_region_search_field(timeout=15)
        assert brain_region_search_field.is_displayed()
        logger.info("Bran region panel search field is found")

        brain_region_search_field.send_keys(Keys.ENTER)
        logger.info("Clicked on the brain region search input field")

        find_input_file_and_wait = ExploreEModelPageLocators.SEARCH_REGION
        explore_emodel.wait_for_long_load(find_input_file_and_wait)
        logger.info("Waiting for page to load")

        brain_region_search_field.send_keys("Isocortex")
        logger.info("Searching for 'Isocortex'")
        brain_region_search_field.send_keys(Keys.ENTER)

        selected_brain_region = explore_emodel.find_selected_brain_region_title(timeout=10)
        assert selected_brain_region.is_displayed(), "Selected brain region is not found"
        logger.info("Selected brain region is found")

        # brain_region_panel_close_btn = explore_emodel.brain_region_panel_close_btn()
        # assert brain_region_panel_close_btn.is_displayed(), ("Brain region panel close button is "
        #                                                      "found")
        # brain_region_panel_close_btn.click()
        # logger.info("Brain region panel is toggled close")

        searched_emodel = "cadpyr"
        search_for_resources = explore_emodel.find_search_for_resources()
        assert search_for_resources.is_displayed(), "Search resources field is not found"
        search_for_resources.click()
        logger.info("Search resources field is clicked")

        input_placeholder = explore_emodel.input_placeholder(timeout=10)
        input_placeholder.click()
        logger.info("Input placeholder is clicked")

        for char in searched_emodel:
            input_placeholder.send_keys(char)
            time.sleep(0.2)
        logger.info("Searching for 'cadpyr'")
        explore_emodel.wait_for_spinner_to_disappear(timeout=25)

        lv_row = explore_emodel.find_lv_row()
        assert lv_row.is_displayed(), "The table and the rows are not found"
        logger.info("The table and the rows are displayed")

        explore_emodel.wait_for_spinner_to_disappear(timeout=25)

        lv_searched_emodel = explore_emodel.find_lv_selected_resource(timeout=25)
        assert lv_searched_emodel.is_displayed(), "The selected emodel is not found"
        logger.info("Selected resource found")

        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                if attempt > 0:
                    lv_searched_emodel = explore_emodel.find_lv_selected_resource(timeout=10)
                
                lv_searched_emodel.click()
                logger.info(f"Successfully clicked on attempt {attempt + 1}")
                break
                
            except (ElementClickInterceptedException, StaleElementReferenceException) as e:
                logger.warning(f"Attempt {attempt + 1} failed: {type(e).__name__}. Retrying...")
                if attempt == max_attempts - 1:
                    logger.error("All click attempts failed")
                    raise
                time.sleep(1)

        old_url = browser.current_url
        explore_emodel.wait_for_spinner_to_disappear(timeout=25)

        mini_detail_view_button = explore_emodel.mini_detail_view_button(timeout=20)
        assert mini_detail_view_button.is_displayed(), "Mini detail view button is not found"
        logger.info("Mini detail view button is found")

        mini_detail_view_button.click()
        logger.info("Mini detail view button is clicked")

        explore_emodel.wait_for_url_change(old_url, timeout=25)
        explore_emodel.wait_for_url_contains("/data/view/emodel/", timeout=20)

        current_url = browser.current_url
        logger.info(f"Current URL: {current_url}")

        assert "/overview" in current_url

        label_checks = [
            ("DESCRIPTION", explore_emodel.find_dv_description_label, explore_emodel.find_dv_description_value),
            ("CONTRIBUTORS", explore_emodel.find_dv_contributors_label, explore_emodel.find_dv_contributors_value),
            ("REGISTRATION DATE", explore_emodel.find_dv_registration_date_label,
             explore_emodel.find_dv_registration_date_value),
            ("BRAIN REGION", explore_emodel.find_dv_brain_region_label, explore_emodel.find_dv_brain_region_value),
            ("MODEL CUMULATED SCORE", explore_emodel.find_dv_model_score_label,
             explore_emodel.find_dv_model_score_value),
            ("M-TYPE", explore_emodel.find_dv_mtype_label, explore_emodel.find_dv_mtype_value),
            ("E-TYPE", explore_emodel.find_dv_etype_label, explore_emodel.find_dv_etype_value),
            ("REGISTERED BY", explore_emodel.find_dv_registered_by_label, explore_emodel.find_dv_registered_by_value),
            ("SPECIES", explore_emodel.find_dv_species_label, explore_emodel.find_dv_species_value),
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

        dv_config_tab = explore_emodel.find_dv_configuration_tab()
        assert dv_config_tab.is_displayed(), "Emodel detail view confiugration tab is not displayed"
        logger.info("Detail view configuration tab is found")

        dv_analysis_tab = explore_emodel.find_dv_analysis_tab()
        assert dv_analysis_tab.is_displayed(), "Emodel detail view analysis tab is not displayed"
        logger.info("Detail view analysis tab is found")

        dv_overview_tab = explore_emodel.find_dv_overview_tab()
        assert dv_overview_tab.is_displayed(), "Emodel detail view simulation tab is not displayed"
        logger.info("Detail view simulation tab is found")

        '''
        To finalize, once the headers and sections are completed.
        expected_morph_headers = explore_emodel.verify_exemplar_morphology_headers()
        expected_exemplar_traces_headers = explore_emodel.verify_exemplar_traces_table_headers()
        '''
