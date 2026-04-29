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
from locators.simulate_ion_channel_locators import SimulateIonChannelLocators as Loc


class SimulateIonChannelPage(HomePage):
    """Page object for the Ion channel (beta) simulation page.

    Entry: Workflows → Simulate → Ion channel → model picker → config → run → results.
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

    def click_ion_channel_card(self):
        """Click the Ion channel card, scrolling the carousel if needed."""
        try:
            el = self.find_element(Loc.ION_CHANNEL_CARD, timeout=5)
            if el.is_displayed():
                el.click()
                self.logger.info("Clicked Ion channel card (already visible)")
                time.sleep(5)
                return
        except TimeoutException:
            pass

        for _ in range(5):
            try:
                next_btn = self.element_to_be_clickable(Loc.TYPE_CAROUSEL_NEXT_BTN, timeout=5)
                next_btn.click()
                self.logger.info("Clicked carousel next arrow")
                time.sleep(1)
                try:
                    el = self.find_element(Loc.ION_CHANNEL_CARD, timeout=3)
                    if el.is_displayed():
                        el.click()
                        self.logger.info("Clicked Ion channel card (after scrolling)")
                        time.sleep(5)
                        return
                except TimeoutException:
                    continue
            except TimeoutException:
                break

        raise RuntimeError("Ion channel card not found after scrolling carousel")

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

    def click_random_row(self):
        """Click a random visible row. Returns the row text snippet."""
        rows = self.get_table_rows()
        if not rows:
            raise RuntimeError("No rows found in the table")

        visible_rows = rows[:min(10, len(rows))]
        row = random.choice(visible_rows)
        row_text = row.text.split('\n')[0][:60]
        self.logger.info(f"Clicking row: '{row_text}...'")
        self.browser.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", row
        )
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
        results = {}
        try:
            title = self.find_element(Loc.MINI_DETAIL_TITLE, timeout=10)
            results['title'] = {'present': True, 'text': title.text.strip()}
        except TimeoutException:
            results['title'] = {'present': False}
        try:
            self.find_element(Loc.MINI_DETAIL_DESCRIPTION, timeout=5)
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

    # ── Right-hand column: Model Traces and Parameters ───────────────────

    def is_model_traces_visible(self, timeout=15):
        """Check if the Model Traces plot is visible in the right column."""
        try:
            el = self.find_element(Loc.MODEL_TRACES_PLOT, timeout=timeout)
            return el.is_displayed()
        except TimeoutException:
            return False

    def is_parameters_section_visible(self, timeout=10):
        """Check if the Parameters section is visible in the right column."""
        try:
            el = self.find_element(Loc.PARAMETERS_SECTION, timeout=timeout)
            return el.is_displayed()
        except TimeoutException:
            return False

    def get_parameter_dropdowns(self, timeout=10):
        """Return all parameter dropdown/accordion elements."""
        try:
            return self.find_all_elements(Loc.PARAMETER_DROPDOWNS, timeout=timeout)
        except TimeoutException:
            return []

    def click_all_parameter_dropdowns(self):
        """Click each parameter dropdown to verify they are clickable."""
        dropdowns = self.get_parameter_dropdowns()
        clicked = 0
        for dd in dropdowns:
            try:
                self.browser.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", dd
                )
                time.sleep(0.3)
                dd.click()
                clicked += 1
                time.sleep(0.3)
            except Exception as e:
                self.logger.warning(f"Could not click parameter dropdown: {e}")
        self.logger.info(f"Clicked {clicked}/{len(dropdowns)} parameter dropdowns")
        return clicked

    # ── Left menu navigation ─────────────────────────────────────────────

    def _click_left_menu_btn(self, locator, label):
        btn = self.element_to_be_clickable(locator, timeout=10)
        self.browser.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", btn
        )
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
        self._click_left_menu_btn(Loc.LEFT_MENU_INITIALIZATION_BTN, "Initialization")

    def click_stimuli_tab(self):
        self._click_left_menu_btn(Loc.LEFT_MENU_STIMULI_BTN, "Stimuli")

    def click_recordings_tab(self):
        self._click_left_menu_btn(Loc.LEFT_MENU_RECORDINGS_BTN, "Recordings")

    # ── Info form ────────────────────────────────────────────────────────

    def is_info_warning_icon_visible(self, timeout=5):
        try:
            el = self.find_element(Loc.INFO_BTN_WARNING_ICON, timeout=timeout)
            return el.is_displayed()
        except TimeoutException:
            return False

    def is_info_check_icon_visible(self, timeout=5):
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
        """Fill name with 'Automated test ddmmyyyy-hhmm' format."""
        stamp = datetime.now().strftime("%d%m%Y-%H%M")
        name = f"Automated test {stamp}"
        self.fill_name(name)
        return name

    # ── Initialization: read blocks, add sweeps ──────────────────────────

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
                results.append({
                    "label": label, "value": value,
                    "has_number_input": has_number_input,
                    "index": i, "element": block,
                })
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

    def _find_block_by_label(self, label_substring):
        """Find a config block element whose label contains the given substring."""
        blocks = self.get_config_block_labels_and_values()
        for b in blocks:
            if label_substring.lower() in b['label'].lower():
                return b
        return None

    def _click_sweep_add_in_block(self, block_element):
        """Click the plus-circle (add sweep) button inside a config block."""
        try:
            add_btn = block_element.find_element(
                By.XPATH,
                ".//button[.//*[contains(@class,'anticon-plus-circle')] or @aria-label='add sweep']"
            )
            self.browser.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", add_btn
            )
            time.sleep(0.3)
            add_btn.click()
            self.logger.info("Clicked sweep add button")
            time.sleep(1)
        except Exception as e:
            self.logger.warning(f"Could not click sweep add button: {e}")

    def _set_number_input_value(self, block_element, value, input_index=0):
        """Set a number input value inside a config block."""
        inputs = block_element.find_elements(*Loc.BLOCK_NUMBER_INPUT)
        if input_index < len(inputs):
            inp = inputs[input_index]
            self.browser.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", inp
            )
            time.sleep(0.3)
            inp.click()
            inp.send_keys(Keys.COMMAND + "a")
            inp.send_keys(Keys.BACKSPACE)
            inp.send_keys(str(value))
            self.logger.info(f"Set input[{input_index}] to {value}")
            time.sleep(0.5)
        else:
            self.logger.warning(
                f"Input index {input_index} out of range ({len(inputs)} inputs)"
            )

    def add_sweep_value(self, label_substring, value):
        """Add a sweep value to a parameter block identified by label substring.

        Clicks the plus-circle button, then fills the new input with *value*.
        """
        block = self._find_block_by_label(label_substring)
        if not block:
            self.logger.warning(f"Block '{label_substring}' not found")
            return
        element = block['element']
        # Count existing inputs before adding
        inputs_before = len(element.find_elements(*Loc.BLOCK_NUMBER_INPUT))
        self._click_sweep_add_in_block(element)
        # Re-fetch to get the new input
        time.sleep(1)
        # Re-find the block since DOM may have changed
        block = self._find_block_by_label(label_substring)
        if block:
            self._set_number_input_value(block['element'], value, input_index=inputs_before)

    def set_parameter_value(self, label_substring, value, input_index=0):
        """Set a parameter value in a block identified by label substring."""
        block = self._find_block_by_label(label_substring)
        if not block:
            self.logger.warning(f"Block '{label_substring}' not found")
            return
        self._set_number_input_value(block['element'], value, input_index=input_index)

    # ── Stimuli ──────────────────────────────────────────────────────────

    def click_add_stimulus(self):
        """Click the Add button inside the active Stimuli sub-entry."""
        btn = self.element_to_be_clickable(Loc.CONFIG_ADD_BTN_IN_SUB_ENTRY, timeout=10)
        self.browser.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", btn
        )
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(btn).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        self.logger.info("Clicked 'Add Stimulus'")
        time.sleep(2)

    def get_dictionary_items(self, timeout=10):
        """Get all dictionary item buttons in the middle column."""
        try:
            items = self.find_all_elements(
                Loc.CONFIG_BLOCK_DICTIONARY_ITEMS, timeout=timeout
            )
            labels = [it.text.strip().split(chr(10))[0][:60] for it in items]
            self.logger.info(f"Dictionary items ({len(items)}): {labels}")
            return items
        except TimeoutException:
            self.logger.warning("No dictionary items found")
            return []

    def click_dictionary_item_by_label(self, target_label):
        """Click a specific dictionary item by its label text."""
        items = self.get_dictionary_items()
        assert items, "No dictionary items found"
        for item in items:
            text = item.text.strip().split(chr(10))[0].strip()
            if target_label.lower() in text.lower():
                self.browser.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", item
                )
                time.sleep(0.5)
                try:
                    ActionChains(self.browser).move_to_element(item).click().perform()
                except Exception:
                    self.browser.execute_script("arguments[0].click();", item)
                self.logger.info(f"Clicked dictionary item: '{text}'")
                time.sleep(2)
                return text
        raise AssertionError(f"Dictionary item '{target_label}' not found")

    def click_random_enabled_dictionary_item(self):
        """Click a random enabled dictionary item. Returns the label text."""
        items = self.get_dictionary_items()
        assert items, "No dictionary items found"
        enabled = [
            it for it in items
            if not it.get_attribute("disabled")
            and "cursor-not-allowed" not in (it.get_attribute("class") or "")
        ]
        assert enabled, "No enabled dictionary items"
        item = random.choice(enabled)
        label = item.text.strip().split(chr(10))[0][:60]
        self.browser.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", item
        )
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
        el = self.find_element(Loc.CONFIG_BLOCK_SINGLE, timeout=timeout)
        self.logger.info("block_single form appeared")
        return el

    # ── Recordings ───────────────────────────────────────────────────────

    def get_recording_checkboxes(self, timeout=10):
        """Return all recording checkbox/toggle elements."""
        try:
            return self.find_all_elements(Loc.RECORDING_CHECKBOXES, timeout=timeout)
        except TimeoutException:
            return []

    def enable_all_recordings(self):
        """Enable all available recording options. Returns count enabled."""
        checkboxes = self.get_recording_checkboxes()
        enabled_count = 0
        for cb in checkboxes:
            try:
                self.browser.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", cb
                )
                time.sleep(0.3)
                # Check if already checked/active
                is_checked = (
                    cb.get_attribute("checked") is not None
                    or "ant-switch-checked" in (cb.get_attribute("class") or "")
                    or "ant-checkbox-checked" in (
                        cb.find_element(By.XPATH, "./ancestor::label").get_attribute("class")
                        if cb.tag_name == "input" else ""
                    )
                )
                if not is_checked:
                    cb.click()
                    time.sleep(0.5)
                enabled_count += 1
            except Exception as e:
                self.logger.warning(f"Could not enable recording checkbox: {e}")
        self.logger.info(f"Enabled {enabled_count} recording(s)")
        return enabled_count

    # ── Generate simulation(s) ───────────────────────────────────────────

    def click_generate_simulation(self):
        btn = self.element_to_be_clickable(Loc.GENERATE_SIMULATION_BTN, timeout=10)
        self.browser.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", btn
        )
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(btn).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        self.logger.info("Clicked 'Generate simulation(s)'")
        time.sleep(3)

    # ── Simulations tab ──────────────────────────────────────────────────

    def click_simulations_tab(self):
        tab = self.element_to_be_clickable(Loc.CONFIG_TAB_SIMULATIONS, timeout=10)
        tab.click()
        self.logger.info("Clicked Simulations tab")
        time.sleep(3)

    def is_simulations_tab_active(self):
        try:
            tab = self.find_element(Loc.CONFIG_TAB_SIMULATIONS, timeout=5)
            data_state = tab.get_attribute("data-state")
            if data_state == "active":
                return True
            classes = tab.get_attribute("class") or ""
            if "text-white" in classes and (
                "bg-linear" in classes or "from-[#003A8C]" in classes
            ):
                return True
            return False
        except TimeoutException:
            return False

    def get_simulation_cards(self, timeout=10):
        """Return all simulation card buttons."""
        try:
            cards = self.find_all_elements(Loc.SIM_CARD_BUTTONS, timeout=timeout)
            labels = [
                c.get_attribute("title") or c.text.strip().split('\n')[0]
                for c in cards
            ]
            self.logger.info(f"Simulation cards ({len(cards)}): {labels}")
            return cards
        except TimeoutException:
            self.logger.warning("No simulation cards found")
            return []

    def get_simulation_card_statuses(self):
        """Return list of {'title': str, 'status': str} for each card."""
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

    # ── Input files ──────────────────────────────────────────────────────

    def get_input_file_buttons(self, timeout=10):
        try:
            buttons = self.find_all_elements(Loc.INPUT_FILE_BUTTONS, timeout=timeout)
            names = [
                b.get_attribute("title") or b.text.strip().split('\n')[0]
                for b in buttons
            ]
            self.logger.info(f"Input files ({len(buttons)}): {names}")
            return buttons
        except TimeoutException:
            self.logger.warning("No input file buttons found")
            return []

    def click_input_file(self, filename):
        """Click a specific input file button by its title."""
        buttons = self.get_input_file_buttons()
        for btn in buttons:
            title = btn.get_attribute("title") or ""
            if title == filename:
                self.browser.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", btn
                )
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
        try:
            code = self.find_element(Loc.JSON_PREVIEW_CODE, timeout=timeout)
            text = code.text.strip()
            self.logger.info(f"JSON preview: {len(text)} chars")
            return text
        except TimeoutException:
            self.logger.warning("JSON preview not found")
            return ""

    # ── Launch simulations ───────────────────────────────────────────────

    def is_launch_simulations_enabled(self, timeout=5):
        try:
            btn = self.find_element(Loc.LAUNCH_SIMULATIONS_BTN, timeout=timeout)
            disabled = btn.get_attribute("disabled")
            enabled = disabled is None
            self.logger.info(f"Launch simulations enabled: {enabled}")
            return enabled
        except TimeoutException:
            return False

    def click_launch_simulations(self):
        btn = self.element_to_be_clickable(Loc.LAUNCH_SIMULATIONS_BTN, timeout=10)
        self.browser.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", btn
        )
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(btn).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        self.logger.info("Clicked 'Launch simulations'")
        time.sleep(3)

    def wait_for_simulation_terminal_state(self, timeout=300, poll_interval=10):
        """Poll simulation card statuses until all reach a terminal state."""
        import time as _time
        terminal = {'done', 'failed', 'error', 'completed', 'success'}
        start = _time.time()
        while _time.time() - start < timeout:
            statuses = self.get_simulation_card_statuses()
            if statuses and all(s['status'] in terminal for s in statuses):
                elapsed = int(_time.time() - start)
                self.logger.info(
                    f"All simulations reached terminal state after {elapsed}s"
                )
                return True
            elapsed = int(_time.time() - start)
            self.logger.info(
                f"Simulations still running after {elapsed}s: "
                f"{[s['status'] for s in statuses]}"
            )
            _time.sleep(poll_interval)
        self.logger.warning(f"Simulations did not complete within {timeout}s")
        return False

    # ── Output files ─────────────────────────────────────────────────────

    def get_output_file_buttons(self, timeout=10):
        try:
            buttons = self.find_all_elements(Loc.OUTPUT_FILE_BUTTONS, timeout=timeout)
            names = [
                b.get_attribute("title") or b.text.strip().split('\n')[0]
                for b in buttons
            ]
            self.logger.info(f"Output files ({len(buttons)}): {names}")
            return buttons
        except TimeoutException:
            self.logger.warning("No output file buttons found")
            return []

    def click_output_file(self, filename):
        """Click a specific output file button by its title."""
        buttons = self.get_output_file_buttons()
        for btn in buttons:
            title = btn.get_attribute("title") or ""
            if title == filename:
                self.browser.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", btn
                )
                time.sleep(0.5)
                try:
                    ActionChains(self.browser).move_to_element(btn).click().perform()
                except Exception:
                    self.browser.execute_script("arguments[0].click();", btn)
                self.logger.info(f"Clicked output file: '{filename}'")
                time.sleep(2)
                return True
        self.logger.warning(f"Output file '{filename}' not found")
        return False

    def is_output_content_visible(self, timeout=10):
        """Check if any output content (plot, image, code, canvas) is visible."""
        try:
            el = self.find_element(Loc.OUTPUT_CONTENT_AREA, timeout=timeout)
            return el.is_displayed()
        except TimeoutException:
            return False

    # ── Recording output: Overview / Interactive details tabs ─────────────

    def is_overview_tab_present(self, timeout=5):
        try:
            el = self.find_element(Loc.OVERVIEW_TAB, timeout=timeout)
            return el.is_displayed()
        except TimeoutException:
            return False

    def is_interactive_details_tab_present(self, timeout=5):
        try:
            el = self.find_element(Loc.INTERACTIVE_DETAILS_TAB, timeout=timeout)
            return el.is_displayed()
        except TimeoutException:
            return False

    def click_overview_tab(self):
        tab = self.element_to_be_clickable(Loc.OVERVIEW_TAB, timeout=10)
        tab.click()
        self.logger.info("Clicked Overview tab")
        time.sleep(2)

    def click_interactive_details_tab(self):
        tab = self.element_to_be_clickable(Loc.INTERACTIVE_DETAILS_TAB, timeout=10)
        tab.click()
        self.logger.info("Clicked Interactive details tab")
        time.sleep(2)

    def is_tab_plot_visible(self, timeout=10):
        """Check if a plot is visible in the currently active tab."""
        try:
            el = self.find_element(Loc.TAB_PLOT_CONTENT, timeout=timeout)
            return el.is_displayed()
        except TimeoutException:
            return False
