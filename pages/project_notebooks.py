# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0


from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from locators.project_notebooks_locators import ProjectNotebooksLocators
from pages.home_page import HomePage


class ProjectNotebooks(HomePage):
    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, base_url)
        self.home_page = HomePage(browser, wait, base_url)
        self.logger = logger

    def go_to_project_notebooks_page(self, lab_id: str, project_id: str):
        path = f"/app/virtual-lab/lab/{lab_id}/project/{project_id}/notebooks"
        try:
            self.browser.set_page_load_timeout(90)
            self.go_to_page(path)
            self.wait_for_page_ready(timeout=60)
        except TimeoutException:
            raise RuntimeError("The Project Notebooks page did not load within 60 seconds.")
        return self.browser.current_url

    def clear_search_notebook_input(self, timeout=15):
        input_field = self.search_input(timeout=timeout)

        # Clear the field
        input_field.clear()

        # Wait until the input is empty, or timeout after `timeout` seconds
        WebDriverWait(self.browser, timeout).until(
            lambda d: input_field.get_attribute("value") == ""
        )

    def filter_clear_btn(self, timeout=15):
        return self.find_element(ProjectNotebooksLocators.FILTER_CLEAR_BTN, timeout=timeout)

    def filter_close_btn(self):
        return self.find_element(ProjectNotebooksLocators.FILTER_CLOSE_BTN)

    def filter_name_input(self, timeout=10):
        return self.find_element(ProjectNotebooksLocators.FILTER_NAME_INPUT, timeout=timeout)

    def filter_scale_title(self, timeout=10):
        return self.find_element(ProjectNotebooksLocators.FILTER_SCALE_TITLE, timeout=timeout)

    def filter_scale_input(self, timeout=10):
        return self.find_element(ProjectNotebooksLocators.FILTER_SELECT_SCALE_INPUT, timeout=timeout)

    def filter_scale_menu_metabolism(self, timeout=10):
        return self.find_element(ProjectNotebooksLocators.FILTER_SCALE_MENU_METABOLISM, timeout=timeout)

    def page_filter(self):
        return self.find_element(ProjectNotebooksLocators.PAGE_FILTER)

    def row1(self):
        return self.find_element(ProjectNotebooksLocators.ROW1)

    def rows(self):
        return self.find_all_elements(ProjectNotebooksLocators.ROWS)

    def table_container(self, timeout=10):
        return self.find_element(ProjectNotebooksLocators.TABLE_CONTAINER, timeout=timeout)

    def table_search_result(self, timeout=20):
        return self.is_visible(ProjectNotebooksLocators.DATA_ROW_KEY_SEARCH_RESULT, timeout=timeout)

    def search_input(self, timeout=10):
        return self.find_element(ProjectNotebooksLocators.SEARCH_NOTEBOOK, timeout=timeout)

    def validate_table_headers(self, expected_headers):
        """
        Validates the column headers of the table. Logs an error if the headers do not match.

        :param expected_headers: List of expected column headers in order.
        :return: None
        """
        try:
            table_element = self.find_element(ProjectNotebooksLocators.TABLE_ELEMENT, timeout=20)
            column_headers = table_element.find_elements(By.TAG_NAME, "th")

            actual_headers = [header.text.strip() for header in column_headers]
            self.logger.info(f"Actual Headers: {actual_headers}")
            print(f"Actual Headers: {actual_headers}")

            if actual_headers != expected_headers:
                self.logger.error(
                    f"Column headers do not match!\nExpected: {expected_headers}\nActual: {actual_headers}"
                )
                raise AssertionError(
                    f"Column headers do not match!\nExpected: {expected_headers}\nActual: {actual_headers}"
                )

            self.logger.info("Table headers validated successfully and match the expected headers.")
            print("Table headers validated successfully and match the expected headers.")
        except TimeoutException:
            self.logger.error("The table element was not found on the Project Notebooks page.")
            raise RuntimeError("The table element was not loaded within the timeout.")


