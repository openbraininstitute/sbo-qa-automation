# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0



from selenium.webdriver.common.by import By


class LandingLocators:
    BANNER_TITLE = (By.XPATH, "//h1[contains(text(),'Create your Virtual Lab to build digital brain mod')]")
    BIG_IMG1 = (By.XPATH, "(//div[starts-with(@class,'SanityContentPreview_vignette')])[1]")
    BIG_IMG2 = (By.XPATH, "(//div[starts-with(@class,'SanityContentPreview_vignette')])[2]")
    BIG_IMG3 = (By.XPATH, "(//div[starts-with(@class,'SanityContentPreview_vignette')])[3]")
    GOTO_LAB = (By.XPATH, "//a[@href='/app/virtual-lab']")
    PARA_TEXT = (By.XPATH, "//div[starts-with(@class, 'Text_text')]")
    P_TEXT1 = (By.XPATH, "(//div[@class='SanityContentPreview_text__ivnWe'])[1]")
    P_TEXT2 = (By.XPATH, "(//div[@class='SanityContentPreview_text__ivnWe'])[2]")
    P_TEXT3 = (By.XPATH, "(//div[@class='SanityContentPreview_text__ivnWe'])[3]")
    P_TEXT4 = (By.XPATH, "(//div[@class='SanityContentPreview_text__ivnWe'])[4]")
    SECTION_BTN1 = (By.XPATH, "(//button[starts-with(@class,'SanityContentPreview_button')])[1]")
    SECTION_BTN2 = (By.XPATH, "(//button[starts-with(@class,'SanityContentPreview_button')])[2]")
    SECTION_BTN3 = (By.XPATH, "(//button[starts-with(@class,'SanityContentPreview_button')])[3]")
    SECTION_BTN4 = (By.XPATH, "(//button[starts-with(@class,'SanityContentPreview_button')])[4]")
    SECTION_BTN5 = (By.XPATH, "(//button[starts-with(@class,'SanityContentPreview_button')])[5]")
    HORIZONTAL_CARDS_SECTION1 = (By.XPATH, "(//div[starts-with(@class,'swipeable-cards-list_scroll')])[1]")
    HORIZONTAL_CARDS_SECTION2 = (By.XPATH, "(//div[starts-with(@class,'swipeable-cards-list_scroll')])[2]")
    NEWS_CARD1 = (By.XPATH, "(//button[starts-with(@class,'NewsCard')])[1]")
    NEWS_CARD2 = (By.XPATH, "(//button[starts-with(@class,'NewsCard')])[2]")
    NEWS_CARD3 = (By.XPATH, "(//button[starts-with(@class,'NewsCard')])[3]")
    NEWS_CARD4 = (By.XPATH, "(//button[starts-with(@class,'NewsCard')])[4]")
    NEWS_CARD_CONTENT1 = (By.XPATH, "(//div[starts-with(@class,'NewsCard_content')])[1]")
    NEWS_CARD_CONTENT2 = (By.XPATH, "(//div[starts-with(@class,'NewsCard_content')])[2]")
    NEWS_CARD_CONTENT3 = (By.XPATH, "(//div[starts-with(@class,'NewsCard_content')])[3]")
    NEWS_CARD_CONTENT4 = (By.XPATH, "(//div[starts-with(@class,'NewsCard_content')])[4]")
    NEWS_CARD_PIC1 = (By.XPATH, "(//div[starts-with(@class,'NewsCard_picture')])[1]")
    NEWS_CARD_PIC2 = (By.XPATH, "(//div[starts-with(@class,'NewsCard_picture')])[2]")
    NEWS_CARD_PIC3 = (By.XPATH, "(//div[starts-with(@class,'NewsCard_picture')])[3]")
    NEWS_CARD_PIC4 = (By.XPATH, "(//div[starts-with(@class,'NewsCard_picture')])[4]")
    TITLE_ACCELERATE = (By.XPATH, "//h1[normalize-space()='Accelerating neuroscience research']")
    TITLE_RECONSTRUCT = (By.XPATH, "//h1[normalize-space()='Reconstructing digital brain models']")
    TITLE_WHO = (By.XPATH, "//h1[normalize-space()='Who is behind the Open Brain Institute']")
    TITLE_NEWS = (By.XPATH, "//h1[normalize-space()='News and events']")
    TOP_MENU = (By.CSS_SELECTOR, "(div[id='LandingPage/menu'])")
    TOP_ABOUT = (By.XPATH, "(//a[@href='/about'])[1]")
    TOP_MISSION = (By.XPATH, "(//a[@href='/mission'])[1]")
    TOP_NEWS = (By.XPATH, "(//a[@href='/news'])[1]")
    TOP_PRICING = (By.XPATH, "(//a[@href='/pricing'])[1]")
    TOP_TEAM = (By.XPATH, "(//a[@href='/team'])[1]")
    TOP_RESOURCES = (By.XPATH, "(//a[@href='/resources'])[1]")
    TOP_CONTACT = (By.XPATH, "(//a[@href='/contact'])[1]")
    TOP_MENU_LOGO = (By.XPATH, "//a[starts-with(@class,'Menu_logo')]")


