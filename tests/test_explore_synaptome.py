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

        # Verify table rows are displayed in Public tab
        lv_row = explore_synaptome.find_lv_row()
        assert lv_row.is_displayed(), "The table and the rows are not found"
        logger.info("The table and the rows are displayed in Public tab")

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
        # First verify thumbnail images are visible in mini detail view
        thumbnails = explore_synaptome.find_mini_detail_thumbnails(timeout=20)
        assert len(thumbnails) > 0, "No thumbnail images found in mini detail view"
        logger.info(f"Found {len(thumbnails)} thumbnail image(s) in mini detail view")
        
        # Verify at least one thumbnail is displayed
        visible_thumbnails = [thumb for thumb in thumbnails if thumb.is_displayed()]
        assert len(visible_thumbnails) > 0, "No visible thumbnail images in mini detail view"
        logger.info(f"{len(visible_thumbnails)} thumbnail(s) are visible")

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

        # Verify breadcrumbs exist in detail view
        breadcrumb_data = explore_synaptome.find_breadcrumb_data(timeout=20)
        assert breadcrumb_data.is_displayed(), "Data breadcrumb is not displayed"
        assert breadcrumb_data.text == "Data", f"Expected 'Data', got '{breadcrumb_data.text}'"
        logger.info("Data breadcrumb is found")

        breadcrumb_model = explore_synaptome.find_breadcrumb_model(timeout=20)
        assert breadcrumb_model.is_displayed(), "Model breadcrumb is not displayed"
        assert breadcrumb_model.text == "Model", f"Expected 'Model', got '{breadcrumb_model.text}'"
        logger.info("Model breadcrumb is found")

        breadcrumb_synaptome = explore_synaptome.find_breadcrumb_synaptome(timeout=20)
        assert breadcrumb_synaptome.is_displayed(), "Synaptome breadcrumb is not displayed"
        assert breadcrumb_synaptome.text == "Synaptome", f"Expected 'Synaptome', got '{breadcrumb_synaptome.text}'"
        logger.info("Synaptome breadcrumb is found")

        breadcrumb_close = explore_synaptome.find_breadcrumb_close(timeout=20)
        assert breadcrumb_close.is_displayed(), "Close button is not displayed"
        logger.info("Close button is found")

        # Verify 3 tabs are present and clickable
        dv_overview_tab = explore_synaptome.find_dv_overview_tab()
        assert dv_overview_tab.is_displayed(), "Overview tab is not displayed"
        logger.info("Overview tab is found and displayed")

        dv_config_tab = explore_synaptome.find_dv_configuration_tab()
        assert dv_config_tab.is_displayed(), "Configuration tab is not displayed"
        logger.info("Configuration tab is found and displayed")

        dv_related_artifacts_tab = explore_synaptome.find_dv_related_artifacts_tab()
        assert dv_related_artifacts_tab.is_displayed(), "Related artifacts tab is not displayed"
        logger.info("Related artifacts tab is found and displayed")

        # Verify action buttons are present
        dv_copy_id_btn = explore_synaptome.find_dv_copy_id_btn()
        assert dv_copy_id_btn.is_displayed(), "Copy ID button is not displayed"
        logger.info("Copy ID button is found")

        dv_simulate_btn = explore_synaptome.find_dv_simulate_btn()
        assert dv_simulate_btn.is_displayed(), "Simulate button is not displayed"
        logger.info("Simulate button is found")

        dv_download_btn = explore_synaptome.find_dv_download_btn()
        assert dv_download_btn.is_displayed(), "Download button is not displayed"
        logger.info("Download button is found")

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

        # Click on Configuration tab
        dv_config_tab.click()
        logger.info("Configuration tab is clicked")
        time.sleep(2)
        
        # Verify URL contains /configuration
        current_url = browser.current_url
        assert "/configuration" in current_url, f"Expected '/configuration' in URL, got {current_url}"
        logger.info(f"Configuration tab URL verified: {current_url}")
        
        # Verify 'single neuron model' title
        config_single_neuron_title = explore_synaptome.find_config_single_neuron_model_title()
        assert config_single_neuron_title.is_displayed(), "'single neuron model' title is not displayed"
        logger.info("'single neuron model' title is displayed")
        
        # Verify Configuration tab elements with labels and values
        config_checks = [
            ("Name", explore_synaptome.find_config_name_label, explore_synaptome.find_config_name_value),
            ("NAME", explore_synaptome.find_config_me_model_label, explore_synaptome.find_config_me_model_value),
            ("m-model", explore_synaptome.find_config_m_model_label, explore_synaptome.find_config_m_model_value),
            ("e-model", explore_synaptome.find_config_e_model_label, explore_synaptome.find_config_e_model_value),
            ("Brain Region", explore_synaptome.find_config_brain_region_label, explore_synaptome.find_config_brain_region_value),
            ("E-Type", explore_synaptome.find_config_e_type_label, explore_synaptome.find_config_e_type_value),
            ("M-Type", explore_synaptome.find_config_m_type_label, explore_synaptome.find_config_m_type_value),
        ]
        
        for label_text, find_label_fn, find_value_fn in config_checks:
            try:
                label_el = find_label_fn()
                value_el = find_value_fn()
                
                assert label_el is not None, f"'{label_text}' label element not found"
                assert value_el is not None, f"{label_text} value element not found"
                assert label_el.is_displayed(), f"'{label_text}' label is not displayed"
                assert value_el.is_displayed(), f"{label_text} value is not displayed"
                value = value_el.text.strip()
                assert value != "", f"{label_text} value is empty"
                logger.info(f"Configuration {label_text}: {value}")
                
            except AssertionError as e:
                logger.error(f"Configuration {label_text} check failed: {e}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error in Configuration {label_text} check: {e}")
                raise
        
        # Verify thumbnail images are displayed
        config_thumbnails = explore_synaptome.find_config_thumbnail_images()
        assert len(config_thumbnails) > 0, "No thumbnail images found in configuration tab"
        logger.info(f"Found {len(config_thumbnails)} thumbnail image(s) in configuration tab")
        
        visible_thumbnails = [thumb for thumb in config_thumbnails if thumb.is_displayed()]
        assert len(visible_thumbnails) > 0, "No visible thumbnail images in configuration tab"
        logger.info(f"{len(visible_thumbnails)} thumbnail(s) are visible in configuration tab")
        
        # Verify Synapse groups title
        config_synapse_groups = explore_synaptome.find_config_synapse_groups_title()
        assert config_synapse_groups.is_displayed(), "Synapse groups title is not displayed"
        logger.info("Synapse groups title is displayed")
        
        # Verify View details button
        config_view_details_btn = explore_synaptome.find_config_view_details_btn()
        assert config_view_details_btn.is_displayed(), "View details button is not displayed"
        logger.info("View details button is displayed")
        
        # Get current window handle before clicking
        original_window = browser.current_window_handle
        original_windows = browser.window_handles
        logger.info(f"Original window count: {len(original_windows)}")
        
        # Click View details button - it should open in a new tab
        config_view_details_btn.click()
        logger.info("View details button is clicked")
        time.sleep(2)
        
        # Check if a new tab was opened
        new_windows = browser.window_handles
        logger.info(f"New window count: {len(new_windows)}")
        
        if len(new_windows) > len(original_windows):
            # New tab was opened
            logger.info("View details opened in a new tab")
            # Switch to the new tab
            for window in new_windows:
                if window != original_window:
                    browser.switch_to.window(window)
                    break
            
            # Verify the new tab URL
            time.sleep(2)
            new_tab_url = browser.current_url
            logger.info(f"New tab URL: {new_tab_url}")
            assert "/data/view/memodel/" in new_tab_url, f"Expected '/data/view/memodel/' in URL, got {new_tab_url}"
            logger.info("View details correctly opens ME-model detail page in new tab")
            
            # Close the new tab and switch back to original
            browser.close()
            browser.switch_to.window(original_window)
            logger.info("Closed new tab and switched back to original window")
        else:
            # Same tab navigation
            logger.info("View details navigated in same tab")
            explore_synaptome.wait_for_url_contains("/data/view/memodel/", timeout=20)
            current_url = browser.current_url
            logger.info(f"Redirected to ME-model URL: {current_url}")
            assert "/data/view/memodel/" in current_url, f"Expected '/data/view/memodel/' in URL, got {current_url}"
            logger.info("View details correctly redirects to ME-model detail page")

        logger.info("Test completed successfully")

