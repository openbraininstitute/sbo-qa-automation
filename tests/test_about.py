# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import random
import re
import time
import uuid
from datetime import datetime

from selenium.common import ElementNotVisibleException
from selenium.webdriver import Keys

from locators.about_locators import AboutLocators
from pages.about_page import AboutPage
from pages.build import Build
from pages.vl_overview import VLOverview
import pytest

class TestAbout:
    def test_about(self, visit_public_pages, logger):
        _visit, base_url  = visit_public_pages
        browser, wait = _visit("/about")
        about_page = AboutPage(browser, wait, base_url, logger=logger)

        about_page.go_to_page()
        assert "About" in browser.title

        about_main_page_title = about_page.about_main_title()
        assert about_main_page_title.is_displayed(), f"The main page title is found"
        about_main_text = about_page.about_main_page_text()
        assert about_main_text.is_displayed(), f"The main page text is found"

        title_paragraphs = [
            (AboutLocators.TITLE1, AboutLocators.PARAGRAPH1),
            (AboutLocators.TITLE2, AboutLocators.PARAGRAPH2),
            (AboutLocators.TITLE3, AboutLocators.PARAGRAPH3),
            (AboutLocators.TITLE4, AboutLocators.PARAGRAPH4),
            (AboutLocators.TITLE5, AboutLocators.PARAGRAPH5),
        ]

        for title_locator, parag_locator in title_paragraphs:
            title_ele = about_page.get_element(title_locator)
            parag_ele = about_page.get_element(parag_locator)

            assert title_ele.is_displayed(), f"Title is not displayed: {title_locator}"
            assert parag_ele.text.strip(), f"Paragraph is not displayed: {parag_locator}"
            logger.info(f"Title displayed: {title_ele.text}")
            logger.info(f"Paragraph with text is displayed.")

        page_buttons = about_page.find_all_page_buttons()
        assert page_buttons, f"No page buttons found"

        for i, button in enumerate(page_buttons, start=1):
            assert button.is_displayed(), f"Button #{i} is not found."
            text = button.text
            no_space_text = re.sub(r'\s+', ' ', text).strip()
            assert text, f"❌ Button #{i} has no visible text content."
            logger.info(f"Button #{i} text: '{no_space_text}'")