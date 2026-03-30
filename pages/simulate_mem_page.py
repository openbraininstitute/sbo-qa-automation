# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import random
from datetime import datetime
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pages.home_page import HomePage
from locators.simulate_mem_locators import SimulateMemLocators


class SimulateMemPage(HomePage):
    """Page object for the ME-model simulation page (non-beta single neuron).

    Entry: Workflows → Simulate → Single neuron → model picker → config → run experiment → results.
    """

    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, base_url)
        self.logger = logger

    # ── Navigation ───────────────────────────────────────────────────────

    def go_to_workflows_simulate(self, lab_id, project_id, retries=3, delay=5):
        """Navigate to the Workflows page with simulate activity filter."""
        path = f"/app/virtual-lab/{lab_id}/{project_id}/workflows?activity=simulate"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(90)
                self.go_to_page(path)
                self.wait_for_page_ready(timeout=60)
                self.logger.info(f"Navigated to workflows simulate: {self.browser.current_url}")
                return
            except TimeoutException:
                self.logger.warning(f"Attempt {attempt + 1} failed. Retrying in {delay}s...")
                time.sleep(delay)
                if attempt == retries - 1:
                    raise RuntimeError("Workflows simulate page did not load")

    def wait_for_page_ready(self, timeout=30):
        super().wait_for_page_ready(timeout=timeout)
        time.sleep(2)

    def click_simulate_category(self):
        el = self.element_to_be_clickable(SimulateMemLocators.SIMULATE_CATEGORY_CARD, timeout=15)
        el.click()
        self.logger.info("Clicked Simulate category")
        time.sleep(3)

    def click_single_neuron_card(self):
        el = self.element_to_be_clickable(SimulateMemLocators.SINGLE_NEURON_CARD, timeout=15)
        el.click()
        self.logger.info("Clicked Single neuron card")
        time.sleep(5)

    # ── Model picker ─────────────────────────────────────────────────────

    def click_public_tab(self):
        el = self.find_element(SimulateMemLocators.PUBLIC_TAB, timeout=15)
        el.click()
        self.logger.info("Clicked Public tab")
        time.sleep(3)

    def get_table_rows(self, timeout=15):
        self.find_element(SimulateMemLocators.TABLE_ROWS, timeout=timeout)
        return self.browser.find_elements(*SimulateMemLocators.TABLE_ROWS)

    def get_row_count(self):
        rows = self.get_table_rows()
        self.logger.info(f"Table has {len(rows)} rows")
        return len(rows)

    def click_random_row(self, exclude_date="10.09.2025", exclude_creator="Gil Barrios"):
        """Click a random row, skipping rows matching excluded date+creator."""
        rows = self.get_table_rows()
        if not rows:
            raise RuntimeError("No rows found in the table")

        headers = self.browser.find_elements(*SimulateMemLocators.COLUMN_HEADERS)
        creator_idx = date_idx = None
        for i, h in enumerate(headers):
            text = h.text.strip()
            if 'Created by' in text:
                creator_idx = i
            if 'Registration date' in text:
                date_idx = i

        visible_rows = rows[:min(10, len(rows))]
        eligible = []
        for row in visible_rows:
            cells = row.find_elements("tag name", "td")
            skip = False
            if creator_idx is not None and date_idx is not None and len(cells) > max(creator_idx, date_idx):
                creator = cells[creator_idx].text.strip()
                reg_date = cells[date_idx].text.strip()
                if exclude_creator in creator and exclude_date in reg_date:
                    self.logger.info(f"Skipping row: creator='{creator}', date='{reg_date}'")
                    skip = True
            if not skip:
                eligible.append(row)

        if not eligible:
            self.logger.warning("No eligible rows after filtering, using all visible")
            eligible = visible_rows

        row = random.choice(eligible)
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

    # ── Mini-detail view ─────────────────────────────────────────────────

    def wait_for_mini_detail(self, timeout=15):
        self.element_visibility(SimulateMemLocators.MINI_VIEWER, timeout=timeout)
        self.logger.info("Mini-detail view appeared")
        time.sleep(1)

    def find_mini_detail_title(self, timeout=10):
        return self.find_element(SimulateMemLocators.MINI_DETAIL_TITLE, timeout=timeout)

    def click_use_model(self):
        btn = self.find_element(SimulateMemLocators.MINI_DETAIL_USE_MODEL_BTN, timeout=10)
        self.logger.info(f"Clicking 'Use model', href: {btn.get_attribute('href')}")
        try:
            btn.click()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        time.sleep(5)

    # ── Config page ──────────────────────────────────────────────────────

    def wait_for_config_page(self, timeout=30):
        self.find_element(SimulateMemLocators.CONFIG_LAYOUT, timeout=timeout)
        self.logger.info("Config page layout loaded")
        time.sleep(2)

    def wait_for_neuron_visualizer(self, timeout=60):
        self.wait_for_long_load(SimulateMemLocators.NEURON_VISUALIZER_CANVAS, timeout=timeout)
        self.logger.info("Neuron visualizer canvas loaded")
        time.sleep(2)

    def verify_config_tabs(self):
        results = {}
        for name, locator in [
            ('configuration', SimulateMemLocators.CONFIG_TAB_CONFIGURATION),
            ('results', SimulateMemLocators.CONFIG_TAB_RESULTS),
        ]:
            try:
                el = self.find_element(locator, timeout=10)
                results[name] = {'present': True, 'displayed': el.is_displayed()}
            except TimeoutException:
                results[name] = {'present': False, 'displayed': False}
        return results

    # ── Left menu navigation ─────────────────────────────────────────────

    def _click_left_menu_btn(self, locator, label):
        btn = self.element_to_be_clickable(locator, timeout=10)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(btn).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        self.logger.info(f"Clicked '{label}' menu button")
        time.sleep(2)

    def click_info_tab(self):
        self._click_left_menu_btn(SimulateMemLocators.LEFT_MENU_INFO_BTN, "Info")

    def click_experimental_setup_tab(self):
        self._click_left_menu_btn(SimulateMemLocators.LEFT_MENU_EXPERIMENTAL_SETUP_BTN, "Experimental setup")

    def click_stimulation_protocol_tab(self):
        self._click_left_menu_btn(SimulateMemLocators.LEFT_MENU_STIMULATION_PROTOCOL_BTN, "Stimulation protocol")

    def click_recording_tab(self):
        self._click_left_menu_btn(SimulateMemLocators.LEFT_MENU_RECORDING_BTN, "Recording")

    def get_active_menu_label(self):
        try:
            btn = self.find_element(SimulateMemLocators.LEFT_MENU_ACTIVE_BTN, timeout=5)
            return btn.text.strip()
        except TimeoutException:
            return ""

    # ── Info form ────────────────────────────────────────────────────────

    def fill_name(self, name):
        inp = self.find_element(SimulateMemLocators.FORM_NAME_INPUT, timeout=10)
        inp.click()
        inp.send_keys(Keys.COMMAND + "a")
        inp.send_keys(Keys.BACKSPACE)
        inp.send_keys(name)
        self.logger.info(f"Filled name: '{name}'")

    def fill_description(self, description):
        inp = self.find_element(SimulateMemLocators.FORM_DESCRIPTION_INPUT, timeout=10)
        inp.click()
        inp.send_keys(Keys.COMMAND + "a")
        inp.send_keys(Keys.BACKSPACE)
        inp.send_keys(description)
        self.logger.info(f"Filled description: '{description}'")

    def fill_name_with_datetime(self):
        name = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.fill_name(name)
        return name

    def get_registered_by(self):
        try:
            el = self.find_element(SimulateMemLocators.FORM_REGISTERED_BY, timeout=5)
            return el.text.strip()
        except TimeoutException:
            return ""

    def get_registered_at(self):
        try:
            el = self.find_element(SimulateMemLocators.FORM_REGISTERED_AT, timeout=5)
            return el.text.strip()
        except TimeoutException:
            return ""

    # ── Experimental setup tab ───────────────────────────────────────────

    def get_panel_labels_and_values(self):
        """Read all label/value pairs visible in the simulation panel.
        Returns list of dicts: [{'label': str, 'value': str}].
        """
        panel = self.find_element(SimulateMemLocators.SIMULATION_PANEL, timeout=10)
        results = []
        # Look for label spans (uppercase) followed by value divs
        labels = panel.find_elements(By.CSS_SELECTOR, "span.text-label")
        for lbl in labels:
            label_text = lbl.text.strip()
            try:
                parent = lbl.find_element(By.XPATH, "./ancestor::div[1]")
                sibling = parent.find_element(By.XPATH, "following-sibling::div[1]")
                value_text = sibling.text.strip()
            except Exception:
                value_text = ""
            if label_text:
                results.append({'label': label_text, 'value': value_text})
        self.logger.info(f"Panel labels ({len(results)}): {[r['label'] for r in results]}")
        return results

    # ── Stimulation protocol tab ─────────────────────────────────────────

    def wait_for_stim_plot(self, timeout=60):
        """Wait for the IDrest plot to appear under Stimulation protocol."""
        self.wait_for_long_load(SimulateMemLocators.STIM_PLOT_IMAGE, timeout=timeout)
        self.logger.info("Stimulation protocol plot loaded")
        time.sleep(2)

    def find_stim_download_btn(self, timeout=10):
        return self.find_element(SimulateMemLocators.STIM_DOWNLOAD_BTN, timeout=timeout)

    def is_stim_download_btn_clickable(self, timeout=10):
        try:
            btn = self.element_to_be_clickable(SimulateMemLocators.STIM_DOWNLOAD_BTN, timeout=timeout)
            return btn.is_displayed() and btn.is_enabled()
        except TimeoutException:
            return False

    # ── Recording tab ────────────────────────────────────────────────────

    def click_add_recording(self):
        btn = self.element_to_be_clickable(SimulateMemLocators.RECORDING_ADD_BTN, timeout=10)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(btn).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        self.logger.info("Clicked 'Add' recording button")
        time.sleep(2)

    def get_recording_dropdowns(self):
        """Get all section dropdown elements in the recording panel."""
        try:
            dropdowns = self.browser.find_elements(*SimulateMemLocators.RECORDING_SECTION_DROPDOWN)
            self.logger.info(f"Found {len(dropdowns)} recording dropdown(s)")
            return dropdowns
        except Exception:
            return []

    def select_recording_section(self, dropdown_index, section_prefix):
        """Open a recording dropdown and select the first option matching the prefix.
        e.g. section_prefix='soma' selects 'soma[0]', 'dend' selects 'dend[0]', etc.
        Returns the selected option text or None.
        """
        dropdowns = self.get_recording_dropdowns()
        if dropdown_index >= len(dropdowns):
            self.logger.warning(f"Dropdown index {dropdown_index} out of range ({len(dropdowns)})")
            return None

        dd = dropdowns[dropdown_index]
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", dd)
        time.sleep(0.5)
        dd.click()
        self.logger.info(f"Opened recording dropdown [{dropdown_index}]")
        time.sleep(1)

        # Find matching option
        options = self.browser.find_elements(*SimulateMemLocators.RECORDING_DROPDOWN_OPTIONS)
        for opt in options:
            title = opt.get_attribute("title") or opt.text.strip()
            if title.startswith(section_prefix):
                opt.click()
                self.logger.info(f"Selected recording section: '{title}'")
                time.sleep(1)
                return title

        # Dismiss dropdown if no match
        try:
            ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
        except Exception:
            pass
        self.logger.warning(f"No option starting with '{section_prefix}' found")
        return None

    def get_available_section_prefixes(self, dropdown_index=0):
        """Open a dropdown and return the unique section prefixes available (soma, dend, apic, myelin)."""
        dropdowns = self.get_recording_dropdowns()
        if dropdown_index >= len(dropdowns):
            return []

        dd = dropdowns[dropdown_index]
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", dd)
        time.sleep(0.5)
        dd.click()
        time.sleep(1)

        options = self.browser.find_elements(*SimulateMemLocators.RECORDING_DROPDOWN_OPTIONS)
        prefixes = set()
        for opt in options:
            title = opt.get_attribute("title") or opt.text.strip()
            prefix = title.split('[')[0] if '[' in title else title
            prefixes.add(prefix)

        # Dismiss
        try:
            ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
        except Exception:
            pass
        time.sleep(0.5)

        self.logger.info(f"Available section prefixes: {sorted(prefixes)}")
        return sorted(prefixes)

    # ── Run experiment ───────────────────────────────────────────────────

    def find_run_experiment_btn(self, timeout=10):
        return self.find_element(SimulateMemLocators.RUN_EXPERIMENT_BTN, timeout=timeout)

    def click_run_experiment(self):
        btn = self.element_to_be_clickable(SimulateMemLocators.RUN_EXPERIMENT_BTN, timeout=10)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(btn).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        self.logger.info("Clicked 'Run experiment'")
        time.sleep(3)

    # ── Results tab ──────────────────────────────────────────────────────

    def click_results_tab(self):
        tab = self.element_to_be_clickable(SimulateMemLocators.CONFIG_TAB_RESULTS, timeout=10)
        tab.click()
        self.logger.info("Clicked Results tab")
        time.sleep(3)

    def is_results_tab_active(self):
        try:
            tab = self.find_element(SimulateMemLocators.CONFIG_TAB_RESULTS, timeout=5)
            return tab.get_attribute("data-state") == "active"
        except TimeoutException:
            return False

    def wait_for_build_done(self, timeout=180, poll_interval=10):
        """Poll build card status until 'done' badge appears."""
        import time as _time
        start = _time.time()
        while _time.time() - start < timeout:
            try:
                cards = self.browser.find_elements(*SimulateMemLocators.RESULTS_BUILD_CARDS)
                for card in cards:
                    try:
                        badge = card.find_element(*SimulateMemLocators.RESULTS_STATUS_BADGE)
                        status = badge.text.strip().lower()
                        elapsed = int(_time.time() - start)
                        self.logger.info(f"Build status after {elapsed}s: '{status}'")
                        if status == 'done':
                            return True
                    except Exception:
                        pass
            except Exception:
                pass
            _time.sleep(poll_interval)

        self.logger.warning(f"Build did not complete within {timeout}s")
        return False

    def verify_output_files(self):
        """Verify MOD and PDF output files are present.
        Returns dict: {'mod': bool, 'pdf_count': int, 'outputs_section': bool}.
        """
        results = {'mod': False, 'pdf_count': 0, 'outputs_section': False}

        try:
            self.find_element(SimulateMemLocators.RESULTS_OUTPUT_SECTION, timeout=10)
            results['outputs_section'] = True
        except TimeoutException:
            pass

        try:
            mod_btn = self.find_element(SimulateMemLocators.RESULTS_OUTPUT_MOD_BTN, timeout=5)
            results['mod'] = mod_btn.is_displayed()
        except TimeoutException:
            pass

        try:
            pdf_btns = self.browser.find_elements(*SimulateMemLocators.RESULTS_OUTPUT_PDF_BTNS)
            results['pdf_count'] = len([b for b in pdf_btns if b.is_displayed()])
        except Exception:
            pass

        self.logger.info(f"Output files — MOD: {results['mod']}, PDFs: {results['pdf_count']}")
        return results

    def click_mod_and_verify_preview(self, timeout=10):
        """Click MOD output file and verify code preview shows NEURON content."""
        mod_btn = self.find_element(SimulateMemLocators.RESULTS_OUTPUT_MOD_BTN, timeout=10)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", mod_btn)
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(mod_btn).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", mod_btn)
        self.logger.info("Clicked MOD output file")
        time.sleep(2)

        try:
            code_el = self.element_visibility(SimulateMemLocators.RESULTS_CODE_PREVIEW, timeout=timeout)
            text = code_el.text.strip()
            has_content = len(text) > 0 and 'NEURON' in text
            self.logger.info(f"MOD preview: {len(text)} chars, has NEURON: {has_content}")
            return has_content
        except TimeoutException:
            self.logger.warning("Code preview not found")
            return False

    # ── Results tab: after Run experiment ─────────────────────────────────

    def get_results_left_menu_buttons(self):
        """Get all left menu buttons on the Results tab (All + recording entries)."""
        try:
            buttons = self.find_all_elements(SimulateMemLocators.RESULTS_LEFT_MENU_BUTTONS, timeout=10)
            labels = [b.text.strip().split('\n')[0] for b in buttons]
            self.logger.info(f"Results left menu buttons ({len(buttons)}): {labels}")
            return buttons
        except TimeoutException:
            return []

    def get_results_recording_buttons(self):
        """Get recording-specific buttons (e.g. soma[0]_0.5, dend[4]_0.5)."""
        try:
            buttons = self.find_all_elements(SimulateMemLocators.RESULTS_RECORDING_BTNS, timeout=10)
            labels = [b.text.strip().split('\n')[0] for b in buttons]
            self.logger.info(f"Recording buttons ({len(buttons)}): {labels}")
            return buttons
        except TimeoutException:
            return []

    def is_download_csv_enabled(self):
        try:
            btn = self.find_element(SimulateMemLocators.RESULTS_DOWNLOAD_CSV_BTN, timeout=5)
            enabled = btn.is_enabled() and btn.get_attribute("disabled") is None
            self.logger.info(f"Download CSV enabled: {enabled}")
            return enabled
        except TimeoutException:
            return False

    def is_reconfigure_enabled(self):
        try:
            btn = self.find_element(SimulateMemLocators.RESULTS_RECONFIGURE_BTN, timeout=5)
            # Reconfigure is inside a popover trigger div that can also be disabled
            parent = btn.find_element(By.XPATH, "./ancestor::div[@data-slot='popover-trigger']")
            parent_disabled = parent.get_attribute("disabled")
            btn_disabled = btn.get_attribute("disabled")
            enabled = btn_disabled is None and parent_disabled is None
            self.logger.info(f"Reconfigure enabled: {enabled}")
            return enabled
        except Exception:
            return False

    def get_idrest_plot_count(self):
        """Count the number of IDREST plotly plots visible."""
        try:
            plots = self.browser.find_elements(*SimulateMemLocators.RESULTS_IDREST_PLOTS)
            visible = [p for p in plots if p.is_displayed()]
            self.logger.info(f"IDREST plots visible: {len(visible)}")
            return len(visible)
        except Exception:
            return 0

    def get_plot_container_labels(self):
        """Get the recording labels from plot containers (e.g. soma[0]_0.5, dend[4]_0.5)."""
        try:
            containers = self.browser.find_elements(*SimulateMemLocators.RESULTS_PLOT_CONTAINERS)
            labels = []
            for c in containers:
                test_id = c.get_attribute("data-testid") or ""
                # data-testid="root-container-soma[0]_0.5"
                label = test_id.replace("root-container-", "")
                if label:
                    labels.append(label)
            self.logger.info(f"Plot container labels: {labels}")
            return labels
        except Exception:
            return []

    def is_neuron_canvas_visible(self):
        try:
            canvas = self.find_element(SimulateMemLocators.RESULTS_NEURON_CANVAS, timeout=10)
            visible = canvas.is_displayed()
            self.logger.info(f"Neuron canvas visible: {visible}")
            return visible
        except TimeoutException:
            return False

    def wait_for_simulation_complete(self, timeout=300, poll_interval=10):
        """Poll until Download CSV button becomes enabled (simulation finished)."""
        import time as _time
        start = _time.time()

        while _time.time() - start < timeout:
            if self.is_download_csv_enabled():
                elapsed = int(_time.time() - start)
                self.logger.info(f"Simulation completed after {elapsed}s (Download CSV enabled)")
                return True

            elapsed = int(_time.time() - start)
            self.logger.info(f"Simulation still running after {elapsed}s...")
            _time.sleep(poll_interval)

        self.logger.warning(f"Simulation did not complete within {timeout}s")
        return False

    def wait_for_success_notification(self, timeout=30):
        """Wait for the success notification toast to appear."""
        try:
            self.element_visibility(SimulateMemLocators.RESULTS_SUCCESS_NOTIFICATION, timeout=timeout)
            self.logger.info("Success notification appeared")
            return True
        except TimeoutException:
            self.logger.warning("Success notification not found")
            return False

    def get_view_simulation_link(self, timeout=10):
        """Get the 'View Simulation' link from the success notification."""
        try:
            link = self.find_element(SimulateMemLocators.RESULTS_VIEW_SIMULATION_LINK, timeout=timeout)
            href = link.get_attribute("href")
            self.logger.info(f"View Simulation link: {href}")
            return link
        except TimeoutException:
            return None
