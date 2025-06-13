# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class ExploreEModelPageLocators:
    AI_ASSISTANT_PANEL = (By.XPATH, "//div[starts-with(@class,'ai-assistant_literatureSuggestions')]")
    AI_ASSISTANT_PANEL_CLOSE_BTN = (By.XPATH, "(//span[@aria-label='minus'])[2]")
    BRAIN_REGION_PANEL = (By.XPATH, "(//div[@class='flex h-screen flex-col bg-primary-8'])[1]")
    BR_SEARCH_FIELD_TYPE = (By.XPATH, "//span[@class='ant-select-selection-search']")
    BR_SEARCH_REGION_SEARCH_FIELD = (By.XPATH, "//div[@class='ant-select-selector']")
    BR_CEREBRUM_TITLE = (By.XPATH, "//button[starts-with(@class, 'flex h-auto "
                                   "items-center')]/span[contains(.,'Cerebrum')]")
    CLOSE_BRAIN_REGION_PANEL_BTN = (By.XPATH, "(//button[starts-with(@class, 'ant-btn')]/span["
                                              "@class='ant-btn-icon'])[1]")
    DV_ANALYSIS_TAB = (By.CSS_SELECTOR, "li[title='Analysis']")
    DV_CONFIGURATION_TAB = (By.CSS_SELECTOR, "li[title='Configuration']")
    DV_SIMULATION_TAB = (By.CSS_SELECTOR, "li[title='Simulation']")
    DV_EXEMPLAR_MORPHOLOGY_TITLE = (By.XPATH, "//div[normalize-space()='Exemplar morphology']")
    DV_NAME_LABEL = (By.XPATH, "//div[@class='text font-thin' and text()='Name']")
    DV_NAME_VALUE = (By.XPATH, "(//div[contains(@class,'text-2xl') and contains(@class,'font-bold')])[1]")
    DV_DESCRIPTION_LABEL = (By.XPATH, "//div[@class='uppercase text-neutral-4' and text()='Description']")
    DV_DESCRIPTION_VALUE = (
    By.XPATH, "//div[@class='uppercase text-neutral-4' and text()='Description']/following-sibling::div")

    DV_CONTRIBUTORS_LABEL = (By.XPATH, "//div[text()='Contributors']")
    DV_CONTRIBUTORS_VALUE = (By.XPATH, "//div[text()='Contributors']/following-sibling::div")

    DV_REGISTRATION_DATE_LABEL = (By.XPATH, "//div[text()='Registration date']")
    DV_REGISTRATION_DATE_VALUE = (By.XPATH, "//div[text()='Registration date']/following-sibling::div")

    DV_BRAIN_REGION_LABEL = (By.XPATH, "//div[text()='Brain Region']")
    DV_BRAIN_REGION_VALUE = (By.XPATH, "//div[text()='Brain Region']/following-sibling::div")

    DV_MODEL_SCORE_LABEL = (By.XPATH, "//div[text()='Model cumulated score']")
    DV_MODEL_SCORE_VALUE = (By.XPATH, "//div[text()='Model cumulated score']/following-sibling::div")

    DV_MTYPE_LABEL = (By.XPATH, "//div[text()='M-Type']")
    DV_MTYPE_VALUE = (By.XPATH, "//div[text()='M-Type']/following-sibling::div")

    DV_ETYPE_LABEL = (By.XPATH, "//div[text()='E-Type']")
    DV_ETYPE_VALUE = (By.XPATH, "//div[text()='E-Type']/following-sibling::div")

    DV_SIMULATION_PARAM_LABEL = (By.XPATH, "//div[normalize-space()='Simulation parameters']")
    DV_EXEMPLAR_TRACE_LABEL = (By.XPATH, "//div[normalize-space()='Exemplar Traces']")
    DV_OPTIMIZATION_TARGET_LABEL = (By.XPATH, "//div[normalize-space()='Optimization target']")
    DV_MECHANISMS_LABEL = (By.XPATH, "//div[normalize-space()='Mechanisms']")

    DV_MORPH_TABLE_HEADER_COLUMNS = (By.XPATH, "(//thead[@class='ant-table-thead'])[1]//th")
    DV_EXEMPLAR_TABLE_HEADER_COLUMNS = (By.XPATH, "(//thead[@class='ant-table-thead'])[2]//th")
    EMODEL_TAB = (By.XPATH, "//li[@title='E-model']")
    ME_MODEL_TAB = (By.XPATH, "//li[@title='ME-model']")
    SEARCH_REGION = (By.XPATH, "//input[@class='ant-select-selection-search-input']")
    SEARCH_RESOURCES = (By.CSS_SELECTOR, "input[placeholder='Search for resources...']")
    SELECTED_BRAIN_REGION = (By.XPATH, "//h1[@title='Isocortex']/span[text()='Isocortex']")
    LV_EM_TD = (By.XPATH, "(//td[@title='cADpyr'][normalize-space()='cADpyr'])[1]")