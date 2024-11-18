# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

import time
from locators.login_locators import LoginPageLocators
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import CustomBasePage


class LoginPage(CustomBasePage):
    def __init__(self, browser, wait):
        super().__init__(browser, wait)

    def navigate_to_homepage(self):
        self.browser.delete_all_cookies()
        target_url = "https://openbluebrain.com/mmb-beta/dev"
        # target_url = "https://staging.openbluebrain.com/"
        self.browser.get(target_url)
        print("Final URL:", self.browser.current_url)
        return self.browser.current_url

    # def find_github_btn(self):
    # return self.wait.until(EC.element_to_be_clickable(LoginPageLocators.GITHUB_BTN))
    # return self.wait.until(EC.element_to_be_clickable(LoginPageLocators.TEST_LOGIN))

    def find_login_button(self):
        return self.wait.until(EC.element_to_be_clickable(LoginPageLocators.LOGIN_BUTTON))

    def login(self):
        # self.wait.until(EC.presence_of_element_located(LoginPageLocators.USERNAME))
        self.wait.until(EC.presence_of_element_located(LoginPageLocators.TEST_USERNAME))
        # self.wait.until(EC.presence_of_element_located(LoginPageLocators.PASSWORD))
        self.wait.until(EC.presence_of_element_located(LoginPageLocators.TEST_PASSWORD))

    def wait_for_login_complete(self):
        """Wait for login to complete by checking URL change"""
        self.wait.until(EC.url_contains("mmb-beta/virtual-lab"))

    def find_username_field(self):
        # return self.wait.until(EC.presence_of_element_located(LoginPageLocators.USERNAME))
        return self.wait.until(EC.presence_of_element_located(LoginPageLocators.TEST_USERNAME))

    def find_password_field(self):
        # return self.wait.until(EC.presence_of_element_located(LoginPageLocators.PASSWORD))
        return self.wait.until(EC.presence_of_element_located(LoginPageLocators.TEST_PASSWORD))

    def find_signin_button(self):
        return self.wait.until(EC.element_to_be_clickable(LoginPageLocators.SIGN_IN))

    def find_logout_button(self):
        return self.wait.until(EC.element_to_be_clickable(LoginPageLocators.LOGOUT))

    def find_submit(self):
        return self.wait.until(EC.element_to_be_clickable(LoginPageLocators.SUBMIT))
