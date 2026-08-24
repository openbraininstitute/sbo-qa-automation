# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class SimulateMeBetaLocators:
    """Locators for the ME-model picker page (single neuron beta simulation).

    URL pattern:
    /app/virtual-lab/{lab_id}/{project_id}/workflows/simulate/new/me-model-circuit-simulation
    """

    """Public / Project tabs on the model picker page."""
    PUBLIC_TAB = (By.XPATH, "//button[@role='tab'][.//span[contains(text(),'Public')] or text()='Public']")
    PROJECT_TAB = (By.XPATH, "//button[@role='tab'][.//span[contains(text(),'Project')] or text()='Project']")

    """Data table container wrappers."""
    DATA_TABLE_WITH_FILTERS = (By.CSS_SELECTOR, "#data-table-container-me_model_circuit")
    BASE_TABLE_WRAPPER = (By.CSS_SELECTOR, "#data-table-container-me_model_circuit")

    """Column headers in the model picker table (10 columns, AG Grid)."""
    COL_NAME = (By.CSS_SELECTOR, ".ag-header-cell[col-id='name']")
    COL_MORPHOLOGY = (By.CSS_SELECTOR, ".ag-header-cell[col-id='meModelMorphologyPreview']")
    COL_TRACE = (By.CSS_SELECTOR, ".ag-header-cell[col-id='meModelTracePreview']")
    COL_VALIDATED = (By.CSS_SELECTOR, ".ag-header-cell[col-id='validationStatus']")
    COL_BRAIN_REGION = (By.CSS_SELECTOR, ".ag-header-cell[col-id='brainRegion']")
    COL_SPECIES = (By.CSS_SELECTOR, ".ag-header-cell[col-id='species']")
    COL_MTYPE = (By.CSS_SELECTOR, ".ag-header-cell[col-id='mtype']")
    COL_ETYPE = (By.CSS_SELECTOR, ".ag-header-cell[col-id='etype']")
    COL_CREATED_BY = (By.CSS_SELECTOR, ".ag-header-cell[col-id='createdBy']")
    COL_REGISTRATION_DATE = (By.CSS_SELECTOR, ".ag-header-cell[col-id='registrationDate']")

    """Table rows and cells (AG Grid)."""
    TABLE_ROWS = (By.CSS_SELECTOR, ".ag-row[role='row']")
    TABLE_FIRST_ROW = (By.CSS_SELECTOR, ".ag-row[row-index='0']")
    TABLE_ROW_NAME_CELLS = (By.CSS_SELECTOR, ".ag-row[role='row'] .ag-cell[col-id='name']")
    COLUMN_HEADERS = (By.CSS_SELECTOR, ".ag-header-cell[role='columnheader']")

    """Filter panel: AG Grid column filter (Radix popover with checkboxes)."""
    FILTER_ETYPE_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Filter E-type']")
    FILTER_POPOVER_DIALOG = (By.CSS_SELECTOR, "[role='dialog'][data-state='open']")
    FILTER_POPOVER_CHECKBOX_LABELS = (By.CSS_SELECTOR, "[role='dialog'][data-state='open'] label.flex.cursor-pointer")
    FILTER_POPOVER_APPLY_BUTTON = (
        By.XPATH,
        "//div[@role='dialog'][@data-state='open']//button[.//text()='Apply']"
    )
    FILTER_POPOVER_RESET_BUTTON = (
        By.XPATH,
        "//div[@role='dialog'][@data-state='open']//button[.//text()='Reset']"
    )
    AG_GRID_LOADING_OVERLAY = (By.CSS_SELECTOR, ".ag-overlay-loading-wrapper")

    """Search bar."""
    SEARCH_BUTTON = (By.XPATH, "//button[@aria-label='Open search']")
    SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search for entities...']")

    """Pagination."""
    PAGINATION = (By.CSS_SELECTOR, "ul.ant-pagination")

    """Mini-detail view that appears after clicking a table row."""
    MINI_DETAIL_CONTAINER = (By.CSS_SELECTOR, "#mini-detail-view-container")
    MINI_VIEWER = (By.CSS_SELECTOR, "[data-testid='mini-viewer']")
    MINI_DETAIL_TITLE = (By.CSS_SELECTOR, "[data-testid='mini-viewer'] h1")
    MINI_DETAIL_DESCRIPTION = (By.CSS_SELECTOR, "#record-description")
    MINI_DETAIL_IMAGES = (By.CSS_SELECTOR, "[data-testid='mini-viewer'] img.ant-image-img")
    MINI_DETAIL_METADATA_LABELS = (
        By.CSS_SELECTOR,
        "[data-testid='mini-viewer'] .text-primary-3.text-base.font-light"
    )
    MINI_DETAIL_VIEW_DETAILS_BTN = (By.CSS_SELECTOR, "[data-testid='mini-viewer'] a[title='Go to details page']")
    MINI_DETAIL_USE_MODEL_BTN = (By.CSS_SELECTOR, "[data-testid='mini-viewer'] [title='Start simulation']")
    MINI_DETAIL_CLOSE_BTN = (By.CSS_SELECTOR, "[data-testid='mini-viewer'] button .anticon-close")

    """Config page layout, top-level tabs (Configuration / Simulations),
    left menu items, campaign name/description inputs, and 3D neuron visualizer."""
    CONFIG_LAYOUT = (
        By.CSS_SELECTOR,
        "button[data-scan-config-menu='left-menu-top-item'], [data-testid='workflow-simulate-layout']"
    )
    CONFIG_TAB_CONFIGURATION = (
        By.XPATH,
        "//button[@id='tab-configuration' or @aria-label='configuration']"
        " | //button[contains(translate(text(),'CONFIGURATION','configuration'),'configuration')]"
    )
    CONFIG_TAB_SIMULATIONS = (
        By.XPATH,
        "//button[@id='tab-simulations' or @aria-label='simulations']"
        " | //button[contains(translate(text(),'SIMULATIONS','simulations'),'simulations')]"
    )
    CONFIG_LEFT_MENU_ITEMS = (By.CSS_SELECTOR, "button[data-scan-config-menu='left-menu-top-item']")
    CONFIG_LEFT_MENU_INFO_ACTIVE = (
        By.CSS_SELECTOR,
        "button[data-scan-config-menu='left-menu-top-item'][data-active='true']"
    )
    CONFIG_CAMPAIGN_NAME_INPUT = (
        By.XPATH,
        "(//input[@data-scan-config-block-element='string_input'])[1]"
    )
    CONFIG_CAMPAIGN_DESC_INPUT = (
        By.XPATH,
        "(//input[@data-scan-config-block-element='string_input'])[2]"
    )
    NEURON_VISUALIZER = (
        By.CSS_SELECTOR,
        "div[class*='morpho-viewer-simul-module'], [data-testid='neuron-visualizer']"
    )
    NEURON_VISUALIZER_CANVAS = (
        By.CSS_SELECTOR,
        "div[class*='morpho-viewer-simul-module'] canvas, [data-testid='neuron-visualizer'] canvas"
    )

    """Initialization tab and its config block elements (labels, number inputs,
    plus-circle buttons for parameter sweep, sweep value inputs)."""
    CONFIG_INIT_TAB = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']//span[contains(text(),'Initialization')]/ancestor::button"
    )
    CONFIG_INIT_TAB_ACTIVE = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item'][@data-active='true']//span[contains(text(),'Initialization')]/ancestor::button"
    )
    CONFIG_BLOCK_LABELS = (
        By.CSS_SELECTOR,
        "div[data-scan-config-block-element] .text-primary-9.text-base.font-semibold"
    )
    CONFIG_BLOCK_ELEMENTS = (
        By.CSS_SELECTOR,
        "div[data-scan-config-block-element]"
    )
    CONFIG_NUMBER_INPUTS = (
        By.CSS_SELECTOR,
        "input.ant-input-number-input"
    )
    CONFIG_PLUS_CIRCLE_BTNS = (
        By.CSS_SELECTOR,
        "button[aria-label='Scan over several values'], button[aria-label='Add a value']"
    )
    CONFIG_SWEEP_INPUTS = (
        By.CSS_SELECTOR,
        "div[data-scan-config-block-element='float_parameter_sweep_multiple'] input.ant-input-number-input"
    )

    """Stimuli and Recordings tabs, sub-entry containers, add buttons, and sub-items."""
    CONFIG_STIMULI_TAB = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']//span[contains(text(),'Stimuli')]/ancestor::button"
    )
    CONFIG_STIMULI_TAB_ACTIVE = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item'][@data-active='true']//span[contains(text(),'Stimuli')]/ancestor::button"
    )
    CONFIG_RECORDINGS_TAB = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']//span[contains(text(),'Recordings')]/ancestor::button"
    )
    CONFIG_RECORDINGS_TAB_ACTIVE = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item'][@data-active='true']//span[contains(text(),'Recordings')]/ancestor::button"
    )
    CONFIG_STIMULI_SUB_ENTRY = (
        By.CSS_SELECTOR,
        "div[data-scan-config-menu*='menu-block-dictionary-sub-entry']"
    )
    CONFIG_STIMULI_ADD_BTN = (
        By.XPATH,
        "//div[contains(@data-scan-config-menu,'menu-block-dictionary-sub-entry')][@data-active='true']//button[.//span[contains(text(),'Add')]]"
    )
    CONFIG_STIMULI_SUB_ITEMS = (
        By.CSS_SELECTOR,
        "div[data-scan-config-menu*='menu-block-dictionary-sub-entry'] button[data-scan-config-menu='left-menu-sub-item']"
    )
    CONFIG_STIMULI_SUB_ITEMS_ACTIVE = (
        By.CSS_SELECTOR,
        "div[data-scan-config-menu*='menu-block-dictionary-sub-entry'] button[data-scan-config-menu='left-menu-sub-item'][data-active='true']"
    )

    """Neuronal manipulations tab."""
    CONFIG_NEURONAL_MANIP_TAB = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']//span[contains(text(),'Neuronal manipulations')]/ancestor::button"
    )
    CONFIG_NEURONAL_MANIP_TAB_ACTIVE = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item'][@data-active='true']//span[contains(text(),'Neuronal manipulations')]/ancestor::button"
    )

    """Dictionary block in the middle column: block_dictionary container,
    individual dictionary items, block_single form, and generic Add button."""
    CONFIG_BLOCK_DICTIONARY = (
        By.CSS_SELECTOR,
        "div[data-scan-config-block='block_dictionary']"
    )
    CONFIG_BLOCK_DICTIONARY_ITEMS = (
        By.CSS_SELECTOR,
        "button[data-scan-config-block-element-item='block_dictionary_item']"
    )
    CONFIG_BLOCK_SINGLE = (
        By.CSS_SELECTOR,
        "div[data-scan-config-block='block_single']"
    )
    CONFIG_ADD_BTN_IN_SUB_ENTRY = (
        By.XPATH,
        "//div[contains(@data-scan-config-menu,'menu-block-dictionary-sub-entry')][@data-active='true']//button[.//span[contains(text(),'Add')]]"
    )

    """Timestamps tab."""
    CONFIG_TIMESTAMPS_TAB = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']//span[contains(text(),'Timestamps')]/ancestor::button"
    )
    CONFIG_TIMESTAMPS_TAB_ACTIVE = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item'][@data-active='true']//span[contains(text(),'Timestamps')]/ancestor::button"
    )

    """Generate simulation button."""
    CONFIG_GENERATE_SIMULATION_BTN = (
        By.XPATH,
        "//button[.//div[contains(text(),'Generate simulation')]]"
    )

    """Reusable sub-element selectors used with parent.find_element() / find_elements()
    inside config blocks, sweep containers, and neuronal manipulation forms."""
    BLOCK_LABEL = (By.CSS_SELECTOR, ".text-primary-9.text-base.font-semibold")
    BLOCK_NUMBER_INPUT = (By.CSS_SELECTOR, "input.ant-input-number-input")
    BLOCK_SELECT_ITEM = (By.CSS_SELECTOR, ".ant-select-selection-item")
    BLOCK_STRING_INPUT = (By.CSS_SELECTOR, "input[data-scan-config-block-element='string_input']")
    BLOCK_PLUS_CIRCLE = (By.CSS_SELECTOR, "button[aria-label='Scan over several values'], button[aria-label='Add a value']")
    BLOCK_COMBOBOX_TRIGGER = (By.CSS_SELECTOR, "button[role='combobox']")
    BLOCK_VALUE_INPUT = (By.CSS_SELECTOR, "input[type='number'][placeholder='Enter value…']")
    WARNING_ICON = (By.CSS_SELECTOR, ".anticon-warning")
    METADATA_VALUE_BOLD = (By.CSS_SELECTOR, ".font-bold")

    """Neuronal manipulation variable select dropdown (radix combobox)."""
    SELECT_GROUP = (By.CSS_SELECTOR, "[data-slot='select-group']")
    SELECT_GROUP_BUTTON = (By.CSS_SELECTOR, "button")
    SELECT_ITEM = (By.CSS_SELECTOR, "[data-slot='select-item']")

    """Sweep containers inside block_single (used for timestamps)."""
    SWEEP_MULTIPLE = (By.CSS_SELECTOR, "div[data-scan-config-block-element='float_parameter_sweep_multiple']")
    SWEEP_SINGLE = (By.CSS_SELECTOR, "div[data-scan-config-block-element='float_parameter_sweep']")

    """Top navigation bar."""
    NAV_HOME = (By.CSS_SELECTOR, "#workspace-home")
    NAV_DATA = (By.CSS_SELECTOR, "#workspace-explore-data")
    NAV_WORKFLOWS = (By.CSS_SELECTOR, "#workspace-workflows")
    NAV_NOTEBOOKS = (By.CSS_SELECTOR, "#workspace-notebooks")
    NAV_REPORTS = (By.CSS_SELECTOR, "#workspace-reports")

    """Breadcrumbs."""
    BREADCRUMB_WORKFLOWS = (By.XPATH, "//a[contains(text(), 'Workflows') or contains(@href, 'workflows')]")

    """Simulations tab: simulation cards (left column), select-all checkbox,
    launch button, input files (middle column), and JSON preview (right column)."""
    SIM_SELECT_ALL_CHECKBOX = (
        By.XPATH,
        "//label[contains(@class,'ant-checkbox-wrapper')]//span[text()='Select all']/ancestor::label"
    )
    SIM_CARDS = (
        By.XPATH,
        "//button[@title[starts-with(.,'Simulation ')]]"
        " | //div[contains(@class,'rounded-lg')][.//button[contains(@title,'Simulation')]]"
    )
    SIM_CARD_STATUS_BADGE = (
        By.XPATH,
        ".//span[contains(@class,'rounded-xl') or contains(@class,'rounded-full')]"
        "[contains(@class,'border') and contains(@class,'px-4')]"
    )
    SIM_CARD_PARAM_LABELS = (By.XPATH, ".//div[contains(@class,'text-gray-400')]")
    SIM_CARD_PARAM_VALUES = (By.XPATH, ".//div[contains(@class,'font-bold') and contains(@class,'truncate')]")
    SIM_LAUNCH_BTN = (
        By.XPATH,
        "//button[.//span[contains(text(),'Launch simulations')]]"
    )
    SIM_COPY_CAMPAIGN_ID_BTN = (
        By.XPATH,
        "//button[@aria-label='Copy campaign ID']"
    )
    SIM_INPUT_FILES_HEADER = (By.XPATH, "//h4[contains(translate(text(),'INPUT FILES','input files'),'input files')]")
    SIM_INPUT_FILE_BUTTONS = (
        By.XPATH,
        "//button[@data-testid[starts-with(.,'task-io-file-item')]]"
        " | //h4[contains(translate(text(),'INPUT FILES','input files'),'input files')]"
        "/ancestor::div[contains(@class,'ant-collapse-item')]//button[@title]"
    )
    SIM_JSON_PREVIEW_CODE = (By.CSS_SELECTOR, "pre.shiki code")
    SIM_JSON_PREVIEW_COPY_BTN = (
        By.XPATH,
        "//div[contains(@class,'group')]//button[.//span[@aria-label='copy']]"
    )
