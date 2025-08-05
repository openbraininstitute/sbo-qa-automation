# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time
from tkinter.constants import RADIOBUTTON

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import TimeoutException
import logging

from locators.build_synaptome_locators import BuildSynaptomeLocators
from pages.home_page import HomePage


class BuildSynaptomePage(HomePage):
    def __init__(self, browser, wait, base_url, logger=None):
        super().__init__(browser, wait, base_url)
        self.logger = logger or logging.getLogger(__name__)
        self.home_page = HomePage(browser, wait, base_url)
        self.logger = logger

    def go_to_build_synaptome(self, lab_id: str, project_id: str):
        path = f"/app/virtual-lab/lab/{lab_id}/project/{project_id}/build"
        try:
            self.browser.set_page_load_timeout(120)
            self.go_to_page(path)
            self.wait_for_page_ready(timeout=60)
        except TimeoutException:
            raise RuntimeError("The Build page did not load within 120 seconds.")
        return self.browser.current_url

    def apply_changes_btn(self):
        return self.find_element(BuildSynaptomeLocators.APPLY_CHANGES)

    def add_new_synapse_set(self):
        return self.find_element(BuildSynaptomeLocators.ADD_SYNAPSES_BTN)

    def brain_region_column_header(self, timeout=10):
        return self.find_element(BuildSynaptomeLocators.BRAIN_REGION_COLUMN_HEADER, timeout=timeout)

    def configure_model(self):
        return self.find_element(BuildSynaptomeLocators.CONFIGURE_MODEL)

    def delete_synapse_set(self, timeout=20):
        return self.find_element(BuildSynaptomeLocators.DELETE_SYNAPSE_SET2, timeout=timeout)

    def description_title(self):
        return self.find_element(BuildSynaptomeLocators.DESCRIPTION_TITLE)

    def filter_synapses_btn(self):
        return self.find_element(BuildSynaptomeLocators.FILTER_SYNAPSES_BTN)

    def find_menu_build(self, timeout=25):
        return self.is_visible(BuildSynaptomeLocators.MENU_BUILD, timeout=timeout)

    def find_synaptome_box(self, timeout=10):
        return self.find_element(BuildSynaptomeLocators.SYNAPTOME_BOX, timeout=timeout)

    def find_synaptome_build_btn(self, timeout=10):
        return self.find_element(BuildSynaptomeLocators.SYNAPTOME_BUILD_BTN, timeout=timeout)

    def form_created_by(self):
        return self.find_element(BuildSynaptomeLocators.FORM_CREATED_BY)

    def form_value_created_by(self):
        return self.find_all_elements(BuildSynaptomeLocators.FORM_VALUE_CREATED_BY)

    def form_creation_date(self):
        return self.find_element(BuildSynaptomeLocators.FORM_CREATION_DATE)

    def form_value_creation_date(self):
        return self.find_element(BuildSynaptomeLocators.FORM_VALUE_CREATION_DATE)

    def get_all_table_rows(self):
        """
        Returns all rows in the table body as a list of WebElement objects.
        """
        return self.find_all_elements(BuildSynaptomeLocators.ROWS)

    def get_column_values(self, column_index):
        """
        Returns the values of a specific column for all rows.
        :param column_index: Index of the column to retrieve values (0-based).
        :return: List of text values from the specified column.
        """
        rows = self.find_all_elements(BuildSynaptomeLocators.ROWS)

        column_values = []
        for row in rows:
            cells = self.find_all_elements(BuildSynaptomeLocators.CELLS)
            if column_index < len(cells):
                column_values.append(cells[column_index].text.strip())

        return column_values

    def get_first_table_row_content(self):
        """
        Fetches the content of the first table cell from the first row.
        """
        first_data_row = self.is_visible(BuildSynaptomeLocators.ROW1)

        return [cell.text.strip() for cell in first_data_row.find_elements(By.TAG_NAME, "td")]


    def get_table_content(self):
        # Wait until the table element is present
        table = self.find_element(BuildSynaptomeLocators.TABLE)
        # Wait until at least one row of the table is populated with data
        WebDriverWait(self.browser, 20).until(
            lambda driver: any(
                self.find_all_elements((By.TAG_NAME, "td"), timeout=10) and  # Corrected Tuple Argument
                any(cell.text.strip() for cell in self.find_all_elements((By.TAG_NAME, "td"), timeout=10))
                # Corrected Tuple Argument
                for row in table.find_elements(By.TAG_NAME, "tr")
            ),
            "Table rows are not populated with data within the timeout."
        )

        # Extract table content once it is fully loaded
        rows = self.find_all_elements((By.TAG_NAME, "tr"))  # Corrected Tuple Argument
        table_content = []
        for row in rows:
            # For each row, get all cell elements using the custom helper
            cells = self.find_all_elements((By.TAG_NAME, "td"), timeout=10)  # Corrected Tuple Argument
            # Extract and clean the text content of all cells in the row
            row_content = [cell.text.strip() for cell in cells]
            if row_content:  # Include non-empty rows only
                table_content.append(row_content)

        return table_content

    def input_name_field(self):
        return self.find_element(BuildSynaptomeLocators.INPUT_NAME_FIELD)

    def is_column_sorted(self, column_index, ascending=True):
        """
        Checks if a specific column in the table is sorted in ascending or descending order.
        :param column_index: Index of the column to check sorting for (0-based).
        :param ascending: If True, validates ascending order. If False, validates descending order.
        :return: True if the column is sorted, otherwise False.
        """
        column_values = self.get_column_values(column_index)

        sorted_values = sorted(column_values)
        if not ascending:
            sorted_values = sorted(column_values, reverse=True)

        return column_values == sorted_values

    def input_description_field(self):
        return self.find_element(BuildSynaptomeLocators.INPUT_DESCRIPTION_FIELD)

    def name_your_set(self):
        return self.find_element(BuildSynaptomeLocators.NAME_YOUR_SET_FIELD)

    def name_your_set2(self):
        return self.find_element(BuildSynaptomeLocators.NAME_YOUR_SET_FIELD2)

    def new_synaptome_title(self):
        return self.find_element(BuildSynaptomeLocators.NEW_SYNAPTOME_TITLE)

    def radio_btn(self, timeout=10):
        return self.element_to_be_clickable(BuildSynaptomeLocators.RADIO_BTN_ME_MODEL, timeout=timeout)

    def results_label(self):
        return self.find_element(BuildSynaptomeLocators.RESULTS)

    def save_btn(self, timeout=15):
        return self.find_element(BuildSynaptomeLocators.SAVE_SYNAPTOME_MODEL, timeout=timeout)

    def start_building_button(self):
        return self.element_to_be_clickable(BuildSynaptomeLocators.START_BUILDING_BTN)

    def select_model(self):
        return self.find_element(BuildSynaptomeLocators.SELECT_MODEL)

    def synaptome_form(self):
        return self.find_element(BuildSynaptomeLocators.SYNAPTOME_FORM)

    def synapse_formula(self):
        return self.find_element(BuildSynaptomeLocators.SYNAPSE_FORMULA)

    def synapse_greater_value(self):
        return self.find_element(BuildSynaptomeLocators.SYNAPSE_GREATER_VALUE)

    def synapse_smaller_value(self):
        return self.find_element(BuildSynaptomeLocators.SYNAPSE_SMALLER_VALUE)

    def synapse_set(self, timeout=15):
        return self.find_element(BuildSynaptomeLocators.SYNAPSE_SETS, timeout=timeout)

    def synapse_set_num(self, text, timeout=15):
        return self.text_is_visible(BuildSynaptomeLocators.SYNAPSE_SET_NUM, text, timeout=timeout)

    def target_field(self, timeout=15):
        return self.find_element(BuildSynaptomeLocators.TARGET_FIELD, timeout=timeout)

    def target_field2(self, timeout=15):
        return self.find_element(BuildSynaptomeLocators.TARGET_FIELD2, timeout=timeout)

    def target_list(self, timeout=20):
        return self.find_element(BuildSynaptomeLocators.TARGET_LIST, timeout=timeout)

    def target_list2(self, timeout=20):
        return self.find_element(BuildSynaptomeLocators.TARGET_LIST2, timeout=timeout)

    def target_soma(self, timeout=15):
        return self.find_element(BuildSynaptomeLocators.TARGET_SOMA, timeout=timeout)

    def target_soma2(self, timeout=15):
        return self.find_element(BuildSynaptomeLocators.TARGET_SOMA2, timeout=timeout)

    def canvas(self, timeout=10):
        return self.is_visible(BuildSynaptomeLocators.CANVAS, timeout=timeout)

    def canvas_pointer(self, timeout=10):
        return self.element_visibility(BuildSynaptomeLocators.CANVAS_POINTER, timeout=timeout)

    def target_dropdown_list(self, timeout=10):
        return self.find_element(BuildSynaptomeLocators.TARGET_DROPDOWN_LIST, timeout=timeout)

    def target_select(self, timeout=25):
        return self.element_to_be_clickable(BuildSynaptomeLocators.TARGET_SELECTOR, timeout=timeout)

    def target_select2(self, timeout=25):
        return self.find_element(BuildSynaptomeLocators.TARGET_SELECT2, timeout=timeout)

    # def wait_for_target_dropdown_expanded(self, timeout=25):
    #     return self.is_visible(BuildSynaptomeLocators.TARGET_DROPDOWN_LIST, timeout=timeout)

    def wait_for_target_dropdown_expanded(self, timeout=25):
        WebDriverWait(self.browser, timeout).until(
            lambda d: d.find_element(*BuildSynaptomeLocators.TARGET_INPUT).get_attribute("aria-expanded") == "true"
        )

    def wait_for_target_dropdown_expanded2(self, timeout=25):
        WebDriverWait(self.browser, timeout).until(
            lambda d: d.find_element(*BuildSynaptomeLocators.TARGET_INPUT2).get_attribute("aria-expanded") == "true"
        )

    def type_field(self):
        return self.find_element(BuildSynaptomeLocators.TYPE_FIELD)

    def type_field2(self):
        return self.find_element(BuildSynaptomeLocators.TYPE_FIELD2)

    def type_excitatory(self):
        return self.element_to_be_clickable(BuildSynaptomeLocators.TYPE_EXCITATORY)

    def type_inhibitory(self):
        return self.element_to_be_clickable(BuildSynaptomeLocators.TYPE_INHIBITORY)

    def select_inhibitory(self):
        return self.element_to_be_clickable(BuildSynaptomeLocators.SELECT_INHIBITORY)

    def use_sn_model_btn(self):
        return self.element_to_be_clickable(BuildSynaptomeLocators.USE_SN_MODEL_BTN)

    def wait_for_table_sorting_to_complete(self, timeout=30):
        """
        Waits for the table sorting to be completed by checking for changes in the first row's content.
        """
        initial_table_content = self.get_table_content()

        try:
            WebDriverWait(self.browser, timeout).until(
                lambda driver: self.get_table_content() != initial_table_content,
                "Table sorting did not complete within the provided timeout."
            )
            print("Table sorting is completed. The table content was updated.")
        except TimeoutException:
            current_table_content = self.get_table_content()
            raise Exception(
                f"Table sorting timed out. Initial content: {initial_table_content}, "
                f"Current table content: {current_table_content}. Timeout: {timeout}s."
            )

    def wait_for_spinner_to_disappear(self, timeout=20):
        return self.wait_for_element_to_disappear(BuildSynaptomeLocators.SPIN_CONTAINER, timeout=timeout)

    def wait_for_table_data_to_load(self, timeout=30):
        """
        Waits for at least one row of data (excluding headers) to be visible in the table body.
        """
        self.wait_for_spinner_to_disappear()
        # Then wait for table rows to load
        WebDriverWait(self.browser, timeout).until(
            lambda driver: len(self.get_all_table_rows()) > 0 and "No data" not in self.get_table_content(),
            "Table data is not loaded within the timeout."
        )

    def wait_for_zoom_ui(self, timeout=15):
        return self.is_visible(BuildSynaptomeLocators.ZOOM_UI_CONTAINER, timeout)