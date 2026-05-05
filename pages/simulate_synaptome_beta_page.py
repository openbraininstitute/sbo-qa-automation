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
from locators.simulate_synaptome_beta_locators import SimulateSynaptomeBetaLocators as Loc


class SimulateSynaptomeBetaPage(HomePage):
    """Page object for the Synaptome (beta) simulation page.

    Entry: Workflows → Simulate → Synaptome (beta) → model picker → config → run → results.
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

    def click_synaptome_beta_card(self):
        """Click the Synaptome (beta) card, scrolling the carousel if needed."""
        try:
            el = self.find_element(Loc.SYNAPTOME_BETA_CARD, timeout=5)
            if el.is_displayed():
                el.click()
                self.logger.info("Clicked Synaptome (beta) card (already visible)")
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
                    el = self.find_element(Loc.SYNAPTOME_BETA_CARD, timeout=3)
                    if el.is_displayed():
                        el.click()
                        self.logger.info("Clicked Synaptome (beta) card (after scrolling)")
                        time.sleep(5)
                        return
                except TimeoutException:
                    continue
            except TimeoutException:
                break

        raise RuntimeError("Synaptome (beta) card not found after scrolling carousel")

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

    def verify_column_headers(self):
        expected = [
            "Name", "Description", "Brain region",
            "Number of neurons", "Number of synapses", "Number of connections",
            "Created by", "Registration date",
        ]
        headers = self.find_all_elements(Loc.COLUMN_HEADERS, timeout=15)
        header_texts = []
        for h in headers:
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

    def get_pagination_page_count(self):
        try:
            self.find_element(Loc.PAGINATION_CONTAINER, timeout=5)
            items = self.browser.find_elements(*Loc.PAGINATION_ITEMS)
            self.logger.info(f"Pagination has {len(items)} page(s)")
            return len(items)
        except TimeoutException:
            return 0

    def navigate_to_random_page(self):
        items = self.browser.find_elements(*Loc.PAGINATION_ITEMS)
        if len(items) <= 1:
            return
        try:
            active = self.browser.find_element(*Loc.PAGINATION_ACTIVE_ITEM)
            active_num = active.text.strip()
        except Exception:
            active_num = ""
        candidates = [i for i in items if i.text.strip() != active_num]
        if not candidates:
            return
        target = random.choice(candidates)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", target)
        time.sleep(0.5)
        target.click()
        self.logger.info(f"Navigated to page {target.text.strip()}")
        time.sleep(3)

    def click_random_row(self):
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
        try:
            el = self.find_element(Loc.CIRCUIT_PREVIEW_IMAGE, timeout=timeout)
            bg = el.get_attribute("style") or ""
            has_image = "background-image" in bg and "blob:" in bg
            self.logger.info(f"Circuit preview image loaded: {has_image}")
            return has_image
        except TimeoutException:
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

    def _dismiss_tooltips(self):
        try:
            body = self.browser.find_element(By.TAG_NAME, "body")
            ActionChains(self.browser).move_to_element_with_offset(body, 0, 0).perform()
            time.sleep(0.5)
        except Exception:
            pass
        try:
            body = self.browser.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.ESCAPE)
            time.sleep(0.3)
        except Exception:
            pass
        try:
            self.browser.execute_script("""
                document.querySelectorAll(
                    '[data-slot="tooltip-content"], [role="tooltip"], ' +
                    '[data-radix-popper-content-wrapper], ' +
                    '.ant-tooltip, .ant-popover'
                ).forEach(el => el.remove());
                document.querySelectorAll('[style*="z-index"]').forEach(el => {
                    const z = parseInt(window.getComputedStyle(el).zIndex);
                    if (z > 1000 && el.offsetHeight < 300) el.remove();
                });
            """)
            time.sleep(0.3)
        except Exception:
            pass

    def _click_left_menu_btn(self, locator, label):
        self._dismiss_tooltips()
        try:
            left_col = self.browser.find_element(By.CSS_SELECTOR, "div[class*='scrollable']")
            self.browser.execute_script("arguments[0].scrollTop = 0;", left_col)
            time.sleep(0.5)
        except Exception:
            pass
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
        self._click_left_menu_btn(Loc.LEFT_MENU_INITIALIZATION_BTN, "Initialization")

    def click_stimuli_tab(self):
        self._click_left_menu_btn(Loc.LEFT_MENU_STIMULI_BTN, "Stimuli")

    def click_recordings_tab(self):
        self._click_left_menu_btn(Loc.LEFT_MENU_RECORDINGS_BTN, "Recordings")

    def click_distributions_tab(self):
        self._click_left_menu_btn(Loc.LEFT_MENU_DISTRIBUTIONS_BTN, "Distributions")

    def click_neuron_sets_tab(self):
        self._click_left_menu_btn(Loc.LEFT_MENU_NEURON_SETS_BTN, "Neuron sets")

    def click_synaptic_manip_tab(self):
        self._click_left_menu_btn(Loc.LEFT_MENU_SYNAPTIC_MANIP_BTN, "Synaptic manipulations")

    def click_timestamps_tab(self):
        self._click_left_menu_btn(Loc.LEFT_MENU_TIMESTAMPS_BTN, "Timestamps")

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
        name = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.fill_name(name)
        return name

    # ── Initialization ───────────────────────────────────────────────────

    def get_initialization_labels(self):
        try:
            elements = self.find_all_elements(Loc.INIT_BLOCK_LABELS, timeout=10)
            labels = [el.text.strip() for el in elements if el.text.strip()]
            self.logger.info(f"Initialization labels ({len(labels)}): {labels}")
            return labels
        except TimeoutException:
            return []

    # ── Dictionary items (shared) ────────────────────────────────────────

    def click_add_button_in_active_sub_entry(self):
        self._dismiss_tooltips()
        btn = self.element_to_be_clickable(Loc.CONFIG_ADD_BTN_IN_SUB_ENTRY, timeout=10)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(btn).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        self.logger.info(f"Clicked Add button")
        time.sleep(2)

    def get_dictionary_items(self, timeout=10):
        try:
            items = self.find_all_elements(Loc.CONFIG_BLOCK_DICTIONARY_ITEMS, timeout=timeout)
            labels = [item.text.strip().split(chr(10))[0][:40] for item in items]
            self.logger.info(f"Dictionary items ({len(items)}): {labels}")
            return items
        except TimeoutException:
            return []

    def click_random_dictionary_item(self):
        items = self.get_dictionary_items()
        assert items, "No dictionary items found"
        enabled = [
            it for it in items
            if not it.get_attribute("disabled")
            and "cursor-not-allowed" not in (it.get_attribute("class") or "")
        ]
        assert enabled, "No enabled dictionary items"
        item = random.choice(enabled)
        label = item.text.strip().split(chr(10))[0][:40]
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", item)
        time.sleep(0.5)
        self.browser.execute_script("arguments[0].click();", item)
        self.logger.info(f"Clicked dictionary item: '{label}'")
        time.sleep(2)
        return label

    def click_dictionary_item_by_label(self, target_label):
        items = self.get_dictionary_items()
        assert items, "No dictionary items found"
        for item in items:
            text = item.text.strip().split(chr(10))[0].strip()
            if target_label.lower() in text.lower():
                self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", item)
                time.sleep(0.5)
                self.browser.execute_script("arguments[0].click();", item)
                self.logger.info(f"Clicked dictionary item: '{text}'")
                time.sleep(2)
                return text
        raise AssertionError(f"Dictionary item '{target_label}' not found")

    def click_dictionary_item_by_label_with_scroll(self, target_label):
        try:
            return self.click_dictionary_item_by_label(target_label)
        except AssertionError:
            pass
        try:
            scrollable = self.find_element(Loc.MIDDLE_COLUMN_SCROLLABLE, timeout=5)
            for _ in range(10):
                self.browser.execute_script("arguments[0].scrollTop += 200;", scrollable)
                time.sleep(0.5)
                try:
                    return self.click_dictionary_item_by_label(target_label)
                except AssertionError:
                    continue
        except TimeoutException:
            for _ in range(10):
                self.browser.execute_script("window.scrollBy(0, 200);")
                time.sleep(0.5)
                try:
                    return self.click_dictionary_item_by_label(target_label)
                except AssertionError:
                    continue
        raise AssertionError(f"Dictionary item '{target_label}' not found after scrolling")

    def wait_for_block_single(self, timeout=10):
        el = self.find_element(Loc.CONFIG_BLOCK_SINGLE, timeout=timeout)
        self.logger.info("block_single form appeared")
        return el

    def set_block_number_input(self, label_substring, value):
        blocks = self.find_all_elements(Loc.CONFIG_BLOCK_ELEMENTS, timeout=10)
        for block in blocks:
            try:
                label_el = block.find_element(*Loc.BLOCK_LABEL)
                label_text = label_el.text.strip()
            except Exception:
                continue
            if label_substring.lower() in label_text.lower():
                try:
                    inp = block.find_element(*Loc.BLOCK_NUMBER_INPUT)
                    self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", inp)
                    time.sleep(0.3)
                    inp.click()
                    inp.send_keys(Keys.COMMAND + "a")
                    inp.send_keys(Keys.BACKSPACE)
                    inp.send_keys(str(value))
                    self.logger.info(f"Set '{label_text}' to {value}")
                    time.sleep(0.5)
                    return True
                except Exception as e:
                    self.logger.warning(f"Could not set value for '{label_text}': {e}")
                    return False
        self.logger.warning(f"Block with label '{label_substring}' not found")
        return False

    # ── Generate / Simulations / Launch ──────────────────────────────────

    def click_generate_simulation(self):
        btn = self.element_to_be_clickable(Loc.GENERATE_SIMULATION_BTN, timeout=10)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        self.browser.execute_script("arguments[0].click();", btn)
        self.logger.info("Clicked 'Generate simulation(s)'")
        time.sleep(3)

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
            if "text-white" in classes and ("bg-linear" in classes or "from-[#003A8C]" in classes):
                return True
            return False
        except TimeoutException:
            return False

    def get_simulation_cards(self, timeout=10):
        try:
            cards = self.find_all_elements(Loc.SIM_CARD_BUTTONS, timeout=timeout)
            return cards
        except TimeoutException:
            return []

    def get_simulation_card_statuses(self):
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
        return results

    def get_input_file_buttons(self, timeout=10):
        try:
            return self.find_all_elements(Loc.INPUT_FILE_BUTTONS, timeout=timeout)
        except TimeoutException:
            return []

    def click_input_file(self, filename):
        buttons = self.get_input_file_buttons()
        for btn in buttons:
            title = btn.get_attribute("title") or ""
            if title == filename:
                self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                time.sleep(0.5)
                self.browser.execute_script("arguments[0].click();", btn)
                self.logger.info(f"Clicked input file: '{filename}'")
                time.sleep(2)
                return True
        return False

    def get_json_preview_text(self, timeout=10):
        try:
            code = self.find_element(Loc.JSON_PREVIEW_CODE, timeout=timeout)
            return code.text.strip()
        except TimeoutException:
            return ""

    def is_plot_or_content_visible(self, timeout=10):
        for loc in [
            (By.CSS_SELECTOR, "div.js-plotly-plot"),
            (By.CSS_SELECTOR, "canvas"),
            (By.CSS_SELECTOR, "div[class*='plot']"),
            (By.CSS_SELECTOR, "svg"),
        ]:
            try:
                el = self.find_element(loc, timeout=3)
                if el.is_displayed():
                    return True
            except TimeoutException:
                continue
        return False

    def is_launch_simulations_enabled(self, timeout=5):
        try:
            btn = self.find_element(Loc.LAUNCH_SIMULATIONS_BTN, timeout=timeout)
            return btn.get_attribute("disabled") is None
        except TimeoutException:
            return False

    def click_launch_simulations(self):
        btn = self.element_to_be_clickable(Loc.LAUNCH_SIMULATIONS_BTN, timeout=10)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        self.browser.execute_script("arguments[0].click();", btn)
        self.logger.info("Clicked 'Launch simulations'")
        time.sleep(3)

    def wait_for_simulation_terminal_state(self, timeout=300, poll_interval=10):
        import time as _time
        terminal = {'done', 'failed', 'error', 'completed', 'success'}
        start = _time.time()
        while _time.time() - start < timeout:
            statuses = self.get_simulation_card_statuses()
            if statuses and all(s['status'] in terminal for s in statuses):
                elapsed = int(_time.time() - start)
                self.logger.info(f"All simulations reached terminal state after {elapsed}s")
                return True
            elapsed = int(_time.time() - start)
            self.logger.info(f"Simulations running after {elapsed}s: {[s['status'] for s in statuses]}")
            _time.sleep(poll_interval)
        return False
