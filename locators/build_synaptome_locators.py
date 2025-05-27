# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By

class BuildSynaptomeLocators:
    MENU_BUILD = (By.XPATH, "//div[@class='mx-4' and text()='Build']")
    SYNAPTOME_BOX = (By.XPATH,"//div[@class='mb-5 mt-8 grid grid-cols-3 gap-5']//div[contains(text(),'Synaptome')]")
    SYNAPTOME_BUILD_BTN = (By.XPATH, "(//button[text()='Build'])")
    BUILD_SYNAPTOME_TAB = (By.XPATH, "//a[normalize-space()='Build Synaptome']")
    # INPUT_SYNAPTOME_NAME = (By.XPATH, "//input[@id='name']")
    # INPUT_SYNAPTOME_DESCRIPTION = (By.XPATH, "//textarea[@id='description']")
    # SAVE_SYNAPTOME_BTN = (By.XPATH, "//button[@title='Save Changes' and @type='submit']")
    # SYNAPTOME_MEMBER_ICON = (By.XPATH, "//div[@data-testid='virtual-lab-member-icon']")
    # ADD_MEMBER = (By.XPATH, "//div[text()='Add Member']")
    # SAVE_TXT = (By.XPATH, "//span[contains(text(), 'Save')]" )
    # SN = (By.XPATH, "//div[normalize-space()='Synaptome']")
