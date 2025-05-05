# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from locators.news_locators import NewsLocators
from pages.home_page import HomePage
from selenium.webdriver.support import expected_conditions as EC



class NewsPage(HomePage):
    def __init__(self, browser, wait, base_url, lab_url=None, logger=None):
        super().__init__(browser, wait, base_url)
        self.home_page = HomePage(browser, wait, base_url)
        self.logger = logger
        self.base_url = base_url
        self.lab_url  = lab_url

    def go_to_page(self, retries=3, delay=5):
        about_url = f"{self.base_url}/news"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(60)
                self.browser.get(about_url)
                self.wait_for_page_ready(timeout=60)
                self.logger.info("✅ News Page loaded successfully.")
                return
            except TimeoutException:
                self.logger.warning(
                    f"⚠️ Landing Page load attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                self.wait.sleep(delay)
        raise TimeoutException("❌ Failed to load Landing Page after multiple attempts.")

    def main_hero_video(self,timeout=10):
        return self.element_visibility(NewsLocators.HERO_VIDEO, timeout=timeout)


    def hero_img(self):
        return self.find_element(NewsLocators.HERO_IMG)

    def main_title(self):
        return self.find_element(NewsLocators.HERO_MAIN_TITLE)

    def main_page_text(self):
        return self.find_element(NewsLocators.HERO_TEXT)

    def page_cards(self):
        return self.find_all_elements(NewsLocators.PAGE_CARDS)

    def cards_main_titles(self):
        return self.find_all_elements(NewsLocators.CARD_MAIN_TITLE)

    def cards_text(self):
        return self.find_all_elements(NewsLocators.CARD_TEXT)

    def cards_img(self):
        return self.find_all_elements(NewsLocators.CARD_IMG)

    def cards_read_more_btn(self):
        return self.find_all_elements(NewsLocators.CARD_READ_MORE_BTN)

    def load_more_btn(self):
        return self.find_element(NewsLocators.LOAD_MORE_BTN)