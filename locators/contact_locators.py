# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class ContactLocators:
    # Page header
    PAGE_TITLE = (By.XPATH, "//h1[contains(text(), 'Contact')]")
    PAGE_DESCRIPTION = (By.CSS_SELECTOR, ".Hero-module__E0OG9W__content")
    
    # Email buttons (instead of traditional contact form)
    EMAIL_BUTTONS = (By.CSS_SELECTOR, ".EmailButton-module__kF7opG__emailButton")
    SUPPORT_EMAIL = (By.XPATH, "//a[@href='mailto:support@openbraininstitute.org']")
    INFO_EMAIL = (By.XPATH, "//a[@href='mailto:info@openbraininstitute.org']")
    
    # Newsletter subscription form (this is the actual form)
    NEWSLETTER_FORM = (By.CSS_SELECTOR, ".NewsLetterSubscription-module__C5psVq__newsLetterSubscription")
    EMAIL_INPUT = (By.XPATH, "//input[@placeholder='Enter your email here...']")
    PRIVACY_CHECKBOX = (By.CSS_SELECTOR, "input[id='_r_b_']")
    SUBSCRIBE_BUTTON = (By.XPATH, "//button[contains(text(), 'Subscribe')]")
    
    # Form validation messages
    REQUIRED_FIELD_ERRORS = (By.XPATH, "//div[contains(@class, 'error')] | //span[contains(@class, 'error')]")
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class, 'success')] | //div[contains(text(), 'Thank you') or contains(text(), 'sent')]")
    
    # Contact information (email addresses)
    CONTACT_INFO_SECTION = (By.CSS_SELECTOR, ".styles-module__5IYxQa__layout")
    
    # Social media links (same as team page)
    SOCIAL_MEDIA_SECTION = (By.CSS_SELECTOR, ".FooterPanel-module__YUozGG__socialmedia")
    LINKEDIN_LINK = (By.XPATH, "//a[contains(@href, 'linkedin')]")
    TWITTER_LINK = (By.XPATH, "//a[contains(@href, 'x.com')]")
    FACEBOOK_LINK = (By.XPATH, "//a[contains(@href, 'facebook')]")
    YOUTUBE_LINK = (By.XPATH, "//a[contains(@href, 'youtube')]")
    BLUESKY_LINK = (By.XPATH, "//a[contains(@href, 'bsky')]")
    
    # Footer
    FOOTER = (By.CSS_SELECTOR, ".FooterPanel-module__YUozGG__footerPanel")