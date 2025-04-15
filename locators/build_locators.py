# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By

class BuildLocators:
    BRAIN_REGION_PANEL_TOGGLE = (By.XPATH, "(//span[@aria-label='minus'])[1]")
    BUILD_MENU_TITLE = (By.XPATH, "//div[@class='mx-4' and text()='Build']")
    NEW_MODEL_TAB = (By.XPATH, "//label[@for='scope-filter-new']")
    SINGLE_NEURON_TITLE = (By.XPATH, "//div[text()='Single neuron']")
    BUILD_SINGLE_NEURON_BTN = (By.XPATH, "//button[@type='button' and contains(text(), 'Build')]")
    FORM_BUILD_NEURON_TITLE = (By.XPATH, "//div[contains(text(), 'Build a new single neuron')]")
    FORM_NAME = (By.XPATH, "//input[@id='name']")
    FORM_DESCRIPTION = (By.XPATH, "//textarea[@id='description']")
    FORM_BRAIN_REGION = (By.XPATH, "//input[@id='brainRegion']")
    START_BUILDING_BTN = (By.XPATH, "//button[@type='submit']/span[text()='Start building']")
    CREATED_BY_NAME = (By.XPATH, "//div[contains(text(), 'Created by')]/following-sibling::div/ul/li")
    CREATION_DATE = (By.XPATH, "//div[contains(text(), 'Creation Date')]")
    DATE = (By.XPATH, "//div[contains(text(), 'Creation Date')]/following-sibling::div")
    SN_NAME = (By.XPATH, "//div[contains(@class, 'text-neutral-4') and text()='name']/following-sibling::div/span")
    SN_DESCRIPTION = (By.XPATH, "//div[contains(@class, 'text-neutral-4') and text()='description']")
    SN_CREATED_BY = (By.XPATH, "//div[contains(@class, 'text-neutral-4') and text()='created date']/following-sibling::div")
    SN_CREATION_DATE = (By.XPATH, "//div[contains(@class, 'text-neutral-4') and text()='created by']/following-sibling::div/ul/li")
    SN_BRAIN_REGION = (By.XPATH, "//div[contains(@class, 'text-neutral-4') and text()='brain region']/following-sibling::div")
    SN_MTYPE = (By.XPATH, "//div[contains(@class, 'text-neutral-4') and text()='m-type']/following-sibling::div")
    SN_ETYPE = (By.XPATH, "//div[contains(@class, 'text-neutral-4') and text()='e-type']/following-sibling::div")
    SELECT_M_MODEL_BTN = (By.XPATH, "(//button[normalize-space()='Select m-model'])[1]")
    SELECT_E_MODEL_BTN = (By.XPATH, "(//button[normalize-space()='Select e-model'])[1]")
    SEARCH_INPUT_FIELD = (By.XPATH, "//input[@placeholder='Search for resources...']")
    SEARCH_M_MODEL_NAME = (By.XPATH, "(//td[@title='C060114A5'])[1]")
    SEARCHED_M_RECORD = (By.XPATH, "(//td[@title='C060114A5'][normalize-space()='C060114A5'])[1]")
    SEARCHED_E_RECORD = (By.XPATH, "//td[@title='EM__1372346__cADpyr__13']")
    TICK_SEARCHED_M_RECORD = (By.XPATH, "(//span[@class='ant-radio-inner'])[1]")
    TICK_SEARCHED_E_RECORD = (By.XPATH, "(//span[@class='ant-radio-inner'])[2]")

    SAVE = (By.XPATH, "//button[text()='Save']")


