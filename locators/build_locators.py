# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By

class BuildLocators:
    BUILD_MENU_TITLE = (By.XPATH, "//div[@class='mx-4' and text()='Build']")
    NEW_MODEL_TAB = (By.XPATH, "//label[@for='scope-filter-new']")
    SINGLE_NEURON_TITLE = (By.XPATH, "//div[text()='Single neuron']")
    BUILD_SINGLE_NEURON_BTN = (By.XPATH, "//button[@type='button' and contains(text(), 'Build')]")
    FORM_BUILD_NEURON_TITLE = (By.XPATH, "//div[contains(text(), 'Build a new single neuron')]")
    FORM_NAME = (By.XPATH, "//input[@id='name']")
    FORM_DESCRIPTION = (By.XPATH, "//textarea[@id='description']")
    FORM_BRAIN_REGION = (By.XPATH, "//input[@id='brainRegion']")
    START_BUILDING_BTN = (By.XPATH, "//button[@type='submit']/span[text()='Start building']")
