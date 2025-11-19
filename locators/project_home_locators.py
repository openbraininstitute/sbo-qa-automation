# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By

class ProjectHomeLocators:
    SKIP_ONBOARDING_BTN = (By.XPATH, "//button[normalize-space()='Skip']")
    TOP_MENU_PROJECT_HOME_BTN = (By.CSS_SELECTOR, "#workspace-home")
    TOP_MENU_PROJECT_DATA_BTN = (By.CSS_SELECTOR, "#workspace-explore-data")
    TOP_MENU_PROJECT_WORKFLOWS_BTN = (By.CSS_SELECTOR, "#workspace-workflows")
    TOP_MENU_PROJECT_NOTEBOOKS_BTN = (By.CSS_SELECTOR, "#workspace-notebooks")
    TOP_MENU_PROJECT_REPORTS_BTN = (By.CSS_SELECTOR, "#workspace-reports")
    TOP_MENU_PROJECT_HELP_BTN = (By.CSS_SELECTOR, "#workspace-help")
    TOP_MENU_VLAB_MENU = (By.CSS_SELECTOR, "#virtual-lab-menu-button")
    TOP_MENU_PROJECT_CREDITS_BTN = (By.CSS_SELECTOR, "#workspace-project-credits")
    PROJECT_DESCRIPTION = (By.CSS_SELECTOR, "#project-form")
    PROJECT_EDIT_BTN = (By.CSS_SELECTOR, "span[aria-label='edit']")
    PROJECT_EDIT_REVERSE = (By.CSS_SELECTOR, "button[aria-label='revert changes']")
    PROJECT_DESC_SHOW_MORE_BTN = (By.XPATH, "//button[normalize-space()='Show more']")
    PROJECT_MEMBERS_TAB = (By.XPATH, "//a[normalize-space()='Members']")
    PROJECT_OVERVIEW_TAB = (By.XPATH, "//a[normalize-space()='Overview']")
    PROJECT_CREDITS_TAB = (By.XPATH, "//a[normalize-space()='Credits']")
