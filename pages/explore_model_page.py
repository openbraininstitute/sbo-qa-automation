# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0
import time

from selenium.common import ElementNotVisibleException, TimeoutException, \
    StaleElementReferenceException

from pages.explore_page import ExplorePage
from locators.explore_model_locators import ExploreModelPageLocators
from util.util_links_checker import LinkChecker
from util.util_scraper import UrlScraper


class ExploreModelDataPage(ExplorePage, LinkChecker):
    def __init__(self, browser, wait, logger):
        super().__init__(browser, wait)
        self.home_page = ExplorePage(browser, wait)
        self.url_scraper = UrlScraper()
        self.logger = logger

    def go_to_explore_model_page(self):
        try:
            self.go_to_page("/explore/interactive/model/e-model")
            self.wait_for_page_ready(timeout=60)
        except TimeoutException:
            raise RuntimeError("The Model data page did not load within 60 seconds.")
        return self.browser.current_url

    def find_emodel_tab(self):
        return self.find_element(ExploreModelPageLocators.EMODEL_TAB)

    def find_brain_region_search_field(self, timeout=20):
        return self.find_element(ExploreModelPageLocators.SEARCH_REGION, timeout=timeout)

    def find_brain_region_panel(self):
        return self.find_element(ExploreModelPageLocators.BRAIN_REGION_PANEL)

    def find_br_cerebrum_title(self):
        return self.find_element(ExploreModelPageLocators.BR_CEREBRUM_TITLE)

    def brain_region_panel_close_btn(self):
        return self.find_element(ExploreModelPageLocators.CLOSE_BRAIN_REGION_PANEL_BTN)

    def find_selected_brain_region_title(self):
        return self.find_element(ExploreModelPageLocators.SELECTED_BRAIN_REGION)



