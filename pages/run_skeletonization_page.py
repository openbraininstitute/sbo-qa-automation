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
from locators.run_skeletonization_locators import RunSkeletonizationLocators as Loc


class RunSkeletonizationPage(HomePage):
    """Page object for the EM mesh skeletonization workflow page.

    Entry: Workflows → Process Data → EM mesh skeletonization → model picker → config → run.
    """

    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, base_url)
        self.logger = logger

    # ── Navigation ───────────────────────────────────────────────────────

    def go_to_workflows(self, lab_id, project_id, retries=3, delay=5):
        """Navigate to the Workflows page."""
        path = f"/app/virtual-lab/{lab_id}/{project_id}/workflows"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(90)
                self.go_to_page(path)
                self.wait_for_page_ready(timeout=60)
                self.logger.info(f"Navigated to workflows: {self.browser.current_url}")
                return
            except TimeoutException:
                self.logger.warning(f"Attempt {attempt + 1} failed. Retrying in {delay}s...")
                time.sleep(delay)
                if attempt == retries - 1:
                    raise RuntimeError("Workflows page did not load")

    def wait_for_page_ready(self, timeout=30):
        super().wait_for_page_ready(timeout=timeout)
        time.sleep(2)

    def click_process_data_category(self):
        """Click the Process Data category card on the workflows page."""
        self.wait_for_network_idle(timeout=10)
        el = self.element_to_be_clickable(Loc.PROCESS_DATA_CATEGORY_CARD, timeout=15)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        time.sleep(0.5)
        try:
            el.click()
        except Exception:
            self.browser.execute_script("arguments[0].click();", el)
        self.logger.info("Clicked Process Data category card")
        time.sleep(3)

    def click_em_mesh_skeletonization_card(self):
        """Click the EM mesh skeletonization card, scrolling carousel if needed."""
        try:
            el = self.find_element(Loc.EM_MESH_SKELETONIZATION_CARD, timeout=5)
            if el.is_displayed():
                el.click()
                self.logger.info("Clicked EM mesh skeletonization card (already visible)")
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
                    el = self.find_element(Loc.EM_MESH_SKELETONIZATION_CARD, timeout=3)
                    if el.is_displayed():
                        el.click()
                        self.logger.info("Clicked EM mesh skeletonization card (after scrolling)")
                        time.sleep(5)
                        return
                except TimeoutException:
                    continue
            except TimeoutException:
                break

        raise RuntimeError("EM mesh skeletonization card not found after scrolling carousel")

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

    def verify_mini_detail_contents(self):
        """Verify mini-detail includes name, description, metadata, View details button.
        Returns dict of presence checks.
        """
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

        try:
            self.find_element(Loc.MINI_DETAIL_METADATA, timeout=5)
            results['metadata'] = {'present': True}
        except TimeoutException:
            results['metadata'] = {'present': False}

        try:
            self.find_element(Loc.MINI_DETAIL_VIEW_DETAILS_BTN, timeout=5)
            results['view_details_btn'] = {'present': True}
        except TimeoutException:
            results['view_details_btn'] = {'present': False}

        try:
            self.find_element(Loc.MINI_DETAIL_CLOSE_BTN, timeout=5)
            results['close_btn'] = {'present': True}
        except TimeoutException:
            results['close_btn'] = {'present': False}

        return results

    def tick_row_checkboxes(self, count=2):
        """Tick the specified number of row checkboxes. Returns the number actually ticked."""
        checkboxes = self.find_all_elements(Loc.TABLE_ROW_CHECKBOXES, timeout=10)
        if not checkboxes:
            raise RuntimeError("No row checkboxes found in the table")

        ticked = 0
        for checkbox in checkboxes[:count]:
            try:
                self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
                time.sleep(0.5)
                checkbox.click()
                ticked += 1
                time.sleep(0.5)
            except Exception as e:
                self.logger.warning(f"Could not tick checkbox: {e}")
        return ticked

    def click_use_selection(self, timeout=10):
        """Click the 'Use selection (N)' button after selecting rows."""
        btn = self.element_to_be_clickable(Loc.USE_SELECTION_BTN, timeout=timeout)
        btn_text = btn.text.strip()
        self.logger.info(f"Clicking '{btn_text}'")
        try:
            btn.click()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        time.sleep(5)

    def get_use_selection_count(self, timeout=5):
        """Get the count shown on the Use selection button (e.g., 2 from 'Use selection (2)')."""
        try:
            btn = self.find_element(Loc.USE_SELECTION_BTN, timeout=timeout)
            text = btn.text.strip()
            import re
            match = re.search(r'\((\d+)\)', text)
            return int(match.group(1)) if match else 0
        except Exception:
            return 0

    # ── Config page ──────────────────────────────────────────────────────

    def wait_for_config_page(self, timeout=30):
        self.find_element(Loc.CONFIG_LAYOUT, timeout=timeout)
        self.logger.info("Config page layout loaded")
        time.sleep(2)

    def verify_config_tabs(self):
        """Verify Configuration and Skeletonizations tabs are present."""
        results = {}
        for name, locator in [
            ('configuration', Loc.CONFIG_TAB_CONFIGURATION),
            ('skeletonizations', Loc.CONFIG_TAB_SKELETONIZATIONS),
        ]:
            try:
                el = self.find_element(locator, timeout=10)
                results[name] = {'present': True, 'displayed': el.is_displayed()}
            except TimeoutException:
                results[name] = {'present': False, 'displayed': False}
        return results

    def is_configuration_tab_active(self):
        """Check if Configuration tab is active."""
        try:
            tab = self.find_element(Loc.CONFIG_TAB_CONFIGURATION, timeout=5)
            data_state = tab.get_attribute("data-state")
            if data_state == "active":
                return True
            classes = tab.get_attribute("class") or ""
            if "text-white" in classes and ("bg-linear" in classes or "from-[#003A8C]" in classes):
                return True
            return False
        except TimeoutException:
            return False

    def is_skeletonizations_tab_active(self):
        """Check if Skeletonizations tab is active."""
        try:
            tab = self.find_element(Loc.CONFIG_TAB_SKELETONIZATIONS, timeout=5)
            data_state = tab.get_attribute("data-state")
            if data_state == "active":
                return True
            classes = tab.get_attribute("class") or ""
            if "text-white" in classes and ("bg-linear" in classes or "from-[#003A8C]" in classes):
                return True
            return False
        except TimeoutException:
            return False

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
        self._click_left_menu_btn(Loc.LEFT_MENU_INITIALIZATION_BTN, "Initialization")

    def is_info_tab_active(self):
        """Check if Info is the active left menu button."""
        try:
            active = self.find_element(Loc.LEFT_MENU_ACTIVE_BTN, timeout=5)
            return "Info" in active.text
        except TimeoutException:
            return False

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

    # ── Info form ────────────────────────────────────────────────────────

    def fill_name(self, name):
        inp = self.find_element(Loc.FORM_NAME_INPUT, timeout=10)
        inp.click()
        inp.send_keys(Keys.COMMAND + "a")
        inp.send_keys(Keys.BACKSPACE)
        inp.send_keys(name)
        self.logger.info(f"Filled Campaign name: '{name}'")

    def fill_description(self, description):
        inp = self.find_element(Loc.FORM_DESCRIPTION_INPUT, timeout=10)
        inp.click()
        inp.send_keys(Keys.COMMAND + "a")
        inp.send_keys(Keys.BACKSPACE)
        inp.send_keys(description)
        self.logger.info(f"Filled Campaign description: '{description}'")

    def fill_name_with_datetime(self):
        name = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.fill_name(name)
        return name

    # ── Initialization tab ───────────────────────────────────────────────

    def verify_initialization_title_and_description(self):
        """Verify Initialization section has title and description text."""
        results = {'title': False, 'description': False}
        try:
            self.find_element(Loc.INIT_TITLE, timeout=10)
            results['title'] = True
        except TimeoutException:
            pass
        try:
            self.find_element(Loc.INIT_DESCRIPTION, timeout=10)
            results['description'] = True
        except TimeoutException:
            pass
        self.logger.info(f"Initialization title: {results['title']}, description: {results['description']}")
        return results

    def get_em_cell_mesh_values(self):
        """Return dict with mesh card names for the multi-selection EM cell mesh field."""
        result = {'names': [], 'count': 0}
        try:
            name_elements = self.find_all_elements(Loc.INIT_EM_CELL_MESH_NAMES, timeout=10)
            result['names'] = [el.text.strip() for el in name_elements if el.text.strip()]
            result['count'] = len(result['names'])
            self.logger.info(f"EM cell mesh — {result['count']} selected: {result['names']}")
        except TimeoutException:
            self.logger.warning("EM cell mesh cards not found")
        return result

    def get_neuron_voxel_size_value(self):
        """Return the value of the Neuron voxel size field."""
        try:
            inp = self.find_element(Loc.INIT_NEURON_VOXEL_SIZE, timeout=10)
            val = inp.get_attribute("value") or ""
            self.logger.info(f"Neuron voxel size: '{val}'")
            return val
        except TimeoutException:
            self.logger.warning("Neuron voxel size field not found")
            return ""

    def get_spine_voxel_size_value(self):
        """Return the value of the Spine voxel size field."""
        try:
            inp = self.find_element(Loc.INIT_SPINE_VOXEL_SIZE, timeout=10)
            val = inp.get_attribute("value") or ""
            self.logger.info(f"Spine voxel size: '{val}'")
            return val
        except TimeoutException:
            self.logger.warning("Spine voxel size field not found")
            return ""

    def is_include_full_res_spines_checked(self):
        """Check if the 'Include full resolution spines' checkbox is ticked."""
        try:
            cb = self.find_element(Loc.INIT_INCLUDE_FULL_RES_SPINES_CHECKBOX, timeout=10)
            checked = cb.is_selected() or cb.get_attribute("checked") is not None
            self.logger.info(f"Include full resolution spines checked: {checked}")
            return checked
        except TimeoutException:
            self.logger.warning("Include full resolution spines checkbox not found")
            return False

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

    # ── Generate skeletonization(s) ──────────────────────────────────────

    def click_generate_skeletonization(self):
        btn = self.element_to_be_clickable(Loc.GENERATE_SKELETONIZATION_BTN, timeout=10)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(btn).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        self.logger.info("Clicked 'Generate skeletonization(s)'")
        time.sleep(3)

    # ── Skeletonizations tab ─────────────────────────────────────────────

    def click_skeletonizations_tab(self):
        tab = self.element_to_be_clickable(Loc.CONFIG_TAB_SKELETONIZATIONS, timeout=10)
        tab.click()
        self.logger.info("Clicked Skeletonizations tab")
        time.sleep(3)

    def get_skeletonization_cards(self, timeout=10):
        """Return all skeletonization card buttons."""
        try:
            cards = self.find_all_elements(Loc.SKEL_CARD_BUTTONS, timeout=timeout)
            labels = [c.get_attribute("title") or c.text.strip().split('\n')[0] for c in cards]
            self.logger.info(f"Skeletonization cards ({len(cards)}): {labels}")
            return cards
        except TimeoutException:
            self.logger.warning("No skeletonization cards found")
            return []

    def get_skeletonization_card_statuses(self):
        """Return list of {'title': str, 'status': str} for each card."""
        cards = self.get_skeletonization_cards()
        results = []
        for card in cards:
            title = card.get_attribute("title") or ""
            status = ""
            try:
                badge = card.find_element(*Loc.SKEL_CARD_STATUS_BADGE)
                status = badge.text.strip().lower()
            except Exception:
                pass
            results.append({"title": title, "status": status})
        self.logger.info(f"Skeletonization statuses: {results}")
        return results

    def verify_select_all_present(self):
        """Verify 'Select all' checkbox is present."""
        try:
            self.find_element(Loc.SKEL_SELECT_ALL_CHECKBOX, timeout=10)
            self.logger.info("Select all checkbox present")
            return True
        except TimeoutException:
            self.logger.warning("Select all checkbox not found")
            return False

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
            title = btn.get_attribute("title") or btn.text.strip()
            if filename in title:
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

    def is_launch_skeletonizations_enabled(self, timeout=5):
        """Check if the Launch skeletonizations button is enabled."""
        try:
            btn = self.find_element(Loc.LAUNCH_SKELETONIZATIONS_BTN, timeout=timeout)
            disabled = btn.get_attribute("disabled")
            enabled = disabled is None
            self.logger.info(f"Launch skeletonizations enabled: {enabled}")
            return enabled
        except TimeoutException:
            return False

    def get_launch_skeletonizations_count(self, timeout=5):
        """Parse the number from 'Launch skeletonizations(N)' button text."""
        try:
            el = self.find_element(Loc.LAUNCH_SKELETONIZATIONS_BTN_TEXT, timeout=timeout)
            text = el.text.strip()
            import re
            match = re.search(r'\((\d+)\)', text)
            count = int(match.group(1)) if match else 0
            self.logger.info(f"Launch skeletonizations count: {count}")
            return count
        except TimeoutException:
            return 0

    def click_launch_skeletonizations(self):
        """Click the Launch skeletonizations button."""
        btn = self.element_to_be_clickable(Loc.LAUNCH_SKELETONIZATIONS_BTN, timeout=10)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(btn).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        self.logger.info("Clicked 'Launch skeletonizations'")
        time.sleep(3)

    def wait_for_skeletonization_terminal_state(self, timeout=300, poll_interval=10):
        """Poll skeletonization card statuses until all reach a terminal state."""
        import time as _time
        terminal = {'done', 'failed', 'error', 'completed', 'success'}
        start = _time.time()
        while _time.time() - start < timeout:
            statuses = self.get_skeletonization_card_statuses()
            if statuses and all(s['status'] in terminal for s in statuses):
                elapsed = int(_time.time() - start)
                self.logger.info(
                    f"All skeletonizations reached terminal state after {elapsed}s: {statuses}"
                )
                return True
            elapsed = int(_time.time() - start)
            self.logger.info(
                f"Skeletonizations still running after {elapsed}s: {[s['status'] for s in statuses]}"
            )
            _time.sleep(poll_interval)
        self.logger.warning(f"Skeletonizations did not complete within {timeout}s")
        return False

    # ── Cost modal ───────────────────────────────────────────────────────

    def verify_cost_modal_title(self, timeout=10):
        """Wait for cost modal and return its title text."""
        try:
            el = self.find_element(Loc.COST_MODAL_TITLE, timeout=timeout)
            title = el.text.strip()
            self.logger.info(f"Cost modal title: '{title}'")
            return title
        except TimeoutException:
            self.logger.warning("Cost modal title not found")
            return ""

    def get_cost_modal_items(self):
        """Return list of item texts in the cost modal (e.g., 'Skeletonization 0')."""
        try:
            items = self.find_all_elements(Loc.COST_MODAL_ITEMS, timeout=5)
            texts = [it.text.strip() for it in items]
            self.logger.info(f"Cost modal items: {texts}")
            return texts
        except TimeoutException:
            return []

    def toggle_cost_modal_checkbox(self, index=0):
        """Toggle a checkbox in the cost modal by index."""
        try:
            checkboxes = self.find_all_elements(Loc.COST_MODAL_CHECKBOXES, timeout=5)
            if index < len(checkboxes):
                cb = checkboxes[index]
                cb.click()
                time.sleep(0.5)
                self.logger.info(f"Toggled cost modal checkbox [{index}]")
        except TimeoutException:
            self.logger.warning("Cost modal checkboxes not found")

    def get_cost_modal_total_credits(self):
        """Return the total credits text from the modal."""
        try:
            el = self.find_element(Loc.COST_MODAL_TOTAL_CREDITS, timeout=5)
            text = el.text.strip()
            self.logger.info(f"Total credits: '{text}'")
            return text
        except TimeoutException:
            return ""

    def is_cost_modal_cancel_present(self):
        try:
            self.find_element(Loc.COST_MODAL_CANCEL_BTN, timeout=5)
            return True
        except TimeoutException:
            return False

    def is_cost_modal_confirm_present(self):
        try:
            self.find_element(Loc.COST_MODAL_CONFIRM_BTN, timeout=5)
            return True
        except TimeoutException:
            return False

    def click_cost_modal_confirm(self):
        """Click the Confirm button in the cost modal."""
        btn = self.element_to_be_clickable(Loc.COST_MODAL_CONFIRM_BTN, timeout=10)
        self.browser.execute_script("arguments[0].click();", btn)
        self.logger.info("Clicked Confirm in cost modal")
        time.sleep(2)

    def handle_consent_tab(self, timeout=15):
        """Handle the consent tab that opens after confirming.
        
        The consent tab opens automatically, shows consent info,
        then closes after ~5 seconds. We wait for it to close and
        switch back to the original tab.
        """
        import time as _time
        original_window = self.browser.current_window_handle
        start = _time.time()

        # Wait for new tab to appear
        while _time.time() - start < timeout:
            if len(self.browser.window_handles) > 1:
                break
            _time.sleep(1)

        if len(self.browser.window_handles) > 1:
            # Switch to the new tab
            new_tab = [h for h in self.browser.window_handles if h != original_window][0]
            self.browser.switch_to.window(new_tab)
            self.logger.info(f"Switched to consent tab: {self.browser.current_url}")

            # Wait for it to close (auto-closes after ~5s)
            wait_start = _time.time()
            while _time.time() - wait_start < 15:
                if len(self.browser.window_handles) == 1:
                    break
                _time.sleep(1)

            # Switch back to original
            if original_window in self.browser.window_handles:
                self.browser.switch_to.window(original_window)
            else:
                self.browser.switch_to.window(self.browser.window_handles[0])
            self.logger.info("Back on original tab after consent")
        else:
            self.logger.info("No new tab appeared — consent may have been inline")
        
        time.sleep(2)

    # ── Output files (after skeletonization completes) ────────────────────

    def get_output_file_buttons(self, timeout=10):
        """Return output file buttons that appear after completion."""
        try:
            buttons = self.find_all_elements(Loc.OUTPUT_FILE_BUTTONS, timeout=timeout)
            names = [b.get_attribute("title") or b.get_attribute("data-file-name") or "" for b in buttons]
            self.logger.info(f"Output files ({len(buttons)}): {names}")
            return buttons
        except TimeoutException:
            self.logger.warning("No output file buttons found")
            return []

    def click_output_file(self, filename, timeout=10):
        """Click an output file button by title or data-file-name."""
        buttons = self.get_output_file_buttons(timeout=timeout)
        for btn in buttons:
            title = btn.get_attribute("title") or btn.get_attribute("data-file-name") or ""
            if filename.lower() in title.lower():
                self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                time.sleep(0.5)
                self.browser.execute_script("arguments[0].click();", btn)
                self.logger.info(f"Clicked output file: '{title}'")
                time.sleep(2)
                return True
        self.logger.warning(f"Output file '{filename}' not found")
        return False

    def verify_output_preview(self):
        """Verify the output preview card shows title, description, image, metadata."""
        results = {}
        try:
            title = self.find_element(Loc.OUTPUT_PREVIEW_TITLE, timeout=10)
            results['title'] = title.text.strip()
        except TimeoutException:
            results['title'] = ""
        try:
            desc = self.find_element(Loc.OUTPUT_PREVIEW_DESCRIPTION, timeout=5)
            results['description'] = desc.text.strip()
        except TimeoutException:
            results['description'] = ""
        try:
            img = self.find_element(Loc.OUTPUT_PREVIEW_IMAGE, timeout=5)
            results['image_visible'] = img.is_displayed()
        except TimeoutException:
            results['image_visible'] = False
        try:
            metadata = self.find_all_elements(Loc.OUTPUT_PREVIEW_METADATA, timeout=5)
            results['metadata_count'] = len(metadata)
        except TimeoutException:
            results['metadata_count'] = 0
        self.logger.info(f"Output preview: {results}")
        return results

    def verify_output_action_buttons(self):
        """Verify Copy ID, Download, View details buttons are present."""
        results = {}
        for name, locator in [
            ('copy_id', Loc.OUTPUT_COPY_ID_BTN),
            ('download', Loc.OUTPUT_DOWNLOAD_BTN),
            ('view_details', Loc.OUTPUT_VIEW_DETAILS_BTN),
        ]:
            try:
                el = self.find_element(locator, timeout=5)
                results[name] = el.is_displayed()
            except TimeoutException:
                results[name] = False
        self.logger.info(f"Output action buttons: {results}")
        return results

    def click_output_view_details(self):
        """Click the View details button in the output preview."""
        btn = self.find_element(Loc.OUTPUT_VIEW_DETAILS_BTN, timeout=10)
        href = btn.get_attribute("href")
        self.logger.info(f"Clicking View details, href: {href}")
        self.browser.execute_script("arguments[0].click();", btn)
        time.sleep(3)
        return href
