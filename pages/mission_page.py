# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.common import TimeoutException, ElementNotInteractableException, NoSuchElementException
from selenium.webdriver import ActionChains
from locators.mission_locators import MissionLocators
from pages.home_page import HomePage


class MissionPage(HomePage):
    def __init__(self, browser, wait, base_url, lab_url=None, logger=None):
        super().__init__(browser, wait, base_url)
        self.home_page = HomePage(browser, wait, base_url)
        self.logger = logger
        self.base_url = base_url
        self.lab_url  = lab_url

    def go_to_page(self, retries=3, delay=5):
        about_url = f"{self.base_url}/mission"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(60)
                self.browser.get(about_url)
                self.wait_for_page_ready(timeout=60)
                self.logger.info("✅ Mission Page loaded successfully.")
                return
            except TimeoutException:
                self.logger.warning(
                    f"⚠️ Landing Page load attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                self.wait.sleep(delay)
        raise TimeoutException("❌ Failed to load Landing Page after multiple attempts.")


    def mission_main_title(self):
        return self.find_element(MissionLocators.MISSION_PAGE_TITLE)

    def mission_main_page_text(self):
        return self.find_element(MissionLocators.MISSION_MAIN_TEXT)

    def main_page_paragraph(self):
        return self.find_element(MissionLocators.MAIN_PAGE_PARAGRAPH)

    def minor_page_paragraph(self):
        return self.find_element(MissionLocators.MINOR_PAGE_PARAGRAPH)


    def platform_sections(self):
        return self.find_element(MissionLocators.PLATFORM_SECTIONS)

    def page_titles(self):
        return self.find_all_elements(MissionLocators.MAIN_TITLES)

    def section_titles(self):
        return self.find_all_elements(MissionLocators.P_SECTION_TITLES)

    def section_texts(self):
        return self.find_all_elements(MissionLocators.P_SECTION_TEXTS)

    def section_images(self):
        return self.find_all_elements(MissionLocators.P_SECTION_IMAGES)


    def hover_over_button(self):
        button_element = self.browser.find_element(MissionLocators.VLAB_CARDS_BTN)
        ActionChains(self.browser).move_to_element(button_element).perform()

    def is_video_playing(self):
        video_element = self.browser.find_element(MissionLocators.VIDEO1)
        return self.browser.execute_script(
            "return arguments[0].readyState >= 3 && !arguments[0].paused;",
            video_element
        )

    def button_download_mission(self):
        return self.find_element(MissionLocators.BTN_DOWNLOAD_MISSION)

    def new_tab_pdf(self):
        return self.find_element(MissionLocators.PDF_NEW_TAB)

    def subscribe_newsletter_title(self):
        return self.find_element(MissionLocators.SUBSCRIBE_NEWSLETTER)

