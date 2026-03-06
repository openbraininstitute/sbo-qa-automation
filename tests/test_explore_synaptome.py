# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import pytest
from selenium.common import ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver import Keys

from pages.explore_synaptome_page import ExploreSynaptomeDataPage


class TestExploreSynaptomePage:
    @pytest.mark.explore_page
    def test_explore_synaptome(self, setup, login_direct_complete, logger, test_config):
        browser, wait, base_url, lab_id, project_id = login_direct_complete
        explore_synaptome = ExploreSynaptomeDataPage(browser, wait, logger, base_url)
        print(f"DEBUG: Using lab_id={lab_id}, project_id={project_id}")

        explore_synaptome.go_to_explore_synaptome_page(lab_id, project_id)
        logger.info("Synaptome page is loaded")

        # Verify brain region is Cerebrum
        cerebrum_title = explore_synaptome.find_br_cerebrum_title(timeout=25)
        cerebrum_text = cerebrum_title.text
        logger.info(f"Found brain region: {cerebrum_text}")
        assert "Cerebrum" in cerebrum_text, f"Expected 'Cerebrum', got '{cerebrum_text}'"

        # Verify Model tab is active
        model_tab = explore_synaptome.model_data_tab()
        assert model_tab.is_displayed(), "Model data tab is not displayed"
        logger.info("Model data tab is found and active")

        # Verify Synaptome button is highlighted/active
        synaptome_btn = explore_synaptome.synaptome_button(timeout=20)
        assert synaptome_btn.is_displayed(), "Synaptome button is not displayed"
        logger.info("Synaptome button is found")

        # Search for a synaptome entry in Public tab
        searched_synaptome = "SSCx"
        search_button = explore_synaptome.find_search_button()
        assert search_button.is_displayed(), "Search button is not found"
        search_button.click()
        logger.info("Search button is clicked")

        input_placeholder = explore_synaptome.input_placeholder(timeout=10)
        input_placeholder.click()
        logger.info("Input placeholder is clicked")

        for char in searched_synaptome:
            input_placeholder.send_keys(char)
            time.sleep(0.2)
        logger.info(f"Searching for '{searched_synaptome}' in Public tab")
        explore_synaptome.wait_for_spinner_to_disappear(timeout=25)

        # Click on first row
        logger.info("Attempting to click first synaptome row")

        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                explore_synaptome.click_first_row(timeout=25)
                logger.info(f"Successfully clicked on attempt {attempt + 1}")
                break
                
            except (ElementClickInterceptedException, StaleElementReferenceException) as e:
                logger.warning(f"Attempt {attempt + 1} failed: {type(e).__name__}. Retrying...")
                if attempt == max_attempts - 1:
                    logger.error("All click attempts failed")
                    raise
                time.sleep(1)

        old_url = browser.current_url
        explore_synaptome.wait_for_spinner_to_disappear(timeout=25)

        # Click mini detail view button
        mini_detail_view_button = explore_synaptome.mini_detail_view_button(timeout=20)
        assert mini_detail_view_button.is_displayed(), "Mini detail view button is not found"
        logger.info("Mini detail view button is found")

        mini_detail_view_button.click()
        logger.info("Mini detail view button is clicked")

        explore_synaptome.wait_for_url_change(old_url, timeout=25)
        explore_synaptome.wait_for_url_contains("/data/view/single-neuron-synaptome/", timeout=20)

        current_url = browser.current_url
        logger.info(f"Current URL: {current_url}")

        assert "/overview" in current_url, f"Expected '/overview' in URL, got {current_url}"

        # Verify detail view labels and values
        label_checks = [
            ("DESCRIPTION", explore_synaptome.find_dv_description_label, explore_synaptome.find_dv_description_value),
            ("ME-MODEL", explore_synaptome.find_dv_me_model_label, explore_synaptome.find_dv_me_model_value),
            ("M-TYPE", explore_synaptome.find_dv_mtype_label, explore_synaptome.find_dv_mtype_value),
            ("E-TYPE", explore_synaptome.find_dv_etype_label, explore_synaptome.find_dv_etype_value),
            ("BRAIN REGION", explore_synaptome.find_dv_brain_region_label, explore_synaptome.find_dv_brain_region_value),
            ("CREATED BY", explore_synaptome.find_dv_created_by_label,
             explore_synaptome.find_dv_created_by_value),
            ("REGISTRATION DATE", explore_synaptome.find_dv_registration_date_label, explore_synaptome.find_dv_registration_date_value),
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
                logger.error(f"{label_text} check failed: {e}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error in {label_text} check: {e}")
                raise

        # Verify Overview tab is present
        dv_overview_tab = explore_synaptome.find_dv_overview_tab()
        assert dv_overview_tab.is_displayed(), "Synaptome detail view overview tab is not displayed"
        logger.info("Detail view overview tab is found")

        logger.info("Test completed successfully")

        # # Verify table rows are displayed in Public tab
        # lv_row = explore_synaptome.find_lv_row()
        # assert lv_row.is_displayed(), "The table and the rows are not found"
        # logger.info("The table and the rows are displayed in Public tab")
        #
        # explore_synaptome.wait_for_spinner_to_disappear(timeout=25)
        #
        # # Now switch to Project tab to check if table has any data
        # project_tab = explore_synaptome.project_tab(timeout=20)
        # assert project_tab.is_displayed(), "Project tab is not displayed"
        # project_tab.click()
        # logger.info("Project tab is clicked")
        # time.sleep(2)  # Wait for tab content to load
        #
        # # Check if table has any data in Project tab (no search, just check table)
        # try:
        #     project_table = explore_synaptome.find_lv_row()
        #     if project_table.is_displayed():
        #         # Check if there are any rows with data
        #         try:
        #             project_first_row = explore_synaptome.find_lv_first_row(timeout=5)
        #             logger.info("Project tab has synaptome data in the table")
        #         except:
        #             logger.info("Project tab table is empty")
        # except:
        #     logger.info("Project tab has no data or table not found")
        #
        # # Switch back to Public tab to continue with detail view test
        # model_tab.click()
        # logger.info("Switched back to Public tab")
        # time.sleep(2)
        # explore_synaptome.wait_for_spinner_to_disappear(timeout=25)

        # The search results for "SSCx" should still be there from before

