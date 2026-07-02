# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
from datetime import datetime
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pages.home_page import HomePage
from locators.build_em_mapping_locators import BuildEMMappingLocators as Loc


class BuildEMMappingPage(HomePage):
    """Page object for the Electron microscopy circuit (beta) build page.

    Entry: Workflows → Build → Electron microscopy circuit (beta) →
           dataset selection → entity selection → config → generate → launch.
    """

    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, base_url)
        self.logger = logger

    # ── Navigation ───────────────────────────────────────────────────────

    def go_to_workflows_build(self, lab_id, project_id, retries=3, delay=5):
        path = f"/app/virtual-lab/{lab_id}/{project_id}/workflows?activity=build"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(90)
                self.go_to_page(path)
                self.wait_for_page_ready(timeout=60)
                self.logger.info(f"Navigated to workflows build: {self.browser.current_url}")
                return
            except TimeoutException:
                self.logger.warning(f"Attempt {attempt + 1} failed. Retrying in {delay}s...")
                time.sleep(delay)
                if attempt == retries - 1:
                    raise RuntimeError("Workflows build page did not load")

    def wait_for_page_ready(self, timeout=30):
        super().wait_for_page_ready(timeout=timeout)
        time.sleep(2)

    def click_build_section(self):
        """Click the Build category card on the workflows page."""
        el = self.element_to_be_clickable(Loc.BUILD_SECTION_CARD, timeout=15)
        el.click()
        self.logger.info("Clicked Build section")
        time.sleep(3)

    def click_em_circuit_card(self):
        """Click the Electron microscopy circuit (beta) card, scrolling carousel if needed."""
        try:
            el = self.find_element(Loc.EM_CIRCUIT_CARD, timeout=5)
            if el.is_displayed():
                el.click()
                self.logger.info("Clicked EM circuit card (already visible)")
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
                    el = self.find_element(Loc.EM_CIRCUIT_CARD, timeout=3)
                    if el.is_displayed():
                        el.click()
                        self.logger.info("Clicked EM circuit card (after scrolling)")
                        time.sleep(5)
                        return
                except TimeoutException:
                    continue
            except TimeoutException:
                break

        raise RuntimeError("Electron microscopy circuit card not found after scrolling carousel")

    # ── Model picker / Dataset selection ──────────────────────────────────

    def click_public_tab(self):
        el = self.element_to_be_clickable(Loc.PUBLIC_TAB, timeout=15)
        el.click()
        self.logger.info("Clicked Public tab")
        time.sleep(3)

    def click_project_tab(self):
        el = self.element_to_be_clickable(Loc.PROJECT_TAB, timeout=15)
        el.click()
        self.logger.info("Clicked Project tab")
        time.sleep(3)

    def verify_breadcrumbs(self):
        """Verify breadcrumbs contain EM build link and dataset selection text."""
        results = {}
        try:
            self.find_element(Loc.BREADCRUMB_EM_BUILD, timeout=10)
            results['em_build'] = True
        except TimeoutException:
            results['em_build'] = False
        try:
            self.find_element(Loc.BREADCRUMB_SELECT_DATASET, timeout=5)
            results['select_dataset'] = True
        except TimeoutException:
            results['select_dataset'] = False
        return results

    def verify_portion_65_card(self):
        """Verify Portion 65 card is displayed with title and description."""
        results = {}
        try:
            self.find_element(Loc.PORTION_65_TITLE, timeout=10)
            results['title_present'] = True
        except TimeoutException:
            results['title_present'] = False
        try:
            desc = self.find_element(Loc.PORTION_65_DESCRIPTION, timeout=5)
            results['description_present'] = bool(desc.text.strip())
        except TimeoutException:
            results['description_present'] = False
        return results

    def click_portion_65_card(self):
        """Click on the Portion 65 card to navigate to the list view."""
        card = self.element_to_be_clickable(Loc.PORTION_65_CARD, timeout=10)
        card.click()
        self.logger.info("Clicked Portion 65 card")
        time.sleep(5)

    # ── Table interactions ────────────────────────────────────────────────

    def get_table_rows(self, timeout=15):
        try:
            self.find_element(Loc.TABLE_ROWS, timeout=timeout)
            return self.browser.find_elements(*Loc.TABLE_ROWS)
        except TimeoutException:
            return []

    def get_row_count(self):
        rows = self.get_table_rows()
        self.logger.info(f"Table has {len(rows)} rows")
        return len(rows)

    def verify_column_headers(self):
        expected = [
            "Preview", "Brain region", "Species",
            "M-type", "Name", "Contributors", "Registration date",
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

    def tick_random_checkbox(self):
        """Tick a random row checkbox in the table."""
        import random
        try:
            checkboxes = self.browser.find_elements(*Loc.TABLE_CHECKBOX)
            if not checkboxes:
                self.logger.warning("No checkboxes found")
                return False
            checkbox = random.choice(checkboxes)
            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
            time.sleep(0.5)
            if not checkbox.is_selected():
                self.browser.execute_script("arguments[0].click();", checkbox)
            self.logger.info(f"Ticked random checkbox (out of {len(checkboxes)})")
            time.sleep(1)
            return True
        except TimeoutException:
            self.logger.warning("No checkbox found")
            return False

    def get_use_selection_button_text(self):
        """Get the text of the Use selection button."""
        try:
            btn = self.find_element(Loc.USE_SELECTION_BTN, timeout=10)
            text = btn.text.strip()
            self.logger.info(f"Use selection button text: '{text}'")
            return text
        except TimeoutException:
            return ""

    def is_use_selection_enabled(self):
        """Check if the Use selection button is enabled."""
        try:
            btn = self.find_element(Loc.USE_SELECTION_BTN, timeout=10)
            disabled = btn.get_attribute("disabled")
            return disabled is None
        except TimeoutException:
            return False

    def click_use_selection(self):
        """Click the Use selection button."""
        btn = self.element_to_be_clickable(Loc.USE_SELECTION_BTN_ENABLED, timeout=10)
        btn.click()
        self.logger.info("Clicked Use selection button")
        time.sleep(5)

    # ── Filter dropdown ──────────────────────────────────────────────────

    def click_filter_dropdown(self):
        """Click on the filter dropdown (Cell morphology by default)."""
        el = self.element_to_be_clickable(Loc.FILTER_DROPDOWN, timeout=10)
        el.click()
        self.logger.info("Clicked filter dropdown")
        time.sleep(2)

    def select_me_model_filter(self):
        """Select ME-model from the filter dropdown."""
        option = self.element_to_be_clickable(Loc.FILTER_ME_MODEL_OPTION, timeout=10)
        option.click()
        self.logger.info("Selected ME-model filter")
        time.sleep(3)

    # ── Config page ──────────────────────────────────────────────────────

    def wait_for_config_page(self, timeout=30):
        self.find_element(Loc.CONFIG_LAYOUT, timeout=timeout)
        self.logger.info("Config page layout loaded")
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

    def is_configuration_tab_active(self):
        """Check if the Configuration tab is currently active."""
        try:
            tab = self.find_element(Loc.CONFIG_TAB_CONFIGURATION, timeout=5)
            classes = tab.get_attribute("class") or ""
            return "text-white" in classes or "from-[#003A8C]" in classes
        except TimeoutException:
            return False

    def is_results_tab_active(self):
        """Check if the Results tab is currently active."""
        try:
            tab = self.find_element(Loc.CONFIG_TAB_RESULTS, timeout=5)
            classes = tab.get_attribute("class") or ""
            return "text-white" in classes or "from-[#003A8C]" in classes
        except TimeoutException:
            return False

    def click_results_tab(self):
        tab = self.element_to_be_clickable(Loc.CONFIG_TAB_RESULTS, timeout=10)
        tab.click()
        self.logger.info("Clicked Results tab")
        time.sleep(3)

    # ── Left menu navigation ─────────────────────────────────────────────

    def _dismiss_tooltips(self):
        """Dismiss any stale tooltips by moving mouse away and removing tooltip DOM."""
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
                    '[data-slot="tooltip-content"], [role="tooltip"], '
                    + '[data-radix-popper-content-wrapper], '
                    + '.ant-tooltip, .ant-popover'
                ).forEach(el => el.remove());
            """)
            time.sleep(0.3)
        except Exception:
            pass

    def _click_left_menu_btn(self, locator, label):
        self._dismiss_tooltips()
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

    # ── Initialization tab ───────────────────────────────────────────────

    def verify_initialization_title(self):
        """Verify INITIALIZATION title is displayed."""
        try:
            self.find_element(Loc.INITIALIZATION_TITLE, timeout=10)
            return True
        except TimeoutException:
            return False

    def verify_neurons_block(self):
        """Verify NEURONS block is displayed with expected content."""
        results = {}
        try:
            self.find_element(Loc.NEURONS_LABEL, timeout=10)
            results['neurons_label'] = True
        except TimeoutException:
            results['neurons_label'] = False

        try:
            containers = self.find_all_elements(Loc.NEURON_GROUP_CONTAINER, timeout=10)
            results['group_count'] = len(containers)
        except TimeoutException:
            results['group_count'] = 0

        try:
            name_input = self.find_element(Loc.NEURON_GROUP_NAME_INPUT, timeout=5)
            results['default_name'] = name_input.get_attribute("value") or ""
        except TimeoutException:
            results['default_name'] = ""

        try:
            badge = self.find_element(Loc.NEURON_GROUP_BADGE_COUNT, timeout=5)
            results['entity_count'] = badge.text.strip()
        except TimeoutException:
            results['entity_count'] = ""

        try:
            self.find_element(Loc.NEURON_ENTITY_CARD, timeout=5)
            results['entity_card_present'] = True
        except TimeoutException:
            results['entity_card_present'] = False

        try:
            self.find_element(Loc.ADD_ITEMS_BTN, timeout=5)
            results['add_items_enabled'] = True
        except TimeoutException:
            results['add_items_enabled'] = False

        return results

    def has_morphology_badge(self):
        try:
            self.find_element(Loc.NEURON_ENTITY_MORPHOLOGY_BADGE, timeout=5)
            return True
        except TimeoutException:
            return False

    def has_me_model_badge(self):
        try:
            self.find_element(Loc.NEURON_ENTITY_ME_MODEL_BADGE, timeout=5)
            return True
        except TimeoutException:
            return False

    # ── Add group / neuron set management ────────────────────────────────

    def is_add_group_to_scan_enabled(self):
        try:
            btn = self.find_element(Loc.ADD_GROUP_TO_SCAN_BTN, timeout=5)
            return btn.get_attribute("disabled") is None
        except TimeoutException:
            return False

    def click_add_group_to_scan(self):
        btn = self.element_to_be_clickable(Loc.ADD_GROUP_TO_SCAN_BTN, timeout=10)
        btn.click()
        self.logger.info("Clicked 'Add group to scan'")
        time.sleep(2)

    def get_neuron_group_count(self):
        """Return the number of neuron group containers."""
        try:
            containers = self.find_all_elements(Loc.NEURON_GROUP_CONTAINER, timeout=10)
            return len(containers)
        except TimeoutException:
            return 0

    def click_add_items_in_group(self, group_index=1):
        """Click 'Add item(s)' button in a specific neuron group (0-indexed)."""
        try:
            btns = self.find_all_elements(Loc.ADD_ITEMS_BTN, timeout=10)
            if group_index < len(btns):
                btns[group_index].click()
                self.logger.info(f"Clicked 'Add item(s)' in group {group_index}")
                time.sleep(3)
                return True
            else:
                self.logger.warning(f"Group index {group_index} out of range ({len(btns)} buttons)")
                return False
        except TimeoutException:
            return False

    def delete_neuron_group(self, group_index=1):
        """Click the delete icon for a specific neuron group (0-indexed)."""
        try:
            btns = self.find_all_elements(Loc.NEURON_ENTITY_DELETE_BTN, timeout=10)
            if group_index < len(btns):
                btns[group_index].click()
                self.logger.info(f"Deleted neuron group {group_index}")
                time.sleep(2)
                return True
            else:
                self.logger.warning(f"Delete button index {group_index} out of range")
                return False
        except TimeoutException:
            return False

    # ── Add neuron set overlay ───────────────────────────────────────────

    def is_overlay_displayed(self):
        """Check if the add neuron set overlay is displayed."""
        try:
            confirm = self.find_element(Loc.OVERLAY_CONFIRM_BTN, timeout=5)
            return confirm.is_displayed()
        except TimeoutException:
            return False

    def is_overlay_cancel_displayed(self):
        try:
            cancel = self.find_element(Loc.OVERLAY_CANCEL_BTN, timeout=5)
            return cancel.is_displayed()
        except TimeoutException:
            return False

    def click_overlay_public_tab(self):
        try:
            tab = self.element_to_be_clickable(Loc.OVERLAY_PUBLIC_TAB, timeout=10)
            tab.click()
            self.logger.info("Clicked Public tab in overlay")
            time.sleep(3)
            return True
        except TimeoutException:
            self.logger.warning("Public tab not found in overlay")
            return False

    def get_overlay_table_row_count(self):
        try:
            rows = self.find_all_elements(Loc.OVERLAY_TABLE_ROWS, timeout=10)
            count = len(rows)
            self.logger.info(f"Overlay table has {count} rows")
            return count
        except TimeoutException:
            return 0

    def click_overlay_cancel(self):
        btn = self.element_to_be_clickable(Loc.OVERLAY_CANCEL_BTN, timeout=10)
        btn.click()
        self.logger.info("Clicked Cancel in overlay")
        time.sleep(2)

    def click_overlay_confirm(self):
        btn = self.element_to_be_clickable(Loc.OVERLAY_CONFIRM_BTN, timeout=10)
        btn.click()
        self.logger.info("Clicked Confirm in overlay")
        time.sleep(3)

    # ── Generate build(s) ────────────────────────────────────────────────

    def is_generate_builds_enabled(self):
        try:
            btn = self.find_element(Loc.GENERATE_BUILDS_BTN, timeout=5)
            return btn.get_attribute("disabled") is None
        except TimeoutException:
            return False

    def click_generate_builds(self):
        btn = self.element_to_be_clickable(Loc.GENERATE_BUILDS_BTN_ENABLED, timeout=10)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(btn).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        self.logger.info("Clicked 'Generate build(s)'")
        time.sleep(5)

    # ── Results tab ──────────────────────────────────────────────────────

    def wait_for_results_tab_active(self, timeout=60):
        """Wait for Results tab to become active after generation."""
        start = time.time()
        while time.time() - start < timeout:
            if self.is_results_tab_active():
                self.logger.info("Results tab is active")
                return True
            time.sleep(2)
        # Try clicking it manually
        try:
            self.click_results_tab()
            time.sleep(3)
            return self.is_results_tab_active()
        except Exception:
            return False

    def get_build_cards(self, timeout=10):
        try:
            cards = self.find_all_elements(Loc.RESULTS_CARD_BUTTONS, timeout=timeout)
            self.logger.info(f"Found {len(cards)} build card(s)")
            return cards
        except TimeoutException:
            return []

    def get_build_card_statuses(self):
        cards = self.get_build_cards()
        results = []
        for card in cards:
            title = card.get_attribute("title") or card.text.strip().split('\n')[0]
            status = ""
            try:
                badge = card.find_element(*Loc.RESULTS_CARD_STATUS_BADGE)
                status = badge.text.strip().lower()
            except Exception:
                pass
            results.append({"title": title, "status": status})
        return results

    # ── Input files ──────────────────────────────────────────────────────

    def get_input_file_buttons(self, timeout=10):
        try:
            buttons = self.find_all_elements(Loc.INPUT_FILE_BUTTONS, timeout=timeout)
            names = [b.get_attribute("title") or b.text.strip() for b in buttons]
            self.logger.info(f"Input files ({len(buttons)}): {names}")
            return buttons
        except TimeoutException:
            return []

    def click_input_file(self, filename):
        buttons = self.get_input_file_buttons()
        for btn in buttons:
            title = btn.get_attribute("title") or btn.text.strip()
            if filename.lower() in title.lower():
                self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                time.sleep(0.5)
                try:
                    ActionChains(self.browser).move_to_element(btn).click().perform()
                except Exception:
                    self.browser.execute_script("arguments[0].click();", btn)
                self.logger.info(f"Clicked input file: '{title}'")
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
            return ""

    # ── Launch builds and modal ──────────────────────────────────────────

    def is_launch_builds_enabled(self, timeout=5):
        try:
            btn = self.find_element(Loc.LAUNCH_BUILDS_BTN, timeout=timeout)
            return btn.get_attribute("disabled") is None
        except TimeoutException:
            return False

    def click_launch_builds(self):
        btn = self.element_to_be_clickable(Loc.LAUNCH_BUILDS_BTN_ENABLED, timeout=10)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(btn).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        self.logger.info("Clicked 'Launch builds'")
        time.sleep(3)

    def is_launch_modal_displayed(self, timeout=10):
        try:
            self.find_element(Loc.LAUNCH_MODAL, timeout=timeout)
            return True
        except TimeoutException:
            return False

    def click_launch_modal_cancel(self):
        btn = self.element_to_be_clickable(Loc.LAUNCH_MODAL_CANCEL_BTN, timeout=10)
        btn.click()
        self.logger.info("Clicked Cancel in launch modal")
        time.sleep(2)

    def click_launch_modal_confirm(self):
        btn = self.element_to_be_clickable(Loc.LAUNCH_MODAL_CONFIRM_BTN, timeout=10)
        btn.click()
        self.logger.info("Clicked Confirm in launch modal")
        time.sleep(3)

    # ── Build status polling ─────────────────────────────────────────────

    def get_current_build_status(self):
        """Get the current status badge text. Tries multiple approaches."""
        # Approach 1: Use the primary locator (span.rounded-full.capitalize)
        try:
            badge = self.find_element(Loc.BUILD_STATUS_BADGE, timeout=5)
            text = badge.text.strip().lower()
            if text:
                return text
        except TimeoutException:
            pass

        # Approach 2: Look inside the build card button for status span
        try:
            badges = self.browser.find_elements(
                By.XPATH,
                "//button[@title]//span[contains(@class,'rounded-full') and contains(@class,'px-4')]"
            )
            for badge in badges:
                text = badge.text.strip().lower()
                if text in ('created', 'pending', 'running', 'done', 'error', 'failed',
                            'completed', 'success'):
                    return text
        except Exception:
            pass

        # Approach 3: Look for any element with capitalize class in the results area
        try:
            badges = self.browser.find_elements(
                By.CSS_SELECTOR,
                "#scan-config-results span.capitalize, "
                "#scan-config-results-left-column span.capitalize"
            )
            for badge in badges:
                text = badge.text.strip().lower()
                if text in ('created', 'pending', 'running', 'done', 'error', 'failed',
                            'completed', 'success'):
                    return text
        except Exception:
            pass

        return ""

    def wait_for_build_terminal_state(self, timeout=300, poll_interval=10):
        """Poll until build reaches a terminal state (Done/Error/Failed)."""
        terminal = {'done', 'failed', 'error', 'completed', 'success'}
        start = time.time()
        empty_count = 0
        while time.time() - start < timeout:
            status = self.get_current_build_status()
            if status in terminal:
                elapsed = int(time.time() - start)
                self.logger.info(f"Build reached terminal state '{status}' after {elapsed}s")
                return status

            elapsed = int(time.time() - start)

            # If status is empty for too long, try refreshing the page
            if not status:
                empty_count += 1
                if empty_count >= 3 and empty_count % 3 == 0:
                    self.logger.info(f"Status empty {empty_count} times, refreshing page...")
                    try:
                        self.browser.refresh()
                        time.sleep(5)
                        # After refresh, try clicking Results tab again
                        if not self.is_results_tab_active():
                            self.click_results_tab()
                            time.sleep(2)
                    except Exception as e:
                        self.logger.warning(f"Refresh failed: {e}")
            else:
                empty_count = 0

            self.logger.info(f"Build status '{status}' after {elapsed}s, waiting...")
            time.sleep(poll_interval)

        self.logger.warning(f"Build did not complete within {timeout}s")
        return self.get_current_build_status()

    # ── Outputs / Task logs ──────────────────────────────────────────────

    def get_task_logs_content(self, timeout=10):
        """Get task logs content from the outputs section."""
        try:
            el = self.find_element(Loc.TASK_LOGS_CONTENT, timeout=timeout)
            return el.text.strip()
        except TimeoutException:
            return ""

    def click_copy_button(self):
        """Click the Copy button."""
        try:
            btn = self.element_to_be_clickable(Loc.COPY_BTN, timeout=10)
            btn.click()
            self.logger.info("Clicked Copy button")
            time.sleep(1)
            return True
        except TimeoutException:
            return False

    def click_copy_json(self):
        """Click JSON option in the copy dropdown."""
        try:
            option = self.element_to_be_clickable(Loc.COPY_JSON_OPTION, timeout=5)
            option.click()
            self.logger.info("Clicked JSON copy option")
            time.sleep(1)
            return True
        except TimeoutException:
            return False

    def is_copy_success_shown(self, timeout=5):
        """Check if copy success indicator is displayed."""
        try:
            self.find_element(Loc.COPY_SUCCESS_INDICATOR, timeout=timeout)
            return True
        except TimeoutException:
            return False

    def click_download_button(self):
        """Click the Download button."""
        try:
            btn = self.element_to_be_clickable(Loc.DOWNLOAD_BTN, timeout=10)
            btn.click()
            self.logger.info("Clicked Download button")
            time.sleep(1)
            return True
        except TimeoutException:
            return False

    def click_download_json(self):
        """Click JSON option in the download dropdown."""
        try:
            option = self.element_to_be_clickable(Loc.DOWNLOAD_JSON_OPTION, timeout=5)
            option.click()
            self.logger.info("Clicked JSON download option")
            time.sleep(2)
            return True
        except TimeoutException:
            return False
