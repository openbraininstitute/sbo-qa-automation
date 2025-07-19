# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait

from locators.explore_page_locators import ExplorePageLocators
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage
from util.util_links_checker import LinkChecker


class ExplorePage(HomePage):
    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, base_url)
        self.logger = logger

    def go_to_explore_page(self, lab_id: str, project_id: str, retries=3, delay=5):
        path = f"/app/virtual-lab/lab/{lab_id}/project/{project_id}/explore/interactive"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(100)
                self.go_to_page(path)
                self.wait_for_page_ready(timeout=90)
            except TimeoutException:
                print(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                time.sleep(delay)  # Wait before retrying
                delay *= 2  # Exponentially increase delay (e.g., 5, 10, 20 seconds)
                if attempt == retries - 1:
                    raise RuntimeError("The Explore page failed to load after multiple attempts.")
            return self.browser.current_url

    def cerebrum_title_br_panel(self):
        return self.find_element(ExplorePageLocators.CEREBRUM_TITLE_BRAIN_REGION_PANEL)

    def wait_for_dynamically_loaded_links(self):
        self.wait.until(EC.presence_of_element_located(ExplorePageLocators.EXPLORE_LINK1))

    def find_ai_assistant_panel(self, timeout=10):
        return self.find_element(ExplorePageLocators.AI_ASSISTANT_PANEL, timeout=timeout)

    def find_ai_assistant_panel_close(self, timeout=10):
        return self.element_to_be_clickable(ExplorePageLocators.AI_ASSISTANT_PANEL_CLOSE, timeout=10)

    def find_ai_assistant_panel_open(self):
        return self.find_element(ExplorePageLocators.AI_ASSISTANT_PANEL_BTN_OPEN)

    def find_atlas_fullscreen_bt(self, timeout=20):
        return self.find_element(ExplorePageLocators.ATLAS_FULLSCREEN, timeout=timeout)

    def find_brain_region_panel(self, timeout=20):
        return self.find_element(ExplorePageLocators.BRAIN_REGION_PANEL, timeout=timeout)

    def find_brain_region_search_field(self, timeout=20):
        return self.find_element(ExplorePageLocators.SEARCH_REGION, timeout=timeout)

    def find_cerebrum_brp(self, timeout=30):
        return self.find_element(ExplorePageLocators.CEREBRUM_TITLE_BRAIN_REGION_PANEL, timeout=timeout)

    def find_cerebral_cortex_brp(self, timeout=15):
        return self.find_element(ExplorePageLocators.CEREBRAL_CORTEX_TITLE, timeout=timeout)

    def find_cerebrum_arrow_btn(self, timeout=20):
        return self.find_element(ExplorePageLocators.CEREBRUM_BTN_VLAB, timeout=timeout)

    def find_cerebrum_title_main_page(self, timeout=30):
        return self.find_element(ExplorePageLocators.CEREBRUM_TITLE_MAIN_PAGE, timeout=timeout)

    def find_count_switch(self):
        return self.find_element(ExplorePageLocators.COUNT_SWITCH)

    def find_data_panel(self):
        return self.find_element(ExplorePageLocators.DATA_PANEL)

    def check_explore_title_is_present(self, timeout=15):
        return self.find_element(ExplorePageLocators.EXPLORE_TITLE_VLAB, timeout=timeout)

    def find_explore_page_titles(self, page_locators, timeout=30):
        elements_list = []
        for locator in page_locators:
            elements_list.extend(self.visibility_of_all_elements(locator, timeout=timeout))
        return elements_list

    def find_experimental_data_titles(self, exp_data_locators, timeout=30):
        result = []
        for locator in exp_data_locators:
            result.extend(self.find_all_elements(locator, timeout=timeout))
        return result

    def get_experiment_record_count(self, record_count_locators, timeout=40):
        record_counts = []
        for locator in record_count_locators:
            try:
                record = self.wait_for_non_empty_text(locator, timeout)
                record_text = record.text.strip()
                record_number = int(''.join(filter(str.isdigit, record_text)))
                record_counts.append(record_number)
            except TimeoutException:
                raise TimeoutException(f"Timeout: No text found for record at {locator} within {timeout} seconds.")
            except ValueError:
                raise ValueError(f"Could not parse record count from text: '{record_text}'")
        return record_counts

    def find_3d_atlas(self):
        return self.find_element(ExplorePageLocators.ATLAS)

    def find_fullscreen_exit(self, timeout=20):
        return self.find_element(ExplorePageLocators.FULLSCREEN_EXIT, timeout=timeout)

    def list_of_neurons_panel(self):
        return self.find_all_elements(ExplorePageLocators.NEURONS_PANEL_GRID_MTYPES)

    def find_model_data_title(self):
        return self.find_element(ExplorePageLocators.MODEL_DATA_BTN)

    def find_neurons_panel(self):
        return self.is_visible(ExplorePageLocators.NEURONS_PANEL)

    def find_selected_brain_region_title(self):
        return self.find_element(ExplorePageLocators.SELECTED_BRAIN_REGION)

    def find_neurons_mtypes_btn(self):
        return self.find_element(ExplorePageLocators.NEURONS_PANEL_MTYPE_BTN)

    def find_neurons_etype_title(self):
        return self.find_element(ExplorePageLocators.NEURONS_PANEL_ETYPES_TITLE)

    def find_neurons_panel_iso_mtype(self):
        return self.find_element(ExplorePageLocators.NEURONS_PANEL_ISOCORTEX_MTYPE)

    def find_panel_circuit(self):
        return self.find_element(ExplorePageLocators.PANEL_CIRCUIT)

    def find_panel_emodel(self):
        return self.find_element(ExplorePageLocators.PANEL_EMODEL)

    def find_panel_memodel(self):
        return self.find_element(ExplorePageLocators.PANEL_MEMODEL)

    def find_panel_synaptome(self):
        return self.find_element(ExplorePageLocators.PANEL_SYNAPTOME)

    def find_panel_mtype(self):
        return self.find_element(ExplorePageLocators.NEURONS_PANEL_MTYPE)

    def find_total_count_density(self):
        return self.find_element(ExplorePageLocators.TOTAL_COUNT_DENSITY)

    def find_total_count_n(self):
        return self.find_element(ExplorePageLocators.TOTAL_COUNT_N)

    def find_total_count_switch(self):
        return self.find_element(ExplorePageLocators.TOTAL_COUNT_SWITCH)

    def find_visible_experimental_data_titles(self, exp_data_locators, timeout=30):
        """Return all visible experimental data elements from a list of locators."""
        result = []
        for locator in exp_data_locators:
            result.extend(self.visibility_of_all_elements(locator, timeout=timeout))
        return result

    def find_visible_explore_page_titles(self, page_locators, timeout=30):
        elements_list = []
        for locator in page_locators:
            elements_list.extend(self.visibility_of_all_elements(locator, timeout=timeout))
        return elements_list

    def wait_for_locators_to_have_text(self, browser, locators, timeout=20):
        for locator in locators:
            WebDriverWait(self.browser, timeout).until(
                EC.text_to_be_present_in_element(locator, '')
            )

