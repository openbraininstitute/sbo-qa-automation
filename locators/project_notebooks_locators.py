# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By

class ProjectNotebooksLocators:
    COLUMN_HEADER = (By.XPATH, "//thead/tr/th")
    COLUMN_NAME_HEADER = (By.XPATH, "//th[@data-testid='column-header']/descendant::div[text()='Name']")
    COLUMN_DESCRIPTION_HEADER = (By.XPATH, "//th[@data-testid='column-header']/descendant::div[text()='Description']")
    COLUMN_SCALE_HEADER = (By.XPATH, "//th[@data-testid='column-header']/descendant::div[text()='Scale']")
    COLUMN_CONTRIBUTORS_HEADER = (By.XPATH, "//th[@data-testid='column-header']/descendant::div[text()='Contributors']")
    COLUMN_CREATION_DATE_HEADER = (By.XPATH, "//th[@data-testid='column-header']/descendant::div[text()='Creation date']")
    DATA_ROW_KEY_SEARCH_RESULT = (By.XPATH, "//tr[@class='ant-table-row ant-table-row-level-0' and "
                               "@data-row-key='Metabolism/analysis_notebook.ipynb']")
    DATA_ROW_NAME = (By.XPATH, "//td[@aria-label='Name']")
    DATA_ROW_DESCRIPTION = (By.XPATH, "//td[@aria-label='Description']")
    DATA_ROW_OBJECT_OF_INTEREST = (By.XPATH, "//td[@aria-label='Object of interest']")
    DATA_ROW_SCALE = (By.XPATH, "//td[@aria-label='Scale']")
    DATA_ROW_AUTHORS = (By.XPATH, "//td[@aria-label='Authors']")
    DATA_ROW_CREATION_DATE = (By.XPATH, "//td[@aria-label='Creation date']")
    FILTER_APPLY_BTN = (By.XPATH, "//button[normalize-space()='Apply filters']")
    FILTER_CLEAR_BTN = (By.XPATH, "//button[normalize-space()='Clear filters']")
    FILTER_CLOSE_BTN = (By.CSS_SELECTOR, "button[aria-label='Close']")
    FILTER_CREATION_DATE_LABEL = (By.XPATH, "//div[starts-with(@class, 'mb-3 flex cursor-pointer') and contains(text(),"
                                       "'Creation date')]")
    FILTER_DESCRIPTION_LABEL = (By.XPATH, "//div[starts-with(@class, 'mb-3 flex cursor-pointer') and contains(text(),'Description')]")
    FILTER_OBJECT_OF_INTEREST_LABEL = (By.XPATH, "//div[starts-with(@class, 'mb-3 flex cursor-pointer') and contains(text(),'Object of interest')]")
    FILTER_NAME_INPUT = (By.XPATH, "(//div[@class='mt-10 flex flex-col gap-5']//input[@type='text'])[1]")
    FILTER_NAME_LABEL = (By.XPATH, "//div[starts-with(@class, 'mb-3 flex cursor-pointer') and contains(text(),'Name')]")
    FILTER_AUTHOR_LABEL = (By.XPATH, "//div[starts-with(@class, 'mb-3 flex cursor-pointer') and contains(text(),'Author')]")
    FILTER_SCALE_TITLE = (By.XPATH, "//div[normalize-space()='Scale']")
    FILTER_SELECT_SCALE_INPUT = (By.XPATH, "(//span[@class='ant-select-selection-search'])[1]")
    FILTER_SCALE_MENU_METABOLISM = (By.CSS_SELECTOR, "div[title='Metabolism']")
    MEMBER_NOTEBOOKS_TAB = (By.XPATH, "//a[normalize-space()='Member Notebooks']")
    OBI_NOTEBOOKS_TAB = (By.XPATH, "//a[normalize-space()='OBI Notebooks']")
    PAGE_FILTER = (By.CSS_SELECTOR, "button[aria-label='listing-view-filter-button']")
    PUBLIC_TAB = (By.XPATH, "//a[normalize-space()='Public']")
    PROJECT_TAB = (By.XPATH, "//a[normalize-space()='Project']")
    ROW1 = (By.XPATH, "//tr[contains(@class, 'ant-table-row')]")
    ROWS = (By.XPATH, "//tbody/tr/td")
    SEARCH_NOTEBOOK = (By.XPATH, "//button[@aria-label='Open search']")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Search for entities...']")
    TABLE_ELEMENT = (By.XPATH, "//table//thead")
    TABLE_CONTAINER = (By.XPATH, "//table[@aria-label='listing-view-table']")
    TH = (By.XPATH, "//th")

