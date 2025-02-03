# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from pages.home_page import HomePage
from util.util_links_checker import LinkChecker
from locators.vlab_overview_locators import VLOverviewLocators
from selenium.common import TimeoutException


class VLOverview(HomePage, LinkChecker):
    def __init__(self, browser, wait, base_url):
        super().__init__(browser, wait, base_url)
        self.home_page = HomePage(browser, wait, base_url)


    def go_to_vloverview(self):
        try:
            self.go_to_page("/virtual-lab/")
            self.wait_for_page_ready(timeout=60)
        except TimeoutException:
            raise RuntimeError("The Explore Morphology page did not load within 60 seconds")
        return self.browser.current_url

    def vl_overview_title(self):
        return self.find_element(VLOverviewLocators.VLOVERVIEW_TITLE)

    def vl_banner(self):
        return self.find_element(VLOverviewLocators.VL_BANNER)

    def create_project(self):
        return self.find_element(VLOverviewLocators.VL_CREATE_PROJECT_BTN)

    def input_project_name(self):
        return self.find_element(VLOverviewLocators.INPUT_PROJECT_NAME)

    def input_project_description(self):
        return self.find_element(VLOverviewLocators.INPUT_PROJECT_DESCRIPTION)

    def project_member_icon(self):
        return self.find_element(VLOverviewLocators.PROJECT_MEMBER_ICON)

    def add_member_btn(self):
        return self.find_element(VLOverviewLocators.ADD_MEMBER)

    def save_text(self):
        return self.find_element(VLOverviewLocators.SAVE_TXT)

    def save_project_btn(self):
        return self.find_element(VLOverviewLocators.SAVE_PROJECT_BTN)

    def save_project_btn_clickable(self, timeout=30):
        try:
            button = self.element_to_be_clickable(VLOverviewLocators.SAVE_PROJECT_BTN, timeout)
            return button
        except TimeoutException:
            print("Save button was not found or not clickable")
            return None
