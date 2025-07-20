# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

from pages.home_page import HomePage
from util.util_links_checker import LinkChecker
from locators.build_locators import BuildLocators
from selenium.common import TimeoutException

class Build(HomePage, LinkChecker):
    def __init__(self, browser, wait, base_url):
        super().__init__(browser, wait, base_url)
        self.home_page = HomePage(browser, wait, base_url)

    def go_to_build(self, lab_id: str, project_id: str):
        path = f"/app/virtual-lab/lab/{lab_id}/project/{project_id}/home"
        try:
            self.go_to_page(path)
            self.wait_for_page_ready(timeout=100)
            self.wait_for_build_page_loaded(timeout=60)
        except TimeoutException:
            raise RuntimeError(f"Failed to load page at {path} within 100 seconds")
        return self.browser.current_url

    def wait_for_build_page_loaded(self, timeout=30):
        return self.wait.until(
            lambda driver: self.build_menu_title(timeout=5).is_displayed(),
            message="Build menu title did not appear within timeout"
        )

    def brain_region_toggle_btn(self):
        return self.find_element(BuildLocators.BRAIN_REGION_PANEL_TOGGLE)

    def build_menu_title(self, timeout=20):
        return self.find_element(BuildLocators.BUILD_MENU_TITLE, timeout=timeout)

    def created_by_name(self):
        return self.find_all_elements(BuildLocators.CREATED_BY_NAME)

    def creation_date(self):
        return self.find_element(BuildLocators.CREATION_DATE_TITLE)

    def date(self):
        return self.find_element(BuildLocators.DATE)

    def find_search_input_search_item(self):
        return self.find_element(BuildLocators.SEARCH_INPUT_FIELD)

    def form_brain_region(self):
        return self.element_to_be_clickable(BuildLocators.FORM_BRAIN_REGION)

    def form_build_single_neuron_title(self):
        return self.find_element(BuildLocators.FORM_BUILD_NEURON_TITLE)

    def form_description(self):
        return self.find_element(BuildLocators.FORM_DESCRIPTION)

    def form_name(self):
        return self.element_visibility(BuildLocators.FORM_NAME)

    def new_model_tab(self):
        return self.find_element(BuildLocators.NEW_MODEL_TAB)

    def save_model(self):
        return self.find_element(BuildLocators.SAVE)

    def searched_e_record(self):
        return self.find_element(BuildLocators.SEARCHED_E_RECORD)

    def searched_m_record(self):
        return self.find_element(BuildLocators.SEARCHED_M_RECORD)

    def select_e_model_btn(self):
        return self.find_element(BuildLocators.SELECT_E_MODEL_BTN)

    def select_specific_e_model_btn(self):
        return self.find_element(BuildLocators.SELECT_SPECIFIC_E_MODEL_BTN)

    def select_m_model_btn(self):
        return self.find_element(BuildLocators.SELECT_M_MODEL_BTN)

    def select_specific_m_model_btn(self):
        return self.find_element(BuildLocators.SELECT_SPECIFIC_M_MODEL_BTN)

    def single_neuron_build_btn(self):
        return self.find_element(BuildLocators.BUILD_SINGLE_NEURON_BTN)

    def single_neuron_title(self):
        return self.find_element(BuildLocators.SINGLE_NEURON_TITLE)

    def sn_brain_region(self):
        return self.find_element(BuildLocators.SN_BRAIN_REGION)

    def sn_creation_date(self):
        return self.find_element(BuildLocators.SN_CREATION_DATE)

    def sn_created_by(self):
        return self.find_all_elements(BuildLocators.SN_CREATED_BY)

    def sn_description(self):
        return self.find_element(BuildLocators.SN_DESCRIPTION)

    def sn_etype(self):
        return self.find_element(BuildLocators.SN_ETYPE)

    def sn_mtype(self):
        return self.find_element(BuildLocators.SN_MTYPE)

    def sn_name(self, timeout=10):
        return self.find_element(BuildLocators.SN_NAME, timeout=timeout)

    def start_building_btn(self):
        return self.element_to_be_clickable(BuildLocators.START_BUILDING_BTN)

    def tick_search_e_record(self):
        return self.find_element(BuildLocators.TICK_SEARCHED_E_RECORD)

    def tick_search_m_record(self):
        return self.find_element(BuildLocators.TICK_SEARCHED_M_RECORD)
