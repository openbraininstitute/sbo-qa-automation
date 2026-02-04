# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.common import TimeoutException
from locators.digital_brain_story_locators import DigitalBrainStoryLocators
from pages.home_page import HomePage


class DigitalBrainStoryPage(HomePage):
    def __init__(self, browser, wait, base_url, logger=None):
        super().__init__(browser, wait, base_url)
        self.logger = logger
        self.base_url = base_url

    def go_to_page(self, retries=3, delay=5):
        """Navigate to the Digital Brain Story page"""
        page_url = f"{self.base_url}/the-real-digital-brain-story"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(60)
                self.browser.get(page_url)
                self.wait_for_page_ready(timeout=60)
                self.logger.info("✅ Digital Brain Story page loaded successfully.")
                return
            except TimeoutException:
                self.logger.warning(
                    f"⚠️ Digital Brain Story page load attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                self.wait.sleep(delay)
        raise TimeoutException("❌ Failed to load Digital Brain Story page after multiple attempts.")

    def get_page_title(self):
        """Get the main page title"""
        return self.find_element(DigitalBrainStoryLocators.PAGE_TITLE)

    def get_hero_description(self):
        """Get the hero section description"""
        return self.find_element(DigitalBrainStoryLocators.HERO_DESCRIPTION)

    def get_hero_image(self):
        """Get the hero image element"""
        return self.find_element(DigitalBrainStoryLocators.HERO_IMAGE)

    def get_hero_video(self):
        """Get the hero video element if present"""
        try:
            return self.find_element(DigitalBrainStoryLocators.HERO_VIDEO, timeout=5)
        except:
            return None

    def get_main_sections(self):
        """Get all main content sections"""
        return self.find_all_elements(DigitalBrainStoryLocators.MAIN_SECTIONS)

    def get_section_titles(self):
        """Get all section titles"""
        return self.find_all_elements(DigitalBrainStoryLocators.SECTION_TITLES)

    def get_section_texts(self):
        """Get all section text content"""
        return self.find_all_elements(DigitalBrainStoryLocators.SECTION_TEXTS)

    def get_section_images(self):
        """Get all section images"""
        return self.find_all_elements(DigitalBrainStoryLocators.SECTION_IMAGES)

    def get_navigation_links(self):
        """Get all navigation links"""
        return self.find_all_elements(DigitalBrainStoryLocators.NAVIGATION_LINKS)

    def get_buttons(self):
        """Get all interactive buttons"""
        return self.find_all_elements(DigitalBrainStoryLocators.BUTTONS)

    def get_story_timeline(self):
        """Get story timeline element if present"""
        try:
            return self.find_element(DigitalBrainStoryLocators.STORY_TIMELINE, timeout=5)
        except:
            return None

    def get_story_chapters(self):
        """Get story chapters if present"""
        try:
            return self.find_all_elements(DigitalBrainStoryLocators.STORY_CHAPTERS, timeout=5)
        except:
            return []

    def get_research_highlights(self):
        """Get research highlights if present"""
        try:
            return self.find_all_elements(DigitalBrainStoryLocators.RESEARCH_HIGHLIGHTS, timeout=5)
        except:
            return []

    def wait_for_hero_image_load(self, timeout=20):
        """Wait for hero image to load completely"""
        hero_image = self.get_hero_image()
        if hero_image:
            self.wait_for_image_to_load(DigitalBrainStoryLocators.HERO_IMAGE, timeout)

    def wait_for_hero_video_load(self, timeout=20):
        """Wait for hero video to load if present"""
        hero_video = self.get_hero_video()
        if hero_video:
            self.wait_for_video_to_load(DigitalBrainStoryLocators.HERO_VIDEO, timeout)

    def scroll_through_content(self):
        """Scroll through the page content to ensure all elements load"""
        import time
        sections = self.get_main_sections()
        for section in sections:
            self.browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", section)
            time.sleep(1)  # Brief pause for content to load

    def validate_images_loaded(self):
        """Validate that all images on the page have loaded properly"""
        images = self.get_section_images()
        failed_images = []
        
        for img in images:
            try:
                # Scroll to image
                self.browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", img)
                
                # Check if image is loaded
                is_loaded = self.browser.execute_script(
                    "return arguments[0].complete && arguments[0].naturalWidth > 0;", img
                )
                
                if not is_loaded or not img.is_displayed():
                    failed_images.append(img.get_attribute('src') or img.get_attribute('alt') or 'Unknown image')
            except Exception as e:
                failed_images.append(f"Error checking image: {str(e)}")
        
        return failed_images