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
from locators.simulate_synaptome_locators import SimulateSynaptomeLocators as Loc


class SimulateSynaptomePage(HomePage):
    """Page object for the Synaptome simulation page (non-beta).

    Entry: Workflows → Simulate → Synaptome → model picker → config → run → results.
    """

    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, base_url)
        self.logger = logger

    # ── Navigation ───────────────────────────────────────────────────────

    def go_to_workflows_simulate(self, lab_id, project_id, retries=3, delay=5):
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
        el = self.element_to_be_clickable(Loc.SIMULATE_CATEGORY_CARD, timeout=15)
        el.click()
        self.logger.info("Clicked Simulate category")
        time.sleep(3)

    def click_synaptome_card(self):
        el = self.element_to_be_clickable(Loc.SYNAPTOME_CARD, timeout=15)
        el.click()
        self.logger.info("Clicked Synaptome card")
        time.sleep(5)

    # ── Model picker ─────────────────────────────────────────────────────

    def click_public_tab(self):
        el = self.find_element(Loc.PUBLIC_TAB, timeout=15)
        el.click()
        self.logger.info("Clicked Public tab")
        time.sleep(3)

    def get_table_rows(self, timeout=15):
        self.find_element(Loc.TABLE_ROWS, timeout=timeout)
        return self.browser.find_elements(*Loc.TABLE_ROWS)

    def get_row_count(self):
        rows = self.get_table_rows()
        self.logger.info(f"Table has {len(rows)} rows")
        return len(rows)

    def click_random_row(self, exclude_date="10.09.2025", exclude_creator="Gil Barrios"):
        rows = self.get_table_rows()
        if not rows:
            raise RuntimeError("No rows found in the table")

        headers = self.browser.find_elements(*Loc.COLUMN_HEADERS)
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

    # ── Filter panel ─────────────────────────────────────────────────────

    def open_filter_panel(self):
        btn = self.find_element(Loc.FILTER_BUTTON, timeout=10)
        btn.click()
        self.logger.info("Opened filter panel")
        time.sleep(2)

    def close_filter_panel(self):
        btn = self.find_element(Loc.FILTER_CLOSE_BUTTON, timeout=5)
        btn.click()
        self.logger.info("Closed filter panel")
        time.sleep(1)

    def click_random_filter_accordion(self):
        """Click a random filter accordion trigger to verify it's clickable."""
        triggers = self.browser.find_elements(*Loc.FILTER_ACCORDION_TRIGGERS)
        if not triggers:
            self.logger.warning("No filter accordion triggers found")
            return None
        trigger = random.choice(triggers)
        label = trigger.text.strip()
        trigger.click()
        self.logger.info(f"Clicked filter accordion: '{label}'")
        time.sleep(1)
        return label

    # ── Mini-detail view ─────────────────────────────────────────────────

    def wait_for_mini_detail(self, timeout=15):
        self.element_visibility(Loc.MINI_VIEWER, timeout=timeout)
        self.logger.info("Mini-detail view appeared")
        time.sleep(1)

    def verify_mini_detail_view(self):
        """Verify all expected elements in the mini-detail view.
        Returns dict of element_name -> present (bool).
        """
        checks = {
            'title': Loc.MINI_DETAIL_TITLE,
            'description': Loc.MINI_DETAIL_DESCRIPTION,
            'close_btn': Loc.MINI_DETAIL_CLOSE_BTN,
            'view_details_btn': Loc.MINI_DETAIL_VIEW_DETAILS_BTN,
            'use_model_btn': Loc.MINI_DETAIL_USE_MODEL_BTN,
        }
        results = {}
        for name, locator in checks.items():
            try:
                el = self.find_element(locator, timeout=10)
                results[name] = el.is_displayed()
                self.logger.info(f"Mini-detail '{name}': {results[name]}")
            except TimeoutException:
                results[name] = False
                self.logger.warning(f"Mini-detail '{name}' not found")

        # Check images (expect at least 2)
        try:
            imgs = self.find_all_elements(Loc.MINI_DETAIL_IMAGES, timeout=10)
            results['images_count'] = len(imgs)
            self.logger.info(f"Mini-detail images: {len(imgs)}")
        except TimeoutException:
            results['images_count'] = 0

        # Check metadata
        try:
            labels = self.find_all_elements(Loc.MINI_DETAIL_METADATA_LABELS, timeout=10)
            results['metadata_count'] = len(labels)
            self.logger.info(f"Mini-detail metadata labels: {len(labels)}")
        except TimeoutException:
            results['metadata_count'] = 0

        return results

    def click_use_model(self):
        btn = self.find_element(Loc.MINI_DETAIL_USE_MODEL_BTN, timeout=10)
        self.logger.info(f"Clicking 'Use model', href: {btn.get_attribute('href')}")
        try:
            btn.click()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        time.sleep(5)

    # ── Config page ──────────────────────────────────────────────────────

    def wait_for_config_page(self, timeout=30):
        self.find_element(Loc.CONFIG_LAYOUT, timeout=timeout)
        self.logger.info("Config page layout loaded")
        time.sleep(2)

    def wait_for_neuron_visualizer(self, timeout=120):
        self.wait_for_long_load(Loc.NEURON_VISUALIZER_CANVAS, timeout=timeout)
        self.logger.info("Neuron visualizer canvas loaded")
        time.sleep(2)

    def verify_config_tabs(self):
        results = {}
        for name, locator in [
            ('configuration', Loc.CONFIG_TAB_CONFIGURATION),
            ('results', Loc.CONFIG_TAB_RESULTS),
        ]:
            try:
                el = self.find_element(locator, timeout=10)
                results[name] = {'present': True, 'displayed': el.is_displayed()}
            except TimeoutException:
                results[name] = {'present': False, 'displayed': False}
        return results

    # ── Left menu ────────────────────────────────────────────────────────

    def _click_menu(self, locator, label):
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
        self._click_menu(Loc.LEFT_MENU_INFO_BTN, "Info")

    def click_experimental_setup_tab(self):
        self._click_menu(Loc.LEFT_MENU_EXPERIMENTAL_SETUP_BTN, "Experimental setup")

    def click_synaptic_input_tab(self):
        self._click_menu(Loc.LEFT_MENU_SYNAPTIC_INPUT_BTN, "Synaptic input")

    def click_stimulation_protocol_tab(self):
        self._click_menu(Loc.LEFT_MENU_STIMULATION_PROTOCOL_BTN, "Stimulation protocol")

    def click_recording_tab(self):
        self._click_menu(Loc.LEFT_MENU_RECORDING_BTN, "Recording")

    # ── Info form ────────────────────────────────────────────────────────

    def fill_name(self, name):
        inp = self.find_element(Loc.FORM_NAME_INPUT, timeout=10)
        inp.click()
        inp.send_keys(Keys.COMMAND + "a")
        inp.send_keys(Keys.BACKSPACE)
        inp.send_keys(name)
        self.logger.info(f"Filled name: '{name}'")

    def fill_description(self, desc):
        inp = self.find_element(Loc.FORM_DESCRIPTION_INPUT, timeout=10)
        inp.click()
        inp.send_keys(Keys.COMMAND + "a")
        inp.send_keys(Keys.BACKSPACE)
        inp.send_keys(desc)
        self.logger.info(f"Filled description: '{desc}'")

    def fill_name_with_datetime(self):
        name = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.fill_name(name)
        return name

    def get_registered_by(self):
        try:
            return self.find_element(Loc.FORM_REGISTERED_BY, timeout=5).text.strip()
        except TimeoutException:
            return ""

    def get_registered_at(self):
        try:
            return self.find_element(Loc.FORM_REGISTERED_AT, timeout=5).text.strip()
        except TimeoutException:
            return ""

    # ── Experimental setup ───────────────────────────────────────────────

    def get_panel_labels(self):
        """Read all label spans visible in the simulation panel."""
        time.sleep(2)
        try:
            panel = self.find_element(Loc.SIMULATION_PANEL, timeout=10)
            labels = panel.find_elements(By.CSS_SELECTOR, "span.text-label")
        except TimeoutException:
            labels = self.browser.find_elements(By.CSS_SELECTOR, "span.text-label")
        result = [l.text.strip() for l in labels if l.text.strip()]
        self.logger.info(f"Panel labels ({len(result)}): {result}")
        return result

    # ── Synaptic input ───────────────────────────────────────────────────

    def get_synaptic_input_count(self):
        try:
            entries = self.browser.find_elements(*Loc.SYNAPTIC_INPUT_ENTRIES)
            visible = [e for e in entries if e.is_displayed()]
            self.logger.info(f"Synaptic input entries: {len(visible)}")
            return len(visible)
        except Exception:
            return 0

    def click_eye_button(self, index=0):
        """Click the eye toggle button on a synaptic input entry."""
        btns = self.browser.find_elements(*Loc.SYNAPTIC_INPUT_EYE_BTN)
        if index >= len(btns):
            self.logger.warning(f"Eye button index {index} out of range ({len(btns)})")
            return
        btn = btns[index]
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(btn).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        self.logger.info(f"Clicked eye toggle button [{index}]")
        time.sleep(2)

    def is_eye_crossed_out(self):
        try:
            self.find_element(Loc.SYNAPTIC_INPUT_EYE_CROSSED, timeout=5)
            self.logger.info("Eye button is crossed out (eye-invisible)")
            return True
        except TimeoutException:
            self.logger.info("Eye button is NOT crossed out")
            return False

    # ── Stimulation protocol ─────────────────────────────────────────────

    def wait_for_stim_plot(self, timeout=60):
        self.wait_for_long_load(Loc.STIM_PLOT_IMAGE, timeout=timeout)
        self.logger.info("Stimulation protocol plot loaded")
        time.sleep(2)

    def is_stim_download_btn_clickable(self, timeout=10):
        try:
            btn = self.element_to_be_clickable(Loc.STIM_DOWNLOAD_BTN, timeout=timeout)
            return btn.is_displayed() and btn.is_enabled()
        except TimeoutException:
            return False

    # ── Recording ────────────────────────────────────────────────────────

    def click_add_recording(self):
        btn = self.element_to_be_clickable(Loc.RECORDING_ADD_BTN, timeout=10)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(btn).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        self.logger.info("Clicked 'Add' recording")
        time.sleep(2)

    def get_recording_dropdowns(self):
        try:
            return self.browser.find_elements(*Loc.RECORDING_SECTION_DROPDOWN)
        except Exception:
            return []

    def select_recording_section(self, dropdown_index, section_prefix):
        dropdowns = self.get_recording_dropdowns()
        if dropdown_index >= len(dropdowns):
            self.logger.warning(f"Dropdown {dropdown_index} out of range ({len(dropdowns)})")
            return None
        dd = dropdowns[dropdown_index]
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", dd)
        time.sleep(0.5)
        dd.click()
        time.sleep(1)
        options = self.browser.find_elements(*Loc.RECORDING_DROPDOWN_OPTIONS)
        for opt in options:
            title = opt.get_attribute("title") or opt.text.strip()
            if title.startswith(section_prefix):
                try:
                    self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", opt)
                    time.sleep(0.3)
                    self.browser.execute_script("arguments[0].click();", opt)
                except Exception:
                    opt.click()
                self.logger.info(f"Selected recording: '{title}'")
                time.sleep(1)
                return title
        try:
            ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
        except Exception:
            pass
        self.logger.warning(f"No option starting with '{section_prefix}'")
        return None

    def get_available_section_prefixes(self, dropdown_index=0):
        dropdowns = self.get_recording_dropdowns()
        if dropdown_index >= len(dropdowns):
            return []
        dd = dropdowns[dropdown_index]
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", dd)
        time.sleep(0.5)
        dd.click()
        time.sleep(1)
        options = self.browser.find_elements(*Loc.RECORDING_DROPDOWN_OPTIONS)
        prefixes = set()
        for opt in options:
            title = opt.get_attribute("title") or opt.text.strip()
            prefixes.add(title.split('[')[0] if '[' in title else title)
        try:
            ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
        except Exception:
            pass
        self.logger.info(f"Available section prefixes: {sorted(prefixes)}")
        return sorted(prefixes)

    # ── Run experiment ───────────────────────────────────────────────────

    def find_run_experiment_btn(self, timeout=10):
        return self.find_element(Loc.RUN_EXPERIMENT_BTN, timeout=timeout)

    def click_run_experiment(self):
        btn = self.element_to_be_clickable(Loc.RUN_EXPERIMENT_BTN, timeout=10)
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
        tab = self.element_to_be_clickable(Loc.CONFIG_TAB_RESULTS, timeout=10)
        tab.click()
        self.logger.info("Clicked Results tab")
        time.sleep(3)

    def is_results_tab_active(self):
        try:
            tab = self.find_element(Loc.CONFIG_TAB_RESULTS, timeout=5)
            return tab.get_attribute("data-state") == "active"
        except TimeoutException:
            return False

    def get_results_left_menu_buttons(self):
        try:
            btns = self.find_all_elements(Loc.RESULTS_LEFT_MENU_BUTTONS, timeout=10)
            labels = [b.text.strip().split('\n')[0] for b in btns]
            self.logger.info(f"Results menu ({len(btns)}): {labels}")
            return btns
        except TimeoutException:
            return []

    def get_results_recording_buttons(self):
        try:
            btns = self.find_all_elements(Loc.RESULTS_RECORDING_BTNS, timeout=10)
            self.logger.info(f"Recording buttons: {len(btns)}")
            return btns
        except TimeoutException:
            return []

    def is_download_csv_enabled(self):
        try:
            btn = self.find_element(Loc.RESULTS_DOWNLOAD_CSV_BTN, timeout=5)
            return btn.is_enabled() and btn.get_attribute("disabled") is None
        except TimeoutException:
            return False

    def is_reconfigure_enabled(self):
        try:
            btn = self.find_element(Loc.RESULTS_RECONFIGURE_BTN, timeout=5)
            parent = btn.find_element(By.XPATH, "./ancestor::div[@data-slot='popover-trigger']")
            return btn.get_attribute("disabled") is None and parent.get_attribute("disabled") is None
        except Exception:
            return False

    def get_idrest_plot_count(self):
        try:
            plots = self.browser.find_elements(*Loc.RESULTS_IDREST_PLOTS)
            return len([p for p in plots if p.is_displayed()])
        except Exception:
            return 0

    def is_neuron_canvas_visible(self):
        try:
            canvas = self.find_element(Loc.RESULTS_NEURON_CANVAS, timeout=10)
            return canvas.is_displayed()
        except TimeoutException:
            return False

    def wait_for_simulation_complete(self, timeout=300, poll_interval=10):
        import time as _time
        start = _time.time()
        while _time.time() - start < timeout:
            if self.is_download_csv_enabled():
                elapsed = int(_time.time() - start)
                self.logger.info(f"Simulation completed after {elapsed}s")
                return True
            elapsed = int(_time.time() - start)
            self.logger.info(f"Simulation running after {elapsed}s...")
            _time.sleep(poll_interval)
        self.logger.warning(f"Simulation did not complete within {timeout}s")
        return False

    def wait_for_success_notification(self, timeout=30):
        try:
            self.element_visibility(Loc.RESULTS_SUCCESS_NOTIFICATION, timeout=timeout)
            self.logger.info("Success notification appeared")
            return True
        except TimeoutException:
            return False

    def get_view_simulation_link(self, timeout=10):
        try:
            link = self.find_element(Loc.RESULTS_VIEW_SIMULATION_LINK, timeout=timeout)
            self.logger.info(f"View Simulation link: {link.get_attribute('href')}")
            return link
        except TimeoutException:
            return None
