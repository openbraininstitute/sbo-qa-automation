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

    def build_menu_title(self):
        return self.find_element(BuildLocators.BUILD_MENU_TITLE)

    def new_model_tab(self):
        return self.find_element(BuildLocators.NEW_MODEL_TAB)

    def single_neuron_title(self):
        return self.find_element(BuildLocators.SINGLE_NEURON_TITLE)

    def single_neuron_build_btn(self):
        return self.find_element(BuildLocators.BUILD_SINGLE_NEURON_BTN)

    def form_build_single_neuron_title(self):
        return self.find_element(BuildLocators.FORM_BUILD_NEURON_TITLE)

    def form_name(self):
        return self.element_visibility(BuildLocators.FORM_NAME)

    def form_description(self):
        return self.find_element(BuildLocators.FORM_DESCRIPTION)

    def form_brain_region(self):
        return self.element_to_be_clickable(BuildLocators.FORM_BRAIN_REGION)

    def start_building_btn(self):
        return self.element_to_be_clickable(BuildLocators.START_BUILDING_BTN)