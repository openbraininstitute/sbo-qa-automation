# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from pages.home_page import HomePage
from util.util_links_checker import LinkChecker
from locators.build_locators import BuildLocators
from selenium.common import TimeoutException

class Build(HomePage, LinkChecker):
    def __init__(self, browser, wait, base_url):
        super().__init__(browser, wait, base_url)
        self.home_page = HomePage(browser, wait, base_url)

    def go_to_build(self, lab_id: str, project_id: str):
        path = f"/virtual-lab/lab/{lab_id}/project/{project_id}/home"
        try:
            self.go_to_page(path)
            self.wait_for_page_ready(timeout=60)
        except TimeoutException:
            raise RuntimeError(f"Failed to load page at {path} within 60 seconds")
        return self.browser.current_url
