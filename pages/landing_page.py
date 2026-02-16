# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

from selenium.common import TimeoutException
from locators.landing_locators import LandingLocators
from pages.home_page import HomePage


class LandingPage(HomePage):
    def __init__(self, browser, wait, base_url, logger):
        # Don't call super().__init__ to avoid parameter confusion
        # Initialize directly
        self.browser = browser
        self.wait = wait
        self.logger = logger
        self.base_url = base_url
        self.browser.set_page_load_timeout(60)

    def go_to_landing_page(self, timeout=20):
        self.browser.get(self.base_url)
        # Set Matomo exclusion flag for automated tests
        try:
            self.browser.execute_script('window._isSeleniumTest = true;')
        except Exception:
            pass
        self.wait_for_page_loaded(timeout=timeout)
        banner_title = self.find_banner_title(timeout=timeout)
        return banner_title

    def wait_for_page_loaded(self, timeout=40):
        return self.wait.until(
            lambda driver: self.obi_logo(timeout=timeout).is_displayed(),
            message=f"Build menu title did not appear within {timeout} seconds"
        )

    def obi_logo(self, timeout=10):
        return self.is_visible(LandingLocators.OBI_LOGO, timeout=timeout)

    def go_to_lab(self, timeout=10):
        return self.find_element(LandingLocators.GOTO_LAB, timeout=timeout)

    def click_go_to_lab(self):
        """Click the Go to Lab button with improved reliability for CI environments."""
        try:
            # First scroll to top to ensure the navigation menu is visible
            self.logger.info("Scrolling to top to ensure navigation menu is visible")
            self.browser.execute_script("window.scrollTo(0, 0);")
            
            import time
            time.sleep(2)  # Increased wait for scroll to complete
            
            # Log current URL before clicking
            current_url = self.browser.current_url
            self.logger.info(f"Current URL before clicking: {current_url}")
            
            # Try the menu "Login" button first (since it's what the user expects)
            try:
                self.logger.info("Attempting to click the menu 'Login' button")
                login_button = self.element_to_be_clickable(LandingLocators.LOGIN_BUTTON, timeout=15)
                
                # Log button details for debugging
                button_href = login_button.get_attribute('href')
                button_text = login_button.text
                self.logger.info(f"Login button found - href: {button_href}, text: '{button_text}'")
                
                # Click and wait briefly
                login_button.click()
                time.sleep(3)  # Wait for navigation to start
                
                # Log URL after click
                new_url = self.browser.current_url
                self.logger.info(f"URL after clicking Login button: {new_url}")
                
                # Check if navigation started
                if new_url != current_url:
                    self.logger.info("✅ Navigation started successfully with Login button")
                    return
                else:
                    self.logger.warning("URL didn't change after clicking Login button")
                    
            except Exception as menu_btn_error:
                self.logger.warning(f"Menu Login button failed: {menu_btn_error}")
            
            # Fallback to the big "Go to Virtual Labs" button
            try:
                self.logger.info("Attempting to click the main 'Go to Virtual Labs' button as fallback")
                
                # Scroll to the main button
                main_button = self.find_element(LandingLocators.GOTO_LAB, timeout=15)
                self.browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", main_button)
                time.sleep(2)
                
                # Log button details
                button_href = main_button.get_attribute('href')
                self.logger.info(f"Main button found - href: {button_href}")
                
                # Make it clickable and click
                clickable_button = self.element_to_be_clickable(LandingLocators.GOTO_LAB, timeout=10)
                clickable_button.click()
                time.sleep(3)
                
                # Log URL after click
                new_url = self.browser.current_url
                self.logger.info(f"URL after clicking main button: {new_url}")
                
                if new_url != current_url:
                    self.logger.info("✅ Navigation started successfully with main button")
                    return
                else:
                    self.logger.warning("URL didn't change after clicking main button")
                    
            except Exception as main_btn_error:
                self.logger.warning(f"Main button failed: {main_btn_error}")
            
            # If both fail, try JavaScript click as last resort
            try:
                self.logger.info("Trying JavaScript click as last resort")
                login_button = self.find_element(LandingLocators.LOGIN_BUTTON, timeout=10)
                self.browser.execute_script("arguments[0].click();", login_button)
                time.sleep(3)
                
                new_url = self.browser.current_url
                self.logger.info(f"URL after JavaScript click: {new_url}")
                
                if new_url != current_url:
                    self.logger.info("✅ Navigation started with JavaScript click")
                    return
                    
            except Exception as js_error:
                self.logger.warning(f"JavaScript click failed: {js_error}")
            
            # If all methods fail, raise an error
            raise Exception("All login button click methods failed - no navigation occurred")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to click any login button: {e}")
            
            # Take screenshot for debugging
            try:
                screenshot_path = f"login_click_failed_{int(time.time())}.png"
                self.browser.save_screenshot(screenshot_path)
                self.logger.info(f"Screenshot saved: {screenshot_path}")
            except:
                pass
                
            raise

    def digital_brains_video(self):
        return self.is_visible(LandingLocators.DIGITAL_BRAINS_VIDEO)

    def digital_brains_play_btn(self, timeout=10):
        return self.find_element(LandingLocators.DIGITAL_BRAINS_PLAY_BTN, timeout=timeout)

    def find_video_container(self, timeout=10):
        return self.find_element(LandingLocators.VIDEO_CONTAINER, timeout=timeout)

    def video_pointer(self, timeout=10):
        return self.find_element(LandingLocators.VIDEO_POINTER, timeout=timeout)

    def digital_brains_pause_btn(self, timeout=10):
        return self.find_element(LandingLocators.DIGITAL_BRAINS_PAUSE_BTN, timeout=timeout)

    def digital_brains_current_step(self):
        return self.find_element(LandingLocators.DIGITAL_BRAINS_VIDEO_CURRENT_STEP)

    def digital_brains_steps(self):
        return self.find_all_elements(LandingLocators.DIGITAL_BRAINS_VIDEO_STEP)

    def find_banner_title(self, timeout=10):
        return self.find_element(LandingLocators.BANNER_TITLE, timeout=timeout)

    def find_title_accelerate(self):
        return self.find_element(LandingLocators.TITLE_ACCELERATE)

    def find_title_dig_brain(self):
        return self.find_element(LandingLocators.TITLE_DIG_BRAIN)

    def find_title_who(self):
        return self.find_element(LandingLocators.TITLE_WHO)

    def find_title_news(self):
        return self.find_element(LandingLocators.TITLE_NEWS)

    def find_p_text1(self):
        return self.find_element(LandingLocators.P_TEXT1)

    def find_p_text2(self):
        return self.find_element(LandingLocators.P_TEXT2)

    def find_p_text3(self):
        return self.find_element(LandingLocators.P_TEXT3)

    def find_p_text4(self):
        return self.find_element(LandingLocators.P_TEXT4)

    def find_p_text5(self):
        return self.find_element(LandingLocators.P_TEXT5)

    def find_paragraph_text(self):
        return self.find_all_elements(LandingLocators.PARA_TEXT)

    def find_big_img1(self):
        return self.find_element(LandingLocators.BIG_IMG1)

    def find_big_img2(self):
        return self.find_element(LandingLocators.BIG_IMG2)

    def find_big_img3(self):
        return self.find_element(LandingLocators.BIG_IMG3)

    def find_section_btn1(self):
        return self.find_element(LandingLocators.SECTION_BTN1)

    def find_section_btn2(self):
        return self.find_element(LandingLocators.SECTION_BTN2)

    def find_section_btn3(self):
        return self.find_element(LandingLocators.SECTION_BTN3)

    def find_section_btn4(self):
        return self.find_element(LandingLocators.SECTION_BTN4)

    def find_section_btn5(self):
        return self.find_element(LandingLocators.SECTION_BTN5)

    def find_horizontal_cards_section1(self):
        return self.find_element(LandingLocators.HORIZONTAL_CARDS_SECTION1)

    def find_horizontal_cards_section2(self):
        return self.find_element(LandingLocators.HORIZONTAL_CARDS_SECTION2)

    def find_horizontal_cards_section3(self):
        return self.find_element(LandingLocators.HORIZONTAL_CARDS_SECTION3)

    def find_news_content1(self):
        return self.find_element(LandingLocators.NEWS_CARD_CONTENT1)

    def find_news_content2(self):
        return self.find_element(LandingLocators.NEWS_CARD_CONTENT2)

    def find_news_content3(self):
        return self.find_element(LandingLocators.NEWS_CARD_CONTENT3)

    def find_news_content4(self):
        return self.find_element(LandingLocators.NEWS_CARD_CONTENT4)

    def find_news_card_pic1(self):
        return self.find_element(LandingLocators.NEWS_CARD_PIC1)

    def find_news_card_pic2(self):
        return self.find_element(LandingLocators.NEWS_CARD_PIC2)

    def find_news_card_pic3(self):
        return self.find_element(LandingLocators.NEWS_CARD_PIC3)

    def find_news_card_pic4(self):
        return self.find_element(LandingLocators.NEWS_CARD_PIC4)

    def find_top_menu(self):
        return self.find_element(LandingLocators.TOP_MENU)

    def find_top_about(self):
        return self.find_element(LandingLocators.TOP_ABOUT)

    def find_top_mission(self):
        return self.find_element(LandingLocators.TOP_MISSION)

    def find_top_news(self):
        return self.find_element(LandingLocators.TOP_NEWS)

    def find_top_pricing(self):
        return self.find_element(LandingLocators.TOP_PRICING)

    def find_top_team(self):
        return self.find_element(LandingLocators.TOP_TEAM)

    def find_top_resources(self):
        return self.find_element(LandingLocators.TOP_RESOURCES)

    def find_top_contact(self):
        return self.find_element(LandingLocators.TOP_CONTACT)

    def find_menu_logo(self):
        return self.find_element(LandingLocators.TOP_MENU_LOGO)

    def footer_obi_logo(self):
        return self.find_element(LandingLocators.FOOTER_OBI_LOGO)

    def footer_obi_copyright(self):
        return  self.find_element(LandingLocators.FOOTER_OBI_COPYRIGHT)

    def footer_link_titles(self):
        """
        Returns a list of footer link titles (text of <a> elements).
        """
        links = self.find_all_elements(LandingLocators.FOOTER_LINK_TITLES)
        return [link.text.strip() for link in links if link.text.strip()]

    def footer_social_media_links(self):
        """
        Returns a list of social media links (href attributes of <a> elements).
        """
        elements = self.find_all_elements(LandingLocators.FOOTER_SOCIAL_MEDIA_LINKS)
        return [el.get_attribute("href") for el in elements]


    def footer_subscribe_block(self):
        return self.find_element(LandingLocators.FOOTER_SUBSCRIBE_BLOCK)

    def hero_background_img(self, timeout=25):
        return self.is_visible(LandingLocators.HERO_BACKGROUND_IMG, timeout=timeout)

    def hero_background_video(self, timeout=25):
        return self.is_visible(LandingLocators.HERO_BACKGROUND_VIDEO, timeout=timeout)

    def horizontal_card_sections(self):
        return {
            "Section 1": self.find_horizontal_cards_section1(),
            "Section 2": self.find_horizontal_cards_section2(),
            "Section 3": self.find_horizontal_cards_section3(),
        }

    def video_title1(self, timeout=15):
        return self.find_element(LandingLocators.VIDEO_TITLE1, timeout=timeout)