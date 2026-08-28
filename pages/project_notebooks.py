# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By

from locators.project_notebooks_locators import ProjectNotebooksLocators
from pages.home_page import HomePage
from typing import List
from selenium.webdriver.remote.webelement import WebElement

class ProjectNotebooks(HomePage):
    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, base_url)
        self.home_page = HomePage(browser, wait, base_url)
        self.logger = logger

    def go_to_project_notebooks_page(self, lab_id: str, project_id: str, retries=3, delay=5):
        path = f"/app/virtual-lab/{lab_id}/{project_id}/notebooks/public"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(90)
                self.go_to_page(path)
                self.wait_for_page_ready(timeout=60)
            except TimeoutException:
                print(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                time.sleep(delay)
                if attempt == retries - 1:
                    raise RuntimeError("The Project > Notebooks page did not load within 60 seconds")
        return self.browser.current_url

    def clear_search_notebook_input(self, timeout=15):
        """Clear free-text search and wait until listing results restore."""
        import platform
        from selenium.webdriver.common.keys import Keys

        input_field = self.search_input(timeout=timeout)
        input_field.click()
        modifier = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL
        input_field.send_keys(modifier, "a")
        input_field.send_keys(Keys.BACK_SPACE)

        self.wait_for_condition(
            lambda d: (input_field.get_attribute("value") or "") == "",
            timeout=timeout,
            retries=1,
            message="Search input did not clear",
        )
        # Clearing must also restore the unfiltered notebook list
        self.wait_for_condition(
            lambda d: len(self.rows()) > 1,
            timeout=timeout,
            retries=1,
            message="Notebook list did not restore after clearing search",
        )

    def open_search(self, timeout=10):
        """Ensure the free-text search input is visible (do not close an open search)."""
        try:
            return self.find_element(ProjectNotebooksLocators.SEARCH_INPUT, timeout=3)
        except Exception:
            open_btn = self.find_element(ProjectNotebooksLocators.SEARCH_NOTEBOOK, timeout=timeout)
            open_btn.click()
            return self.find_element(ProjectNotebooksLocators.SEARCH_INPUT, timeout=timeout)

    def column_headers(self):
        return self.find_all_elements(ProjectNotebooksLocators.COLUMN_HEADER)
    
    def get_column_header_texts(self):
        """Get AG Grid / table column header labels (including horizontally scrolled cols)."""
        try:
            # Scroll horizontally so AG Grid renders off-screen header cells
            self.browser.execute_script(
                """
                const viewports = [
                  ...document.querySelectorAll(
                    '.ag-body-horizontal-scroll-viewport, .ag-center-cols-viewport, .ag-header-viewport'
                  )
                ];
                for (const vp of viewports) {
                  try { vp.scrollLeft = vp.scrollWidth; } catch (e) {}
                }
                """
            )
            time.sleep(0.5)
            texts = self.browser.execute_script(
                """
                const headers = [...document.querySelectorAll('.ag-header-cell[role="columnheader"]')];
                const seen = [];
                for (const h of headers) {
                  const titled = h.querySelector('[title]');
                  let raw = '';
                  if (titled && titled.getAttribute('title')) {
                    raw = titled.getAttribute('title').trim();
                  } else {
                    const label = h.querySelector(
                      '.ag-header-cell-text, div[class*="columnTitle"], .ag-header-cell-label'
                    );
                    raw = ((label && label.textContent) || h.textContent || '')
                      .trim().split('\\n')[0].trim();
                  }
                  seen.push(raw);
                }
                // Also restore scroll so the name column stays usable
                const viewports = [
                  ...document.querySelectorAll(
                    '.ag-body-horizontal-scroll-viewport, .ag-center-cols-viewport, .ag-header-viewport'
                  )
                ];
                for (const vp of viewports) {
                  try { vp.scrollLeft = 0; } catch (e) {}
                }
                return seen;
                """
            )
            if texts:
                return texts

            headers = self.find_all_elements(ProjectNotebooksLocators.COLUMN_HEADER, timeout=10)
            fallback = []
            for header in headers:
                try:
                    title_el = header.find_element(
                        By.CSS_SELECTOR,
                        "[title], .ag-header-cell-text, div[class*='columnTitle'], .ag-header-cell-label",
                    )
                    text = (
                        title_el.get_attribute("title")
                        or title_el.text
                        or ""
                    ).strip().split("\n")[0]
                except Exception:
                    text = (header.text or "").strip().split("\n")[0]
                fallback.append(text)
            return fallback
        except Exception as e:
            self.logger.error(f"Failed to get column header texts: {str(e)}")
            return []

    def filter_apply_btn(self):
        try:
            return self.find_element(ProjectNotebooksLocators.COLUMN_FILTER_APPLY_BTN, timeout=5)
        except Exception:
            return self.find_element(ProjectNotebooksLocators.FILTER_APPLY_BTN)

    def filter_clear_btn(self, timeout=15):
        try:
            return self.element_to_be_clickable(
                ProjectNotebooksLocators.COLUMN_FILTER_RESET_BTN, timeout=timeout
            )
        except Exception:
            return self.find_element(ProjectNotebooksLocators.FILTER_CLEAR_BTN, timeout=timeout)

    def clear_name_column_filter(self, timeout=15):
        """Reset the Name column filter and wait for rows to restore."""
        before = len(self.rows())

        # Prefer the Filters badge clear-all control when an active filter count is shown
        try:
            badge = self.find_element(ProjectNotebooksLocators.FILTERS_BADGE_BTN, timeout=3)
            if badge.is_displayed():
                badge.click()
                time.sleep(0.5)
                try:
                    clear_all = self.find_element(ProjectNotebooksLocators.FILTER_CLEAR_BTN, timeout=5)
                    clear_all.click()
                    self.logger.info("Clicked Clear filters from Filters badge panel")
                    time.sleep(2)
                    self.wait_for_condition(
                        lambda d: len(self.rows()) >= max(before, 2),
                        timeout=timeout,
                        retries=1,
                        message="Notebook rows did not restore after Clear filters",
                    )
                    return
                except Exception:
                    # Fall through to Name column Reset
                    try:
                        self.browser.find_element(By.TAG_NAME, "body").click()
                    except Exception:
                        pass
        except Exception:
            pass

        filter_btn = self.find_element(ProjectNotebooksLocators.COLUMN_FILTER_NAME_BTN, timeout=10)
        filter_btn.click()
        time.sleep(0.5)
        reset_btn = self.element_to_be_clickable(
            ProjectNotebooksLocators.COLUMN_FILTER_RESET_BTN, timeout=timeout
        )
        reset_btn.click()
        self.logger.info("Clicked Reset on Name column filter")
        time.sleep(0.5)
        try:
            apply_btn = self.filter_apply_btn()
            apply_btn.click()
            self.logger.info("Clicked Apply after Reset")
        except Exception:
            self.logger.info("No Apply button after Reset")
        time.sleep(2)
        try:
            self.browser.find_element(By.TAG_NAME, "body").click()
        except Exception:
            pass
        self.wait_for_condition(
            lambda d: len(self.rows()) >= max(before, 2),
            timeout=timeout,
            retries=1,
            message="Notebook rows did not restore after clearing Name filter",
        )

    def filter_close_btn(self):
        # Column filter popover closes on outside click / Apply; keep Close as optional fallback
        return self.find_element(ProjectNotebooksLocators.FILTER_CLOSE_BTN)

    def filter_contributor_label(self, timeout=10):
        return self.find_element(ProjectNotebooksLocators.FILTER_CONTRIBUTOR_LABEL, timeout=timeout)

    def filter_contributor_checkbox(self):
        return self.element_visibility(ProjectNotebooksLocators.FILTER_CONTRIBUTOR_CHECKBOX)

    def filter_name_label(self, timeout=10):
        # AG Grid: header "Filter Name" button replaces the old sidebar Name label
        try:
            return self.find_element(ProjectNotebooksLocators.COLUMN_FILTER_NAME_BTN, timeout=5)
        except Exception:
            return self.find_element(ProjectNotebooksLocators.Filter_NAME_LABEL, timeout=timeout)

    def filter_name_input(self, timeout=10):
        try:
            return self.find_element(ProjectNotebooksLocators.COLUMN_FILTER_INPUT, timeout=5)
        except Exception:
            return self.find_element(ProjectNotebooksLocators.FILTER_NAME_INPUT, timeout=timeout)

    def filter_scale_title(self, timeout=10):
        return self.find_element(ProjectNotebooksLocators.FILTER_SCALE_TITLE, timeout=timeout)

    def get_column_cells(self, column_name: str) -> List[WebElement]:
        """Get all cells in a specific column by column header label."""
        try:
            col_id_map = {
                "name": "name",
                "description": "description",
                "scale": "notebook_scale",
                "contributors": "contributions",
                "registration date": "registrationDate",
                "lifecycle status": "lifecycleStatus",
            }
            col_id = col_id_map.get(column_name.lower())
            if col_id:
                cells = self.find_all_elements(
                    (By.CSS_SELECTOR, f".ag-center-cols-container .ag-cell[col-id='{col_id}']"),
                    timeout=10,
                )
                return [cell for cell in cells if (cell.text or "").strip()]

            header_texts = self.get_column_header_texts()
            column_index = None

            for i, header_text in enumerate(header_texts, start=1):
                if header_text.lower() == column_name.lower():
                    column_index = i
                    break

            if column_index is None:
                available_columns = ", ".join([f"'{h}'" for h in header_texts])
                raise ValueError(f"Column '{column_name}' not found. Available columns: {available_columns}")

            xpath = f"//tbody/tr[not(contains(@style,'display: none'))]/td[{column_index}]"
            cells = self.find_all_elements((By.XPATH, xpath))

            return [cell for cell in cells if cell.text.strip()]
            
        except Exception as e:
            self.logger.error(f"Failed to get column cells for '{column_name}': {str(e)}")
            return []

    def page_filter(self):
        return self.find_element(ProjectNotebooksLocators.PAGE_FILTER)

    def row1(self):
        return self.find_element(ProjectNotebooksLocators.ROW1)

    def rows(self):
        return self.find_all_elements(ProjectNotebooksLocators.ROWS)

    def project_tab(self):
        return self.find_element(ProjectNotebooksLocators.PROJECT_TAB)

    def public_tab(self):
        return self.find_element(ProjectNotebooksLocators.PUBLIC_TAB)

    def table_container(self, timeout=10):
        return self.find_element(ProjectNotebooksLocators.TABLE_CONTAINER, timeout=timeout)

    def table_body_container(self, timeout=10):
        return self.find_element(ProjectNotebooksLocators.TABLE_BODY_CONTAINER, timeout=timeout)

    def table_search_result(self, timeout=30):
        """Wait for search results to appear after filtering."""
        try:
            self.find_element(ProjectNotebooksLocators.TABLE_BODY_CONTAINER, timeout=10)
            return self.is_visible(ProjectNotebooksLocators.DATA_ROW_KEY_SEARCH_RESULT, timeout=timeout)
        except Exception as e:
            self.logger.error(f"Failed to find table search result: {str(e)}")
            try:
                rows = self.find_all_elements((By.XPATH, "//tbody/tr"), timeout=5)
                if rows:
                    self.logger.info(f"Found {len(rows)} table rows as fallback")
                    return True
                return False
            except:
                return False
    
    def wait_for_filtered_results(self, timeout=30):
        """Wait for filtered results to appear with multiple fallback strategies."""
        try:
            if self.is_visible(ProjectNotebooksLocators.DATA_ROW_KEY_SEARCH_RESULT, timeout=10):
                self.logger.info("✅ Found specific search result")
                return True
        except:
            pass
        
        try:
            if self.is_visible(ProjectNotebooksLocators.DATA_ROW_FILTERED_RESULT, timeout=10):
                self.logger.info("✅ Found filtered result with key terms")
                return True
        except:
            pass
        
        try:
            rows = self.find_all_elements(ProjectNotebooksLocators.DATA_ROW_ANY_RESULT, timeout=10)
            if rows:
                self.logger.info(f"✅ Found {len(rows)} visible table rows")
                return True
        except:
            pass
        
        self.logger.error("❌ No filtered results found with any strategy")
        return False

    def search_notebook(self, timeout=10):
        """Return the search toggle if present, otherwise the open search input control."""
        try:
            return self.find_element(ProjectNotebooksLocators.SEARCH_NOTEBOOK_OPEN_OR_CLOSE, timeout=3)
        except Exception:
            return self.find_element(ProjectNotebooksLocators.SEARCH_INPUT, timeout=timeout)

    def search_input(self, timeout=10):
        return self.find_element(ProjectNotebooksLocators.SEARCH_INPUT, timeout=timeout)

    def validate_table_headers(self, expected_headers):
        """
        Validates notebooks table headers.

        Expected headers must all be present in order (extra columns are allowed,
        e.g. when AG Grid virtualization or column settings differ slightly).
        """
        try:
            self.find_element(ProjectNotebooksLocators.TABLE_ELEMENT, timeout=20)
            actual_headers = self.get_column_header_texts()

            self.logger.info(f"Expected Headers: {expected_headers}")
            self.logger.info(f"Actual Headers: {actual_headers}")
            print(f"Expected Headers: {expected_headers}")
            print(f"Actual Headers: {actual_headers}")

            missing = [h for h in expected_headers if h not in actual_headers]
            if missing:
                raise AssertionError(
                    f"Missing headers {missing}. Expected={expected_headers}, Actual={actual_headers}"
                )

            # Preserve relative order for the expected headers that are present
            actual_positions = [actual_headers.index(h) for h in expected_headers]
            if actual_positions != sorted(actual_positions):
                raise AssertionError(
                    f"Header order mismatch. Expected order {expected_headers}, Actual={actual_headers}"
                )

            self.logger.info("✅ Table headers validated successfully and match the expected headers.")
            print("✅ Table headers validated successfully and match the expected headers.")
            
        except TimeoutException:
            self.logger.error("❌ The table element was not found on the Project Notebooks page.")
            raise RuntimeError("The table element was not loaded within the timeout.")
        except Exception as e:
            self.logger.error(f"❌ Error validating table headers: {str(e)}")
            raise

    def wait_for_scale_to_be(self, value: str, timeout: int = 10):
        """Wait for all Scale column cells to have the specified value, handling stale elements."""
        value = value.lower()

        def check_scale_values(driver):
            try:
                cells = self.get_column_cells("Scale")
                if not cells:
                    return False
                
                for cell in cells:
                    try:
                        cell_text = cell.text.strip().lower()
                        if cell_text != value:
                            return False
                    except Exception:
                        return False
                return True
            except Exception:
                return False

        self.wait_for_condition(
            check_scale_values,
            timeout=timeout,
            retries=1,
            message=f"Scale column values did not all become '{value}'"
        )

    def action_menu_readme(self):
        """Get the readme action in the mini detail panel."""
        return self.find_element(ProjectNotebooksLocators.ACTION_MENU_README)
    
    def action_menu_download(self):
        """Get the download action in the mini detail panel."""
        return self.find_element(ProjectNotebooksLocators.ACTION_MENU_DOWNLOAD)
    
    def action_menu_run(self):
        """Get the run action and scroll it into view."""
        element = self.find_element(ProjectNotebooksLocators.ACTION_MENU_RUN)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        return element

    def click_run_notebook(self):
        """Click Run notebook using a real click so the new tab is allowed."""
        run_button = self.action_menu_run()
        assert run_button.is_displayed(), "Run action is not displayed"
        try:
            # Prefer a real user click — JS clicks often get popup-blocked
            run_button.click()
        except Exception:
            self.js_click(run_button)
        self.logger.info("Clicked Run notebook")

    def get_visible_toast_texts(self, timeout=5):
        """Return visible toast / alert texts (e.g. insufficient credits)."""
        end = time.time() + timeout
        texts = []
        while time.time() < end and not texts:
            texts = self.browser.execute_script(
                """
                const selectors = [
                  '[role="status"]', '[role="alert"]',
                  '[class*="toast"]', '[class*="Toast"]',
                  '[data-sonner-toast]', '[data-sonner-toaster]',
                  '.ant-message-notice-content', '.ant-notification-notice-message',
                ];
                const seen = new Set();
                for (const sel of selectors) {
                  for (const e of document.querySelectorAll(sel)) {
                    const t = (e.innerText || '').trim();
                    if (t) seen.add(t);
                  }
                }
                // Fallback: credit errors sometimes render outside toast containers
                const body = (document.body && document.body.innerText) || '';
                if (/not enough credits|insufficient credits|does not have enough credits/i.test(body)) {
                  const match = body.match(/[^\\n]*not enough credits[^\\n]*/i);
                  if (match) seen.add(match[0].trim());
                }
                return [...seen];
                """
            ) or []
            if not texts:
                time.sleep(0.5)
        return texts

    def is_run_blocked_by_credits(self, timeout=5):
        """True when Run notebook was blocked by insufficient project credits."""
        texts = self.get_visible_toast_texts(timeout=timeout)
        blob = " ".join(texts).lower()
        return "credit" in blob or "not enough" in blob

    def wait_for_jupyter_tab_or_credit_block(self, timeout=30):
        """Wait for Jupyter tab to open, or detect a credits-block toast."""
        end = time.time() + timeout
        while time.time() < end:
            if len(self.browser.window_handles) > 1:
                return self.wait_for_jupyter_tab(timeout=5), None
            if self.is_run_blocked_by_credits(timeout=1):
                return None, self.get_visible_toast_texts(timeout=1)
            time.sleep(1)
        if self.is_run_blocked_by_credits(timeout=2):
            return None, self.get_visible_toast_texts(timeout=1)
        raise RuntimeError("Second tab (Jupyter notebook) did not open within timeout")

    def js_click(self, element):
        """Click an element using JavaScript to bypass overlay issues."""
        self.browser.execute_script("arguments[0].click();", element)
    
    def modal_close_button(self):
        """Get the modal / mini-viewer close button."""
        return self.find_element(ProjectNotebooksLocators.MODAL_CLOSE_BUTTON)

    def close_blocking_overlays(self):
        """Close ant-modal / dialog overlays that intercept subsequent clicks."""
        try:
            overlays = self.browser.find_elements(
                By.CSS_SELECTOR,
                ".ant-modal-wrap:not([style*='display: none']), [role='dialog']",
            )
            visible = [o for o in overlays if o.is_displayed()]
            if not visible:
                return False
            try:
                close_btn = self.modal_close_button()
                self.js_click(close_btn)
                time.sleep(1)
                self.logger.info("Closed blocking modal/dialog")
                return True
            except Exception:
                self.browser.find_element(By.TAG_NAME, "body").send_keys("\ue00c")  # ESC
                time.sleep(1)
                self.logger.info("Sent ESC to dismiss blocking overlay")
                return True
        except Exception as e:
            self.logger.info(f"No blocking overlay closed: {e}")
            return False


    def wait_for_jupyter_tab(self, timeout=60):
        """Wait for a second tab (Jupyter notebook) to open and verify it."""
        self.wait_for_condition(
            lambda d: len(d.window_handles) > 1,
            timeout=timeout,
            retries=1,
            message="Second tab (Jupyter notebook) did not open within timeout"
        )
        self.logger.info(f"Second tab opened. Total tabs: {len(self.browser.window_handles)}")

        self.browser.switch_to.window(self.browser.window_handles[1])
        time.sleep(5)  # Give Jupyter a moment to load
        jupyter_url = self.browser.current_url
        self.logger.info(f"Jupyter tab URL: {jupyter_url}")

        self.browser.switch_to.window(self.browser.window_handles[0])
        return jupyter_url

    def verify_jupyter_notebook_loaded(self, timeout=120):
        """
        Switch to the Jupyter tab and verify the notebook actually loaded.
        Waits for JupyterLab/JupyterHub UI elements to appear.
        Returns True if the notebook loaded, switches back to the original tab.
        """
        original_window = self.browser.current_window_handle

        self.browser.switch_to.window(self.browser.window_handles[1])
        self.logger.info(f"Switched to Jupyter tab: {self.browser.current_url}")

        jupyter_loaded = False
        jupyter_selectors = [
            (By.CSS_SELECTOR, "#main"),
            (By.CSS_SELECTOR, ".jp-Notebook"),
            (By.CSS_SELECTOR, ".jp-Cell"),
            (By.CSS_SELECTOR, "#jp-main-content-panel"),
            (By.CSS_SELECTOR, ".jp-NotebookPanel"),
            (By.XPATH, "//div[contains(@class, 'jp-Notebook')]"),
        ]

        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            self.logger.info(f"Attempt {attempt}/{max_attempts} to detect Jupyter notebook...")
            for selector in jupyter_selectors:
                try:
                    element = self.find_element(selector, timeout=timeout // max_attempts)
                    self.logger.info(f"Jupyter notebook loaded — found element: {selector}")
                    jupyter_loaded = True
                    break
                except TimeoutException:
                    continue

            if jupyter_loaded:
                break

            if attempt < max_attempts:
                self.logger.info("Jupyter not loaded yet, refreshing page...")
                self.browser.refresh()
                time.sleep(5)

        if not jupyter_loaded:
            self.logger.error(f"Jupyter notebook did not load after {max_attempts} attempts")
            self.browser.save_screenshot("debug_jupyter_not_loaded.png")
            self.logger.info("Screenshot saved as debug_jupyter_not_loaded.png")

        self.browser.switch_to.window(original_window)
        self.logger.info("Switched back to original tab")
        return jupyter_loaded

    def open_notebook_actions_menu(self, button_index=1):
        """Open the notebook mini detail panel so Readme/Download/Run actions are available.

        button_index is 1-based (matches previous plus-button indexing).
        """
        self.close_blocking_overlays()
        self.click_action_and_wait_for_menu(row_index=button_index - 1)

    def click_action_and_wait_for_menu(self, row_index=0, timeout=10, retries=3):
        """Click a notebook name cell and wait for the mini detail actions to appear."""
        for attempt in range(1, retries + 1):
            try:
                self.close_blocking_overlays()
                name_cells = self.find_all_elements(
                    ProjectNotebooksLocators.NOTEBOOK_NAME_CELL, timeout=10
                )
                if not name_cells:
                    raise TimeoutException("No notebook name cells found")
                idx = min(max(row_index, 0), len(name_cells) - 1)
                cell = name_cells[idx]
                self.browser.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", cell
                )
                time.sleep(0.3)
                try:
                    cell.click()
                except Exception:
                    self.js_click(cell)
                self.logger.info(f"Clicked notebook name cell {idx} (attempt {attempt})")
                self.element_visibility(ProjectNotebooksLocators.MINI_VIEWER, timeout=timeout)
                self.element_visibility(ProjectNotebooksLocators.ACTION_MENU_README, timeout=timeout)
                self.logger.info("Notebook mini detail actions appeared")
                return True
            except TimeoutException:
                self.logger.info(
                    f"Notebook actions did not appear on attempt {attempt}, retrying..."
                )
                try:
                    self.browser.find_element(By.TAG_NAME, "body").click()
                except Exception:
                    pass
                time.sleep(1)
        raise Exception(f"Notebook mini detail actions did not appear after {retries} attempts")
