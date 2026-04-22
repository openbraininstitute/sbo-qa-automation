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
from locators.simulate_small_microcircuit_locators import SimulateSmallMicrocircuitLocators as Loc


class SimulateSmallMicrocircuitPage(HomePage):
    """Page object for the Small microcircuit (beta) simulation page.

    Entry: Workflows → Simulate → Small microcircuit → model picker → config → run → results.
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
        el = self.element_to_be_clickable(Loc.SIMULATE_CATEGORY_CARD, timeout=15)
        el.click()
        self.logger.info("Clicked Simulate category")
        time.sleep(3)

    def click_small_microcircuit_card(self):
        """Click the Small microcircuit card, scrolling the carousel if needed."""
        # Try to find the card first; if not visible, scroll the carousel right
        try:
            el = self.find_element(Loc.SMALL_MICROCIRCUIT_CARD, timeout=5)
            if el.is_displayed():
                el.click()
                self.logger.info("Clicked Small microcircuit card (already visible)")
                time.sleep(5)
                return
        except TimeoutException:
            pass

        # Card not visible — scroll carousel right until it appears
        for _ in range(5):
            try:
                next_btn = self.element_to_be_clickable(Loc.TYPE_CAROUSEL_NEXT_BTN, timeout=5)
                next_btn.click()
                self.logger.info("Clicked carousel next arrow")
                time.sleep(1)
                try:
                    el = self.find_element(Loc.SMALL_MICROCIRCUIT_CARD, timeout=3)
                    if el.is_displayed():
                        el.click()
                        self.logger.info("Clicked Small microcircuit card (after scrolling)")
                        time.sleep(5)
                        return
                except TimeoutException:
                    continue
            except TimeoutException:
                break

        raise RuntimeError("Small microcircuit card not found after scrolling carousel")

    # ── Model picker ─────────────────────────────────────────────────────

    def click_public_tab(self):
        el = self.find_element(Loc.PUBLIC_TAB, timeout=15)
        el.click()
        self.logger.info("Clicked Public tab")
        time.sleep(3)

    def verify_column_headers(self):
        """Verify expected column headers are present. Returns dict of {name: {'present': bool}}."""
        expected = [
            "Name", "Description", "Brain region",
            "Number of neurons", "Number of synapses", "Number of connections",
            "Created by", "Registration date"
            # "Species" — temporarily excluded, will appear in next deployment
        ]
        headers = self.find_all_elements(Loc.COLUMN_HEADERS, timeout=15)
        header_texts = []
        for h in headers:
            # Read from the inner columnTitle div to avoid sort icon text
            try:
                title_div = h.find_element(By.CSS_SELECTOR, "div[class*='columnTitle']")
                header_texts.append(title_div.text.strip())
            except Exception:
                header_texts.append(h.text.strip().split("\n")[0])
        self.logger.info(f"Column headers found: {header_texts}")
        results = {}
        for name in expected:
            results[name] = {'present': name in header_texts}
        return results

    def get_table_rows(self, timeout=15):
        self.find_element(Loc.TABLE_ROWS, timeout=timeout)
        return self.browser.find_elements(*Loc.TABLE_ROWS)

    def get_row_count(self):
        rows = self.get_table_rows()
        self.logger.info(f"Table has {len(rows)} rows")
        return len(rows)

    def get_pagination_page_count(self):
        """Return the number of pagination page buttons, or 0 if no pagination."""
        try:
            self.find_element(Loc.PAGINATION_CONTAINER, timeout=5)
            items = self.browser.find_elements(*Loc.PAGINATION_ITEMS)
            self.logger.info(f"Pagination has {len(items)} page(s)")
            return len(items)
        except TimeoutException:
            self.logger.info("No pagination found")
            return 0

    def navigate_to_random_page(self):
        """Click a random pagination page (not the currently active one)."""
        items = self.browser.find_elements(*Loc.PAGINATION_ITEMS)
        if len(items) <= 1:
            self.logger.info("Only 1 page, skipping random navigation")
            return

        try:
            active = self.browser.find_element(*Loc.PAGINATION_ACTIVE_ITEM)
            active_num = active.text.strip()
        except Exception:
            active_num = ""

        candidates = [i for i in items if i.text.strip() != active_num]
        if not candidates:
            self.logger.info("No other pages to navigate to")
            return

        target = random.choice(candidates)
        page_num = target.text.strip()
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", target)
        time.sleep(0.5)
        target.click()
        self.logger.info(f"Navigated to page {page_num}")
        time.sleep(3)

    def click_random_row(self):
        """Click a random visible row. Returns the row text snippet."""
        rows = self.get_table_rows()
        if not rows:
            raise RuntimeError("No rows found in the table")

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

    # ── Mini-detail view ─────────────────────────────────────────────────

    def wait_for_mini_detail(self, timeout=15):
        self.element_visibility(Loc.MINI_VIEWER, timeout=timeout)
        self.logger.info("Mini-detail view appeared")
        time.sleep(1)

    def verify_mini_detail_title_and_description(self):
        """Verify title and description are present. Returns dict."""
        results = {}
        try:
            title = self.find_element(Loc.MINI_DETAIL_TITLE, timeout=10)
            results['title'] = {'present': True, 'text': title.text.strip()}
        except TimeoutException:
            results['title'] = {'present': False}
        try:
            desc = self.find_element(Loc.MINI_DETAIL_DESCRIPTION, timeout=5)
            results['description'] = {'present': True}
        except TimeoutException:
            results['description'] = {'present': False}
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

    def wait_for_circuit_preview(self, timeout=30):
        """Wait for the circuit preview image to load."""
        try:
            el = self.find_element(Loc.CIRCUIT_PREVIEW_IMAGE, timeout=timeout)
            bg = el.get_attribute("style") or ""
            has_image = "background-image" in bg and "blob:" in bg
            self.logger.info(f"Circuit preview image loaded: {has_image}")
            return has_image
        except TimeoutException:
            self.logger.warning("Circuit preview image not found")
            return False

    def verify_config_tabs(self):
        results = {}
        for name, locator in [
            ('configuration', Loc.CONFIG_TAB_CONFIGURATION),
            ('simulations', Loc.CONFIG_TAB_SIMULATIONS),
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
        self._click_left_menu_btn(Loc.LEFT_MENU_INFO_BTN, "Info")

    def click_initialization_tab(self):
        self._click_left_menu_btn(Loc.LEFT_MENU_INITIALIZATION_BTN, "Experimental setup")

    def click_stimuli_tab(self):
        self._click_left_menu_btn(Loc.LEFT_MENU_STIMULI_BTN, "Stimulation protocol")

    def click_recordings_tab(self):
        self._click_left_menu_btn(Loc.LEFT_MENU_RECORDINGS_BTN, "Recording")

    # ── Info form ────────────────────────────────────────────────────────

    def is_info_warning_icon_visible(self, timeout=5):
        """Check if the warning icon is visible on the Info menu button."""
        try:
            el = self.find_element(Loc.INFO_BTN_WARNING_ICON, timeout=timeout)
            return el.is_displayed()
        except TimeoutException:
            return False

    def is_info_check_icon_visible(self, timeout=5):
        """Check if the check icon is visible on the Info menu button."""
        try:
            el = self.find_element(Loc.INFO_BTN_CHECK_ICON, timeout=timeout)
            return el.is_displayed()
        except TimeoutException:
            return False

    def fill_name(self, name):
        inp = self.find_element(Loc.FORM_NAME_INPUT, timeout=10)
        inp.click()
        inp.send_keys(Keys.COMMAND + "a")
        inp.send_keys(Keys.BACKSPACE)
        inp.send_keys(name)
        self.logger.info(f"Filled name: '{name}'")

    def fill_description(self, description):
        inp = self.find_element(Loc.FORM_DESCRIPTION_INPUT, timeout=10)
        inp.click()
        inp.send_keys(Keys.COMMAND + "a")
        inp.send_keys(Keys.BACKSPACE)
        inp.send_keys(description)
        self.logger.info(f"Filled description: '{description}'")

    def fill_name_with_datetime(self):
        name = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.fill_name(name)
        return name

    def get_created_by(self):
        try:
            el = self.find_element(Loc.FORM_CREATED_BY, timeout=5)
            return el.text.strip()
        except TimeoutException:
            return ""

    def get_registration_date(self):
        try:
            el = self.find_element(Loc.FORM_REGISTRATION_DATE, timeout=5)
            return el.text.strip()
        except TimeoutException:
            return ""

    # ── Experimental setup tab ───────────────────────────────────────────

    def get_panel_labels(self):
        """Read all labels visible in the simulation panel. Returns list of label texts."""
        panel = self.find_element(Loc.SIMULATION_PANEL, timeout=10)
        labels = panel.find_elements(*Loc.PANEL_LABELS)
        texts = [lbl.text.strip() for lbl in labels if lbl.text.strip()]
        self.logger.info(f"Panel labels ({len(texts)}): {texts}")
        return texts

    # ── Stimulation protocol tab ─────────────────────────────────────────

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

    # ── Recording tab ────────────────────────────────────────────────────

    def click_add_recording(self):
        btn = self.element_to_be_clickable(Loc.RECORDING_ADD_BTN, timeout=10)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(btn).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        self.logger.info("Clicked 'Add' recording button")
        time.sleep(2)

    def get_recording_dropdowns(self):
        try:
            dropdowns = self.browser.find_elements(*Loc.RECORDING_SECTION_DROPDOWN)
            self.logger.info(f"Found {len(dropdowns)} recording dropdown(s)")
            return dropdowns
        except Exception:
            return []

    def get_available_section_prefixes(self, dropdown_index=0):
        """Open a dropdown and return the unique section prefixes available."""
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
            prefix = title.split('[')[0] if '[' in title else title
            prefixes.add(prefix)

        try:
            ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
        except Exception:
            pass
        time.sleep(0.5)

        self.logger.info(f"Available section prefixes: {sorted(prefixes)}")
        return sorted(prefixes)

    def select_recording_section(self, dropdown_index, section_prefix):
        """Open a recording dropdown and select the first option matching the prefix."""
        dropdowns = self.get_recording_dropdowns()
        if dropdown_index >= len(dropdowns):
            self.logger.warning(f"Dropdown index {dropdown_index} out of range ({len(dropdowns)})")
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
                opt.click()
                self.logger.info(f"Selected recording section: '{title}'")
                time.sleep(1)
                return title

        try:
            ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
        except Exception:
            pass
        self.logger.warning(f"No option starting with '{section_prefix}' found")
        return None

    # ── Run experiment ───────────────────────────────────────────────────


    def click_neuron_sets_tab(self):
        self._click_left_menu_btn(Loc.LEFT_MENU_NEURON_SETS_BTN, "Neuron sets")

    def click_synaptic_manip_tab(self):
        self._click_left_menu_btn(Loc.LEFT_MENU_SYNAPTIC_MANIP_BTN, "Synaptic manipulations")

    def click_timestamps_tab(self):
        self._click_left_menu_btn(Loc.LEFT_MENU_TIMESTAMPS_BTN, "Timestamps")

    def get_config_block_labels_and_values(self):
        """Read all config block labels and values in the middle column."""
        blocks = self.find_all_elements(Loc.CONFIG_BLOCK_ELEMENTS, timeout=10)
        results = []
        for i, block in enumerate(blocks):
            label = ""
            value = ""
            has_number_input = False
            try:
                label_el = block.find_element(*Loc.BLOCK_LABEL)
                label = label_el.text.strip()
            except Exception:
                pass
            try:
                input_el = block.find_element(*Loc.BLOCK_NUMBER_INPUT)
                value = input_el.get_attribute("value") or ""
                has_number_input = True
            except Exception:
                pass
            if label:
                results.append({"label": label, "value": value, "has_number_input": has_number_input, "index": i})
                self.logger.info(f"  Block: '{label}' = '{value}'")
        return results

    def get_initialization_labels(self):
        """Return the list of label texts visible in the Initialization tab."""
        try:
            elements = self.find_all_elements(Loc.INIT_BLOCK_LABELS, timeout=10)
            labels = [el.text.strip() for el in elements if el.text.strip()]
            self.logger.info(f"Initialization labels ({len(labels)}): {labels}")
            return labels
        except TimeoutException:
            self.logger.warning("No initialization labels found")
            return []

    def click_add_button_in_active_sub_entry(self):
        """Click the Add button inside the currently active sub-entry."""
        btn = self.element_to_be_clickable(Loc.CONFIG_ADD_BTN_IN_SUB_ENTRY, timeout=10)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(btn).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        self.logger.info(f"Clicked Add button: '{btn.text.strip()}'")
        time.sleep(2)

    def get_dictionary_items(self, timeout=10):
        """Get all dictionary item buttons in the middle column."""
        try:
            items = self.find_all_elements(Loc.CONFIG_BLOCK_DICTIONARY_ITEMS, timeout=timeout)
            short_labels = [item.text.strip().split(chr(10))[0][:40] for item in items]
            self.logger.info(f"Dictionary items ({len(items)}): {short_labels}")
            return items
        except TimeoutException:
            self.logger.warning("No dictionary items found")
            return []

    def click_random_dictionary_item(self):
        """Click a random enabled dictionary item. Returns the label text."""
        import random
        items = self.get_dictionary_items()
        assert items, "No dictionary items found"
        enabled = [
            it for it in items
            if not it.get_attribute("disabled") and "cursor-not-allowed" not in (it.get_attribute("class") or "")
        ]
        assert enabled, "No enabled dictionary items"
        item = random.choice(enabled)
        label = item.text.strip().split(chr(10))[0][:40]
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", item)
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(item).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", item)
        self.logger.info(f"Clicked dictionary item: '{label}'")
        time.sleep(2)
        return label

    def click_dictionary_item_by_label(self, target_label):
        """Click a specific dictionary item by its label text. Returns the label or raises."""
        items = self.get_dictionary_items()
        assert items, "No dictionary items found"
        for item in items:
            text = item.text.strip().split(chr(10))[0].strip()
            if text == target_label:
                self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", item)
                time.sleep(0.5)
                try:
                    ActionChains(self.browser).move_to_element(item).click().perform()
                except Exception:
                    self.browser.execute_script("arguments[0].click();", item)
                self.logger.info(f"Clicked dictionary item: '{target_label}'")
                time.sleep(2)
                return target_label
        raise AssertionError(f"Dictionary item '{target_label}' not found")

    def wait_for_block_single(self, timeout=10):
        """Wait for a block_single form to appear after selecting a dictionary item."""
        el = self.find_element(Loc.CONFIG_BLOCK_SINGLE, timeout=timeout)
        self.logger.info("block_single form appeared")
        return el

    def click_generate_simulation(self):
        btn = self.element_to_be_clickable(Loc.GENERATE_SIMULATION_BTN, timeout=10)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(btn).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        self.logger.info("Clicked 'Generate simulation(s)'")
        time.sleep(3)

    # ── Results tab ──────────────────────────────────────────────────────

    def click_results_tab(self):
        tab = self.element_to_be_clickable(Loc.CONFIG_TAB_SIMULATIONS, timeout=10)
        tab.click()
        self.logger.info("Clicked Simulations tab")
        time.sleep(3)

    def is_results_tab_active(self):
        try:
            tab = self.find_element(Loc.CONFIG_TAB_SIMULATIONS, timeout=5)
            # Beta-style tabs use data-state or gradient background for active
            data_state = tab.get_attribute("data-state")
            if data_state == "active":
                return True
            # Fallback: check for active styling (gradient bg + white text)
            classes = tab.get_attribute("class") or ""
            if "text-white" in classes and ("bg-linear" in classes or "from-[#003A8C]" in classes):
                return True
            return False
        except TimeoutException:
            return False

    # ── Simulations tab: cards, input files, launch ──────────────────────

    def get_simulation_cards(self, timeout=10):
        """Return all simulation card buttons (Simulation 0, Simulation 1, …)."""
        try:
            cards = self.find_all_elements(Loc.SIM_CARD_BUTTONS, timeout=timeout)
            labels = [c.get_attribute("title") or c.text.strip().split('\n')[0] for c in cards]
            self.logger.info(f"Simulation cards ({len(cards)}): {labels}")
            return cards
        except TimeoutException:
            self.logger.warning("No simulation cards found")
            return []

    def get_simulation_card_statuses(self):
        """Return list of {'title': str, 'status': str} for each simulation card."""
        cards = self.get_simulation_cards()
        results = []
        for card in cards:
            title = card.get_attribute("title") or ""
            status = ""
            try:
                badge = card.find_element(*Loc.SIM_CARD_STATUS_BADGE)
                status = badge.text.strip().lower()
            except Exception:
                pass
            results.append({"title": title, "status": status})
        self.logger.info(f"Simulation statuses: {results}")
        return results

    def get_input_file_buttons(self, timeout=10):
        """Return all input file buttons in the middle column."""
        try:
            buttons = self.find_all_elements(Loc.INPUT_FILE_BUTTONS, timeout=timeout)
            names = [b.get_attribute("title") or b.text.strip().split('\n')[0] for b in buttons]
            self.logger.info(f"Input files ({len(buttons)}): {names}")
            return buttons
        except TimeoutException:
            self.logger.warning("No input file buttons found")
            return []

    def click_input_file(self, filename):
        """Click a specific input file button by its title. Returns True if found."""
        buttons = self.get_input_file_buttons()
        for btn in buttons:
            title = btn.get_attribute("title") or ""
            if title == filename:
                self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                time.sleep(0.5)
                try:
                    ActionChains(self.browser).move_to_element(btn).click().perform()
                except Exception:
                    self.browser.execute_script("arguments[0].click();", btn)
                self.logger.info(f"Clicked input file: '{filename}'")
                time.sleep(2)
                return True
        self.logger.warning(f"Input file '{filename}' not found")
        return False

    def get_json_preview_text(self, timeout=10):
        """Return the text content of the JSON preview code block."""
        try:
            code = self.find_element(Loc.JSON_PREVIEW_CODE, timeout=timeout)
            text = code.text.strip()
            self.logger.info(f"JSON preview: {len(text)} chars")
            return text
        except TimeoutException:
            self.logger.warning("JSON preview not found")
            return ""

    def is_launch_simulations_enabled(self, timeout=5):
        """Check if the Launch simulations button is enabled."""
        try:
            btn = self.find_element(Loc.LAUNCH_SIMULATIONS_BTN, timeout=timeout)
            disabled = btn.get_attribute("disabled")
            enabled = disabled is None
            self.logger.info(f"Launch simulations enabled: {enabled}")
            return enabled
        except TimeoutException:
            return False

    def get_launch_simulations_count(self, timeout=5):
        """Parse the number from 'Launch simulations (N)' button text."""
        try:
            el = self.find_element(Loc.LAUNCH_SIMULATIONS_BTN_TEXT, timeout=timeout)
            text = el.text.strip()
            # Extract number from "Launch simulations (1)"
            import re
            match = re.search(r'\((\d+)\)', text)
            count = int(match.group(1)) if match else 0
            self.logger.info(f"Launch simulations count: {count}")
            return count
        except TimeoutException:
            return 0

    def click_launch_simulations(self):
        """Click the Launch simulations button."""
        btn = self.element_to_be_clickable(Loc.LAUNCH_SIMULATIONS_BTN, timeout=10)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(btn).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        self.logger.info("Clicked 'Launch simulations'")
        time.sleep(3)

    def wait_for_simulation_terminal_state(self, timeout=300, poll_interval=10):
        """Poll simulation card statuses until all reach a terminal state (done/failed/error)."""
        import time as _time
        terminal = {'done', 'failed', 'error', 'completed', 'success'}
        start = _time.time()
        while _time.time() - start < timeout:
            statuses = self.get_simulation_card_statuses()
            if statuses and all(s['status'] in terminal for s in statuses):
                elapsed = int(_time.time() - start)
                self.logger.info(f"All simulations reached terminal state after {elapsed}s: {statuses}")
                return True
            elapsed = int(_time.time() - start)
            self.logger.info(f"Simulations still running after {elapsed}s: {[s['status'] for s in statuses]}")
            _time.sleep(poll_interval)
        self.logger.warning(f"Simulations did not complete within {timeout}s")
        return False

    def get_results_left_menu_buttons(self):
        try:
            buttons = self.find_all_elements(Loc.RESULTS_LEFT_MENU_BUTTONS, timeout=10)
            labels = [b.text.strip().split('\n')[0] for b in buttons]
            self.logger.info(f"Results left menu buttons ({len(buttons)}): {labels}")
            return buttons
        except TimeoutException:
            return []

    def get_results_recording_buttons(self):
        try:
            buttons = self.find_all_elements(Loc.RESULTS_RECORDING_BTNS, timeout=10)
            labels = [b.text.strip().split('\n')[0] for b in buttons]
            self.logger.info(f"Recording buttons ({len(buttons)}): {labels}")
            return buttons
        except TimeoutException:
            return []

    def is_download_csv_enabled(self):
        try:
            btn = self.find_element(Loc.RESULTS_DOWNLOAD_CSV_BTN, timeout=5)
            enabled = btn.is_enabled() and btn.get_attribute("disabled") is None
            self.logger.info(f"Download CSV enabled: {enabled}")
            return enabled
        except TimeoutException:
            return False

    def is_reconfigure_enabled(self):
        try:
            btn = self.find_element(Loc.RESULTS_RECONFIGURE_BTN, timeout=5)
            parent = btn.find_element(By.XPATH, "./ancestor::div[@data-slot='popover-trigger']")
            parent_disabled = parent.get_attribute("disabled")
            btn_disabled = btn.get_attribute("disabled")
            enabled = btn_disabled is None and parent_disabled is None
            self.logger.info(f"Reconfigure enabled: {enabled}")
            return enabled
        except Exception:
            return False

    def get_idrest_plot_count(self):
        try:
            plots = self.browser.find_elements(*Loc.RESULTS_IDREST_PLOTS)
            visible = [p for p in plots if p.is_displayed()]
            self.logger.info(f"IDREST plots visible: {len(visible)}")
            return len(visible)
        except Exception:
            return 0

    def is_neuron_canvas_visible(self):
        try:
            canvas = self.find_element(Loc.CIRCUIT_PREVIEW_IMAGE, timeout=10)
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
        try:
            self.element_visibility(Loc.RESULTS_SUCCESS_NOTIFICATION, timeout=timeout)
            self.logger.info("Success notification appeared")
            return True
        except TimeoutException:
            self.logger.warning("Success notification not found")
            return False

    def get_view_simulation_link(self, timeout=10):
        try:
            link = self.find_element(Loc.RESULTS_VIEW_SIMULATION_LINK, timeout=timeout)
            href = link.get_attribute("href")
            self.logger.info(f"View Simulation link: {href}")
            return link
        except TimeoutException:
            return None
