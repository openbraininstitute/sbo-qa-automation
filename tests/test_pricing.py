# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

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

        obi_top_menu = pricing_page.obi_menu()
        assert obi_top_menu.is_displayed(), "The top navigation menu is not found."
        logger.info("The top navigation menu is found.")

        obi_top_nav = pricing_page.obi_homepage_main_nav()
        assert obi_top_nav.is_displayed(), "The OBI homepage main menu is not found."
        logger.info("The OBI homepage main menu is found.")

        pricing_hero_img = pricing_page.hero_img(timeout=15)
        assert pricing_hero_img.is_displayed(), "The main hero image is not found."
        logger.info("The main hero image is found.")

        pricing_hero_video = pricing_page.hero_video(timeout=15)
        assert pricing_hero_video, "The main hero/background video is not found."
        logger.info("The main hero/background video is found.")

        page_title = pricing_page.page_title()
        assert page_title.is_displayed(), "'Discover our plans' title is not found."
        logger.info("'Discover our plans' title is found.")

        create_your_vlab_btn = pricing_page.temp_goto_vlab_btn()
        assert create_your_vlab_btn.is_displayed(), "'Create your virtual lab' button is not found."
        logger.info("'Create your virtual lab' button is found.")

        price_list_container = pricing_page.price_list_container()
        assert price_list_container.is_displayed(), "Price list container is not found."
        logger.info("Price list container is found.")

        price_list_plans = pricing_page.price_list_plans()
        assert price_list_plans, "Price list plans are not found."
        logger.info( "Price list plans are found.")

        contact_us_btn_premium_plan = pricing_page.contact_us()
        assert contact_us_btn_premium_plan.is_displayed(), "Button 'Contact us' is not found."
        logger.info("Button 'Contact us' is found.")

        container_detail_plan = pricing_page.detail_plans()
        assert container_detail_plan.is_displayed(), "Container with details of plans is not found."
        logger.info("Container with details of plans is not found.")

        page_footer = pricing_page.footer()
        assert page_footer.is_displayed(), "Page footer is not found."
        logger.info("Page footer is found.")




