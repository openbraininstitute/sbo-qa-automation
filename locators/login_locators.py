# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class LoginPageLocators:
    FORM_CONTAINER = (By.ID, "kc-form-wrapper")
    LOGIN_FORM = (By.ID, "kc-form-login")
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    SUBMIT_BUTTON = (By.ID, "kc-login")
    LOGOUT = (By.XPATH, "//button[normalize-space()='Log out']")
    MODAL_TOR = (By.XPATH, "//div[starts-with(@class, 'terms-of-use-acceptance_body')]")
    MODAL_HREF_TERMS = (By.XPATH, "//a[@href='/terms']")
    MODAL_CONTINUE_BTN = (By.XPATH, "//button[starts-with(@class, 'terms-of-use-acceptance') and text()='Continue']")

