# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By

class ProjectNotebooksLocators:
    OBI_NOTEBOOKS_TAB = (By.XPATH, "//a[normalize-space()='OBI Notebooks']")
    MEMBER_NOTEBOOKS_TAB = (By.XPATH, "//a[normalize-space()='Member Notebooks']")
    TABLE_ELEMENT = (By.XPATH, "//table//thead")
    COLUMN_NAME_HEADER = (By.XPATH, "//th[@aria-label='Name']")
    COLUMN_DESCRIPTION_HEADER = (By.XPATH, "//th[@aria-label='Description']")
    COLUMN_OBJECT_OF_INTEREST_HEADER = (By.XPATH, "//th[@aria-label='Object of interest']")
    COLUMN_SCALE_HEADER = (By.XPATH, "//th[@aria-label='Scale']")
    COLUMN_AUTHORS_HEADER = (By.XPATH, "//th[@aria-label='Authors']")
    COLUMN_CREATION_DATE_HEADER = (By.XPATH, "//th[@aria-label='Creation date']")
    ROW1 = (By.XPATH, "//tr[contains(@class, 'ant-table-row')]")
    SEARCH_NOTEBOOK = (By.CSS_SELECTOR, "input[placeholder='Search for notebooks']")
    TABLE_CONTAINER = (By.CSS_SELECTOR, "#table-container")
    TH = (By.XPATH, "//th")

