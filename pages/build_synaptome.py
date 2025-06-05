# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException
import logging

from locators.build_synaptome_locators import BuildSynaptomeLocators
from pages.home_page import HomePage


class BuildSynaptomePage(HomePage):
    def __init__(self, browser, wait, base_url, logger=None):
        super().__init__(browser, wait, base_url)
        self.logger = logger or logging.getLogger(__name__)
        self.home_page = HomePage(browser, wait, base_url)
        self.logger = logger

    def go_to_build_synaptome(self, lab_id: str, project_id: str):
        path = f"/app/virtual-lab/lab/{lab_id}/project/{project_id}/build"
        try:
            self.browser.set_page_load_timeout(90)
            self.go_to_page(path)
            self.wait_for_page_ready(timeout=60)
        except TimeoutException:
            raise RuntimeError("The Build page did not load within 60 seconds.")
        return self.browser.current_url

    def description_title(self):
        return self.find_element(BuildSynaptomeLocators.DESCRIPTION_TITLE)

    def find_menu_build(self):
        return self.find_element(BuildSynaptomeLocators.MENU_BUILD)

    def find_synaptome_box(self):
        return self.find_element(BuildSynaptomeLocators.SYNAPTOME_BOX)

    def find_synaptome_build_btn(self):
        return self.find_element(BuildSynaptomeLocators.SYNAPTOME_BUILD_BTN)

    def form_created_by(self):
        return self.find_element(BuildSynaptomeLocators.FORM_CREATED_BY)

    def form_value_created_by(self):
        return self.find_all_elements(BuildSynaptomeLocators.FORM_VALUE_CREATED_BY)

    def form_creation_date(self):
        return self.find_element(BuildSynaptomeLocators.FORM_CREATION_DATE)

    def form_value_creation_date(self):
        return self.find_element(BuildSynaptomeLocators.FORM_VALUE_CREATION_DATE)

    def input_name_field(self):
        return self.find_element(BuildSynaptomeLocators.INPUT_NAME_FIELD)

    def input_description_field(self):
        return self.find_element(BuildSynaptomeLocators.INPUT_DESCRIPTION_FIELD)

    def new_synaptome_title(self):
        return self.find_element(BuildSynaptomeLocators.NEW_SYNAPTOME_TITLE)

    def start_building_button(self):
        return self.element_to_be_clickable(BuildSynaptomeLocators.START_BUILDING_BTN)

    def synaptome_form(self):
        return self.find_element(BuildSynaptomeLocators.SYNAPTOME_FORM)
