# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from locators.home_page_locators import HomePageLocators
from util.util_links_checker import LinkChecker
from .base_page import CustomBasePage
from util.util_scraper import UrlScraper


class HomePage(CustomBasePage):

    def __init__(self, browser, wait, base_url):
        super().__init__(browser, wait, base_url)

    def go_to_home_page(self):
        self.go_to_page("")

