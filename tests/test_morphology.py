# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
from asyncio import timeout

import pytest
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from locators.explore_morphology_locators import ExploreMorphologyPageLocators
from pages.explore_morphology import ExploreMorphologyPage


class TestExploreMorphologyPage:
    @pytest.mark.explore_page
    @pytest.mark.run(order=4)
    def test_explore_morphology(self, setup, login_direct_complete, logger, test_config):
        browser, wait, base_url, lab_id, project_id = login_direct_complete
        explore_morphology = ExploreMorphologyPage(browser, wait, logger, base_url)
        print(f"DEBUG: Using lab_id={lab_id}, project_id={project_id}")
        explore_morphology.go_to_explore_morphology_page(lab_id, project_id)
        logger.info("Explore morphology page is displayed")

        ai_assistant_panel = explore_morphology.find_ai_assistant_panel(timeout=25)
        logger.info("AI Assistant panel is open. Attempting to close it.")

        ai_assistant_open_btn = explore_morphology.find_ai_assistant_panel_open()
        assert ai_assistant_open_btn.is_displayed(), "AI Assistant panel is still open."
        logger.info("AI Assistant open button is displayed, means the panel is open.")
        ai_assistant_open_btn.click()

        ai_assistant_panel_close_btn = explore_morphology.find_ai_assistant_panel_close()
        assert ai_assistant_panel_close_btn.is_displayed(), ("Close button on the AI literature search panel is not "
                                                             "found")
        ai_assistant_panel_close_btn.click()
        logger.info("AI assistant panel is closed ")
        table_list_view = explore_morphology.find_table()
        logger.info("Morphology table is displayed.")

        column_locators = [
            ExploreMorphologyPageLocators.LV_PREVIEW,
            ExploreMorphologyPageLocators.LV_BRAIN_REGION,
            ExploreMorphologyPageLocators.LV_MTYPE,
            ExploreMorphologyPageLocators.LV_NAME,
            ExploreMorphologyPageLocators.LV_SPECIES,
            ExploreMorphologyPageLocators.LV_REGISTRATION_DATE
        ]

        explore_morphology.assert_elements_present_and_displayed(
            locators=column_locators,
            context_name="Morphology column headers",
            timeout=10
        )

        thumbnail_img = explore_morphology.verify_all_thumbnails_displayed()
        logger.info("Morphology thumbnail is displayed.")
        for thumbnail in thumbnail_img:
            assert thumbnail['is_displayed'], f"Thumbnail {thumbnail['element']} is not displayed!"
            logger.info(f"Thumbnail {thumbnail['element']} is displayed.")

        morphology_results = explore_morphology.find_results()
        logger.info("Total number of results for morphology tab is displayed.")

        original_data = explore_morphology.get_table_data()
        logger.info("Fetch table data before sorting")


        br_sort_arrow = explore_morphology.find_br_sort_arrow()
        br_sort_arrow.click()
        logger.info("Click the column sort arrow.")
        
        explore_morphology.wait_for_page_ready(timeout=15)
        logger.info("Wait for the sorting action to complete.")
        sorted_data = explore_morphology.get_table_data()
        assert original_data != sorted_data, "Table data did not change after sorting."
        logger.info("Asserting that the table data was sorted.")
        
        '''

        morphology_filter = explore_morphology.morphology_filter()
        morphology_filter.click()
        logger.info("Filter is toggled open")

        filter_mtype = explore_morphology.filter_mtype()
        logger.info("In the filter Mtype button is displayed.")
        filter_mtype.click()
        logger.info("In the filter Mtype button is clicked.")
        time.sleep(2)

        filter_mtype_search = explore_morphology.filter_mtype_search()
        logger.info("In the filter Mtype Search Field is found.")
        filter_mtype_search.click()
        logger.info("In the filter Mtype Search Field is CLICKED.")

        filter_mtype_text_input = explore_morphology.filter_mtype_text_input()
        if filter_mtype_text_input:
            logger.info("Text input field is found.")
        else:
            logger.error("input_id is not valid or cannot be found.")
        filter_mtype_text_input.click()
        logger.info("Text input field is CLICKED.")
        filter_mtype_text_input.send_keys("L5_TPC:A")
        logger.info("Looking for L5_TPC:A")
        filter_mtype_text_input.send_keys(Keys.ENTER)
        logger.info("L5_TPC:A is typed in the search field.")
        explore_morphology.wait_for_page_ready(timeout=15)
        lv_filter_search_field = explore_morphology.lv_filter_search_field()
        lv_filter_search_field.click()
        lv_filter_apply_btn = explore_morphology.lv_filter_apply(timeout=10)
        assert lv_filter_apply_btn, f"The APPLY button is not found"
        logger.info("Inside the filter 'Apply' button is FOUND.")
        lv_filter_apply_btn.click()
        logger.info("Inside the filter 'Apply' button is CLICKED.")

        close_filter = explore_morphology.morphology_filter_close_btn()
        logger.info("Find button to close the filter.")
        close_filter.click()
        logger.info("Filter panel is CLOSED.")
        assert explore_morphology.is_filter_panel_closed(), ("Filter panel was not closed "
                                                             "successfully.")

        find_table = explore_morphology.find_table()
        filtered_mtype = explore_morphology.find_filtered_mtype()
        if filtered_mtype:
            assert True
        else:
            print("Filtered Mtype cells cannot be found")

        expected = "L5_TPC:A"
        value_found = any(expected in row.text for row in filtered_mtype)
        assert value_found, (f'The value {expected} is not found in the table after applying the '
                             f'filter')

        morphology_filter = explore_morphology.morphology_filter()
        morphology_filter.click()
        logger.info("Filter is toggled open")
        clear_filters_btn = explore_morphology.clear_filters_btn().click()
        logger.info("Filter cleared")
        close_filter = explore_morphology.morphology_filter_close_btn().click()
        logger.info("Find button to and close the filter.")

        find_search_input = explore_morphology.find_search_input_search_item()
        logger.info("Search input field is found")
        browser.execute_script("arguments[0].click();", find_search_input)

        find_search_input.send_keys("mtC070301B_idC")
        logger.info("Search input is searching for 'mtC070301B_idC'")
        found_name = explore_morphology.search_name()
        logger.info("Searching for name")
        text_found_name = found_name.text
        logger.info(f"Found searched species:{text_found_name}")
        found_name.click()
        logger.info("Clicked on the researched name")

        dv_header_locators = [
            ExploreMorphologyPageLocators.DV_BRAIN_REGION_TITLE,
            ExploreMorphologyPageLocators.DV_NAME_TITLE,
            ExploreMorphologyPageLocators.DV_SPECIES_TITLE,
            ExploreMorphologyPageLocators.DV_DESCRIPTION_TITLE,
            ExploreMorphologyPageLocators.DV_CONTRIBUTORS_TITLE,
            ExploreMorphologyPageLocators.DV_REGISTRATION_DATE_TITLE,
            ExploreMorphologyPageLocators.DV_LICENSE_TITLE,
            ExploreMorphologyPageLocators.DV_MTYPE_TITLE
        ]

        try:
            logger.info("Found metadata header locators.")
            dv_header_locators = explore_morphology.find_dv_title_header(dv_header_locators)

            for data in dv_header_locators:
                assert data.is_displayed(), f"DV title header {data} is not displayed"
                logger.info(f"Detail view header found: {data.text}")

            logger.info("Found detail view title headers.")
        except Exception as e:
            logger.error(f"Test failed due to missing locator(s): {e}")
            raise

        morphometrics_title = explore_morphology.find_morphometrics_title()
        morpho_title = morphometrics_title.text
        assert morpho_title == "Morphometrics"

        morphology_titles = [
            ExploreMorphologyPageLocators.DV_NM_TITLE,
            ExploreMorphologyPageLocators.DV_AXON_TITLE,
            ExploreMorphologyPageLocators.DV_BD_TITLE,
            ExploreMorphologyPageLocators.DV_AP_TITLE,
            ExploreMorphologyPageLocators.DV_SOMA_TITLE
        ]
        logger.info("Found 'Detail view' titles.")
        morphology_titles = explore_morphology.find_morphology_titles(morphology_titles)

        try:
            logger.info("Found metadate header locators.")
            morphology_titles = explore_morphology.find_dv_title_header(morphology_titles)

            for data in morphology_titles:
                assert data.is_displayed(), f"DV title header {data} is not displayed"
                logger.info(f"Detail view header found: {data.text}")

            logger.info("Found detail view title headers.")
        except Exception as e:
            logger.error(f"Test failed due to missing locator(s): {e}")
            raise

        morpho_viewer = explore_morphology.find_morpho_viewer()
        logger.info("Morphology viewer is displayed")
        morpho_fullscreen_btn = explore_morphology.find_fullscreen_btn()
        logger.info("Morphology viewer full screen button is displayed")
        morpho_fullscreen_btn.click()
        logger.info("Click to view morphology full screen")
        morpho_viewer_settings_btn = explore_morphology.morpho_viewer_settings_btn()
        morpho_viewer_settings_btn.click()
        logger.info("Morphology viewer settings button clicked")
        morpho_fullscreen_btn.click()
        logger.info("Close full screen")
        # time.sleep(10)
        download_btn = explore_morphology.find_download_btn()
        logger.info("Morphology 'Download' button is displayed")

        try:
            back_btn = explore_morphology.find_back_to_list_btn()
            browser.execute_script("arguments[0].scrollIntoView(true);", back_btn)
            logger.info("Found the Back button to go back to list view")
            # 1 sec delay is necessary to ensure scrolling is complete
            time.sleep(1)
            back_btn.click()
            logger.info("'Back to list' button to go back to list view is clicked.")
        except TimeoutException:
            print("Timed out waiting for page to load")
            logger.info("The 'Back to list' button was not displayed.")

        back_to_ie = explore_morphology.find_back_to_ie_btn()
        logger.info("Back to Interactive exploration button found.")
        back_to_ie.click()
        logger.info("Returned to the Interactive exploration page.")
'''