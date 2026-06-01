# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class TeamLocators:
    # Page header
    PAGE_TITLE = (By.XPATH, "//h1[normalize-space()='The team']")
    TEAM_PHOTO = (By.CSS_SELECTOR, "img[alt*='whole team']")
    
    # Team member cards/profiles
    TEAM_MEMBER_CARDS = (By.XPATH, "//div[contains(@class,'team-member-module') and contains(@class,'__teamMember')]")
    MEMBER_NAMES = (By.XPATH, "//div[contains(@class,'team-member-module') and contains(@class,'__name')]")
    MEMBER_ROLES = (By.XPATH, "//div[contains(@class,'team-member-module') and contains(@class,'__profile')]")
    MEMBER_PHOTOS = (By.XPATH, "//div[contains(@class,'team-member-module') and contains(@class,'__image')]//img")
    MEMBER_BIOS = (By.XPATH, "//div[contains(@class,'text-module') and contains(@class,'__text')]")
    
    # Social links (footer)
    SOCIAL_LINKS = (By.XPATH, "//div[contains(@class,'social-media-links-module') and contains(@class,'__socialMediaLinks')]//a")
    LINKEDIN_LINKS = (By.XPATH, "//a[contains(@href, 'linkedin')]")
    TWITTER_LINKS = (By.XPATH, "//a[contains(@href, 'x.com') or contains(@href, 'twitter')]")
    YOUTUBE_LINKS = (By.XPATH, "//a[contains(@href, 'youtube')]")
    BLUESKY_LINKS = (By.XPATH, "//a[contains(@href, 'bsky')]")
    
    # Team sections
    TEAM_SECTIONS = (By.XPATH, "//div[contains(@class,'company-members-module') and contains(@class,'__people')]")
    BOARD_SECTION = (By.XPATH, "//div[contains(@class,'company-members-module') and contains(@class,'__board')]")
