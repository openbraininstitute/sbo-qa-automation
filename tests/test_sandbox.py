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
            # vl_email_field.send_keys("ayima.okeeva@openbrainintitute.org").send_keys(Keys.ENTER)
            for char in "ayima.okeeva@openbraininstitute.org":
                vl_email_field.send_keys(char)
                time.sleep(0.1)
            vl_entity_field = sandbox_page.find_vl_entity_field()
            for char in "OBI":
                vl_entity_field.send_keys(char)
                time.sleep(0.1)
            time.sleep(5)
            modal_next_btn = sandbox_page.modal_next_btn(timeout=15)
            find_text = modal_next_btn.text
            print(find_text)
            assert modal_next_btn.is_enabled(),  "The Next button is disabled!"
            # print("Submit button state:", modal_next_btn.get_attribute("disabled"))
            # modal_next_btn.is_displayed(), "The submit button is not found"
            browser.execute_script("arguments[0].click();", modal_next_btn)
            time.sleep(4)
            create_vl = sandbox_page.create_vl().click()
            time.sleep(25)


        except NoSuchElementException:
            print(f"An error occurred:")
            raise
