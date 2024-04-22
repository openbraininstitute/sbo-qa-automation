# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class HomePageLocators:
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Login')]")
    EXPLORE_TITLE = (By.XPATH, "//div[text()='Explore']")
    BUILD_TITLE = (By.XPATH, "//div[text()='Build']")
    SIMULATE_TITLE = (By.XPATH, "//div[text()='Simulate']")
    BUILD_URL = (By.XPATH, '//a[@href="/mmb-beta/build/load-brain-config"]')