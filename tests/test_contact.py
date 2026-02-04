# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from pages.contact_page import ContactPage


class TestContact:
    def test_contact(self, visit_public_pages, logger):
        """Test the Contact page functionality"""
        _visit, base_url = visit_public_pages
        browser, wait = _visit("/contact")
        contact_page = ContactPage(browser, wait, base_url, logger=logger)

        # Navigate to page
        contact_page.go_to_page()
        assert "Contact" in browser.title
        logger.info("Contact page loaded successfully")

        # Test page title
        page_title = contact_page.get_page_title()
        assert page_title.is_displayed(), "Page title is not displayed"
        logger.info(f"Page title found: {page_title.text}")

        # Test page description (optional)
        page_description = contact_page.get_page_description()
        if page_description:
            assert page_description.is_displayed(), "Page description is not displayed"
            logger.info("Page description is present")

        # Test newsletter form presence (this is the actual form on the page)
        newsletter_form = contact_page.get_newsletter_form()
        if newsletter_form:
            assert newsletter_form.is_displayed(), "Newsletter form is not displayed"
            logger.info("Newsletter subscription form found")
        else:
            logger.info("No newsletter form found")

        # Test email contact buttons
        email_buttons = contact_page.get_email_buttons()
        assert len(email_buttons) > 0, "No email contact buttons found"
        logger.info(f"Found {len(email_buttons)} email contact buttons")

        # Test support email button
        support_email = contact_page.get_support_email()
        if support_email:
            assert support_email.is_displayed(), "Support email button is not displayed"
            assert support_email.is_enabled(), "Support email button is not enabled"
            href = support_email.get_attribute('href')
            assert 'mailto:support@openbraininstitute.org' in href, f"Invalid support email link: {href}"
            logger.info("Support email button is functional")

        # Test info email button
        info_email = contact_page.get_info_email()
        if info_email:
            assert info_email.is_displayed(), "Info email button is not displayed"
            assert info_email.is_enabled(), "Info email button is not enabled"
            href = info_email.get_attribute('href')
            assert 'mailto:info@openbraininstitute.org' in href, f"Invalid info email link: {href}"
            logger.info("Info email button is functional")

        # Test newsletter form fields (if form exists)
        if newsletter_form:
            email_input = contact_page.get_email_input()
            if email_input:
                assert email_input.is_displayed(), "Newsletter email input is not displayed"
                assert email_input.is_enabled(), "Newsletter email input is not enabled"
                logger.info("Newsletter email input is functional")

            privacy_checkbox = contact_page.get_privacy_checkbox()
            if privacy_checkbox:
                assert privacy_checkbox.is_displayed(), "Privacy checkbox is not displayed"
                logger.info("Privacy policy checkbox found")

            subscribe_button = contact_page.get_subscribe_button()
            if subscribe_button:
                assert subscribe_button.is_displayed(), "Subscribe button is not displayed"
                # Button might be disabled until email is entered and checkbox is checked
                logger.info(f"Subscribe button found (enabled: {subscribe_button.is_enabled()})")

        # Test contact information section
        contact_info = contact_page.get_contact_info_section()
        if contact_info:
            assert contact_info.is_displayed(), "Contact information section is not displayed"
            logger.info("Contact information section found")

        # Validate contact information
        contact_info_data = contact_page.validate_contact_info()
        if contact_info_data:
            logger.info("Contact information found:")
            if 'address' in contact_info_data:
                logger.info(f"  Address: {contact_info_data['address'][:50]}...")
            if 'phone' in contact_info_data:
                logger.info(f"  Phone: {contact_info_data['phone']}")
            if 'email' in contact_info_data:
                logger.info(f"  Email: {contact_info_data['email']}")

        # Test address
        address = contact_page.get_address()
        if address:
            assert address.is_displayed(), "Address is not displayed"
            assert address.text.strip(), "Address text is empty"
            logger.info("Address information is present")

        # Test phone number
        phone = contact_page.get_phone_number()
        if phone:
            assert phone.is_displayed(), "Phone number is not displayed"
            phone_text = phone.text.strip() or phone.get_attribute('href')
            assert phone_text, "Phone number is empty"
            logger.info("Phone number is present")

        # Test email address
        email = contact_page.get_email_address()
        if email:
            assert email.is_displayed(), "Email address is not displayed"
            email_text = email.text.strip() or email.get_attribute('href')
            assert email_text, "Email address is empty"
            logger.info("Email address is present")

        # Test map functionality
        map_functional = contact_page.check_map_functionality()
        if map_functional:
            logger.info("Map integration is present and functional")
        else:
            logger.info("No map integration found")

        # Test social media links
        social_links = contact_page.validate_social_links()
        if social_links:
            logger.info("Social media links found:")
            for platform, url in social_links.items():
                assert url and url.startswith('http'), f"Invalid {platform} link: {url}"
                logger.info(f"  {platform.capitalize()}: {url}")

        # Test individual social links
        linkedin_link = contact_page.get_linkedin_link()
        if linkedin_link:
            href = linkedin_link.get_attribute('href')
            assert 'linkedin.com' in href, f"Invalid LinkedIn link: {href}"
            logger.info("LinkedIn link is valid")

        twitter_link = contact_page.get_twitter_link()
        if twitter_link:
            href = twitter_link.get_attribute('href')
            assert 'twitter.com' in href or 'x.com' in href, f"Invalid Twitter link: {href}"
            logger.info("Twitter link is valid")

        facebook_link = contact_page.get_facebook_link()
        if facebook_link:
            href = facebook_link.get_attribute('href')
            assert 'facebook.com' in href, f"Invalid Facebook link: {href}"
            logger.info("Facebook link is valid")

        # Test office hours (if present)
        office_hours = contact_page.get_office_hours()
        if office_hours:
            assert office_hours.is_displayed(), "Office hours are not displayed"
            assert office_hours.text.strip(), "Office hours text is empty"
            logger.info("Office hours information is present")

        # Test newsletter form filling (without submitting)
        if newsletter_form and email_input:
            logger.info("Testing newsletter form filling functionality...")
            
            # Fill email
            email_input.clear()
            email_input.send_keys("test@example.com")
            
            # Check privacy checkbox if present
            if privacy_checkbox:
                if not privacy_checkbox.is_selected():
                    privacy_checkbox.click()
                logger.info("Privacy checkbox checked")
            
            # Verify form was filled
            assert email_input.get_attribute('value') == "test@example.com", "Email field was not filled correctly"
            
            if privacy_checkbox:
                assert privacy_checkbox.is_selected(), "Privacy checkbox was not checked"
            
            # Clear form for cleanup
            email_input.clear()
            if privacy_checkbox and privacy_checkbox.is_selected():
                privacy_checkbox.click()
            
            logger.info("Newsletter form filled and cleared successfully")
        else:
            logger.info("No newsletter form to test")

        logger.info("✅ Contact page test completed successfully")