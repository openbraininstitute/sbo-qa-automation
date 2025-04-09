# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

from selenium.common import TimeoutException

from pages.explore_page import ExplorePage
from locators.explore_ndensity_locators import ExploreNDensityPageLocators
from util.util_links_checker import LinkChecker
from util.util_scraper import UrlScraper


class ExploreNeuronDensityPage(ExplorePage, LinkChecker):
    def __init__(self, browser, wait, base_url):
        super().__init__(browser, wait, base_url)
        self.home_page = ExplorePage(browser, wait, base_url)
        self.url_scraper = UrlScraper()

    def go_to_explore_neuron_density_page(self, lab_id: str, project_id: str, retries=3, delay=5):
        path = f"/lab/{lab_id}/project/{project_id}/explore/interactive/experimental/neuron-density"
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

    def find_ai_assistant_panel(self):
        return self.find_element(ExploreNDensityPageLocators.AI_ASSISTANT_PANEL)

    def find_ai_assistant_panel_close(self):
        return self.find_element(ExploreNDensityPageLocators.AI_ASSISTANT_PANEL_CLOSE)

    def find_column_headers(self, column_locators, timeout=60):
        column_headers = []
        for locator in column_locators:
            try:
                self.element_visibility(locator, timeout=timeout),
                elements = self.find_all_elements(locator)
                if len(elements) > 1:
                    column_headers.extend(elements)
                else:
                    column_headers.append(elements[0])
            except TimeoutException:
                print(f"Column header with locator {locator} is not visible")
                raise
        return column_headers

    def find_dv_title_header(self, title_locators):
        title_headers = []
        for title in title_locators:
            title_headers.extend(self.find_all_elements(title))
        return title_headers

    def lv_br_row1(self):
        return self.find_element(ExploreNDensityPageLocators.LV_BR_ROW1)

    def find_cerebrum_brp(self, timeout=30):
        return self.find_element(ExploreNDensityPageLocators.BRP_CEREBRUM, timeout=timeout)

    def find_dv_name(self):
        return self.element_visibility(ExploreNDensityPageLocators.DV_NAME)

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




