# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class LoginPageLocators:
    FORM_CONTAINER = (By.CSS_SELECTOR, "div.form-container.display-none")
    LOGIN_FORM = (By.XPATH, "//form[@class='login-form']")
    LOGIN_BUTTON = (By.XPATH, "//a[contains(.,'Log in')]")
    LOGOUT = (By.XPATH, "//button[@type='button' and text()='Log out']")
    MODAL_TOR = (By.XPATH, "//div[starts-with(@class, 'terms-of-use-acceptance_body')]")
    MODAL_HREF_TERMS = (By.XPATH, "//a[@href='/terms']")
    MODAL_CONTINUE_BTN = (By.XPATH, "//button[starts-with(@class, 'terms-of-use-acceptance') and text()='Continue']")
    PASSWORD_FIELD = (By.XPATH, "//fieldset[@class='login-form-group']/input[@id='password']")
    SIGN_IN = (By.XPATH, "//input[@type='submit']")
    SUBMIT = (By.CSS_SELECTOR, ".login-form-submit")
    SUBMIT_BUTTON = (By.XPATH, "//input[@name='login']")
    USERNAME_FIELD = (By.XPATH, "//fieldset[@class='login-form-group']/input[@id='username']")
