# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By

class ExploreMeModelLocators:
    EXPLORE_TAB = (By.XPATH, "//a[normalize-space()='Explore me']")
    MODEL_NAME_HEADER = (By.XPATH, "//h2[text()='Model name']")
    MODEL_DESCRIPTION_HEADER = (By.XPATH, "//h2[text()='Model description']")
    MODEL_DESCRIPTION_TEXT = (By.XPATH, "//div[@class='col-md-12']")
    MODEL_AUTHOR_HEADER = (By.XPATH, "//h2[text()='Author']")
    MODEL_AUTHOR_TEXT = (By.XPATH, "//div[@class='col-md-12']")
    MODEL_VERSION_HEADER = (By.XPATH, "//h2[text()='Version']")