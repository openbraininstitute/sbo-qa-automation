# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time

from pages.pricing_page import PricingPage


class TestPricing:
    def test_pricing(self, visit_public_pages, logger):
        _visit, base_url = visit_public_pages
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

        discover_plans_btn = pricing_page.discover_plans_button()
        assert discover_plans_btn.is_displayed(), "'Discover our plans' button is not found."
        logger.info("'Discover our plans' button is found.")

        # Scroll to plans section and widen viewport for xl:grid visibility
        pricing_page.scroll_to_plans()

        # Verify plan cards container and all 4 plans
        plan_cards_container = pricing_page.plan_cards_container()
        assert plan_cards_container.is_displayed(), "Plan cards container is not found."
        logger.info("Plan cards container is found.")

        plan_cards = pricing_page.plan_cards()
        assert len(plan_cards) == 4, f"Expected 4 plan cards, found {len(plan_cards)}"
        logger.info(f"Found {len(plan_cards)} plan cards.")

        free_plan = pricing_page.plan_card_free()
        assert free_plan.is_displayed(), "Free plan card is not found."
        logger.info("Free plan card is found.")

        pro_plan = pricing_page.plan_card_pro()
        assert pro_plan.is_displayed(), "Pro plan card is not found."
        logger.info("Pro plan card is found.")

        enterprise_plan = pricing_page.plan_card_enterprise()
        assert enterprise_plan.is_displayed(), "Enterprise plan card is not found."
        logger.info("Enterprise plan card is found.")

        education_plan = pricing_page.plan_card_education()
        assert education_plan.is_displayed(), "Education plan card is not found."
        logger.info("Education plan card is found.")

        # Verify Contact Us links on Enterprise and Education
        contact_us_enterprise = pricing_page.contact_us_enterprise()
        assert contact_us_enterprise.is_displayed(), "Enterprise 'Contact Us' link is not found."
        logger.info("Enterprise 'Contact Us' link is found.")

        contact_us_education = pricing_page.contact_us_education()
        assert contact_us_education.is_displayed(), "Education 'Contact Us' link is not found."
        logger.info("Education 'Contact Us' link is found.")

        # Verify Pro plan price
        pro_price = pricing_page.pro_price()
        assert pro_price.is_displayed(), "Pro plan price is not found."
        assert "CHF" in pro_price.text, f"Expected CHF in price, got: {pro_price.text}"
        logger.info(f"Pro plan price found: {pro_price.text}")

        page_footer = pricing_page.footer()
        assert page_footer.is_displayed(), "Page footer is not found."
        logger.info("Page footer is found.")
