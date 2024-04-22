# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class CustomBasePageLocators:
    PAGE_LOAD = (By.XPATH, "//a[@href='https://bbp.epfl.ch/mmb-beta']")
