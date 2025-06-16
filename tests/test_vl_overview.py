# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import uuid

from pages.vl_overview import VLOverview
import pytest


class TestVLOverview:
    # @pytest.mark.explore_page
    @pytest.mark.run(order=3)
    def test_vl_overview(self, setup, login, logger):
        """
        Tests Virtual Lab Home
        """
        browser, wait, base_url, lab_id, project_id = setup
        vl_overview = VLOverview(browser, wait, base_url)
        vl_overview.go_to_vloverview(lab_id, project_id)
        logger.info("Virtual Lab Overview page is loaded")

        vl_overview_title = vl_overview.vl_overview_title()
        logger.info("'Your Virtual Labs and Projects' title is found")

        vl_banner_name_label = vl_overview.vl_banner_name_label()
        assert vl_banner_name_label.is_displayed(), "The VLAB name title is not displayed."
        logger.info("VLAB name title is displayed")

        # vl_banner_description_value = vl_overview.vl_banner_description_value()

        vl_banner_admin_label = vl_overview.vl_banner_admin_label()
        assert vl_banner_admin_label, "The VLAB admin label is not found."
        logger.info(f"The VLAB admin label is found.")

        menu_team_label = vl_overview.menu_team_label()
        assert menu_team_label, "The menu team label is not found."
        logger.info("The menu team label is found.")

        menu_projects_label = vl_overview.menu_projects_label()
        assert menu_projects_label, "The menu projects label is not found."
        logger.info("The menu projects label is found.")

        menu_admin_label = vl_overview.menu_admin_label()
        assert menu_admin_label, "The menu admin label is not found."
        logger.info("The menu admin label is found.")

        vl_banner_creation_date = vl_overview.vl_banner_creation_date()
        assert vl_banner_creation_date, "VLAB banner creation date label is not found."
        logger.info("The VLAB creation date label is found.")

        vl_banner_credit_balance_label = vl_overview.vl_banner_credit_balance_label()
        assert vl_banner_credit_balance_label, "VLAB credit balance label is not found."
        logger.info("VLAB credit balance is found.")

        members_section_title = vl_overview.members_section_title()
        assert members_section_title, "Members section title is not found."
        logger.info("Members section title is found.")

        members_section_admin_name = vl_overview.members_section_admin_name()
        assert members_section_admin_name is not None, "Members section admin name is not found."
        logger.info("Members section admin name is found.")
        
        
        
        

        """
        logger.info("Redirected to the Virtual lab and clicked on 'Create a project button'")
        unique_name = f"Project-{uuid.uuid4().hex[:8]}"
        logger.info(f"Generated unique project name: {unique_name}")

        project_name =  vl_overview.input_project_name()
        # time.sleep(0.1) is required to simulate human typing
        for char in unique_name:
            project_name.send_keys(char)
            time.sleep(0.1)

        project_description = vl_overview.input_project_description()
        unique_description = f" Project Description for {unique_name}"
        for char in unique_description:
            project_description.send_keys(char)
            time.sleep(0.1)

        project_member_icon = vl_overview.project_member_icon()
        logger.info("Project member icon is found")
        add_member_btn = vl_overview.add_member_btn()
        save_text = vl_overview.save_text()
        logger.info("Text 'Save' button is found")
        save_project_btn = vl_overview.save_project_btn()

        enable_save_btn = vl_overview.save_project_btn_clickable()

        if enable_save_btn:
            print(f"Button Enabled: {enable_save_btn.is_enabled()}")
            enable_save_btn.click()
            # time.sleep(120)
        else:
            logger.error("Save button was not found or was not clickable")
        logger.info("New project with its description are created.")
        """