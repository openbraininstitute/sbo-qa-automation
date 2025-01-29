# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute

# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By

class VLOverviewLocators:
    VLOVERVIEW_TITLE = (By.XPATH, "//div[text()='Your virtual labs and projects']")
    # VL_NAME_TITLE = (By.XPATH, "div[contains(text(), 'Virtual lab Name')]")
    VL_BANNER = (By.XPATH, "(//span[@data-testid='dashboard-banner-name-element'])[1]")
    VL_CREATE_PROJECT_BTN = (By.XPATH, "//button[@type='button']//h4[contains(text(), 'Create a project')]")
    INPUT_PROJECT_NAME = (By.XPATH, "//input[@id='name']")
    INPUT_PROJECT_DESCRIPTION = (By.XPATH, "//textarea[@id='description']")
    SAVE_PROJECT_BTN = (By.XPATH, "//button[@title='Save Changes' and @type='submit']")
    PROJECT_MEMBER_ICON = (By.XPATH, "//div[@data-testid='virtual-lab-member-icon']")
    ADD_MEMBER = (By.XPATH, "//div[text()='Add Member']")
    SAVE_TXT = (By.XPATH, "//span[contains(text(), 'Save')]" )
