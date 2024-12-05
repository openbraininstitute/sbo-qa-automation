# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

from locators.explore_page_locators import ExplorePageLocators
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage
from util.util_links_checker import LinkChecker
from util.util_scraper import UrlScraper


class ExplorePage(HomePage, LinkChecker):
    def __init__(self, browser, wait):
        super().__init__(browser, wait)
        self.home_page = HomePage(browser, wait)
        # self.url_scraper = UrlScraper()

    def go_to_explore_page(self):
        self.browser.get(self.base_url + "/explore/interactive")
        print("PAGES/EXPLORE_PAGE.PY current url", self.browser.current_url)
        return self.browser.current_url

    # def scrape_links(self):
    #     page_source = self.browser.page_source
    #     links = self.url_scraper.scrape_links(page_source)

    def wait_for_dynamically_loaded_links(self):
        self.wait.until(EC.presence_of_element_located(ExplorePageLocators.EXPLORE_LINK1))

    def check_explore_title_is_present(self):
        return self.element_to_be_clickable(ExplorePageLocators.EXPLORE_TITLE)

    def find_model_data_title(self):
        return self.find_element(ExplorePageLocators.MODEL_DATA_BTN)

    def literature_title(self):
        return self.find_element(ExplorePageLocators.LITERATURE)

    def literature_link(self):
        return self.find_element(ExplorePageLocators.LITERATURE_LINK)

    def find_explore_page_titles(self, page_locators):
        elements_list = []
        for locator in page_locators:
            elements_list.extend(self.find_all_elements(locator))
        return elements_list

    def find_experimental_data_titles(self, exp_data_locators):
        result = []
        for locator in exp_data_locators:
            result.extend(self.find_all_elements(locator))
        return result

    def get_experiment_record_count(self, record_count_locators):
        record_counts = []
        for locator in record_count_locators:
            record = self.find_element(locator)
            record_text = record.text.strip()
            try:
                record_number = int(''.join(filter(str.isdigit, record_text)))
            except ValueError:
                raise ValueError(f"Unable to parse record count from text: {record_text}")
            record_counts.append(record_number)
        return record_counts

    def find_brain_region_panel(self):
        return self.find_element(ExplorePageLocators.BRAIN_REGION_PANEL)

    def find_cerebrum_brp(self, timeout=30):
        return self.find_element(ExplorePageLocators.BRP_CEREBRUM, timeout=timeout)

    def find_cerebral_cortex_brp(self):
        return self.find_element(ExplorePageLocators.CEREBRAL_CORTEX_TITLE)

    def find_cerebrum_arrow_btn(self):
        return self.find_element(ExplorePageLocators.CEREBRUM_BTN)

    def find_3d_atlas(self):
        return self.find_element(ExplorePageLocators.ATLAS)

    def find_atlas_fullscreen_bt(self, timeout=20):
        return self.find_element(ExplorePageLocators.ATLAS_FULLSCREEN, timeout=timeout)

    def find_fullscreen_exit(self, timeout=20):
        return self.find_element(ExplorePageLocators.FULLSCREEN_EXIT, timeout=timeout)

    def find_neurons_panel(self):
        return self.find_element(ExplorePageLocators.NEURONS_PANEL)

    def find_count_switch(self):
        return self.find_element(ExplorePageLocators.COUNT_SWITCH)

    def find_brain_region_search_field(self, timeout=20):
        return self.find_element(ExplorePageLocators.SEARCH_REGION, timeout=timeout)

    def find_selected_brain_region_title(self):
        return self.find_element(ExplorePageLocators.SELECTED_BRAIN_REGION)

    def find_data_panel(self):
        return self.find_element(ExplorePageLocators.DATA_PANEL)

    def find_panel_emodel(self):
        return self.find_element(ExplorePageLocators.PANEL_EMODEL)

    def find_panel_memodel(self):
        return self.find_element(ExplorePageLocators.PANEL_MEMODEL)

    def find_panel_synaptome(self):
        return self.find_element(ExplorePageLocators.PANEL_SYNAPTOME)

    def find_lit_morphology_tab(self):
        return self.find_element(ExplorePageLocators.LITERATURE_MORPHOLOGY_TAB)

    def find_lit_ephys_tab(self):
        return self.find_element(ExplorePageLocators.LITERATURE_EPHYS_TAB)

    def find_lit_ndensity_tab(self):
        return self.find_element(ExplorePageLocators.LITERATURE_NDENSITY_TAB)

    def find_lit_bdensity_tab(self):
        return self.find_element(ExplorePageLocators.LITERATURE_BDENSITY_TAB)

    def find_lit_synapses_tab(self):
        return self.find_element(ExplorePageLocators.LITERATURE_SYNAPSES_TAB)

    def find_literature_panel_data(self, lit_data_locators):
        result = []
        for locator in lit_data_locators:
            result.extend(self.find_all_elements(locator))
        return result
