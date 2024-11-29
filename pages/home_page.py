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

    def find_login_button(self):
        return self.find_element(HomePageLocators.LOGIN_BUTTON)

    def find_about_btn(self):
        return self.find_element(HomePageLocators.ABOUT)

    def find_big_title1(self):
        return self.find_element(HomePageLocators.BIG_TITLE1)

    def find_big_title2(self):
        return self.find_element(HomePageLocators.BIG_TITLE2)

    def find_bbop_logo1(self):
        return self.find_element(HomePageLocators.BBOP1)

    def find_bbop_logo2(self):
        return self.find_element(HomePageLocators.BBOP2)

    def find_bbp1(self):
        return self.find_element(HomePageLocators.BBP1)

    def find_bbp2(self):
        return self.find_element(HomePageLocators.BBP2)

    def find_doc1(self):
        return self.find_element(HomePageLocators.DOC1)

    def find_doc2(self):
        return self.find_element(HomePageLocators.DOC2)

    def find_doc3(self):
        return self.find_element(HomePageLocators.DOC3)

    def find_doc4(self):
        return self.find_element(HomePageLocators.DOC4)

    def find_contributor_table(self):
        return self.find_element(HomePageLocators.CONTRIBUTOR_TABLE)

    def find_contributor(self):
        return self.find_element(HomePageLocators.CONTRIBUTOR)

    def find_github_btn(self):
        return self.find_element(HomePageLocators.BB_GITHUB_BTN)

    def find_main_title(self):
        return self.find_element(HomePageLocators.MAIN_TITLE)




    # def scrape_links(self):
    #     page_source = self.browser.page_source
    #     links = self.url_scraper.scrape_links(page_source)
