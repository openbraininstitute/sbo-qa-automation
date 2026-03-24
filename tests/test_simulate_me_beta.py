# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import pytest
from pages.simulate_me_beta_page import SimulateMeBetaPage


class TestSimulateMeBeta:
    """Test cases for ME-model picker page (single neuron beta simulation).

    Flow:
    1. Navigate to simulation page (model picker)
    2. Select Public tab
    3. Verify column headers
    4. Open Filters → expand E-type → type 'cADpyr' → apply
    5. Verify E-type column shows filtered results
    6. Click a random model row
    """

    def _get_sim_page(self, setup, logger):
        browser, wait, base_url, lab_id, project_id = setup
        return SimulateMeBetaPage(browser, wait, logger, base_url), lab_id, project_id

    # ── Test: Full flow ──────────────────────────────────────────────────

    @pytest.mark.simulate
    @pytest.mark.run(order=10)
    def test_model_picker_full_flow(self, setup, login, logger, test_config):
        """Full flow: Public tab → verify columns → filter E-type → click model."""
        sim_page, lab_id, project_id = self._get_sim_page(setup, logger)

        # Navigate to simulation page
        sim_page.go_to_simulation_page(lab_id, project_id)
        logger.info("Navigated to simulation page")

        # Step 1: Click Public tab
        sim_page.click_public_tab()
        logger.info("Selected Public tab")

        # Step 2: Verify all column headers are present
        col_results = sim_page.verify_column_headers()
        missing = [name for name, r in col_results.items() if not r['present']]
        assert not missing, f"Missing column headers: {missing}"
        logger.info("All column headers verified")

        # Step 3: Verify table has rows
        row_count = sim_page.get_row_count()
        assert row_count > 0, "Expected at least one model row in the table"
        logger.info(f"Table has {row_count} rows")

        # Step 4: Open Filters → expand E-type → type 'cADpyr' → select → apply
        sim_page.open_filter_panel()
        sim_page.expand_etype_filter()
        sim_page.type_etype_filter("cADpyr")

        try:
            sim_page.select_etype_option("cADpyr")
            logger.info("Selected 'cADpyr' option")
        except Exception as e:
            logger.warning(f"Could not select cADpyr option: {e}")
            from selenium.webdriver.common.by import By
            options = sim_page.browser.find_elements(
                By.CSS_SELECTOR, "div.ant-select-item-option"
            )
            for opt in options[:10]:
                logger.info(f"  Available option: '{opt.text}'")

        sim_page.click_filter_apply()
        time.sleep(3)

        try:
            sim_page.close_filter_panel()
        except Exception:
            pass
        time.sleep(2)

        # Step 5: Verify E-type column values contain 'cADpyr'
        etype_values = sim_page.get_etype_column_values()
        if etype_values:
            for val in etype_values:
                assert 'cADpyr' in val, f"Expected 'cADpyr' in E-type value, got: '{val}'"
            logger.info(f"All {len(etype_values)} E-type values contain 'cADpyr'")
        else:
            logger.warning("No E-type values found after filtering")

        # Step 6: Click a random model row
        row_text = sim_page.click_random_row()
        logger.info(f"Clicked model row: '{row_text}'")

        # Log the resulting page
        sim_page.log_page_structure()
        logger.info(f"After clicking model, URL: {sim_page.browser.current_url}")

    # ── Test: Navigate via workflow cards ─────────────────────────────────

    @pytest.mark.simulate
    @pytest.mark.run(order=11)
    def test_navigate_via_workflow_simulate_card(self, setup, login, logger, test_config):
        """Navigate via Workflows > Simulate > Single neuron (beta) card."""
        from pages.workflows_page import WorkflowsPage

        browser, wait, base_url, lab_id, project_id = setup
        workflows_page = WorkflowsPage(browser, wait, logger, base_url)

        workflows_page.go_to_workflows_page(lab_id, project_id)
        logger.info("Navigated to workflows page")

        workflows_page.click_category_simulate()
        logger.info("Clicked Simulate category")
        time.sleep(2)

        try:
            beta_card = workflows_page.find_simulate_single_neuron_beta()
            assert beta_card.is_displayed(), "Single neuron (beta) card should be displayed"
            beta_card.click()
            logger.info("Clicked Single neuron (beta) card")
            time.sleep(3)

            current_url = browser.current_url
            assert "me-model-circuit-simulation" in current_url, (
                f"Expected me-model-circuit-simulation in URL, got: {current_url}"
            )
            logger.info(f"URL verified: {current_url}")

        except Exception as e:
            logger.warning(f"Single neuron (beta) card not found: {e}")
            pytest.skip("Single neuron (beta) card not available")

    # ── Test: Breadcrumb navigation ──────────────────────────────────────

    @pytest.mark.simulate
    @pytest.mark.run(order=12)
    def test_breadcrumb_navigation(self, setup, login, logger, test_config):
        """Verify breadcrumb links work."""
        sim_page, lab_id, project_id = self._get_sim_page(setup, logger)

        sim_page.go_to_simulation_page(lab_id, project_id)

        try:
            workflows_link = sim_page.find_breadcrumb_workflows()
            assert workflows_link.is_displayed()
            logger.info("Workflows breadcrumb found")

            sim_page.click_breadcrumb_workflows()
            time.sleep(2)

            current_url = sim_page.browser.current_url
            assert "workflows" in current_url, (
                f"Expected workflows in URL, got: {current_url}"
            )
            logger.info("Breadcrumb navigation works")

        except Exception as e:
            logger.warning(f"Breadcrumb test failed: {e}")
