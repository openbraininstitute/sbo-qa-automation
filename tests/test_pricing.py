# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import re
import time

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from locators.about_locators import AboutLocators
from pages.about_page import AboutPage
from pages.pricing_page import PricingPage


class TestPricing:
    def test_pricing(self, visit_public_pages, logger):
        _visit, base_url  = visit_public_pages
        browser, wait = _visit("/pricing")
        pricing_page = PricingPage(browser, wait, base_url, logger=logger)

        pricing_page.go_to_page()

        obi_homepage_logo = pricing_page.obi_homepage_logo()
        assert obi_homepage_logo, "The OBI Homepage Logo is not found."
        logger.info("The OBI Homepage Logo is found")

        pricing_page_title = pricing_page.pricing_main_title()
        assert pricing_page_title.is_displayed(), "Pricing main page title is not found."
        logger.info("Pricing main page title is found.")