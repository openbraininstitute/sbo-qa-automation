# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

from locators.home_page_locators import HomePageLocators
from util.util_links_checker import LinkChecker
from .base_page import CustomBasePage
from util.util_scraper import UrlScraper


class HomePage(CustomBasePage, LinkChecker):

    def __init__(self, browser, wait):
        super().__init__(browser, wait)
        self.url_scraper = UrlScraper()

    def go_to_home_page(self):
        self.go_to_page("")

    # def scrape_links(self):
    #     page_source = self.browser.page_source
    #     links = self.url_scraper.scrape_links(page_source)
    #
    # def find_explore_title(self):
    #     return self.find_element(HomePageLocators.EXPLORE_TITLE)
    #
    # def find_build_title(self):
    #     return self.find_element(HomePageLocators.BUILD_TITLE)
    #
    # def find_simulate_title(self):
    #     return self.find_element(HomePageLocators.SIMULATE_TITLE)
    #
    def find_login_button(self):
        return self.find_element(HomePageLocators.LOGIN_BUTTON)

    def find_github_btn(self):
        return self.find_element(HomePageLocators.GITHUB_BTN)
