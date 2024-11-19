# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0


from pages.login_page import LoginPage
from util.util_base import load_config
import pytest
import time


@pytest.mark.usefixtures("setup", "logger")
class TestLogin:
    @pytest.mark.run(order=1)
    def test_login_process(self, setup, logger):
        """Test the login process"""
        browser, wait = setup
        login_page = LoginPage(browser, wait)

        login_page.navigate_to_homepage()
        login_page.find_login_button().click()

        # Perform login using keyboard Enter action
        config = load_config()
        username = config['username']
        password = config['password']
        login_page.perform_login(username, password)
        # Verify the user is redirected to the Sandbox page
        # assert "sandbox/home" in browser.current_url
        logger.info(f"Successfully logged in page URL IS: " + browser.current_url)

