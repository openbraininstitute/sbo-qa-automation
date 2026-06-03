# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import random

from selenium.common import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from pages.explore_page import ExplorePage
from locators.explore_me_model_locators import ExploreMeModelLocators


class ExploreMeModelPage(ExplorePage):
    """Page object for the ME-model Detail View.

    Entry: Login → Data → Model → ME-model → click row → Detail View.
    """

    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, logger, base_url)
        self.logger = logger

    # ── Navigation ───────────────────────────────────────────────────────

    def go_to_explore_memodel_page(self, lab_id: str, project_id: str, retries=3, delay=5):
        """Navigate to Data > Model > ME-model list."""
        path = f"/app/virtual-lab/{lab_id}/{project_id}/data/browse/entity/memodel?group=models"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(90)
                self.go_to_page(path)
                self.wait_for_page_ready(timeout=60)
                self.logger.info(f"ME-model list page loaded: {self.browser.current_url}")
                return
            except TimeoutException:
                self.logger.warning(f"Attempt {attempt + 1} failed. Retrying in {delay}s...")
                time.sleep(delay)
                if attempt == retries - 1:
                    raise RuntimeError("ME-model list page did not load")

    # ── Species selection ────────────────────────────────────────────────

    def select_random_species(self):
        """Open species dropdown and select a random species that has data.
        Tries each available species until one with table data is found.
        """
        max_attempts = 5
        tried_species = set()

        for attempt in range(max_attempts):
            dropdown = self.element_to_be_clickable(
                ExploreMeModelLocators.BRAIN_REGION_SPECIES_DROPDOWN, timeout=15
            )
            dropdown.click()
            time.sleep(1)

            options = self.find_all_elements(
                ExploreMeModelLocators.BRAIN_REGION_SPECIES_OPTIONS, timeout=10
            )
            if not options:
                self.logger.warning("No species options found, closing dropdown")
                ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
                return None

            # Pick a random option we haven't tried yet (skip "All" option)
            untried = [o for o in options
                       if o.text.strip() not in tried_species
                       and o.text.strip()
                       and 'all' not in o.text.strip().lower().split('\n')[0].lower()]
            if not untried:
                self.logger.warning("All species tried, none have data")
                ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
                return None

            option = random.choice(untried)
            species_name = option.text.strip()
            tried_species.add(species_name)
            option.click()
            self.logger.info(f"Trying species: '{species_name}'")
            time.sleep(3)

            # Check if table has data
            try:
                rows = self.get_table_rows(timeout=10)
                if len(rows) > 0:
                    self.logger.info(f"Selected species '{species_name}' has {len(rows)} rows")
                    return species_name
            except Exception:
                pass

            self.logger.info(f"Species '{species_name}' has no data, trying next...")

        self.logger.warning("No species with data found after all attempts")
        return None

    def get_current_species(self):
        """Get the currently selected species value."""
        el = self.find_element(ExploreMeModelLocators.BRAIN_REGION_SPECIES_VALUE, timeout=10)
        return el.text.strip()

    def select_species_by_name(self, species_name):
        """Open species dropdown and select a specific species by name."""
        dropdown = self.element_to_be_clickable(
            ExploreMeModelLocators.BRAIN_REGION_SPECIES_DROPDOWN, timeout=15
        )
        dropdown.click()
        time.sleep(1)

        options = self.find_all_elements(
            ExploreMeModelLocators.BRAIN_REGION_SPECIES_OPTIONS, timeout=10
        )
        for option in options:
            if species_name.lower() in option.text.strip().lower():
                option.click()
                self.logger.info(f"Selected species: '{species_name}'")
                time.sleep(2)
                return species_name

        # Close dropdown if not found
        ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
        self.logger.warning(f"Species '{species_name}' not found in options")
        return None

    # ── Brain region ─────────────────────────────────────────────────────

    def get_brain_region_title(self, timeout=25):
        """Get the brain region displayed in the panel."""
        el = self.find_element(ExploreMeModelLocators.BR_CEREBRUM_TITLE, timeout=timeout)
        return el.text.strip()

    # ── Model / ME-model tab ─────────────────────────────────────────────

    def click_model_data_tab(self, timeout=15):
        tab = self.element_to_be_clickable(ExploreMeModelLocators.MODEL_DATA_TAB, timeout=timeout)
        tab.click()
        self.logger.info("Clicked Model data tab")
        time.sleep(2)

    def click_me_model_tab(self, timeout=25):
        tab = self.element_to_be_clickable(ExploreMeModelLocators.ME_MODEL_TAB, timeout=timeout)
        tab.click()
        self.logger.info("Clicked ME-model tab")
        time.sleep(3)

    # ── List view ────────────────────────────────────────────────────────

    def wait_for_table(self, timeout=30):
        """Wait for the ME-model table to be visible."""
        self.is_visible(ExploreMeModelLocators.LV_TABLE_BODY, timeout=timeout)
        self.logger.info("ME-model table is visible")
        time.sleep(2)

    def get_table_rows(self, timeout=20):
        """Return all visible table rows."""
        try:
            return self.find_all_elements(ExploreMeModelLocators.LV_TABLE_ROWS, timeout=timeout)
        except TimeoutException:
            return []

    def click_random_row(self):
        """Click a random row from the ME-model table."""
        rows = self.get_table_rows()
        if not rows:
            raise RuntimeError("No rows found in ME-model table")

        visible_rows = rows[:min(10, len(rows))]
        row = random.choice(visible_rows)
        row_text = row.text.split('\n')[0][:60]
        self.logger.info(f"Clicking row: '{row_text}...'")
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", row)
        time.sleep(1)
        try:
            ActionChains(self.browser).move_to_element(row).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", row)
        time.sleep(3)
        return row_text

    def click_detail_view_button(self, timeout=20):
        """Click 'Go to details page' button in the mini detail view."""
        btn = self.element_to_be_clickable(
            ExploreMeModelLocators.MINI_DETAIL_VIEW_BTN, timeout=timeout
        )
        old_url = self.browser.current_url
        btn.click()
        self.logger.info("Clicked detail view button")
        self.wait_for_url_change(old_url, timeout=25)
        time.sleep(3)

    def wait_for_spinner_to_disappear(self, timeout=15):
        return self.wait_for_element_to_disappear(ExploreMeModelLocators.SPINNER, timeout=timeout)

    # ── Detail View: Tabs ────────────────────────────────────────────────

    def find_overview_tab(self, timeout=15):
        return self.find_element(ExploreMeModelLocators.DV_OVERVIEW_TAB, timeout=timeout)

    def find_analysis_tab(self, timeout=15):
        return self.find_element(ExploreMeModelLocators.DV_ANALYSIS_TAB, timeout=timeout)

    def find_configuration_tab(self, timeout=15):
        return self.find_element(ExploreMeModelLocators.DV_CONFIGURATION_TAB, timeout=timeout)

    def find_related_artifacts_tab(self, timeout=15):
        return self.find_element(ExploreMeModelLocators.DV_RELATED_ARTIFACTS_TAB, timeout=timeout)

    def click_analysis_tab(self):
        tab = self.element_to_be_clickable(ExploreMeModelLocators.DV_ANALYSIS_TAB, timeout=10)
        tab.click()
        self.logger.info("Clicked Analysis tab")
        time.sleep(3)

    def click_configuration_tab(self):
        tab = self.element_to_be_clickable(ExploreMeModelLocators.DV_CONFIGURATION_TAB, timeout=10)
        tab.click()
        self.logger.info("Clicked Configuration tab")
        time.sleep(3)

    def click_related_artifacts_tab(self):
        tab = self.element_to_be_clickable(ExploreMeModelLocators.DV_RELATED_ARTIFACTS_TAB, timeout=10)
        tab.click()
        self.logger.info("Clicked Related artifacts tab")
        time.sleep(3)

    # ── Detail View: Action buttons ──────────────────────────────────────

    def find_copy_id_btn(self, timeout=10):
        return self.find_element(ExploreMeModelLocators.DV_COPY_ID_BTN, timeout=timeout)

    def find_simulate_btn(self, timeout=10):
        return self.find_element(ExploreMeModelLocators.DV_SIMULATE_BTN, timeout=timeout)

    def find_download_btn(self, timeout=10):
        return self.find_element(ExploreMeModelLocators.DV_DOWNLOAD_BTN, timeout=timeout)

    def click_copy_id(self):
        btn = self.element_to_be_clickable(ExploreMeModelLocators.DV_COPY_ID_BTN, timeout=10)
        btn.click()
        self.logger.info("Clicked Copy ID button")
        time.sleep(1)

    def click_simulate(self):
        """Click Simulate and measure redirect time."""
        import time as perf_time
        # Click the actual <a> link inside the Simulate div
        try:
            simulate_link = self.find_element(
                (By.XPATH, "//a[contains(@href,'simulate') and contains(@href,'memodel')]"),
                timeout=10
            )
        except Exception:
            # Fallback to the div
            simulate_link = self.element_to_be_clickable(ExploreMeModelLocators.DV_SIMULATE_BTN, timeout=10)

        old_url = self.browser.current_url
        start_time = perf_time.time()

        self.browser.execute_script("arguments[0].click();", simulate_link)
        self.logger.info("Clicked Simulate link")

        # Wait for redirect with performance measurement
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            WebDriverWait(self.browser, 30).until(
                lambda d: d.current_url != old_url
            )
            redirect_time = round(perf_time.time() - start_time, 2)
            self.logger.info(f"Simulate redirect took {redirect_time}s")
            if redirect_time > 5:
                self.logger.warning(f"PERFORMANCE: Simulate redirect took {redirect_time}s (expected < 5s)")
        except Exception:
            redirect_time = round(perf_time.time() - start_time, 2)
            self.logger.warning(f"Simulate did not redirect after {redirect_time}s")

        return old_url

    def click_download(self):
        btn = self.element_to_be_clickable(ExploreMeModelLocators.DV_DOWNLOAD_BTN, timeout=10)
        btn.click()
        self.logger.info("Clicked Download button")
        time.sleep(2)

    # ── Detail View: Overview metadata ───────────────────────────────────

    def get_overview_metadata(self):
        """Read all Overview tab metadata.
        Returns dict of {field_name: {'label_el': el, 'value_el': el, 'value': str, 'required': bool}}.
        """
        fields = {
            'Name': {
                'value_locator': ExploreMeModelLocators.DV_NAME_VALUE,
                'required': True,
            },
            'Description': {
                'label_locator': ExploreMeModelLocators.DV_DESCRIPTION_LABEL,
                'value_locator': ExploreMeModelLocators.DV_DESCRIPTION_VALUE,
                'required': False,
            },
            'Created by': {
                'label_locator': ExploreMeModelLocators.DV_CREATED_BY_LABEL,
                'value_locator': ExploreMeModelLocators.DV_CREATED_BY_VALUE,
                'required': True,
            },
            'Contributors': {
                'label_locator': ExploreMeModelLocators.DV_CONTRIBUTORS_LABEL,
                'value_locator': ExploreMeModelLocators.DV_CONTRIBUTORS_VALUE,
                'required': False,
            },
            'Institutional contributors': {
                'label_locator': ExploreMeModelLocators.DV_INSTITUTIONAL_CONTRIBUTORS_LABEL,
                'value_locator': ExploreMeModelLocators.DV_INSTITUTIONAL_CONTRIBUTORS_VALUE,
                'required': False,
            },
            'Brain region': {
                'label_locator': ExploreMeModelLocators.DV_BRAIN_REGION_LABEL,
                'value_locator': ExploreMeModelLocators.DV_BRAIN_REGION_VALUE,
                'required': True,
            },
            'E-type': {
                'label_locator': ExploreMeModelLocators.DV_ETYPE_LABEL,
                'value_locator': ExploreMeModelLocators.DV_ETYPE_VALUE,
                'required': True,
            },
            'Validated': {
                'label_locator': ExploreMeModelLocators.DV_VALIDATED_LABEL,
                'value_locator': ExploreMeModelLocators.DV_VALIDATED_VALUE,
                'required': True,
            },
            'Species': {
                'label_locator': ExploreMeModelLocators.DV_SPECIES_LABEL,
                'value_locator': ExploreMeModelLocators.DV_SPECIES_VALUE,
                'required': True,
            },
            'Registration date': {
                'label_locator': ExploreMeModelLocators.DV_REGISTRATION_DATE_LABEL,
                'value_locator': ExploreMeModelLocators.DV_REGISTRATION_DATE_VALUE,
                'required': True,
            },
            'M-type': {
                'label_locator': ExploreMeModelLocators.DV_MTYPE_LABEL,
                'value_locator': ExploreMeModelLocators.DV_MTYPE_VALUE,
                'required': True,
            },
            'Strain': {
                'label_locator': ExploreMeModelLocators.DV_STRAIN_LABEL,
                'value_locator': ExploreMeModelLocators.DV_STRAIN_VALUE,
                'required': False,
            },
        }

        results = {}
        for field_name, config in fields.items():
            value_text = ""
            value_el = None
            try:
                value_el = self.find_element(config['value_locator'], timeout=5)
                value_text = value_el.text.strip()
            except TimeoutException:
                pass

            results[field_name] = {
                'value': value_text,
                'element': value_el,
                'required': config['required'],
            }

        return results

    # ── Detail View: Analysis tab ────────────────────────────────────────

    def find_analysis_dropdown(self, timeout=10):
        return self.find_element(ExploreMeModelLocators.DV_ANALYSIS_DROPDOWN, timeout=timeout)

    def find_read_description_btn(self, timeout=10):
        return self.element_to_be_clickable(
            ExploreMeModelLocators.DV_ANALYSIS_READ_DESCRIPTION_BTN, timeout=timeout
        )

    def get_analysis_plots(self, timeout=15):
        """Return list of plot elements visible on the Analysis tab."""
        try:
            return self.find_all_elements(ExploreMeModelLocators.DV_ANALYSIS_PLOTS, timeout=timeout)
        except TimeoutException:
            return []

    def find_analysis_plot_text(self, timeout=10):
        """Return text explanation elements for plots."""
        try:
            return self.find_all_elements(ExploreMeModelLocators.DV_ANALYSIS_PLOT_TEXT, timeout=timeout)
        except TimeoutException:
            return []

    def find_analysis_plot_download_btn(self, timeout=10):
        return self.element_to_be_clickable(
            ExploreMeModelLocators.DV_ANALYSIS_PLOT_DOWNLOAD_BTN, timeout=timeout
        )

    def get_validation_cards(self, timeout=10):
        """Return all validation result card elements."""
        try:
            return self.find_all_elements(ExploreMeModelLocators.DV_ANALYSIS_VALIDATION_CARDS, timeout=timeout)
        except TimeoutException:
            return []

    def click_validation_card_toggle(self, index=0):
        """Click a validation card summary to expand/collapse it."""
        summaries = self.browser.find_elements(*ExploreMeModelLocators.DV_ANALYSIS_VALIDATION_SUMMARIES)
        if index < len(summaries):
            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", summaries[index])
            time.sleep(0.5)
            summaries[index].click()
            self.logger.info(f"Clicked validation card toggle [{index}]")
            time.sleep(1)

    # ── Detail View: Configuration tab ───────────────────────────────────

    def find_config_me_model_name(self, timeout=10):
        return self.find_element(ExploreMeModelLocators.DV_CONFIG_ME_MODEL_NAME, timeout=timeout)

    def find_config_m_model_section(self, timeout=10):
        return self.find_element(ExploreMeModelLocators.DV_CONFIG_M_MODEL_SECTION, timeout=timeout)

    def find_config_e_model_section(self, timeout=10):
        return self.find_element(ExploreMeModelLocators.DV_CONFIG_E_MODEL_SECTION, timeout=timeout)

    # ── Detail View: Related artifacts tab ───────────────────────────────

    def get_simulation_entries(self, timeout=10):
        """Return simulation entries if present, else empty list."""
        try:
            return self.find_all_elements(
                ExploreMeModelLocators.DV_RELATED_SIMULATION_ENTRIES, timeout=timeout
            )
        except TimeoutException:
            return []

    def find_no_simulations_message(self, timeout=10):
        """Return 'No simulations available' message element if present."""
        try:
            return self.find_element(
                ExploreMeModelLocators.DV_RELATED_NO_SIMULATIONS_MSG, timeout=timeout
            )
        except TimeoutException:
            return None

    # ── Detail View: Related artifacts — simulation data ─────────────────

    def get_simulation_name(self, sim_entry):
        """Get the simulation name from a related artifact entry."""
        try:
            name_el = sim_entry.find_element(By.XPATH, ".//div[contains(@class,'text-2xl') and contains(@class,'font-bold')]//a")
            return name_el.text.strip()
        except Exception:
            return None

    def get_simulation_params(self, sim_entry):
        """Get simulation parameters (Temperature, Time step, etc.) from an entry."""
        params = {}
        try:
            param_divs = sim_entry.find_elements(By.XPATH, ".//div[contains(@class,'font-thin')]")
            for label_div in param_divs:
                label = label_div.text.strip()
                try:
                    value_div = label_div.find_element(By.XPATH, "following-sibling::div[1]")
                    params[label] = value_div.text.strip()
                except Exception:
                    pass
        except Exception:
            pass
        return params

    def has_stimulus_plot(self, sim_entry):
        """Check if a stimulus plot (Plotly chart) is present in the simulation entry."""
        try:
            plots = sim_entry.find_elements(By.CSS_SELECTOR, "div.js-plotly-plot")
            return len(plots) > 0
        except Exception:
            return False

    def has_recording_section(self, sim_entry):
        """Check if a Recording section is present in the simulation entry."""
        try:
            recording = sim_entry.find_elements(By.XPATH, ".//div[contains(text(),'Recording')]")
            return len(recording) > 0
        except Exception:
            return False
