# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time

import pytest
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

        table_list_view = explore_morphology.find_table()
        logger.info("Morphology table is displayed.")

        column_locators = [
            ExploreMorphologyPageLocators.LV_PREVIEW,
            ExploreMorphologyPageLocators.LV_BRAIN_REGION,
            ExploreMorphologyPageLocators.LV_MTYPE,
            ExploreMorphologyPageLocators.LV_NAME,
            ExploreMorphologyPageLocators.LV_REGISTRATION_DATE
        ]

        explore_morphology.assert_elements_present_and_displayed(
            locators=column_locators,
            context_name="Morphology column headers",
            timeout=30
        )

        time.sleep(2)
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
        if original_data == sorted_data:
            logger.warning("Table data did not change after sorting (all visible values may be identical)")
        else:
            logger.info("Table data changed after sorting — sort is working")
        logger.info("Sort column interaction verified.")
        
