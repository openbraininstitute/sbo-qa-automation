# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import pytest

from locators.landing_locators import LandingLocators
from pages.landing_page import LandingPage
from selenium.webdriver.common.action_chains import ActionChains

@pytest.mark.no_auto_nav
@pytest.mark.usefixtures("visit_public_pages")
class TestLanding:
    @pytest.mark.run(order=1)
    def test_landingpage(self, setup, logger, visit_public_pages):
        """Verifies that the landing page."""

        _visit, base_url = visit_public_pages
        browser, wait = _visit("")
        landing_page = LandingPage(browser, wait, logger, base_url)
        logger.info("✅ Landing Page loaded successfully.")

        background_page_image = landing_page.hero_background_img(timeout=15)
        assert background_page_image.is_displayed(), "The main page image is not found."
        logger.info("The main page image is found.")

        background_page_video = landing_page.hero_background_video(timeout=15)
        assert background_page_video.is_displayed(), "The page background video is not displayed"
        logger.info("The main background video is displayed.")

        banner_title = landing_page.find_banner_title()
        assert banner_title.is_displayed(), "Page main banner title is not found"
        logger.info("Landing Page main banner title is found.")

        title_accelerate = landing_page.find_title_accelerate()
        assert title_accelerate.is_displayed(), "Accelerate title is missing"
        logger.info("Title Accelerate is displayed")

        title_reconstruct = landing_page.find_title_dig_brain()
        assert title_reconstruct.is_displayed(), "Reconstruct title is missing"
        logger.info("Title Reconstruct is displayed")

        title_who = landing_page.find_title_who()
        assert title_who.is_displayed(), "Who we are title is missing"
        logger.info("Title 'Who we are' is displayed")

        title_news = landing_page.find_title_who()
        assert title_news.is_displayed(), "News title is missing"
        logger.info("Title News is displayed")

        para_text = landing_page.find_paragraph_text()
        assert len(para_text) == 6, f"Expected 6 text paragraphs, found {len(para_text)}"

        for idx, para in enumerate(para_text, start=1):
            text = para.text.strip()
            assert text, f"Paragraph text {idx} is empty!"
            logger.info(f"Paragraph {idx}: '{text}'")

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

        digital_brains_video = landing_page.digital_brains_video()
        assert digital_brains_video, "The digital brains video is not found (line 107)"
        logger.info("The digital brains video is displayed")

        video_title = landing_page.video_title1(timeout=15)
        assert video_title.is_displayed(), "The video title is not displayed."
        logger.info("Looking for video title 1")

        video_container = landing_page.browser.find_element(*LandingLocators.VIDEO_CONTAINER)
        landing_page.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", video_container)
        time.sleep(2)  # Let layout settle

        video_play_btn = landing_page.digital_brains_play_btn(timeout=10)
        logger.info("looking for play button")
        video_play_btn.click()
        logger.info("Clicked on play btn")

        logger.info("Video play button is clicked")
        landing_page.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", video_container)
        actions = ActionChains(landing_page.browser)
        actions.move_to_element(video_container).perform()

        digital_brains_steps = landing_page.digital_brains_steps()
        assert digital_brains_steps, "No digital brains video steps found!"
        assert len(digital_brains_steps) == 5, f"Expected 5 steps, found {len(digital_brains_steps)}"

        for idx, step in enumerate(digital_brains_steps, start=1):
            text = step.text.strip()
            logger.info(f"Step {idx} text: '{text}'")
            assert text != "", f"Step {idx} text is empty!"

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



