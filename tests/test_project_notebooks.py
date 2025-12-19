# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

import pytest
from selenium.webdriver.common.by import By

from pages.project_notebooks import ProjectNotebooks


class TestProjectNotebooks:
    @pytest.mark.project_page
    def test_project_notebooks(self, setup, login_direct_complete, logger, test_config):
        browser, wait, base_url, lab_id, project_id = login_direct_complete
        project_notebooks = ProjectNotebooks(browser, wait, logger, base_url)
        print(f"DEBUG: Using lab_id={lab_id}, project_id={project_id}")

        project_notebooks.go_to_project_notebooks_page(lab_id, project_id)
        logger.info("Project Home page loaded successfully")

        project_tab = project_notebooks.project_tab()
        logger.info("Project tab is found")

        public_tab = project_notebooks.public_tab()
        logger.info("Public tab is found")

        expected_headers = [
            "Name",
            "Description",
            "Contributors",
            "Registration date",
            "Scale",
            ""
        ]

        project_notebooks.validate_table_headers(expected_headers)

        search_notebook = project_notebooks.search_notebook()
        assert search_notebook.is_displayed(), "Search input is not displayed"
        logger.info("Search input is found")

        search_notebook.click()
        logger.info("Search input is clicked")

        search_input = project_notebooks.search_input()
        search_input.send_keys("circuit")
        logger.info("Searching for 'circuit' using the free text search")

        project_notebooks.wait_for_scale_to_be("circuit")
        scale_cells = project_notebooks.get_column_cells("Scale")

        for i, cell in enumerate(scale_cells, start=1):
            assert cell.text.strip().lower() == "circuit", f"Row {i}: expected 'circuit', got '{cell.text.strip()}'"

        logger.info("All Scale values are 'circuit'")

        clear_search_input = project_notebooks.clear_search_notebook_input()
        logger.info("Search input is cleared")

        assert search_notebook.get_attribute("value") == "", "Search input is not empty after clearing"
        logger.info("Search input is confirmed to be empty")

        time.sleep(5)
        rows_before_filter = project_notebooks.rows()
        total_rows_before_filter = len(rows_before_filter)
        logger.info(f"Total rows before filter: {total_rows_before_filter}")

        page_filter = project_notebooks.page_filter()
        assert page_filter.is_displayed(), "Page filter is not displayed"
        logger.info("Page filter is found")

        page_filter.click()
        logger.info("Page filter is clicked")

        filter_name_label = project_notebooks.filter_name_label(timeout=10)
        assert filter_name_label.is_displayed(), "Filter name label is not displayed"
        logger.info("Filter name label is found")
        filter_name_label.click()
        logger.info("Filter name label is clicked")

        filter_name_input = project_notebooks.filter_name_input(timeout=10)
        assert filter_name_input.is_displayed(), "Filter name input is not displayed"
        logger.info("Filter name input is found")
        filter_name_input.click()
        logger.info("Filter name input is clicked")

        filter_name_input.send_keys("Visualize skeletonized neuronal")
        logger.info("Filter name input is filled")

        filter_name_label.click()
        logger.info("Filter name label is clicked again")

        filter_scale_title = project_notebooks.filter_scale_title(timeout=10)
        assert filter_scale_title, "'Scale' title inside the filter is not found."
        logger.info("'Scale' title inside Filter is found.")

        filter_contributor_label = project_notebooks.filter_contributor_label(timeout=10)
        assert filter_contributor_label.is_displayed(), "Filter scale input is not displayed"
        logger.info("Filter contributor input is found")
        filter_contributor_label.click()
        logger.info("Filter contributor input is clicked")

        filter_contributor_checkbox = project_notebooks.filter_contributor_checkbox()
        assert filter_contributor_checkbox.is_displayed(), "Filter contributor checkbox is not displayed"
        logger.info("Filter contributor checkbox is found")
        filter_contributor_checkbox.click()
        logger.info("Filter contributor checkbox is clicked")

        filter_apply_btn = project_notebooks.filter_apply_btn()
        assert filter_apply_btn.is_displayed(), "Filter apply button is not displayed"
        logger.info("Filter apply button is found")
        filter_apply_btn.click()
        logger.info("Filter is applied")

        filter_close_btn = project_notebooks.filter_close_btn()
        assert filter_close_btn.is_displayed(), "Filter close button is not displayed"
        logger.info("Filter close button is found")
        filter_close_btn.click()
        logger.info("Filter is closed")

        table_container = project_notebooks.table_container(timeout=10)
        logger.info("Looking for table container")
        time.sleep(5)
        data_search_result = project_notebooks.table_search_result(timeout=20)
        assert data_search_result.is_displayed(), "Table search result is not displayed"
        logger.info("Table search result is found")

        filtered_rows = project_notebooks.rows()
        total_filtered_rows = len(filtered_rows)
        logger.info(f"Total filtered rows: {total_filtered_rows}")

        page_filter.click()
        logger.info("Page filter is clicked")

        filter_clear_btn = project_notebooks.filter_clear_btn(timeout=15)
        assert filter_clear_btn.is_displayed(), "Filter clear button is not displayed"
        logger.info("Filter clear button is found")
        filter_clear_btn.click()
        logger.info("Filter is cleared")

        rows_after_filter = project_notebooks.rows()
        total_rows_after_filter = len(rows_after_filter)
        logger.info(f"Total rows after filter: {total_rows_after_filter}")

        assert total_rows_after_filter == total_rows_before_filter, ("Total rows before filtering and after clearing "
                                                                     "filter are not equal")
        logger.info("Total rows before and after filtering are equal")