# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0



from selenium.webdriver.common.by import By

class NewsLocators:
    CARD_MAIN_TITLE = (By.XPATH, "//div[starts-with(@class,'Card-module__cjArhG__card')]/h1")
    CARD_SUBTITLE = (By.XPATH, "Card-module__cjArhG__subtitle")
    CARD_TEXT = (By.XPATH, "//div[starts-with(@class, 'Card-module__cjArhG__text')]")
    CARD_IMG = (By.XPATH, "//div[starts-with(@class, 'Card-module__cjArhG__image')]")
    CARD_READ_MORE_BTN = (By.XPATH, "//button[@type='button']/div[contains(text(), 'Read more')]")
    LOAD_MORE_BTN = (By.XPATH, "//button[contains(text(), 'Load')]")
    HERO_IMG = (By.CSS_SELECTOR, "img[alt='Hero image']")
    HERO_VIDEO = (By.CSS_SELECTOR, ".Hero-module__E0OG9W__show")
    HERO_TEXT = (By.CSS_SELECTOR, ".Hero-module__E0OG9W__content")
    HERO_MAIN_TITLE = (By.XPATH, "//h1[normalize-space()='News']")
    PAGE_CARDS = (By.XPATH, "//div[starts-with(@class, 'Card-module__cjArhG__card')]")
    TITLE = (By.LINK_TEXT, "")
