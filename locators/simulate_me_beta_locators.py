# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class SimulateMeBetaLocators:
    """Locators for the ME-model picker page (single neuron beta simulation).

    URL pattern:
    /app/virtual-lab/{lab_id}/{project_id}/workflows/simulate/new/me-model-circuit-simulation
    """

    # ── Tabs: Public / Project ───────────────────────────────────────────
    PUBLIC_TAB = (By.XPATH, "//button[@role='tab' and text()='Public']")
    PROJECT_TAB = (By.XPATH, "//button[@role='tab' and text()='Project']")

    # ── Data table container ─────────────────────────────────────────────
    DATA_TABLE_WITH_FILTERS = (By.CSS_SELECTOR, "#data-table-with-filters")
    BASE_TABLE_WRAPPER = (By.CSS_SELECTOR, "#base-table-wrapper")

    # ── Column headers ───────────────────────────────────────────────────
    COL_NAME = (By.XPATH, "//th[@data-testid='column-header']//div[contains(@class,'columnTitle') and text()='Name']")
    COL_MORPHOLOGY = (By.XPATH, "//th[@data-testid='column-header']//div[contains(@class,'columnTitle') and text()='Morphology']")
    COL_TRACE = (By.XPATH, "//th[@data-testid='column-header']//div[contains(@class,'columnTitle') and text()='Trace']")
    COL_VALIDATED = (By.XPATH, "//th[@data-testid='column-header']//div[contains(@class,'columnTitle') and text()='Validated']")
    COL_BRAIN_REGION = (By.XPATH, "//th[@data-testid='column-header']//div[contains(@class,'columnTitle') and text()='Brain region']")
    COL_MTYPE = (By.XPATH, "//th[@data-testid='column-header']//div[contains(@class,'columnTitle') and text()='M-type']")
    COL_ETYPE = (By.XPATH, "//th[@data-testid='column-header']//div[contains(@class,'columnTitle') and text()='E-type']")
    COL_CREATED_BY = (By.XPATH, "//th[@data-testid='column-header']//div[contains(@class,'columnTitle') and text()='Created by']")
    COL_REGISTRATION_DATE = (By.XPATH, "//th[@data-testid='column-header']//div[contains(@class,'columnTitle') and text()='Registration date']")

    # ── Table rows / cells ───────────────────────────────────────────────
    TABLE_ROWS = (By.CSS_SELECTOR, "tbody.ant-table-tbody tr.ant-table-row")
    TABLE_FIRST_ROW = (By.CSS_SELECTOR, "tbody.ant-table-tbody tr.ant-table-row:first-child")
    TABLE_ROW_NAME_CELLS = (By.XPATH, "//tbody[@class='ant-table-tbody']//tr[contains(@class,'ant-table-row')]//td[1]")

    # ── Filter panel ─────────────────────────────────────────────────────
    FILTER_BUTTON = (By.XPATH, "//button[@aria-label='listing-view-filter-button']")
    FILTER_CLOSE_BUTTON = (By.XPATH, "//button[@aria-label='Close']")

    # E-type filter accordion trigger (inside filter panel)
    FILTER_ETYPE_TRIGGER = (
        By.XPATH,
        "//button[contains(@class,'accordionTrigger')]//span[text()='E-type']/parent::button"
    )
    FILTER_ETYPE_SEARCH_INPUT = (By.XPATH, "(//input[@class='ant-select-selection-search-input'])[last()]")
    FILTER_ETYPE_SEARCH_OVERFLOW = (By.XPATH, "//div[@class='ant-select-selection-overflow']")

    # Apply button inside filter panel
    FILTER_APPLY_BUTTON = (By.XPATH, "//button[@role='button']//span[text()='Apply']/parent::button")

    # ── Search ───────────────────────────────────────────────────────────
    SEARCH_BUTTON = (By.XPATH, "//button[@aria-label='Open search']")
    SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search for entities...']")

    # ── Pagination ───────────────────────────────────────────────────────
    PAGINATION = (By.CSS_SELECTOR, "ul.ant-pagination")

    # ── Mini-detail view (appears after clicking a row) ─────────────────
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
    MINI_DETAIL_USE_MODEL_BTN = (By.CSS_SELECTOR, "[data-testid='mini-viewer'] a[title='Start simulation']")
    MINI_DETAIL_CLOSE_BTN = (By.CSS_SELECTOR, "[data-testid='mini-viewer'] button .anticon-close")

    # ── Config page (after clicking "Use model") ─────────────────────────
    CONFIG_LAYOUT = (By.CSS_SELECTOR, "[data-testid='workflow-simulate-layout']")
    CONFIG_TAB_CONFIGURATION = (
        By.XPATH,
        "//div[@data-testid='workflow-simulate-layout']//button[contains(translate(text(),'CONFIGURATION','configuration'),'configuration')]"
    )
    CONFIG_TAB_SIMULATIONS = (
        By.XPATH,
        "//div[@data-testid='workflow-simulate-layout']//button[contains(translate(text(),'SIMULATIONS','simulations'),'simulations')]"
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
    NEURON_VISUALIZER = (By.CSS_SELECTOR, "[data-testid='neuron-visualizer']")
    NEURON_VISUALIZER_CANVAS = (By.CSS_SELECTOR, "[data-testid='neuron-visualizer'] canvas")

    # ── Config page: Initialization tab ─────────────────────────────────
    CONFIG_INIT_TAB = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']//span[contains(text(),'Initialization')]/ancestor::button"
    )
    CONFIG_INIT_TAB_ACTIVE = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item'][@data-active='true']//span[contains(text(),'Initialization')]/ancestor::button"
    )
    # Middle column: config block labels and values
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
    # Plus button to add parameter sweep values
    CONFIG_PLUS_CIRCLE_BTNS = (
        By.XPATH,
        "//span[@aria-label='plus-circle']"
    )
    # Sweep value inputs (inside float_parameter_sweep_multiple blocks)
    CONFIG_SWEEP_INPUTS = (
        By.CSS_SELECTOR,
        "div[data-scan-config-block-element='float_parameter_sweep_multiple'] input.ant-input-number-input"
    )

    # ── Config page: Stimuli & Recordings section ─────────────────────
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
    # Sub-entry container under Stimuli (holds "Add Stimulus" and any stimulus items)
    CONFIG_STIMULI_SUB_ENTRY = (
        By.CSS_SELECTOR,
        "div[data-scan-config-menu='menu-block-dictionary-sub-entry']"
    )
    # "Add Stimulus" button inside the sub-entry
    CONFIG_STIMULI_ADD_BTN = (
        By.XPATH,
        "//div[@data-scan-config-menu='menu-block-dictionary-sub-entry']//button[.//span[contains(text(),'Add')]]"
    )
    # Individual stimulus sub-items (appear after adding stimuli)
    CONFIG_STIMULI_SUB_ITEMS = (
        By.CSS_SELECTOR,
        "div[data-scan-config-menu='menu-block-dictionary-sub-entry'] button[data-scan-config-menu='left-menu-sub-item']"
    )
    CONFIG_STIMULI_SUB_ITEMS_ACTIVE = (
        By.CSS_SELECTOR,
        "div[data-scan-config-menu='menu-block-dictionary-sub-entry'] button[data-scan-config-menu='left-menu-sub-item'][data-active='true']"
    )

    # ── Config page: Neuronal manipulations tab ─────────────────────────
    CONFIG_NEURONAL_MANIP_TAB = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']//span[contains(text(),'Neuronal manipulations')]/ancestor::button"
    )
    CONFIG_NEURONAL_MANIP_TAB_ACTIVE = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item'][@data-active='true']//span[contains(text(),'Neuronal manipulations')]/ancestor::button"
    )

    # ── Dictionary block (middle column after clicking "Add X") ─────────
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

    # Generic "Add" button inside any active sub-entry
    CONFIG_ADD_BTN_IN_SUB_ENTRY = (
        By.XPATH,
        "//div[@data-scan-config-menu='menu-block-dictionary-sub-entry'][@data-active='true']//button[.//span[contains(text(),'Add')]]"
    )

    # ── Top navigation bar ───────────────────────────────────────────────
    NAV_HOME = (By.CSS_SELECTOR, "#workspace-home")
    NAV_DATA = (By.CSS_SELECTOR, "#workspace-explore-data")
    NAV_WORKFLOWS = (By.CSS_SELECTOR, "#workspace-workflows")
    NAV_NOTEBOOKS = (By.CSS_SELECTOR, "#workspace-notebooks")
    NAV_REPORTS = (By.CSS_SELECTOR, "#workspace-reports")

    # ── Breadcrumbs ──────────────────────────────────────────────────────
    BREADCRUMB_WORKFLOWS = (By.XPATH, "//a[contains(text(), 'Workflows') or contains(@href, 'workflows')]")
