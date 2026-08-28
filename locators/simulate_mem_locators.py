# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class SimulateMemLocators:
    """Locators for the ME-model simulation page (Single neuron card entry).

    Entry point: Workflows page → Simulate category → Single neuron card
    URL pattern:
    /app/virtual-lab/{lab_id}/{project_id}/workflows?activity=simulate

    The config UI after "Use model" matches the ME-beta scan-config layout;
    use SimulateMeBetaLocators / SimulateMeBetaPage for post-picker steps.
    """

    """Workflows page: Simulate category card and Single neuron type card."""
    SIMULATE_CATEGORY_CARD = (
        By.XPATH,
        "//div[@data-slot='card-title'][contains(., 'Simulate')]/ancestor::div[@data-slot='card']"
        " | (//div[@data-slot='card'])[2]"
    )
    SINGLE_NEURON_CARD = (
        By.XPATH,
        "//div[@data-slot='card']//div[@data-slot='card-title'][contains(., 'Single neuron') and not(contains(., 'beta'))]"
    )

    """Model picker: Public/Project tabs."""
    PUBLIC_TAB = (By.XPATH, "//button[@role='tab'][.//span[contains(text(),'Public')] or text()='Public']")
    PROJECT_TAB = (By.XPATH, "//button[@role='tab'][.//span[contains(text(),'Project')] or text()='Project']")

    """Column headers in the model picker table (AG Grid)."""
    COLUMN_HEADERS = (By.CSS_SELECTOR, ".ag-header-cell[role='columnheader']")
    COL_CREATED_BY = (By.CSS_SELECTOR, ".ag-header-cell[col-id='createdBy']")
    COL_REGISTRATION_DATE = (By.CSS_SELECTOR, ".ag-header-cell[col-id='registrationDate']")

    """Table rows (AG Grid)."""
    TABLE_ROWS = (By.CSS_SELECTOR, ".ag-center-cols-container .ag-row[role='row']")
    TABLE_ROW_NAME_CELLS = (By.CSS_SELECTOR, ".ag-center-cols-container .ag-row[role='row'] .ag-cell[col-id='name']")

    """Mini-detail view after clicking a table row."""
    MINI_VIEWER = (By.CSS_SELECTOR, "[data-testid='mini-viewer']")
    MINI_DETAIL_TITLE = (By.CSS_SELECTOR, "[data-testid='mini-viewer'] h1")
    MINI_DETAIL_USE_MODEL_BTN = (By.CSS_SELECTOR, "[data-testid='mini-viewer'] [title='Start simulation']")
