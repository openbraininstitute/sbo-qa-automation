# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.common import TimeoutException

from locators.about_locators import AboutLocators
from locators.landing_locators import LandingLocators
from pages.home_page import HomePage


class AboutPage(HomePage):
    def __init__(self, browser, wait, base_url, lab_url=None, logger=None):
        super().__init__(browser, wait, base_url)
        self.home_page = HomePage(browser, wait, base_url)
        self.logger = logger
        self.base_url = base_url
        self.lab_url  = lab_url

    def go_to_page(self, retries=3, delay=5):
        about_url = f"{self.base_url}/about"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(60)
                self.browser.get(about_url)
                self.wait_for_page_ready(timeout=60)
                self.logger.info("✅ Landing Page loaded successfully.")
                return
            except TimeoutException:
                self.logger.warning(
                    f"⚠️ Landing Page load attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                self.wait.sleep(delay)
        raise TimeoutException("❌ Failed to load Landing Page after multiple attempts.")

    def about_main_title(self):
        return self.find_element(AboutLocators.ABOUT_PAGE_TITLE)

    def about_main_page_text(self):
        return self.find_element(AboutLocators.ABOUT_MAIN_TEXT)

    def get_element(self, locator):
        return self.find_element(locator)

    def find_all_page_buttons(self, timeout=10):
        return self.find_all_elements(AboutLocators.ABOUT_PAGE_BTNS, timeout=timeout)