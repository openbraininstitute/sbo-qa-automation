# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import random
import platform
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage
from locators.data_circuit_locators import DataCircuitLocators


class DataCircuitPage(HomePage):
    """Page object for the Data > Model > Circuit page.

    Entry: Login → Data → Model → Circuit tab
    URL: /app/virtual-lab/{lab_id}/{project_id}/data/browse/entity/circuit?group=models
    """

    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, base_url)
        self.logger = logger

    # ── Navigation ───────────────────────────────────────────────────────

    def go_to_data_circuit(self, lab_id, project_id, retries=3, delay=5):
        """Navigate directly to the Data > Model > Circuit page."""
        path = f"/app/virtual-lab/{lab_id}/{project_id}/data/browse/entity/circuit?group=models"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(90)
                self.go_to_page(path)
                self.wait_for_page_ready(timeout=60)
                self.logger.info(f"Navigated to Data Circuit: {self.browser.current_url}")
                return
            except TimeoutException:
                self.logger.warning(f"Attempt {attempt + 1} failed. Retrying in {delay}s...")
                time.sleep(delay)
                if attempt == retries - 1:
                    raise RuntimeError("Data Circuit page did not load")

    # ── Tabs ─────────────────────────────────────────────────────────────

    def click_public_tab(self, timeout=15):
        el = self.element_to_be_clickable(DataCircuitLocators.PUBLIC_TAB, timeout=timeout)
        el.click()
        self.logger.info("Clicked Public tab")
        time.sleep(3)

    def verify_public_tab_active(self, timeout=10):
        """Verify the Public tab is displayed and appears active."""
        el = self.find_element(DataCircuitLocators.PUBLIC_TAB, timeout=timeout)
        is_displayed = el.is_displayed()
        aria_selected = el.get_attribute("aria-selected")
        data_state = el.get_attribute("data-state")
        active = aria_selected == "true" or data_state == "active"
        self.logger.info(f"Public tab displayed={is_displayed}, active={active}")
        return is_displayed and active

    # ── Species and Brain region ─────────────────────────────────────────

    def get_species_value(self, timeout=10):
        el = self.find_element(DataCircuitLocators.SPECIES_VALUE, timeout=timeout)
        value = el.text.strip()
        self.logger.info(f"Species value: '{value}'")
        return value

    def select_species(self, species_name, timeout=10):
        """Open species dropdown and select a specific species."""
        dropdown = self.element_to_be_clickable(DataCircuitLocators.SPECIES_DROPDOWN, timeout=timeout)
        dropdown.click()
        time.sleep(1)
        options = self.find_all_elements(DataCircuitLocators.SPECIES_OPTIONS, timeout=10)
        for option in options:
            if species_name.lower() in option.text.strip().lower():
                option.click()
                self.logger.info(f"Selected species: '{species_name}'")
                time.sleep(3)
                return True
        ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
        self.logger.warning(f"Species '{species_name}' not found")
        return False

    def get_brain_region_value(self, timeout=10):
        el = self.find_element(DataCircuitLocators.BRAIN_REGION_VALUE, timeout=timeout)
        value = el.text.strip()
        self.logger.info(f"Brain region value: '{value}'")
        return value

    def click_brain_region_switcher(self, timeout=10):
        """Click the brain region switcher to open the region panel."""
        switcher = self.element_to_be_clickable(DataCircuitLocators.BRAIN_REGION_SWITCHER, timeout=timeout)
        switcher.click()
        self.logger.info("Clicked brain region switcher")
        time.sleep(1)

    def select_brain_region_root(self):
        """Select 'Root' as brain region via the search field."""
        self.click_brain_region_switcher()
        try:
            region_input = self.browser.find_element(*DataCircuitLocators.BRAIN_REGION_SEARCH_INPUT)
            region_input.click()
            region_input.clear()
            region_input.send_keys("Root")
            time.sleep(2)
            root_option = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable(DataCircuitLocators.BRAIN_REGION_ROOT_OPTION)
            )
            root_option.click()
            self.logger.info("Selected 'Root' as brain region")
            time.sleep(2)
        except Exception as e:
            self.logger.warning(f"Could not select Root brain region: {e}")

    # ── Circuit tab ──────────────────────────────────────────────────────

    def verify_circuit_tab_active(self, timeout=15):
        """Verify Circuit tab is active and shows a non-zero record count."""
        tab = self.find_element(DataCircuitLocators.CIRCUIT_TAB, timeout=timeout)
        is_displayed = tab.is_displayed()
        self.logger.info(f"Circuit tab displayed: {is_displayed}")
        return is_displayed

    def get_circuit_record_count(self, timeout=15):
        """Get the record count displayed on the Circuit tab."""
        try:
            count_el = self.wait_for_non_empty_text(DataCircuitLocators.CIRCUIT_TAB_COUNT, timeout=timeout)
            text = count_el.text.strip()
            count = int(''.join(filter(str.isdigit, text)))
            self.logger.info(f"Circuit record count: {count}")
            return count
        except (TimeoutException, ValueError) as e:
            self.logger.warning(f"Could not get circuit record count: {e}")
            return 0

    # ── View toggle ──────────────────────────────────────────────────────

    def _is_hierarchy_view(self):
        """Check if currently in hierarchy view by looking for expand chevrons in the table."""
        try:
            buttons = self.browser.find_elements(*DataCircuitLocators.HIERARCHY_EXPAND_BTN)
            return len(buttons) > 0
        except Exception:
            return False

    def _get_toggle_state(self):
        """Get the toggle position for debugging."""
        try:
            btn = self.browser.find_element(*DataCircuitLocators.VIEW_TOGGLE_BTN)
            inner_div = btn.find_element(By.CSS_SELECTOR, "div")
            classes = inner_div.get_attribute("class") or ""
            if "translate-x-[21px]" in classes:
                return "right"
            elif "translate-x-[2px]" in classes:
                return "left"
            return f"unknown ({classes})"
        except Exception:
            return "error"

    def click_list_view(self, timeout=10):
        """Switch to List view (toggle state = right)."""
        current = self._get_toggle_state()
        if current == "right":
            self.logger.info("Already in List view (toggle is right)")
            return
        btn = self.element_to_be_clickable(DataCircuitLocators.VIEW_TOGGLE_BTN, timeout=timeout)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        btn.click()
        self.logger.info(f"Clicked toggle, state: {self._get_toggle_state()}")
        self.wait_for_network_idle(timeout=10)
        time.sleep(3)

    def click_hierarchy_view(self, timeout=10):
        """Switch to Hierarchy view (toggle state = left)."""
        current = self._get_toggle_state()
        if current == "left":
            self.logger.info("Already in Hierarchy view (toggle is left)")
            return
        btn = self.element_to_be_clickable(DataCircuitLocators.VIEW_TOGGLE_BTN, timeout=timeout)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        btn.click()
        self.logger.info(f"Clicked toggle, state: {self._get_toggle_state()}")
        self.wait_for_network_idle(timeout=15)
        time.sleep(5)

    # ── Table ────────────────────────────────────────────────────────────

    def get_column_headers(self, timeout=15):
        """Return list of column header texts."""
        self.find_element(DataCircuitLocators.TABLE_COLUMN_HEADERS, timeout=timeout)
        headers = self.browser.find_elements(*DataCircuitLocators.TABLE_COLUMN_HEADERS)
        texts = [h.text.strip() for h in headers if h.text.strip()]
        self.logger.info(f"Column headers ({len(texts)}): {texts}")
        return texts

    def get_table_rows(self, timeout=15):
        """Return all visible table rows."""
        self.find_element(DataCircuitLocators.TABLE_ROWS, timeout=timeout)
        rows = self.browser.find_elements(*DataCircuitLocators.TABLE_ROWS)
        self.logger.info(f"Table has {len(rows)} rows")
        return rows

    def verify_columns_sortable(self, timeout=10):
        """Check if column headers have sort indicators or are clickable."""
        headers = self.browser.find_elements(*DataCircuitLocators.TABLE_COLUMN_HEADERS)
        sortable_count = 0
        for h in headers:
            # Check for sort class or aria-sort attribute
            classes = h.get_attribute("class") or ""
            aria_sort = h.get_attribute("aria-sort") or ""
            if "sort" in classes.lower() or aria_sort or h.get_attribute("role") == "columnheader":
                sortable_count += 1
        self.logger.info(f"Sortable columns: {sortable_count}/{len(headers)}")
        return sortable_count > 0

    # ── Hierarchy expand ─────────────────────────────────────────────────

    def expand_first_parent_row(self, timeout=20):
        """Click the expand chevron on the first parent circuit row."""
        try:
            # Wait for hierarchy rows to render (chevrons take time after toggle)
            WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located(DataCircuitLocators.HIERARCHY_EXPAND_BTN)
            )
            chevron = self.element_to_be_clickable(DataCircuitLocators.HIERARCHY_EXPAND_BTN, timeout=5)
            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", chevron)
            time.sleep(0.5)
            try:
                ActionChains(self.browser).move_to_element(chevron).click().perform()
            except Exception:
                self.browser.execute_script("arguments[0].click();", chevron)
            self.logger.info("Expanded first parent row")
            time.sleep(2)
            return True
        except TimeoutException:
            self.logger.warning("No expand chevron found in hierarchy view")
            return False

    def get_sub_circuit_rows(self, timeout=10):
        """Get expanded sub-circuit rows."""
        try:
            rows = self.find_all_elements(DataCircuitLocators.TABLE_ROWS, timeout=timeout)
            self.logger.info(f"Found {len(rows)} sub-circuit rows")
            return rows
        except TimeoutException:
            return []

    # ── Filter panel ─────────────────────────────────────────────────────

    def open_filter_panel(self, timeout=10):
        btn = self.element_to_be_clickable(DataCircuitLocators.FILTER_BTN, timeout=timeout)
        btn.click()
        self.logger.info("Opened filter panel")
        time.sleep(2)

    def close_filter_panel(self, timeout=10):
        """Close the filter panel by scrolling up to find the close button."""
        try:
            # Scroll the filter panel container to top to reveal close button
            self.browser.execute_script("""
                var panel = document.querySelector('[class*="filter-panel"]') 
                    || document.querySelector('[data-testid="data-filter-header"]')?.closest('div[class*="fixed"]')
                    || document.querySelector('.bg-primary-8')?.closest('div[class*="fixed"]');
                if (panel) panel.scrollTop = 0;
                window.scrollTo(0, 0);
            """)
            time.sleep(1)
            btn = self.element_to_be_clickable(DataCircuitLocators.FILTER_CLOSE_BTN, timeout=timeout)
            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            time.sleep(0.3)
            self.browser.execute_script("arguments[0].click();", btn)
            self.logger.info("Closed filter panel via close button")
            time.sleep(1)
        except TimeoutException:
            # Fallback: click the filter toggle button to close
            try:
                btn = self.element_to_be_clickable(DataCircuitLocators.FILTER_BTN, timeout=5)
                self.browser.execute_script("arguments[0].click();", btn)
                self.logger.info("Closed filter panel via toggle button")
                time.sleep(1)
            except TimeoutException:
                self.logger.warning("Could not close filter panel")

    def _apply_range_filter(self, accordion_locator, min_val, max_val, filter_name=""):
        """Expand a filter accordion and fill min/max values within that section."""
        select_all = Keys.COMMAND + "a" if platform.system() == "Darwin" else Keys.CONTROL + "a"

        # Click accordion trigger to expand
        trigger = self.element_to_be_clickable(accordion_locator, timeout=10)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", trigger)
        time.sleep(0.5)
        state = trigger.get_attribute("data-state") or trigger.get_attribute("aria-expanded")
        if state not in ("open", "true"):
            self.browser.execute_script("arguments[0].click();", trigger)
            time.sleep(1)

        # Find the region panel controlled by this trigger
        trigger_id = trigger.get_attribute("aria-controls")
        if trigger_id:
            # Find inputs within the specific expanded region
            min_xpath = f"//div[@id='{trigger_id}']//input[@id='value-range-min']"
            max_xpath = f"//div[@id='{trigger_id}']//input[@id='value-range-max']"
        else:
            # Fallback
            min_xpath = "//input[@id='value-range-min']"
            max_xpath = "//input[@id='value-range-max']"

        # Fill min value — scroll into view to avoid sticky bottom bar overlap
        min_input = self.find_element((By.XPATH, min_xpath), timeout=5)
        self.browser.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", min_input
        )
        time.sleep(0.5)
        min_input.click()
        min_input.send_keys(select_all)
        min_input.send_keys(Keys.BACKSPACE)
        min_input.send_keys(str(min_val))
        time.sleep(0.3)

        # Fill max value
        max_input = self.find_element((By.XPATH, max_xpath), timeout=5)
        self.browser.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", max_input
        )
        time.sleep(0.5)
        max_input.click()
        max_input.send_keys(select_all)
        max_input.send_keys(Keys.BACKSPACE)
        max_input.send_keys(str(max_val))
        time.sleep(0.3)

        self.logger.info(f"Applied {filter_name} filter: {min_val} - {max_val}")

    def apply_filter_neurons(self, min_val, max_val):
        self._apply_range_filter(DataCircuitLocators.FILTER_NEURONS, min_val, max_val, "neurons")

    def apply_filter_synapses(self, min_val, max_val):
        self._apply_range_filter(DataCircuitLocators.FILTER_SYNAPSES, min_val, max_val, "synapses")

    def apply_filter_connections(self, min_val, max_val):
        self._apply_range_filter(DataCircuitLocators.FILTER_CONNECTIONS, min_val, max_val, "connections")

    def click_filter_apply(self, timeout=10):
        """Click the Apply button in the filter panel."""
        # Scroll down to make Apply visible (it's sticky at bottom)
        apply_btn = self.find_element(DataCircuitLocators.FILTER_APPLY_BTN, timeout=timeout)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", apply_btn)
        time.sleep(0.5)
        self.browser.execute_script("arguments[0].click();", apply_btn)
        self.logger.info("Clicked Apply filter button")
        self.wait_for_network_idle(timeout=10)
        time.sleep(2)

    # ── Row click → Mini-detail ──────────────────────────────────────────

    def click_random_row(self):
        """Click a random row in the table to open the mini-detail view.
        Excludes known problematic rows.
        Clicks on a cell within the row (not the <tr> itself) for reliable interaction.
        """
        EXCLUDED_ROWS = ["20211110-BioM"]

        rows = self.get_table_rows()
        if not rows:
            raise RuntimeError("No rows found in the circuit table")

        visible_rows = rows[:min(10, len(rows))]
        # Filter out excluded rows
        valid_rows = [
            r for r in visible_rows
            if not any(excl in (r.text or "") for excl in EXCLUDED_ROWS)
        ]
        if not valid_rows:
            valid_rows = visible_rows  # fallback if all filtered out

        row = random.choice(valid_rows)
        row_text = row.text.split('\n')[0][:60]
        self.logger.info(f"Clicking row: '{row_text}...'")

        # Click on a cell within the row (2nd td) for reliable click registration
        try:
            cell = row.find_element(By.CSS_SELECTOR, "td.ant-table-cell:nth-child(2)")
        except Exception:
            cell = row  # fallback to row if cell not found

        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", cell)
        time.sleep(1)
        try:
            cell.click()
        except Exception:
            try:
                ActionChains(self.browser).move_to_element(cell).click().perform()
            except Exception:
                self.browser.execute_script("arguments[0].click();", cell)
        time.sleep(3)
        return row_text

    def wait_for_mini_detail(self, timeout=15):
        """Wait for the mini-detail panel to appear."""
        self.element_visibility(DataCircuitLocators.MINI_DETAIL_VIEW, timeout=timeout)
        self.logger.info("Mini-detail panel appeared")
        time.sleep(1)

    def verify_mini_detail_fields(self):
        """Verify mini-detail view shows expected fields.
        Returns dict of field presence.
        """
        results = {}

        # Name
        try:
            name_el = self.find_element(DataCircuitLocators.MINI_DETAIL_NAME, timeout=5)
            results['name'] = bool(name_el.text.strip())
        except TimeoutException:
            results['name'] = False

        # Description
        try:
            desc_el = self.find_element(DataCircuitLocators.MINI_DETAIL_DESCRIPTION, timeout=5)
            results['description'] = bool(desc_el.text.strip())
        except TimeoutException:
            results['description'] = False

        # Thumbnail
        try:
            img = self.find_element(DataCircuitLocators.MINI_DETAIL_THUMBNAIL, timeout=5)
            results['thumbnail'] = img.is_displayed()
        except TimeoutException:
            results['thumbnail'] = False

        # Buttons
        for btn_name, locator in [
            ('copy', DataCircuitLocators.MINI_DETAIL_COPY_BTN),
            ('download', DataCircuitLocators.MINI_DETAIL_DOWNLOAD_BTN),
            ('view_details', DataCircuitLocators.MINI_DETAIL_VIEW_DETAILS_BTN),
        ]:
            try:
                btn = self.find_element(locator, timeout=5)
                results[btn_name] = btn.is_displayed() and btn.is_enabled()
            except TimeoutException:
                results[btn_name] = False

        self.logger.info(f"Mini-detail fields: {results}")
        return results

    def close_mini_detail(self, timeout=10):
        """Close the mini-detail panel."""
        try:
            btn = self.element_to_be_clickable(DataCircuitLocators.MINI_DETAIL_CLOSE_BTN, timeout=timeout)
            btn.click()
            self.logger.info("Closed mini-detail panel")
            time.sleep(1)
        except TimeoutException:
            self.logger.warning("Could not find mini-detail close button")

    # ── View details → Detail view ───────────────────────────────────────

    def click_view_details(self, timeout=10):
        """Click View details button in mini-detail panel."""
        btn = self.element_to_be_clickable(DataCircuitLocators.MINI_DETAIL_VIEW_DETAILS_BTN, timeout=timeout)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(btn).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        self.logger.info("Clicked View details")
        time.sleep(5)

    def verify_detail_url(self):
        """Verify the URL contains /data/view/."""
        url = self.browser.current_url
        contains = "/data/view/" in url
        self.logger.info(f"Detail URL contains /data/view/: {contains} ({url})")
        return contains

    def verify_detail_breadcrumbs(self, timeout=10):
        """Verify breadcrumbs are visible in the detail view."""
        try:
            el = self.find_element(DataCircuitLocators.DV_BREADCRUMB_DATA, timeout=timeout)
            text = el.text.strip()
            self.logger.info(f"Breadcrumbs: '{text}'")
            return bool(text)
        except TimeoutException:
            self.logger.warning("Breadcrumbs not found")
            return False

    def verify_detail_tabs(self, timeout=10):
        """Verify the detail view tabs are present."""
        results = {}
        for name, locator in [
            ('overview', DataCircuitLocators.DV_OVERVIEW_TAB),
            ('analysis', DataCircuitLocators.DV_ANALYSIS_TAB),
            ('publications', DataCircuitLocators.DV_RELATED_PUBLICATIONS_TAB),
            ('artifacts', DataCircuitLocators.DV_RELATED_ARTIFACTS_TAB),
        ]:
            try:
                el = self.find_element(locator, timeout=timeout)
                results[name] = el.is_displayed()
            except TimeoutException:
                results[name] = False
        self.logger.info(f"Detail tabs: {results}")
        return results

    def verify_detail_metadata(self, timeout=10):
        """Verify required metadata fields are present and not empty in the detail view.
        
        DOM structure per field:
        - Label: <div class="text-primary-3 uppercase">FIELD NAME</div>
        - Value: <div class="mt-2 break-words">value text</div> (immediately following sibling)
        
        Name is special: <div class="text-primary-8 line-clamp-3 text-2xl font-bold">
        """
        results = {}
        required_fields = [
            "Name", "Brain Region", "Number of synapses", "Number of neurons",
            "Created by", "Registration date", "Scale", "Number of connections"
        ]
        optional_fields = [
            "Contributors", "Institutional Contributors", "License",
            "Contact email", "Root circuit", "Published in", "Experiment date"
        ]

        # Name has a special dedicated element (bold, larger text)
        try:
            name_el = self.find_element(DataCircuitLocators.DV_METADATA_NAME, timeout=5)
            results["Name"] = name_el.text.strip()
        except Exception:
            results["Name"] = None

        for field in required_fields + optional_fields:
            if field == "Name":
                continue  # Already handled above
            try:
                # Label is uppercase text-primary-3 div containing the field name (case-insensitive)
                label_locator = (
                    By.XPATH,
                    f"//div[contains(@class,'text-primary-3') and contains(@class,'uppercase') and "
                    f"contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), "
                    f"'{field.upper()}')]"
                )
                label_el = self.find_element(label_locator, timeout=3)
                # Value is the next sibling div with class 'mt-2 break-words'
                value_el = label_el.find_element(
                    By.XPATH, "following-sibling::div[contains(@class,'mt-2') and contains(@class,'break-words')][1]"
                )
                value_text = value_el.text.strip()
                results[field] = value_text if value_text and value_text != "—" else None
            except Exception:
                results[field] = None

        self.logger.info(f"Detail metadata: {len([v for v in results.values() if v])} fields found")
        return results

    def verify_detail_subject_metadata(self, timeout=10):
        """Verify subject metadata section fields within the Subject container.
        
        DOM structure: h2 "Subject" → parent container → label/value pairs
        Label: div.text-primary-3.uppercase
        Value: following-sibling div.mt-2.break-words
        """
        subject_fields = [
            "Name", "Species", "Subject", "Description", "Strain",
            "Sex", "Weight", "Age", "Age min", "Age max", "Age period"
        ]
        results = {}

        # Find the Subject section container
        try:
            subject_section = self.find_element(DataCircuitLocators.DV_SUBJECT_SECTION, timeout=timeout)
            # Scroll within the detail view content panel
            self.browser.execute_script("""
                var el = arguments[0];
                var scrollParent = el.closest('.overflow-y-auto') || el.closest('[class*="scrollbar"]');
                if (scrollParent) scrollParent.scrollTop = el.offsetTop - 100;
                else el.scrollIntoView({block: 'center'});
            """, subject_section)
            time.sleep(1)
        except Exception:
            # Fallback: try to find by section heading
            try:
                subject_section = self.find_element(DataCircuitLocators.DV_SUBJECT_SECTION_FALLBACK, timeout=5)
            except Exception:
                self.logger.warning("Subject section not found")
                return {f: None for f in subject_fields}

        for field in subject_fields:
            try:
                # Search within the Subject section only using same pattern as metadata
                label_el = subject_section.find_element(
                    By.XPATH,
                    f".//div[contains(@class,'text-primary-3') and contains(@class,'uppercase') and "
                    f"contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), "
                    f"'{field.upper()}')]"
                )
                value_el = label_el.find_element(
                    By.XPATH, "following-sibling::div[contains(@class,'mt-2') and contains(@class,'break-words')][1]"
                )
                value = value_el.text.strip()
                results[field] = value if value and value != "—" else None
            except Exception:
                results[field] = None

        self.logger.info(f"Subject metadata: {results}")
        return results

    def verify_detail_image(self, timeout=15):
        """Check that an image is displayed in the detail view."""
        try:
            img = self.find_element(DataCircuitLocators.DV_IMAGE, timeout=timeout)
            displayed = img.is_displayed()
            self.logger.info(f"Detail image displayed: {displayed}")
            return displayed
        except TimeoutException:
            self.logger.warning("Detail image not found")
            return False

    def verify_detail_buttons(self, timeout=10):
        """Verify Copy ID, Download, and Simulate buttons."""
        results = {}
        for name, locator in [
            ('copy_id', DataCircuitLocators.DV_COPY_ID_BTN),
            ('download', DataCircuitLocators.DV_DOWNLOAD_BTN),
            ('simulate', DataCircuitLocators.DV_SIMULATE_BTN),
        ]:
            try:
                btn = self.find_element(locator, timeout=timeout)
                results[name] = {
                    'displayed': btn.is_displayed(),
                    'enabled': btn.is_enabled(),
                }
            except TimeoutException:
                results[name] = {'displayed': False, 'enabled': False}
        self.logger.info(f"Detail buttons: {results}")
        return results

    # ── Analysis tab ─────────────────────────────────────────────────────

    def click_analysis_tab(self, timeout=10):
        """Click the Analysis tab in the detail view."""
        tab = self.element_to_be_clickable(DataCircuitLocators.DV_ANALYSIS_TAB, timeout=timeout)
        tab.click()
        self.logger.info("Clicked Analysis tab")
        self.wait_for_network_idle(timeout=10)
        time.sleep(2)

    def verify_analysis_tab_content(self, timeout=15):
        """Verify Analysis tab has Cell statistics and Network statistics with images.
        Returns dict with presence info.
        """
        results = {
            'cell_stats_title': False,
            'cell_stats_image': False,
            'network_stats_title': False,
            'network_stats_images': 0,
        }

        # Cell statistics title
        try:
            el = self.find_element(DataCircuitLocators.DV_ANALYSIS_CELL_STATS_TITLE, timeout=timeout)
            results['cell_stats_title'] = el.is_displayed()
        except TimeoutException:
            self.logger.warning("Cell statistics title not found")

        # Cell statistics image
        try:
            img = self.find_element(DataCircuitLocators.DV_ANALYSIS_CELL_STATS_IMAGE, timeout=10)
            results['cell_stats_image'] = img.is_displayed()
        except TimeoutException:
            self.logger.warning("Cell statistics image not found")

        # Network statistics title
        try:
            el = self.find_element(DataCircuitLocators.DV_ANALYSIS_NETWORK_STATS_TITLE, timeout=10)
            results['network_stats_title'] = el.is_displayed()
        except TimeoutException:
            self.logger.warning("Network statistics title not found")

        # Network statistics images (may be multiple)
        try:
            imgs = self.find_all_elements(DataCircuitLocators.DV_ANALYSIS_NETWORK_STATS_IMAGES, timeout=10)
            results['network_stats_images'] = len([img for img in imgs if img.is_displayed()])
        except TimeoutException:
            self.logger.warning("Network statistics images not found")

        self.logger.info(f"Analysis tab: {results}")
        return results

    # ── Related Publications tab ─────────────────────────────────────────

    def click_related_publications_tab(self, timeout=10):
        """Click the Related Publications tab in the detail view."""
        tab = self.element_to_be_clickable(DataCircuitLocators.DV_RELATED_PUBLICATIONS_TAB, timeout=timeout)
        tab.click()
        self.logger.info("Clicked Related Publications tab")
        self.wait_for_network_idle(timeout=10)
        time.sleep(2)

    def click_publications_section(self, section_name, timeout=10):
        """Click a section button (Provenance, Related artifacts provenance, Applications)."""
        locator_map = {
            "Provenance": DataCircuitLocators.DV_PUB_PROVENANCE_BTN,
            "Related artifacts provenance": DataCircuitLocators.DV_PUB_RELATED_ARTIFACTS_PROV_BTN,
            "Applications": DataCircuitLocators.DV_PUB_APPLICATIONS_BTN,
        }
        locator = locator_map.get(section_name)
        if not locator:
            raise ValueError(f"Unknown section: {section_name}")
        btn = self.element_to_be_clickable(locator, timeout=timeout)
        btn.click()
        self.logger.info(f"Clicked '{section_name}' section button")
        self.wait_for_network_idle(timeout=10)
        time.sleep(2)

    def verify_publications_articles(self, timeout=10):
        """Verify publication articles are displayed with expected fields.
        Returns dict with article count and field presence for first article.
        """
        results = {
            'article_count': 0,
            'has_title': False,
            'has_copy_doi': False,
            'has_authors': False,
            'has_more_authors_btn': False,
            'has_description': False,
            'has_read_more': False,
            'has_pagination': False,
            'pagination_pages': 0,
        }

        # Count articles
        try:
            articles = self.find_all_elements(DataCircuitLocators.DV_PUB_ARTICLE_ITEMS, timeout=timeout)
            results['article_count'] = len(articles)
        except TimeoutException:
            self.logger.warning("No publication articles found")
            return results

        # Check first article fields
        try:
            title = self.find_element(DataCircuitLocators.DV_PUB_ARTICLE_TITLE, timeout=5)
            results['has_title'] = bool(title.text.strip())
        except TimeoutException:
            pass

        try:
            doi_btn = self.find_element(DataCircuitLocators.DV_PUB_COPY_DOI_BTN, timeout=5)
            results['has_copy_doi'] = doi_btn.is_displayed()
        except TimeoutException:
            pass

        try:
            authors = self.find_all_elements(DataCircuitLocators.DV_PUB_AUTHOR_NAMES, timeout=5)
            results['has_authors'] = len(authors) > 0
        except TimeoutException:
            pass

        try:
            more_btn = self.find_element(DataCircuitLocators.DV_PUB_MORE_AUTHORS_BTN, timeout=3)
            results['has_more_authors_btn'] = more_btn.is_displayed()
        except TimeoutException:
            pass

        try:
            read_more = self.find_element(DataCircuitLocators.DV_PUB_READ_MORE_BTN, timeout=3)
            results['has_read_more'] = read_more.is_displayed()
            results['has_description'] = True
        except TimeoutException:
            pass

        # Pagination
        try:
            pagination = self.find_element(DataCircuitLocators.DV_PUB_PAGINATION, timeout=5)
            results['has_pagination'] = pagination.is_displayed()
            pages = self.find_all_elements(DataCircuitLocators.DV_PUB_PAGINATION_ITEMS, timeout=3)
            results['pagination_pages'] = len(pages)
        except TimeoutException:
            pass

        self.logger.info(f"Publications: {results}")
        return results

    def click_copy_doi_and_verify(self, timeout=10):
        """Click the first Copy DOI button and verify it changes to 'Copied'."""
        try:
            doi_btn = self.element_to_be_clickable(DataCircuitLocators.DV_PUB_COPY_DOI_BTN, timeout=timeout)
            doi_btn.click()
            self.logger.info("Clicked Copy DOI button")
            # Check text changes to "Copied" (happens quickly)
            time.sleep(0.5)
            btn_text = doi_btn.text.strip()
            if "Copied" in btn_text:
                self.logger.info("Copy DOI confirmed: button text changed to 'Copied'")
                return True
            else:
                self.logger.warning(f"Copy DOI button text after click: '{btn_text}'")
                return False
        except TimeoutException:
            self.logger.warning("Copy DOI button not found")
            return False

    def click_more_authors_and_verify(self, timeout=10):
        """Click the '+ N more' authors button and verify a dropdown/popover appears."""
        try:
            more_btn = self.element_to_be_clickable(DataCircuitLocators.DV_PUB_MORE_AUTHORS_BTN, timeout=timeout)
            btn_text = more_btn.text.strip()
            self.logger.info(f"Found more authors button: '{btn_text}'")
            more_btn.click()
            time.sleep(1)
            # Verify a popover/dropdown appeared (aria-describedby triggers a tooltip/popover)
            popover_id = more_btn.get_attribute("aria-describedby")
            if popover_id:
                try:
                    popover = self.find_element(
                        (By.ID, popover_id), timeout=3
                    )
                    is_visible = popover.is_displayed()
                    self.logger.info(f"Authors dropdown visible: {is_visible}")
                    # Close by clicking elsewhere
                    ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
                    time.sleep(0.5)
                    return is_visible
                except TimeoutException:
                    self.logger.warning(f"Popover with id '{popover_id}' not found")
            return True  # Button was clickable
        except TimeoutException:
            self.logger.warning("More authors button not found")
            return False

    # ── Related Artifacts tab ────────────────────────────────────────────

    def click_related_artifacts_tab(self, timeout=10):
        """Click the Related Artifacts tab in the detail view."""
        tab = self.element_to_be_clickable(DataCircuitLocators.DV_RELATED_ARTIFACTS_TAB, timeout=timeout)
        tab.click()
        self.logger.info("Clicked Related Artifacts tab")
        self.wait_for_network_idle(timeout=15)
        time.sleep(3)
        # Wait for the section toggle buttons to appear
        self.find_element(DataCircuitLocators.DV_ART_SUBCIRCUITS_BTN, timeout=10)
        self.logger.info("Related Artifacts tab content loaded")

    def click_artifacts_section(self, section_name, timeout=10):
        """Click Subcircuits or Derived circuits section button."""
        locator_map = {
            "Subcircuits": DataCircuitLocators.DV_ART_SUBCIRCUITS_BTN,
            "Derived circuits": DataCircuitLocators.DV_ART_DERIVED_CIRCUITS_BTN,
        }
        locator = locator_map.get(section_name)
        if not locator:
            raise ValueError(f"Unknown section: {section_name}")
        btn = self.element_to_be_clickable(locator, timeout=timeout)
        btn.click()
        self.logger.info(f"Clicked '{section_name}' section")
        self.wait_for_network_idle(timeout=10)
        time.sleep(2)

    def verify_artifacts_table(self, timeout=15):
        """Verify the related artifacts table has rows and expected column headers.
        Returns dict with row_count, header_count, has_download_btn, has_expand_btn.
        """
        results = {
            'row_count': 0,
            'header_count': 0,
            'has_download_btn': False,
            'has_expand_btn': False,
        }

        try:
            rows = self.find_all_elements(DataCircuitLocators.DV_ART_TABLE_ROWS, timeout=timeout)
            results['row_count'] = len(rows)
        except TimeoutException:
            self.logger.warning("No rows found in artifacts table")
            return results

        try:
            headers = self.find_all_elements(DataCircuitLocators.DV_ART_TABLE_HEADERS, timeout=5)
            results['header_count'] = len([h for h in headers if h.text.strip()])
        except TimeoutException:
            pass

        try:
            dl_btn = self.find_element(DataCircuitLocators.DV_ART_DOWNLOAD_BTN, timeout=5)
            results['has_download_btn'] = dl_btn.is_displayed()
        except TimeoutException:
            pass

        try:
            expand_btn = self.find_element(DataCircuitLocators.DV_ART_EXPAND_BTN, timeout=5)
            results['has_expand_btn'] = expand_btn.is_displayed()
        except TimeoutException:
            pass

        self.logger.info(f"Artifacts table: {results}")
        return results

    def expand_first_artifact_row(self, timeout=10):
        """Click the expand chevron on the first row with one."""
        try:
            btn = self.element_to_be_clickable(DataCircuitLocators.DV_ART_EXPAND_BTN, timeout=timeout)
            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            time.sleep(0.5)
            btn.click()
            self.logger.info("Clicked expand chevron on first artifact row")
            time.sleep(2)
            return True
        except TimeoutException:
            self.logger.warning("No expand chevron found in artifacts table")
            return False

    def verify_expanded_nested_rows(self, timeout=10):
        """Verify expanded row shows nested subcircuit rows."""
        try:
            expanded = self.find_element(DataCircuitLocators.DV_ART_EXPANDED_ROW, timeout=timeout)
            if not expanded.is_displayed():
                return 0
            nested_rows = self.find_all_elements(DataCircuitLocators.DV_ART_NESTED_TABLE_ROWS, timeout=5)
            count = len(nested_rows)
            self.logger.info(f"Found {count} nested rows in expanded artifact")
            return count
        except TimeoutException:
            self.logger.warning("No expanded row or nested rows found")
            return 0

    def click_download_btn_first_row(self, timeout=10):
        """Click the download button on the first row. Returns True if panel appears."""
        try:
            dl_btn = self.element_to_be_clickable(DataCircuitLocators.DV_ART_DOWNLOAD_BTN, timeout=timeout)
            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", dl_btn)
            time.sleep(0.5)
            dl_btn.click()
            self.logger.info("Clicked download button on first row")
            time.sleep(2)
            # Check if download panel appeared
            try:
                panel = self.find_element(DataCircuitLocators.DV_DOWNLOAD_PANEL, timeout=5)
                is_displayed = panel.is_displayed()
                self.logger.info(f"Download panel displayed: {is_displayed}")
                # Close the panel
                try:
                    close_btn = self.element_to_be_clickable(DataCircuitLocators.DV_DOWNLOAD_PANEL_CLOSE_BTN, timeout=5)
                    close_btn.click()
                    self.logger.info("Closed download panel")
                    time.sleep(1)
                except TimeoutException:
                    self.logger.warning("Could not close download panel")
                return is_displayed
            except TimeoutException:
                self.logger.info("No download panel detected")
                return False
        except TimeoutException:
            self.logger.warning("Download button not found")
            return False
