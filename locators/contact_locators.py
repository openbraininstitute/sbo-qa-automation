# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class ContactLocators:
    # Page header
    PAGE_TITLE = (By.XPATH, "//div[contains(@class,'__hero')]//h1[text()='Contact']")
    PAGE_DESCRIPTION = (By.XPATH, "//div[contains(@class,'__hero')]//div[contains(@class,'__content')]")
    HERO_IMAGE = (By.CSS_SELECTOR, "img[alt='Hero image']")
    HERO_VIDEO = (By.XPATH, "//div[contains(@class,'__hero')]//video")

    # Email buttons
    EMAIL_BUTTONS = (By.XPATH, "//a[contains(@class,'email-button-module') and contains(@class,'__emailButton')]")
    SUPPORT_EMAIL = (By.XPATH, "//a[@href='mailto:support@openbraininstitute.org']")
    INFO_EMAIL = (By.XPATH, "//a[@href='mailto:info@openbraininstitute.org']")
    SUPPORT_EMAIL_LABEL = (By.XPATH, "//a[@href='mailto:support@openbraininstitute.org']//div")
    INFO_EMAIL_LABEL = (By.XPATH, "//a[@href='mailto:info@openbraininstitute.org']//div")

    # Newsletter subscription form
    NEWSLETTER_FORM = (By.XPATH, "//div[contains(@class,'newsletter-subscription-module') and contains(@class,'__newsLetterSubscription')]")
    EMAIL_INPUT = (By.XPATH, "//input[@placeholder='Enter your email here...']")
    PRIVACY_CHECKBOX = (By.XPATH, "//div[contains(@class,'newsletter-subscription-module')]//input[@type='checkbox']")
    SUBSCRIBE_BUTTON = (By.XPATH, "//button[contains(text(), 'Subscribe')]")

    # Social media links
    SOCIAL_MEDIA_SECTION = (By.XPATH, "//div[contains(@class,'social-media-links-module') and contains(@class,'__socialMediaLinks')]")
    LINKEDIN_LINK = (By.XPATH, "//a[contains(@href, 'linkedin')]")
    TWITTER_LINK = (By.XPATH, "//a[contains(@href, 'x.com')]")
    YOUTUBE_LINK = (By.XPATH, "//a[contains(@href, 'youtube')]")
    BLUESKY_LINK = (By.XPATH, "//a[contains(@href, 'bsky')]")

    # Footer
    FOOTER = (By.XPATH, "//div[contains(@class,'footer-panel-module') and contains(@class,'__footerPanel')]")
