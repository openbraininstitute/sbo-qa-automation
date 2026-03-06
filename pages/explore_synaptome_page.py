# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.explore_page import ExplorePage
from locators.explore_synaptome_locators import ExploreSynaptomePageLocators


class ExploreSynaptomeDataPage(ExplorePage):
    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, logger, base_url)
        self.logger = logger
        self.base_url = base_url

    def go_to_explore_synaptome_page(self, lab_id, project_id):
        """Navigate to the synaptome browse page"""
        url = f"{self.base_url}/app/virtual-lab/{lab_id}/{project_id}/data/browse/entity/single-neuron-synaptome?br_id=5c60bf3e-5335-4971-a8ec-6597292452b2&br_av=567&group=models"
        self.browser.get(url)
        self.logger.info(f"Navigated to synaptome page: {url}")
        time.sleep(2)

    def model_data_tab(self):
        """Find and return the Model data tab"""
        return self.wait.until(EC.presence_of_element_located(ExploreSynaptomePageLocators.MODEL_DATA_TAB))

    def project_tab(self, timeout=20):
        """Find and return the Project tab"""
        return self.find_element(ExploreSynaptomePageLocators.PROJECT_TAB, timeout)

    def synaptome_button(self, timeout=20):
        """Find and return the Synaptome button"""
        return self.find_element(ExploreSynaptomePageLocators.SYNAPTOME_BUTTON, timeout)

    def find_br_cerebrum_title(self, timeout=20):
        """Find the Cerebrum brain region title"""
        return self.find_element(ExploreSynaptomePageLocators.BR_CEREBRUM_TITLE, timeout)

    def find_brain_region_panel(self, timeout=20):
        """Find the brain region panel"""
        return self.find_element(ExploreSynaptomePageLocators.BRAIN_REGION_PANEL, timeout)

    def find_search_button(self, timeout=20):
        """Find the search button"""
        return self.find_element(ExploreSynaptomePageLocators.SEARCH_BUTTON, timeout)

    def input_placeholder(self, timeout=20):
        """Find the search input field"""
        return self.find_element(ExploreSynaptomePageLocators.INPUT_PLACEHOLDER, timeout)

    def find_lv_row(self):
        """Find the table body with rows"""
        return self.find_element(ExploreSynaptomePageLocators.LV_ROW)

    def find_lv_first_row(self, timeout=20):
        """Find the first row in the table"""
        return self.find_element(ExploreSynaptomePageLocators.LV_FIRST_ROW, timeout)

    def click_first_row(self, timeout=25):
        """Click on the first row in the table using scroll into view"""
        # Try clicking on a cell within the row instead of the row itself
        try:
            return self.scroll_into_view_and_click(ExploreSynaptomePageLocators.LV_FIRST_ROW_CELL, timeout)
        except:
            # Fallback to clicking the row
            return self.scroll_into_view_and_click(ExploreSynaptomePageLocators.LV_FIRST_ROW, timeout)

    def mini_detail_view_button(self, timeout=20):
        """Find the mini detail view button"""
        return self.find_element(ExploreSynaptomePageLocators.MINI_DETAIL_VIEW, timeout)

    # Detail view methods
    def find_dv_description_label(self):
        """Find description label in detail view"""
        return self.find_element(ExploreSynaptomePageLocators.DV_DESCRIPTION_LABEL)

    def find_dv_description_value(self):
        """Find description value in detail view"""
        return self.find_element(ExploreSynaptomePageLocators.DV_DESCRIPTION_VALUE)

    def find_dv_me_model_label(self):
        """Find ME-model label in detail view"""
        return self.find_element(ExploreSynaptomePageLocators.DV_ME_MODEL_LABEL)

    def find_dv_me_model_value(self):
        """Find ME-model value in detail view"""
        return self.find_element(ExploreSynaptomePageLocators.DV_ME_MODEL_VALUE)

    def find_dv_mtype_label(self):
        """Find M-Type label in detail view"""
        return self.find_element(ExploreSynaptomePageLocators.DV_MTYPE_LABEL)

    def find_dv_mtype_value(self):
        """Find M-Type value in detail view"""
        return self.find_element(ExploreSynaptomePageLocators.DV_MTYPE_VALUE)

    def find_dv_etype_label(self):
        """Find E-Type label in detail view"""
        return self.find_element(ExploreSynaptomePageLocators.DV_ETYPE_LABEL)

    def find_dv_etype_value(self):
        """Find E-Type value in detail view"""
        return self.find_element(ExploreSynaptomePageLocators.DV_ETYPE_VALUE)

    def find_dv_brain_region_label(self):
        """Find Brain Region label in detail view"""
        return self.find_element(ExploreSynaptomePageLocators.DV_BRAIN_REGION_LABEL)

    def find_dv_brain_region_value(self):
        """Find Brain Region value in detail view"""
        return self.find_element(ExploreSynaptomePageLocators.DV_BRAIN_REGION_VALUE)

    def find_dv_created_by_label(self):
        """Find Registered by label in detail view"""
        return self.find_element(ExploreSynaptomePageLocators.DV_CREATED_BY_LABEL)

    def find_dv_created_by_value(self):
        """Find Registered by value in detail view"""
        return self.find_element(ExploreSynaptomePageLocators.DV_CREATED_BY_VALUE)

    def find_dv_registration_date_label(self):
        """Find Registration date label in detail view"""
        return self.find_element(ExploreSynaptomePageLocators.DV_REGISTRATION_DATE_LABEL)

    def find_dv_registration_date_value(self):
        """Find Registration date value in detail view"""
        return self.find_element(ExploreSynaptomePageLocators.DV_REGISTRATION_DATE_VALUE)

    def find_dv_overview_tab(self):
        """Find Overview tab in detail view"""
        return self.find_element(ExploreSynaptomePageLocators.DV_OVERVIEW_TAB)

    def wait_for_spinner_to_disappear(self, timeout=30):
        """Wait for loading spinner to disappear"""
        try:
            self.wait.until(EC.invisibility_of_element_located(ExploreSynaptomePageLocators.SPINNER))
            self.logger.info("Spinner disappeared")
        except TimeoutException:
            self.logger.warning(f"Spinner did not disappear within {timeout} seconds")
