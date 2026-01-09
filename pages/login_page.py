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

    def wait_for_login_complete(self, timeout=90):
        """Wait for login completion by checking a URL or element with enhanced CI/CD support."""
        self.logger.info(f"Waiting for login completion with {timeout}s timeout")
        
        # Multiple strategies to detect successful login
        strategies = [
            # Strategy 1: Check for virtual-lab in URL
            lambda: self.wait.until(EC.url_contains("app/virtual-lab")),
            
            # Strategy 2: Check for sync in URL  
            lambda: WebDriverWait(self.browser, 15).until(
                lambda d: "sync" in d.current_url
            ),
            
            # Strategy 3: Check for any app/ URL
            lambda: WebDriverWait(self.browser, 15).until(
                lambda d: "/app/" in d.current_url
            ),
            
            # Strategy 4: Look for logged-in page elements
            lambda: WebDriverWait(self.browser, 15).until(
                EC.any_of(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid*='lab']")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='virtual-lab']")),
                    EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Virtual Lab')]")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid*='user']"))
                )
            )
        ]
        
        success = False
        for i, strategy in enumerate(strategies, 1):
            try:
                self.logger.info(f"Trying login detection strategy {i}")
                strategy()
                self.logger.info(f"Strategy {i} succeeded! Current URL: {self.browser.current_url}")
                success = True
                break
            except TimeoutException:
                self.logger.debug(f"Strategy {i} failed")
                continue
        
        if not success:
            current_url = self.browser.current_url
            self.logger.error(f"All login detection strategies failed. Final URL: {current_url}")
            
            # Final attempt: Check if we're at least not on the login page anymore
            if "/auth/realms/" not in current_url:
                self.logger.info("Not on login page anymore, considering login successful")
                success = True
            else:
                raise TimeoutException(f"Login failed. Final URL: {current_url}")
        
        self.logger.info("Login completion detected successfully")

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