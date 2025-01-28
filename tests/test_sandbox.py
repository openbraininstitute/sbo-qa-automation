# # Copyright (c) 2024 Blue Brain Project/EPFL
# #
# # SPDX-License-Identifier: Apache-2.0

import os
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys

from pages.sandbox_page import SandboxPage
import pytest
import time

# Skip module if `SKIP_TESTS` environment variable is set
if os.getenv("SKIP_TESTS") == "1":
    pytest.skip("Skipping Morphology tests temporarily.", allow_module_level=True)


@pytest.mark.usefixtures("setup", "logger", "login")
class TestSandbox:
    def test_sandbox(self, setup, logger):
        """Test the login process"""
        browser, wait, base_url = setup
        try:
            sandbox_page = SandboxPage(browser, wait, base_url)
            sandbox_url = sandbox_page.go_to_sandbox_page()
            print(f"Navigated to the Sandbox Page: {sandbox_url}")
            assert "/sandbox/home" in sandbox_url, "Failed to navigate t othe sandbox page"
            logger.info(f"Navigated to the Sandbox Page: {browser.current_url}")

            sandbox_title = sandbox_page.find_sandbox_banner_title()
            title = sandbox_title.text
            assert title == "Welcome to Blue Brain Open Platform"

            create_vlab = sandbox_page.find_create_vlab_btn().click()
            logger.info("Create your Virtual Lab button is clicked.")
            form_modal = sandbox_page.find_form_modal()
            assert form_modal is not None, "Modal is not found."


            vl_name = sandbox_page.find_vl_name_field()
            unique_name = f"UI Tests Virtual Lab {int(time.time())}"
            vl_name.send_keys(unique_name)

            vl_desc_field = sandbox_page.find_vl_desc_field()
            for char in "This VL is for UI automated tests":
                vl_desc_field.send_keys(char)
                time.sleep(0.1)

            vl_email_field = sandbox_page.find_vl_email_field()
            for char in "ayima.okeeva@openbraininstitute.org":
                vl_email_field.send_keys(char)
                time.sleep(0.1)
            vl_entity_field = sandbox_page.find_vl_entity_field()
            for char in "OBI":
                vl_entity_field.send_keys(char)
                time.sleep(0.1)
            time.sleep(3)
            modal_next_btn = sandbox_page.modal_next_btn(timeout=15)
            assert modal_next_btn.is_enabled(),  "The Next button is disabled!"
            browser.execute_script("arguments[0].click();", modal_next_btn)
            create_vl = sandbox_page.create_vl().click()
            # vl_banner_title = sandbox_page.vl_banner_title()
            logger.info("New Virtual Lab is created")
            vl_overview = sandbox_page.vl_overview()
            assert vl_overview.is_displayed(), "VL overview is not displayed"
            vl_menu_projects = sandbox_page.vl_menu_projects()
            logger.info("In the VL menu, 'Projects' title is displayed")
            create_project_btn = sandbox_page.create_projects_btn()
            create_project_btn.click()
            logger.info("Clicked to create a new project")

            project_name = sandbox_page.input_project_name()
            counter = getattr(sandbox_page, "project_counter", 0)
            sandbox_page.project_counter = counter + 1
            unique_name = f"Project.{sandbox_page.project_counter}"
            for char in unique_name:
                project_name.send_keys(char)
                time.sleep(0.1)

            project_description = sandbox_page.input_project_description()
            unique_description = f" Project Description for {unique_name}"
            for char in unique_description:
                project_description.send_keys(char)
                time.sleep(0.1)
            logger.info("New project with its description are created.")
            click_save_project = sandbox_page.save_project_btn()
            browser.execute_script("arguments[0].click();", click_save_project)
            time.sleep(20)
            logger.info("The new project creation has been saved")
        except NoSuchElementException:
            print(f"An error occurred:")
            raise
