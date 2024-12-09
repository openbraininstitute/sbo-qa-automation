# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

from pages.explore_page import ExplorePage
from locators.explore_ndensity_locators import ExploreNDensityPageLocators
from util.util_links_checker import LinkChecker
from util.util_scraper import UrlScraper


class ExploreNeuronDensityPage(ExplorePage, LinkChecker):
    def __init__(self, browser, wait):
        super().__init__(browser, wait)
        self.home_page = ExplorePage(browser, wait)
        self.url_scraper = UrlScraper()

    def go_to_explore_neuron_density_page(self):
        self.go_to_page("/explore/interactive/experimental/neuron-density")

    def find_load_more_btn(self):
        return self.find_element(ExploreNDensityPageLocators.LOAD_MORE_BUTTON)

    def find_table_rows(self):
        return self.wait.find_all_elements(ExploreNDensityPageLocators.TABLE_ROWS)

    def find_ndensity_tab(self):
        return self.find_element(ExploreNDensityPageLocators.NDENSITY_TAB)

    def find_column_headers(self, column_locators):
        column_headers = []
        for locator in column_locators:
            column_headers.extend(self.find_all_elements(locator))
        return column_headers

    def find_dv_title_header(self, title_locators):
        title_headers = []
        for title in title_locators:
            title_headers.extend(self.find_all_elements(title))
        return title_headers

    def lv_br_row1(self):
        return self.find_element(ExploreNDensityPageLocators.LV_BR_ROW1)

    def find_dv_name(self):
        return self.element_visibility(ExploreNDensityPageLocators.DV_NAME)

    def find_cerebrum_brp(self, timeout=30):
        return self.find_element(ExploreNDensityPageLocators.BRP_CEREBRUM, timeout=timeout)

    def find_registration_date(self):
        return self.find_element(ExploreNDensityPageLocators.LV_REGISTRATION_DATE)

