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

    # ── Right-hand column: Model Traces and Activation dropdowns ────────

    def is_model_traces_dropdown_visible(self, timeout=10):
        """Check if the Model traces dropdown is visible in the right column."""
        try:
            el = self.find_element(Loc.MODEL_TRACES_DROPDOWN, timeout=timeout)
            return el.is_displayed()
        except TimeoutException:
            return False

    def is_activation_dropdown_visible(self, timeout=10):
        """Check if the Activation/Inactivation dropdown is visible."""
        try:
            el = self.find_element(Loc.ACTIVATION_DROPDOWN, timeout=timeout)
            return el.is_displayed()
        except TimeoutException:
            return False

    def click_model_traces_dropdown(self, timeout=10):
        """Click the Model traces dropdown and return the items."""
        dd = self.element_to_be_clickable(Loc.MODEL_TRACES_DROPDOWN, timeout=timeout)
        dd.click()
        self.logger.info("Clicked Model traces dropdown")
        time.sleep(1)
        return self._get_select_dropdown_items()

    def click_activation_dropdown(self, timeout=10):
        """Click the Activation dropdown and return the items."""
        dd = self.element_to_be_clickable(Loc.ACTIVATION_DROPDOWN, timeout=timeout)
        dd.click()
        self.logger.info("Clicked Activation dropdown")
        time.sleep(1)
        return self._get_select_dropdown_items()

    def _get_select_dropdown_items(self, timeout=5):
        """Return the list of items in the currently open select dropdown."""
        try:
            items = self.find_all_elements(Loc.SELECT_DROPDOWN_ITEMS, timeout=timeout)
            labels = [it.text.strip() for it in items if it.text.strip()]
            self.logger.info(f"Dropdown items ({len(labels)}): {labels}")
            return items
        except TimeoutException:
            self.logger.warning("No dropdown items found")
            return []

    def select_dropdown_item(self, items, index=0):
        """Click a specific item from an open dropdown by index."""
        if index < len(items):
            item = items[index]
            label = item.text.strip()
            item.click()
            self.logger.info(f"Selected dropdown item [{index}]: '{label}'")
            time.sleep(1)
            return label
        self.logger.warning(f"Dropdown item index {index} out of range ({len(items)})")
        return None

    def get_right_column_plot_count(self, timeout=5):
        """Return the number of plot canvases visible in the right column."""
        try:
            canvases = self.find_all_elements(Loc.RIGHT_COLUMN_PLOT_CANVAS, timeout=timeout)
            visible = [c for c in canvases if c.is_displayed()]
            self.logger.info(f"Right column plots visible: {len(visible)}")
            return len(visible)
        except TimeoutException:
            return 0

    def verify_right_column_after_model_selection(self):
        """Verify Model traces dropdown, Activation dropdown, and plots
        are present in the right column after selecting an ion channel model.
        Returns a dict with results."""
        results = {}

        # Model traces dropdown
        results['model_traces_visible'] = self.is_model_traces_dropdown_visible(timeout=10)
        if results['model_traces_visible']:
            items = self.click_model_traces_dropdown()
            results['model_traces_items'] = len(items)
            self.logger.info(f"Model traces dropdown has {len(items)} item(s)")
            # Close dropdown by pressing Escape
            try:
                ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
                time.sleep(0.5)
            except Exception:
                pass
        else:
            results['model_traces_items'] = 0

        # Activation dropdown
        results['activation_visible'] = self.is_activation_dropdown_visible(timeout=5)
        if results['activation_visible']:
            items = self.click_activation_dropdown()
            results['activation_items'] = len(items)
            self.logger.info(f"Activation dropdown has {len(items)} item(s)")
            # Select first item to verify plot updates
            if items:
                selected = self.select_dropdown_item(items, index=0)
                results['activation_selected'] = selected
            else:
                try:
                    ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
                    time.sleep(0.5)
                except Exception:
                    pass
        else:
            results['activation_items'] = 0

        # Plots
        results['plot_count'] = self.get_right_column_plot_count(timeout=5)

        return results

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

    def collapse_stimuli_tab(self):
        """Click the Stimuli button to collapse its sub-entry if open."""
        self._collapse_left_menu_section(Loc.LEFT_MENU_STIMULI_BTN, "Stimuli")

    def click_recordings_tab(self):
        self._click_left_menu_btn(Loc.LEFT_MENU_RECORDINGS_BTN, "Recordings")

    # ── Ion channel models tab ───────────────────────────────────────────

    def click_ion_channel_models_tab(self):
        self._click_left_menu_btn(Loc.LEFT_MENU_ION_CHANNEL_MODELS_BTN, "Ion channel models")

    def collapse_ion_channel_models_tab(self):
        """Click the Ion channel models button to collapse its sub-entry if open."""
        self._collapse_left_menu_section(Loc.LEFT_MENU_ION_CHANNEL_MODELS_BTN, "Ion channel models")

    def _collapse_left_menu_section(self, locator, label):
        """Collapse a left-menu section if its sub-entry is expanded."""
        try:
            btn = self.find_element(locator, timeout=5)
            self.browser.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", btn
            )
            time.sleep(0.3)

            # Check if the sub-entry is open by looking for an active sub-entry
            # sibling within the same parent container
            parent = btn.find_element(By.XPATH, "./ancestor::div[contains(@class,'flex-col')][1]")
            try:
                sub_entry = parent.find_element(
                    By.CSS_SELECTOR,
                    "div[data-scan-config-menu='menu-block-dictionary-sub-entry'][data-active='true']"
                )
                if sub_entry.is_displayed():
                    btn.click()
                    self.logger.info(f"Collapsed {label} sub-entry")
                    time.sleep(1)
                    return
            except Exception:
                pass

            self.logger.info(f"{label} sub-entry already collapsed")
        except Exception as e:
            self.logger.warning(f"Could not collapse {label}: {e}")

    def click_add_ion_channel_model(self):
        """Click the + / Add button inside the Ion channel models sub-entry."""
        btn = self.element_to_be_clickable(Loc.ION_CHANNEL_MODELS_ADD_BTN, timeout=10)
        self.browser.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", btn
        )
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(btn).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        self.logger.info("Clicked 'Add' ion channel model")
        time.sleep(2)

    def get_ion_channel_model_type_items(self, timeout=10):
        """Get all model type items in the middle column after clicking Add."""
        try:
            items = self.find_all_elements(
                Loc.ION_CHANNEL_MODEL_TYPE_ITEMS, timeout=timeout
            )
            labels = [it.text.strip().split(chr(10))[0][:60] for it in items]
            self.logger.info(f"Ion channel model type items ({len(items)}): {labels}")
            return items
        except TimeoutException:
            self.logger.warning("No ion channel model type items found")
            return []

    def click_ion_channel_model_type(self, index=0):
        """Click a model type item by index. Returns the label text."""
        items = self.get_ion_channel_model_type_items()
        assert len(items) > index, (
            f"Expected at least {index + 1} model type items, got {len(items)}"
        )
        item = items[index]
        label = item.text.strip().split(chr(10))[0][:60]
        self.browser.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", item
        )
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(item).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", item)
        self.logger.info(f"Clicked model type item [{index}]: '{label}'")
        time.sleep(2)
        return label

    def click_ion_channel_model_field(self, timeout=10):
        """Click the ion channel model selection field to open the model list."""
        field = self.element_to_be_clickable(Loc.ION_CHANNEL_MODEL_FIELD, timeout=timeout)
        self.browser.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", field
        )
        time.sleep(0.5)
        field.click()
        self.logger.info("Clicked ion channel model selection field")
        time.sleep(3)

    def select_ion_channel_model_from_list(self, row_index=None, exclude_prefix="Test_DONT_USE_", timeout=15):
        """Select a model from the list view by clicking its radio button.

        By default picks a random row, skipping the first two rows and any row
        whose name starts with *exclude_prefix*.  If *row_index* is explicitly
        provided, that specific row is selected instead (legacy behaviour).
        """
        rows = self.find_all_elements(Loc.ION_CHANNEL_MODEL_LIST_ROWS, timeout=timeout)
        assert len(rows) > 0, "No model rows found in the list"

        if row_index is not None:
            # Legacy explicit index selection
            assert len(rows) > row_index, (
                f"Expected at least {row_index + 1} model rows, got {len(rows)}"
            )
            row = rows[row_index]
        else:
            # Skip first 2 rows and any row matching exclude_prefix
            eligible = []
            for i, r in enumerate(rows):
                if i < 2:
                    row_name = r.text.split('\n')[0].strip()
                    self.logger.info(f"Skipping row [{i}]: '{row_name[:60]}' (first two)")
                    continue
                row_name = r.text.split('\n')[0].strip()
                if exclude_prefix and row_name.startswith(exclude_prefix):
                    self.logger.info(f"Skipping row [{i}]: '{row_name[:60]}' (matches exclude prefix)")
                    continue
                eligible.append(r)

            if not eligible:
                self.logger.warning(
                    "No eligible rows after filtering, falling back to all rows except first two"
                )
                eligible = rows[2:] if len(rows) > 2 else rows

            row = random.choice(eligible)

        row_text = row.text.split('\n')[0][:60]
        self.browser.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", row
        )
        time.sleep(0.5)

        # Try clicking the radio button inside the row
        try:
            radio = row.find_element(
                By.XPATH, ".//input[@type='radio'] | .//span[contains(@class,'ant-radio-inner')]"
            )
            radio.click()
        except Exception:
            # Fallback: click the row itself
            try:
                ActionChains(self.browser).move_to_element(row).click().perform()
            except Exception:
                self.browser.execute_script("arguments[0].click();", row)

        self.logger.info(f"Selected model row: '{row_text}'")
        time.sleep(1)

        # Click the Select button if present (modal footer)
        try:
            select_btn = self.element_to_be_clickable(
                Loc.ION_CHANNEL_MODEL_SELECT_BTN, timeout=5
            )
            select_btn.click()
            self.logger.info("Clicked 'Select' button in modal")
            time.sleep(2)
        except TimeoutException:
            self.logger.info("No modal Select button found — selection may be inline")

        return row_text

    def fill_conductance_value(self, value, timeout=10):
        """Fill in the conductance value input."""
        inp = self.find_element(Loc.ION_CHANNEL_CONDUCTANCE_INPUT, timeout=timeout)
        self.browser.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", inp
        )
        time.sleep(0.3)
        inp.click()
        inp.send_keys(Keys.COMMAND + "a")
        inp.send_keys(Keys.BACKSPACE)
        inp.send_keys(str(value))
        self.logger.info(f"Filled conductance value: {value}")
        time.sleep(0.5)

    def add_and_configure_ion_channel_model(self, type_index, model_row_index=None,
                                             conductance=0.1, permeability=None):
        """Full flow: click model type → select model from list → fill conductance or permeability.

        Args:
            type_index: Index of the model type item to click in the middle column.
            model_row_index: Which row to select from the model list.
                None (default) = random selection, skipping first two rows and
                rows named "Test_DONT_USE_*".
            conductance: Conductance value to fill in (S/cm²).
                None = skip conductance (model has no conductance field).
            permeability: Max permeability value to fill in (ms/s).
                None = skip. Takes precedence over conductance when set.
        """
        label = self.click_ion_channel_model_type(index=type_index)
        self.logger.info(f"Configuring ion channel model type: '{label}'")

        self.wait_for_block_single(timeout=10)

        self.click_ion_channel_model_field()
        model_name = self.select_ion_channel_model_from_list(row_index=model_row_index)
        self.logger.info(f"Selected model: '{model_name}'")

        if permeability is not None:
            self.fill_conductance_value(permeability)
            self.logger.info(
                f"Ion channel model configured: type='{label}', "
                f"model='{model_name}', permeability={permeability} ms/s"
            )
        elif conductance is not None:
            self.fill_conductance_value(conductance)
            self.logger.info(
                f"Ion channel model configured: type='{label}', "
                f"model='{model_name}', conductance={conductance}"
            )
        else:
            self.logger.info(
                f"Ion channel model configured (no conductance/permeability): "
                f"type='{label}', model='{model_name}'"
            )

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
        """Click the plus-circle (add sweep) icon inside a config block."""
        try:
            # The plus-circle is a <span class="anticon anticon-plus-circle">, not a button
            add_icon = block_element.find_element(
                By.XPATH,
                ".//*[contains(@class,'anticon-plus-circle')]"
            )
            self.browser.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", add_icon
            )
            time.sleep(0.3)
            try:
                add_icon.click()
            except Exception:
                self.browser.execute_script("arguments[0].click();", add_icon)
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

    def click_dictionary_item_by_label(self, target_label, exclude_labels=None):
        """Click a specific dictionary item by its label text.

        Args:
            target_label: Substring to match (case-insensitive).
            exclude_labels: List of substrings to skip even if they match target_label.
        """
        items = self.get_dictionary_items()
        assert items, "No dictionary items found"
        exclude_labels = [e.lower() for e in (exclude_labels or [])]
        for item in items:
            text = item.text.strip().split(chr(10))[0].strip()
            if target_label.lower() in text.lower():
                # Skip if it matches an exclusion
                if any(excl in text.lower() for excl in exclude_labels):
                    self.logger.info(f"Skipping excluded match: '{text}'")
                    continue
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

    def click_random_enabled_dictionary_item(self, exclude_labels=None):
        """Click a random enabled dictionary item. Returns the label text.

        Args:
            exclude_labels: List of label substrings to skip (case-insensitive).
        """
        items = self.get_dictionary_items()
        assert items, "No dictionary items found"
        exclude_labels = [e.lower() for e in (exclude_labels or [])]
        enabled = []
        for it in items:
            if it.get_attribute("disabled"):
                continue
            if "cursor-not-allowed" in (it.get_attribute("class") or ""):
                continue
            label = it.text.strip().split(chr(10))[0][:60]
            if any(excl in label.lower() for excl in exclude_labels):
                self.logger.info(f"Skipping excluded stimulus: '{label}'")
                continue
            enabled.append(it)
        assert enabled, "No enabled dictionary items after exclusions"
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

    # ── Recordings (dictionary-based, same pattern as Ion channel models) ─

    def click_add_recording(self):
        """Click the Add Recording button inside the Recordings sub-entry."""
        try:
            btn = self.element_to_be_clickable(Loc.CONFIG_ADD_BTN_IN_SUB_ENTRY, timeout=10)
            self.browser.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", btn
            )
            time.sleep(0.5)
            try:
                btn.click()
            except Exception:
                self.browser.execute_script("arguments[0].click();", btn)
            self.logger.info("Clicked 'Add Recording'")
            time.sleep(2)
        except TimeoutException:
            self.logger.warning("Add Recording button not found")

    def get_recording_entry_count(self, timeout=5):
        """Return the number of recording entry buttons currently visible."""
        try:
            entries = self.find_all_elements(
                Loc.RECORDING_ENTRY_BUTTONS, timeout=timeout
            )
            count = len(entries)
            self.logger.info(f"Recording entries: {count}")
            return count
        except TimeoutException:
            return 0

    def click_recording_entry(self, index=0, timeout=10):
        """Click a recording entry by index, re-fetching from DOM to avoid stale refs."""
        entries = self.find_all_elements(
            Loc.RECORDING_ENTRY_BUTTONS, timeout=timeout
        )
        if index >= len(entries):
            self.logger.warning(
                f"Recording entry index {index} out of range ({len(entries)})"
            )
            return False
        entry = entries[index]
        self.browser.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", entry
        )
        time.sleep(0.5)
        try:
            entry.click()
        except Exception:
            self.browser.execute_script("arguments[0].click();", entry)
        label = entry.text.strip().split(chr(10))[0][:40]
        self.logger.info(f"Clicked recording entry [{index}]: '{label}'")
        time.sleep(2)
        return True

    def select_recording_variable(self, item_index=0, timeout=10):
        """Open the Ion Channel Variable Name dropdown and select an item.

        This must be called after clicking a recording entry so the form is visible.
        Only the 1st recording type has this dropdown; returns None if not found.
        """
        try:
            dd = self.find_element(Loc.RECORDING_VARIABLE_DROPDOWN, timeout=timeout)
            self.browser.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", dd
            )
            time.sleep(1)

            # Check current state
            placeholder = dd.get_attribute("data-placeholder")
            value_spans = dd.find_elements(
                By.CSS_SELECTOR, "span[data-slot='select-value']"
            )
            value_text = value_spans[0].text.strip() if value_spans else ""
            self.logger.info(
                f"Recording variable dropdown state: "
                f"placeholder attr exists={placeholder is not None}, "
                f"value='{value_text[:50]}'"
            )

            # If already filled (no placeholder and has real value), skip
            if placeholder is None and value_text and "select" not in value_text.lower():
                self.logger.info(f"Variable already selected: '{value_text[:50]}'")
                return value_text

            # Click the dropdown to open it
            self.logger.info("Attempting to click the variable dropdown...")
            try:
                ActionChains(self.browser).move_to_element(dd).click().perform()
            except Exception:
                self.browser.execute_script("arguments[0].click();", dd)
            self.logger.info("Clicked Ion Channel Variable Name dropdown")
            time.sleep(3)  # Radix portals can be slow

            # Log the page source around the dropdown for debugging
            expanded = dd.get_attribute("aria-expanded")
            self.logger.info(f"Dropdown aria-expanded after click: {expanded}")

            # After opening the dropdown, try to select by clicking at offsets
            # The Radix portal items are not reliably findable in DOM
            # Strategy: click at increasing Y offsets below the trigger until
            # the placeholder attribute disappears (meaning a value was selected)
            self.logger.info("Attempting to select variable via offset clicks...")

            for y_offset in [45, 90, 135, 45, 90]:
                try:
                    ActionChains(self.browser).move_to_element_with_offset(
                        dd, 0, y_offset
                    ).click().perform()
                    self.logger.info(f"  Clicked at offset y={y_offset}")
                    time.sleep(2)

                    # Check if selection is complete
                    dd_check = self.find_element(
                        Loc.RECORDING_VARIABLE_DROPDOWN, timeout=2
                    )
                    if dd_check.get_attribute("data-placeholder") is None:
                        self.logger.info("Variable selection confirmed!")
                        return "selected via offset click"
                except Exception as e:
                    self.logger.info(f"  Offset y={y_offset} click: {e}")
                    continue

            self.logger.warning("Could not select variable after all offset attempts")
            # Close any open dropdown
            try:
                ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
                time.sleep(0.5)
            except Exception:
                pass
            return None
        except TimeoutException:
            # Dropdown not present — this recording type doesn't have it
            return None

    def add_recordings(self, total=3):
        """Add recordings by selecting recording types from the dictionary items.

        Flow per recording:
        1. Click "Add Recording" → middle column shows recording type options
        2. Click a recording type → it gets added and form appears
        3. For the 1st recording only: select Ion Channel Variable Name

        Returns the final count of recording entries.
        """
        for i in range(total):
            self.logger.info(f"Adding recording {i}...")

            # Click Add to show recording type options in middle column
            self.click_add_recording()

            # Get the available recording types (dictionary items in middle column)
            items = self.get_dictionary_items(timeout=10)
            if not items:
                self.logger.warning(f"No recording type items found for recording {i}")
                break

            # Pick a recording type — use index i (mod available items)
            type_index = i % len(items)
            item = items[type_index]
            label = item.text.strip().split(chr(10))[0][:60]
            self.browser.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", item
            )
            time.sleep(0.5)
            try:
                item.click()
            except Exception:
                self.browser.execute_script("arguments[0].click();", item)
            self.logger.info(f"Selected recording type [{type_index}]: '{label}'")
            time.sleep(2)

            # Wait for the form to appear
            try:
                self.wait_for_block_single(timeout=5)
            except Exception:
                self.logger.warning(f"Recording {i} form did not appear")
                continue

            # Only the 1st recording type needs Ion Channel Variable Name
            if i == 0:
                selected = self.select_recording_variable(item_index=0, timeout=5)
                if selected:
                    self.logger.info(f"Recording {i}: variable = '{selected}'")
                else:
                    self.logger.warning(f"Recording {i}: could not select variable")
            else:
                self.logger.info(f"Recording {i}: no variable needed for this type")

        # Return final count
        final_count = self.get_recording_entry_count()
        self.logger.info(f"Final recording count: {final_count}")
        return final_count

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
