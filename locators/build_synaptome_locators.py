# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By

class BuildSynaptomeLocators:
    MENU_BUILD = (By.XPATH, "//div[@class='mx-4' and text()='Build']")
    SYNAPTOME_BOX = (By.XPATH,"//div[@class='mb-5 mt-8 grid grid-cols-3 gap-5']//div[contains(text(),'Synaptome')]")
    SYNAPTOME_BUILD_BTN = (By.XPATH, "(//button[text()='Build'])")
    BUILD_SYNAPTOME_TAB = (By.XPATH, "//a[normalize-space()='Build Synaptome']")
    SYNAPTOME_FORM = (By.CSS_SELECTOR, "#synaptome-model-configuration-form")
    NEW_SYNAPTOME_TITLE = (By.XPATH, "//h1[normalize-space()='Build new synaptome model']")
    NAME_TITLE = (By.CSS_SELECTOR, "//h1[normalize-space()='Build new synaptome model']")
    INPUT_NAME_FIELD = (By.CSS_SELECTOR, "#synaptome-model-configuration-form_name")
    DESCRIPTION_TITLE = (By.CSS_SELECTOR, "label[for='synaptome-model-configuration-form_description']")
    INPUT_DESCRIPTION_FIELD = (By.CSS_SELECTOR, "#synaptome-model-configuration-form_description")
    FORM_CREATED_BY = (By.XPATH, "//span[text()='created by']")
    FORM_VALUE_CREATED_BY = (By.XPATH, "//span[text()='created by']/following-sibling::div[normalize-space() != '']")
    FORM_CREATION_DATE = (By.XPATH, "//span[text()='creation date']")
    FORM_VALUE_CREATION_DATE = (By.XPATH, "//span[text()='creation date']/following-sibling::div[normalize-space() != '']")
    START_BUILDING_BTN = (By.XPATH, "(//button[normalize-space()='Start building'])[1]")
    SELECT_SINGLE_NEURON_MODEL_TITLE = (By.XPATH, "//h1[contains(text(),'Select a single neuron model to build a synaptome ')]")
    BRAIN_REGION_COLUMN_HEADER = (By.XPATH, "(//div[@class='ant-table-column-sorters'])[2]")
    ROW2 = (By.XPATH, "//tr[starts-with(@class,'ant-table-row ant-table-row-level-0')]")
    ROW1 = (By.XPATH, "//tr[position()=1]")
    TABLE_ROW = (By.XPATH, "//tr[starts-with(@class,'ant-table-row ant-table-row-level-0')]")
    TABLE = (By.XPATH, "//table[@aria-label='listing-view-table']")


