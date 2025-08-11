# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
from selenium.common import TimeoutException

from locators.pricing_locators import PricingLocators
from pages.home_page import HomePage


class PricingPage(HomePage):
    def __init__(self, browser, wait, base_url, lab_url=None, logger=None):
        super().__init__(browser, wait, base_url)
        self.home_page = HomePage(browser, wait, base_url)
        self.logger = logger
        self.base_url = base_url
        self.lab_url  = lab_url


    def go_to_page(self, retries=3, delay=5):
        pricing_url = f"{self.base_url}/pricing"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(60)
                self.browser.get(pricing_url)
                self.wait_for_page_ready(timeout=60)
                self.logger.info("✅ About Page loaded successfully.")
                return
            except TimeoutException:
                self.logger.warning(
                    f"⚠️ Landing Page load attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                self.wait.sleep(delay)
        raise TimeoutException("❌ Failed to load Landing Page after multiple attempts.")

    def obi_homepage_logo(self):
        return self.is_visible(PricingLocators.OBI_HOMEPAGE_LOGO_BTN)


    def obi_menu(self):
        return self.element_visibility(PricingLocators.OBI_MENU)

    def obi_homepage_main_nav(self):
        return self.element_visibility(PricingLocators.OBI_HOMEPAGE_MAIN_NAV)

    def pricing_main_title(self, timeout=10):
        return self.element_visibility(PricingLocators.PRICING_TITLE, timeout=timeout)

    def hero_img(self, timeout=15):
        return self.element_visibility(PricingLocators.HERO_IMG, timeout=timeout)

    def hero_video(self, timeout=20):
        return self.element_visibility(PricingLocators.HERO_VIDEO, timeout=timeout)