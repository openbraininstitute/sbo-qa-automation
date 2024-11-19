# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

from selenium.common import NoSuchElementException
from selenium.webdriver import Keys

from pages.sandbox_page import SandboxPage
from util.util_base import load_config
import pytest
import time


class TestSandbox:
    @pytest.mark.run(order=1)
    def test_sandbox(self, setup, logger):
        """Test the login process"""
        browser, wait = setup
        try:
            sandbox_page = SandboxPage(browser, wait)
            sandbox_page = sandbox_page.go_to_sandbox_page()
            logger.info("Navigated to the Sandbox Page")

            time.sleep(5)

            # sandbox_title = sandbox_page.find_sandbox_banner_title()

            # assert sandbox_title == "Welcome to Blue Brain Open Platform"


        except NoSuchElementException:
            print(f"An error occurred:")
            raise
