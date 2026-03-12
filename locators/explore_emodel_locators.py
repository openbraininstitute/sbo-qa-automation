# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class ExploreEModelPageLocators:
    AI_ASSISTANT_PANEL = (By.XPATH, "//div[starts-with(@class,'ai-assistant-module')]")
    AI_ASSISTANT_PANEL_CLOSE_BTN = (By.XPATH, "(//span[@aria-label='minus'])[3]")
    BRAIN_REGION_PANEL = (By.CSS_SELECTOR, "#atlas-regions-selector")
    BR_SEARCH_FIELD_TYPE = (By.CSS_SELECTOR, "#region-search")
    BR_SEARCH_REGION_SEARCH_FIELD = (By.XPATH, "//div[@class='ant-select-selector']")
    BR_CEREBRUM_TITLE = (By.XPATH, "//span[normalize-space(text())='Cerebrum']")

    CLOSE_BRAIN_REGION_PANEL_BTN = (By.XPATH, "(//button[starts-with(@class, 'ant-btn')]/span["
                                              "@class='ant-btn-icon'])[1]")
    DV_ANALYSIS_TAB = (By.XPATH, "//a[normalize-space()='Analysis']")
    DV_BRAIN_REGION_LABEL = (By.XPATH, "//div[text()='Brain Region']")
    DV_BRAIN_REGION_VALUE = (By.XPATH, "//div[text()='Brain Region']/following-sibling::div")
    DV_CREATED_BY_LABEL = (By.XPATH, "//div[normalize-space()='Created by']")
    DV_CREATED_BY_VALUE = (By.XPATH, "//div[normalize-space()='Created by']/following-sibling::div")
    DV_CONFIGURATION_TAB = (By.XPATH, "//a[normalize-space()='Configuration']")
    DV_CONTRIBUTORS_LABEL = (By.XPATH, "//div[text()='Contributors']")
    DV_CONTRIBUTORS_VALUE = (By.XPATH, "//div[text()='Contributors']/following-sibling::div")
    DV_DESCRIPTION_LABEL = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Description']")
    DV_DESCRIPTION_VALUE = (
        By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Description']/following-sibling::div")
    DV_EXEMPLAR_TRACE_LABEL = (By.XPATH, "//div[normalize-space()='Exemplar Traces']")
    DV_ETYPE_LABEL = (By.XPATH, "//div[text()='E-Type']")
    DV_ETYPE_VALUE = (By.XPATH, "//div[text()='E-Type']/following-sibling::div")
    DV_EXEMPLAR_TABLE_HEADER_COLUMNS = (By.XPATH, "(//thead[@class='ant-table-thead'])[2]//th")
    DV_EXEMPLAR_MORPHOLOGY_TITLE = (By.XPATH, "//div[normalize-space()='Exemplar morphology']")
    DV_MECHANISMS_LABEL = (By.XPATH, "//div[normalize-space()='Mechanisms']")
    DV_MODEL_SCORE_LABEL = (By.XPATH, "//div[text()='Model cumulated score']")
    DV_MODEL_SCORE_VALUE = (By.XPATH, "//div[text()='Model cumulated score']/following-sibling::div")
    DV_MTYPE_LABEL = (By.XPATH, "//div[text()='M-Type']")
    DV_MTYPE_VALUE = (By.XPATH, "//div[text()='M-Type']/following-sibling::div")
    DV_MORPH_TABLE_HEADER_COLUMNS = (By.XPATH, "(//thead[@class='ant-table-thead'])[1]//th")
    DV_NAME_LABEL = (By.XPATH, "//div[@class='text font-thin' and text()='Name']")
    DV_NAME_VALUE = (By.XPATH, "(//div[contains(@class,'text-2xl') and contains(@class,'font-bold')])[1]")
    DV_OPTIMIZATION_TARGET_LABEL = (By.XPATH, "//div[normalize-space()='Optimization target']")
    DV_OVERVIEW_TAB = (By.XPATH, "//a[normalize-space()='Overview']")
    DV_REGISTRATION_DATE_LABEL = (By.XPATH, "//div[text()='Registration date']")
    DV_REGISTRATION_DATE_VALUE = (By.XPATH, "//div[text()='Registration date']/following-sibling::div")
    DV_SIMULATION_TAB = (By.CSS_SELECTOR, "#tab_simulation")
    DV_SIMULATION_PARAM_LABEL = (By.XPATH, "//div[normalize-space()='Simulation parameters']")
    DV_SPECIES_LABEL = (By.XPATH, "//div[normalize-space()='Species']")
    DV_SPECIES_VALUE = (By.XPATH, "//div[normalize-space()='Species']/following-sibling::div")
    EMODEL_TAB = (By.XPATH, "//div[normalize-space()='E-model']")
    FREE_TEXT_SEARCH = (By.CSS_SELECTOR, "button[aria-label='Open search']")
    INPUT_PLACEHOLDER = (By.CSS_SELECTOR, "input[placeholder='Search for entities...']")
    LV_EM_TD = (By.XPATH, "(//tr[starts-with(@class,'ant-table-row')]//td[starts-with(@class,'ant-table-cell')])[6]")
    LV_ROW = (By.CSS_SELECTOR, ".ant-table-body")
    ME_MODEL_TAB = (By.XPATH, "//li[@title='ME-model']")
    MINI_DETAIL_VIEW = (By.CSS_SELECTOR, "a[title='Go to details page']")
    MODEL_DATA_TAB = (By.XPATH, "//button[@role='tab' and text()='Model']")
    SEARCH_REGION = (By.XPATH, "//input[@class='ant-select-selection-search-input']")
    SEARCH_RESOURCES = (By.CSS_SELECTOR, "input[placeholder='Search for resources...']")
    SELECTED_BRAIN_REGION = (By.XPATH, "//div[@id='atlas-regions-selector']//span[contains(text(), 'Isocortex')]")
    SPINNER = (By.XPATH, "//div[@class='ant-spin ant-spin-spinning']")

