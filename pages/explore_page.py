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
        self.browser.get(self.base_url + "/main")
        return self.browser.current_url

    # def scrape_links(self):
    #     page_source = self.browser.page_source
    #     links = self.url_scraper.scrape_links(page_source)

    def wait_for_dynamically_loaded_links(self):
        self.wait.until(EC.presence_of_element_located(ExplorePageLocators.EXPLORE_LINK1))

    def check_explore_title_is_present(self):
        return self.element_to_be_clickable(ExplorePageLocators.EXPLORE_TITLE)

    def brain_models_title(self):
        return self.find_element(ExplorePageLocators.BRAIN_MODELS)

    # def interactive_exploration_title(self):
    #     return find_element(self.wait, ExplorePageLocators.INTERACTIVE_EXPLORATION)
    #
    # def interactive_exploration_link(self):
    #     return find_element(self.wait, ExplorePageLocators.INTERACTIVE_EXPLORATION_LINK)

    # def simulations_link(self):
    #     return self.wait.until(EC.presence_of_element_located(ExplorePageLocators.SIMULATIONS_LINK))
    #
    # def simulations_title(self):
    #     return self.wait.until(EC.presence_of_element_located(ExplorePageLocators.SIMULATIONS))

    # def portals_title(self):
    #     return find_element(self.wait, ExplorePageLocators.PORTALS)
    #
    # def gallery_title(self):
    #     return find_element(self.wait, ExplorePageLocators.GALLERY)
    #
    # def literature_title(self):
    #     return find_element(self.wait, ExplorePageLocators.LITERATURE)
    #
    # def portals_link(self):
    #     return find_element(self.wait, ExplorePageLocators.PORTALS_LINK)
    #
    # def literature_link(self):
    #     return find_element(self.wait, ExplorePageLocators.LITERATURE_LINK)
    #
    # def gallery_link(self):
    #     return find_element(self.wait, ExplorePageLocators.GALLERY_LINK)


