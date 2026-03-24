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

    # ── Breadcrumbs ──────────────────────────────────────────────────────
    BREADCRUMB_WORKFLOWS = (By.XPATH, "//a[contains(text(), 'Workflows') or contains(@href, 'workflows')]")
