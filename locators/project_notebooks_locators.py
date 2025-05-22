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
    TH = (By.XPATH, "//th")

