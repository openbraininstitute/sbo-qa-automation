# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class LoginPageLocators:
    LOGIN_BUTTON = (By.XPATH, "//button[@type='button' and @aria-label='Log in']")
    USERNAME = (By.XPATH, '//input[@id="username"]')
    PASSWORD = (By.XPATH, "//input[@id='password']")
    LOGOUT = (By.XPATH, "//button[@type='button' and text()='Log out']")
    GITHUB_BTN = (By.XPATH, "//a[@id='social-github']//span[contains(text(),'GitHub')]")
    SIGN_IN = (By.XPATH, "//input[@value='Sign In']")