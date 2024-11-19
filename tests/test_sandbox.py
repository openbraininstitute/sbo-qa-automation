# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

from selenium.common import NoSuchElementException
from pages.sandbox_page import SandboxPage
import pytest
import time


@pytest.mark.usefixtures("setup", "logger", "login")
class TestSandbox:
    @pytest.mark.run(order=1)
    def test_sandbox(self, setup, logger):
        """Test the login process"""
        browser, wait = setup
        try:
            sandbox_page = SandboxPage(browser, wait)
            time.sleep(10)
            assert "sandbox/home" in browser.current_url, (f"Expected 'sandbox/home' in URL, but "
                                                           f"got: {browser.current_url}")
            logger.info("Navigated to the Sandbox Page")

            sandbox_title = sandbox_page.find_sandbox_banner_title()
            title = sandbox_title.text
            assert title == "Welcome to Blue Brain Open Platform"

        except NoSuchElementException:
            print(f"An error occurred:")
            raise
