# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.common import TimeoutException
from locators.landing_locators import LandingLocators
from pages.home_page import HomePage
from util.util_links_checker import LinkChecker


class LandingPage(HomePage, LinkChecker):
    def __init__(self, browser, wait, base_url, logger):
        super().__init__(browser, wait, base_url)
        self.home_page = HomePage(browser, wait, base_url)
        self.logger = logger


    def go_to_landing_page(self, retries=3, delay=5):
        """Navigates to the OBI landing page and ensures it loads properly."""
        landing_url = "https://staging.openbraininstitute.org/"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(60)
                self.browser.get(landing_url)
                self.wait_for_page_ready(timeout=60)
                self.logger.info("✅ Landing Page loaded successfully.")
                return
            except TimeoutException:
                self.logger.warning(
                    f"⚠️ Landing Page load attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                self.wait.sleep(delay)
        raise TimeoutException("❌ Failed to load Landing Page after multiple attempts.")

    def is_landing_page_displayed(self):
        try:
            expected_title = "Open Brain Platform"
            return expected_title in self.browser.title
        except TimeoutException as e:
            self.logger.warning(f"Error loading OBI Landing Page")
            return False

    def go_to_lab(self):
        return self.find_element(LandingLocators.GOTO_LAB)

    def click_go_to_lab(self):
        try:
            go_to_lab = self.find_element(LandingLocators.GOTO_LAB)
            go_to_lab.click()
            self.logger.info("✅ Clicked 'Go to Lab' button.")
        except Exception as e:
            self.logger.error(f"❌ Failed to click 'Go to Lab' button: {e}")
            raise

    def find_banner_title(self):
        return self.find_element(LandingLocators.BANNER_TITLE)

    def find_title_accelerate(self):
        return self.find_element(LandingLocators.TITLE_ACCELERATE)

    def find_title_reconstruct(self):
        return self.find_element(LandingLocators.TITLE_RECONSTRUCT)

    def find_title_who(self):
        return self.find_element(LandingLocators.TITLE_WHO)

    def find_title_news(self):
        return self.find_element(LandingLocators.TITLE_NEWS)

    def find_p_text1(self):
        return self.find_element(LandingLocators.P_TEXT1)

    def find_p_text2(self):
        return self.find_element(LandingLocators.P_TEXT2)

    def find_p_text3(self):
        return self.find_element(LandingLocators.P_TEXT3)

    def find_p_text4(self):
        return self.find_element(LandingLocators.P_TEXT4)

