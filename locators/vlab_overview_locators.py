# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By

class VLOverviewLocators:
    ADD_MEMBER = (By.XPATH, "//div[text()='Add Member']")
    CREATE_PROJECT_BTN_BANNER = (By.XPATH, "//a[@type='button']//h4[contains(text(),'Create a project')]")
    CREATE_PROJECT_BTN = (By.XPATH, "//button[@type='submit']/span[contains(text(), 'Create project')]")
    INPUT_PROJECT_NAME = (By.XPATH, "//input[@id='project-creation-flow_name']")
    INPUT_PROJECT_DESCRIPTION = (By.XPATH, "//textarea[@id='project-creation-flow_description']")
    NAV_INFORMATION_BTN = (By.XPATH, "//button[@type='button' and @aria-label='Information']")
    NAV_MEMBERS_BTN = (By.CSS_SELECTOR, "button[aria-label='Members']")
    NEXT = (By.XPATH, "//button[@type='button']/span[contains(text(), 'Next')]")
    MEMBERS_SECTION_TITLE = (By.XPATH, "(//div[@class='flex flex-col'])[4]/div[text()='Members']")
    MEMBERS_SECTION_ADMIN_NAME = (By.XPATH, "(//div[text()='Admin']/following::div[@class='font-bold'])[2]")
    MENU_PROJECTS = (By.CSS_SELECTOR, "a[href='projects']")
    MENU_TEAM = (By.CSS_SELECTOR, "a[href='team']")
    MENU_ADMIN = (By.CSS_SELECTOR, "a[href='admin']")
    PROJECT_MEMBER_ICON = (By.XPATH, "//div[@data-testid='virtual-lab-member-icon']")
    PROJECT_CREATION_BACK_BTN = (By.XPATH, "//button[@type='button']/span[contains(text(), 'Back')]")
    SAVE_PROJECT_BTN = (By.XPATH, "//button[@title='Save Changes' and @type='submit']")
    SAVE_TXT = (By.XPATH, "//span[contains(text(), 'Save')]")
    VLOVERVIEW_TITLE = (By.XPATH, "//div[normalize-space()='Virtual lab overview']")
    VL_BANNER = (By.XPATH, "//div[starts-with(@class,'virtual-lab-banner_bannerImg')]")
    VL_BANNER_NAME_LABEL = (By.XPATH, "//div[@class='text-primary-2' and contains(text(),'Virtual lab Name')]")
    VL_BANNER_NAME_VALUE = (By.XPATH, "//span[@data-testid='lab-detail-banner-name-element']")
    VL_BANNER_DESCRIPTION_VALUE = (By.XPATH, "//p[@data-testid='lab-detail-banner-description-element']")
    VL_BANNER_MEMBERS_LABEL = (By.XPATH, "//div[@class='text-primary-3'][normalize-space()='Members']")
    VL_BANNER_ADMIN_LABEL = (By.XPATH, "//div[@class='text-primary-3'][normalize-space()='Admin']")
    VL_BANNER_CREATION_DATE_LABEL = (By.XPATH, "//div[@class='text-primary-3'][normalize-space()='Creation date']")
    VL_BANNER_CREDIT_BALANCE_LABEL = (By.XPATH, "//div[@class='text-primary-3'][normalize-space()='Credit balance']")
    # SAVE_TXT = (By.XPATH, "//span[contains(text(), 'Next')]" )
    FREE_PLAN_CREATE_PROJECT_BTN = (By.XPATH, "//button[@type='submit']/span[contains(text(), 'Create project')]")


