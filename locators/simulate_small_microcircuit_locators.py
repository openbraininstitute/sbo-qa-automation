# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class SimulateSmallMicrocircuitLocators:
    """Locators for the Small microcircuit (beta) simulation page.

    Entry point: Workflows page → Simulate category → Small microcircuit (beta) card
    URL pattern:
    /app/virtual-lab/{lab_id}/{project_id}/workflows/simulate/new/small-micro-circuit-simulation
    """

    """Workflows page: Simulate category card and Small microcircuit type card."""
    SIMULATE_CATEGORY_CARD = (
        By.XPATH,
        "(//div[@data-slot='card'])[2]"
    )
    SMALL_MICROCIRCUIT_CARD = (
        By.XPATH,
        "//div[@data-slot='card']//div[@data-slot='card-title'][contains(., 'Small microcircuit')]"
    )
    TYPE_CAROUSEL_NEXT_BTN = (
        By.XPATH,
        "//div[@id='workflow-types-menu-simulate']//button[.//span[@aria-label='right']]"
    )

    """Model picker: Public/Project tabs."""
    PUBLIC_TAB = (By.XPATH, "//button[@role='tab' and text()='Public']")
    PROJECT_TAB = (By.XPATH, "//button[@role='tab' and text()='Project']")

    """Column headers in the model picker table."""
    COLUMN_HEADERS = (By.CSS_SELECTOR, "th[data-testid='column-header']")

    """Table rows."""
    TABLE_ROWS = (By.CSS_SELECTOR, "tbody.ant-table-tbody tr.ant-table-row")

    """Pagination."""
    PAGINATION_CONTAINER = (By.CSS_SELECTOR, "ul.ant-pagination")
    PAGINATION_ITEMS = (By.CSS_SELECTOR, "li.ant-pagination-item")
    PAGINATION_ACTIVE_ITEM = (By.CSS_SELECTOR, "li.ant-pagination-item-active")

    """Mini-detail view after clicking a table row."""
    MINI_VIEWER = (By.CSS_SELECTOR, "[data-testid='mini-viewer']")
    MINI_DETAIL_TITLE = (By.CSS_SELECTOR, "[data-testid='mini-viewer'] h1")
    MINI_DETAIL_DESCRIPTION = (By.CSS_SELECTOR, "#record-description")
    MINI_DETAIL_USE_MODEL_BTN = (By.CSS_SELECTOR, "[data-testid='mini-viewer'] a[title='Start simulation']")

    """Config page layout and top-level tabs (Configuration / Results)."""
    CONFIG_LAYOUT = (By.CSS_SELECTOR, "button[data-scan-config-menu='left-menu-top-item']")
    CONFIG_TAB_CONFIGURATION = (
        By.XPATH,
        "//button[contains(translate(text(),'CONFIGURATION','configuration'),'configuration')]"
    )
    CONFIG_TAB_SIMULATIONS = (
        By.XPATH,
        "//button[contains(translate(text(),'SIMULATIONS','simulations'),'simulations')]"
    )
    CIRCUIT_PREVIEW_IMAGE = (By.CSS_SELECTOR, "div[class*='circuitPreview'] div[class*='zoomableImage']")

    """Left menu buttons (Setup and Experiment sections)."""
    LEFT_MENU_INFO_BTN = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']//span[contains(text(),'Info')]/ancestor::button"
    )
    LEFT_MENU_INITIALIZATION_BTN = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']//span[contains(text(),'Initialization')]/ancestor::button"
    )
    LEFT_MENU_STIMULI_BTN = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']//span[contains(text(),'Stimuli')]/ancestor::button"
    )
    LEFT_MENU_RECORDINGS_BTN = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']//span[contains(text(),'Recordings')]/ancestor::button"
    )
    LEFT_MENU_ACTIVE_BTN = (
        By.CSS_SELECTOR,
        "button[data-scan-config-menu='left-menu-top-item'][data-active='true']"
    )

    """Run experiment button (bottom of left menu)."""
    GENERATE_SIMULATION_BTN = (
        By.XPATH,
        "//button[.//div[contains(text(),'Generate simulation')]]"
    )

    """Info form fields (name, description, created by, registration date)."""
    FORM_NAME_INPUT = (
        By.XPATH,
        "(//input[@data-scan-config-block-element='string_input'])[1]"
    )
    FORM_DESCRIPTION_INPUT = (
        By.XPATH,
        "(//input[@data-scan-config-block-element='string_input'])[2]"
    )
    FORM_CREATED_BY = (
        By.XPATH,
        "//span[contains(translate(text(),'CREATED BY','created by'),'created by')]/ancestor::div[1]/following-sibling::div"
    )
    FORM_REGISTRATION_DATE = (
        By.XPATH,
        "//span[contains(translate(text(),'REGISTERED AT','registered at'),'registered at')]/ancestor::div[1]/following-sibling::div"
    )

    """Simulation panel (middle column content area)."""
    SIMULATION_PANEL = (By.CSS_SELECTOR, "[data-testid='memodel-simulation-panel']")

    """Experimental setup: labels in the panel."""
    PANEL_LABELS = (By.CSS_SELECTOR, "span.text-label")

    """Stimulation protocol: plot and download button."""
    STIM_PLOT_IMAGE = (
        By.XPATH,
        "//div[@id='memodel-simulation-panel']//img[contains(@alt,'plot') or contains(@alt,'IDrest')] "
        "| //div[@id='memodel-simulation-panel']//canvas "
        "| //div[@id='memodel-simulation-panel']//*[contains(@class,'plot')]"
    )
    STIM_DOWNLOAD_BTN = (
        By.XPATH,
        "//div[@id='memodel-simulation-panel']//button[.//span[@aria-label='download'] or contains(text(),'Download')]"
    )

    """Recording section: add recording button, section dropdown, dropdown options."""
    RECORDING_ADD_BTN = (
        By.XPATH,
        "//div[@id='memodel-simulation-panel']//button[contains(text(),'Add') or .//span[contains(text(),'Add')]]"
    )
    RECORDING_SECTION_DROPDOWN = (
        By.XPATH,
        "//div[contains(@id,'record_from')]//div[contains(@class,'ant-select')]"
    )
    RECORDING_DROPDOWN_OPTIONS = (
        By.CSS_SELECTOR,
        "div.ant-select-item.ant-select-item-option"
    )

    """Results tab: left menu buttons, Download CSV, Reconfigure, plots, canvas, notification."""
    RESULTS_LEFT_MENU_BUTTONS = (
        By.XPATH,
        "//div[@id='menu']//button[@data-slot='button']"
    )
    RESULTS_ALL_BTN = (
        By.XPATH,
        "//div[@id='menu']//button[.//div[text()='All']]"
    )
    RESULTS_RECORDING_BTNS = (
        By.XPATH,
        "//div[@id='menu']//button[.//div[contains(text(),'[') and contains(text(),'_')]]"
    )
    RESULTS_DOWNLOAD_CSV_BTN = (
        By.XPATH,
        "//div[@id='menu']//button[.//div[contains(text(),'Download')]]"
    )
    RESULTS_RECONFIGURE_BTN = (
        By.XPATH,
        "//div[@id='menu']//button[.//div[contains(text(),'Reconfigure')]]"
    )
    RESULTS_IDREST_PLOTS = (
        By.CSS_SELECTOR,
        "div.js-plotly-plot"
    )
    RESULTS_NEURON_CANVAS = (By.CSS_SELECTOR, "[data-testid='neuron-visualizer'] canvas")
    RESULTS_SUCCESS_NOTIFICATION = (
        By.CSS_SELECTOR,
        "div.ant-notification-notice-success"
    )
    RESULTS_VIEW_SIMULATION_LINK = (
        By.XPATH,
        "//div[contains(@class,'ant-notification-notice-success')]//a[contains(text(),'View Simulation')]"
    )

    """Beta config: additional left menu tabs (Circuit Components, Manipulations, Events)."""
    LEFT_MENU_NEURON_SETS_BTN = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']//span[contains(text(),'Neuron sets')]/ancestor::button"
    )
    LEFT_MENU_SYNAPTIC_MANIP_BTN = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']//span[contains(text(),'Synaptic manipulations')]/ancestor::button"
    )
    LEFT_MENU_TIMESTAMPS_BTN = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']//span[contains(text(),'Timestamps')]/ancestor::button"
    )

    """Config block elements (middle column)."""
    CONFIG_BLOCK_ELEMENTS = (By.CSS_SELECTOR, "div[data-scan-config-block-element]")
    BLOCK_LABEL = (By.CSS_SELECTOR, ".text-primary-9.text-base.font-semibold")
    BLOCK_NUMBER_INPUT = (By.CSS_SELECTOR, "input.ant-input-number-input")
    CONFIG_BLOCK_SINGLE = (By.CSS_SELECTOR, "div[data-scan-config-block='block_single']")
    WARNING_ICON = (By.CSS_SELECTOR, ".anticon-warning")
    CHECK_ICON = (By.CSS_SELECTOR, ".anticon-check-circle")

    """Dictionary items (for Stimuli/Recordings)."""
    CONFIG_BLOCK_DICTIONARY_ITEMS = (
        By.CSS_SELECTOR,
        "button[data-scan-config-block-element-item='block_dictionary_item']"
    )
    CONFIG_ADD_BTN_IN_SUB_ENTRY = (
        By.XPATH,
        "//div[@data-scan-config-menu='menu-block-dictionary-sub-entry'][@data-active='true']//button[.//span[contains(text(),'Add')]]"
    )
