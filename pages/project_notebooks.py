# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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
    
    def get_column_header_texts(self):
        """Get the text content of all column headers using the specific column title class."""
        try:
            column_title_elements = self.find_all_elements(
                (By.CSS_SELECTOR, "th[data-testid='column-header'] .table-module__1pe1kq__columnTitle"),
                timeout=10
            )
            return [header.text.strip() for header in column_title_elements]
        except Exception as e:
            self.logger.error(f"Failed to get column header texts: {str(e)}")
            return []

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
        """Get all cells in a specific column by column name."""
        try:
            # Get column headers using the improved method
            header_texts = self.get_column_header_texts()
            column_index = None

            # Find the column index
            for i, header_text in enumerate(header_texts, start=1):
                if header_text.lower() == column_name.lower():
                    column_index = i
                    break

            if column_index is None:
                available_columns = ", ".join([f"'{h}'" for h in header_texts])
                raise ValueError(f"Column '{column_name}' not found. Available columns: {available_columns}")

            # Get cells from that column (excluding hidden rows)
            xpath = f"//tbody/tr[not(contains(@style,'display: none'))]/td[{column_index}]"
            cells = self.find_all_elements((By.XPATH, xpath))

            # Filter out empty cells
            return [cell for cell in cells if cell.text.strip()]
            
        except Exception as e:
            self.logger.error(f"Failed to get column cells for '{column_name}': {str(e)}")
            return []

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

    def table_search_result(self, timeout=30):
        """Wait for search results to appear after filtering."""
        try:
            self.find_element(ProjectNotebooksLocators.TABLE_BODY_CONTAINER, timeout=10)
            
            return self.is_visible(ProjectNotebooksLocators.DATA_ROW_KEY_SEARCH_RESULT, timeout=timeout)
        except Exception as e:
            self.logger.error(f"Failed to find table search result: {str(e)}")
            try:
                rows = self.find_all_elements((By.XPATH, "//tbody/tr"), timeout=5)
                if rows:
                    self.logger.info(f"Found {len(rows)} table rows as fallback")
                    return True
                return False
            except:
                return False
    
    def wait_for_filtered_results(self, timeout=30):
        """Wait for filtered results to appear with multiple fallback strategies."""
        try:
            # Strategy 1: Wait for specific search result
            if self.is_visible(ProjectNotebooksLocators.DATA_ROW_KEY_SEARCH_RESULT, timeout=10):
                self.logger.info("✅ Found specific search result")
                return True
        except:
            pass
        
        try:
            # Strategy 2: Wait for any filtered result containing key terms
            if self.is_visible(ProjectNotebooksLocators.DATA_ROW_FILTERED_RESULT, timeout=10):
                self.logger.info("✅ Found filtered result with key terms")
                return True
        except:
            pass
        
        try:
            # Strategy 3: Wait for any visible table rows
            rows = self.find_all_elements(ProjectNotebooksLocators.DATA_ROW_ANY_RESULT, timeout=10)
            if rows:
                self.logger.info(f"✅ Found {len(rows)} visible table rows")
                return True
        except:
            pass
        
        self.logger.error("❌ No filtered results found with any strategy")
        return False

    def search_notebook(self, timeout=10):
        return self.find_element(ProjectNotebooksLocators.SEARCH_NOTEBOOK, timeout=timeout)

    def search_input(self, timeout=10):
        return self.find_element(ProjectNotebooksLocators.SEARCH_INPUT, timeout=timeout)

    def validate_table_headers(self, expected_headers):
        """
        Validates the column headers of the table. Logs an error if the headers do not match.
        Works with Ant Design table structure.

        :param expected_headers: List of expected column headers in order.
        :return: None
        """
        try:
            # Wait for table to load
            table_element = self.find_element(ProjectNotebooksLocators.TABLE_ELEMENT, timeout=20)
            
            # Get all column header elements with the specific class for column titles
            column_title_elements = self.find_all_elements(
                (By.CSS_SELECTOR, "th[data-testid='column-header'] .table-module__1pe1kq__columnTitle"),
                timeout=10
            )
            
            # Extract text from column title elements
            actual_headers = [header.text.strip() for header in column_title_elements]
            
            self.logger.info(f"Expected Headers: {expected_headers}")
            self.logger.info(f"Actual Headers: {actual_headers}")
            print(f"Expected Headers: {expected_headers}")
            print(f"Actual Headers: {actual_headers}")

            # Compare headers
            if len(actual_headers) != len(expected_headers):
                self.logger.error(
                    f"Header count mismatch! Expected {len(expected_headers)} headers, got {len(actual_headers)}"
                )
                raise AssertionError(
                    f"Header count mismatch! Expected {len(expected_headers)} headers, got {len(actual_headers)}"
                )

            for i, (expected, actual) in enumerate(zip(expected_headers, actual_headers)):
                if expected != actual:
                    self.logger.error(
                        f"Header mismatch at position {i+1}! Expected: '{expected}', Actual: '{actual}'"
                    )
                    raise AssertionError(
                        f"Header mismatch at position {i+1}! Expected: '{expected}', Actual: '{actual}'"
                    )

            self.logger.info("✅ Table headers validated successfully and match the expected headers.")
            print("✅ Table headers validated successfully and match the expected headers.")
            
        except TimeoutException:
            self.logger.error("❌ The table element was not found on the Project Notebooks page.")
            raise RuntimeError("The table element was not loaded within the timeout.")
        except Exception as e:
            self.logger.error(f"❌ Error validating table headers: {str(e)}")
            raise

    def wait_for_scale_to_be(self, value: str, timeout: int = 10):
        """Wait for all Scale column cells to have the specified value, handling stale elements."""
        value = value.lower()

        def check_scale_values(driver):
            try:
                # Re-fetch elements on each check to avoid stale element exceptions
                cells = self.get_column_cells("Scale")
                if not cells:
                    return False
                
                # Check if all cells have the expected value
                for cell in cells:
                    try:
                        cell_text = cell.text.strip().lower()
                        if cell_text != value:
                            return False
                    except Exception:
                        # If we get a stale element exception, return False to retry
                        return False
                return True
            except Exception:
                # If any error occurs, return False to retry
                return False

        WebDriverWait(self.browser, timeout).until(check_scale_values)

    def notebook_actions_button_1(self):
        """Get the first notebook action button."""
        return self.find_element(ProjectNotebooksLocators.NOTEBOOK_ACTIONS_BUTTON_1)
    
    def notebook_actions_button_2(self):
        """Get the second notebook action button."""
        return self.find_element(ProjectNotebooksLocators.NOTEBOOK_ACTIONS_BUTTON_2)
    
    def notebook_actions_button_3(self):
        """Get the third notebook action button."""
        return self.find_element(ProjectNotebooksLocators.NOTEBOOK_ACTIONS_BUTTON_3)
    
    def action_menu_readme(self):
        """Get the readme action menu item."""
        return self.find_element(ProjectNotebooksLocators.ACTION_MENU_README)
    
    def action_menu_download(self):
        """Get the download action menu item."""
        return self.find_element(ProjectNotebooksLocators.ACTION_MENU_DOWNLOAD)
    
    def action_menu_run(self):
        """Get the run action menu item."""
        return self.find_element(ProjectNotebooksLocators.ACTION_MENU_RUN)
    
    def modal_close_button(self):
        """Get the modal close button."""
        return self.find_element(ProjectNotebooksLocators.MODAL_CLOSE_BUTTON)

