# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By

class BuildIcLocators:
    """Locators for Ion Channel build workflow"""
    
    # Build section selectors
    BUILD_BUTTON = (By.XPATH, "//button[contains(text(), 'Build')]")
    BUILD_DIV = (By.XPATH, "//div[contains(text(), 'Build')]")
    BUILD_ANY = (By.XPATH, "//*[contains(text(), 'Build')]")
    BUILD_LINK = (By.XPATH, "//a[contains(text(), 'Build')]")
    BUILD_SPAN = (By.XPATH, "//span[contains(text(), 'Build')]")
    
    # Ion channel card selectors
    ION_CHANNEL_CARD_PRIMARY = (By.XPATH, "//div[@data-slot='card-title']//div[text()='Ion channel']")
    ION_CHANNEL_CARD_SUBTITLE = (By.XPATH, "//div[@data-slot='card-title']//div[text()='Subcellular']")
    ION_CHANNEL_CARD_COMBINED = (By.XPATH, "//div[@data-slot='card-title'][.//div[text()='Subcellular'] and .//div[text()='Ion channel']]")
    ION_CHANNEL_CARD_CLASS = (By.XPATH, "//div[contains(@class, 'card')]//div[text()='Ion channel']")
    ION_CHANNEL_CARD_TEXT = (By.XPATH, "//div[text()='Ion channel']")
    ION_CHANNEL_CARD_ANY = (By.XPATH, "//*[contains(text(), 'Ion channel')]")
    ION_CHANNEL_CARD_BUTTON = (By.XPATH, "//button[contains(text(), 'Ion channel')]")
    ION_CHANNEL_CARD_CASE_INSENSITIVE = (By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'ion channel')]")
    
    # Configuration form fields
    CONFIG_NAME_FIELD = (By.ID, "root_info_campaign_name")
    CONFIG_NAME_FIELD_ALT = (By.XPATH, "//input[@placeholder='Please enter a name']")
    CONFIG_NAME_FIELD_FALLBACK = (By.XPATH, "//input[contains(@id, 'campaign_name')]")
    CONFIG_DESCRIPTION_FIELD = (By.ID, "root_info_campaign_description")
    CONFIG_DESCRIPTION_FIELD_ALT = (By.XPATH, "//textarea[@placeholder='Please enter a description']")
    CONFIG_DESCRIPTION_FIELD_FALLBACK = (By.XPATH, "//textarea[contains(@id, 'campaign_description')]")
    CONFIG_CREATED_BY = (By.XPATH, "//span[text()='Created by ']/following-sibling::div")
    CONFIG_CREATED_AT = (By.XPATH, "//span[text()='created at ']/following-sibling::div")
    
    # Model selection buttons
    M_MODEL_BUTTON_PRIMARY = (By.XPATH, "//button[.//div[text()='M-model']]")
    M_MODEL_BUTTON_TEXT = (By.XPATH, "//button[contains(text(), 'M-model')]")
    M_MODEL_BUTTON_ANCESTOR = (By.XPATH, "//div[text()='M-model']/ancestor::button")
    M_MODEL_ANY = (By.XPATH, "//*[contains(text(), 'M-model')]")
    
    E_MODEL_BUTTON_PRIMARY = (By.XPATH, "//button[.//div[text()='E-model']]")
    E_MODEL_BUTTON_TEXT = (By.XPATH, "//button[contains(text(), 'E-model')]")
    E_MODEL_BUTTON_ANCESTOR = (By.XPATH, "//div[text()='E-model']/ancestor::button")
    E_MODEL_ANY = (By.XPATH, "//*[contains(text(), 'E-model')]")
    
    # Model selection table and radio buttons
    MODELS_TABLE = (By.XPATH, "//table")
    RADIO_BUTTON_ANT_INPUT = (By.XPATH, "//span[contains(@class, 'ant-radio')]//input[@class='ant-radio-input']")
    RADIO_BUTTON_INPUT_CLASS = (By.XPATH, "//input[@class='ant-radio-input']")
    RADIO_BUTTON_SPAN_TARGET = (By.XPATH, "//span[@class='ant-radio ant-wave-target']//input[@type='radio']")
    RADIO_BUTTON_SPAN_WRAPPER = (By.XPATH, "//span[contains(@class, 'ant-radio')]")
    RADIO_BUTTON_TABLE_FIRST = (By.XPATH, "//table//input[@type='radio'][1]")
    RADIO_BUTTON_ANY = (By.XPATH, "//input[@type='radio']")
    
    # Build button
    BUILD_ION_CHANNEL_BUTTON = (By.XPATH, "//button[contains(., 'Build ion channel')]")
    BUILD_MODEL_BUTTON = (By.XPATH, "//button[contains(., 'Build model')]")
    BUILD_BUTTON_PRIMARY = (By.XPATH, "//button[@type='submit' and contains(., 'Build')]")
    
    # Loading and status indicators
    LOADING_SPINNER = (By.XPATH, "//div[contains(@class, 'loading') or contains(@class, 'spinner')]")
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class, 'success') or contains(text(), 'successfully')]")
    
    # Initialization tab selectors
    INITIALIZATION_TAB_PRIMARY = (By.XPATH, "//button[@role='tab' and text()='Initialization']")
    INITIALIZATION_TAB_TEXT = (By.XPATH, "//button[text()='Initialization']")
    INITIALIZATION_TAB_CONTAINS = (By.XPATH, "//button[contains(text(), 'Initialization')]")
    INITIALIZATION_TAB_ANY = (By.XPATH, "//*[contains(text(), 'Initialization')]")
    
    # Info tab selectors
    INFO_TAB_PRIMARY = (By.XPATH, "//button[@role='tab' and text()='Info']")
    INFO_TAB_TEXT = (By.XPATH, "//button[text()='Info']")
    INFO_TAB_ANY = (By.XPATH, "//*[contains(text(), 'Info')]")
    
    # Ion channel recording selectors
    ION_CHANNEL_RECORDING_PRIMARY = (By.XPATH, "//button[.//div[text()='Ion channel recording']]")
    ION_CHANNEL_RECORDING_TEXT = (By.XPATH, "//button[contains(text(), 'Ion channel recording')]")
    ION_CHANNEL_RECORDING_DIV = (By.XPATH, "//div[text()='Ion channel recording']")
    ION_CHANNEL_RECORDING_ANCESTOR = (By.XPATH, "//div[text()='Ion channel recording']/ancestor::button")
    ION_CHANNEL_RECORDING_ANY = (By.XPATH, "//*[contains(text(), 'Ion channel recording')]")
    
    # Click to select recording button
    CLICK_TO_SELECT_RECORDING_PRIMARY = (By.XPATH, "//button[contains(text(), 'Click to select recording')]")
    CLICK_TO_SELECT_RECORDING_DIV = (By.XPATH, "//div[contains(text(), 'Click to select recording')]")
    CLICK_TO_SELECT_RECORDING_ANY = (By.XPATH, "//*[contains(text(), 'Click to select recording')]")
    CLICK_TO_SELECT_RECORDING_PLACEHOLDER = (By.XPATH, "//button[contains(@class, 'placeholder') or contains(., 'select recording')]")
    
    # Public tab selectors (for ion channel recordings list)
    PUBLIC_TAB_PRIMARY = (By.XPATH, "//button[@role='tab' and text()='Public']")
    PUBLIC_TAB_TEXT = (By.XPATH, "//button[text()='Public']")
    PUBLIC_TAB_ROLE = (By.XPATH, "//*[@role='tab'][contains(text(), 'Public')]")
    PUBLIC_TAB_ANY = (By.XPATH, "//*[contains(text(), 'Public')]")
    
    # Select button in modal footer (after selecting recording)
    SELECT_BUTTON_MODAL = (By.XPATH, "//div[@id='modal-footer']//button[contains(., 'Select')]")
    SELECT_BUTTON_PRIMARY = (By.XPATH, "//button[contains(., 'Select') and not(contains(., 'select recording'))]")
    SELECT_BUTTON_ANY = (By.XPATH, "//button[text()='Select']")
    
    # m∞ Equation selectors
    M_INFINITY_EQUATION_SECTION = (By.XPATH, "//button[contains(., 'm') and contains(., 'equation')]")
    M_INFINITY_EQUATION_TAB = (By.XPATH, "//button[@role='button' and contains(., 'equation')]")
    M_INFINITY_EQUATION_ACCORDION = (By.XPATH, "//button[.//span[contains(., 'equation')]]")
    SIGMOID_EQUATION_BUTTON = (By.XPATH, "//button[contains(., 'Sigmoid equation for')]")
    SIGMOID_EQUATION_M_INFINITY = (By.XPATH, "//button[contains(., 'Sigmoid equation') and contains(., 'm')]")
    SIGMOID_EQUATION_ANY = (By.XPATH, "//button[contains(., 'Sigmoid')]")
    
    # Navigation buttons for tabs
    NEXT_BUTTON = (By.XPATH, "//button[contains(., 'Next') or contains(@aria-label, 'next')]")
    NEXT_BUTTON_PRIMARY = (By.XPATH, "//button[@type='button' and contains(., 'Next')]")
    
    # Build model button (final step)
    BUILD_MODEL_BUTTON_FINAL = (By.XPATH, "//button[@type='submit' and contains(., 'Build model')]")
    BUILD_MODEL_BUTTON_ENABLED = (By.XPATH, "//button[@type='submit' and contains(., 'Build model') and not(@disabled)]")
    
    # Output tab and build completion selectors
    OUTPUT_TAB = (By.XPATH, "//button[@role='tab' and contains(text(), 'Output')]")
    OUTPUT_TAB_ACTIVE = (By.XPATH, "//button[@role='tab' and @data-state='active' and contains(text(), 'Output')]")
    
    # Build status badge
    BUILD_STATUS_DONE = (By.XPATH, "//div[@data-slot='badge' and contains(text(), 'done')]")
    BUILD_STATUS_RUNNING = (By.XPATH, "//div[@data-slot='badge' and contains(text(), 'running')]")
    
    # Output files
    OUTPUT_MOD_FILE = (By.XPATH, "//h3[contains(text(),'Outputs')]/following-sibling::div//button[.//div[@data-slot='badge' and contains(text(),'MOD')]]")
    OUTPUT_PDF_FILES = (By.XPATH, "//h3[contains(text(),'Outputs')]/following-sibling::div//button[.//div[@data-slot='badge' and contains(text(),'PDF')]]")
    OUTPUT_JSON_FILE = (By.XPATH, "//h3[contains(text(),'Outputs')]/following-sibling::div//button[.//div[@data-slot='badge' and contains(text(),'JSON')]]")
    OUTPUT_FILES_SECTION = (By.XPATH, "//h3[contains(text(), 'Outputs')]")
    OUTPUT_CODE_PREVIEW = (By.CSS_SELECTOR, "pre.shiki code")
    
    # Debug elements
    CLICKABLE_ELEMENTS = (By.XPATH, "//button | //a | //div[@role='button'] | //tr[@role='button'] | //td[@role='button']")
    TABLE_ROWS = (By.XPATH, "//tr")
