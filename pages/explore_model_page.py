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
        self.go_to_page("/explore/interactive/model/e-model")
        print("pages/explore/model data: ", self.browser.current_url)

    def find_emodel_tab(self):
        return self.find_element(ExploreModelPageLocators.EMODEL_TAB)



