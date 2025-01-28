# # Copyright (c) 2024 Blue Brain Project/EPFL
# #
# # SPDX-License-Identifier: Apache-2.0

import time

from selenium.common import TimeoutException, NoSuchElementException

from locators.sandbox_locatators import SandboxPageLocators
from pages.home_page import HomePage
from selenium.webdriver.support import expected_conditions as EC


class SandboxPage(HomePage):
    def __init__(self, browser, wait, base_url):
        super().__init__(browser, wait, base_url)
        self.home_page = HomePage(browser, wait, base_url)

    def go_to_sandbox_page(self):
        """
        Navigate to the Sandbox page, ensuring the user is logged in.
        """
        print("PRINTING THE BASE URL FROM THE SANDBOX PAGE")
        print(self.base_url)

        sandbox_url = f"{self.base_url}/virtual-lab/sandbox/home"
        print(f"Navigating to: {sandbox_url}")
        self.browser.get(sandbox_url)
        self.wait_for_condition(
            EC.url_contains("/sandbox/home"),
            timeout=15,
            message=f"Expected URL to contain 'sandbox/home', but got: {self.browser.current_url}"
        )

        print(f"After wait: {self.browser.current_url}")
        return self.browser.current_url

    def is_user_logged_in(self):
        """
        Check if the user is already logged in by verifying the current URL or cookies.
        """
        cookies = self.browser.get_cookies()
        logged_in_cookie = any(cookie['name'] == "session" for cookie in cookies)
        return logged_in_cookie and "/virtual-lab" in self.browser.current_url

    def find_sandbox_banner_title(self):
        return self.find_element(SandboxPageLocators.SANDBOX_BANNER_TITLE)

    def find_create_vlab_btn(self):
        return self.find_element(SandboxPageLocators.CREATE_VLAB_BTN)

    def find_form_modal(self):
        try:
            return self.is_visible(SandboxPageLocators.FORM_MODAL)
        except NoSuchElementException:
            return None

    def find_vl_name_field(self):
        return self.find_element(SandboxPageLocators.INPUT_VLAB_NAME)

    def find_vl_desc_field(self):
        return self.find_element(SandboxPageLocators.INPUT_VLAB_DESC)

    def find_vl_email_field(self):
        return self.find_element(SandboxPageLocators.INPUT_VLAB_EMAIL)

    def find_vl_entity_field(self):
        return self.find_element(SandboxPageLocators.INPUT_VLAB_ENTITY)

    def modal_next_btn(self, timeout=15):
        return self.find_element(SandboxPageLocators.MODAL_NEXT_BTN, timeout=timeout)

    def create_vl(self):
        return self.find_element(SandboxPageLocators.CREATE_VL)

    def vl_banner_title(self):
        return self.find_element(SandboxPageLocators.VL_BANNER_TITLE)

    def vl_overview(self):
        return self.find_element(SandboxPageLocators.VL_OVERVIEW)

    def vl_menu_projects(self):
        return self.find_element(SandboxPageLocators.PROJECTS)

    def create_projects_btn(self):
        return self.find_element(SandboxPageLocators.CREATE_PROJECT_BTN)

    def input_project_name(self):
        return self.find_element(SandboxPageLocators.INPUT_PROJECT_NAME)

    def input_project_description(self):
        return self.find_element(SandboxPageLocators.INPUT_PROJECT_DESCRIPTION)

    def save_project_btn(self):
        return self.find_element(SandboxPageLocators.SAVE_PROJECT)