# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class SandboxPageLocators:
    SANDBOX_BANNER_TITLE = (By.CSS_SELECTOR, '[data-testid=sandbox-banner-name-element]')
