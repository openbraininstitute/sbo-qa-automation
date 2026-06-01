# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class DigitalBrainStoryLocators:
    # Hero section
    PAGE_TITLE = (By.XPATH, "//div[contains(@class, '__hero')]//h1")
    HERO_DESCRIPTION = (By.XPATH, "//div[contains(@class, '__hero')]//div[contains(@class, '__content')]")
    HERO_IMAGE = (By.CSS_SELECTOR, "img[alt='Hero image']")
    HERO_VIDEO = (By.XPATH, "//div[contains(@class, '__hero')]//video")
    
    # Chapter titles (numbered sections like "01. A Two-Decade Odyssey...")
    CHAPTER_TITLES = (By.XPATH, "//h1[starts-with(normalize-space(), '0') or starts-with(normalize-space(), '1') or starts-with(normalize-space(), '2')]")
    
    # Paragraphs
    PARAGRAPHS = (By.XPATH, "//div[contains(@class, 'text-module') and contains(@class, '__text')]")
    
    # Main content sections
    MAIN_SECTIONS = (By.XPATH, "//div[contains(@class, 'sanity-content-paragraph-module')]")
    SECTION_TITLES = (By.XPATH, "//h1")
    SECTION_TEXTS = (By.XPATH, "//div[contains(@class, 'text-module') and contains(@class, '__text')]//p")
    SECTION_IMAGES = (By.CSS_SELECTOR, "img[alt]")
    
    # Interactive elements
    NAVIGATION_LINKS = (By.XPATH, "//a[contains(@href, '/')]")
    BUTTONS = (By.XPATH, "//button | //a[contains(@class, '__button')]")
    
    # Footer button to discover story
    DISCOVER_BUTTON = (By.XPATH, "//button[contains(@class, '__nextPanel')]")