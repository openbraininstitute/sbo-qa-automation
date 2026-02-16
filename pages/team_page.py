# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.common import TimeoutException, NoSuchElementException
from locators.team_locators import TeamLocators
from pages.home_page import HomePage


class TeamPage(HomePage):
    def __init__(self, browser, wait, base_url, logger=None):
        super().__init__(browser, wait, base_url)
        self.logger = logger
        self.base_url = base_url

    def go_to_page(self, retries=3):
        """Navigate to the Team page"""
        page_url = f"{self.base_url}/team"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(60)
                self.browser.get(page_url)
                self.wait_for_page_ready(timeout=60)
                
                # Wait for actual content to load (page title element)
                self.get_page_title()
                
                self.logger.info("✅ Team page loaded successfully.")
                return
            except TimeoutException:
                if attempt < retries - 1:
                    self.logger.warning(f"⚠️ Team page load attempt {attempt + 1} failed. Retrying...")
                else:
                    self.logger.error("❌ Failed to load Team page after multiple attempts.")
        raise TimeoutException("❌ Failed to load Team page after multiple attempts.")

    def get_page_title(self):
        """Get the main page title"""
        return self.find_element(TeamLocators.PAGE_TITLE)

    def get_page_description(self):
        """Get the page description"""
        try:
            return self.find_element(TeamLocators.PAGE_DESCRIPTION)
        except:
            return None

    def get_team_member_cards(self):
        """Get all team member cards"""
        return self.find_all_elements(TeamLocators.TEAM_MEMBER_CARDS)

    def get_member_names(self):
        """Get all team member names"""
        return self.find_all_elements(TeamLocators.MEMBER_NAMES)

    def get_member_roles(self):
        """Get all team member roles/positions"""
        return self.find_all_elements(TeamLocators.MEMBER_ROLES)

    def get_member_photos(self):
        """Get all team member photos"""
        return self.find_all_elements(TeamLocators.MEMBER_PHOTOS)

    def get_member_bios(self):
        """Get all team member bios/descriptions"""
        return self.find_all_elements(TeamLocators.MEMBER_BIOS)

    def get_social_links(self):
        """Get all social media links"""
        try:
            return self.find_all_elements(TeamLocators.SOCIAL_LINKS, timeout=5)
        except:
            return []

    def get_linkedin_links(self):
        """Get LinkedIn links"""
        try:
            return self.find_all_elements(TeamLocators.LINKEDIN_LINKS, timeout=5)
        except:
            return []

    def get_twitter_links(self):
        """Get Twitter/X links"""
        try:
            return self.find_all_elements(TeamLocators.TWITTER_LINKS, timeout=5)
        except:
            return []

    def get_youtube_links(self):
        """Get YouTube links"""
        try:
            return self.find_all_elements(TeamLocators.YOUTUBE_LINKS, timeout=5)
        except:
            return []

    def get_bluesky_links(self):
        """Get BlueSky links"""
        try:
            return self.find_all_elements(TeamLocators.BLUESKY_LINKS, timeout=5)
        except:
            return []

    def get_search_input(self):
        """Get search input if present"""
        try:
            return self.find_element(TeamLocators.SEARCH_INPUT, timeout=5)
        except:
            return None

    def get_filter_buttons(self):
        """Get filter buttons if present"""
        try:
            return self.find_all_elements(TeamLocators.FILTER_BUTTONS, timeout=5)
        except:
            return []

    def get_team_sections(self):
        """Get team sections (departments/roles)"""
        try:
            return self.find_all_elements(TeamLocators.TEAM_SECTIONS, timeout=5)
        except:
            return []

    def get_section_headers(self):
        """Get section headers"""
        try:
            return self.find_all_elements(TeamLocators.SECTION_HEADERS, timeout=5)
        except:
            return []

    def extract_member_info(self, member_card):
        """Extract information from a team member card"""
        info = {
            'name': '',
            'role': '',
            'photo_src': '',
            'bio': '',  # Optional - only top management has bios
            'social_links': [],
            'has_bio': False
        }
        
        try:
            # Extract name
            name_element = member_card.find_element(*TeamLocators.MEMBER_NAMES)
            info['name'] = name_element.text.strip()
        except NoSuchElementException:
            pass
        
        try:
            # Extract role
            role_element = member_card.find_element(*TeamLocators.MEMBER_ROLES)
            info['role'] = role_element.text.strip()
        except NoSuchElementException:
            pass
        
        try:
            # Extract photo
            photo_element = member_card.find_element(*TeamLocators.MEMBER_PHOTOS)
            info['photo_src'] = photo_element.get_attribute('src')
        except NoSuchElementException:
            pass
        
        try:
            # Extract bio (optional - only for top management)
            bio_element = member_card.find_element(*TeamLocators.MEMBER_BIOS)
            bio_text = bio_element.text.strip()
            if bio_text:
                info['bio'] = bio_text
                info['has_bio'] = True
        except NoSuchElementException:
            # Bio not present - this is normal for regular team members
            pass
        
        try:
            # Extract social links
            social_elements = member_card.find_elements(*TeamLocators.SOCIAL_LINKS)
            info['social_links'] = [link.get_attribute('href') for link in social_elements]
        except NoSuchElementException:
            pass
        
        return info

    def validate_member_photos_loaded(self):
        """Validate that all member photos have loaded properly"""
        photos = self.get_member_photos()
        failed_photos = []
        
        for photo in photos:
            try:
                # Scroll to photo
                self.browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", photo)
                
                # Check if photo is loaded
                is_loaded = self.browser.execute_script(
                    "return arguments[0].complete && arguments[0].naturalWidth > 0;", photo
                )
                
                if not is_loaded or not photo.is_displayed():
                    failed_photos.append(photo.get_attribute('src') or photo.get_attribute('alt') or 'Unknown photo')
            except Exception as e:
                failed_photos.append(f"Error checking photo: {str(e)}")
        
        return failed_photos

    def search_team_members(self, search_term):
        """Search for team members if search functionality exists"""
        search_input = self.get_search_input()
        if search_input:
            search_input.clear()
            search_input.send_keys(search_term)
            # Wait for search results to update
            self.wait.sleep(2)
            return True
        return False

    def get_management_members(self):
        """Get team members who have bios (typically top management)"""
        all_members = self.get_team_member_cards()
        management_members = []
        
        for member in all_members:
            member_info = self.extract_member_info(member)
            if member_info['has_bio']:
                management_members.append(member)
        
        return management_members

    def get_regular_members(self):
        """Get team members who don't have bios (regular team members)"""
        all_members = self.get_team_member_cards()
        regular_members = []
        
        for member in all_members:
            member_info = self.extract_member_info(member)
            if not member_info['has_bio']:
                regular_members.append(member)
        
        return regular_members

    def validate_team_structure(self):
        """Validate the team page structure - management vs regular members"""
        all_members = self.get_team_member_cards()
        management_count = 0
        regular_count = 0
        
        for member in all_members:
            member_info = self.extract_member_info(member)
            if member_info['has_bio']:
                management_count += 1
            else:
                regular_count += 1
        
        return {
            'total_members': len(all_members),
            'management_members': management_count,
            'regular_members': regular_count,
            'has_management_bios': management_count > 0
        }