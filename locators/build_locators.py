# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By

class BuildLocators:
    BRAIN_REGION_PANEL_TOGGLE = (By.XPATH, "(//span[@aria-label='minus'])[1]")
    BUILD_MENU_TITLE = (By.XPATH, "//div[@class='mx-4' and text()='Build']")
    BUILD_SINGLE_NEURON_BTN = (By.XPATH, "//div[@id='single-neuron']//span[contains(text(), 'Build')]")
    CREATED_BY_NAME = (By.XPATH, "//div[@class='font-bold']")
    CREATION_DATE_TITLE = (By.XPATH, "//span[normalize-space()='creation date']")
    DATE = (By.CSS_SELECTOR, "div[class='text-primary-8 font-bold']")
    FORM_BUILD_NEURON_TITLE = (By.XPATH, "//div[contains(text(), 'Build a new single neuron')]")
    FORM_NAME = (By.CSS_SELECTOR, "#single-model-configuration-form_name")
    FORM_DESCRIPTION = (By.CSS_SELECTOR, "#single-model-configuration-form_description")
    FORM_BRAIN_REGION = (By.XPATH, "//input[@id='single-model-configuration-form_brainRegion']")
    NEW_MODEL_TAB = (By.XPATH, "//label[@for='scope-filter-new']")
    SAVE = (By.XPATH, "//button[contains(.,'Save')]")
    SINGLE_NEURON_TITLE = (By.XPATH, "//div[text()='Single Neuron']")
    SELECT_M_MODEL_BTN = (By.XPATH, "//a[normalize-space()='Select m-model']")
    SELECT_SPECIFIC_M_MODEL_BTN = (By.XPATH, "//button[normalize-space()='Select m-model']")
    SELECT_E_MODEL_BTN = (By.XPATH, "//a[normalize-space()='Select e-model']")
    SELECT_SPECIFIC_E_MODEL_BTN = (By.XPATH, "//button[normalize-space()='Select e-model']")
    SEARCH_INPUT_FIELD = (By.XPATH, "//input[@placeholder='Search for resources...']")
    SEARCH_M_MODEL_NAME = (By.XPATH, "(//td[@title='C060114A5'])[1]")
    SEARCHED_M_RECORD = (By.XPATH, "(//td[@title='C060114A5'][normalize-space()='C060114A5'])[1]")
    SEARCHED_E_RECORD = (By.XPATH, "//td[@title='EM__1372346__cADpyr__13']")
    SN_NAME = (By.XPATH, "//div[contains(@class, 'text-neutral-4') and text()='name']/following-sibling::div/span")
    SN_DESCRIPTION = (By.XPATH, "//div[contains(@class, 'text-neutral-4') and text()='description']")
    SN_CREATED_BY = (
    By.XPATH, "//div[contains(@class, 'text-neutral-4') and text()='created date']/following-sibling::div")
    SN_CREATION_DATE = (
    By.XPATH, "//div[contains(@class, 'text-neutral-4') and text()='created by']/following-sibling::div/ul/li")
    SN_BRAIN_REGION = (
    By.XPATH, "//div[contains(@class, 'text-neutral-4') and text()='brain region']/following-sibling::div")
    SN_MTYPE = (By.XPATH, "//div[contains(@class, 'text-neutral-4') and text()='m-type']/following-sibling::div")
    SN_ETYPE = (By.XPATH, "//div[contains(@class, 'text-neutral-4') and text()='e-type']/following-sibling::div")
    START_BUILDING_BTN = (By.XPATH, "//button[normalize-space()='Start building']")
    TICK_SEARCHED_M_RECORD = (By.XPATH, "(//span[@class='ant-radio-inner'])[1]")
    TICK_SEARCHED_E_RECORD = (By.XPATH, "(//span[@class='ant-radio-inner'])[2]")



