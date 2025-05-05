# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from pages.news_page import NewsPage


class TestAbout:
    def test_about(self, visit_public_pages, logger):
        _visit, base_url = visit_public_pages
        browser, wait = _visit("/news")
        news_page = NewsPage(browser, wait, base_url, logger=logger)