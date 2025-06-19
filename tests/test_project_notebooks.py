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



