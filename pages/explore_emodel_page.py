# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

from selenium.common import ElementNotVisibleException, TimeoutException, \
    StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait

from pages.explore_page import ExplorePage
from locators.explore_emodel_locators import ExploreEModelPageLocators


class ExploreEModelDataPage(ExplorePage):
    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, logger, base_url)
        self.home_page = ExplorePage(browser, wait, logger, base_url)
        self.logger = logger

    def go_to_explore_emodel_page(self, lab_id: str, project_id: str, retries=3, delay=5):
        path = f"/app/virtual-lab/{lab_id}/{project_id}/data/browse/entity/emodel"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(90)
                self.go_to_page(path)
                self.wait_for_page_ready(timeout=60)
            except TimeoutException:
                print(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                time.sleep(delay)
                if attempt == retries - 1:
                    raise RuntimeError("The Explore E-Model page did not load within 60 seconds")
        return self.browser.current_url

    def brain_region_panel_close_btn(self):
        return self.find_element(ExploreEModelPageLocators.CLOSE_BRAIN_REGION_PANEL_BTN)

    def find_ai_assistant_panel(self, timeout=10):
        return self.find_element(ExploreEModelPageLocators.AI_ASSISTANT_PANEL, timeout=timeout)

    def find_ai_assistant_panel_close_btn(self):
        return self.find_element(ExploreEModelPageLocators.AI_ASSISTANT_PANEL_CLOSE_BTN)

    def find_brain_region_search_field(self, timeout=20):
        return self.find_element(ExploreEModelPageLocators.BR_SEARCH_FIELD_TYPE, timeout=timeout)

    def find_brain_region_panel(self, timeout=40):
        WebDriverWait(self.browser, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        return self.is_visible(ExploreEModelPageLocators.BRAIN_REGION_PANEL, timeout=timeout)

    def find_br_cerebrum_title(self, timeout=15):
        return self.find_element(ExploreEModelPageLocators.BR_CEREBRUM_TITLE, timeout=timeout)

    def find_dv_analysis_tab(self):
        return self.find_element(ExploreEModelPageLocators.DV_ANALYSIS_TAB)

    def find_dv_brain_region_label(self):
        return self.find_element(ExploreEModelPageLocators.DV_BRAIN_REGION_LABEL)

    def find_dv_brain_region_value(self):
        return self.find_element(ExploreEModelPageLocators.DV_BRAIN_REGION_VALUE)

    def find_dv_created_by_label(self):
        return self.find_element(ExploreEModelPageLocators.DV_CREATED_BY_LABEL)

    def find_dv_created_by_value(self):
        return self.find_element(ExploreEModelPageLocators.DV_CREATED_BY_VALUE)

    def find_dv_species_label(self):
        return self.find_element(ExploreEModelPageLocators.DV_SPECIES_LABEL)

    def find_dv_species_value(self):
        return self.find_element(ExploreEModelPageLocators.DV_SPECIES_VALUE)

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

    def find_dv_overview_tab(self):
        return self.find_element(ExploreEModelPageLocators.DV_OVERVIEW_TAB)

    def find_emodel_tab(self, timeout=25):
        return self.is_visible(ExploreEModelPageLocators.EMODEL_TAB, timeout=timeout)

    def find_lv_em_td(self):
        return self.find_element(ExploreEModelPageLocators.LV_EM_TD)

    def find_lv_row(self, timeout=15):
        return self.is_visible(ExploreEModelPageLocators.LV_ROW, timeout=timeout)

    def find_lv_selected_resource(self, timeout=25):
        return self.is_visible(ExploreEModelPageLocators.LV_EM_TD, timeout=timeout)

    def find_selected_brain_region_title(self, timeout=10):
        return self.find_element(ExploreEModelPageLocators.SELECTED_BRAIN_REGION, timeout=timeout)

    def find_search_for_resources(self, timeout=5):
        return self.element_to_be_clickable(ExploreEModelPageLocators.FREE_TEXT_SEARCH, timeout=timeout)

    def input_placeholder(self, timeout=5):
        return self.element_to_be_clickable(ExploreEModelPageLocators.INPUT_PLACEHOLDER, timeout=timeout)

    def mini_detail_view_button(self, timeout=5):
        return self.element_to_be_clickable(ExploreEModelPageLocators.MINI_DETAIL_VIEW, timeout=timeout)

    def model_data_tab(self):
        return self.find_element(ExploreEModelPageLocators.MODEL_DATA_TAB)

    def verify_exemplar_morphology_headers(self):
        expected_headers = ["PREVIEW", "NAME", "DESCRIPTION", "BRAIN REGION", "M-TYPE", "CONTRIBUTORS"]
        actual_headers = self.dv_get_table_headers()
        assert actual_headers == expected_headers, (
            f"Expected morphology headers: {expected_headers}, but got: {actual_headers}"
        )
        self.logger.info("Exemplar Morphology headers match expected.")

    def verify_exemplar_traces_table_headers(self):
        expected_headers = ["PREVIEW", "NAME", "M-TYPE", "E-TYPE", "SPECIES"]
        actual_headers = self.dv_get_trace_table_headers()
        assert actual_headers == expected_headers, (
            f"Expected trace headers: {expected_headers}, but got: {actual_headers}"
        )
        self.logger.info("Exemplar Traces headers match expected.")

    def wait_for_spinner_to_disappear(self, timeout=15):
        return self.wait_for_element_to_disappear(ExploreEModelPageLocators.SPINNER, timeout=timeout)

    def wait_for_emodel_tab_ready(self, timeout=30):
        WebDriverWait(self.browser, timeout).until(
            lambda driver: driver.execute_script(
                "return document.readyState === 'complete';"
            ),
            "Page did not reach readyState=complete"
        )
        self.is_visible(ExploreEModelPageLocators.EMODEL_TAB, timeout=timeout)
        return self.browser.find_element(*ExploreEModelPageLocators.EMODEL_TAB)

    def wait_for_emodel_detail_page(self, timeout: int = 10):
        WebDriverWait(self.browser, timeout).until(
            EC.url_contains("/data/view/emodel/")
        )