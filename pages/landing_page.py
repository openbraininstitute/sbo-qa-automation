# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.common import TimeoutException
from locators.landing_locators import LandingLocators
from pages.home_page import HomePage
from util.util_links_checker import LinkChecker


class LandingPage(HomePage):
    def __init__(self, browser, wait, base_url, logger):
        super().__init__(browser, wait, logger)
        self.browser = browser
        self.wait = wait
        self.logger = logger
        self.base_url = base_url

    def go_to_landing_page(self):
        self.browser.get(self.base_url)
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    def is_landing_page_displayed(self):
        try:
            expected_title = "Open Brain Platform"
            return expected_title in self.browser.title
        except TimeoutException as e:
            self.logger.warning(f"Error loading OBI Landing Page")
            return False

    def go_to_lab(self, timeout=10):
        return self.find_element(LandingLocators.GOTO_LAB, timeout=timeout)

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

    def find_paragraph_text(self):
        return self.find_all_elements(LandingLocators.PARA_TEXT)

    def find_big_img1(self):
        return self.find_element(LandingLocators.BIG_IMG1)

    def find_big_img2(self):
        return self.find_element(LandingLocators.BIG_IMG2)

    def find_big_img3(self):
        return self.find_element(LandingLocators.BIG_IMG3)

    def find_section_btn1(self):
        return self.find_element(LandingLocators.SECTION_BTN1)

    def find_section_btn2(self):
        return self.find_element(LandingLocators.SECTION_BTN2)

    def find_section_btn3(self):
        return self.find_element(LandingLocators.SECTION_BTN3)

    def find_section_btn4(self):
        return self.find_element(LandingLocators.SECTION_BTN4)

    def find_section_btn5(self):
        return self.find_element(LandingLocators.SECTION_BTN5)

    def find_horizontal_cards_section1(self):
        return self.find_element(LandingLocators.HORIZONTAL_CARDS_SECTION1)

    def find_horizontal_cards_section2(self):
        return self.find_element(LandingLocators.HORIZONTAL_CARDS_SECTION2)

    def find_news_content1(self):
        return self.find_element(LandingLocators.NEWS_CARD_CONTENT1)

    def find_news_content2(self):
        return self.find_element(LandingLocators.NEWS_CARD_CONTENT2)

    def find_news_content3(self):
        return self.find_element(LandingLocators.NEWS_CARD_CONTENT3)

    def find_news_content4(self):
        return self.find_element(LandingLocators.NEWS_CARD_CONTENT4)

    def find_news_card_pic1(self):
        return self.find_element(LandingLocators.NEWS_CARD_PIC1)

    def find_news_card_pic2(self):
        return self.find_element(LandingLocators.NEWS_CARD_PIC2)

    def find_news_card_pic3(self):
        return self.find_element(LandingLocators.NEWS_CARD_PIC3)

    def find_news_card_pic4(self):
        return self.find_element(LandingLocators.NEWS_CARD_PIC4)

    def find_top_menu(self):
        return self.find_element(LandingLocators.TOP_MENU)

    def find_top_about(self):
        return self.find_element(LandingLocators.TOP_ABOUT)

    def find_top_mission(self):
        return self.find_element(LandingLocators.TOP_MISSION)

    def find_top_news(self):
        return self.find_element(LandingLocators.TOP_NEWS)

    def find_top_pricing(self):
        return self.find_element(LandingLocators.TOP_PRICING)

    def find_top_team(self):
        return self.find_element(LandingLocators.TOP_TEAM)

    def find_top_resources(self):
        return self.find_element(LandingLocators.TOP_RESOURCES)

    def find_top_contact(self):
        return self.find_element(LandingLocators.TOP_CONTACT)

    def find_menu_logo(self):
        return self.find_element(LandingLocators.TOP_MENU_LOGO)