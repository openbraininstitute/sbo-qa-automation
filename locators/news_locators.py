# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0



from selenium.webdriver.common.by import By

class NewsLocators:
    TITLE = (By.LINK_TEXT, "")
    HERO_IMG = (By.CSS_SELECTOR, "img[alt='Hero image']")
    HERO_VIDEO = (By.XPATH, "//video[starts-with(@class,'Hero_show')]")
    HERO_TEXT = (By.XPATH, "//div[starts-with(@class,'Hero_text')]")
    HERO_MAIN_TITLE = (By.XPATH, "//h1[normalize-space()='News']")
    PAGE_CARDS = (By.XPATH, "//div[starts-with(@class, 'Card_card')]")
    CARD_MAIN_TITLE = (By.XPATH, "//div[starts-with(@class, 'Card_card')]/h1")
    CARD_SUBTITLE = (By.XPATH, "//div[starts-with(@class, 'Card_subtitle')]")
    CARD_TEXT = (By.XPATH, "//div[starts-with(@class, 'Card_content')]/div[starts-with(@class,'Card_text')]")
    CARD_IMG = (By.XPATH, "//div[starts-with(@class, 'Card_content')]/div[starts-with(@class,'Card_image')]")
    CARD_READ_MORE_BTN = (By.XPATH, "//div[starts-with(@class,'Card_content')]//div[contains(text(), 'Read more')]")