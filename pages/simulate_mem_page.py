# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import random
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pages.home_page import HomePage
from locators.simulate_mem_locators import SimulateMemLocators


class SimulateMemPage(HomePage):
    """Page object for Single neuron simulation entry + model picker.

    Entry: Workflows → Simulate → Single neuron → model picker → Use model.
    Config / generate / launch uses the shared ME-beta scan-config UI —
    hand off to SimulateMeBetaPage after click_use_model().
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
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        el = self.find_element(SimulateMemLocators.PUBLIC_TAB, timeout=15)
        el.click()
        self.logger.info("Clicked Public tab")
        time.sleep(3)
        try:
            WebDriverWait(self.browser, 30).until(
                EC.presence_of_element_located(SimulateMemLocators.TABLE_ROWS)
            )
            self.logger.info("Table rows appeared after Public tab click")
        except Exception:
            self.logger.warning("Table rows not found within 30s after Public tab click")
        time.sleep(1)

    def get_table_rows(self, timeout=15):
        self.find_element(SimulateMemLocators.TABLE_ROWS, timeout=timeout)
        return self.browser.find_elements(*SimulateMemLocators.TABLE_ROWS)

    def get_row_count(self):
        rows = self.get_table_rows()
        self.logger.info(f"Table has {len(rows)} rows")
        return len(rows)

    def click_random_row(self, exclude_date="10.09.2025", exclude_creator="Gil Barrios"):
        """Click a random AG Grid row, skipping rows matching excluded date+creator."""
        rows = self.get_table_rows()
        if not rows:
            raise RuntimeError("No rows found in the table")

        visible_rows = rows[:min(10, len(rows))]
        eligible = []
        for row in visible_rows:
            skip = False
            try:
                creator_cells = row.find_elements(By.CSS_SELECTOR, ".ag-cell[col-id='createdBy']")
                date_cells = row.find_elements(By.CSS_SELECTOR, ".ag-cell[col-id='registrationDate']")
                creator = creator_cells[0].text.strip() if creator_cells else ""
                reg_date = date_cells[0].text.strip() if date_cells else ""
                if exclude_creator in creator and exclude_date in reg_date:
                    self.logger.info(f"Skipping row: creator='{creator}', date='{reg_date}'")
                    skip = True
            except Exception:
                pass
            if not skip:
                eligible.append(row)

        if not eligible:
            self.logger.warning("No eligible rows after filtering, using all visible")
            eligible = visible_rows

        row = random.choice(eligible)
        click_target = row
        name_cells = row.find_elements(By.CSS_SELECTOR, ".ag-cell[col-id='name']")
        if name_cells:
            click_target = name_cells[0]
        row_text = (click_target.text or row.text).split('\n')[0][:60]
        self.logger.info(f"Clicking row: '{row_text}...'")
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", click_target)
        time.sleep(1)
        try:
            ActionChains(self.browser).move_to_element(click_target).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", click_target)
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

    def as_me_beta_page(self):
        """Hand off to SimulateMeBetaPage for shared scan-config UI steps."""
        from pages.simulate_me_beta_page import SimulateMeBetaPage
        return SimulateMeBetaPage(self.browser, self.wait, self.logger, self.lab_url)
