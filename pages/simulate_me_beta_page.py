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

    # ── Initialization tab ───────────────────────────────────────────────

    def click_initialization_tab(self):
        """Click the Initialization tab in the left menu."""
        btn = self.element_to_be_clickable(SimulateMeBetaLocators.CONFIG_INIT_TAB, timeout=10)
        btn.click()
        self.logger.info("Clicked Initialization tab")
        time.sleep(2)

    def is_initialization_tab_active(self):
        """Check if the Initialization tab has data-active='true'."""
        try:
            self.find_element(SimulateMeBetaLocators.CONFIG_INIT_TAB_ACTIVE, timeout=5)
            self.logger.info("Initialization tab is active")
            return True
        except TimeoutException:
            self.logger.warning("Initialization tab is NOT active")
            return False

    def get_config_block_labels_and_values(self):
        """Read all config block labels and their corresponding input values.
        Returns list of dicts: [{'label': str, 'value': str, 'has_number_input': bool, 'index': int}, ...]
        """
        blocks = self.find_all_elements(SimulateMeBetaLocators.CONFIG_BLOCK_ELEMENTS, timeout=10)
        results = []
        for i, block in enumerate(blocks):
            label = ""
            value = ""
            has_number_input = False
            try:
                label_el = block.find_element(By.CSS_SELECTOR, ".text-primary-9.text-base.font-semibold")
                label = label_el.text.strip()
            except Exception:
                pass
            try:
                input_el = block.find_element(By.CSS_SELECTOR, "input.ant-input-number-input")
                value = input_el.get_attribute("value") or ""
                has_number_input = True
            except Exception:
                pass
            if label:
                results.append({'label': label, 'value': value, 'has_number_input': has_number_input, 'index': i})
                self.logger.info(f"  Block: '{label}' = '{value}' (number_input={has_number_input})")
        self.logger.info(f"Found {len(results)} config blocks with labels")
        return results

    def verify_initialization_data(self):
        """Verify all labels are present and numeric blocks have values.
        Returns the list of block dicts.
        """
        blocks = self.get_config_block_labels_and_values()
        assert len(blocks) > 0, "Expected at least one config block on Initialization tab"
        for b in blocks:
            assert b['label'], f"Config block has empty label: {b}"
            if b['has_number_input']:
                assert b['value'], f"Config block '{b['label']}' has empty value"
        numeric_blocks = [b for b in blocks if b['has_number_input']]
        self.logger.info(f"All {len(numeric_blocks)} numeric Initialization blocks have labels and values")
        return blocks

    def add_parameter_sweep_value(self, block_index, value):
        """Add a sweep value to a specific config block.
        1. Click the plus-circle on the block to convert to sweep mode
        2. Click the inner plus-circle to add a new input row
        3. Type the value into the new empty input
        """
        from selenium.webdriver.common.action_chains import ActionChains

        # Find all config blocks that have a plus-circle button
        blocks = self.find_all_elements(SimulateMeBetaLocators.CONFIG_BLOCK_ELEMENTS, timeout=10)
        target_block = blocks[block_index]
        label = ""
        try:
            label = target_block.find_element(By.CSS_SELECTOR, ".text-primary-9.text-base.font-semibold").text.strip()
        except Exception:
            pass

        # Step 1: Click the first plus-circle to convert to sweep mode
        plus_btn = target_block.find_element(By.XPATH, ".//span[@aria-label='plus-circle']")
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", plus_btn)
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(plus_btn).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", plus_btn)
        self.logger.info(f"Clicked plus-circle on block [{block_index}] '{label}' to enable sweep")
        time.sleep(1)

        # Re-find the block after DOM change (it becomes float_parameter_sweep_multiple)
        blocks = self.find_all_elements(SimulateMeBetaLocators.CONFIG_BLOCK_ELEMENTS, timeout=10)
        target_block = blocks[block_index]

        # Step 2: Click the inner plus-circle to add a new input row
        inner_plus_btns = target_block.find_elements(By.XPATH, ".//span[@aria-label='plus-circle']")
        if inner_plus_btns:
            inner_plus = inner_plus_btns[-1]  # last plus-circle in the block
            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", inner_plus)
            time.sleep(0.5)
            try:
                ActionChains(self.browser).move_to_element(inner_plus).click().perform()
            except Exception:
                self.browser.execute_script("arguments[0].click();", inner_plus)
            self.logger.info(f"Clicked inner plus-circle to add new sweep input row")
            time.sleep(1)

        # Step 3: Find the empty input and type the value
        blocks = self.find_all_elements(SimulateMeBetaLocators.CONFIG_BLOCK_ELEMENTS, timeout=10)
        target_block = blocks[block_index]
        inputs = target_block.find_elements(By.CSS_SELECTOR, "input.ant-input-number-input")
        # Find the last input (the newly added empty one)
        if inputs:
            new_input = inputs[-1]
            new_input.click()
            new_input.clear()
            new_input.send_keys(str(value))
            self.logger.info(f"Typed sweep value '{value}' into block [{block_index}] '{label}'")
            time.sleep(0.5)

    def add_extra_sweep_value(self, block_index, value):
        """Add another sweep value to a block already in sweep mode.
        Clicks the inner plus-circle to add a new row, then types the value.
        """
        from selenium.webdriver.common.action_chains import ActionChains

        blocks = self.find_all_elements(SimulateMeBetaLocators.CONFIG_BLOCK_ELEMENTS, timeout=10)
        target_block = blocks[block_index]
        label = ""
        try:
            label = target_block.find_element(By.CSS_SELECTOR, ".text-primary-9.text-base.font-semibold").text.strip()
        except Exception:
            pass

        # Click the last plus-circle in the block to add a new input row
        plus_btns = target_block.find_elements(By.XPATH, ".//span[@aria-label='plus-circle']")
        if plus_btns:
            plus_btn = plus_btns[-1]
            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", plus_btn)
            time.sleep(0.5)
            try:
                ActionChains(self.browser).move_to_element(plus_btn).click().perform()
            except Exception:
                self.browser.execute_script("arguments[0].click();", plus_btn)
            self.logger.info(f"Clicked plus-circle to add sweep row in block [{block_index}] '{label}'")
            time.sleep(1)

        # Type value into the last (newly added) input
        blocks = self.find_all_elements(SimulateMeBetaLocators.CONFIG_BLOCK_ELEMENTS, timeout=10)
        target_block = blocks[block_index]
        inputs = target_block.find_elements(By.CSS_SELECTOR, "input.ant-input-number-input")
        if inputs:
            new_input = inputs[-1]
            new_input.click()
            new_input.clear()
            new_input.send_keys(str(value))
            self.logger.info(f"Typed extra sweep value '{value}' into block [{block_index}] '{label}'")
            time.sleep(0.5)

    def get_sweep_input_count(self, block_index):
        """Count how many sweep inputs exist in a specific config block."""
        blocks = self.find_all_elements(SimulateMeBetaLocators.CONFIG_BLOCK_ELEMENTS, timeout=10)
        target_block = blocks[block_index]
        inputs = target_block.find_elements(By.CSS_SELECTOR, "input.ant-input-number-input")
        count = len(inputs)
        self.logger.info(f"Block [{block_index}] has {count} input(s)")
        return count

    # ── Stimuli & Recordings ────────────────────────────────────────────

    def click_stimuli_tab(self):
        """Click the Stimuli tab in the left menu."""
        btn = self.element_to_be_clickable(SimulateMeBetaLocators.CONFIG_STIMULI_TAB, timeout=10)
        btn.click()
        self.logger.info("Clicked Stimuli tab")
        time.sleep(2)

    def is_stimuli_tab_active(self):
        """Check if the Stimuli tab has data-active='true'."""
        try:
            self.find_element(SimulateMeBetaLocators.CONFIG_STIMULI_TAB_ACTIVE, timeout=5)
            self.logger.info("Stimuli tab is active")
            return True
        except TimeoutException:
            self.logger.warning("Stimuli tab is NOT active")
            return False

    def click_recordings_tab(self):
        """Click the Recordings tab in the left menu."""
        btn = self.element_to_be_clickable(SimulateMeBetaLocators.CONFIG_RECORDINGS_TAB, timeout=10)
        btn.click()
        self.logger.info("Clicked Recordings tab")
        time.sleep(2)

    def is_recordings_tab_active(self):
        """Check if the Recordings tab has data-active='true'."""
        try:
            self.find_element(SimulateMeBetaLocators.CONFIG_RECORDINGS_TAB_ACTIVE, timeout=5)
            self.logger.info("Recordings tab is active")
            return True
        except TimeoutException:
            self.logger.warning("Recordings tab is NOT active")
            return False

    def get_stimuli_sub_entry(self, timeout=10):
        """Get the sub-entry container under Stimuli (holds Add button and stimulus items)."""
        try:
            return self.find_element(SimulateMeBetaLocators.CONFIG_STIMULI_SUB_ENTRY, timeout=timeout)
        except TimeoutException:
            self.logger.warning("Stimuli sub-entry container not found")
            return None

    def click_add_stimulus(self):
        """Click the 'Add Stimulus' button."""
        from selenium.webdriver.common.action_chains import ActionChains
        btn = self.element_to_be_clickable(SimulateMeBetaLocators.CONFIG_STIMULI_ADD_BTN, timeout=10)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(btn).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        self.logger.info("Clicked 'Add Stimulus' button")
        time.sleep(2)

    def get_stimuli_sub_items(self):
        """Get all stimulus sub-items in the left menu (e.g. Stimulus 1, Stimulus 2)."""
        try:
            items = self.find_all_elements(SimulateMeBetaLocators.CONFIG_STIMULI_SUB_ITEMS, timeout=10)
            labels = [item.text.strip() for item in items]
            self.logger.info(f"Stimuli sub-items: {labels}")
            return items
        except TimeoutException:
            self.logger.warning("No stimuli sub-items found")
            return []

    def click_stimulus_sub_item(self, index=0):
        """Click a specific stimulus sub-item by index."""
        from selenium.webdriver.common.action_chains import ActionChains
        items = self.get_stimuli_sub_items()
        if index < len(items):
            item = items[index]
            label = item.text.strip()
            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", item)
            time.sleep(0.5)
            try:
                ActionChains(self.browser).move_to_element(item).click().perform()
            except Exception:
                self.browser.execute_script("arguments[0].click();", item)
            self.logger.info(f"Clicked stimulus sub-item [{index}]: '{label}'")
            time.sleep(1)
            return label
        else:
            raise IndexError(f"Stimulus sub-item index {index} out of range (have {len(items)})")

    def get_stimuli_config_blocks(self):
        """Read all config block labels and values on the current Stimuli view.
        Returns list of dicts: [{'label': str, 'value': str, 'has_number_input': bool,
                                  'has_select': bool, 'index': int}, ...]
        """
        blocks = self.find_all_elements(SimulateMeBetaLocators.CONFIG_BLOCK_ELEMENTS, timeout=10)
        results = []
        for i, block in enumerate(blocks):
            label = ""
            value = ""
            has_number_input = False
            has_select = False
            try:
                label_el = block.find_element(By.CSS_SELECTOR, ".text-primary-9.text-base.font-semibold")
                label = label_el.text.strip()
            except Exception:
                pass
            try:
                input_el = block.find_element(By.CSS_SELECTOR, "input.ant-input-number-input")
                value = input_el.get_attribute("value") or ""
                has_number_input = True
            except Exception:
                pass
            if not has_number_input:
                try:
                    select_el = block.find_element(By.CSS_SELECTOR, ".ant-select-selection-item")
                    value = select_el.text.strip()
                    has_select = True
                except Exception:
                    pass
            if not value:
                try:
                    string_input = block.find_element(By.CSS_SELECTOR, "input[data-scan-config-block-element='string_input']")
                    value = string_input.get_attribute("value") or ""
                except Exception:
                    pass
            if label:
                results.append({
                    'label': label, 'value': value,
                    'has_number_input': has_number_input,
                    'has_select': has_select, 'index': i
                })
                self.logger.info(f"  Stimuli block: '{label}' = '{value}' "
                                 f"(number={has_number_input}, select={has_select})")
        self.logger.info(f"Found {len(results)} stimuli config blocks")
        return results

    def verify_stimuli_data(self):
        """Verify stimuli tab has blocks with labels. Returns the block list."""
        blocks = self.get_stimuli_config_blocks()
        assert len(blocks) > 0, "Expected at least one config block on Stimuli tab"
        for b in blocks:
            assert b['label'], f"Stimuli block has empty label: {b}"
        self.logger.info(f"Stimuli tab has {len(blocks)} blocks, all with labels")
        return blocks

    # ── Neuronal manipulations tab ──────────────────────────────────────

    def click_neuronal_manip_tab(self):
        """Click the Neuronal manipulations tab in the left menu."""
        btn = self.element_to_be_clickable(SimulateMeBetaLocators.CONFIG_NEURONAL_MANIP_TAB, timeout=10)
        btn.click()
        self.logger.info("Clicked Neuronal manipulations tab")
        time.sleep(2)

    def is_neuronal_manip_tab_active(self):
        """Check if the Neuronal manipulations tab has data-active='true'."""
        try:
            self.find_element(SimulateMeBetaLocators.CONFIG_NEURONAL_MANIP_TAB_ACTIVE, timeout=5)
            self.logger.info("Neuronal manipulations tab is active")
            return True
        except TimeoutException:
            self.logger.warning("Neuronal manipulations tab is NOT active")
            return False

    # ── Generic dictionary tab flow ─────────────────────────────────────

    def click_add_button_in_active_sub_entry(self):
        """Click the 'Add X' button inside the currently active sub-entry."""
        from selenium.webdriver.common.action_chains import ActionChains
        btn = self.element_to_be_clickable(SimulateMeBetaLocators.CONFIG_ADD_BTN_IN_SUB_ENTRY, timeout=10)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(btn).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        self.logger.info(f"Clicked 'Add' button: '{btn.text.strip()}'")
        time.sleep(2)

    def get_dictionary_items(self, timeout=10):
        """Get all block_dictionary_item buttons in the middle column."""
        try:
            items = self.find_all_elements(SimulateMeBetaLocators.CONFIG_BLOCK_DICTIONARY_ITEMS, timeout=timeout)
            labels = [item.text.strip() for item in items]
            self.logger.info(f"Dictionary items: {labels}")
            return items
        except TimeoutException:
            self.logger.warning("No dictionary items found")
            return []

    def click_random_dictionary_item(self):
        """Click a random block_dictionary_item from the middle column.
        Returns the label text of the clicked item.
        """
        from selenium.webdriver.common.action_chains import ActionChains
        items = self.get_dictionary_items()
        assert items, "No dictionary items found to click"
        item = random.choice(items)
        label = item.text.strip()
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", item)
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(item).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", item)
        self.logger.info(f"Clicked dictionary item: '{label}'")
        time.sleep(2)
        return label

    def wait_for_block_single(self, timeout=10):
        """Wait for a block_single form to appear after selecting a dictionary item."""
        el = self.find_element(SimulateMeBetaLocators.CONFIG_BLOCK_SINGLE, timeout=timeout)
        self.logger.info("block_single form appeared")
        return el

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
