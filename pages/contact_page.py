# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from locators.contact_locators import ContactLocators
from pages.home_page import HomePage


class ContactPage(HomePage):
    def __init__(self, browser, wait, base_url, logger=None):
        super().__init__(browser, wait, base_url)
        self.logger = logger
        self.base_url = base_url

    def go_to_page(self, retries=3, delay=5):
        """Navigate to the Contact page"""
        page_url = f"{self.base_url}/contact"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(60)
                self.browser.get(page_url)
                self.wait_for_page_ready(timeout=60)
                self.logger.info("✅ Contact page loaded successfully.")
                return
            except TimeoutException:
                self.logger.warning(
                    f"⚠️ Contact page load attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                self.wait.sleep(delay)
        raise TimeoutException("❌ Failed to load Contact page after multiple attempts.")

    def get_page_title(self):
        """Get the main page title"""
        return self.find_element(ContactLocators.PAGE_TITLE)

    def get_page_description(self):
        """Get the page description"""
        try:
            return self.find_element(ContactLocators.PAGE_DESCRIPTION)
        except:
            return None

    def get_newsletter_form(self):
        """Get the newsletter subscription form (this is the actual form on the page)"""
        try:
            return self.find_element(ContactLocators.NEWSLETTER_FORM)
        except:
            return None

    def get_email_buttons(self):
        """Get the email contact buttons"""
        try:
            return self.find_all_elements(ContactLocators.EMAIL_BUTTONS)
        except:
            return []

    def get_support_email(self):
        """Get the support email button"""
        try:
            return self.find_element(ContactLocators.SUPPORT_EMAIL)
        except:
            return None

    def get_info_email(self):
        """Get the info email button"""
        try:
            return self.find_element(ContactLocators.INFO_EMAIL)
        except:
            return None

    def get_email_input(self):
        """Get the newsletter email input field"""
        try:
            return self.find_element(ContactLocators.EMAIL_INPUT)
        except:
            return None

    def get_privacy_checkbox(self):
        """Get the privacy policy checkbox"""
        try:
            return self.find_element(ContactLocators.PRIVACY_CHECKBOX)
        except:
            return None

    def get_subscribe_button(self):
        """Get the newsletter subscribe button"""
        try:
            return self.find_element(ContactLocators.SUBSCRIBE_BUTTON)
        except:
            return None

    def get_required_field_errors(self):
        """Get validation error messages"""
        return self.find_all_elements(ContactLocators.REQUIRED_FIELD_ERRORS)

    def get_success_message(self):
        """Get success message after form submission"""
        try:
            return self.find_element(ContactLocators.SUCCESS_MESSAGE, timeout=10)
        except:
            return None

    def get_contact_info_section(self):
        """Get the contact information section"""
        try:
            return self.find_element(ContactLocators.CONTACT_INFO_SECTION)
        except:
            return None

    def get_address(self):
        """Get the address information"""
        try:
            return self.find_element(ContactLocators.ADDRESS)
        except:
            return None

    def get_phone_number(self):
        """Get the phone number"""
        try:
            return self.find_element(ContactLocators.PHONE_NUMBER)
        except:
            return None

    def get_email_address(self):
        """Get the email address"""
        try:
            return self.find_element(ContactLocators.EMAIL_ADDRESS)
        except:
            return None

    def get_map_container(self):
        """Get the map container"""
        try:
            return self.find_element(ContactLocators.MAP_CONTAINER, timeout=10)
        except:
            return None

    def get_map_iframe(self):
        """Get the map iframe"""
        try:
            return self.find_element(ContactLocators.MAP_IFRAME, timeout=10)
        except:
            return None

    def get_social_media_section(self):
        """Get the social media section"""
        try:
            return self.find_element(ContactLocators.SOCIAL_MEDIA_SECTION)
        except:
            return None

    def get_linkedin_link(self):
        """Get LinkedIn link"""
        try:
            return self.find_element(ContactLocators.LINKEDIN_LINK)
        except:
            return None

    def get_twitter_link(self):
        """Get Twitter link"""
        try:
            return self.find_element(ContactLocators.TWITTER_LINK)
        except:
            return None

    def get_facebook_link(self):
        """Get Facebook link"""
        try:
            return self.find_element(ContactLocators.FACEBOOK_LINK)
        except:
            return None

    def get_office_hours(self):
        """Get office hours information"""
        try:
            return self.find_element(ContactLocators.OFFICE_HOURS)
        except:
            return None

    def fill_contact_form(self, name, email, subject=None, message=""):
        """Fill out the contact form"""
        # Fill name
        name_input = self.get_name_input()
        name_input.clear()
        name_input.send_keys(name)
        
        # Fill email
        email_input = self.get_email_input()
        email_input.clear()
        email_input.send_keys(email)
        
        # Fill subject if field exists
        subject_input = self.get_subject_input()
        if subject_input and subject:
            subject_input.clear()
            subject_input.send_keys(subject)
        
        # Fill message
        message_textarea = self.get_message_textarea()
        message_textarea.clear()
        message_textarea.send_keys(message)

    def submit_form(self):
        """Submit the contact form"""
        submit_button = self.get_submit_button()
        submit_button.click()

    def validate_form_fields(self):
        """Validate that required form fields are present"""
        required_fields = {
            'name': self.get_name_input(),
            'email': self.get_email_input(),
            'message': self.get_message_textarea()
        }
        
        missing_fields = []
        for field_name, field_element in required_fields.items():
            if not field_element or not field_element.is_displayed():
                missing_fields.append(field_name)
        
        return missing_fields

    def test_form_validation(self):
        """Test form validation by submitting empty form"""
        # Clear all fields
        name_input = self.get_name_input()
        email_input = self.get_email_input()
        message_textarea = self.get_message_textarea()
        
        name_input.clear()
        email_input.clear()
        message_textarea.clear()
        
        # Try to submit
        self.submit_form()
        
        # Wait for validation messages
        self.wait.sleep(2)
        
        # Check for validation errors
        errors = self.get_required_field_errors()
        return len(errors) > 0

    def validate_contact_info(self):
        """Validate that contact information is present and properly formatted"""
        info = {}
        
        # Check address
        address = self.get_address()
        if address:
            info['address'] = address.text.strip()
        
        # Check phone
        phone = self.get_phone_number()
        if phone:
            info['phone'] = phone.text.strip() or phone.get_attribute('href')
        
        # Check email
        email = self.get_email_address()
        if email:
            info['email'] = email.text.strip() or email.get_attribute('href')
        
        return info

    def validate_social_links(self):
        """Validate social media links"""
        social_links = {}
        
        linkedin = self.get_linkedin_link()
        if linkedin:
            social_links['linkedin'] = linkedin.get_attribute('href')
        
        twitter = self.get_twitter_link()
        if twitter:
            social_links['twitter'] = twitter.get_attribute('href')
        
        facebook = self.get_facebook_link()
        if facebook:
            social_links['facebook'] = facebook.get_attribute('href')
        
        return social_links

    def check_map_functionality(self):
        """Check if map is present and functional"""
        map_container = self.get_map_container()
        map_iframe = self.get_map_iframe()
        
        if map_iframe:
            # Switch to iframe and check if it loads
            try:
                self.browser.switch_to.frame(map_iframe)
                # Check if map content is loaded
                map_loaded = self.wait.until(
                    EC.presence_of_element_located(("xpath", "//div | //canvas")),
                    timeout=10
                )
                self.browser.switch_to.default_content()
                return True
            except:
                self.browser.switch_to.default_content()
                return False
        
        return map_container is not None