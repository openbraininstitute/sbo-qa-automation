# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

import pytest

from pages.login_page import LoginPage


@pytest.mark.usefixtures("setup", "logger", "login")
class TestLogin:
    @pytest.mark.run(order=1)
    def test_login_process(self, setup, logger, test_config):
        """Test the login process"""
        browser, wait, base_url, lab_id, project_id = setup
        # Validate the user is logged in
        print("Login process completed via fixture")
        assert "/virtual-lab" in browser.current_url, \
            f"Unexpected URL after login: {browser.current_url}"
        logger.info(f"Successfully logged in. Current page URL: {browser.current_url}")
        browser.execute_script("window.localStorage.clear();")




