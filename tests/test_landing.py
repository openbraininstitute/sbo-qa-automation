# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import pytest
from pages.landing_page import LandingPage

@pytest.mark.no_auto_nav
@pytest.mark.usefixtures("setup", "logger")
class TestLanding:
    @pytest.mark.run(order=1)
    def test_landingpage(self, setup, logger, test_config):
        """Verifies that the landing page."""
        browser, wait, base_url, lab_id, project_id = setup
        landing_page = LandingPage(browser, wait, base_url, test_config["landing_url"], logger)

        landing_page.go_to_landing_page()
        # time.sleep(10)
        assert landing_page.is_landing_page_displayed(), "Landing Page did not load correctly."
        logger.info("✅ Landing Page loaded successfully.")

        title_accelerate = landing_page.find_title_accelerate()
        assert title_accelerate.is_displayed(), "Accelerate title is missing"
        logger.info("Title Accelerate is displayed")

        # title_reconstruct = landing_page.find_title_reconstruct()
        # assert title_reconstruct.is_displayed(), "Reconstruct title is missing"
        # logger.info("Title Reconstruct is displayed")

        title_who = landing_page.find_title_who()
        assert title_who.is_displayed(), "Who we are title is missing"
        logger.info("Title 'Who we are' is displayed")

        title_news = landing_page.find_title_who()
        assert title_news.is_displayed(), "News title is missing"
        logger.info("Title News is displayed")

        p_text1 = landing_page.find_p_text1()
        ptext1_text = p_text1.get_attribute("textContent").strip()
        # logger.info(f"Paragraph content: '{ptext1_text}'")
        assert ptext1_text != "", "Paragraph text is empty!"

        para_text = landing_page.find_paragraph_text()
        assert len(para_text) == 6, f"Expected 6 text paragraphs, found {len(para_text)}"
        for idx, para in enumerate(para_text, start=1):
            text = para.text.strip()
            assert text, f"Paragraph text {idx} is empty"

        big_img1 = landing_page.find_big_img1()
        assert big_img1.is_displayed(), "Section 1 big image is not found"
        logger.info("Accelerating neuroscience research section img is found")
        big_img2 = landing_page.find_big_img2()
        assert big_img2.is_displayed(), "Section 2 big image is not found"
        logger.info("Who is behind OBI img section is found")
        big_img3 = landing_page.find_big_img3()
        assert big_img3.is_displayed(), "Section 3 big image is not found"
        logger.info("How can we collaborate and help you achieve greatness img is found")

        section_btn1 = landing_page.find_section_btn1()
        assert section_btn1.is_displayed(), "Section 1 button is not displayed"
        logger.info("'Discover our mission' button is found")

        section_btn2 = landing_page.find_section_btn2()
        assert section_btn2.is_displayed(), "Section 2 button is not displayed"
        logger.info("'More about us' button is found")

        section_btn3 = landing_page.find_section_btn3()
        assert section_btn3.is_displayed(), "Section 3 button is not displayed"
        logger.info("'Discover our team' button is found")

        section_btn4 = landing_page.find_section_btn4()
        assert section_btn4.is_displayed(), "Section 4 button is not displayed"
        logger.info("'Contact us' button is found")

        section_btn5 = landing_page.find_section_btn5()
        assert section_btn5.is_displayed(), "Section 5 button is not displayed"
        logger.info("'Discover story in detail' button is found")

        gotolab = landing_page.go_to_lab()
        assert gotolab.is_displayed(), "Unable to find 'Go to Lab' button"
        gotolab.click()
        try:
            landing_page.wait_for_url_contains("openid-connect", timeout=30)
            redirected = (
                    "openid-connect" in landing_page.browser.current_url or
                    "auth" in landing_page.browser.current_url
            )
            assert redirected, (
                f"Expected to redirect to the login page, "
                f"got: {landing_page.browser.current_url}"
            )
            logger.info(f"Redirected to the login page:  {landing_page.browser.current_url}")
        except Exception as e:
            logger.error(f"Failed during login redirection: {e}")
            raise

