# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from locators.explore_page_locators import ExplorePageLocators
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage


class ExplorePage(HomePage):
    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, base_url)
        self.logger = logger

    def go_to_explore_page(self, lab_id: str, project_id: str, retries=3, delay=5):
        path = f"/app/virtual-lab/{lab_id}/{project_id}/data"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(100)
                self.go_to_page(path)
                self.wait_for_page_ready(timeout=90)
            except TimeoutException:
                print(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                time.sleep(delay)
                if attempt == retries - 1:
                    raise RuntimeError("The Explore page failed to load after multiple attempts.")
            return self.browser.current_url
        return None

    def skip_onboardin_btn(self, timeout=10):
        try:
            return self.element_to_be_clickable(ExplorePageLocators.SKIP_ONBOARDING_BTN, timeout=timeout)
        except TimeoutException:
            return None

    def data_skip_onboardin_btn(self, timeout=10):
        try:
            return self.find_element(ExplorePageLocators.DATA_SKIP_BTN, timeout=timeout)
        except TimeoutException:
            return None

    def cerebrum_title_br_panel(self):
        return self.find_element(ExplorePageLocators.CEREBRUM_TITLE_BRAIN_REGION_PANEL)

    def experimental_data_tab(self):
        return self.find_element(ExplorePageLocators.EXPERIMENTAL_DATA_BTN)

    def wait_for_dynamically_loaded_links(self):
        self.wait.until(EC.presence_of_element_located(ExplorePageLocators.EXPLORE_LINK1))

    def find_ai_assistant_panel(self, timeout=25):
        return self.is_visible(ExplorePageLocators.AI_ASSISTANT_PANEL, timeout=timeout)

    def find_ai_assistant_panel_close(self, timeout=35):
        return self.element_to_be_clickable(ExplorePageLocators.AI_ASSISTANT_PANEL_CLOSE, timeout=timeout)

    def find_ai_assistant_panel_open(self):
        return self.find_element(ExplorePageLocators.AI_ASSISTANT_PANEL_BTN_OPEN)

    def find_atlas_fullscreen_bt(self, timeout=20):
        return self.find_element(ExplorePageLocators.ATLAS_FULLSCREEN, timeout=timeout)

    def find_brain_region_panel(self, timeout=40):
        WebDriverWait(self.browser, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        return self.is_visible(ExplorePageLocators.BRAIN_REGION_PANEL, timeout=timeout)

    def find_species_dropdown(self, timeout=10):
        return self.find_element(ExplorePageLocators.BRAIN_REGION_SPECIES_DROPDOWN, timeout=timeout)

    def get_species_value(self, timeout=10):
        el = self.find_element(ExplorePageLocators.BRAIN_REGION_SPECIES_VALUE, timeout=timeout)
        return el.text.strip()

    def click_species_dropdown(self, timeout=10):
        dd = self.element_to_be_clickable(ExplorePageLocators.BRAIN_REGION_SPECIES_DROPDOWN, timeout=timeout)
        dd.click()
        import time
        time.sleep(1)
        return dd

    def find_brain_region_search_field(self, timeout=20):
        return self.find_element(ExplorePageLocators.SEARCH_REGION, timeout=timeout)

    def find_cerebrum_brp(self, timeout=30):
        return self.find_element(ExplorePageLocators.CEREBRUM_TITLE_BRAIN_REGION_PANEL, timeout=timeout)

    def click_basic_cell_groups_arrow(self, timeout=15):
        """Click the expand arrow on 'Basic cell groups and regions' to reveal children."""
        from selenium.webdriver.common.action_chains import ActionChains
        arrow = self.element_to_be_clickable(ExplorePageLocators.BASIC_CELL_GROUPS_ARROW, timeout=timeout)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", arrow)
        import time
        time.sleep(0.5)
        ActionChains(self.browser).move_to_element(arrow).click().perform()
        time.sleep(1)
        return arrow

    def find_cerebrum_in_tree(self, timeout=15):
        """Find the Cerebrum button in the brain region tree."""
        return self.find_element(ExplorePageLocators.CEREBRUM_BTN, timeout=timeout)

    def find_cerebrum_arrow_btn(self, timeout=20):
        """Find the expand arrow on the Cerebrum node."""
        return self.find_element(ExplorePageLocators.CEREBRUM_ARROW_BTN, timeout=timeout)

    def find_cerebral_cortex_brp(self, timeout=15):
        return self.find_element(ExplorePageLocators.CEREBRAL_CORTEX_TITLE, timeout=timeout)

    def search_and_select_brain_region(self, search_term, timeout=10):
        """Type a brain region name in the region search dropdown and select it."""
        region_input = self.element_to_be_clickable(ExplorePageLocators.REGION_SEARCH_INPUT, timeout=timeout)
        region_input.click()
        region_input.send_keys(search_term)
        self.logger.info(f"Typed '{search_term}' in region search")
        time.sleep(2)

        option_locator = (By.XPATH, f"//div[contains(@class,'ant-select-item')]//div[text()='{search_term}']")
        option = self.element_to_be_clickable(option_locator, timeout=timeout)
        option.click()
        self.logger.info(f"Selected '{search_term}' from region search dropdown")
        time.sleep(2)

    def find_cerebrum_title_main_page(self, timeout=30):
        return self.find_element(ExplorePageLocators.CEREBRUM_TITLE_MAIN_PAGE, timeout=timeout)

    def find_count_switch(self, timeout=10):
        return self.is_visible(ExplorePageLocators.COUNT_SWITCH, timeout=timeout)

    def find_data_panel(self, timeout=10):
        return self.find_element(ExplorePageLocators.DATA_PANEL, timeout=timeout)

    def check_explore_title_is_present(self, timeout=15):
        return self.find_element(ExplorePageLocators.EXPLORE_TITLE_VLAB, timeout=timeout)

    def find_explore_page_titles(self, page_locators, timeout=25):
        elements_list = []
        for locator in page_locators:
            elements_list.extend(self.visibility_of_all_elements(locator, timeout=timeout))
        return elements_list

    def find_experimental_data_titles(self, exp_data_locators, timeout=30):
        result = []
        for locator in exp_data_locators:
            result.extend(self.visibility_of_all_elements(locator, timeout=timeout))
        return result

    def get_experiment_record_count(self, record_count_locators, timeout=40):
        record_counts = []
        for locator in record_count_locators:
            try:
                record = self.wait_for_non_empty_text(locator, timeout)
                record_text = record.text.strip()
                record_number = int(''.join(filter(str.isdigit, record_text)))
                record_counts.append(record_number)
            except TimeoutException:
                raise TimeoutException(f"Timeout: No text found for record at {locator} within {timeout} seconds.")
            except ValueError:
                raise ValueError(f"Could not parse record count from text: '{record_text}'")
        return record_counts

    def find_3d_atlas(self):
        return self.find_element(ExplorePageLocators.ATLAS)

    def find_fullscreen_exit(self, timeout=20):
        return self.find_element(ExplorePageLocators.FULLSCREEN_EXIT, timeout=timeout)

    def list_of_neurons_panel(self):
        return self.find_all_elements(ExplorePageLocators.NEURONS_PANEL_GRID_MTYPES)

    def find_model_data_title(self):
        return self.find_element(ExplorePageLocators.MODEL_DATA_BTN)

    def find_neurons_panel(self):
        return self.is_visible(ExplorePageLocators.NEURONS_PANEL)

    def find_selected_brain_region_title(self):
        return self.find_element(ExplorePageLocators.SELECTED_BRAIN_REGION)

    def find_neurons_mtypes_btn(self):
        return self.find_element(ExplorePageLocators.NEURONS_PANEL_MTYPE_BTN)

    def find_neurons_etype_title(self):
        return self.find_element(ExplorePageLocators.NEURONS_PANEL_ETYPES_TITLE)

    def find_neurons_panel_iso_mtype(self):
        return self.find_element(ExplorePageLocators.NEURONS_PANEL_ISOCORTEX_MTYPE)

    def find_panel_circuit(self):
        return self.find_element(ExplorePageLocators.PANEL_CIRCUIT)

    def find_panel_emodel(self):
        return self.find_element(ExplorePageLocators.PANEL_EMODEL)

    def find_panel_memodel(self):
        return self.find_element(ExplorePageLocators.PANEL_MEMODEL)

    def find_panel_synaptome(self):
        return self.find_element(ExplorePageLocators.PANEL_SYNAPTOME)

    def find_panel_mtype(self):
        return self.find_element(ExplorePageLocators.NEURONS_PANEL_MTYPE)

    def find_total_count_density(self, timeout=30):
        return self.find_element(ExplorePageLocators.TOTAL_COUNT_DENSITY, timeout=timeout)

    def find_total_count_n(self):
        return self.find_element(ExplorePageLocators.TOTAL_COUNT_N)

    def find_total_count_switch(self):
        return self.find_element(ExplorePageLocators.TOTAL_COUNT_SWITCH)

    def find_visible_experimental_data_titles(self, exp_data_locators, timeout=30):
        """Return all visible experimental data elements from a list of locators."""
        result = []
        for locator in exp_data_locators:
            result.extend(self.visibility_of_all_elements(locator, timeout=timeout))
        return result

    def find_visible_explore_page_titles(self, page_locators, timeout=30):
        elements_list = []
        for locator in page_locators:
            elements_list.extend(self.visibility_of_all_elements(locator, timeout=timeout))
        return elements_list

    def search_region_input_field(self, timeout=10):
        return self.find_element(ExplorePageLocators.SEARCH_REGION_INPUT, timeout=timeout)

    def wait_for_locators_to_have_text(self, browser, locators, timeout=20):
        for locator in locators:
            WebDriverWait(self.browser, timeout).until(
                EC.text_to_be_present_in_element(locator, '')
            )

    def get_record_type_total_count(self, locator, timeout=10):
        """Get the total record count (second number after 'of') for a record type.
        Returns the total as int, or 0 if not found.
        """
        try:
            element = self.find_element(locator, timeout=timeout)
            # The total count is the last span.font-bold inside the element
            spans = element.find_elements(By.XPATH, ".//span[contains(@class,'font-bold')]")
            if len(spans) >= 2:
                total_text = spans[-1].text.strip()
                # Remove thousands separators
                total_text = total_text.replace("'", "").replace(",", "").replace(" ", "")
                return int(total_text) if total_text.isdigit() else 0
            return 0
        except (TimeoutException, ValueError):
            return 0

    def verify_experimental_record_counts(self, timeout=10):
        """Verify all experimental record type counters have a non-zero total.
        Returns dict with type name → total count.
        """
        record_types = {
            "Morphology": ExplorePageLocators.COUNTER_MORPHOLOGY,
            "Single cell electrophysiology": ExplorePageLocators.COUNTER_ELECTROPHYSIOLOGY,
            "Ion channel electrophysiology": ExplorePageLocators.COUNTER_ION_CHANNEL_EPHYS,
            "Neuron density": ExplorePageLocators.COUNTER_NEURON_DENSITY,
            "EM Mesh": ExplorePageLocators.COUNTER_EM_MESH,
        }
        results = {}
        for name, locator in record_types.items():
            total = self.get_record_type_total_count(locator, timeout=timeout)
            results[name] = total
            if total > 0:
                self.logger.info(f"  {name}: total={total}")
            else:
                self.logger.warning(f"  {name}: total is 0 or not found")
        return results
