# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import random
import re
import time
import uuid
from datetime import datetime

from selenium.common import ElementNotVisibleException, NoSuchElementException
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
        errors = []

        for i, button in enumerate(page_buttons, start=1):
            text = re.sub(r'\s+', ' ', button.text).strip()
            is_visible = button.is_displayed()
            href = button.get_attribute("href")

            if not is_visible or not text or not href:
                errors.append(
                    f"Button #{i} - Visible: {is_visible}, Text: '{text}', Href: '{href}'"
                )

        assert not errors, f"❌ Some buttons failed checks:\n" + "\n".join(errors)

        portals_cards = about_page.find_portals_cards()
        assert portals_cards, f"Portal cards are not found"
        portal_cards_errors = []

        for i, card in enumerate(portals_cards, start=1):
            info = about_page.extract_card_info(card)
            if not info["visible"] or not info["title"] or not info["href"]:
                portal_cards_errors.append(f"Card #{i} failed - {info}")
                print(f"Card #{i} failed - Title: {info['title']}, Href: {info['href']}, Visible: {info['visible']}")

        assert not portal_cards_errors, f"❌ Some cards failed:\n" + "\n".join(portal_cards_errors)
