# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class SimulatePairedNeuronsLocators:
    """Locators for the Paired neurons (beta) simulation page.

    Entry point: Workflows page → Simulate category → Paired neurons (beta) card
    URL pattern:
    /app/virtual-lab/{lab_id}/{project_id}/workflows/simulate/new/paired-neurons-simulation
    """

    """Workflows page: Simulate category card and Paired neurons type card."""
    SIMULATE_CATEGORY_CARD = (
        By.XPATH,
        "//div[@data-slot='card-title'][contains(., 'Simulate')]/ancestor::div[@data-slot='card']"
        " | (//div[@data-slot='card'])[2]",
    )
    PAIRED_NEURONS_CARD = (
        By.XPATH,
        "//div[@data-slot='card']//div[@data-slot='card-title']"
        "[contains(., 'Paired neurons')]",
    )
    TYPE_CAROUSEL_NEXT_BTN = (
        By.XPATH,
        "//div[@id='workflow-types-menu-simulate']"
        "//button[.//span[@aria-label='right']]",
    )

    """Model picker: Public/Project tabs."""
    PUBLIC_TAB = (By.XPATH, "//button[@role='tab'][.//span[contains(text(),'Public')] or text()='Public']")

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
    MINI_DETAIL_USE_MODEL_BTN = (
        By.CSS_SELECTOR,
        "[data-testid='mini-viewer'] [title='Start simulation']",
    )

    """Config page layout and top-level tabs."""
    CONFIG_LAYOUT = (
        By.CSS_SELECTOR,
        "button[data-scan-config-menu='left-menu-top-item']",
    )
    CONFIG_TAB_CONFIGURATION = (
        By.XPATH,
        "//button[contains(translate(text(),'CONFIGURATION','configuration'),'configuration')]",
    )
    CONFIG_TAB_SIMULATIONS = (
        By.XPATH,
        "//button[contains(translate(text(),'SIMULATIONS','simulations'),'simulations')]",
    )
    CIRCUIT_PREVIEW_IMAGE = (
        By.CSS_SELECTOR,
        "div[class*='circuitPreview'] div[class*='zoomableImage']",
    )

    """Left menu buttons — Setup."""
    LEFT_MENU_INFO_BTN = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']"
        "//span[contains(text(),'Info')]/ancestor::button",
    )
    LEFT_MENU_INITIALIZATION_BTN = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']"
        "//span[contains(text(),'Initialization')]/ancestor::button",
    )

    """Left menu buttons — Stimuli & Recordings."""
    LEFT_MENU_STIMULI_BTN = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']"
        "//span[contains(text(),'Stimuli')]/ancestor::button",
    )
    LEFT_MENU_RECORDINGS_BTN = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']"
        "//span[contains(text(),'Recordings')]/ancestor::button",
    )

    """Left menu buttons — Circuit Components."""
    LEFT_MENU_DISTRIBUTIONS_BTN = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']"
        "//span[contains(text(),'Distributions')]/ancestor::button",
    )
    LEFT_MENU_NEURON_SETS_BTN = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']"
        "//span[contains(text(),'Neuron sets')]/ancestor::button",
    )

    """Left menu buttons — Manipulations."""
    LEFT_MENU_SYNAPTIC_MANIP_BTN = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']"
        "//span[contains(text(),'Synaptic manipulations')]/ancestor::button",
    )

    """Left menu buttons — Events."""
    LEFT_MENU_TIMESTAMPS_BTN = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']"
        "//span[contains(text(),'Timestamps')]/ancestor::button",
    )

    """Warning / check icons on Info button."""
    INFO_BTN_WARNING_ICON = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']"
        "[.//span[contains(text(),'Info')]]"
        "//span[contains(@class,'anticon-warning')]",
    )
    INFO_BTN_CHECK_ICON = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']"
        "[.//span[contains(text(),'Info')]]"
        "//span[contains(@class,'anticon-check')]",
    )

    """Info form fields."""
    FORM_NAME_INPUT = (
        By.XPATH,
        "(//input[@data-scan-config-block-element='string_input'])[1]",
    )
    FORM_DESCRIPTION_INPUT = (
        By.XPATH,
        "(//input[@data-scan-config-block-element='string_input'])[2]",
    )

    """Initialization block labels and inputs."""
    CONFIG_BLOCK_ELEMENTS = (By.CSS_SELECTOR, "div[data-scan-config-block-element]")
    BLOCK_LABEL = (By.CSS_SELECTOR, ".text-primary-9.text-base.font-semibold")
    BLOCK_NUMBER_INPUT = (By.CSS_SELECTOR, "input.ant-input-number-input")
    INIT_BLOCK_LABELS = (
        By.XPATH,
        "//div[@data-scan-config-block-element]"
        "//div[contains(@class,'text-primary-9') and contains(@class,'font-semibold')]",
    )

    """Dictionary items and Add button (shared by Stimuli, Recordings, etc.)."""
    CONFIG_BLOCK_DICTIONARY_ITEMS = (
        By.CSS_SELECTOR,
        "button[data-scan-config-block-element-item='block_dictionary_item']",
    )
    CONFIG_ADD_BTN_IN_SUB_ENTRY = (
        By.XPATH,
        "//div[contains(@data-scan-config-menu,'menu-block-dictionary-sub-entry')]"
        "[@data-active='true']//button[.//span[contains(text(),'Add')]]",
    )
    CONFIG_BLOCK_SINGLE = (
        By.CSS_SELECTOR,
        "div[data-scan-config-block='block_single']",
    )

    """Middle column scrollable area (for scrolling to find items)."""
    MIDDLE_COLUMN_SCROLLABLE = (
        By.CSS_SELECTOR,
        "div[class*='scrollable']",
    )

    """Generate simulation(s) button."""
    GENERATE_SIMULATION_BTN = (
        By.XPATH,
        "//button[.//div[contains(text(),'Generate simulation')]]",
    )

    """Simulations tab: cards, statuses, Launch button."""
    SIM_CARD_BUTTONS = (
        By.XPATH,
        "//button[@title[starts-with(.,'Simulation ')]]",
    )
    SIM_CARD_STATUS_BADGE = (
        By.XPATH,
        ".//span[contains(@class,'rounded-xl') or contains(@class,'rounded-full')][contains(@class,'border') and contains(@class,'px-4')]",
    )
    LAUNCH_SIMULATIONS_BTN = (
        By.XPATH,
        "//button[.//span[contains(text(),'Launch simulations')]]",
    )

    """Input files."""
    INPUT_FILE_BUTTONS = (
        By.XPATH,
        "//button[@data-testid[starts-with(.,'task-io-file-item')]]"
        " | //h4[contains(translate(text(),'INPUT FILES','input files'),'input files')]"
        "/ancestor::div[contains(@class,'ant-collapse-item')]//button[@title]",
    )
    JSON_PREVIEW_CODE = (By.CSS_SELECTOR, "pre.shiki code")
