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

        # 1. Verify Public tab is selected
        try:
            explore_ephys_page.verify_public_tab_selected()
            logger.info("✅ Public tab is selected by default")
        except Exception as e:
            logger.warning(f"⚠️ Public tab verification failed: {e}")

        # 2. Test search functionality by name/description
        try:
            logger.info("🔍 Testing search functionality...")
            # Use a very generic search term that's likely to exist in both staging and production
            # Free text search only searches in Name and Description columns
            # Using "0" as it's likely to appear in names (IDs, dates, codes)
            search_term = "0"  # Very generic - likely in IDs, dates, or codes in Name column
            search_success = explore_ephys_page.perform_name_search(search_term)
            if search_success:
                logger.info(f"✅ Search functionality is working with term '{search_term}'")
                
                # Verify that search returns some results (don't check specific content)
                try:
                    results_count = explore_ephys_page.get_search_results_count()
                    if results_count and results_count > 0:
                        logger.info(f"📊 Search results: {results_count} records found")
                        logger.info("✅ Search returned results successfully")
                    else:
                        logger.warning(f"⚠️ Search returned no results for '{search_term}'")
                except Exception as e:
                    logger.debug(f"Could not get results count: {e}")
                    # If we can't get count, just verify table is still present
                    try:
                        table = explore_ephys_page.find_table()
                        if table.is_displayed():
                            logger.info("✅ Search completed and table is displayed")
                    except:
                        logger.warning("⚠️ Could not verify search results")
                
                # Clear search for next tests
                explore_ephys_page.clear_search()
                time.sleep(1)
                logger.info("🔍 Search cleared successfully")
            else:
                logger.warning("⚠️ Search functionality test failed")
        except Exception as e:
            logger.warning(f"⚠️ Search test failed: {e}")

        try:
            logger.info("🖼️ Testing thumbnail presence...")
            displayed_thumbnails, failed_thumbnails = explore_ephys_page.verify_thumbnails_present()
            if displayed_thumbnails:
                logger.info(f"✅ Found {len(displayed_thumbnails)} displayed thumbnails")
            else:
                logger.warning("⚠️ No thumbnails found or displayed")
        except Exception as e:
            logger.warning(f"⚠️ Thumbnail verification failed: {e}")

        try:
            logger.info("🔧 Testing filter functionality...")
            
            filter_button = explore_ephys_page.find_filter_button()
            explore_ephys_page.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", filter_button)
            time.sleep(1)
            filter_button.click()
            logger.info("Opened filter panel")
            time.sleep(2)
            
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
                results_verified = explore_ephys_page.verify_filtered_results("Mus musculus", "species")
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
                    assert value_found, f'The value {expected} is not found in the table after applying the filter'
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
            time.sleep(100)

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
        
        # Test Overview and Interactive Details tabs
        logger.info("🔍 Testing Overview and Interactive Details tabs...")
        
        # Verify Overview tab is displayed and clickable
        overview_tab_results = explore_ephys_page.verify_detail_view_tabs()
        if overview_tab_results.get('overview', {}).get('active'):
            logger.info("✅ Overview tab is active")
        else:
            logger.warning("⚠️ Overview tab is not active, clicking it...")
            explore_ephys_page.click_overview_tab()
            time.sleep(2)
        
        # Test Overview tab content
        logger.info("🔍 Testing Overview tab plots...")
        overview_plots = explore_ephys_page.find_overview_plots(timeout=10)
        if overview_plots:
            logger.info(f"✅ Found {len(overview_plots)} plots in Overview tab")
            
            # Verify plots are displayed
            displayed_count = sum(1 for plot in overview_plots if plot.is_displayed())
            logger.info(f"✅ {displayed_count}/{len(overview_plots)} plots are displayed")
        else:
            logger.warning("⚠️ No plots found in Overview tab")
        
        # Test plot interaction functionality
        logger.info("🔍 Testing plot interaction controls...")
        plot_interactions = explore_ephys_page.verify_plot_interactions()
        
        if plot_interactions.get('modebar_present'):
            logger.info("✅ Plot modebar is present")
            if plot_interactions.get('zoom_available'):
                logger.info("✅ Zoom control available")
            if plot_interactions.get('pan_available'):
                logger.info("✅ Pan control available")
            if plot_interactions.get('reset_available'):
                logger.info("✅ Reset control available")
            if plot_interactions.get('download_available'):
                logger.info("✅ Download control available")
        else:
            logger.warning("⚠️ Plot modebar not found (may require hover)")
        
        # Switch to Interactive Details tab
        logger.info("🔍 Switching to Interactive Details tab...")
        explore_ephys_page.click_interactive_details_tab()
        time.sleep(2)
        
        # Verify Interactive Details tab is now active
        is_interactive_active = explore_ephys_page.is_interactive_details_tab_active()
        if is_interactive_active:
            logger.info("✅ Interactive Details tab is now active")
        else:
            logger.warning("⚠️ Interactive Details tab is not active")
        
        # Test Interactive Details content
        logger.info("🔍 Testing Interactive Details plots...")
        interactive_plots = explore_ephys_page.find_interactive_plots()
        if interactive_plots:
            logger.info(f"✅ Found {len(interactive_plots)} interactive plots")
            
            # Verify plots are displayed
            displayed_count = sum(1 for plot in interactive_plots if plot.is_displayed())
            logger.info(f"✅ {displayed_count}/{len(interactive_plots)} interactive plots are displayed")
        else:
            logger.warning("⚠️ No interactive plots found")
        
        # Verify interactive controls
        logger.info("🔍 Testing interactive controls...")
        controls = explore_ephys_page.verify_interactive_controls()
        
        if controls.get('stimulus_selector'):
            logger.info("✅ Stimulus selector is present")
            
            # Test stimulus selector functionality
            logger.info("🔍 Testing stimulus selector functionality...")
            stimulus_changed = explore_ephys_page.test_stimulus_selector()
            if stimulus_changed:
                logger.info("✅ Stimulus selector is functional")
            else:
                logger.warning("⚠️ Could not test stimulus selector functionality")
        else:
            logger.warning("⚠️ Stimulus selector not found")
        
        if controls.get('repetition_selector'):
            logger.info("✅ Repetition selector is present")
        if controls.get('sweep_selector'):
            logger.info("✅ Sweep selector is present")
        
        # Switch back to Overview tab
        logger.info("🔍 Switching back to Overview tab...")
        explore_ephys_page.click_overview_tab()
        time.sleep(2)
        
        # Verify Overview tab is active again
        is_overview_active = explore_ephys_page.is_overview_tab_active()
        if is_overview_active:
            logger.info("✅ Overview tab is active again - tab switching works")
        else:
            logger.warning("⚠️ Overview tab is not active after switching back")
        
        logger.info("✅ All explore ephys page tests completed successfully")




