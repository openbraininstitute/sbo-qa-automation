# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import random
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from pages.home_page import HomePage
from locators.simulate_me_beta_locators import SimulateMeBetaLocators


class SimulateMeBetaPage(HomePage):
    """Page object for the ME-model picker page (single neuron beta simulation)."""

    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, base_url)
        self.logger = logger

    # ── Navigation ───────────────────────────────────────────────────────

    def go_to_simulation_page(self, lab_id, project_id,
                               br_id=None, br_av=None,
                               retries=3, delay=5):
        """Navigate to the ME-model circuit simulation page."""
        path = (f"/app/virtual-lab/{lab_id}/{project_id}"
                f"/workflows/simulate/new/me-model-circuit-simulation")
        if br_id and br_av:
            path += f"?br_id={br_id}&br_av={br_av}"

        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(90)
                self.go_to_page(path)
                self.wait_for_page_ready(timeout=60)
                self.logger.info(f"Navigated to simulation page: {self.browser.current_url}")
                return self.browser.current_url
            except TimeoutException:
                self.logger.warning(f"Attempt {attempt + 1} failed. Retrying in {delay}s...")
                time.sleep(delay)
                if attempt == retries - 1:
                    raise RuntimeError("Simulation page did not load within timeout")
        return self.browser.current_url

    def wait_for_page_ready(self, timeout=30):
        """Wait for the page to be fully loaded."""
        super().wait_for_page_ready(timeout=timeout)
        time.sleep(2)

    # ── Tabs ─────────────────────────────────────────────────────────────

    def click_public_tab(self):
        """Click the Public tab."""
        el = self.find_element(SimulateMeBetaLocators.PUBLIC_TAB, timeout=15)
        el.click()
        self.logger.info("Clicked Public tab")
        time.sleep(3)

    def click_project_tab(self):
        """Click the Project tab."""
        el = self.find_element(SimulateMeBetaLocators.PROJECT_TAB, timeout=15)
        el.click()
        self.logger.info("Clicked Project tab")
        time.sleep(3)

    # ── Column headers ───────────────────────────────────────────────────

    EXPECTED_COLUMNS = [
        'Name', 'Morphology', 'Trace', 'Validated',
        'Brain region', 'M-type', 'E-type',
        'Created by', 'Registration date',
    ]

    COLUMN_LOCATORS = {
        'Name': SimulateMeBetaLocators.COL_NAME,
        'Morphology': SimulateMeBetaLocators.COL_MORPHOLOGY,
        'Trace': SimulateMeBetaLocators.COL_TRACE,
        'Validated': SimulateMeBetaLocators.COL_VALIDATED,
        'Brain region': SimulateMeBetaLocators.COL_BRAIN_REGION,
        'M-type': SimulateMeBetaLocators.COL_MTYPE,
        'E-type': SimulateMeBetaLocators.COL_ETYPE,
        'Created by': SimulateMeBetaLocators.COL_CREATED_BY,
        'Registration date': SimulateMeBetaLocators.COL_REGISTRATION_DATE,
    }

    def verify_column_headers(self):
        """Verify all expected column headers are present.
        Returns dict of column_name -> {present: bool, displayed: bool}.
        """
        results = {}
        for name, locator in self.COLUMN_LOCATORS.items():
            try:
                el = self.find_element(locator, timeout=10)
                results[name] = {'present': True, 'displayed': el.is_displayed()}
                self.logger.info(f"Column '{name}' found")
            except TimeoutException:
                results[name] = {'present': False, 'displayed': False}
                self.logger.warning(f"Column '{name}' not found")
        return results

    def find_column_header(self, column_name, timeout=10):
        """Find a specific column header by name."""
        locator = self.COLUMN_LOCATORS.get(column_name)
        if not locator:
            raise ValueError(f"Unknown column: {column_name}")
        return self.find_element(locator, timeout=timeout)

    # ── Table rows ───────────────────────────────────────────────────────

    def get_table_rows(self, timeout=15):
        """Get all visible table rows."""
        self.find_element(SimulateMeBetaLocators.TABLE_ROWS, timeout=timeout)
        return self.browser.find_elements(*SimulateMeBetaLocators.TABLE_ROWS)

    def get_row_count(self):
        """Get the number of visible table rows."""
        rows = self.get_table_rows()
        count = len(rows)
        self.logger.info(f"Table has {count} rows")
        return count

    def click_random_row(self):
        """Click a random row in the table, using ActionChains for reliable click."""
        from selenium.webdriver.common.action_chains import ActionChains
        rows = self.get_table_rows()
        if not rows:
            raise RuntimeError("No rows found in the table")
        # Pick from first 10 rows to avoid scroll issues
        visible_rows = rows[:min(10, len(rows))]
        row = random.choice(visible_rows)
        row_text = row.text.split('\n')[0][:60]
        self.logger.info(f"Clicking random row: '{row_text}...'")
        # Scroll into view first
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", row)
        time.sleep(1)
        # Use ActionChains for a real click that triggers event listeners
        try:
            ActionChains(self.browser).move_to_element(row).click().perform()
        except Exception:
            self.logger.info("ActionChains click failed, using JS click")
            self.browser.execute_script("arguments[0].click();", row)
        time.sleep(3)
        return row_text

    def click_first_row(self):
        """Click the first row in the table."""
        from selenium.webdriver.common.action_chains import ActionChains
        row = self.find_element(SimulateMeBetaLocators.TABLE_FIRST_ROW, timeout=15)
        row_text = row.text.split('\n')[0][:60]
        self.logger.info(f"Clicking first row: '{row_text}...'")
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", row)
        time.sleep(1)
        try:
            ActionChains(self.browser).move_to_element(row).click().perform()
        except Exception:
            self.logger.info("ActionChains click failed, using JS click")
            self.browser.execute_script("arguments[0].click();", row)
        time.sleep(3)
        return row_text

    def log_table_header_order(self):
        """Log the actual column header order to verify indices."""
        try:
            headers = self.browser.find_elements("css selector", "th[data-testid='column-header']")
            for i, h in enumerate(headers):
                self.logger.info(f"  Column [{i}]: '{h.text.strip()}'")
        except Exception as e:
            self.logger.warning(f"Could not read column headers: {e}")

    def get_etype_column_values(self):
        """Get all E-type values from the visible rows by finding the E-type column index dynamically."""
        # Find E-type column index from headers
        etype_idx = None
        try:
            headers = self.browser.find_elements("css selector", "th[data-testid='column-header']")
            for i, h in enumerate(headers):
                if 'E-type' in h.text:
                    etype_idx = i
                    break
        except Exception:
            pass

        if etype_idx is None:
            self.logger.warning("E-type column header not found, defaulting to index 6")
            etype_idx = 6

        self.logger.info(f"E-type column index: {etype_idx}")

        rows = self.get_table_rows()
        values = []
        for row in rows:
            cells = row.find_elements("tag name", "td")
            if len(cells) > etype_idx:
                values.append(cells[etype_idx].text.strip())
        self.logger.info(f"E-type values: {values[:5]}...")
        return values

    # ── Filter panel ─────────────────────────────────────────────────────

    def open_filter_panel(self):
        """Click the Filters button to open the filter panel."""
        btn = self.find_element(SimulateMeBetaLocators.FILTER_BUTTON, timeout=10)
        btn.click()
        self.logger.info("Opened filter panel")
        time.sleep(2)

    def close_filter_panel(self):
        """Close the filter panel."""
        btn = self.find_element(SimulateMeBetaLocators.FILTER_CLOSE_BUTTON, timeout=5)
        btn.click()
        self.logger.info("Closed filter panel")
        time.sleep(1)

    def expand_etype_filter(self):
        """Expand the E-type accordion in the filter panel."""
        trigger = self.find_element(SimulateMeBetaLocators.FILTER_ETYPE_TRIGGER, timeout=10)
        trigger.click()
        self.logger.info("Expanded E-type filter")
        time.sleep(1)

    def type_etype_filter(self, value):
        """Type a value into the E-type filter search input."""
        input_el = self.find_element(
            SimulateMeBetaLocators.FILTER_ETYPE_SEARCH_INPUT, timeout=10
        )
        input_el.click()
        input_el.send_keys(value)
        self.logger.info(f"Typed '{value}' in E-type filter")
        time.sleep(2)

    def select_etype_option(self, option_text):
        """Select an option from the E-type dropdown."""
        locator = (By.XPATH, f"//div[contains(@class,'ant-select-item-option') and @title='{option_text}']")
        option = self.element_to_be_clickable(locator, timeout=10)
        option.click()
        self.logger.info(f"Selected E-type option: '{option_text}'")
        time.sleep(1)

    def click_filter_apply(self):
        """Click the Apply button in the filter panel."""
        try:
            btn = self.find_element(SimulateMeBetaLocators.FILTER_APPLY_BUTTON, timeout=5)
            btn.click()
            self.logger.info("Clicked Apply filter")
        except TimeoutException:
            self.logger.info("No explicit Apply button found — filter may auto-apply")
        time.sleep(3)

    def filter_by_etype(self, etype_value):
        """Full flow: open filters, expand E-type, type value, select, close."""
        self.open_filter_panel()
        self.expand_etype_filter()
        self.type_etype_filter(etype_value)
        self.select_etype_option(etype_value)
        self.close_filter_panel()
        time.sleep(2)

    # ── Search ───────────────────────────────────────────────────────────

    def open_search(self):
        """Click the search button to open the search input."""
        btn = self.find_element(SimulateMeBetaLocators.SEARCH_BUTTON, timeout=10)
        btn.click()
        self.logger.info("Opened search")
        time.sleep(1)

    def search_for(self, query):
        """Type a search query."""
        self.open_search()
        input_el = self.find_element(SimulateMeBetaLocators.SEARCH_INPUT, timeout=10)
        input_el.clear()
        input_el.send_keys(query)
        self.logger.info(f"Searched for: '{query}'")
        time.sleep(3)

    # ── Breadcrumbs ──────────────────────────────────────────────────────

    def find_breadcrumb_workflows(self, timeout=10):
        return self.find_element(SimulateMeBetaLocators.BREADCRUMB_WORKFLOWS, timeout=timeout)

    def click_breadcrumb_workflows(self):
        link = self.find_breadcrumb_workflows()
        link.click()
        self.logger.info("Clicked Workflows breadcrumb")
        time.sleep(2)

    # ── Mini-detail view ────────────────────────────────────────────────

    def wait_for_mini_detail(self, timeout=15):
        """Wait for the mini-detail view to appear after clicking a row."""
        self.element_visibility(SimulateMeBetaLocators.MINI_VIEWER, timeout=timeout)
        self.logger.info("Mini-detail view appeared")
        time.sleep(1)

    def find_mini_detail_title(self, timeout=10):
        """Find the title (h1) in the mini-detail view."""
        return self.find_element(SimulateMeBetaLocators.MINI_DETAIL_TITLE, timeout=timeout)

    def find_mini_detail_description(self, timeout=10):
        """Find the description paragraph in the mini-detail view."""
        return self.find_element(SimulateMeBetaLocators.MINI_DETAIL_DESCRIPTION, timeout=timeout)

    def find_mini_detail_images(self, timeout=10):
        """Find all images in the mini-detail view."""
        return self.find_all_elements(SimulateMeBetaLocators.MINI_DETAIL_IMAGES, timeout=timeout)

    def get_mini_detail_metadata(self, timeout=10):
        """Get metadata labels and values from the mini-detail view.
        Returns dict of label -> value.
        """
        labels = self.find_all_elements(SimulateMeBetaLocators.MINI_DETAIL_METADATA_LABELS, timeout=timeout)
        metadata = {}
        for label_el in labels:
            label_text = label_el.text.strip()
            try:
                parent = label_el.find_element(By.XPATH, "..")
                value_el = parent.find_element(By.CSS_SELECTOR, ".font-bold")
                metadata[label_text] = value_el.text.strip()
            except Exception:
                metadata[label_text] = ""
        self.logger.info(f"Mini-detail metadata: {metadata}")
        return metadata

    def find_view_details_btn(self, timeout=10):
        """Find the 'View details' button in the mini-detail view."""
        return self.find_element(SimulateMeBetaLocators.MINI_DETAIL_VIEW_DETAILS_BTN, timeout=timeout)

    def find_use_model_btn(self, timeout=10):
        """Find the 'Use model' button in the mini-detail view."""
        return self.find_element(SimulateMeBetaLocators.MINI_DETAIL_USE_MODEL_BTN, timeout=timeout)

    def click_use_model(self):
        """Click the 'Use model' button to go to the config page."""
        btn = self.find_use_model_btn()
        href = btn.get_attribute("href")
        self.logger.info(f"Clicking 'Use model', href: {href}")
        try:
            btn.click()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        time.sleep(5)
        return href

    def verify_mini_detail_view(self):
        """Verify all expected elements in the mini-detail view.
        Returns dict of element_name -> {present: bool, displayed: bool}.
        """
        checks = {
            'title': SimulateMeBetaLocators.MINI_DETAIL_TITLE,
            'description': SimulateMeBetaLocators.MINI_DETAIL_DESCRIPTION,
            'view_details_btn': SimulateMeBetaLocators.MINI_DETAIL_VIEW_DETAILS_BTN,
            'use_model_btn': SimulateMeBetaLocators.MINI_DETAIL_USE_MODEL_BTN,
        }
        results = {}
        for name, locator in checks.items():
            try:
                el = self.find_element(locator, timeout=10)
                results[name] = {'present': True, 'displayed': el.is_displayed()}
                self.logger.info(f"Mini-detail '{name}' found")
            except TimeoutException:
                results[name] = {'present': False, 'displayed': False}
                self.logger.warning(f"Mini-detail '{name}' not found")

        # Check images separately (multiple)
        try:
            imgs = self.find_mini_detail_images(timeout=10)
            results['images'] = {'present': True, 'displayed': len(imgs) > 0, 'count': len(imgs)}
            self.logger.info(f"Mini-detail images: {len(imgs)} found")
        except TimeoutException:
            results['images'] = {'present': False, 'displayed': False, 'count': 0}
            self.logger.warning("Mini-detail images not found")

        # Check metadata
        try:
            metadata = self.get_mini_detail_metadata(timeout=10)
            results['metadata'] = {'present': True, 'displayed': len(metadata) > 0, 'fields': list(metadata.keys())}
            self.logger.info(f"Mini-detail metadata fields: {list(metadata.keys())}")
        except TimeoutException:
            results['metadata'] = {'present': False, 'displayed': False, 'fields': []}
            self.logger.warning("Mini-detail metadata not found")

        return results

    # ── Config page ──────────────────────────────────────────────────────

    def wait_for_config_page(self, timeout=30):
        """Wait for the config page layout to appear."""
        self.find_element(SimulateMeBetaLocators.CONFIG_LAYOUT, timeout=timeout)
        self.logger.info("Config page layout loaded")
        time.sleep(2)

    def wait_for_neuron_visualizer(self, timeout=60):
        """Wait for the 3D morphology viewer canvas to be present."""
        self.wait_for_long_load(SimulateMeBetaLocators.NEURON_VISUALIZER_CANVAS, timeout=timeout)
        self.logger.info("Neuron visualizer canvas loaded")
        time.sleep(2)

    def find_config_tab(self, timeout=10):
        """Find the Configuration tab button."""
        return self.find_element(SimulateMeBetaLocators.CONFIG_TAB_CONFIGURATION, timeout=timeout)

    def find_simulations_tab(self, timeout=10):
        """Find the Simulations tab button."""
        return self.find_element(SimulateMeBetaLocators.CONFIG_TAB_SIMULATIONS, timeout=timeout)

    def verify_config_tabs(self):
        """Verify Configuration and Simulations tabs are present.
        Returns dict of tab_name -> {present: bool, displayed: bool}.
        """
        results = {}
        for name, locator in [
            ('configuration', SimulateMeBetaLocators.CONFIG_TAB_CONFIGURATION),
            ('simulations', SimulateMeBetaLocators.CONFIG_TAB_SIMULATIONS),
        ]:
            try:
                el = self.find_element(locator, timeout=10)
                results[name] = {'present': True, 'displayed': el.is_displayed()}
                self.logger.info(f"Config tab '{name}' found")
            except TimeoutException:
                results[name] = {'present': False, 'displayed': False}
                self.logger.warning(f"Config tab '{name}' not found")
        return results

    def is_info_tab_active(self):
        """Check if the 'Info' menu item is active (blue background)."""
        try:
            active_btn = self.find_element(
                SimulateMeBetaLocators.CONFIG_LEFT_MENU_INFO_ACTIVE, timeout=5
            )
            text = active_btn.text.strip()
            is_info = 'Info' in text
            self.logger.info(f"Active left menu item: '{text}', is Info: {is_info}")
            return is_info
        except TimeoutException:
            self.logger.warning("No active left menu item found")
            return False

    def fill_campaign_name(self, name):
        """Fill in the Campaign Name input."""
        input_el = self.find_element(SimulateMeBetaLocators.CONFIG_CAMPAIGN_NAME_INPUT, timeout=10)
        input_el.clear()
        input_el.send_keys(name)
        self.logger.info(f"Filled campaign name: '{name}'")

    def fill_campaign_description(self, description):
        """Fill in the Campaign Description input."""
        input_el = self.find_element(SimulateMeBetaLocators.CONFIG_CAMPAIGN_DESC_INPUT, timeout=10)
        input_el.clear()
        input_el.send_keys(description)
        self.logger.info(f"Filled campaign description: '{description}'")

    def verify_top_nav(self):
        """Verify top navigation items are present."""
        nav_items = {
            'Home': SimulateMeBetaLocators.NAV_HOME,
            'Data': SimulateMeBetaLocators.NAV_DATA,
            'Workflows': SimulateMeBetaLocators.NAV_WORKFLOWS,
            'Notebooks': SimulateMeBetaLocators.NAV_NOTEBOOKS,
            'Reports': SimulateMeBetaLocators.NAV_REPORTS,
        }
        results = {}
        for name, locator in nav_items.items():
            try:
                el = self.find_element(locator, timeout=5)
                results[name] = {'present': True, 'displayed': el.is_displayed()}
            except TimeoutException:
                results[name] = {'present': False, 'displayed': False}
        self.logger.info(f"Top nav: {list(results.keys())}")
        return results

    # ── Debug ────────────────────────────────────────────────────────────

    def log_page_structure(self):
        """Log key page elements for debugging."""
        self.logger.info("=== PAGE STRUCTURE DEBUG ===")
        self.logger.info(f"URL: {self.browser.current_url}")
        self.logger.info(f"Title: {self.browser.title}")
        for tag in ['h1', 'h2', 'h3']:
            try:
                elements = self.browser.find_elements("tag name", tag)
                for el in elements:
                    self.logger.info(f"  <{tag}>: '{el.text.strip()}'")
            except Exception:
                pass
        try:
            buttons = self.browser.find_elements("tag name", "button")
            for btn in buttons[:20]:
                self.logger.info(f"  <button>: '{btn.text.strip()}' enabled={btn.is_enabled()}")
        except Exception:
            pass
        try:
            inputs = self.browser.find_elements("tag name", "input")
            for inp in inputs[:20]:
                name = inp.get_attribute('name') or ''
                placeholder = inp.get_attribute('placeholder') or ''
                self.logger.info(f"  <input>: name='{name}' placeholder='{placeholder}' type='{inp.get_attribute('type')}'")
        except Exception:
            pass
        self.logger.info("=== END PAGE STRUCTURE ===")
