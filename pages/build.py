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

    def created_by_name(self):
        return self.find_all_elements(BuildLocators.CREATED_BY_NAME)

    def creation_date(self):
        return self.find_element(BuildLocators.CREATION_DATE)

    def date(self):
        return self.find_element(BuildLocators.DATE)

    def form_name(self):
        return self.element_visibility(BuildLocators.FORM_NAME)

    def form_description(self):
        return self.find_element(BuildLocators.FORM_DESCRIPTION)

    def form_brain_region(self):
        return self.element_to_be_clickable(BuildLocators.FORM_BRAIN_REGION)

    def start_building_btn(self):
        return self.element_to_be_clickable(BuildLocators.START_BUILDING_BTN)

    def sn_name(self):
        return self.find_element(BuildLocators.SN_NAME)

    def sn_description(self):
        return self.find_element(BuildLocators.SN_DESCRIPTION)

    def sn_creation_date(self):
        return self.find_element(BuildLocators.SN_CREATION_DATE)

    def sn_created_by(self):
        return self.find_all_elements(BuildLocators.SN_CREATED_BY)

    def sn_brain_region(self):
        return self.find_element(BuildLocators.SN_BRAIN_REGION)

    def sn_mtype(self):
        return self.find_element(BuildLocators.SN_MTYPE)

    def sn_etype(self):
        return self.find_element(BuildLocators.SN_ETYPE)

    def find_search_input_search_item(self):
        return self.find_element(BuildLocators.SEARCH_INPUT_FIELD)

