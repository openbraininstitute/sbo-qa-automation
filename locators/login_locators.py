# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class LoginPageLocators:
    LOGIN_BUTTON = (By.XPATH, "//a[contains(.,'Log in')]")
    USERNAME = (By.XPATH, "//input[@autocomplete='username']")
    PASSWORD = (By.XPATH, "//input[@type='password']")
    LOGOUT = (By.XPATH, "//button[@type='button' and text()='Log out']")
    GITHUB_BTN = (By.XPATH, "//a[@class='social-link']")
    SIGN_IN = (By.XPATH, "//input[@type='submit']")
