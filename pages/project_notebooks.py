# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from locators.project_notebooks_locators import ProjectNotebooksLocators
from pages.home_page import HomePage
from typing import List
from selenium.webdriver.remote.webelement import WebElement

class ProjectNotebooks(HomePage):
    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, base_url)
        self.home_page = HomePage(browser, wait, base_url)
        self.logger = logger

    def go_to_project_notebooks_page(self, lab_id: str, project_id: str, retries=3, delay=5):
        path = f"/app/virtual-lab/{lab_id}/{project_id}/notebooks/public"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(90)
                self.go_to_page(path)
                self.wait_for_page_ready(timeout=60)
            except TimeoutException:
                print(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                time.sleep(delay)
                if attempt == retries - 1:
                    raise RuntimeError("The Project > Notebooks page did not load within 60 seconds")
        return self.browser.current_url

    def clear_search_notebook_input(self, timeout=15):
        input_field = self.search_input(timeout=timeout)

        input_field.clear()

        WebDriverWait(self.browser, timeout).until(
            lambda d: input_field.get_attribute("value") == ""
        )
    def column_headers(self):
        return self.find_all_elements(ProjectNotebooksLocators.COLUMN_HEADER)

    def filter_apply_btn(self):
        return self.find_element(ProjectNotebooksLocators.FILTER_APPLY_BTN)

    def filter_clear_btn(self, timeout=15):
        return self.find_element(ProjectNotebooksLocators.FILTER_CLEAR_BTN, timeout=timeout)

    def filter_close_btn(self):
        return self.find_element(ProjectNotebooksLocators.FILTER_CLOSE_BTN)

    def filter_contributor_label(self, timeout=10):
        return self.find_element(ProjectNotebooksLocators.FILTER_CONTRIBUTOR_LABEL, timeout=timeout)

    def filter_contributor_checkbox(self):
        return self.element_visibility(ProjectNotebooksLocators.FILTER_CONTRIBUTOR_CHECKBOX)

    def filter_name_label(self, timeout=10):
        return self.find_element(ProjectNotebooksLocators.Filter_NAME_LABEL, timeout=timeout)

    def filter_name_input(self, timeout=10):
        return self.find_element(ProjectNotebooksLocators.FILTER_NAME_INPUT, timeout=timeout)

    def filter_scale_title(self, timeout=10):
        return self.find_element(ProjectNotebooksLocators.FILTER_SCALE_TITLE, timeout=timeout)

    def get_column_cells(self, column_name: str) -> List[WebElement]:
        headers = self.column_headers()
        column_index = None

        for i, th in enumerate(headers, start=1):
            if th.text.strip().lower() == column_name.lower():
                column_index = i
                break

        if column_index is None:
            raise ValueError(f"Column '{column_name}' not found")

        xpath = f"//tbody/tr[not(contains(@style,'display: none'))]/td[{column_index}]"
        cells = self.find_all_elements((By.XPATH, xpath))

        return [cell for cell in cells if cell.text.strip()]

    def page_filter(self):
        return self.find_element(ProjectNotebooksLocators.PAGE_FILTER)

    def row1(self):
        return self.find_element(ProjectNotebooksLocators.ROW1)

    def rows(self):
        return self.find_all_elements(ProjectNotebooksLocators.ROWS)

    def project_tab(self):
        return self.find_element(ProjectNotebooksLocators.PROJECT_TAB)

    def public_tab(self):
        return self.find_element(ProjectNotebooksLocators.PUBLIC_TAB)

    def table_container(self, timeout=10):
        return self.find_element(ProjectNotebooksLocators.TABLE_CONTAINER, timeout=timeout)

    def table_body_container(self, timeout=10):
        return self.find_element(ProjectNotebooksLocators.TABLE_BODY_CONTAINER, timeout=timeout)

    def table_search_result(self, timeout=20):
        return self.is_visible(ProjectNotebooksLocators.DATA_ROW_KEY_SEARCH_RESULT, timeout=timeout)

    def search_notebook(self, timeout=10):
        return self.find_element(ProjectNotebooksLocators.SEARCH_NOTEBOOK, timeout=timeout)

    def search_input(self, timeout=10):
        return self.find_element(ProjectNotebooksLocators.SEARCH_INPUT, timeout=timeout)

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

    def wait_for_scale_to_be(self, value: str, timeout: int = 10):
        value = value.lower()

        WebDriverWait(self.browser, timeout).until(
            lambda d: all(
                cell.text.strip().lower() == value
                for cell in self.get_column_cells("Scale")
            )
        )

