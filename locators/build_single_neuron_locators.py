# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By

class BuildSingleNeuronLocators:
    BRAIN_REGION_PANEL_TOGGLE = (By.XPATH, "(//span[@aria-label='minus'])[1]")
    BRAIN_REGION_DROPDOWN_CONTAINER = (By.CSS_SELECTOR, "div.rc-virtual-list-holder-inner")
    BRAIN_REGION_OPTIONS = (By.CSS_SELECTOR, "div.ant-select-item.ant-select-item-option")
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
    TICK_SEARCHED_M_RECORD = (By.XPATH, "//table[@id='data-table-with-filters']//tbody//tr[2]//span[@class='ant-radio-inner']")
    TICK_SEARCHED_E_RECORD = (By.XPATH, "//table[@id='data-table-with-filters']//tbody//tr[2]//span[@class='ant-radio-inner']")

    # Workflow Build Locators - moved from workflow_build_locators.py
    # Main workflow page - Build button to access workflow options
    BUILD_BUTTON = (By.XPATH, "//div[normalize-space()='Build']")
    
    # Build type selection
    SINGLE_NEURON_TYPE = (By.XPATH, "//div[contains(@class, 'build-type') or contains(@class, 'type-selection')]//button[contains(text(), 'Single neuron') or contains(text(), 'single neuron')]")
    SINGLE_NEURON_CARD = (By.XPATH, "//div[contains(@class, 'card') or contains(@class, 'option')]//h3[contains(text(), 'Single neuron')] | //div[contains(@class, 'card') or contains(@class, 'option')][.//text()[contains(., 'Single neuron')]]")
    
    # Configuration page elements - based on actual HTML
    MODEL_NAME_INPUT = (By.ID, "single-model-configuration-form_name")
    MODEL_NAME_INPUT_ALT = (By.XPATH, "//input[@placeholder='your model name']")
    MODEL_NAME_INPUT_FALLBACK = (By.XPATH, "//input[contains(@id, 'name') and @type='text']")
    
    # Description field (optional)
    DESCRIPTION_TEXTAREA = (By.ID, "single-model-configuration-form_description")
    DESCRIPTION_TEXTAREA_ALT = (By.XPATH, "//textarea[@placeholder='your description']")
    
    # M-model selection - based on actual HTML structure
    M_MODEL_BUTTON = (By.XPATH, "//button[.//div[contains(text(), 'M-model')]]")
    M_MODEL_BUTTON_ALT = (By.XPATH, "//button[contains(@class, 'group')]//div[text()='M-model']")
    M_MODEL_BUTTON_FALLBACK = (By.XPATH, "//div[text()='M-model']/ancestor::button")
    
    # E-model selection - based on actual HTML structure  
    E_MODEL_BUTTON = (By.XPATH, "//button[.//div[contains(text(), 'E-model')]]")
    E_MODEL_BUTTON_ALT = (By.XPATH, "//button[contains(@class, 'group')]//div[text()='E-model']")
    E_MODEL_BUTTON_FALLBACK = (By.XPATH, "//div[text()='E-model']/ancestor::button")
    
    # Build model button - based on actual HTML
    BUILD_MODEL_BUTTON = (By.XPATH, "//button[.//div[text()='Build model']]")
    BUILD_MODEL_BUTTON_ALT = (By.XPATH, "//button[contains(text(), 'Build model')]")
    BUILD_MODEL_BUTTON_DISABLED = (By.XPATH, "//button[@disabled][.//div[text()='Build model']]")
    
    # Configuration form and sections
    CONFIGURATION_FORM = (By.ID, "single-model-configuration-form")
    SETUP_SECTION = (By.XPATH, "//div[text()='Setup']")
    MODELING_SECTION = (By.XPATH, "//div[text()='Modeling']")
    
    # M-model and E-model table selectors (for when redirected to selection tables)
    M_MODEL_TABLE = (By.ID, "data-table-with-filters")
    M_MODEL_RADIO_BUTTON = (By.XPATH, "(//span[@class='ant-radio-inner'])[2]")
    FIRST_M_MODEL_RADIO = (By.XPATH, "//table[@id='data-table-with-filters']//tbody//tr[2]//input[@type='radio']")
    SECOND_M_MODEL_RADIO = (By.XPATH, "//table[@id='data-table-with-filters']//tbody//tr[3]//input[@type='radio']")
    
    E_MODEL_TABLE = (By.ID, "data-table-with-filters")
    E_MODEL_RADIO_BUTTON = (By.XPATH, "//table//input[@type='radio'][1] | //table//tr[position()>1][1]//input[@type='radio']")
    FIRST_E_MODEL_RADIO = (By.XPATH, "//table[@id='data-table-with-filters']//tbody//tr[2]//input[@type='radio']")
    SECOND_E_MODEL_RADIO = (By.XPATH, "//table[@id='data-table-with-filters']//tbody//tr[3]//input[@type='radio']")
    
    # Status indicators
    SELECT_M_MODEL_TEXT = (By.XPATH, "//div[text()='Select M-model']")
    SELECT_E_MODEL_TEXT = (By.XPATH, "//div[text()='Select E-model']")
    
    # Loading and success indicators
    LOADING_SPINNER = (By.XPATH, "//div[contains(@class, 'loading') or contains(@class, 'spinner')]")
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class, 'success') or contains(text(), 'successfully')]")
    
    # Navigation and page indicators
    CONFIGURATION_PANEL = (By.XPATH, "//button[text()='Configuration']")
    WORKFLOW_TITLE = (By.XPATH, "//h1[contains(text(), 'Workflow') or contains(text(), 'Build')]")
    
    # Warning indicators
    WARNING_ICON = (By.XPATH, "//span[@aria-label='warning']")



