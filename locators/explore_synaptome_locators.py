# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class ExploreSynaptomePageLocators:
    # Brain region panel
    BRAIN_REGION_PANEL = (By.CSS_SELECTOR, "#atlas-regions-selector")
    BR_CEREBRUM_TITLE = (By.XPATH, "//span[normalize-space(text())='Cerebrum']")
    BR_SEARCH_FIELD = (By.CSS_SELECTOR, "#region-search")
    SELECTED_BRAIN_REGION = (By.XPATH, "//button[@id='5c60bf3e-5335-4971-a8ec-6597292452b2']")
    
    # Data type selector
    MODEL_DATA_TAB = (By.XPATH, "//button[@role='tab' and text()='Model']")
    PROJECT_TAB = (By.XPATH, "//button[.='Project']")
    SYNAPTOME_BUTTON = (By.CSS_SELECTOR, "#counter-single_neuron_synaptome")
    
    # Search
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Open search']")
    INPUT_PLACEHOLDER = (By.CSS_SELECTOR, "input[placeholder='Search for entities...']")
    
    # Table
    LV_ROW = (By.CSS_SELECTOR, ".ant-table-body")
    LV_FIRST_ROW = (By.XPATH, "//tr[@data-row-key][1]")
    LV_FIRST_ROW_CELL = (By.XPATH, "//tr[@data-row-key][1]//td[2]")  # Click on the name cell
    
    # Detail view
    MINI_DETAIL_VIEW = (By.CSS_SELECTOR, "a[title='Go to details page']")
    
    # Detail view labels and values
    DV_DESCRIPTION_LABEL = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Description']")
    DV_DESCRIPTION_VALUE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Description']/following-sibling::div")
    DV_ME_MODEL_LABEL = (By.XPATH, "//div[text()='ME-model']")
    DV_ME_MODEL_VALUE = (By.XPATH, "//div[text()='ME-model']/following-sibling::div")
    DV_MTYPE_LABEL = (By.XPATH, "//div[text()='M-Type']")
    DV_MTYPE_VALUE = (By.XPATH, "//div[text()='M-Type']/following-sibling::div")
    DV_ETYPE_LABEL = (By.XPATH, "//div[text()='E-Type']")
    DV_ETYPE_VALUE = (By.XPATH, "//div[text()='E-Type']/following-sibling::div")
    DV_BRAIN_REGION_LABEL = (By.XPATH, "//div[text()='Brain Region']")
    DV_BRAIN_REGION_VALUE = (By.XPATH, "//div[text()='Brain Region']/following-sibling::div")
    DV_CREATED_BY_LABEL = (By.XPATH, "//div[normalize-space()='Created by']")
    DV_CREATED_BY_VALUE = (By.XPATH, "//div[normalize-space()='Created by']/following-sibling::div")
    DV_REGISTRATION_DATE_LABEL = (By.XPATH, "//div[text()='Registration date']")
    DV_REGISTRATION_DATE_VALUE = (By.XPATH, "//div[text()='Registration date']/following-sibling::div")
    
    # Tabs
    DV_OVERVIEW_TAB = (By.XPATH, "//a[normalize-space()='Overview']")
    
    # Spinner
    SPINNER = (By.XPATH, "//div[@class='ant-spin ant-spin-spinning']")
