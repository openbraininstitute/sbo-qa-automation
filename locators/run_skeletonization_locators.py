# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class RunSkeletonizationLocators:
    """Locators for the EM mesh skeletonization workflow page.

    Entry point: Workflows page → Process Data category → EM mesh skeletonization card
    URL pattern:
    /app/virtual-lab/{lab_id}/{project_id}/workflows/process-data/new/em-mesh-skeletonization
    """

    """Workflows page: Process Data category card and EM mesh skeletonization type card."""
    PROCESS_DATA_CATEGORY_CARD = (
        By.XPATH,
        "//div[@data-slot='card-title'][contains(., 'Process data')]"
        "/ancestor::div[@data-slot='card']"
    )
    EM_MESH_SKELETONIZATION_CARD = (
        By.XPATH,
        "//div[@data-slot='card']//div[@data-slot='card-title'][contains(., 'EM mesh skeletonization')]"
    )
    TYPE_CAROUSEL_NEXT_BTN = (
        By.XPATH,
        "//div[contains(@id,'workflow-types-menu')]//button[.//span[@aria-label='right']]"
    )

    """Breadcrumb."""
    BREADCRUMB = (
        By.XPATH,
        "//nav[@aria-label='breadcrumb'] | //div[contains(@class,'breadcrumb')]"
    )

    """Model picker: Public/Project tabs."""
    PUBLIC_TAB = (By.XPATH, "//button[@role='tab'][.//span[contains(text(),'Public')] or text()='Public']")
    PROJECT_TAB = (By.XPATH, "//button[@role='tab'][.//span[contains(text(),'Project')] or text()='Project']")

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
    MINI_DETAIL_METADATA = (
        By.XPATH,
        "//*[@data-testid='mini-viewer']//*[contains(text(),'Metadata') or contains(text(),'metadata')]"
    )
    MINI_DETAIL_VIEW_DETAILS_BTN = (
        By.XPATH,
        "//*[@data-testid='mini-viewer']//a[contains(text(),'View details') or @title='View details']"
        " | //*[@data-testid='mini-viewer']//button[contains(text(),'View details')]"
    )
    MINI_DETAIL_USE_MODEL_BTN = (
        By.XPATH,
        "//*[@data-testid='mini-viewer']//a[@title='Use model' or contains(text(),'Use model')]"
        " | //*[@data-testid='mini-viewer']//button[contains(text(),'Use model')]"
    )
    MINI_DETAIL_CLOSE_BTN = (
        By.XPATH,
        "//*[@data-testid='mini-viewer']//button[contains(@aria-label,'close') or contains(@class,'close')]"
        " | //*[@data-testid='mini-viewer']//button[.//span[contains(@class,'anticon-close')]]"
    )

    """Config page layout and top-level tabs (Configuration / Skeletonizations)."""
    CONFIG_LAYOUT = (By.CSS_SELECTOR, "button[data-scan-config-menu='left-menu-top-item']")
    CONFIG_TAB_CONFIGURATION = (
        By.XPATH,
        "//button[contains(translate(text(),'CONFIGURATION','configuration'),'configuration')]"
    )
    CONFIG_TAB_SKELETONIZATIONS = (
        By.XPATH,
        "//button[contains(translate(text(),'SKELETONIZATIONS','skeletonizations'),'skeletonization')]"
    )

    """Left menu buttons (Info and Initialization)."""
    LEFT_MENU_INFO_BTN = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']"
        "//span[contains(text(),'Info')]/ancestor::button"
    )
    LEFT_MENU_INITIALIZATION_BTN = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']"
        "//span[contains(text(),'Initialization')]/ancestor::button"
    )
    LEFT_MENU_ACTIVE_BTN = (
        By.CSS_SELECTOR,
        "button[data-scan-config-menu='left-menu-top-item'][data-active='true']"
    )

    """Warning / check icons scoped to Info menu button."""
    INFO_BTN_WARNING_ICON = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']"
        "[.//span[contains(text(),'Info')]]"
        "//span[contains(@class,'anticon-warning')]"
    )
    INFO_BTN_CHECK_ICON = (
        By.XPATH,
        "//button[@data-scan-config-menu='left-menu-top-item']"
        "[.//span[contains(text(),'Info')]]"
        "//span[contains(@class,'anticon-check')]"
    )

    """Info form fields (Campaign name, Campaign description)."""
    FORM_NAME_INPUT = (
        By.XPATH,
        "(//input[@data-scan-config-block-element='string_input'])[1]"
    )
    FORM_DESCRIPTION_INPUT = (
        By.XPATH,
        "(//input[@data-scan-config-block-element='string_input'])[2]"
    )

    """Initialization section: title and description."""
    INIT_TITLE = (
        By.XPATH,
        "//div[contains(@class,'font-semibold') or contains(@class,'text-primary')]"
        "[contains(translate(text(),'INFO','info'),'info')]"
    )
    INIT_DESCRIPTION = (
        By.XPATH,
        "//*[contains(text(),'Parameters for initializing the skeletonization')]"
    )

    """Initialization fields."""
    INIT_EM_CELL_MESH_ID = (
        By.XPATH,
        "//div[@data-scan-config-block-element='model_identifier']"
        "//div[@data-testid='model-identifier-entity']"
    )
    INIT_EM_CELL_MESH_NAME = (
        By.XPATH,
        "//div[@data-scan-config-block-element='model_identifier']"
        "//span[contains(@class,'truncate') and contains(@class,'font-semibold')]"
    )
    INIT_NEURON_VOXEL_SIZE = (
        By.XPATH,
        "//div[@data-scan-config-block-element='float_parameter_sweep']"
        "[.//div[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'neuron voxel size')]]"
        "//input[contains(@class,'ant-input-number-input')]"
    )
    INIT_SPINE_VOXEL_SIZE = (
        By.XPATH,
        "//div[@data-scan-config-block-element='float_parameter_sweep']"
        "[.//div[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'spine voxel size')]]"
        "//input[contains(@class,'ant-input-number-input')]"
    )
    INIT_INCLUDE_FULL_RES_SPINES_CHECKBOX = (
        By.XPATH,
        "//div[@data-scan-config-block-element='boolean_input']"
        "[.//div[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'include full resolution spines')]]"
        "//input[@type='checkbox']"
    )

    """Initialization block labels."""
    INIT_BLOCK_LABELS = (
        By.XPATH,
        "//div[@data-scan-config-block-element]"
        "//div[contains(@class,'text-primary-9') and contains(@class,'font-semibold')]"
    )

    """Generate skeletonization(s) button."""
    GENERATE_SKELETONIZATION_BTN = (
        By.XPATH,
        "//button[.//div[contains(text(),'Generate skeletonization')]]"
    )

    """Skeletonizations tab: cards, statuses, select all, Launch button."""
    SKEL_CARD_BUTTONS = (
        By.XPATH,
        "//button[@title[starts-with(.,'Skeletonization ')]]"
        " | //button[@title[starts-with(.,'Task ')]]"
    )
    SKEL_CARD_STATUS_BADGE = (
        By.XPATH,
        ".//span[contains(@class,'rounded-xl') or contains(@class,'rounded-full')]"
        "[contains(@class,'border') and contains(@class,'px-4')]"
    )
    SKEL_SELECT_ALL_CHECKBOX = (
        By.XPATH,
        "//label[contains(@class,'ant-checkbox-wrapper')]//span[contains(text(),'Select all')]"
        " | //*[contains(text(),'Select all')]"
    )
    LAUNCH_SKELETONIZATIONS_BTN = (
        By.XPATH,
        "//button[.//span[contains(text(),'Launch skeletonization')]]"
    )
    LAUNCH_SKELETONIZATIONS_BTN_TEXT = (
        By.XPATH,
        "//button[.//span[contains(text(),'Launch skeletonization')]]"
        "//span[contains(text(),'Launch skeletonization')]"
    )

    """Skeletonizations tab: input files (middle column)."""
    INPUT_FILES_HEADING = (
        By.XPATH,
        "//h4[contains(translate(text(),'INPUT FILES','input files'),'input files')]"
    )
    INPUT_FILE_BUTTONS = (
        By.XPATH,
        "//button[@data-testid[starts-with(.,'task-io-file-item')]]"
    )

    """Skeletonizations tab: JSON preview (right column)."""
    JSON_PREVIEW_CODE = (By.CSS_SELECTOR, "pre.shiki code")

    """Cost modal (appears after clicking Launch skeletonizations)."""
    COST_MODAL_TITLE = (
        By.XPATH,
        "//*[contains(text(),'Estimated cost breakdown')]"
    )
    COST_MODAL_ITEMS = (
        By.XPATH,
        "//label[.//button[@role='checkbox']]"
        " | //label[.//span[contains(text(),'Skeletonization')]]"
    )
    COST_MODAL_CHECKBOXES = (
        By.XPATH,
        "//button[@role='checkbox']"
    )
    COST_MODAL_TOTAL_CREDITS = (
        By.XPATH,
        "//span[contains(text(),'Total')]/parent::div"
        " | //div[.//span[contains(text(),'Total')]]//span[contains(text(),'credits')]"
    )
    COST_MODAL_CANCEL_BTN = (
        By.XPATH,
        "//button[contains(text(),'Cancel')]"
    )
    COST_MODAL_CONFIRM_BTN = (
        By.XPATH,
        "//button[contains(text(),'Confirm')]"
    )

    """Output files (appear after skeletonization completes)."""
    OUTPUT_FILE_BUTTONS = (
        By.XPATH,
        "//button[@data-testid[starts-with(.,'task-io-file-item')]][@data-file-name]"
        " | //button[@title='Skeletonized morphology']"
    )
    OUTPUT_FILE_BADGE = (
        By.XPATH,
        "//button[@title='Skeletonized morphology']//span[contains(text(),'swc')]"
    )

    """Output preview card (right column after clicking output file)."""
    OUTPUT_PREVIEW_TITLE = (By.CSS_SELECTOR, "[data-testid='mini-viewer'] h1")
    OUTPUT_PREVIEW_DESCRIPTION = (By.CSS_SELECTOR, "#record-description")
    OUTPUT_PREVIEW_IMAGE = (By.CSS_SELECTOR, "[data-testid='mini-viewer'] img")
    OUTPUT_PREVIEW_METADATA = (
        By.XPATH,
        "//*[@data-testid='mini-viewer']//div[contains(@class,'text-label')]"
    )
    OUTPUT_COPY_ID_BTN = (
        By.XPATH,
        "//*[@data-testid='mini-viewer']//button[@title='Copy ID']"
    )
    OUTPUT_DOWNLOAD_BTN = (
        By.XPATH,
        "//*[@data-testid='mini-viewer']//button[@title='download']"
    )
    OUTPUT_VIEW_DETAILS_BTN = (
        By.XPATH,
        "//*[@data-testid='mini-viewer']//a[@title='Go to details page']"
    )
