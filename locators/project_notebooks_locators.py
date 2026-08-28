# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By

class ProjectNotebooksLocators:
    COLUMN_HEADER = (By.CSS_SELECTOR, ".ag-header-cell[role='columnheader'], thead tr th")
    COLUMN_NAME_HEADER = (
        By.XPATH,
        "//div[contains(@class,'ag-header-cell') and contains(.,'Name')]"
        " | //th[@data-testid='column-header']//div[contains(@class,'columnTitle') and text()='Name']",
    )
    COLUMN_DESCRIPTION_HEADER = (
        By.XPATH,
        "//div[contains(@class,'ag-header-cell') and contains(.,'Description')]"
        " | //th[@data-testid='column-header']//div[contains(@class,'columnTitle') and text()='Description']",
    )
    COLUMN_CONTRIBUTORS_HEADER = (
        By.XPATH,
        "//div[contains(@class,'ag-header-cell') and contains(.,'Contributors')]"
        " | //th[@data-testid='column-header']//div[contains(@class,'columnTitle') and text()='Contributors']",
    )
    COLUMN_REGISTRATION_DATE_HEADER = (
        By.XPATH,
        "//div[contains(@class,'ag-header-cell') and contains(.,'Registration date')]"
        " | //th[@data-testid='column-header']//div[contains(@class,'columnTitle') and text()='Registration date']",
    )
    COLUMN_SCALE_HEADER = (
        By.XPATH,
        "//div[contains(@class,'ag-header-cell') and contains(.,'Scale')]"
        " | //th[@data-testid='column-header']//div[contains(@class,'columnTitle') and text()='Scale']",
    )
    COLUMN_EMPTY_HEADER = (
        By.XPATH,
        "//div[contains(@class,'ag-header-cell') and @col-id='ag-Grid-SelectionColumn']"
        " | //th[@data-testid='column-header']//div[contains(@class,'columnTitle') and text()='']",
    )
    
    # Keep the old creation date locator for backward compatibility if needed
    COLUMN_CREATION_DATE_HEADER = (
        By.XPATH,
        "//div[contains(@class,'ag-header-cell') and contains(.,'Creation date')]"
        " | //th[@data-testid='column-header']//div[contains(@class,'columnTitle') and text()='Creation date']",
    )
    DATA_ROW_KEY_SEARCH_RESULT = (
        By.XPATH,
        "//*[contains(@class,'ag-cell') and contains(.,'Visualize skeletonized neuronal morphologies')]"
        " | //td[contains(@title,'Visualize skeletonized neuronal morphologies')]",
    )
    # Alternative more robust locator for search results
    DATA_ROW_ANY_RESULT = (
        By.CSS_SELECTOR,
        ".ag-center-cols-container .ag-row[role='row'], tbody tr:not([style*='display: none'])",
    )
    DATA_ROW_FILTERED_RESULT = (
        By.XPATH,
        "//*[contains(@class,'ag-cell') and (contains(.,'Visualize') or contains(.,'neuronal'))]"
        " | //tbody/tr/td[contains(text(), 'Visualize') or contains(text(), 'neuronal')]",
    )
    DATA_ROW_NAME = (By.XPATH, "//td[@aria-label='Name']")
    DATA_ROW_DESCRIPTION = (By.XPATH, "//td[@aria-label='Description']")
    DATA_ROW_OBJECT_OF_INTEREST = (By.XPATH, "//td[@aria-label='Object of interest']")
    DATA_ROW_SCALE = (By.XPATH, "//td[@aria-label='Scale']")
    DATA_ROW_AUTHORS = (By.XPATH, "//td[@aria-label='Authors']")
    DATA_ROW_CREATION_DATE = (By.XPATH, "//td[@aria-label='Creation date']")
    FILTER_APPLY_BTN = (By.XPATH, "//button[contains(.,'Apply')]")
    FILTER_CLEAR_BTN = (By.XPATH, "//button[normalize-space()='Clear filters']")
    FILTER_CLOSE_BTN = (By.CSS_SELECTOR, "button[aria-label='Close']")
    FILTER_CREATION_DATE_LABEL = (By.XPATH, "//div[starts-with(@class, 'mb-3 flex cursor-pointer') and contains(text(),"
                                       "'Creation date')]")
    FILTER_DESCRIPTION_LABEL = (By.XPATH, "//div[starts-with(@class, 'mb-3 flex cursor-pointer') and contains(text(),'Description')]")
    FILTER_OBJECT_OF_INTEREST_LABEL = (By.XPATH, "//div[starts-with(@class, 'mb-3 flex cursor-pointer') and contains(text(),'Object of interest')]")
    Filter_NAME_LABEL = (By.XPATH, "//span[contains(text(),'Name')]")
    FILTER_NAME_INPUT = (By.XPATH, "//input[starts-with(@class,'ant-input')]")
    FILTER_NAME_LABEL = (By.XPATH, "//div[starts-with(@class, 'mb-3 flex cursor-pointer') and contains(text(),'Name')]")
    FILTER_CONTRIBUTOR_LABEL = (By.XPATH, "//span[normalize-space()='Contributors']")
    FILTER_CONTRIBUTOR_CHECKBOX = (By.XPATH, "//button[@role='checkbox']")
    FILTER_SCALE_TITLE = (By.XPATH, "//div[normalize-space()='Scale']")
    MEMBER_NOTEBOOKS_TAB = (By.XPATH, "//a[normalize-space()='Member Notebooks']")
    OBI_NOTEBOOKS_TAB = (By.XPATH, "//a[normalize-space()='OBI Notebooks']")
    PAGE_FILTER = (
        By.CSS_SELECTOR,
        "button[aria-label='Filter Name']",
    )
    FILTERS_BADGE_BTN = (
        By.XPATH,
        "//button[@aria-label='Filters' or @title='Filters' or @aria-label='listing-view-filter-button']",
    )
    COLUMN_FILTER_NAME_BTN = (By.CSS_SELECTOR, "button[aria-label='Filter Name']")
    COLUMN_FILTER_INPUT = (
        By.CSS_SELECTOR,
        "input[placeholder='Enter text to match'], input[placeholder*='Enter text']",
    )
    COLUMN_FILTER_APPLY_BTN = (
        By.XPATH,
        "//button[normalize-space()='Apply']",
    )
    COLUMN_FILTER_RESET_BTN = (
        By.XPATH,
        "//button[normalize-space()='Reset']",
    )
    PUBLIC_TAB = (
        By.XPATH,
        "//button[@role='tab'][.//span[contains(text(),'Public')] or normalize-space()='Public']"
        " | //a[normalize-space()='Public']",
    )
    PROJECT_TAB = (
        By.XPATH,
        "//button[@role='tab'][.//span[contains(text(),'Project')] or normalize-space()='Project']"
        " | //a[normalize-space()='Project']",
    )
    ROW1 = (
        By.CSS_SELECTOR,
        ".ag-center-cols-container .ag-row[role='row'], tr.ant-table-row",
    )
    ROWS = (
        By.CSS_SELECTOR,
        ".ag-center-cols-container .ag-row[role='row'], tbody tr.ant-table-row",
    )
    SEARCH_NOTEBOOK = (
        By.XPATH,
        "//button[@aria-label='Open search']",
    )
    SEARCH_NOTEBOOK_OPEN_OR_CLOSE = (
        By.XPATH,
        "//button[@aria-label='Open search' or @aria-label='Close search']",
    )
    SEARCH_INPUT = (
        By.CSS_SELECTOR,
        "input[placeholder*='Search for entities'], input[aria-label='Search'], input[placeholder*='Search']",
    )
    TABLE_ELEMENT = (
        By.CSS_SELECTOR,
        ".ag-header, table thead",
    )
    TABLE_CONTAINER = (
        By.CSS_SELECTOR,
        ".ag-root, .ag-root-wrapper, table[aria-label='listing-view-table']",
    )
    TABLE_BODY_CONTAINER = (
        By.CSS_SELECTOR,
        ".ag-body-viewport, .ag-center-cols-viewport, .ant-table-body",
    )
    TH = (By.CSS_SELECTOR, ".ag-header-cell[role='columnheader'], th")

    # Open notebook mini detail by clicking a name cell (row index is 0-based)
    NOTEBOOK_NAME_CELL = (
        By.CSS_SELECTOR,
        ".ag-center-cols-container .ag-row[role='row'] .ag-cell[col-id='name']",
    )
    MINI_VIEWER = (By.CSS_SELECTOR, "[data-testid='mini-viewer']")

    # Action buttons live in the mini detail panel (titles, not legacy popover data-ids)
    ACTION_MENU_README = (
        By.CSS_SELECTOR,
        "[data-testid='mini-viewer'] button[title='Readme'], button[data-id='readme-btn-0']",
    )
    ACTION_MENU_DOWNLOAD = (
        By.CSS_SELECTOR,
        "[data-testid='mini-viewer'] button[title='Download'], button[data-id='download-btn-0']",
    )
    ACTION_MENU_RUN = (
        By.CSS_SELECTOR,
        "[data-testid='mini-viewer'] button[title='Run notebook'], button[data-id='run-btn-0']",
    )

    # Modal/popup close button (readme ant-modal, dialog, or mini-viewer)
    MODAL_CLOSE_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'ant-modal-wrap') and not(contains(@style,'display: none'))]"
        "//button[@aria-label='Close' or .//span[@aria-label='close']]"
        " | //div[@role='dialog']//button[@aria-label='Close' or .//span[@aria-label='close']]"
        " | //button[@aria-label='Close']"
        " | //*[@data-testid='mini-viewer']//button[.//span[@aria-label='close']]",
    )

