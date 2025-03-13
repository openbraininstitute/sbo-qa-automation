# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import pytest
from pages.landing_page import LandingPage


@pytest.mark.usefixtures("setup", "logger")
class TestLanding:
    @pytest.mark.run(order=1)
    def test_landingpage(self, setup, logger):
        """Verifies that the landing page loads correctly."""
        browser, wait, base_url = setup
        landing_page = LandingPage(browser, wait, base_url, logger)

        # Go to the landing page
        landing_page.go_to_landing_page()
        assert landing_page.is_landing_page_displayed(), "Landing Page did not load correctly."
        logger.info("✅ Landing Page loaded successfully.")

        title_accelerate = landing_page.find_title_accelerate()
        assert title_accelerate.is_displayed(), "Accelerate title is missing"
        logger.info("Title Accelerate is displayed")
        title_reconstruct = landing_page.find_title_reconstruct()
        assert title_reconstruct.is_displayed(), "Reconstruct title is missing"
        logger.info("Title Reconstruct is displayed")
        title_who = landing_page.find_title_who()
        assert title_who.is_displayed(), "Who we are title is missing"
        logger.info("Title 'Who we are' is displayed")
        title_news = landing_page.find_title_who()
        assert title_news.is_displayed(), "News title is missing"
        logger.info("Title News is displayed")

        p_text1 = landing_page.find_p_text1()
        ptext1_text = p_text1.get_attribute("textContent").strip()
        logger.info(f"Paragraph content: '{ptext1_text}'")
        assert ptext1_text != "", "Paragraph text is empty!"

