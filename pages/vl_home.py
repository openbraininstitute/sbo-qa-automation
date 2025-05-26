# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

from locators.vlab_home_locators import VLHomeLocators
from pages.home_page import HomePage
from util.util_links_checker import LinkChecker
from selenium.common import TimeoutException

class VlabHome(HomePage, LinkChecker):
    def __init__(self, browser, wait, base_url):
        super().__init__(browser, wait, base_url)
        self.home_page = HomePage(browser, wait, base_url)

    def go_to_vlab_home(self, lab_id: str, project_id: str):
        path = f"/app/virtual-lab"
        try:
            self.go_to_page(path)
            self.wait_for_page_ready(timeout=60)
        except TimeoutException:
            raise RuntimeError(f"Failed to load page at {path} within 60 seconds")
        return self.browser.current_url

    def find_user_vlab(self):
        return self.find_element(VLHomeLocators.USER_VLAB)

    def find_other_vlab(self):
        return self.find_element(VLHomeLocators.OTHER_VLABS)

    def go_to_your_vlab(self):
        return self.find_element(VLHomeLocators.GO_TO_YOUR_VLAB)

    def find_num_projects(self):
        return self.find_element(VLHomeLocators.NUM_PROJECTS)

    def find_num_members(self):
        return self.find_element(VLHomeLocators.NUM_MEMBERS)

    def find_num_vlabs(self):
        return self.find_element(VLHomeLocators.NUM_VLABS)

    def find_public_projects(self):
        return self.find_element(VLHomeLocators.PUBLIC_PROJECTS)

    def find_outside_explore(self):
        return self.find_element(VLHomeLocators.OUTSIDE_EXPLORE)

    def find_qna_btn(self):
        return self.find_element(VLHomeLocators.QNA_BTN)

    def find_menu_about_btn(self):
        return self.find_element(VLHomeLocators.MENU_ABOUT_OBI_BTN)

    def find_menu_contact_btn(self):
        return self.find_element(VLHomeLocators.MENU_CONTACT_OBI_BTN)

    def find_menu_terms_btn(self):
        return self.find_element(VLHomeLocators.MENU_TERMS_BTN)

    def find_home_btn(self):
        return self.find_element(VLHomeLocators.HOME_BTN)

    def find_profile_btn(self):
        return self.find_element(VLHomeLocators.PROFILE_BTN)

