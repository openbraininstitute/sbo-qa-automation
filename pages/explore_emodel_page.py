# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

from selenium.common import ElementNotVisibleException, TimeoutException, \
    StaleElementReferenceException

from pages.explore_page import ExplorePage
from locators.explore_emodel_locators import ExploreEModelPageLocators
from util.util_links_checker import LinkChecker
from util.util_scraper import UrlScraper


class ExploreEModelDataPage(ExplorePage, LinkChecker):
    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, base_url)
        self.home_page = ExplorePage(browser, wait, base_url)
        self.url_scraper = UrlScraper()
        self.logger = logger

    def go_to_explore_emodel_page(self, lab_id: str, project_id: str):
        path = f"/app/virtual-lab/lab/{lab_id}/project/{project_id}/explore/interactive/model/e-model"
        try:
            self.browser.set_page_load_timeout(90)
            self.go_to_page(path)
            self.wait_for_page_ready(timeout=60)
        except TimeoutException:
            raise RuntimeError("The Model data page did not load within 60 seconds.")
        return self.browser.current_url

    def brain_region_panel_close_btn(self):
        return self.find_element(ExploreEModelPageLocators.CLOSE_BRAIN_REGION_PANEL_BTN)

    def find_ai_assistant_panel(self, timeout=10):
        return self.find_element(ExploreEModelPageLocators.AI_ASSISTANT_PANEL, timeout=timeout)

    def find_ai_assistant_panel_close_btn(self):
        return self.find_element(ExploreEModelPageLocators.AI_ASSISTANT_PANEL_CLOSE_BTN)

    def find_brain_region_search_field(self, timeout=20):
        return self.find_element(ExploreEModelPageLocators.SEARCH_REGION, timeout=timeout)

    def find_brain_region_panel(self):
        return self.find_element(ExploreEModelPageLocators.BRAIN_REGION_PANEL)

    def find_br_cerebrum_title(self):
        return self.find_element(ExploreEModelPageLocators.BR_CEREBRUM_TITLE)

    def find_dv_analysis_tab(self):
        return self.find_element(ExploreEModelPageLocators.DV_ANALYSIS_TAB)

    def find_dv_brain_region_label(self):
        return self.find_element(ExploreEModelPageLocators.DV_BRAIN_REGION_LABEL)

    def find_dv_brain_region_value(self):
        return self.find_element(ExploreEModelPageLocators.DV_BRAIN_REGION_VALUE)

    def find_dv_configuration_tab(self):
        return self.find_element(ExploreEModelPageLocators.DV_CONFIGURATION_TAB)

    def find_dv_contributors_label(self):
        return self.find_element(ExploreEModelPageLocators.DV_CONTRIBUTORS_LABEL)

    def find_dv_contributors_value(self):
        return self.find_element(ExploreEModelPageLocators.DV_CONTRIBUTORS_VALUE)

    def find_dv_description_label(self):
        return self.find_element(ExploreEModelPageLocators.DV_DESCRIPTION_LABEL)

    def find_dv_description_value(self):
        return self.find_element(ExploreEModelPageLocators.DV_DESCRIPTION_VALUE)

    def dv_get_table_headers(self):
        """Returns the visible text of all column headers."""
        element = self.find_all_elements(ExploreEModelPageLocators.DV_MORPH_TABLE_HEADER_COLUMNS)
        return [el.text.strip() for el in element if el.text.strip()]

    def dv_get_trace_table_headers(self):
        """Returns the visible text of all column headers in the Exemplar Traces table."""
        elements = self.find_all_elements(ExploreEModelPageLocators.DV_EXEMPLAR_TABLE_HEADER_COLUMNS)
        return [el.text.strip() for el in elements if el.text.strip()]

    def find_dv_name_label(self):
        return self.find_element(ExploreEModelPageLocators.DV_NAME_LABEL)

    def find_dv_name_value(self):
        return self.find_element(ExploreEModelPageLocators.DV_NAME_VALUE)

    def find_dv_model_score_label(self):
        return self.find_element(ExploreEModelPageLocators.DV_MODEL_SCORE_LABEL)

    def find_dv_model_score_value(self):
        return self.find_element(ExploreEModelPageLocators.DV_MODEL_SCORE_VALUE)

    def find_dv_mtype_label(self):
        return self.find_element(ExploreEModelPageLocators.DV_MTYPE_LABEL)

    def find_dv_mtype_value(self):
        return self.find_element(ExploreEModelPageLocators.DV_MTYPE_VALUE)

    def find_dv_etype_label(self):
        return self.find_element(ExploreEModelPageLocators.DV_ETYPE_LABEL)

    def find_dv_etype_value(self):
        return self.find_element(ExploreEModelPageLocators.DV_ETYPE_VALUE)

    def find_dv_registration_date_label(self):
        return self.find_element(ExploreEModelPageLocators.DV_REGISTRATION_DATE_LABEL)

    def find_dv_registration_date_value(self):
        return self.find_element(ExploreEModelPageLocators.DV_REGISTRATION_DATE_VALUE)

    def find_dv_simulation_tab(self):
        return self.find_element(ExploreEModelPageLocators.DV_SIMULATION_TAB)

    def find_emodel_tab(self):
        return self.find_element(ExploreEModelPageLocators.EMODEL_TAB)

    def find_lv_em_td(self):
        return self.find_element(ExploreEModelPageLocators.LV_EM_TD)

    def find_lv_selected_resource(self):
        return self.find_element(ExploreEModelPageLocators.LV_EM_TD)

    def find_selected_brain_region_title(self):
        return self.find_element(ExploreEModelPageLocators.SELECTED_BRAIN_REGION)

    def find_search_for_resources(self):
        return self.find_element(ExploreEModelPageLocators.SEARCH_RESOURCES)

    def verify_exemplar_morphology_headers(self):
        expected_headers = ["PREVIEW", "NAME", "DESCRIPTION", "BRAIN LOCATION", "M-TYPE", "CONTRIBUTOR"]
        actual_headers = self.dv_get_table_headers()
        assert actual_headers == expected_headers, (
            f"Expected morphology headers: {expected_headers}, but got: {actual_headers}"
        )
        self.logger.info("Exemplar Morphology headers match expected.")

    def verify_exemplar_traces_table_headers(self):
        expected_headers = ["PREVIEW", "CELL NAME", "M-TYPE", "E-TYPE", "E-CODE", "SUBJECT SPECIES"]
        actual_headers = self.dv_get_trace_table_headers()
        assert actual_headers == expected_headers, (
            f"Expected trace headers: {expected_headers}, but got: {actual_headers}"
        )
        self.logger.info("Exemplar Traces headers match expected.")
