# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By

class ProjectHomeLocators:
    PROJECT_HOME_TITLE = (By.XPATH, "//div[normalize-space()='Project Home']")
    PROJECT_LIBRARY_TITLE = (By.XPATH, "//span[normalize-space()='Project Library']")
    PROJECT_TEAM_TITLE = (By.XPATH, "//span[normalize-space()='Project Team']")
    PROJECT_ACTIVITY_TITLE = (By.XPATH, "//div[normalize-space()='Activity']")
    PROJECT_NOTEBOOKS_TITLE = (By.XPATH, "//span[normalize-space()='Notebooks']")
    PROJECT_EXPLORE_TITLE = (By.XPATH, "//div[normalize-space()='Explore']")
    PROJECT_BUILD_TITLE = (By.XPATH, "//div[normalize-space()='Build']")
    PROJECT_EXPERIMENT_TITLE = (By.XPATH, "//div[normalize-space()='Experiment']")
    PROJECT_ADMIN_TITLE = (By.XPATH, "(//div[normalize-space()='Admin'])[1]")
    MEMBERS_SECTION = (By.XPATH, "(//div[contains(text(),'Members')])[2]")
    PROJECT_NAME_TITLE = (By.XPATH, "//div[normalize-space()='Project Name']")
    MEMBERS_TITLE = (By.XPATH, "//div[@class='text-primary-3' and text()='Members']")
    ADMIN_TITLE = (By.XPATH, "//div[@class='text-primary-3' and text()='Admin']")
    CREATION_DATE_TITLE = (By.XPATH, "//div[@class='text-primary-3' and text()='Creation date']")
    CREDIT_BALANCE_TITLE = (By.XPATH, "//div[@class='text-primary-3' and text()='Credit balance']")
    EDIT_BTN = (By.XPATH, "//button[@data-testid='edit-project-info']")
    EDIT_BTN_UNLOCKED = (By.XPATH, "//span[@aria-label='unlock']")
