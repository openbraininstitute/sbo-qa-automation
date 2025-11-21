# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import os

import pytest

from locators.project_home_locators import ProjectHomeLocators
from pages.project_home import ProjectHome


class TestProjectHomePage:
    @pytest.mark.project_page
    def test_project_home(self, setup, logger, login_direct_complete, test_config):
        browser, wait, base_url, lab_id, project_id = login_direct_complete
        project_home = ProjectHome(browser, wait, logger, base_url)
        print(f"DEBUG: Using lab_id={lab_id}, project_id={project_id}")

        project_home.go_to_project_page(lab_id, project_id)
        logger.info("Project Home page loaded successfully")

        skip_onboarding = project_home.skip_onboardin_btn()
        if skip_onboarding.is_displayed():
           skip_onboarding.click()
        logger.info("Clicked on 'Skip' on the overlay")

        project_menu_titles = [
            (ProjectHomeLocators.TOP_MENU_PROJECT_HOME_BTN, "Project Home"),
            (ProjectHomeLocators.TOP_MENU_PROJECT_DATA_BTN, "Data"),
            (ProjectHomeLocators.TOP_MENU_PROJECT_WORKFLOWS_BTN, "Workflows"),
            (ProjectHomeLocators.TOP_MENU_PROJECT_NOTEBOOKS_BTN, "Notebooks"),
            (ProjectHomeLocators.TOP_MENU_PROJECT_REPORTS_BTN, "Reports"),
            (ProjectHomeLocators.TOP_MENU_PROJECT_HELP_BTN, "Help"),
            (ProjectHomeLocators.TOP_MENU_VLAB_MENU, "Virtual Lab"),
            (ProjectHomeLocators.TOP_MENU_PROJECT_CREDITS_BTN, "Credits button"),

        ]

        titles_mapping = dict(project_menu_titles)
        locators = [item[0] for item in project_menu_titles]

        found_titles = project_home.project_menu_titles(locators)
        missing_elements = []

        for locator, element in found_titles.items():
            title_name = titles_mapping[locator]

            if not element:
                logger.warning(f"'{title_name}' was not found on the page.")
                print(f"'{title_name}' was not found on the page.")
                missing_elements.append(f"'{title_name}' was not found")
            elif not element.is_displayed():
                logger.warning(f"'{title_name}' was found, but it is not visible.")
                print(f"'{title_name}' was found, but it is not visible.")
                missing_elements.append(f"'{title_name}' was not visible")
            else:
                logger.info(f"'{title_name}' is displayed: {element.text}")
                print(f"'{title_name}' is displayed: {element.text}")

        if missing_elements:
            missing_summary = "\n".join(missing_elements)
            raise AssertionError(f"The following menu items are missing or not visible:\n{missing_summary}")

        edit_btn = project_home.edit_btn()
        assert edit_btn.is_displayed(), "Edit button is not displayed"
        logger.info("Edit button is found")

        edit_btn.click()
        logger.info("Edit button clicked")

        edit_btn_unlocked = project_home.edit_btn_unlock()
        assert edit_btn_unlocked.is_displayed(), "Edit button is not locked"
        logger.info("It is possible to edit the project name")
        edit_btn_unlocked.click()
        logger.info("Project editing is saved")

        left_menu_project_overview_tab = project_home.project_overview_tab()
        assert left_menu_project_overview_tab.is_displayed()
        logger.info("Left menuL: 'Overview tab' is displayed")

        left_menu_members_tab = project_home.members_tab()
        assert left_menu_members_tab.is_displayed()
        logger.info("Left menu: 'Members' tab is displayed")

        left_menu_members_tab = project_home.credits_tab()
        assert left_menu_members_tab.is_displayed()
        logger.info("Left menu: 'Credits' tab is displayed")


