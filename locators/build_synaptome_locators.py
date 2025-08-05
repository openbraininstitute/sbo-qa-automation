# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By

class BuildSynaptomeLocators:
    ADD_RULE_BTN = (By.CSS_SELECTOR, "button[aria-label='Add new rule']")
    ADD_SYNAPSES_BTN = (By.CSS_SELECTOR, "button[aria-label='Add Synapse']")
    APPLY_CHANGES = (By.XPATH, "(//span[normalize-space()='Apply changes'])[1]")
    BRAIN_REGION_COLUMN_HEADER = (By.XPATH, "(//div[@class='ant-table-column-sorters'])[2]")
    BUILD_SYNAPTOME_TAB = (By.XPATH, "//a[normalize-space()='Build Synaptome']")
    CANVAS = (By.XPATH, "(//canvas)[1]")
    CANVAS_POINTER = (By.CSS_SELECTOR, ".pointer-events-none.absolute.top-0.left-0.size-full")
    CELLS = (By.XPATH, "//td[starts-with(@class,'ant-table-cell')]")
    CONFIGURE_MODEL = (By.XPATH, "//div[contains(text(),'configure model')]")
    DELETE_SYNAPSE_SET1 = (By.CSS_SELECTOR, "div[id='synaptic-input-0'] button[title='Delete Synapse']")
    DELETE_SYNAPSE_SET2 = (By.CSS_SELECTOR, "div[id='synaptic-input-1'] button[title='Delete Synapse']")
    DESCRIPTION_TITLE = (By.CSS_SELECTOR, "label[for='synaptome-model-configuration-form_description']")
    FILTER_SYNAPSES_BTN = (By.CSS_SELECTOR, "#exclusion-rules-header")
    FORM_CREATED_BY = (By.XPATH, "//span[text()='created by']")
    FORM_VALUE_CREATED_BY = (By.XPATH, "//span[text()='created by']/following-sibling::div[normalize-space() != '']")
    FORM_CREATION_DATE = (By.XPATH, "//span[text()='creation date']")
    FORM_VALUE_CREATION_DATE = (
    By.XPATH, "//span[text()='creation date']/following-sibling::div[normalize-space() != '']")
    INPUT_NAME_FIELD = (By.CSS_SELECTOR, "#synaptome-model-configuration-form_name")
    INPUT_DESCRIPTION_FIELD = (By.CSS_SELECTOR, "#synaptome-model-configuration-form_description")
    MENU_BUILD = (By.XPATH, "//div[@class='mx-4' and text()='Build']")
    NAME_TITLE = (By.CSS_SELECTOR, "//h1[normalize-space()='Build new synaptome model']")
    NAME_YOUR_SET_FIELD = (By.CSS_SELECTOR, "#synaptome-model-configuration-form_synapses_0_name")
    NAME_YOUR_SET_FIELD2 = (By.CSS_SELECTOR, "#synaptome-model-configuration-form_synapses_1_name")
    NEW_SYNAPTOME_TITLE = (By.XPATH, "//h1[normalize-space()='Build new synaptome model']")
    RADIO_BTN_ME_MODEL = (By.XPATH, "(//span[@class='ant-radio ant-wave-target'])[2]")
    RESULTS = (By.XPATH, "//div[@aria-label='listing-view-title']/span[contains(text(),'Results')]")
    ROW2 = (By.XPATH, "//tr[starts-with(@class,'ant-table-row ant-table-row-level-0')]")
    ROW1 = (By.XPATH, "//tr[starts-with(@class,'ant-table-row ant-table-row-level-0')]")
    ROWS = (By.CSS_SELECTOR, ".ant-table-tbody")
    SAVE_SYNAPTOME_MODEL = (By.CSS_SELECTOR, "button[type='submit']")
    SELECT_MODEL = (By.XPATH, "//h1[contains(text(),'Select a single neuron model to build a synaptome ')]")
    SELECT_SINGLE_NEURON_MODEL_TITLE = (
    By.XPATH, "//h1[contains(text(),'Select a single neuron model to build a synaptome ')]")
    SPIN_CONTAINER = (By.XPATH, "//div[starts-with(@class,'ant-spin-container ant-spin-blur')]")
    START_BUILDING_BTN = (By.XPATH, "(//button[normalize-space()='Start building'])[1]")
    SYNAPTOME_FORM = (By.CSS_SELECTOR, "#synaptome-model-configuration-form")
    SYNAPTOME_BOX = (By.XPATH, "//div[@id='synaptome']")
    SYNAPTOME_BUILD_BTN = (By.XPATH, "//div[@id='synaptome']//button[@type='button']/span[text()='Build']")
    SYNAPSE_GREATER_VALUE = (By.CSS_SELECTOR, "#synaptome-model-configuration-form_synapses_0_exclusion_rules_0_distance_soma_gte")
    SYNAPSE_SMALLER_VALUE = (By.CSS_SELECTOR,
                         "#synaptome-model-configuration-form_synapses_0_exclusion_rules_0_distance_soma_lte")
    SYNAPSE_SETS = (By.CSS_SELECTOR, "#synaptic-input-1")
    SYNAPSE_SET_NUM = (By.XPATH, "//span[text()='Synapses sets']/span")
    SYNAPSE_FORMULA = (By.CSS_SELECTOR, "#synaptome-model-configuration-form_synapses_0_formula")
    TARGET_DROPDOWN_LIST = (By.CSS_SELECTOR, "div.rc-virtual-list-holder-inner")
    TARGET_FIELD = (By.XPATH, "(//span[@class='ant-select-selection-search'])[1]")
    TARGET_FIELD2 = (By.XPATH, "(//span[@class='ant-select-selection-search'])[3]")
    TARGET_INPUT = (By.ID, "synaptome-model-configuration-form_synapses_0_target")
    TARGET_INPUT2 = (By.ID, "synaptome-model-configuration-form_synapses_1_target")
    TARGET_SELECTOR = (
        By.XPATH,
        "//input[@id='synaptome-model-configuration-form_synapses_0_target']/ancestor::div[contains(@class, 'ant-select')]/div[contains(@class, 'ant-select-selector')]"
    )
    TARGET_SELECT2 = (By.CSS_SELECTOR, "#synaptome-model-configuration-form_synapses_1_target")
    TARGET_LIST = (By.XPATH, "//div[@class='rc-virtual-list']")
    TARGET_LIST2 = (By.CSS_SELECTOR, "div.ant-select-dropdown:not(.ant-select-dropdown-hidden)")


    TARGET_SOMA = (By.XPATH, "//div[@class='ant-select-item-option-content' and text()='Soma']")
    TARGET_SOMA2 = (
    By.XPATH, "//div[contains(@class, 'ant-select-dropdown') and not(contains(@class,'hidden'))]//div[text()='Soma']")

    TABLE_ROW = (By.XPATH, "//tr[starts-with(@class,'ant-table-row ant-table-row-level-0')]")
    TABLE = (By.CSS_SELECTOR, ".ant-table-tbody")
    TYPE_FIELD = (By.XPATH, "(//span[@class='ant-select-selection-wrap'])[2]")
    TYPE_FIELD2 = (By.CSS_SELECTOR, "span[title='Inhibitory Synapses']")
    TYPE_EXCITATORY = (By.CSS_SELECTOR, "div[title='Excitatory Synapses']")
    TYPE_INHIBITORY = (By.XPATH, "(//span[@title='Excitatory Synapses'][normalize-space()='Excitatory Synapses'])[2]")
    SELECT_INHIBITORY = (By.XPATH, "(//div[@class='ant-select-item-option-content'][normalize-space()='Inhibitory "
                              "Synapses'])[2]")
    USE_SN_MODEL_BTN = (By.XPATH, "//button[text()='Use single neuron model']")


