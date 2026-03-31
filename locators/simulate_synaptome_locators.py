# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class SimulateSynaptomeLocators:
    """Locators for the Synaptome simulation page (non-beta).

    Entry point: Workflows page → Simulate category → Synaptome card
    URL pattern:
    /app/virtual-lab/{lab_id}/{project_id}/workflows/simulate/new/synaptome-simulation
    """

    """Workflows page: Simulate category card and Synaptome type card."""
    SIMULATE_CATEGORY_CARD = (
        By.XPATH,
        "(//div[@data-slot='card'])[2]"
    )
    SYNAPTOME_CARD = (
        By.XPATH,
        "//div[@data-slot='card']//div[@data-slot='card-title'][contains(., 'Synaptome') and not(contains(., 'beta'))]"
    )

    """Model picker: Public/Project tabs."""
    PUBLIC_TAB = (By.XPATH, "//button[@role='tab' and text()='Public']")
    PROJECT_TAB = (By.XPATH, "//button[@role='tab' and text()='Project']")

    """Column headers and table rows."""
    COLUMN_HEADERS = (By.CSS_SELECTOR, "th[data-testid='column-header']")
    TABLE_ROWS = (By.CSS_SELECTOR, "tbody.ant-table-tbody tr.ant-table-row")

    """Filter panel."""
    FILTER_BUTTON = (By.XPATH, "//button[@aria-label='listing-view-filter-button']")
    FILTER_CLOSE_BUTTON = (By.XPATH, "//button[@aria-label='Close']")
    FILTER_ACCORDION_TRIGGERS = (
        By.XPATH,
        "//button[contains(@class,'accordionTrigger')]"
    )

    """Mini-detail view after clicking a table row."""
    MINI_VIEWER = (By.CSS_SELECTOR, "[data-testid='mini-viewer']")
    MINI_DETAIL_TITLE = (By.CSS_SELECTOR, "[data-testid='mini-viewer'] h1")
    MINI_DETAIL_DESCRIPTION = (By.CSS_SELECTOR, "#record-description")
    MINI_DETAIL_IMAGES = (By.CSS_SELECTOR, "[data-testid='mini-viewer'] img.ant-image-img")
    MINI_DETAIL_METADATA_LABELS = (
        By.CSS_SELECTOR,
        "[data-testid='mini-viewer'] .text-primary-3.text-base.font-light"
    )
    MINI_DETAIL_CLOSE_BTN = (By.CSS_SELECTOR, "[data-testid='mini-viewer'] button .anticon-close")
    MINI_DETAIL_VIEW_DETAILS_BTN = (By.CSS_SELECTOR, "[data-testid='mini-viewer'] a[title='Go to details page']")
    MINI_DETAIL_USE_MODEL_BTN = (By.CSS_SELECTOR, "[data-testid='mini-viewer'] a[title='Start simulation']")

    """Config page layout and top-level radix tabs (Configuration / Results)."""
    CONFIG_LAYOUT = (By.CSS_SELECTOR, "[data-testid='workflow-simulate-layout']")
    CONFIG_TAB_CONFIGURATION = (By.XPATH, "//button[@role='tab' and contains(text(),'Configuration')]")
    CONFIG_TAB_RESULTS = (By.XPATH, "//button[@role='tab' and contains(text(),'Results')]")
    NEURON_VISUALIZER_CANVAS = (By.CSS_SELECTOR, "[data-testid='neuron-visualizer'] canvas")

    """Left menu buttons."""
    LEFT_MENU_INFO_BTN = (By.XPATH, "//div[@id='menu']//button[.//div[contains(text(),'Info')]]")
    LEFT_MENU_EXPERIMENTAL_SETUP_BTN = (By.XPATH, "//div[@id='menu']//button[.//div[contains(text(),'Experimental setup')]]")
    LEFT_MENU_SYNAPTIC_INPUT_BTN = (By.XPATH, "//div[@id='menu']//button[.//div[contains(text(),'Synaptic') and contains(text(),'nput')]]")
    LEFT_MENU_STIMULATION_PROTOCOL_BTN = (By.XPATH, "//div[@id='menu']//button[.//div[contains(text(),'Stimulation protocol')]]")
    LEFT_MENU_RECORDING_BTN = (By.XPATH, "//div[@id='menu']//button[.//div[contains(text(),'Recording')]]")
    LEFT_MENU_ACTIVE_BTN = (By.XPATH, "//div[@id='menu']//button[contains(@class,'bg-primary-9') and contains(@class,'text-white')]")
    RUN_EXPERIMENT_BTN = (By.XPATH, "//div[@id='menu']//button[.//div[contains(text(),'Run experiment')]]")

    """Info form fields."""
    FORM_NAME_INPUT = (By.CSS_SELECTOR, "#single-model-configuration-form_name")
    FORM_DESCRIPTION_INPUT = (By.CSS_SELECTOR, "#single-model-configuration-form_description")
    FORM_REGISTERED_BY = (
        By.XPATH,
        "//span[contains(translate(text(),'CREATED BY','created by'),'created by')]/ancestor::div[1]/following-sibling::div"
    )
    FORM_REGISTERED_AT = (
        By.XPATH,
        "//span[contains(translate(text(),'REGISTERED AT','registered at'),'registered at')]/ancestor::div[1]/following-sibling::div"
    )

    """Simulation panel (middle column — synaptome-specific)."""
    SIMULATION_PANEL = (By.CSS_SELECTOR, "[data-testid='synaptome-simulation-panel']")

    """Synaptic input section: entries, eye toggle, form fields."""
    SYNAPTIC_INPUT_ENTRIES = (
        By.XPATH,
        "//div[starts-with(@id,'synaptic-input-')]"
    )
    SYNAPTIC_INPUT_EYE_BTN = (
        By.XPATH,
        "//button[@aria-label='Show synapses']"
    )
    SYNAPTIC_INPUT_EYE_CROSSED = (
        By.XPATH,
        "//button[@aria-label='Hide synapses']"
    )
    SYNAPTIC_INPUT_ADD_BTN = (
        By.XPATH,
        "//button[contains(text(),'Add synaptic input')]"
    )

    """Stimulation protocol: plot and download button."""
    STIM_PLOT_IMAGE = (
        By.XPATH,
        "//div[@id='synaptome-simulation-panel']//*[contains(@class,'plot')] | //div[@id='synaptome-simulation-panel']//img"
    )
    STIM_DOWNLOAD_BTN = (
        By.XPATH,
        "//div[@id='synaptome-simulation-panel']//button[.//span[@aria-label='download'] or contains(text(),'Download')]"
    )

    """Recording section."""
    RECORDING_ADD_BTN = (
        By.XPATH,
        "//div[@id='synaptome-simulation-panel']//button[contains(text(),'Add') or .//span[contains(text(),'Add')]]"
    )
    RECORDING_SECTION_DROPDOWN = (
        By.XPATH,
        "//div[contains(@id,'record_from')]//div[contains(@class,'ant-select')]"
    )
    RECORDING_DROPDOWN_OPTIONS = (By.CSS_SELECTOR, "div.ant-select-item.ant-select-item-option")

    """Results tab: left menu, buttons, plots, canvas, notification."""
    RESULTS_LEFT_MENU_BUTTONS = (By.XPATH, "//div[@id='menu']//button[@data-slot='button']")
    RESULTS_ALL_BTN = (By.XPATH, "//div[@id='menu']//button[.//div[text()='All']]")
    RESULTS_RECORDING_BTNS = (By.XPATH, "//div[@id='menu']//button[.//div[contains(text(),'[') and contains(text(),'_')]]")
    RESULTS_DOWNLOAD_CSV_BTN = (By.XPATH, "//div[@id='menu']//button[.//div[contains(text(),'Download')]]")
    RESULTS_RECONFIGURE_BTN = (By.XPATH, "//div[@id='menu']//button[.//div[contains(text(),'Reconfigure')]]")
    RESULTS_IDREST_PLOTS = (By.CSS_SELECTOR, "div.js-plotly-plot")
    RESULTS_PLOT_CONTAINERS = (By.XPATH, "//div[contains(@id,'root-container-')]")
    RESULTS_NEURON_CANVAS = (By.CSS_SELECTOR, "[data-testid='neuron-visualizer'] canvas")
    RESULTS_SUCCESS_NOTIFICATION = (By.CSS_SELECTOR, "div.ant-notification-notice-success")
    RESULTS_VIEW_SIMULATION_LINK = (
        By.XPATH,
        "//div[contains(@class,'ant-notification-notice-success')]//a[contains(text(),'View Simulation')]"
    )
