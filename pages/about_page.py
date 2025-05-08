# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from locators.about_locators import AboutLocators
from pages.home_page import HomePage
from selenium.webdriver.support import expected_conditions as EC



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
                self.logger.info("✅ About Page loaded successfully.")
                return
            except TimeoutException:
                self.logger.warning(
                    f"⚠️ Landing Page load attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                self.wait.sleep(delay)
        raise TimeoutException("❌ Failed to load Landing Page after multiple attempts.")

    def main_hero_video(self):
        return self.find_element(AboutLocators.MAIN_HERO_VIDEO)

    def main_title(self):
        return self.find_element(AboutLocators.ABOUT_PAGE_TITLE)

    def main_page_text(self):
        return self.find_element(AboutLocators.ABOUT_MAIN_TEXT)

    def get_element(self, locator):
        return self.find_element(locator)

    def find_all_page_buttons(self, timeout=10):
        return self.find_all_elements(AboutLocators.ABOUT_PAGE_BTNS, timeout=timeout)

    def find_portals_cards(self, timeout=10):
        return self.find_all_elements(AboutLocators.ABOUT_PORTALS_CARDS, timeout=timeout)

    def extract_card_info(self, card_element):

        try:
            title = card_element.find_element(*AboutLocators.PORTALS_TITLES).text.strip()
            print(f"Extracted title: '{title}'")
        except NoSuchElementException:
            title = ""

        try:
            content_divs = card_element.find_elements(By.XPATH, ".//div[contains(@class, "
                                                                    "'PortalCard_content')]/div")
            description = content_divs[-1].text.strip() if len(content_divs) >= 2 else ""
            print(f"Extracted title: '{description}'")
        except NoSuchElementException:
            description = ""

        href = card_element.get_attribute("href")
        visible = card_element.is_displayed()

        return {
            "title": title,
            "description": description,
            "href": href,
            "visible": visible
        }

    def find_contributor_panel(self):
        return self.find_element(AboutLocators.CONTRIBUTORS_PANEL)

    def find_contributors_list(self):
        return self.find_element(AboutLocators.CONTRIBUTORS_LIST)

    def find_contributors_name(self):
        return self.find_all_elements(AboutLocators.CONTRIBUTORS_NAME)

    def click_b_btn(self, timeout=20):
        return self.wait_and_click(AboutLocators.B_BTN, timeout=timeout)

    def find_load_more_column(self, timeout=10):
        return self.find_element(AboutLocators.LOAD_MORE_COLUMN, timeout=timeout)

    def find_load_more_btn(self, timeout=20):
        return self.wait_and_click(AboutLocators.LOAD_MORE_BTN, timeout=timeout)

    def find_all_social_images(self):
        return self.find_all_elements(AboutLocators.IMG_VIGNETTE)

    def get_image(self, locator):
        return self.find_element(locator)

    def wait_for_image_to_load(self, img_element, timeout=10):
        WebDriverWait(self.browser, timeout).until(
            lambda d: d.execute_script(
                "return arguments[0].complete && arguments[0].naturalWidth > 0;", img_element
            )
        )
