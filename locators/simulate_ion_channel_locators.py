# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class SimulateIonChannelLocators:
    """Locators for the Ion channel (beta) simulation page.

    Entry point: Workflows page → Simulate category → Ion channel (beta) card
    URL pattern:
    /app/virtual-lab/{lab_id}/{project_id}/workflows/simulate/new/ion-channel-simulation
    """

    # ── Workflows page: Simulate category and Ion channel type card ──────
    SIMULATE_CATEGORY_CARD = (
        By.XPATH,
        "(//div[@data-slot='card'])[2]",
    )
    ION_CHANNEL_CARD = (
        By.XPATH,
        "//div[@data-slot='card']//div[@data-slot='card-title'][contains(., 'Ion channel')]",
    )
    TYPE_CAROUSEL_NEXT_BTN = (
        By.XPATH,
        "//div[@id='workflow-types-menu-simulate']//button[.//span[@aria-label='right']]",
    )

    # ── Model picker ─────────────────────────────────────────────────────
    PUBLIC_TAB = (By.XPATH, "//button[@role='tab' and text()='Public']")
    TABLE_ROWS = (By.CSS_SELECTOR, "tbody.ant-table-tbody tr.ant-table-row")

    # ── Mini-detail view ─────────────────────────────────────────────────
    MINI_VIEWER = (By.CSS_SELECTOR, "[data-testid='mini-viewer']")
    MINI_DETAIL_TITLE = (By.CSS_SELECTOR, "[data-testid='mini-viewer'] h1")
    MINI_DETAIL_DESCRIPTION = (By.CSS_SELECTOR, "#record-description")
    MINI_DETAIL_USE_MODEL_BTN = (
        By.CSS_SELECTOR,
        "[data-testid='mini-viewer'] a[title='Start simulation']",
    )

    # ── Config page layout and top-level tabs ────────────────────────────
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

    # ── Right-hand column: Model Traces and Parameters ───────────────────
    MODEL_TRACES_DROPDOWN = (
        By.XPATH,
        "//button[@data-slot='select-trigger']"
        "[.//span[@data-slot='select-value'][contains(text(),'Model traces')]]",
    )
    ACTIVATION_DROPDOWN = (
        By.XPATH,
        "//button[@data-slot='select-trigger']"
        "[.//span[@data-slot='select-value']"
        "[contains(text(),'Activation') or contains(text(),'Inactivation')]]",
    )
    RIGHT_COLUMN_SELECT_TRIGGERS = (
        By.XPATH,
        "//button[@data-slot='select-trigger']"
        "[.//span[@data-slot='select-value']]",
    )
    # Dropdown list items (appear after clicking a select-trigger)
    SELECT_DROPDOWN_ITEMS = (
        By.XPATH,
        "//div[@data-slot='select-content']//div[@data-slot='select-item']"
        " | //div[@role='option']"
        " | //div[@data-radix-collection-item]"
        " | //div[contains(@class,'SelectItem')]"
        " | //div[@data-slot='select-item']",
    )
    # Plot canvases in the right column (PDF-rendered plots)
    RIGHT_COLUMN_PLOT_CANVAS = (
        By.CSS_SELECTOR,
        "canvas.react-pdf__Page__canvas",
    )
    # Plot section labels (Stimuli, Traces)
    RIGHT_COLUMN_PLOT_LABELS = (
        By.XPATH,
        "//div[contains(@class,'text-label') and contains(@class,'uppercase')]",
    )
    MODEL_TRACES_PLOT = (
        By.XPATH,
        "//div[contains(@class,'js-plotly-plot')]"
        " | //div[contains(@class,'plot')]"
        " | //canvas[contains(@class,'react-pdf__Page__canvas')]"
        " | //*[name()='svg'][.//*[name()='g']]",
    )
    PARAMETERS_SECTION = (
        By.XPATH,
        "//div[contains(translate(text(),'PARAMETERS','parameters'),'parameters')]"
        " | //h3[contains(translate(text(),'PARAMETERS','parameters'),'parameters')]"
        " | //span[contains(translate(text(),'PARAMETERS','parameters'),'parameters')]",
    )
    PARAMETER_DROPDOWNS = (
        By.XPATH,
        "//div[contains(@class,'ant-collapse-item')] | //div[contains(@class,'ant-select')]",
    )

    # ── Left menu buttons ────────────────────────────────────────────────
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

    # ── Ion channel models: left menu button and sub-entry ───────────────
    LEFT_MENU_ION_CHANNEL_MODELS_BTN = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']"
        "//span[contains(text(),'Ion channel model')]/ancestor::button",
    )
    ION_CHANNEL_MODELS_ADD_BTN = (
        By.XPATH,
        "//div[@data-scan-config-menu='menu-block-dictionary-sub-entry']"
        "[@data-active='true']//button[.//span[contains(text(),'Add')]]",
    )
    ION_CHANNEL_MODEL_TYPE_ITEMS = (
        By.CSS_SELECTOR,
        "button[data-scan-config-block-element-item='block_dictionary_item']",
    )
    ION_CHANNEL_MODEL_FIELD = (
        By.XPATH,
        "//div[@data-scan-config-block='block_single']"
        "//button[contains(@class,'ant-select') or contains(@class,'placeholder')]"
        " | //div[@data-scan-config-block='block_single']"
        "//div[contains(@class,'ant-select-selector')]"
        " | //div[@data-scan-config-block='block_single']"
        "//button[contains(text(),'Click to select') or contains(text(),'select')]",
    )
    ION_CHANNEL_MODEL_LIST_ROWS = (
        By.CSS_SELECTOR,
        "tbody.ant-table-tbody tr.ant-table-row",
    )
    ION_CHANNEL_MODEL_RADIO_BTN = (
        By.XPATH,
        "//table//input[@type='radio']"
        " | //table//span[contains(@class,'ant-radio-inner')]",
    )
    ION_CHANNEL_MODEL_SELECT_BTN = (
        By.XPATH,
        "//div[@id='modal-footer']//button[contains(.,'Select')]"
        " | //button[text()='Select']",
    )
    ION_CHANNEL_CONDUCTANCE_INPUT = (
        By.XPATH,
        "//div[@data-scan-config-block='block_single']"
        "//input[contains(@class,'ant-input-number-input')]",
    )

    # ── Warning / check icons on Info button ─────────────────────────────
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

    # ── Info form fields ─────────────────────────────────────────────────
    FORM_NAME_INPUT = (
        By.XPATH,
        "(//input[@data-scan-config-block-element='string_input'])[1]",
    )
    FORM_DESCRIPTION_INPUT = (
        By.XPATH,
        "(//input[@data-scan-config-block-element='string_input'])[2]",
    )

    # ── Initialization: config blocks and sweep (plus-circle) buttons ────
    CONFIG_BLOCK_ELEMENTS = (
        By.CSS_SELECTOR,
        "div[data-scan-config-block-element]",
    )
    BLOCK_LABEL = (
        By.CSS_SELECTOR,
        ".text-primary-9.text-base.font-semibold",
    )
    BLOCK_NUMBER_INPUT = (
        By.CSS_SELECTOR,
        "input.ant-input-number-input",
    )
    INIT_BLOCK_LABELS = (
        By.XPATH,
        "//div[@data-scan-config-block-element]"
        "//div[contains(@class,'text-primary-9') and contains(@class,'font-semibold')]",
    )
    SWEEP_ADD_BTN = (
        By.XPATH,
        "//button[.//*[contains(@class,'anticon-plus-circle')] or @aria-label='add sweep']",
    )

    # ── Stimuli: dictionary items and Add button ─────────────────────────
    CONFIG_ADD_BTN_IN_SUB_ENTRY = (
        By.XPATH,
        "//div[@data-scan-config-menu='menu-block-dictionary-sub-entry']"
        "[@data-active='true']//button[.//span[contains(text(),'Add')]]",
    )
    CONFIG_BLOCK_DICTIONARY_ITEMS = (
        By.CSS_SELECTOR,
        "button[data-scan-config-block-element-item='block_dictionary_item']",
    )
    CONFIG_BLOCK_SINGLE = (
        By.CSS_SELECTOR,
        "div[data-scan-config-block='block_single']",
    )

    # ── Recordings use the same dictionary pattern as Ion channel models ──
    # (CONFIG_ADD_BTN_IN_SUB_ENTRY and CONFIG_BLOCK_DICTIONARY_ITEMS)

    # Recording form: Ion Channel Variable Name dropdown
    RECORDING_VARIABLE_DROPDOWN = (
        By.XPATH,
        "//div[@data-scan-config-block='block_single']"
        "//div[@data-scan-config-block-element='select_recordable_ion_channel_variable']"
        "//button[@data-slot='select-trigger']",
    )

    # Recording entry buttons in the left-column sub-entry
    RECORDING_ENTRY_BUTTONS = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']"
        "[.//span[contains(text(),'Recordings')]]"
        "/ancestor::div[contains(@class,'flex-col')][1]"
        "//div[@data-scan-config-menu='menu-block-dictionary-sub-entry']"
        "//div[contains(@class,'entryButton') and @role='button']",
    )

    # Add Recording button (scoped to the Recordings sub-entry)
    RECORDING_ADD_BTN = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']"
        "[.//span[contains(text(),'Recordings')]]"
        "/ancestor::div[contains(@class,'flex-col')][1]"
        "//button[.//span[contains(text(),'Add')]]",
    )

    # ── Generate simulation(s) button ────────────────────────────────────
    GENERATE_SIMULATION_BTN = (
        By.XPATH,
        "//button[.//div[contains(text(),'Generate simulation')]]",
    )

    # ── Simulations tab: cards, statuses, Launch button ──────────────────
    SIM_CARD_BUTTONS = (
        By.XPATH,
        "//button[@title[starts-with(.,'Simulation ')]]",
    )
    SIM_CARD_STATUS_BADGE = (
        By.XPATH,
        ".//span[contains(@class,'rounded-xl')]",
    )
    LAUNCH_SIMULATIONS_BTN = (
        By.XPATH,
        "//button[.//span[contains(text(),'Launch simulations')]]",
    )

    # ── Input files ──────────────────────────────────────────────────────
    INPUT_FILES_HEADING = (
        By.XPATH,
        "//h4[contains(translate(text(),'INPUT FILES','input files'),'input files')]",
    )
    INPUT_FILE_BUTTONS = (
        By.XPATH,
        "//h4[contains(translate(text(),'INPUT FILES','input files'),'input files')]"
        "/following-sibling::div//button[@title]",
    )
    JSON_PREVIEW_CODE = (By.CSS_SELECTOR, "pre.shiki code")

    # ── Output files ─────────────────────────────────────────────────────
    OUTPUT_FILES_HEADING = (
        By.XPATH,
        "//h4[contains(translate(text(),'OUTPUT FILES','output files'),'output files')]",
    )
    OUTPUT_FILE_BUTTONS = (
        By.XPATH,
        "//h4[contains(translate(text(),'OUTPUT FILES','output files'),'output files')]"
        "/following-sibling::div//button[@title]",
    )
    OUTPUT_CONTENT_AREA = (
        By.XPATH,
        "//div[contains(@class,'js-plotly-plot')]"
        " | //img[contains(@alt,'plot') or contains(@src,'blob:')]"
        " | //pre[contains(@class,'shiki')]"
        " | //canvas",
    )

    # ── Recording output: Overview / Interactive details tabs ─────────────
    OVERVIEW_TAB = (
        By.XPATH,
        "//button[@role='tab' and contains(text(),'Overview')]",
    )
    INTERACTIVE_DETAILS_TAB = (
        By.XPATH,
        "//button[@role='tab' and contains(text(),'Interactive details')]",
    )
    TAB_PLOT_CONTENT = (
        By.XPATH,
        "//div[contains(@class,'js-plotly-plot')]"
        " | //img[contains(@alt,'plot') or contains(@src,'blob:')]"
        " | //canvas",
    )
