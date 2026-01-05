# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait

from locators.login_locators import LoginPageLocators
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import CustomBasePage
from selenium.webdriver.common.by import By


class LoginPage(CustomBasePage):
    def __init__(self, browser, wait, lab_url, logger):
        super().__init__(browser, wait, lab_url)
        self.logger = logger

    def navigate_to_homepage(self):
        self.browser.delete_all_cookies()
        print(f"INFO: From pages/login_page.py 'self.base_url': {self.lab_url}")
        target_url = self.lab_url
        self.browser.get(target_url)
        self.logger.info(f"INFO: Target URL is {target_url}")
        try:
            WebDriverWait(self.browser, 30).until(
                lambda d: "openid-connect" in d.current_url or "auth" in d.current_url
            )
            self.logger.info(f"INFO: Successfully reached {self.browser.current_url}")
        except TimeoutException:
            self.logger.error(f"ERROR: Timeout while waiting for URL containing 'openid-connect'")
        self.logger.info(f"INFO: target_url from pages/login_page.py:, {target_url}")
        self.logger.info(f"INFO: Starting URL from pages/login_page.py:, {self.browser.current_url}")
        return target_url

    def wait_for_login_complete(self, timeout=30):
        """Wait for login completion by checking a URL or element."""
        try:
            self.wait.until(EC.url_contains("app/virtual-lab"))
            print(f"INFO: Successfully redirected to {self.browser.current_url}")
        except TimeoutException:
            print(
                f"Timeout waiting for URL to contain 'virtual-lab'. Current URL: "
                f"{self.browser.current_url}")
            raise

    def find_form_container(self, timeout=10):
        return self.find_element(LoginPageLocators.FORM_CONTAINER, timeout=timeout)

    def find_username_field(self):
        return self.element_visibility(LoginPageLocators.USERNAME_FIELD)

    def find_password_field(self):
        return self.element_visibility(LoginPageLocators.PASSWORD_FIELD)

    def find_logout_button(self):
        return self.wait.until(EC.element_to_be_clickable(LoginPageLocators.LOGOUT))

    def submit_button(self):
        return self.element_to_be_clickable(LoginPageLocators.SUBMIT_BUTTON)

    def perform_login(self, username, password):
        self.logger.info("Performing login with the provided credentials.")

        self.wait.until(EC.url_contains("/auth/realms/"))
        print(f"DEBUG: Current URL: {self.browser.current_url}")

        self.wait.until(EC.presence_of_element_located((By.ID, "kc-form-wrapper")))

        self.make_form_visible()
        self.wait.until(EC.visibility_of_element_located((By.ID, "username")))
        self.wait.until(EC.visibility_of_element_located((By.ID, "password")))

        username_field = self.browser.find_element(By.ID, "username")
        password_field = self.browser.find_element(By.ID, "password")
        username_field.send_keys(username)
        password_field.send_keys(password)
        password_field.send_keys(Keys.ENTER)
        self.wait.until(EC.url_contains("app/virtual-lab"))
        print("DEBUG: Login completed successfully.")

    def make_form_visible(self):
        """Use JavaScript to make the hidden form visible by removing 'display:none'."""
        form_container = self.find_form_container()
        if not form_container:
            raise RuntimeError("Login form container not found in DOM")

        self.browser.execute_script("""
                arguments[0].classList.remove('display-none', 'hidden');
                arguments[0].style.display = 'block';
                arguments[0].style.visibility = 'visible';
            """, form_container)

        print("DEBUG: Form container made visible via JavaScript.")


    def ensure_element_interactable(self, element):
        """Ensure the element is visible and interactable, even if hidden."""
        if not element.is_displayed():
            self.browser.execute_script("arguments[0].style.display = 'block';", element)
        if not element.is_enabled():
            raise Exception(f"Element {element} is not enabled for interaction.")

    def terms_modal(self):
        return self.find_element(LoginPageLocators.MODAL_TOR)

    def terms_modal_link(self):
        return self.find_element(LoginPageLocators.MODAL_HREF_TERMS)

    def terms_modal_continue(self):
        return self.find_element(LoginPageLocators.MODAL_CONTINUE_BTN)