# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

import pytest

from pages.project_notebooks import ProjectNotebooks


class TestProjectNotebooks:
    @pytest.mark.project_page
    def test_project_notebooks(self, setup, login, logger, test_config):
        browser, wait, base_url, lab_id, project_id = setup
        project_notebooks = ProjectNotebooks(browser, wait, logger, base_url)
        print(f"DEBUG: Using lab_id={lab_id}, project_id={project_id}")

        project_notebooks.go_to_project_notebooks_page(lab_id, project_id)
        logger.info("Project Home page loaded successfully")

        expected_headers = [
            "Name",
            "Description",
            "Object of interest",
            "Scale",
            "Authors",
            "Creation date",
            ""
        ]

        project_notebooks.validate_table_headers(expected_headers)

        search_notebook = project_notebooks.search_input()
        assert search_notebook.is_displayed(), "Search input is not displayed"
        logger.info("Search input is found")

        search_notebook.send_keys("Single cell")

        result1 = project_notebooks.row1()
        result_text = result1.text
        assert "single cell" in result_text, "Expected 'Single cell' in the result"
        logger.info("Expected 'Single cell' in the result")

        search_notebook.clear()
        logger.info("Search input is cleared")

        assert search_notebook.get_attribute("value") == "", "Search input is not empty after clearing"
        logger.info("Search input is confirmed to be empty")

        page_filter = project_notebooks.page_filter()
        assert page_filter.is_displayed(), "Page filter is not displayed"
        logger.info("Page filter is found")

        page_filter.click()
        logger.info("Page filter is clicked")

        filter_name_input = project_notebooks.filter_name_input()
        assert filter_name_input.is_displayed(), "Filter name input is not displayed"
        logger.info("Filter name input is found")

        filter_name_input.send_keys("Metabolism")
        logger.info("Filter name input is filled")

        filter_scale_input = project_notebooks.filter_scale_input()
        assert filter_scale_input.is_displayed(), "Filter scale input is not displayed"
        logger.info("Filter scale input is found")
        filter_scale_input.click()

        filter_scale_menu_metabolism = project_notebooks.filter_scale_menu_metabolism()
        assert filter_scale_menu_metabolism.is_displayed(), "Filter scale input is not displayed"
        filter_scale_menu_metabolism.click()
        logger.info("Filter scale input is selected")

        filter_close_btn = project_notebooks.filter_close_btn()
        assert filter_close_btn.is_displayed(), "Filter close button is not displayed"
        logger.info("Filter close button is found")
        filter_close_btn.click()
        logger.info("Filter is closed")

        data_search_result = project_notebooks.table_search_result()
        assert data_search_result.is_displayed(), "Table search result is not displayed"
        logger.info("Table search result is found")

        page_filter.click()
        logger.info("Page filter is clicked")

        filter_clear_btn = project_notebooks.filter_clear_btn()
        assert filter_clear_btn.is_displayed(), "Filter clear button is not displayed"
        logger.info("Filter clear button is found")
        filter_clear_btn.click()
        logger.info("Filter is cleared")
        time.sleep(2)
