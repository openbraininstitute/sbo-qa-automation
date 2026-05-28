# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0



from selenium.webdriver.common.by import By

class NewsLocators:
    # Hero section
    HERO_IMG = (By.CSS_SELECTOR, "img[alt='Hero image']")
    HERO_VIDEO = (By.XPATH, "//div[contains(@class,'__hero')]//video")
    HERO_TEXT = (By.XPATH, "//div[contains(@class,'__hero')]//div[contains(@class,'__content')]")
    HERO_MAIN_TITLE = (By.XPATH, "//div[contains(@class,'__hero')]//h1[text()='News']")

    # News cards
    PAGE_CARDS = (By.XPATH, "//div[contains(@class,'card-module') and contains(@class,'__card')]")
    CARD_MAIN_TITLE = (By.XPATH, "//div[contains(@class,'card-module') and contains(@class,'__card')]//h1")
    CARD_SUBTITLE = (By.XPATH, "//div[contains(@class,'card-module') and contains(@class,'__subtitle')]")
    CARD_TEXT = (By.XPATH, "//div[contains(@class,'card-module') and contains(@class,'__text')]")
    CARD_IMG = (By.XPATH, "//div[contains(@class,'card-module') and contains(@class,'__image')]")
    CARD_READ_MORE_BTN = (By.XPATH, "//a[contains(@class,'card-module') and contains(@class,'__button')]")

    # Load more button
    LOAD_MORE_BTN = (By.XPATH, "//button[contains(text(), 'Load')]")
