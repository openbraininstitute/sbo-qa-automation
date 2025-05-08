# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0



from selenium.webdriver.common.by import By


class AboutLocators:
    ABOUT_PAGE_TITLE = (By.XPATH, "//div[starts-with(@class,'Hero_text')]//h1[text()='About']")
    ABOUT_MAIN_TEXT = (By.XPATH, "//*[starts-with(@class,'Hero_content') and contains(text(), 'The Open Brain Institute')]")
    ABOUT_PAGE_BTNS = (By.XPATH, "//a[starts-with(@class,'OurFoundations_link')]")
    ABOUT_PORTALS_CARDS = (By.XPATH, "//a[starts-with(@class,'PortalCard_card')]")
    B_BTN = (By.XPATH, "//button[normalize-space()='B']")
    CONTRIBUTORS_PANEL = (By.XPATH, "//div[starts-with(@class,'ContributorsNavigation_pages')]")
    CONTRIBUTORS_LIST = (By.XPATH, "//div[starts-with(@class,'ContributorsList_contributorsList')]")
    CONTRIBUTORS_NAME = (By.XPATH, "//div[starts-with(@class,'ContributorsList_name')]")
    IMG_HERO = (By.CSS_SELECTOR, "img[alt='Hero image']")
    IMG_BACKGROUND = (By.CSS_SELECTOR, "img[alt='Background']")
    IMG_VIGNETTE = (By.XPATH, "(//img[@alt='Vignette'])")
    IMG1 = (By.CSS_SELECTOR, "img[alt='The Neocortical Microcircuit Collaboration Portal']")
    IMG2 = (By.CSS_SELECTOR, "img[alt='The Neuro-Glia-Vasculature Portal']")
    IMG3 = (By.CSS_SELECTOR, "img[alt='The Hippocampus Hub']")
    IMG4 = (By.CSS_SELECTOR, "img[alt='The Blue Brain Cell Atlas']")
    IMG5 = (By.CSS_SELECTOR, "img[alt='Channelpedia']")
    IMG6 = (By.CSS_SELECTOR, "img[alt='The SSCx Portal']")
    IMG7 = (By.CSS_SELECTOR, "img[alt='The Thalamus Studio']")
    IMG8 = (By.CSS_SELECTOR, "img[alt='The Hippocampus Hub']")
    LOAD_MORE_COLUMN = (By.XPATH, "//div[starts-with(@class,'CenteredColumn')]")
    LOAD_MORE_BTN = (By.XPATH, "//button[normalize-space()='Load more']")
    MAIN_HERO_VIDEO = (By.XPATH, "//video[starts-with(@class,'Hero_show')]")
    PARAGRAPH1 = (By.XPATH, "//div[starts-with(@class,'Text_text')]/p[contains(text(),'Founded in 2025')]")
    PARAGRAPH2 = (By.XPATH, "(//div[starts-with(@class,'Text_text') and contains(text(), 'Henry Markram is a')])")
    PARAGRAPH3 = (By.XPATH, "(//div[starts-with(@class,'Text_text')])[3]")
    PARAGRAPH4 = (By.XPATH, "(//div[starts-with(@class,'Text_text')])[4]")
    PARAGRAPH5 = (By.XPATH, "(//div[starts-with(@class,'Text_text')])[5]")
    PARAGRAPH6 = (By.XPATH, "(//div[starts-with(@class,'Text_text')])[6]")
    PORTALS_TITLES = (By.XPATH, ".//h2")
    PORTALS_CARDS_DESCRIPTION = (By.XPATH, "./div[2]")
    TITLE1 = (By.XPATH, "//h1[normalize-space()='2025: The Open Brain Institute']")
    TITLE2 = (By.XPATH, "//h1[normalize-space()='The Real Digital Brain Story']")
    TITLE3 = (By.XPATH, "//h1[normalize-space()='Our Foundations: Blue Brain']")
    TITLE4 = (By.XPATH, "//h1[normalize-space()='Browse our portals']")
    TITLE5 = (By.XPATH, "//h1[contains(text(),'We thank all Blue Brain collaborators and contribu')]")