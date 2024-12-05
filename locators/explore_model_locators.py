# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class ExploreModelPageLocators:
    EMODEL_TAB = (By.XPATH, "//li[@title='E-model']")
    ME_MODEL_TAB = (By.XPATH, "//li[@title='ME-model']")