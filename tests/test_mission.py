# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import os
import time

from selenium.webdriver.support.wait import WebDriverWait
from pages.mission_page import MissionPage
from selenium.webdriver.support import expected_conditions as EC


class TestMission:
    def test_mission(self, visit_public_pages, logger):
        _visit, base_url = visit_public_pages
        browser, wait = _visit("/mission")
        mission_page = MissionPage(browser, wait, base_url, logger=logger)

        mission_page.go_to_page()
        assert "Our mission" in browser.title
        logger.info("Mission page is loaded")

        main_title = mission_page.mission_main_title()
        assert main_title.is_displayed(), "Mission main title is not found."
        logger.info("Mission main 'hero' title is displayed")

        mission_main_text = mission_page.mission_main_page_text()
        assert mission_main_text.is_displayed(), "Mission main text is not found."
        logger.info("Mission main 'hero' text is displayed")

        main_hero_img = mission_page.main_hero_img(timeout=15)
        assert main_hero_img, "The page main page image is not found."
        logger.info("Main page image is displayed.")

        main_hero_video = mission_page.main_hero_video(timeout=15)
        assert main_hero_video, "The page main video is not found."
        logger.info("Main page video is displayed.")

        main_page_paragraph = mission_page.main_page_paragraph()
        assert main_page_paragraph.is_displayed(), "The main paragraph describing the mission is not found."
        logger.info("The main paragraph describing the mission is displayed.")

        minor_page_paragraph = mission_page.minor_page_paragraph()
        assert minor_page_paragraph.is_displayed(), "The supporting paragraph describing the mission is not found."
        logger.info("The supporting paragraph describing the mission is displayed.")

        platform_sections = mission_page.platform_sections()
        assert platform_sections.is_displayed(), "The sections describing the platform are not found."
        logger.info("The sections describing the platform are displayed")

        page_titles = mission_page.section_titles()
        assert page_titles, "Section titles are not found"
        page_title_errors = [title.text for title in page_titles if not title.text.strip()]
        assert not page_title_errors, f"Some section titles are empty: {page_title_errors}"
        logger.info(f"All section titles are present: {[t.text for t in page_titles]}")

        section_texts = mission_page.section_texts()
        assert section_texts, "Section texts are not found"
        empty_texts = [text.text for text in section_texts if not text.text.strip()]
        assert not empty_texts, f"Some section texts are empty: {empty_texts}"
        logger.info(f"All section texts are present")

        section_images = mission_page.section_images()
        assert section_images, "Section images are not found"
        missing_imgs = [img.get_attribute('src') for img in section_images if not img.get_attribute('src')]
        assert not missing_imgs, "Some section images are missing src attributes"
        logger.info("All section images are present")

        # mission_page.hover_over_button()

        # assert mission_page.is_video_playing(), "Video 1 should be playing on hover"

        subscribe_title = mission_page.subscribe_newsletter_title()
        browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", subscribe_title)
        assert subscribe_title.is_displayed(), "The 'Subscribe'title is not found."
        logger.info("Found title 'Subscribe to our newsletter'")

        original_window = browser.current_window_handle
        assert len(browser.window_handles) == 1

        current_tabs = browser.window_handles.copy()
        logger.info(f"Current tabs before click: {current_tabs}")

        ele = mission_page.button_download_mission()
        browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", ele)
        WebDriverWait(browser, 10).until(EC.visibility_of(ele))
        time.sleep(0.5)  # this time.sleep is required.
        browser.execute_script("arguments[0].click();", ele)

        wait.until(EC.number_of_windows_to_be(2))

        for window_handle in browser.window_handles:
            if window_handle != original_window:
               browser.switch_to.window(window_handle)
               break

        new_tab = [tab for tab in browser.window_handles if tab not in current_tabs][0]
        browser.switch_to.window(new_tab)
        WebDriverWait(browser, 10).until(
            lambda d: d.current_url != "about:blank"
        )

        new_url = browser.current_url
        logger.info(f"New tab URL: {new_url}")

        assert new_url.startswith("https://cdn.sanity.io/files/fgi7eh1v/"), "Not from Sanity CDN"
        assert "/staging/" in new_url or "/production/" in new_url, "PDF not served from expected environment"

        browser.close()
        browser.switch_to.window(current_tabs[0])