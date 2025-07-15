# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import pytest
from pages.home_page import HomePage


@pytest.mark.usefixtures("setup", "logger")
class TestOldHomepage:
    def test_homepage(self, setup):
        browser, wait, base_url, *_ = setup
        home_page = HomePage(browser, wait, base_url)

