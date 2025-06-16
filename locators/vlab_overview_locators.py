# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By

class VLOverviewLocators:
    VLOVERVIEW_TITLE = (By.XPATH, "//div[normalize-space()='Virtual lab overview']")
    VL_BANNER = (By.XPATH, "//div[starts-with(@class,'virtual-lab-banner_bannerImg')]")
    VL_CREATE_PROJECT_BTN = (By.XPATH, "//button[@type='button']//h4[contains(text(), 'Create a project')]")
    VL_BANNER_NAME_LABEL = (By.XPATH, "//div[@class='text-primary-2' and contains(text(),'Virtual lab Name')]")
    VL_BANNER_NAME_VALUE = (By.XPATH, "//span[@data-testid='lab-detail-banner-name-element']")
    VL_BANNER_DESCRIPTION_VALUE = (By.XPATH, "//p[@data-testid='lab-detail-banner-description-element']")
    VL_BANNER_MEMBERS_LABEL = (By.XPATH, "//div[@class='text-primary-3'][normalize-space()='Members']")
    VL_BANNER_ADMIN_LABEL = (By.XPATH, "//div[@class='text-primary-3'][normalize-space()='Admin']")
    VL_BANNER_CREATION_DATE_LABEL = (By.XPATH, "//div[@class='text-primary-3'][normalize-space()='Creation date']")
    VL_BANNER_CREDIT_BALANCE_LABEL = (By.XPATH, "//div[@class='text-primary-3'][normalize-space()='Credit balance']")


    INPUT_PROJECT_NAME = (By.XPATH, "//input[@id='name']")
    INPUT_PROJECT_DESCRIPTION = (By.XPATH, "//textarea[@id='description']")
    SAVE_PROJECT_BTN = (By.XPATH, "//button[@title='Save Changes' and @type='submit']")
    PROJECT_MEMBER_ICON = (By.XPATH, "//div[@data-testid='virtual-lab-member-icon']")
    ADD_MEMBER = (By.XPATH, "//div[text()='Add Member']")
    SAVE_TXT = (By.XPATH, "//span[contains(text(), 'Save')]" )
    MENU_PROJECTS = (By.CSS_SELECTOR, "a[href='projects']")
    MENU_TEAM = (By.CSS_SELECTOR, "a[href='team']")
    MENU_ADMIN = (By.CSS_SELECTOR, "a[href='admin']")
