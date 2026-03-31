# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class SimulateMemLocators:
    """Locators for the ME-model simulation page (non-beta single neuron).

    Entry point: Workflows page → Simulate category → Single neuron card
    URL pattern:
    /app/virtual-lab/{lab_id}/{project_id}/workflows?activity=simulate
    """

    """Workflows page: Simulate category card and Single neuron type card."""
    SIMULATE_CATEGORY_CARD = (
        By.XPATH,
        "(//div[@data-slot='card'])[2]"
    )
    SINGLE_NEURON_CARD = (
        By.XPATH,
        "//div[@data-slot='card']//div[@data-slot='card-title'][contains(., 'Single neuron') and not(contains(., 'beta'))]"
    )

    """Model picker: Public/Project tabs."""
    PUBLIC_TAB = (By.XPATH, "//button[@role='tab' and text()='Public']")
    PROJECT_TAB = (By.XPATH, "//button[@role='tab' and text()='Project']")

    """Column headers in the model picker table."""
    COLUMN_HEADERS = (By.CSS_SELECTOR, "th[data-testid='column-header']")

    """Table rows."""
    TABLE_ROWS = (By.CSS_SELECTOR, "tbody.ant-table-tbody tr.ant-table-row")

    """Mini-detail view after clicking a table row."""
    MINI_VIEWER = (By.CSS_SELECTOR, "[data-testid='mini-viewer']")
    MINI_DETAIL_TITLE = (By.CSS_SELECTOR, "[data-testid='mini-viewer'] h1")
    MINI_DETAIL_USE_MODEL_BTN = (By.CSS_SELECTOR, "[data-testid='mini-viewer'] a[title='Start simulation']")

    """Config page layout and top-level radix tabs (Configuration / Results)."""
    CONFIG_LAYOUT = (By.CSS_SELECTOR, "[data-testid='workflow-simulate-layout']")
    CONFIG_TAB_CONFIGURATION = (
        By.XPATH,
        "//button[@role='tab' and contains(text(),'Configuration')]"
    )
    CONFIG_TAB_RESULTS = (
        By.XPATH,
        "//button[@role='tab' and contains(text(),'Results')]"
    )
    NEURON_VISUALIZER_CANVAS = (By.CSS_SELECTOR, "[data-testid='neuron-visualizer'] canvas")

    """Left menu buttons (Setup and Experiment sections)."""
    LEFT_MENU_INFO_BTN = (
        By.XPATH,
        "//div[@id='menu']//button[.//div[contains(text(),'Info')]]"
    )
    LEFT_MENU_EXPERIMENTAL_SETUP_BTN = (
        By.XPATH,
        "//div[@id='menu']//button[.//div[contains(text(),'Experimental setup')]]"
    )
    LEFT_MENU_STIMULATION_PROTOCOL_BTN = (
        By.XPATH,
        "//div[@id='menu']//button[.//div[contains(text(),'Stimulation protocol')]]"
    )
    LEFT_MENU_RECORDING_BTN = (
        By.XPATH,
        "//div[@id='menu']//button[.//div[contains(text(),'Recording')]]"
    )
    LEFT_MENU_ACTIVE_BTN = (
        By.XPATH,
        "//div[@id='menu']//button[contains(@class,'bg-primary-9') and contains(@class,'text-white')]"
    )
    LEFT_MENU_WARNING_ICON = (By.CSS_SELECTOR, ".anticon-warning")

    """Run experiment button (bottom of left menu)."""
    RUN_EXPERIMENT_BTN = (
        By.XPATH,
        "//div[@id='menu']//button[.//div[contains(text(),'Run experiment')]]"
    )

    """Info form fields (name, description)."""
    FORM_NAME_INPUT = (
        By.CSS_SELECTOR,
        "#single-model-configuration-form_name"
    )
    FORM_DESCRIPTION_INPUT = (
        By.CSS_SELECTOR,
        "#single-model-configuration-form_description"
    )
    FORM_REGISTERED_BY = (
        By.XPATH,
        "//span[contains(translate(text(),'CREATED BY','created by'),'created by')]/ancestor::div[1]/following-sibling::div"
    )
    FORM_REGISTERED_AT = (
        By.XPATH,
        "//span[contains(translate(text(),'REGISTERED AT','registered at'),'registered at')]/ancestor::div[1]/following-sibling::div"
    )

    """Simulation panel (middle column content area)."""
    SIMULATION_PANEL = (By.CSS_SELECTOR, "[data-testid='memodel-simulation-panel']")
    SIMULATION_PANEL_WRAPPER = (By.CSS_SELECTOR, "[data-testid='simulation-panel-wrapper']")

    """Stimulation protocol: IDrest plot and download button."""
    STIM_PLOT_IMAGE = (
        By.XPATH,
        "//div[@id='memodel-simulation-panel']//img[contains(@alt,'plot') or contains(@alt,'IDrest')] | //div[@id='memodel-simulation-panel']//canvas | //div[@id='memodel-simulation-panel']//*[contains(@class,'plot')]"
    )
    STIM_DOWNLOAD_BTN = (
        By.XPATH,
        "//div[@id='memodel-simulation-panel']//button[.//span[@aria-label='download'] or contains(text(),'Download')]"
    )
    STIM_N_STEPS_LABEL = (
        By.XPATH,
        "//span[contains(translate(text(),'N OF STEPS','n of steps'),'n of steps')]"
    )

    """Recording section: add recording button, recording entries, section dropdown."""
    RECORDING_ADD_BTN = (
        By.XPATH,
        "//div[@id='memodel-simulation-panel']//button[contains(text(),'Add') or .//span[contains(text(),'Add')]]"
    )
    RECORDING_ENTRIES = (
        By.XPATH,
        "//div[@id='memodel-simulation-panel']//div[contains(@class,'ant-form-item')]//div[contains(@class,'ant-select')]"
    )
    RECORDING_SECTION_DROPDOWN = (
        By.XPATH,
        "//div[contains(@id,'record_from')]//div[contains(@class,'ant-select')]"
    )
    RECORDING_DROPDOWN_OPTIONS = (
        By.CSS_SELECTOR,
        "div.ant-select-item.ant-select-item-option"
    )

    """Results tab: build cards, output files, code preview."""
    RESULTS_BUILD_CARDS = (
        By.XPATH,
        "//div[@data-slot='card'][.//div[@data-slot='card-title']]"
    )
    RESULTS_STATUS_BADGE = (By.XPATH, ".//div[@data-slot='badge']")
    RESULTS_OUTPUT_SECTION = (By.XPATH, "//h3[contains(text(),'Outputs')]")
    RESULTS_OUTPUT_MOD_BTN = (
        By.XPATH,
        "//h3[contains(text(),'Outputs')]/following-sibling::div//button[.//div[@data-slot='badge' and contains(text(),'MOD')]]"
    )
    RESULTS_OUTPUT_PDF_BTNS = (
        By.XPATH,
        "//h3[contains(text(),'Outputs')]/following-sibling::div//button[.//div[@data-slot='badge' and contains(text(),'PDF')]]"
    )
    RESULTS_CODE_PREVIEW = (By.CSS_SELECTOR, "pre.shiki code")

    """Results tab after Run experiment: left menu buttons (All + recording entries),
    Download CSV / Reconfigure buttons, IDREST plots, 3D canvas, success notification."""
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
    RESULTS_PLOT_CONTAINERS = (
        By.XPATH,
        "//div[contains(@id,'root-container-')]"
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
