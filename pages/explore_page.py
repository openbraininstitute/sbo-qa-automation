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
        # self.browser.get(self.base_url)
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

    def find_experimental_data_titles(self, exp_data_title):
        exp_data_title = []
        for title in exp_data_title:
            exp_data_title.extend(self.find_all_elements(title))
        return exp_data_title






