# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import pytest

from locators.project_home_locators import ProjectHomeLocators
from pages.project_home import ProjectHome


class TestProjectHomePage:
    @pytest.mark.project_page
    def test_project_home(self, setup, login, logger, test_config):
        browser, wait, base_url, lab_id, project_id = setup
        project_home = ProjectHome(browser, wait, logger, base_url)
        print(f"DEBUG: Using lab_id={lab_id}, project_id={project_id}")

        project_home.go_to_project_page(lab_id, project_id)
        logger.info("Project Home page loaded successfully")

        project_menu_titles = [
            (ProjectHomeLocators.PROJECT_HOME_TITLE, "Project Home"),
            (ProjectHomeLocators.PROJECT_LIBRARY_TITLE, "Project Library"),
            (ProjectHomeLocators.PROJECT_TEAM_TITLE, "Project Team"),
            (ProjectHomeLocators.PROJECT_ACTIVITY_TITLE, "Activity"),
            (ProjectHomeLocators.PROJECT_NOTEBOOKS_TITLE, "Project Notebooks"),
            (ProjectHomeLocators.PROJECT_EXPLORE_TITLE, "Explore"),
            (ProjectHomeLocators.PROJECT_BUILD_TITLE, "Build"),
            (ProjectHomeLocators.PROJECT_EXPERIMENT_TITLE, "Experiment"),
            (ProjectHomeLocators.PROJECT_ADMIN_TITLE, "Admin"),
            (ProjectHomeLocators.MEMBERS_SECTION, "Members"),
            (ProjectHomeLocators.PROJECT_NAME_TITLE, "Project Name"),
            (ProjectHomeLocators.MEMBERS_TITLE, "Members"),
            (ProjectHomeLocators.ADMIN_TITLE, "Admin"),
            (ProjectHomeLocators.CREATION_DATE_TITLE, "Creation Date"),
            (ProjectHomeLocators.CREDIT_BALANCE_TITLE, "Credit Balance"),
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


