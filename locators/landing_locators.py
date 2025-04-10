# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0



from selenium.webdriver.common.by import By


class LandingLocators:
    BANNER_TITLE = (By.XPATH, "//h1[contains(text(),'Create your Virtual Lab to build digital brain mod')]")
    GOTO_LAB = (By.XPATH, "//*[contains(@class, 'Menu_loginButton__')]")
    PARA_TEXT = (By.XPATH, "//div[starts-with(@class, 'Text_text')]")
    P_TEXT1 = (By.XPATH, "(//div[@class='SanityContentPreview_text__ivnWe'])[1]")
    P_TEXT2 = (By.XPATH, "(//div[@class='SanityContentPreview_text__ivnWe'])[2]")
    P_TEXT3 = (By.XPATH, "(//div[@class='SanityContentPreview_text__ivnWe'])[3]")
    P_TEXT4 = (By.XPATH, "(//div[@class='SanityContentPreview_text__ivnWe'])[4]")
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


