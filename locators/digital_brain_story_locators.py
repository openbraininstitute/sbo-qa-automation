# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class DigitalBrainStoryLocators:
    # Hero section
    PAGE_TITLE = (By.XPATH, "//h1[contains(text(), 'Digital Brain') or contains(text(), 'Real Digital Brain')]")
    HERO_DESCRIPTION = (By.XPATH, "//div[contains(@class, 'Hero-module')]//div[contains(@class, 'content')] | //div["
                                  "contains(@class, 'Hero')]//div[contains(text(), 'research') or contains(text(), "
                                  "'simulation')]")
    HERO_IMAGE = (By.CSS_SELECTOR, "img[alt='Hero image'], .ProgressiveImage-module img, .Hero-module img")
    HERO_VIDEO = (By.CSS_SELECTOR, ".Hero-module video, video[src*='vimeo'], video[autoplay]")
    
    # Main content sections
    MAIN_SECTIONS = (By.XPATH, "//section | //div[contains(@class, 'section') or contains(@class, 'Section')]")
    SECTION_TITLES = (By.XPATH, "//h1 | //h2 | //h3[contains(@class, 'title') or contains(@class, 'Title')]")
    SECTION_TEXTS = (By.XPATH, "//p[contains(@class, 'text') or contains(@class, 'Text')] | //div[contains(@class, "
                               "'text') or contains(@class, 'Text')]")
    SECTION_IMAGES = (By.CSS_SELECTOR, "img[alt], img[src]")
    
    # Interactive elements
    NAVIGATION_LINKS = (By.XPATH, "//a[contains(@href, '/')]")
    BUTTONS = (By.XPATH, "//button | //a[contains(@class, 'button') or contains(@class, 'btn')]")
    
    # Specific content (to be updated after page inspection)
    STORY_TIMELINE = (By.XPATH, "//div[contains(@class, 'timeline') or contains(@class, 'Timeline')]")
    STORY_CHAPTERS = (By.XPATH, "//div[contains(@class, 'chapter') or contains(@class, 'Chapter')]")
    RESEARCH_HIGHLIGHTS = (By.XPATH, "//div[contains(@class, 'highlight') or contains(@class, 'Highlight')]")