# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

import pytest

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
            "",
            "Name",
            "Description",
            "Scale",
            "Contributors",
            "Registration date",
        ]

        project_notebooks.validate_table_headers(expected_headers)

        search_toggle = project_notebooks.search_notebook()
        assert search_toggle.is_displayed(), "Search control is not displayed"
        logger.info("Search control is found")

        # Search may already be open (Close search); only click Open search when needed
        search_input = project_notebooks.open_search()
        search_input.clear()
        search_input.send_keys("cellular")
        logger.info("Searching for 'cellular' using the free text search")

        time.sleep(3)  # Wait for search results to load

        # Verify search returned results
        scale_cells = project_notebooks.get_column_cells("Scale")
        assert len(scale_cells) > 0, "Search for 'cellular' should return results"
        logger.info(f"Search returned {len(scale_cells)} results")

        # Log the Scale values found (informational, not asserted)
        scale_values = [cell.text.strip() for cell in scale_cells]
        logger.info(f"Scale values in results: {scale_values}")

        project_notebooks.clear_search_notebook_input()
        logger.info("Search input is cleared")

        search_input = project_notebooks.search_input()
        assert search_input.get_attribute("value") == "", "Search input is not empty after clearing"
        logger.info("Search input is confirmed to be empty")

        time.sleep(5)
        rows_before_filter = project_notebooks.rows()
        total_rows_before_filter = len(rows_before_filter)
        logger.info(f"Total rows before filter: {total_rows_before_filter}")

        page_filter = project_notebooks.page_filter()
        assert page_filter.is_displayed(), "Name column filter is not displayed"
        logger.info("Name column filter is found")

        page_filter.click()
        logger.info("Name column filter is clicked")

        filter_name_input = project_notebooks.filter_name_input(timeout=10)
        assert filter_name_input.is_displayed(), "Filter name input is not displayed"
        logger.info("Filter name input is found")
        filter_name_input.click()
        logger.info("Filter name input is clicked")

        filter_name_input.clear()
        filter_name_input.send_keys("Visualize skeletonized neuronal")
        logger.info("Filter name input is filled")

        filter_apply_btn = project_notebooks.filter_apply_btn()
        assert filter_apply_btn.is_displayed(), "Filter apply button is not displayed"
        logger.info("Filter apply button is found")

        filter_apply_btn.click()
        logger.info("Filter is applied")

        table_body_container = project_notebooks.table_body_container(timeout=15)
        logger.info("Looking for table container")
        
        time.sleep(3)
        
        search_result_found = project_notebooks.wait_for_filtered_results(timeout=30)
        assert search_result_found, "No filtered search results found after applying filter"
        logger.info("✅ Filtered search results found")
        
        try:
            data_search_result = project_notebooks.table_search_result(timeout=10)
            if data_search_result and data_search_result.is_displayed():
                logger.info("✅ Specific search result also found")
        except Exception as e:
            logger.warning(f"Specific search result not found, but filtered results are present: {e}")

        filtered_rows = project_notebooks.rows()
        total_filtered_rows = len(filtered_rows)
        logger.info(f"Total filtered rows: {total_filtered_rows}")
        assert total_filtered_rows < total_rows_before_filter, (
            "Name filter should reduce the number of rows"
        )

        project_notebooks.clear_name_column_filter(timeout=15)
        logger.info("Name column filter cleared")

        rows_after_filter = project_notebooks.rows()
        total_rows_after_filter = len(rows_after_filter)
        logger.info(f"Total rows after filter: {total_rows_after_filter}")

        assert total_rows_after_filter == total_rows_before_filter, ("Total rows before filtering and after clearing "
                                                                     "filter are not equal")
        logger.info("Total rows before and after filtering are equal")