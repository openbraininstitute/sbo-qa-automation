# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class BuildEMMappingLocators:
    """Locators for the Electron microscopy circuit (beta) build page.

    Entry point: Workflows page → Build section → Electron microscopy circuit (beta) card
    URL pattern:
    /app/virtual-lab/{lab_id}/{project_id}/workflows?activity=build&type=em_synapse_mapping_campaign
    """

    # ── Workflows page: Build section and EM card ────────────────────────

    BUILD_SECTION_CARD = (
        By.XPATH,
        "//div[@data-slot='card-title'][contains(., 'Build')]/ancestor::div[@data-slot='card']"
        " | //div[@data-slot='card'][.//div[@data-slot='card-title'][contains(., 'Build')]]",
    )

    EM_CIRCUIT_CARD = (
        By.XPATH,
        "//div[@data-slot='card']//div[@data-slot='card-title']"
        "[contains(., 'Electron microscopy circuit')]",
    )

    TYPE_CAROUSEL_NEXT_BTN = (
        By.XPATH,
        "//div[contains(@id,'workflow-types-menu')]"
        "//button[.//span[@aria-label='right']]",
    )

    # ── Model picker: Public/Project tabs ────────────────────────────────

    PUBLIC_TAB = (
        By.XPATH,
        "//button[@id='scope-selector-tab-public' or (@role='tab' and .//span[contains(text(),'Public')])]",
    )

    PROJECT_TAB = (
        By.XPATH,
        "//button[@id='scope-selector-tab-project' or (@role='tab' and .//span[contains(text(),'Project')])]",
    )

    # ── Breadcrumbs ──────────────────────────────────────────────────────

    BREADCRUMB_LIST = (
        By.CSS_SELECTOR,
        "ol[data-slot='breadcrumb-list']",
    )

    BREADCRUMB_EM_BUILD = (
        By.XPATH,
        "//ol[@data-slot='breadcrumb-list']"
        "//a[contains(text(),'Electron microscopy circuit')]",
    )

    BREADCRUMB_SELECT_DATASET = (
        By.XPATH,
        "//ol[@data-slot='breadcrumb-list']"
        "//span[contains(text(),'Select electron microscopy dense reconstruction dataset')]",
    )

    # ── Portion 65 card (dataset selection) ──────────────────────────────

    PORTION_65_CARD = (
        By.XPATH,
        "//div[@data-slot='card']//span[contains(text(),'Portion 65 of the IARPA MICrONS dataset')]"
        "/ancestor::div[@data-slot='card']",
    )

    PORTION_65_TITLE = (
        By.XPATH,
        "//span[contains(text(),'Portion 65 of the IARPA MICrONS dataset')]",
    )

    PORTION_65_DESCRIPTION = (
        By.XPATH,
        "//div[@data-slot='card']//span[contains(text(),'Portion 65 of the IARPA MICrONS dataset')]"
        "/ancestor::div[@data-slot='card']//span[contains(@class,'text-gray')]",
    )

    # ── Table: column headers, rows, checkboxes (AG Grid) ────────────────

    COLUMN_HEADERS = (By.CSS_SELECTOR, ".ag-header-cell[role='columnheader']")

    TABLE_ROWS = (
        By.CSS_SELECTOR,
        ".ag-center-cols-container .ag-row[role='row']",
    )

    TABLE_CHECKBOX = (
        By.CSS_SELECTOR,
        ".ag-pinned-left-cols-container .ag-row input.ag-checkbox-input, "
        ".ag-cell[col-id='ag-Grid-SelectionColumn'] input.ag-checkbox-input, "
        ".ag-selection-checkbox input.ag-checkbox-input",
    )

    TABLE_FIRST_CHECKBOX = (
        By.CSS_SELECTOR,
        ".ag-pinned-left-cols-container .ag-row input.ag-checkbox-input, "
        ".ag-center-cols-container .ag-row input.ag-checkbox-input",
    )

    # ── Use selection button ─────────────────────────────────────────────

    USE_SELECTION_BTN = (
        By.XPATH,
        "//div[@id='workflow-browse-use-selection']"
        "//button[contains(normalize-space(.),'Use selection')]",
    )

    USE_SELECTION_BTN_ENABLED = (
        By.XPATH,
        "//div[@id='workflow-browse-use-selection']"
        "//button[not(@disabled) and contains(normalize-space(.),'Use selection')]",
    )

    # ── Filter dropdown (Cell morphology / ME-model) ─────────────────────

    FILTER_DROPDOWN = (
        By.XPATH,
        "//button[@role='combobox'][.//span[contains(text(),'Cell morphology')]]"
        " | //button[@role='combobox'][.//span[contains(text(),'ME-model')]]",
    )

    FILTER_ME_MODEL_OPTION = (
        By.XPATH,
        "//div[@role='option'][contains(.,'ME-model')]"
        " | //span[contains(text(),'ME-model')]/ancestor::div[@role='option']",
    )

    # ── Config page: layout and top-level tabs ───────────────────────────

    CONFIG_LAYOUT = (
        By.CSS_SELECTOR,
        "button[data-scan-config-menu='left-menu-top-item']",
    )

    CONFIG_TAB_CONFIGURATION = (
        By.XPATH,
        "//button[@id='tab-configuration' or "
        "contains(translate(text(),'CONFIGURATION','configuration'),'configuration')]",
    )

    CONFIG_TAB_RESULTS = (
        By.XPATH,
        "//button[@id='tab-results' or "
        "contains(translate(text(),'RESULTS','results'),'results')]",
    )

    # ── Left menu buttons ────────────────────────────────────────────────

    LEFT_MENU_INFO_BTN = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']"
        "[.//span[contains(text(),'Info')]]",
    )

    LEFT_MENU_INITIALIZATION_BTN = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']"
        "[.//span[contains(text(),'Initialization')]]",
    )

    # ── Warning / check icons ────────────────────────────────────────────

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

    # ── Initialization tab content ───────────────────────────────────────

    INITIALIZATION_TITLE = (
        By.XPATH,
        "//div[@data-scan-config-block='block_single']"
        "//div[contains(@class,'uppercase')][contains(text(),'Initialization')]",
    )

    NEURONS_LABEL = (
        By.XPATH,
        "//div[@data-scan-config-block-element='model_identifier_multiple']"
        "//div[contains(@class,'font-semibold')][contains(text(),'Neurons')]",
    )

    NEURON_GROUP_CONTAINER = (
        By.CSS_SELECTOR,
        "div[data-testid='model-identifier-multiple-summary-view-group']",
    )

    NEURON_GROUP_NAME_INPUT = (
        By.XPATH,
        "//div[@data-testid='model-identifier-multiple-summary-view-group']"
        "//input[@placeholder='Name of the group']",
    )

    NEURON_GROUP_BADGE_COUNT = (
        By.XPATH,
        "//div[@data-testid='model-identifier-multiple-summary-view-group']"
        "//div[@data-slot='badge']",
    )

    NEURON_ENTITY_CARD = (
        By.CSS_SELECTOR,
        "div[data-testid='model-identifier-entity-card']",
    )

    NEURON_ENTITY_MORPHOLOGY_BADGE = (
        By.XPATH,
        "//div[@data-testid='model-identifier-entity-card']"
        "//span[contains(text(),'MORPHOLOGY')]",
    )

    NEURON_ENTITY_ME_MODEL_BADGE = (
        By.XPATH,
        "//div[@data-testid='model-identifier-entity-card']"
        "//span[contains(text(),'ME-MODEL')]",
    )

    NEURON_ENTITY_DELETE_BTN = (
        By.XPATH,
        "//div[@data-testid='model-identifier-multiple-summary-view-group']"
        "//button[@aria-label='Remove group']",
    )

    ADD_ITEMS_BTN = (
        By.XPATH,
        "//div[@data-testid='model-identifier-multiple-summary-view-group']"
        "//button[.//span[contains(text(),'Add item')]]",
    )

    ADD_GROUP_TO_SCAN_BTN = (
        By.XPATH,
        "//button[.//span[contains(text(),'Add group to scan')]]",
    )

    # ── Add neuron set overlay (list view with Confirm/Cancel) ───────────

    OVERLAY_CONFIRM_BTN = (
        By.XPATH,
        "//button[.//span[contains(text(),'Confirm')]]",
    )

    OVERLAY_CANCEL_BTN = (
        By.XPATH,
        "//button[contains(@class,'rounded-full')][contains(text(),'Cancel')]"
        " | //button[.//text()[contains(.,'Cancel')]]",
    )

    OVERLAY_PUBLIC_TAB = (
        By.XPATH,
        "//div[@id='scan-config-model-selection-overlay']"
        "//button[@id='scope-selector-tab-public' or .//span[contains(text(),'Public')]]",
    )

    OVERLAY_TABLE_ROWS = (
        By.XPATH,
        "//div[@id='scan-config-model-selection-overlay']"
        "//tbody[contains(@class,'ant-table-tbody')]//tr[contains(@class,'ant-table-row')]",
    )

    OVERLAY_CLOSE_BTN = (
        By.XPATH,
        "//div[@id='scan-config-model-selection-overlay']"
        "//button[@aria-label='Close selection']",
    )

    # ── Generate build(s) button ─────────────────────────────────────────

    GENERATE_BUILDS_BTN = (
        By.XPATH,
        "//button[.//div[contains(text(),'Generate build')]]",
    )

    GENERATE_BUILDS_BTN_ENABLED = (
        By.XPATH,
        "//button[not(@disabled)][.//div[contains(text(),'Generate build')]]",
    )

    # ── Results tab content ──────────────────────────────────────────────

    RESULTS_CARD_BUTTONS = (
        By.XPATH,
        "//div[@id='scan-config-results-left-column']//button[@title]"
        " | //div[@id='scan-config-results']//button[contains(@class,'rounded')][@title]",
    )

    RESULTS_CARD_STATUS_BADGE = (
        By.XPATH,
        ".//span[contains(@class,'rounded')]"
        "[contains(@class,'border') or contains(@class,'px')]",
    )

    # ── Input files (INPUTS section) ─────────────────────────────────────

    INPUT_FILE_BUTTONS = (
        By.XPATH,
        "//div[@id='scan-config-results-middle-column']//button[@title]"
        " | //button[contains(@title,'.json')]",
    )

    JSON_PREVIEW_CODE = (By.CSS_SELECTOR, "pre.shiki code, pre code")

    # ── Launch builds button and modal ───────────────────────────────────

    LAUNCH_BUILDS_BTN = (
        By.XPATH,
        "//button[.//span[contains(text(),'Launch builds')]]",
    )

    LAUNCH_BUILDS_BTN_ENABLED = (
        By.XPATH,
        "//button[not(@disabled)][.//span[contains(text(),'Launch builds')]]",
    )

    LAUNCH_MODAL = (
        By.XPATH,
        "//div[contains(@class,'modal') or @role='dialog']"
        "[.//text()[contains(.,'Estimated cost')]]"
        " | //div[contains(text(),'Estimated cost')]"
        "/ancestor::div[contains(@class,'fixed') or @role='dialog']",
    )

    LAUNCH_MODAL_CONFIRM_BTN = (
        By.XPATH,
        "//div[contains(@class,'modal') or @role='dialog' or contains(@class,'fixed')]"
        "//button[contains(text(),'Confirm') or .//span[contains(text(),'Confirm')]]",
    )

    LAUNCH_MODAL_CANCEL_BTN = (
        By.XPATH,
        "//div[contains(@class,'modal') or @role='dialog' or contains(@class,'fixed')]"
        "//button[contains(text(),'Cancel') or .//span[contains(text(),'Cancel')]]",
    )

    # ── Build status badges ──────────────────────────────────────────────

    BUILD_STATUS_BADGE = (
        By.XPATH,
        "//span[contains(@class,'rounded-full') and contains(@class,'capitalize')]",
    )

    # ── Outputs section (Task logs) ──────────────────────────────────────

    OUTPUTS_SECTION = (
        By.XPATH,
        "//div[@id='scan-config-results-right-column']"
        " | //*[contains(text(),'OUTPUTS') or contains(text(),'Task logs')]",
    )

    TASK_LOGS_CONTENT = (
        By.XPATH,
        "//div[@id='scan-config-results-right-column']//pre"
        " | //div[contains(@class,'overflow')]//pre[contains(@class,'shiki')]",
    )

    # ── Copy and Download buttons ────────────────────────────────────────

    COPY_BTN = (
        By.XPATH,
        "//button[contains(text(),'Copy') or @aria-label='Copy' or "
        ".//span[contains(text(),'Copy')]]",
    )

    COPY_JSON_OPTION = (
        By.XPATH,
        "//div[@role='menu' or @role='listbox' or contains(@class,'dropdown')]"
        "//button[contains(text(),'JSON')]"
        " | //button[contains(text(),'JSON')]",
    )

    DOWNLOAD_BTN = (
        By.XPATH,
        "//button[contains(text(),'Download') or @aria-label='Download' or "
        ".//span[contains(text(),'Download')]]",
    )

    DOWNLOAD_JSON_OPTION = (
        By.XPATH,
        "//div[@role='menu' or @role='listbox' or contains(@class,'dropdown')]"
        "//button[contains(text(),'JSON')]"
        " | //button[contains(text(),'JSON')]",
    )

    COPY_SUCCESS_INDICATOR = (
        By.XPATH,
        "//*[contains(text(),'success') or contains(text(),'Copied') or "
        "contains(@class,'anticon-check')]",
    )
