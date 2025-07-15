# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By

class VLHomeLocators:
    ACCOUNT_PROFILE_BTN = (By.XPATH, "//a[@href='/app/virtual-lab/account/profile']")
    ACCOUNT_SUBSCRIPTIONS_BTN = (By.XPATH, "(//a[@href='/app/virtual-lab/account/subscription'])[2]")
    ACCOUNT_INVOICES_BTN = (By.XPATH, "//a[@href='/app/virtual-lab/account/invoices']")
    ADD_PROJECT_BTN = (By.XPATH, "//a[@href='/app/virtual-lab/project/create']")
    ADD_VLAB_BTN = (By.XPATH, "//a[@href='/app/virtual-lab/create']")
    BANNER_TITLE = (By.XPATH, "//h1[normalize-space()='Blue Brain Project']")
    BANNER_SUBTITLE = (By.XPATH, "//h2[normalize-space()='Virtual labs']")
    GO_TO_YOUR_VLAB = (By.XPATH, "//a[normalize-space()='Go to virtual lab']")
    HOME_BTN = (By.XPATH, "//a[@aria-label='home']")
    LOGOUT_BTN = (By.XPATH, "//a[@href='/app/log-out']")
    MENU_ABOUT_OBI_BTN = (By.XPATH, "//a[normalize-space()='About OBI']")
    MENU_CONTACT_OBI_BTN = (By.XPATH, "//a[normalize-space()='Contact support']")
    MENU_TERMS_BTN = (By.XPATH, "//a[normalize-space()='Terms and conditions']")
    NUM_MEMBERS = (By.XPATH, "//span[text()='Members:']/span[@class='ml-2 font-bold text-white']")
    NUM_PROJECTS = (By.XPATH, "//span[text()='Projects:']/span[@class='ml-2 font-bold text-white']")
    NUM_VLABS = (By.XPATH, "//a[@href='/app/virtual-lab' and text()='Virtual labs']")
    OTHER_VLABS = (By.XPATH, "//a[normalize-space()='Virtual lab memberships']")
    OUTSIDE_EXPLORE = (By.XPATH, "//h3[normalize-space()='Explore']")
    PROFILE_BTN = (By.XPATH, "(//button[@role='menuitem'])[2]")
    PUBLIC_PROJECTS = (By.XPATH, "//a[@href='/app/virtual-lab/public-projects']")
    QNA_BTN = (By.XPATH, "(//button[@role='menuitem'])[1]")
    TUTORIALS_CARDS = (By.XPATH, "//a[contains(@class, 'h-44') and starts-with(@href, '/app/documentation')]")
    TUTORIALS_CARROUSEL = (By.XPATH, "//div[starts-with(@class,'tutorials-carrousel')]")
    TUTORIALS_TITLE = (By.XPATH, "//h1[normalize-space()='Our tutorials']")
    USER_VLAB = (By.XPATH, "//a[normalize-space()='My virtual lab']")
