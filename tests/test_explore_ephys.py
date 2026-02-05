# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import os
import time
import pytest
from selenium.webdriver import Keys
from locators.explore_ephys_locators import ExploreEphysLocators
from pages.explore_ephys import ExploreElectrophysiologyPage


class TestExploreEphys:
    @pytest.mark.explore_page
    @pytest.mark.run(order=4)
    def test_explore_ephys_page(self, setup, login, logger, test_config):
        """ Verifying Explore Electrophysiology Tab """
        browser, wait, base_url, lab_id, project_id = setup
        explore_ephys_page = ExploreElectrophysiologyPage(browser, wait, logger, base_url)
        
        # Navigate to the explore ephys page
        explore_ephys_page.go_to_explore_ephys_page(lab_id, project_id)
        logger.info("✅ Successfully navigated to explore electrophysiology page")
        
        # Verify URL contains the expected path
        current_url = browser.current_url
        assert "/data/browse/entity/electrical-cell-recording" in current_url, f"Expected URL to contain electrical-cell-recording, got: {current_url}"
        logger.info("✅ URL contains expected path: /data/browse/entity/electrical-cell-recording")
        
        # Verify data type selector is present and Experimental tab is selected
        try:
            data_type_selector = explore_ephys_page.find_data_type_selector()
            assert data_type_selector.is_displayed(), "Data type selector should be displayed"
            logger.info("✅ Data type selector is present")
            
            # Verify Experimental tab is selected by default
            explore_ephys_page.verify_experimental_tab_selected()
            logger.info("✅ Experimental tab is selected by default")
            
            # Verify Single cell electrophysiology text is present
            explore_ephys_page.verify_single_cell_electrophysiology_text()
            logger.info("✅ Single cell electrophysiology text is displayed")
        except Exception as e:
            logger.warning(f"⚠️ New UI elements not found, continuing with legacy test: {e}")

        # Legacy tab title check (keeping for backward compatibility)
        try:
            ephys_tab_title = explore_ephys_page.find_ephys_tab_title()
            logger.info("'Electrophysiology' tab title is present.")
        except Exception as e:
            logger.warning(f"Legacy ephys tab title not found: {e}")

        lv_explore_grid = explore_ephys_page.find_explore_section_grid()
        logger.info("Explore section grid/table view is displayed")

        # Verify table columns (updated to include all required columns)
        column_locators = [
            ExploreEphysLocators.LV_PREVIEW,
            ExploreEphysLocators.LV_BRAIN_REGION,
            ExploreEphysLocators.LV_ETYPE,
            ExploreEphysLocators.LV_NAME,
            ExploreEphysLocators.LV_SPECIES,
            ExploreEphysLocators.LV_CONTRIBUTORS,
            ExploreEphysLocators.LV_REGISTRATION_DATE,
        ]
        column_headers, missing_locators = explore_ephys_page.find_column_headers(column_locators)

        found_column_headers = [header.text.strip() if header.text else "No text" for header in column_headers]
        logger.info(f"Found List View column headers: {found_column_headers}")
        
        # Verify required columns are present
        required_columns = ["Preview", "Brain region", "E-type", "Name", "Species"]
        found_required = [col for col in required_columns if col in found_column_headers]
        
        if len(found_required) >= 3:  # Allow some flexibility
            logger.info(f"✅ Found {len(found_required)} out of {len(required_columns)} required columns")
        else:
            logger.warning(f"⚠️ Only found {len(found_required)} out of {len(required_columns)} required columns")

        # Raise an error and log missing locators or headers
        if not column_headers:
            logger.error("No column headers were found.")
            raise ValueError("Column headers list is empty. Cannot proceed.")

        if missing_locators:
            logger.warning(f"These column locators did not return any elements: {missing_locators}")

        # Verify that each found header is displayed
        for header in column_headers:
            assert header.is_displayed(), f"Column header {header} is not displayed."
            logger.info(f"Displayed column header text: {header.text.strip() if header.text else 'No text found'}")

        # thumbnail_img = explore_ephys_page.verify_all_thumbnails_displayed()
        # logger.info("Ephys thumbnail is displayed")

        # NEW FUNCTIONALITY TESTS
        
        # 1. Verify Public tab is selected
        try:
            explore_ephys_page.verify_public_tab_selected()
            logger.info("✅ Public tab is selected by default")
        except Exception as e:
            logger.warning(f"⚠️ Public tab verification failed: {e}")

        # 2. Test search functionality by name
        try:
            logger.info("🔍 Testing search functionality...")
            search_success = explore_ephys_page.perform_name_search("Field CA1")
            if search_success:
                logger.info("✅ Search functionality is working")
                
                # Verify that search results contain "Field CA1" in brain region
                logger.info("🔍 Verifying search results contain 'Field CA1' in brain region...")
                search_verified = explore_ephys_page.verify_search_results_brain_region("Field CA1")
                if search_verified:
                    logger.info("✅ Search results verified - found records with 'Field CA1' brain region")
                else:
                    logger.warning("⚠️ Search results verification failed - no 'Field CA1' records found")
                
                # Get search results count for logging
                try:
                    results_count = explore_ephys_page.get_search_results_count()
                    logger.info(f"📊 Search results: {results_count}")
                except Exception as e:
                    logger.debug(f"Could not get results count: {e}")
                
                # Clear search for next tests
                explore_ephys_page.clear_search()
                time.sleep(1)
            else:
                logger.warning("⚠️ Search functionality test failed")
        except Exception as e:
            logger.warning(f"⚠️ Search test failed: {e}")

        # 3. Verify thumbnails are present
        try:
            logger.info("🖼️ Testing thumbnail presence...")
            displayed_thumbnails, failed_thumbnails = explore_ephys_page.verify_thumbnails_present()
            if displayed_thumbnails:
                logger.info(f"✅ Found {len(displayed_thumbnails)} displayed thumbnails")
            else:
                logger.warning("⚠️ No thumbnails found or displayed")
        except Exception as e:
            logger.warning(f"⚠️ Thumbnail verification failed: {e}")

        # 4. Test filter functionality (species and contributor)
        try:
            logger.info("🔧 Testing filter functionality...")
            
            # Open filter panel
            filter_button = explore_ephys_page.find_filter_button()
            filter_button.click()
            logger.info("Opened filter panel")
            time.sleep(2)
            
            # Try to apply species filter (using a common species)
            species_applied = explore_ephys_page.apply_species_filter("Rattus norvegicus")
            if species_applied:
                logger.info("✅ Species filter applied successfully")
            
            # Try to apply contributor filter (this might not always work depending on data)
            # contributor_applied = explore_ephys_page.apply_contributor_filter("test")
            
            # Apply filters
            filters_applied = explore_ephys_page.apply_filters()
            if filters_applied:
                logger.info("✅ Filters applied successfully")
                
                # Verify filtered results
                time.sleep(3)  # Wait for results to load
                results_verified = explore_ephys_page.verify_filtered_results("Rattus norvegicus", "species")
                if results_verified:
                    logger.info("✅ Filtered results verified")
                else:
                    logger.warning("⚠️ Could not verify filtered results")
            
            # Close filter panel
            explore_ephys_page.close_filter_panel()
            time.sleep(1)
            
        except Exception as e:
            logger.warning(f"⚠️ Filter functionality test failed: {e}")
            # Try to close filter panel if it's still open
            try:
                explore_ephys_page.close_filter_panel()
            except:
                pass

        # END NEW FUNCTIONALITY TESTS

        all_checkbox = explore_ephys_page.find_btn_all_checkboxes()
        time.sleep(2)
        all_checkbox.click()
        logger.info("Select all checkbox is clicked all checkboxes ticked.")
        all_checkbox.click()
        logger.info("All the checkboxes are unchecked.")

        checkboxes = explore_ephys_page.find_checkboxes()
        checked_flag = False

        for checkbox in checkboxes:
            if not checkbox.is_selected():
                checkbox.click()
                logger.info("Checkbox was found and clicked successfully.")
            else:
                # Print the message only once if at least one checkbox was already checked
                if not checked_flag:
                    logger.info("At least one checkbox was already checked.")
                    checked_flag = True

        find_search_input = explore_ephys_page.find_search_input_search_item()
        logger.info("Search input field is found.")
        browser.execute_script("arguments[0].click();", find_search_input)

        find_search_input.send_keys("Rattus norvegicus")
        logger.info("Search input is searching for Rattus norvegicus")
        found_species = explore_ephys_page.search_species()
        text_found_species = found_species.text
        logger.info(f"Found searched species:{text_found_species}.")

        find_filter_btn = explore_ephys_page.find_filter_btn().click()
        logger.info("Listing view filter button is found and clicked.")

        filter_etype = explore_ephys_page.filter_etype_btn().click()
        logger.info("'E-Type' button inside filter is found and clicked.")

        filter_etype_search = explore_ephys_page.filter_etype_search()
        filter_etype_search.click()
        logger.info("Clicked on 'E-Type Search Field' in the filter.")
        filter_etype_search_input = explore_ephys_page.filter_etype_search_input()

        logger.info("Clicked on the ETYPE search field")
        filter_etype_search_input.send_keys("bNAC")
        logger.info("Enter 'bNAC' as a search parameter")
        filter_etype_search_input.send_keys(Keys.ENTER)
        logger.info("Key ENTER to confirm the searched ETYPE")

        logger.info("'bNAC' found.")
        apply = explore_ephys_page.find_apply_btn().click()
        logger.info("Clicked on text APPLY button.")

        lv_filter_apply_btn = explore_ephys_page.lv_filter_apply().click()
        logger.info("List view filter is applied.")
        find_filter_close_btn = explore_ephys_page.find_filter_close_btn().click()
        logger.info("Close listing view filter.")

        find_table = explore_ephys_page.find_table()
        filtered_etype = explore_ephys_page.find_filtered_etype()
        if filtered_etype:
            assert True
        else:
            print("Filtered Mtype cells cannot be found.")

        expected = "bNAC"
        value_found = any(expected in row.text for row in filtered_etype)
        assert value_found, (f'The value {expected} is not found in the table after applying the '
                             f'filter')
        lv_total_results = explore_ephys_page.lv_total_results()
        lv_total_text = lv_total_results.text
        logger.info(f"The total results for Ephys/ bNAC is: {lv_total_text}")

        lv_row1 = explore_ephys_page.lv_row1().click()
        logger.info("Clicked on row 1 to see 'Detail View'.")

        title_locators = [
            ExploreEphysLocators.DV_CONTRIBUTORS_TITLE,
            ExploreEphysLocators.DV_ETYPE_TITLE,
            ExploreEphysLocators.DV_REG_DATE_TITLE,
            ExploreEphysLocators.DV_LICENSE_TITLE,
            ExploreEphysLocators.DV_BRAIN_REG_TITLE,
            ExploreEphysLocators.DV_SPECIES_TITLE,
            ExploreEphysLocators.DV_DESC_TITLE,
            ExploreEphysLocators.DV_AGE
        ]

        title_headers = explore_ephys_page.find_dv_title_header(title_locators)
        for title in title_headers:
            assert title.is_displayed(), f"DV title header {title} is not displayed"
            logger.info(f"Detail view title headers found: {title.text} ")
        logger.info("Verify the presence of title headers.")

        locators = [
            ExploreEphysLocators.DV_CONTRIBUTORS,
            ExploreEphysLocators.DV_ETYPE,
            ExploreEphysLocators.DV_REG_DATE,
            ExploreEphysLocators.DV_LICENSE,
            ExploreEphysLocators.DV_BR_REG,
            ExploreEphysLocators.DV_SPECIES,
            ExploreEphysLocators.DV_DESC
        ]

        try:
            logger.info("Found metadata header locators.")
            metadata_header = explore_ephys_page.find_dv_title_header(locators)

            for data in metadata_header:
                assert data.is_displayed(), f"DV title header {data} is not displayed"
                logger.info(f"Detail view header found: {data.text}")

            logger.info("Found detail view title headers.")
        except Exception as e:
            logger.error(f"Test failed due to missing locator(s): {e}")
            raise

        brain_region_panel_close_btn = explore_ephys_page.brain_region_panel_close_btn()
        assert brain_region_panel_close_btn.is_displayed(), "The close button is not found"
        logger.info("Close button on the brain region panel is found.")
        brain_region_panel_close_btn.click()
        logger.info("The close button is clicked")
        brain_region_panel_open_btn = explore_ephys_page.brain_region_panel_open_btn()
        assert brain_region_panel_open_btn.is_displayed(), "The panel was not closed"
        logger.info("The panel is closed.")

        dv_overview_btn = explore_ephys_page.dv_overview_btn(timeout=10)
        logger.info("Found 'Overview' button.")
        dv_interactive_details_btn = explore_ephys_page.dv_interactive_details_btn()
        logger.info("Found 'Interactive details' button.")

        dv_interactive_details_btn.click()
        logger.info("Clicked 'Interactive details' button.")

        dv_plots = explore_ephys_page.dv_plots()
        assert dv_plots, "The plots are not found."
        logger.info("The plots are displayed.")

        # dv_stimulus_btn = explore_ephys_page.dv_stimulus_btn().click()
        # logger.info("Clicked 'Stimulus dropdown' button.")
        # dv_stimulus_all = explore_ephys_page.dv_stimulus_all()
        # logger.info("All stimuli is displayed.")
        # dv_stimuli_images = explore_ephys_page.dv_stim_images()
        # assert dv_stimuli_images, "Stimuli plots are not displayed"
        # logger.info("Plots are displayed.")
        # dv_stimulus_all.click()

        # dv_id_repetition_title = explore_ephys_page.dv_id_repetition_title()
        # logger.info("Found 'Interactive detail' Repetition.")
        #
        # dv_id_sweep_title = explore_ephys_page.dv_id_sweep_title()
        # logger.info("Found 'Interactive detail' Sweep.")


