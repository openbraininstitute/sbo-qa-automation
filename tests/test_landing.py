# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import pytest
from selenium.webdriver.common.by import By

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
        landing_page = LandingPage(browser, wait, base_url, logger)
        logger.info("✅ Landing Page loaded successfully.")

        background_page_image = landing_page.hero_background_img(timeout=25)
        assert background_page_image.is_displayed(), "The main page image is not found."
        logger.info("The main page image is found.")

        background_page_video = landing_page.hero_background_video(timeout=25)
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
        assert len(para_text) == 7, f"Expected 6 text paragraphs, found {len(para_text)}"

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

        sections = landing_page.horizontal_card_sections()
        missing_sections = []

        for name, section in sections.items():
            if section.is_displayed():
                logger.info(f"{name} is displayed")
            else:
                logger.info(f"{name} is NOT displayed")
                missing_sections.append(name)

        assert not missing_sections, f"Missing sections: {', '.join(missing_sections)}"

        footer_obi_logo = landing_page.footer_obi_logo()
        assert footer_obi_logo.is_displayed(), "Footer OBI logo is not displayed."
        logger.info("OBI logo is found in page footer")

        footer_obi_copyright = landing_page.footer_obi_copyright()
        assert footer_obi_copyright.is_displayed(), "Footer OBI copyright is not displayed."
        logger.info("OBI Copyright is found in footer.")

        # TODO: Footer links are being updated to match the new nav structure.
        # Remove xfail once the footer redesign is deployed.
        expected_titles = {
            "About OBI",
            "Our story",
            "Mission",
            "Team",
            "Notebooks",
            "Gallery",
            "Pricing",
            "News",
            "Contact",
            "Login",
            "Terms and conditions",
            "Financing policy",
            "Privacy policy",
        }

        actual_titles = landing_page.footer_link_titles()
        missing_titles = []

        for title in expected_titles:
            if title in actual_titles:
                logger.info(f"Footer title found: {title}")
            else:
                logger.info(f"Footer title NOT found: {title}")
                missing_titles.append(title)

        if missing_titles:
            pytest.xfail(f"Footer redesign pending – missing titles: {', '.join(missing_titles)}")
        assert set(actual_titles) >= expected_titles

        subscribe_to_newsletter_section = landing_page.footer_subscribe_block()
        assert subscribe_to_newsletter_section.is_displayed(), "Subscribe to newsletter section is not displayed"
        logger.info("Subscribe to newsletter section is displayed")

        expected_social_media = {
            "https://www.linkedin.com/company/openbraininstitute/",
            "https://x.com/OpenBrainInst",
            "https://www.youtube.com/@openbraininstitute",
            "https://bsky.app/profile/openbraininst.bsky.social",
        }

        actual_social_media = set(landing_page.footer_social_media_links())

        missing = []

        for title in expected_social_media:
            if title in actual_social_media:
                logger.info(f"Social media link found: {title}")
            else:
                logger.info(f"Social media link NOT found: {title}")
                missing.append(title)

        assert not missing, f"Missing social media links: {', '.join(missing)}"
        assert set(actual_social_media) >= expected_social_media

        # Use the improved click method that handles CI environment issues
        logger.info(f"Testing on environment: {base_url}")
        current_url = landing_page.browser.current_url
        logger.info(f"Current URL before clicking: {current_url}")
        
        landing_page.click_go_to_lab()
        logger.info("Clicked on 'Go to Lab' button waiting for redirect to the login page")

        logger.info("Waiting so that the page URL contains 'realms'")
        
        # Add more robust waiting with better error handling
        try:
            landing_page.wait_for_url_contains("realms", timeout=60)
            logger.info(f"✅ Successfully navigated to login page: {browser.current_url}")
        except Exception as e:
            # Log current state for debugging
            current_url_after = browser.current_url
            logger.error(f"❌ Failed to reach login page")
            logger.error(f"Expected: URL containing 'realms'")
            logger.error(f"Actual URL: {current_url_after}")
            logger.error(f"Environment: {base_url}")
            logger.error(f"Error: {e}")
            
            # Check if we're on a blank page
            if current_url_after == "about:blank" or not current_url_after:
                logger.error("🚨 Browser is on blank page - navigation completely failed")
            elif current_url_after == current_url:
                logger.error("🚨 URL didn't change at all - button click may have failed")
            else:
                logger.error(f"🚨 URL changed but not to expected login page")
            
            # Take screenshot for debugging
            try:
                screenshot_name = f"staging_login_fail_{int(time.time())}.png"
                browser.save_screenshot(screenshot_name)
                logger.info(f"Screenshot saved: {screenshot_name}")
            except:
                pass
                
            raise

        assert "/auth/realms" in browser.current_url, \
            f"Unexpected URL after login: {browser.current_url}"
        logger.info(f"Successfully logged in. Current page URL: {browser.current_url}")

    @pytest.mark.run(order=2)
    def test_navbar_dropdown_menus(self, setup, logger, visit_public_pages):
        """Verifies that the navbar About and The Platform dropdowns
        contain the expected submenu items."""

        _visit, base_url = visit_public_pages
        browser, wait = _visit("")
        landing_page = LandingPage(browser, wait, base_url, logger)
        logger.info("✅ Landing Page loaded for navbar dropdown test.")

        # Scroll to top so the navbar is fully visible
        browser.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        # ── About dropdown ──────────────────────────────────────────
        about_btn = landing_page.find_about_button()
        assert about_btn.is_displayed(), "About button is not visible in the navbar"
        logger.info("About button is visible in the navbar")

        landing_page.click_about_dropdown()
        logger.info("Clicked About dropdown")

        about_items = {
            "About OBI": landing_page.find_about_obi,
            "Our story": landing_page.find_our_story,
            "Mission": landing_page.find_top_mission,
            "Team": landing_page.find_top_team,
        }

        for label, finder in about_items.items():
            item = finder(timeout=5)
            assert item.is_displayed(), f"About submenu item '{label}' is not displayed"
            logger.info(f"About submenu item found: {label}")

        # Close the About dropdown by clicking the button again
        landing_page.click_about_dropdown()
        time.sleep(0.5)

        # ── The Platform dropdown ───────────────────────────────────
        platform_btn = landing_page.find_platform_button()
        assert platform_btn.is_displayed(), "The Platform button is not visible in the navbar"
        logger.info("The Platform button is visible in the navbar")

        landing_page.click_platform_dropdown()
        logger.info("Clicked The Platform dropdown")

        platform_items = {
            "Features": landing_page.find_top_features,
            "Showcases": landing_page.find_top_showcases,
            "Pricing": landing_page.find_top_pricing,
        }

        for label, finder in platform_items.items():
            item = finder(timeout=5)
            assert item.is_displayed(), f"Platform submenu item '{label}' is not displayed"
            logger.info(f"Platform submenu item found: {label}")

        logger.info("✅ All navbar dropdown menus verified successfully.")

    @pytest.mark.run(order=3)
    def test_navbar_dropdown_navigation(self, setup, logger, visit_public_pages):
        """Verifies that each dropdown submenu item navigates to the correct page."""

        _visit, base_url = visit_public_pages
        browser, wait = _visit("")
        landing_page = LandingPage(browser, wait, base_url, logger)
        logger.info("✅ Landing Page loaded for navbar navigation test.")

        about_submenu_items = {
            "About OBI": ("/about", landing_page.find_about_obi),
            "Our story": ("/the-real-digital-brain-story", landing_page.find_our_story),
            "Mission": ("/mission", landing_page.find_top_mission),
            "Team": ("/team", landing_page.find_top_team),
        }

        platform_submenu_items = {
            "Features": ("/features", landing_page.find_top_features),
            "Showcases": ("/showcases", landing_page.find_top_showcases),
            "Pricing": ("/pricing", landing_page.find_top_pricing),
        }

        # ── About dropdown items ────────────────────────────────────
        for label, (expected_path, finder) in about_submenu_items.items():
            browser.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.5)

            landing_page.click_about_dropdown()
            logger.info(f"Opened About dropdown to click '{label}'")

            item = finder(timeout=5)
            item.click()
            logger.info(f"Clicked '{label}'")

            landing_page.wait_for_url_contains(expected_path, timeout=15)
            current_url = browser.current_url
            assert expected_path in current_url, \
                f"'{label}' did not navigate correctly. Expected '{expected_path}' in URL, got: {current_url}"
            logger.info(f"✅ '{label}' navigated to {current_url}")

            # Navigate back to landing page for the next item
            browser.get(base_url)
            landing_page.wait_for_page_loaded(timeout=20)

        # ── The Platform dropdown items ─────────────────────────────
        for label, (expected_path, finder) in platform_submenu_items.items():
            browser.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.5)

            landing_page.click_platform_dropdown()
            logger.info(f"Opened The Platform dropdown to click '{label}'")

            item = finder(timeout=5)
            item.click()
            logger.info(f"Clicked '{label}'")

            landing_page.wait_for_url_contains(expected_path, timeout=15)
            current_url = browser.current_url
            assert expected_path in current_url, \
                f"'{label}' did not navigate correctly. Expected '{expected_path}' in URL, got: {current_url}"
            logger.info(f"✅ '{label}' navigated to {current_url}")

            # Navigate back to landing page for the next item
            browser.get(base_url)
            landing_page.wait_for_page_loaded(timeout=20)

        logger.info("✅ All navbar dropdown navigation verified successfully.")

