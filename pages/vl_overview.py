# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

from pages.home_page import HomePage
from util.util_links_checker import LinkChecker
from locators.vlab_overview_locators import VLOverviewLocators
from selenium.common import TimeoutException


class VLOverview(HomePage):
    def __init__(self, browser, wait, base_url):
        super().__init__(browser, wait, base_url)
        self.home_page = HomePage(browser, wait, base_url)


    def go_to_vloverview(self, lab_id: str, project_id: str, retries=3, delay=5):
        path = f"/app/virtual-lab/lab/{lab_id}/overview"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(90)
                self.go_to_page(path)
                self.wait_for_page_ready(timeout=90)
            except TimeoutException:
                print(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                time.sleep(delay)  # Wait before retrying
                delay *= 2  # Exponentially increase delay (e.g., 5, 10, 20 seconds)
                if attempt == retries - 1:
                    raise RuntimeError("The Explore page failed to load after multiple attempts.")
            return self.browser.current_url

    def vl_overview_title(self):
        return self.find_element(VLOverviewLocators.VLOVERVIEW_TITLE)

    def vl_banner(self):
        return self.find_element(VLOverviewLocators.VL_BANNER)

    def vl_banner_name_label(self):
        return self.find_element(VLOverviewLocators.VL_BANNER_NAME_LABEL)

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
