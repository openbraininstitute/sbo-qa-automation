# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import os
import time

from selenium.common import TimeoutException, StaleElementReferenceException
from locators.explore_page_locators import ExplorePageLocators
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage


class OutsideExplorePage(HomePage):
    def __init__(self, browser, wait, base_url):
        super().__init__(browser, wait, base_url)
        self.home_page = HomePage(browser, wait, base_url)

    def go_to_outside_explore_page(self, retries=3, delay=5):
        path = f"/app/virtual-lab/explore/interactive"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(90)
                self.go_to_page(path)
                self.wait_for_page_ready(timeout=90)
            except TimeoutException:
                print(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                time.sleep(delay)  # Wait before retrying
                delay *= 2  # Exponentially increase delay (e.g., 5, 10, 20 seconds)
                if attempt == retries - 1:
                    raise RuntimeError("The Explore page failed to load after multiple attempts.")
            return self.browser.current_url

    def wait_for_dynamically_loaded_links(self):
        self.wait.until(EC.presence_of_element_located(ExplorePageLocators.EXPLORE_LINK1))

    def find_ai_assistant_panel(self, timeout=15):
        return self.find_element(ExplorePageLocators.AI_ASSISTANT_PANEL, timeout=timeout)

    def find_ai_assistant_panel_close(self, timeout=15):
        return self.element_to_be_clickable(ExplorePageLocators.AI_ASSISTANT_PANEL_CLOSE, timeout=timeout)

    def find_ai_assistant_panel_open(self):
        return self.find_element(ExplorePageLocators.AI_ASSISTANT_PANEL_BTN_OPEN)

    def find_atlas_fullscreen_bt(self, timeout=20):
        return self.find_element(ExplorePageLocators.ATLAS_FULLSCREEN, timeout=timeout)

    def find_brain_region_panel(self):
        return self.find_element(ExplorePageLocators.BRAIN_REGION_PANEL)

    def find_brain_region_search_field(self, timeout=20):
        return self.find_element(ExplorePageLocators.SEARCH_REGION, timeout=timeout)

    def find_cerebrum_title_main_page(self, timeout=15):
        return self.find_element(ExplorePageLocators.CEREBRUM_TITLE_MAIN_PAGE, timeout=timeout)

    def find_cerebrum_brp(self, timeout=30):
        return self.find_element(ExplorePageLocators.CEREBRUM_TITLE_BRAIN_REGION_PANEL, timeout=timeout)

    def find_cerebral_cortex_brp(self, timeout=15):
        return self.find_element(ExplorePageLocators.CEREBRAL_CORTEX_TITLE, timeout=timeout)

    def find_cerebrum_arrow_btn(self):
        return self.find_element(ExplorePageLocators.CEREBRUM_BTN)

    def find_data_panel(self):
        return self.find_element(ExplorePageLocators.DATA_PANEL)

    def check_explore_title_is_present(self, timeout=15):
        return self.is_visible(ExplorePageLocators.EXPLORE_TITLE, timeout=timeout)

    def cerebrum_title(self, timeout=15):
        return self.find_element(ExplorePageLocators.CEREBRUM_TITLE_MAIN_PAGE, timeout=timeout)

    def find_explore_page_titles(self, page_locators, timeout=30):
        elements_list = []
        for locator in page_locators:
            elements_list.extend(self.find_all_elements(locator, timeout=timeout))
        return elements_list

    def find_experimental_data_titles(self, exp_data_locators, timeout=25):
        result = []
        for locator in exp_data_locators:
            result.extend(self.find_all_elements(locator, timeout))
        return result

    # def get_experiment_record_count(self, record_count_locators, timeout=40, retries=2):
    #     if timeout is None:
    #         timeout = 60 if os.getenv("CI") == "true" else 40
    #     for attempt in range(retries):
    #         try:
    #             return self._get_counts_with_retry(record_count_locators, timeout)
    #         except TimeoutException as e:
    #             if attempt == retries - 1:
    #                 raise e
    #             time.sleep(5)
    #             self.logger.warning(
    #                 f"Retrying get_experiment_record_count due to timeout... Attempt {attempt + 2}/{retries}")

    # def _get_counts_with_retry(self, record_count_locators, timeout):
    #     record_counts = {}
    #     for locator in record_count_locators:
    #         try:
    #             element = self.find_element(locator)
    #             record_counts[locator] = element.text
    #         except StaleElementReferenceException:
    #             element = self.find_element(locator)
    #             record_counts[locator] = element.text
    #     return record_counts

    def find_3d_atlas(self):
        return self.find_element(ExplorePageLocators.ATLAS)

    def find_fullscreen_exit(self, timeout=20):
        return self.find_element(ExplorePageLocators.FULLSCREEN_EXIT, timeout=timeout)

    def find_count_switch(self):
        return self.find_element(ExplorePageLocators.COUNT_SWITCH)

    def list_of_neurons_panel(self):
        return self.find_all_elements(ExplorePageLocators.NEURONS_PANEL_GRID_MTYPES)

    def find_model_data_title(self):
        return self.find_element(ExplorePageLocators.MODEL_DATA_BTN)

    def find_neurons_panel(self):
        return self.is_visible(ExplorePageLocators.NEURONS_PANEL)

    def find_neurons_mtypes_btn(self):
        return self.find_element(ExplorePageLocators.NEURONS_PANEL_MTYPE_BTN)

    def find_neurons_etype_title(self):
        return self.find_element(ExplorePageLocators.NEURONS_PANEL_ETYPES_TITLE)

    def find_neurons_panel_iso_mtype(self):
        return self.find_element(ExplorePageLocators.NEURONS_PANEL_ISOCORTEX_MTYPE)

    def find_panel_emodel(self):
        return self.find_element(ExplorePageLocators.PANEL_EMODEL)

    def find_panel_memodel(self):
        return self.find_element(ExplorePageLocators.PANEL_MEMODEL)

    def find_panel_synaptome(self):
        return self.find_element(ExplorePageLocators.PANEL_SYNAPTOME)

    def find_selected_brain_region_title(self):
        return self.find_element(ExplorePageLocators.SELECTED_BRAIN_REGION)

    def find_total_count_density(self):
        return self.find_element(ExplorePageLocators.TOTAL_COUNT_DENSITY)

    def find_total_count_n(self):
        return self.find_element(ExplorePageLocators.TOTAL_COUNT_N)

    def find_total_count_switch(self):
        return self.find_element(ExplorePageLocators.TOTAL_COUNT_SWITCH)

    def find_panel_mtype(self):
        return self.find_element(ExplorePageLocators.NEURONS_PANEL_MTYPE)

    def find_visible_experimental_data_titles(self, locators, timeout=30):
        """Return all visible experimental data elements from a list of locators."""
        result = []
        for locator in locators:
            elements = self.visibility_of_all_elements(locator, timeout=timeout)
            result.extend(elements)
        return result