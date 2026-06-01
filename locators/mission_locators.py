# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0



from selenium.webdriver.common.by import By


class MissionLocators:
    BTN_DOWNLOAD_MISSION = (By.XPATH, "//a[contains(@class,'mission-statement-module') and contains(@class,'__missionStatement')]")
    MAIN_HERO_IMG = (By.CSS_SELECTOR, "img[alt='Hero image']")
    MAIN_HERO_VIDEO = (By.XPATH, "//div[contains(@class,'__hero')]//video")
    MISSION_PAGE_TITLE = (By.XPATH, "//div[contains(@class,'__hero')]//h1[text()='Mission']")
    MISSION_MAIN_TEXT = (By.XPATH, "//div[contains(@class,'__content') and contains(text(), 'The Open Brain Institute')]")
    MAIN_TITLES = (By.XPATH, "//h1[contains(@class,'blockSmall')]")
    MAIN_PAGE_PARAGRAPH = (By.XPATH, "(//div[contains(@class, 'text-module') and contains(@class, '__text')])[1]")
    MINOR_PAGE_PARAGRAPH = (By.XPATH, "(//div[contains(@class, 'text-module') and contains(@class, '__text')])[2]")
    MODELS_CARDS = (By.XPATH, "//div[contains(@class,'swipeable-cards-list')]")
    PLATFORM_SECTIONS = (By.XPATH, "//div[contains(@class, 'virtual-labs-panel-module') and contains(@class, '__triBlocks')]")
    PDF_NEW_TAB = (By.XPATH, "//a[contains(@href, '.pdf')]")
    P_SECTION_TITLES = (By.XPATH, "//ul[contains(@class,'sanity-content-items-module')]//li//h3")
    P_SECTION_TEXTS = (By.XPATH, "//ul[contains(@class,'sanity-content-items-module')]//li//div[last()]")
    P_SECTION_IMAGES = (By.XPATH, "//ul[contains(@class,'sanity-content-items-module')]//li//img")
    SUBSCRIBE_NEWSLETTER = (By.XPATH, "//h2[text()='Subscribe to our newsletter']")

    VLAB_CARDS_BTN = (By.XPATH, "//button[contains(@class,'card-module') and contains(@class,'__card')]")
    VIDEO1 = (By.XPATH, "(//div[contains(@class,'__triBlocks')]//video)[1]")
    VIDEO2 = (By.XPATH, "(//div[contains(@class,'__triBlocks')]//video)[2]")
    VIDEO3 = (By.XPATH, "(//div[contains(@class,'__triBlocks')]//video)[3]")
