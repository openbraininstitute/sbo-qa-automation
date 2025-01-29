## Copyright (c) 2024 Blue Brain Project/EPFL
## Copyright (c) 2025 Open Brain Institute
## SPDX-License-Identifier: Apache-2.0

import time
import uuid
from datetime import datetime


from pages.vl_overview import VLOverview
import pytest


class TestVLOverview:
    # @pytest.mark.explore_page
    @pytest.mark.run(order=3)
    def test_vl_overview(self, setup, login, logger):
        """
        The commented out code below is pending changes in the platform.
        """
        browser, wait, base_url = setup
        vl_overview = VLOverview(browser, wait, base_url)
        vl_overview.go_to_vloverview()
        logger.info("Virtual Lab Overview page is loaded")

        vl_overview_title = vl_overview.vl_overview_title()
        logger.info("'Your Virtual Labs and Projects' title is found")

        vl_banner = vl_overview.vl_banner().click()
        logger.info("Found Virtual lab banner and clicked")
        create_project = vl_overview.create_project().click()
        logger.info("Redirected to the Virtual lab and clicked on 'Create a project button'")

        unique_name = f"Project-{uuid.uuid4().hex[:8]}"
        logger.info(f"Generated unique project name: {unique_name}")

        project_name =  vl_overview.input_project_name()
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
        else:
            logger.error("Save button was not found or was not clickable")
        logger.info("New project with its description are created.")
    time.sleep(20)
