# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class ExploreModelPageLocators:
    AI_ASSISTANT_PANEL = (By.XPATH, "//button[starts-with(@class, 'literature-suggestions')]")
    BRAIN_REGION_PANEL = (By.XPATH, "(//div[@class='flex h-screen flex-col bg-primary-8'])[1]")
    BR_SEARCH_FIELD_TYPE = (By.XPATH, "//span[@class='ant-select-selection-search']")
    BR_SEARCH_REGION_SEARCH_FIELD = (By.XPATH, "//div[@class='ant-select-selector']")
    BR_CEREBRUM_TITLE = (By.XPATH, "//button[starts-with(@class, 'flex h-auto "
                                   "items-center')]/span[contains(.,'Cerebrum')]")
    CLOSE_BRAIN_REGION_PANEL_BTN = (By.XPATH, "(//button[starts-with(@class, 'ant-btn')]/span["
                                              "@class='ant-btn-icon'])[1]")
    EMODEL_TAB = (By.XPATH, "//li[@title='E-model']")
    ME_MODEL_TAB = (By.XPATH, "//li[@title='ME-model']")
    SEARCH_REGION = (By.XPATH, "//input[@class='ant-select-selection-search-input']")
    SELECTED_BRAIN_REGION = (By.XPATH, "//h1[@title='Isocortex']/span[text()='Isocortex']")
