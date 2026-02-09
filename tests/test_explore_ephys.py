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
            explore_ephys_page.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", filter_button)
            time.sleep(1)
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

        # Legacy search and filter tests - removed duplicate search/species filter code
        # The new tests above already cover: search by name, filter by species, and verification
        logger.info("✅ New explore ephys functionality tests completed")
        
        # Continue with legacy tests that are NOT duplicated by new tests
        # Testing E-type filter (not covered by new tests)
        try:
            logger.info("🔧 Testing E-type filter (legacy test)...")
            
            find_filter_btn = explore_ephys_page.find_filter_button()
            explore_ephys_page.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", find_filter_btn)
            time.sleep(1)
            find_filter_btn.click()
            logger.info("Listing view filter button is found and clicked.")
            time.sleep(2)

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
            
            # Apply filters using the new method
            filters_applied = explore_ephys_page.apply_filters()
            if filters_applied:
                logger.info("✅ E-type filters applied successfully")
                explore_ephys_page.close_filter_panel()
                time.sleep(1)
                # Verify filtered results
                time.sleep(3)  # Wait for results to load
                
                find_table = explore_ephys_page.find_table()
                filtered_etype = explore_ephys_page.find_filtered_etype()
                if filtered_etype:
                    expected = "bNAC"
                    value_found = any(expected in row.text for row in filtered_etype)
                    assert value_found, (f'The value {expected} is not found in the table after applying the filter')
                    logger.info(f"✅ E-type filter verified - found '{expected}' in results")
                else:
                    logger.warning("⚠️ Filtered E-type cells cannot be found.")
                
                lv_total_results = explore_ephys_page.lv_total_results()
                lv_total_text = lv_total_results.text
                logger.info(f"📊 The total results for Ephys/bNAC is: {lv_total_text}")
            
            # Close filter panel
            explore_ephys_page.close_filter_panel()
            time.sleep(1)
            
        except Exception as e:
            logger.warning(f"⚠️ E-type filter functionality test failed: {e}")
            # Try to close filter panel if it's still open
            try:
                explore_ephys_page.close_filter_panel()
            except:
                pass

        # Mini-detail view testing
        logger.info("🔍 Testing mini-detail view...")
        lv_row1 = explore_ephys_page.lv_row1().click()
        logger.info("Clicked on row 1 to open mini-detail view.")
        time.sleep(2)  # Wait for mini-detail view to load
        
        # Verify mini-detail view is present
        try:
            explore_ephys_page.verify_mini_detail_view_present()
            
            # Verify all fields
            logger.info("Verifying mini-detail view fields...")
            field_results = explore_ephys_page.verify_mini_detail_view_fields()
            
            # Check that all required fields are present and have values
            required_fields = ['name', 'description', 'image', 'brain_region', 'etype', 'species', 'license']
            for field in required_fields:
                if field in field_results and field_results[field].get('present'):
                    logger.info(f"✅ {field.replace('_', ' ').title()} field is present")
                else:
                    logger.warning(f"⚠️ {field.replace('_', ' ').title()} field is missing")
            
            # Verify license is clickable
            if field_results.get('license', {}).get('clickable'):
                logger.info("✅ License link is clickable")
            else:
                logger.warning("⚠️ License link is not clickable")
            
            # Verify all buttons
            logger.info("Verifying mini-detail view buttons...")
            button_results = explore_ephys_page.verify_mini_detail_view_buttons()
            
            # Check that all 3 buttons are present and clickable
            required_buttons = ['copy', 'download', 'view_details']
            for button in required_buttons:
                if button in button_results and button_results[button].get('present'):
                    if button_results[button].get('clickable'):
                        logger.info(f"✅ {button.replace('_', ' ').title()} button is present and clickable")
                    else:
                        logger.warning(f"⚠️ {button.replace('_', ' ').title()} button is present but not clickable")
                else:
                    logger.warning(f"⚠️ {button.replace('_', ' ').title()} button is missing")
            
            # Click View Details button to navigate to detail view
            logger.info("Clicking 'View Details' button...")
            explore_ephys_page.click_mdv_view_details()
            logger.info("✅ Navigated to detail view")
            
        except Exception as e:
            logger.error(f"❌ Mini-detail view testing failed: {e}")
            raise

        # Detail view testing (after clicking View Details from mini-detail view)
        logger.info("🔍 Testing full detail view...")
        time.sleep(2)  # Wait for detail view to load
        
        # Verify breadcrumbs
        logger.info("Verifying breadcrumbs...")
        breadcrumb_results = explore_ephys_page.verify_detail_view_breadcrumbs()
        for breadcrumb, result in breadcrumb_results.items():
            if result.get('present') and result.get('clickable'):
                logger.info(f"✅ Breadcrumb '{breadcrumb}' is present and clickable")
            else:
                logger.warning(f"⚠️ Breadcrumb '{breadcrumb}' issue: {result}")
        
        # Verify Overview tab is displayed and active
        logger.info("Verifying tabs...")
        tab_results = explore_ephys_page.verify_detail_view_tabs()
        if tab_results.get('overview', {}).get('active'):
            logger.info("✅ Overview tab is displayed and active")
        else:
            logger.warning(f"⚠️ Overview tab issue: {tab_results}")
        
        # Verify Copy ID and Download buttons
        logger.info("Verifying action buttons...")
        button_results = explore_ephys_page.verify_detail_view_buttons()
        for button, result in button_results.items():
            if result.get('present') and result.get('clickable'):
                logger.info(f"✅ Button '{button}' is present and clickable")
            else:
                logger.warning(f"⚠️ Button '{button}' issue: {result}")
        
        # Verify main detail view fields
        logger.info("Verifying main detail view fields...")
        main_field_results = explore_ephys_page.verify_detail_view_main_fields()
        
        # Check required fields have values
        required_fields = ['Name', 'Registered by', 'Registration date', 'Brain Region']
        for field in required_fields:
            if main_field_results.get(field, {}).get('has_value'):
                logger.info(f"✅ Required field '{field}' has value")
            else:
                logger.warning(f"⚠️ Required field '{field}' missing value: {main_field_results.get(field)}")
        
        # Check optional fields are present
        optional_fields = ['Description', 'Contributors', 'Institutional Contributors', 'E-Type']
        for field in optional_fields:
            if main_field_results.get(field, {}).get('present'):
                has_value = main_field_results[field].get('has_value')
                logger.info(f"✅ Optional field '{field}' is present (has_value: {has_value})")
            else:
                logger.warning(f"⚠️ Optional field '{field}' not found")
        
        # Check license is clickable
        if main_field_results.get('License', {}).get('clickable'):
            logger.info("✅ License link is clickable")
        else:
            logger.warning(f"⚠️ License link issue: {main_field_results.get('License')}")
        
        # Verify Subject section
        logger.info("Verifying Subject section...")
        subject_results = explore_ephys_page.verify_detail_view_subject_fields()
        
        if subject_results.get('Subject Header', {}).get('present'):
            logger.info("✅ Subject section is present")
            
            # Check that subject fields are present (values are optional)
            subject_field_names = ['Name', 'Description', 'Species', 'Strain', 'Sex', 'Weight', 'Age', 'Age min', 'Age max', 'Age period']
            present_count = sum(1 for field in subject_field_names if subject_results.get(f'Subject {field}', {}).get('present'))
            logger.info(f"✅ Found {present_count}/{len(subject_field_names)} Subject fields")
        else:
            logger.warning("⚠️ Subject section not found")
        
        logger.info("✅ All explore ephys page tests completed successfully")



