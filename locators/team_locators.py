# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class TeamLocators:
    # Page header
    PAGE_TITLE = (By.XPATH, "//h1[contains(text(), 'Team') or contains(text(), 'Our Team')]")
    PAGE_DESCRIPTION = (By.XPATH, "//div[contains(@class, 'Hero') or contains(@class, 'hero')]//p | //div[contains(@class, 'description')]")
    
    # Team member cards/profiles
    TEAM_MEMBER_CARDS = (By.CSS_SELECTOR, ".TeamMember-module__ZvVo3q__teamMember")
    MEMBER_NAMES = (By.CSS_SELECTOR, ".TeamMember-module__ZvVo3q__name")
    MEMBER_ROLES = (By.CSS_SELECTOR, ".TeamMember-module__ZvVo3q__profile")
    MEMBER_PHOTOS = (By.CSS_SELECTOR, ".TeamMember-module__ZvVo3q__ready")
    MEMBER_BIOS = (By.CSS_SELECTOR, ".Text-module__KTJYiG__text")
    
    # Social links
    SOCIAL_LINKS = (By.CSS_SELECTOR, ".social-media-links-module__xlL8Lq__socialMediaLinks a")
    LINKEDIN_LINKS = (By.XPATH, "//a[contains(@href, 'linkedin')]")
    TWITTER_LINKS = (By.XPATH, "//a[contains(@href, 'x.com') or contains(@href, 'twitter')]")
    YOUTUBE_LINKS = (By.XPATH, "//a[contains(@href, 'youtube')]")
    BLUESKY_LINKS = (By.XPATH, "//a[contains(@href, 'bsky')]")
    
    # Filter/search functionality (if present)
    SEARCH_INPUT = (By.XPATH, "//input[@type='search'] | //input[@placeholder*='search' or @placeholder*='Search']")
    FILTER_BUTTONS = (By.XPATH, "//button[contains(@class, 'filter')] | //div[contains(@class, 'filter')]//button")
    
    # Team sections (if organized by departments/roles)
    TEAM_SECTIONS = (By.CSS_SELECTOR, ".CompanyMembers-module__gpObla__people, .CompanyMembers-module__gpObla__board")
    SECTION_HEADERS = (By.XPATH, "//h2[contains(@class, 'section')] | //h3[contains(@class, 'department')]")