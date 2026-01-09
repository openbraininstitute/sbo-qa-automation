# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class CICDLocators:
    """Locators specifically for CI/CD stability testing."""
    
    # Generic success indicators
    SUCCESS_INDICATORS = [
        (By.CSS_SELECTOR, "[data-testid*='success']"),
        (By.CSS_SELECTOR, "[class*='success']"),
        (By.XPATH, "//*[contains(text(), 'Success') or contains(text(), 'Complete')]")
    ]
    
    # Loading indicators
    LOADING_INDICATORS = [
        (By.CSS_SELECTOR, "[data-testid*='loading']"),
        (By.CSS_SELECTOR, "[class*='loading']"),
        (By.CSS_SELECTOR, "[class*='spinner']"),
        (By.XPATH, "//*[contains(text(), 'Loading') or contains(text(), 'Please wait')]")
    ]
    
    # Error indicators
    ERROR_INDICATORS = [
        (By.CSS_SELECTOR, "[data-testid*='error']"),
        (By.CSS_SELECTOR, "[class*='error']"),
        (By.CSS_SELECTOR, "[class*='alert-danger']"),
        (By.XPATH, "//*[contains(text(), 'Error') or contains(text(), 'Failed')]")
    ]
    
    # Virtual Lab specific elements
    VIRTUAL_LAB_INDICATORS = [
        (By.CSS_SELECTOR, "[data-testid*='virtual-lab']"),
        (By.CSS_SELECTOR, "[data-testid*='lab']"),
        (By.XPATH, "//h1[contains(text(), 'Virtual Lab')]"),
        (By.XPATH, "//div[contains(@class, 'virtual-lab')]")
    ]
    
    # Login success indicators
    LOGIN_SUCCESS_INDICATORS = [
        (By.CSS_SELECTOR, "[data-testid*='user-menu']"),
        (By.CSS_SELECTOR, "[data-testid*='logout']"),
        (By.CSS_SELECTOR, "[class*='user-avatar']"),
        (By.XPATH, "//button[contains(text(), 'Logout') or contains(text(), 'Sign out')]")
    ]