# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import random
import time
import uuid
from datetime import datetime

from selenium.common import ElementNotVisibleException
from selenium.webdriver import Keys

from pages.about_page import AboutPage
from pages.build import Build
from pages.vl_overview import VLOverview
import pytest

class TestAbout:
    def test_about(self, visit_public_pages, logger):
        _visit, base_url  = visit_public_pages
        browser, wait = _visit("/about")
        about_page = AboutPage(browser, wait, base_url, logger=logger)

        about_page.go_to_page()
        assert "About" in browser.title

