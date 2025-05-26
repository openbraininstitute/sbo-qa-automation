# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By

class VLHomeLocators:
    USER_VLAB = (By.XPATH, "//a[normalize-space()='My virtual lab']")
    OTHER_VLABS = (By.XPATH, "//a[normalize-space()='Virtual lab memberships']")
    GO_TO_YOUR_VLAB = (By.XPATH, "//a[normalize-space()='Go to virtual lab']")
    NUM_PROJECTS = (By.XPATH, "//span[@class='text-base text-primary-2' and text()='Projects:']")
    NUM_MEMBERS = (By.XPATH, "//span[@class='text-base text-primary-2' and text()='Members:']")
    NUM_VLABS = (By.XPATH, "//a[@href='/app/virtual-lab' and text()='Virtual labs']")
    PUBLIC_PROJECTS = (By.XPATH, "//a[@href='/app/virtual-lab/public-projects' and text()='Public projects']")
    OUTSIDE_EXPLORE = (By.XPATH, "//h3[normalize-space()='Explore']")
    QNA_BTN  = (By.XPATH, "(//button[@role='menuitem'])[1]")
    PROFILE_BTN  = (By.XPATH, "(//button[@role='menuitem'])[2]")
    HOME_BTN = (By.XPATH, "//a[@aria-label='home']")
    MENU_ABOUT_OBI_BTN = (By.XPATH, "//a[@role='menuitem' and text()='About OBI']")
    MENU_CONTACT_OBI_BTN = (By.XPATH, "//a[@href='/contact']")
    MENU_TERMS_BTN = (By.XPATH, "//a[@href='/terms']")

