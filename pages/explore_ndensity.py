# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

from selenium.common import TimeoutException

from pages.explore_page import ExplorePage
from locators.explore_ndensity_locators import ExploreNDensityPageLocators
from util.util_links_checker import LinkChecker
from util.util_scraper import UrlScraper


class ExploreNeuronDensityPage(ExplorePage):
    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, logger, base_url)
        self.logger = logger

    def go_to_explore_neuron_density_page(self, lab_id: str, project_id: str, retries=3, delay=5):
        path = f"/app/virtual-lab/lab/{lab_id}/project/{project_id}/explore/interactive/experimental/neuron-density"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(90)
                self.go_to_page(path)
                self.wait_for_page_ready(timeout=60)
            except TimeoutException:
                print(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                time.sleep(delay)  # Wait before retrying
                delay *= 2  # Exponentially increase delay (e.g., 5, 10, 20 seconds)
                if attempt == retries - 1:
                    raise RuntimeError("The Explore page failed to load after multiple attempts.")
            return self.browser.current_url

    def wait_for_ndensity_tab(self, timeout=60):
        """
        Waits for the neuron density tab to become visible.
        """
        self.wait_for_long_load(ExploreNDensityPageLocators.NDENSITY_TAB, timeout)

    def find_ai_assistant_panel(self, timeout=10):
        return self.find_element(ExploreNDensityPageLocators.AI_ASSISTANT_PANEL, timeout=timeout)

    def find_ai_assistant_panel_close(self, timeout=10):
        return self.find_element(ExploreNDensityPageLocators.AI_ASSISTANT_PANEL_CLOSE, timeout=timeout)

    def find_brain_regions_panel_btn(self):
        return self.find_element(ExploreNDensityPageLocators.BRAIN_REGIONS_PANEL_BTN)

    def find_column_headers(self, column_locators, timeout=30):

        column_headers = []
        for locator in column_locators:
            self.logger.info(f"Checking locator: {locator}")
            try:
                self.element_visibility(locator, timeout=timeout)  # Debug visibility
                elements = self.find_all_elements(locator)
                if not elements:
                    self.logger.warning(f"No elements found with locator {locator}")
                    continue
                if len(elements) > 1:
                    self.logger.info(f"Found multiple elements for {locator}")
                    column_headers.extend(elements)
                else:
                    column_headers.append(elements[0])
            except TimeoutException:
                self.logger.error(f"Timeout: Column header with locator {locator} is not visible after {timeout}s")
                raise
        self.logger.info(f"Found {len(column_headers)} column headers")
        return column_headers

    def find_cerebrum_brp(self, timeout=30):
        return self.is_visible(ExploreNDensityPageLocators.BR_VERTICAL_PANEL_CEREBRUM, timeout=timeout)

    def find_dv_title_header(self, title_locators, timeout=30):
        title_headers = []

        for locator in title_locators:
            self.logger.info(f"Checking locator: {locator}")
            try:
                self.element_visibility(locator, timeout=timeout)
                elements = self.find_all_elements(locator)
                if not elements:
                    self.logger.warning(f"No elements found with locator: {locator}")
                    continue
                if len(elements) > 1:
                    self.logger.info(f"Found multiple elements for: {locator}")
                    title_headers.extend(elements)
                else:
                    title_headers.append(elements[0])
            except TimeoutException:
                self.logger.error(f"Timeout: Title header with locator {locator} is not visible after {timeout}s")
                raise
        self.logger.info(f"Found {len(title_headers)} DV title headers")
        return title_headers

    def find_dv_name_title(self):
        return self.element_visibility(ExploreNDensityPageLocators.DV_NAME_TITLE)

    def find_load_more_btn(self):
        return self.find_element(ExploreNDensityPageLocators.LOAD_MORE_BUTTON)

    def find_lv_contributor_header(self):
        return self.find_element(ExploreNDensityPageLocators.LV_CONTRIBUTORS)

    def find_ndensity_tab(self):
        return self.find_element(ExploreNDensityPageLocators.NDENSITY_TAB)

    def find_registration_date(self):
        return self.find_element(ExploreNDensityPageLocators.LV_REGISTRATION_DATE)

    def find_table_rows(self):
        return self.wait.find_all_elements(ExploreNDensityPageLocators.TABLE_ROWS)

    def find_name_value(self):
        return self.find_element(ExploreNDensityPageLocators.DV_NAME_VALUE)

    def find_description_value(self):
        return self.find_element(ExploreNDensityPageLocators.DV_DESC_VALUE)

    def find_contributors_value(self):
        return self.find_element(ExploreNDensityPageLocators.DV_CONTRIBUTORS_VALUE)

    def find_registration_date_value(self):
        return self.find_element(ExploreNDensityPageLocators.DV_REG_DATE_VALUE)

    def find_species_value(self):
        return self.find_element(ExploreNDensityPageLocators.DV_SPECIES_VALUE)

    def find_mtype_value(self):
        return self.find_element(ExploreNDensityPageLocators.DV_MTYPE_VALUE)

    def find_etype_value(self):
        return self.find_element(ExploreNDensityPageLocators.DV_ETYPE_VALUE)

    def find_density_value(self):
        return self.find_element(ExploreNDensityPageLocators.DV_DENSITY_VALUE)

    def find_num_meas_value(self):
        return self.find_element(ExploreNDensityPageLocators.DV_NUM_MEAS_VALUE)

    def lv_br_row1(self):
        return self.find_element(ExploreNDensityPageLocators.LV_BR_ROW1)

    def scroll_sideways(self):
        return self.element_visibility(ExploreNDensityPageLocators.SCROLL_SIDEWAYS)
