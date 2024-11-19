# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

import time
from locators.sandbox_locatators import SandboxPageLocators
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import CustomBasePage
from pages.home_page import HomePage


class SandboxPage(HomePage):
    def __init__(self, browser, wait):
        super().__init__(browser, wait)
        self.home_page = HomePage(browser, wait)

    def go_to_sandbox_page(self):
        """
        Navigate to the Sandbox page, ensuring the user is logged in.
        """
        if not self.is_user_logged_in():
            raise RuntimeError("User is not logged in. Ensure the login fixture is applied.")

        self.go_to_page("/virtual-lab/sandbox/home")
        return self.browser.current_url

    def is_user_logged_in(self):
        """
        Check if the user is already logged in by verifying the current URL or cookies.
        """
        return "sandbox/home" in self.browser.current_url in self.browser.current_url

    def find_sandbox_banner_title(self):
        return self.wait.until(EC.presence_of_element_located(
            SandboxPageLocators.SANDBOX_BANNER_TITLE))
