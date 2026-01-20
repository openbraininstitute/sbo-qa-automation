# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.common import TimeoutException, ElementNotInteractableException, NoSuchElementException
from selenium.webdriver import ActionChains
from locators.mission_locators import MissionLocators
from pages.home_page import HomePage


class MissionPage(HomePage):
    def __init__(self, browser, wait, base_url, lab_url=None, logger=None):
        super().__init__(browser, wait, base_url)
        self.home_page = HomePage(browser, wait, base_url)
        self.logger = logger
        self.base_url = base_url
        self.lab_url  = lab_url

    def go_to_page(self, retries=3, delay=5):
        about_url = f"{self.base_url}/mission"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(60)
                self.browser.get(about_url)
                self.wait_for_page_ready(timeout=60)
                self.logger.info("✅ Mission Page loaded successfully.")
                return
            except TimeoutException:
                self.logger.warning(
                    f"⚠️ Landing Page load attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                self.wait.sleep(delay)
        raise TimeoutException("❌ Failed to load Landing Page after multiple attempts.")

    def button_download_mission(self):
        return self.find_element(MissionLocators.BTN_DOWNLOAD_MISSION)

    def hover_over_button(self):
        button_element = self.browser.find_element(MissionLocators.VLAB_CARDS_BTN)
        ActionChains(self.browser).move_to_element(button_element).perform()

    def is_video_playing(self):
        video_element = self.browser.find_element(MissionLocators.VIDEO1)
        return self.browser.execute_script(
            "return arguments[0].readyState >= 3 && !arguments[0].paused;",
            video_element
        )

    def mission_main_title(self):
        return self.find_element(MissionLocators.MISSION_PAGE_TITLE)

    def mission_main_page_text(self):
        return self.find_element(MissionLocators.MISSION_MAIN_TEXT)

    def main_hero_img(self, timeout=15):
        return self.element_visibility(MissionLocators.MAIN_HERO_IMG, timeout=timeout)

    def main_hero_video(self, timeout=15):
        return self.element_visibility(MissionLocators.MAIN_HERO_VIDEO, timeout=timeout)

    def main_page_paragraph(self):
        return self.find_element(MissionLocators.MAIN_PAGE_PARAGRAPH)

    def minor_page_paragraph(self):
        return self.find_element(MissionLocators.MINOR_PAGE_PARAGRAPH)

    def new_tab_pdf(self):
        return self.find_element(MissionLocators.PDF_NEW_TAB)

    def debug_platform_sections(self):
        """Debug method to help identify platform section elements."""
        try:
            # Look for any div with VirtualLab in class name
            virtual_lab_elements = self.browser.find_elements(By.XPATH, "//div[contains(@class, 'VirtualLab')]")
            self.logger.info(f"Found {len(virtual_lab_elements)} elements with 'VirtualLab' in class")
            
            # Look for any div with Panel in class name  
            panel_elements = self.browser.find_elements(By.XPATH, "//div[contains(@class, 'Panel')]")
            self.logger.info(f"Found {len(panel_elements)} elements with 'Panel' in class")
            
            # Look for section elements
            section_elements = self.browser.find_elements(By.XPATH, "//section")
            self.logger.info(f"Found {len(section_elements)} section elements")
            
            # Log some class names for debugging
            all_divs = self.browser.find_elements(By.XPATH, "//div[@class]")[:20]  # First 20 divs with classes
            for i, div in enumerate(all_divs):
                class_name = div.get_attribute('class')
                if 'module' in class_name.lower() or 'panel' in class_name.lower():
                    self.logger.info(f"Div {i}: class='{class_name}'")
                    
        except Exception as e:
            self.logger.error(f"Debug failed: {e}")

    def platform_sections(self, timeout=20):
        """Get platform sections using base page wrapper methods."""
        try:
            self.logger.info("Looking for platform sections...")
            
            # Use the base page wrapper method to wait for element presence
            element = self.find_element(MissionLocators.PLATFORM_SECTIONS, timeout=timeout)
            
            # Scroll to the element to ensure it's in view
            self.browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            
            # Wait a moment for any animations
            import time
            time.sleep(2)
            
            # Use the base page wrapper method to wait for visibility
            visible_element = self.element_visibility(MissionLocators.PLATFORM_SECTIONS, timeout=10)
            
            self.logger.info("✅ Platform sections found and visible")
            return visible_element
                
        except Exception as e:
            self.logger.error(f"Failed to find platform sections: {e}")
            
            # Run debug to see what's available
            self.debug_platform_sections()
            
            # Re-raise the exception to fail the test with debug info
            raise

    def page_titles(self):
        return self.find_all_elements(MissionLocators.MAIN_TITLES)

    def section_titles(self):
        return self.find_all_elements(MissionLocators.P_SECTION_TITLES)

    def section_texts(self):
        return self.find_all_elements(MissionLocators.P_SECTION_TEXTS)

    def section_images(self):
        return self.find_all_elements(MissionLocators.P_SECTION_IMAGES)

    def subscribe_newsletter_title(self):
        return self.find_element(MissionLocators.SUBSCRIBE_NEWSLETTER)

