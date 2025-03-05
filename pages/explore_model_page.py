# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

from selenium.common import ElementNotVisibleException, TimeoutException, \
    StaleElementReferenceException

from pages.explore_page import ExplorePage
from locators.explore_model_locators import ExploreModelPageLocators
from util.util_links_checker import LinkChecker
from util.util_scraper import UrlScraper


class ExploreModelDataPage(ExplorePage, LinkChecker):
    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, base_url)
        self.home_page = ExplorePage(browser, wait, base_url)
        self.url_scraper = UrlScraper()
        self.logger = logger

    def go_to_explore_model_page(self, lab_id: str, project_id: str):
        path = f"/lab/{lab_id}/project/{project_id}/explore/interactive/model/e-model"
        try:
            self.browser.set_page_load_timeout(90)
            self.go_to_page(path)
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



