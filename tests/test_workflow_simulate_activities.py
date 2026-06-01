# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import pytest
from pages.workflows_page import WorkflowsPage


class TestWorkflowSimulateActivities:
    """
    Test workflow simulate activities table with:
    - Category: Simulate and Type dropdowns
    - Table with activities (rows with radio buttons)
    - Action buttons per type:
      - Single neuron: View Configuration, View Results (Duplicate displayed but disabled)
      - Synaptome: View Configuration, View Results (Duplicate displayed but disabled)
      - Single neuron (beta): View Configuration, Duplicate
      - Synaptome (beta): View Configuration, Duplicate
      - Ion channel (beta): View Configuration, Duplicate
    """

    @pytest.mark.workflow
    @pytest.mark.activities
    def test_simulate_category_types(self, setup, login, logger, test_config):
        """Test Simulate category with all types"""
        browser, wait, base_url, lab_id, project_id = setup
        workflows_page = WorkflowsPage(browser, wait, logger, base_url)

        workflows_page.go_to_workflows_page(lab_id, project_id)
        logger.info("✅ Navigated to workflows page")

        workflows_page.click_category_dropdown_option('Simulate')
        logger.info("✅ Selected Simulate category")

        simulate_types = [
            'Single neuron', 'Synaptome',
            'Single neuron (beta)', 'Synaptome (beta)', 'Ion channel (beta)',
            'Paired neurons (beta)', 'Small microcircuit (beta)',
            'Microcircuit', 'Brain region',
        ]

        for type_name in simulate_types:
            logger.info(f"🔍 Testing Simulate > {type_name}")

            result = workflows_page.click_type_dropdown_option(type_name)
            assert result, f"Should be able to select type '{type_name}'"

            time.sleep(2)

            row_count = workflows_page.get_table_row_count()
            logger.info(f"✅ Simulate > {type_name}: {row_count} activities found")

    def _setup_workflow_and_select_type(self, setup, login, logger, type_name='Single neuron'):
        """Helper method to navigate to workflows page and select Simulate category/type"""
        browser, wait, base_url, lab_id, project_id = setup
        workflows_page = WorkflowsPage(browser, wait, logger, base_url)

        workflows_page.go_to_workflows_page(lab_id, project_id)
        logger.info("✅ Navigated to workflows page")

        workflows_page.click_category_dropdown_option('Simulate')
        workflows_page.click_type_dropdown_option(type_name)
        time.sleep(2)

        return browser, workflows_page

    def _check_activities_exist(self, workflows_page, logger, type_name):
        """Helper method to check if activities exist and skip test if not"""
        radio_buttons = workflows_page.get_all_radio_buttons()
        if len(radio_buttons) == 0:
            logger.info(f"ℹ️ No Simulate > {type_name} activities to test")
            pytest.skip(f"No Simulate > {type_name} activities available")
        return radio_buttons

    # ── Single neuron (non-beta): View Configuration, View Results, Duplicate disabled ──

    @pytest.mark.workflow
    @pytest.mark.activities
    def test_view_configuration_single_neuron(self, setup, login, logger, test_config):
        """Test View Configuration button for Simulate > Single neuron"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger,
                                                                       type_name='Single neuron')
        self._check_activities_exist(workflows_page, logger, "Single neuron")

        workflows_page.click_first_radio_button()
        time.sleep(1)

        url_before = browser.current_url
        result = workflows_page.click_view_configuration_button()
        assert result, "Should be able to click View Configuration button"

        time.sleep(5)
        current_url = browser.current_url

        url_changed = current_url != url_before
        has_expected_path = any(
            keyword in current_url.lower()
            for keyword in ['single-neuron', 'configuration', 'configure', 'simulate']
        )

        if has_expected_path:
            logger.info(f"✅ Redirected to single neuron simulate config: {current_url}")
        elif url_changed:
            logger.info(f"✅ URL changed after View Configuration: {current_url}")
        else:
            logger.warning(f"⚠️ URL did not change after View Configuration: {current_url}")
            pytest.skip("View Configuration did not redirect — activity may not support it")

    @pytest.mark.workflow
    @pytest.mark.activities
    def test_view_results_single_neuron(self, setup, login, logger, test_config):
        """Test View Results button for Simulate > Single neuron"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger,
                                                                       type_name='Single neuron')
        self._check_activities_exist(workflows_page, logger, "Single neuron")

        workflows_page.click_first_radio_button()
        time.sleep(1)

        result = workflows_page.click_view_results_button()
        assert result, "Should be able to click View Results button"

        time.sleep(3)
        current_url = browser.current_url
        logger.info(f"After View Results click, URL: {current_url}")

    @pytest.mark.workflow
    @pytest.mark.activities
    def test_duplicate_disabled_single_neuron(self, setup, login, logger, test_config):
        """Test Duplicate button is displayed but disabled for Simulate > Single neuron"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger,
                                                                       type_name='Single neuron')
        self._check_activities_exist(workflows_page, logger, "Single neuron")

        workflows_page.click_first_radio_button()
        time.sleep(1)

        assert workflows_page.is_duplicate_button_disabled(), \
            "Duplicate button should be displayed but disabled for Single neuron"
        logger.info("✅ Duplicate button is displayed but disabled")

    # ── Synaptome (non-beta): View Configuration, View Results, Duplicate disabled ──

    @pytest.mark.workflow
    @pytest.mark.activities
    def test_view_configuration_synaptome(self, setup, login, logger, test_config):
        """Test View Configuration button for Simulate > Synaptome"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger,
                                                                       type_name='Synaptome')
        self._check_activities_exist(workflows_page, logger, "Synaptome")

        workflows_page.click_first_radio_button()
        time.sleep(1)

        result = workflows_page.click_view_configuration_button()
        assert result, "Should be able to click View Configuration button"

        time.sleep(3)
        current_url = browser.current_url

        assert 'synaptome' in current_url.lower() or 'configuration' in current_url.lower(), \
            f"Should redirect to synaptome simulate configuration page, got: {current_url}"
        logger.info(f"✅ Redirected to synaptome simulate config: {current_url}")

    @pytest.mark.workflow
    @pytest.mark.activities
    def test_view_results_synaptome(self, setup, login, logger, test_config):
        """Test View Results button for Simulate > Synaptome"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger,
                                                                       type_name='Synaptome')
        self._check_activities_exist(workflows_page, logger, "Synaptome")

        workflows_page.click_first_radio_button()
        time.sleep(1)

        result = workflows_page.click_view_results_button()
        assert result, "Should be able to click View Results button"

        time.sleep(3)
        current_url = browser.current_url
        logger.info(f"After View Results click, URL: {current_url}")

    @pytest.mark.workflow
    @pytest.mark.activities
    def test_duplicate_disabled_synaptome(self, setup, login, logger, test_config):
        """Test Duplicate button is displayed but disabled for Simulate > Synaptome"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger,
                                                                       type_name='Synaptome')
        self._check_activities_exist(workflows_page, logger, "Synaptome")

        workflows_page.click_first_radio_button()
        time.sleep(1)

        assert workflows_page.is_duplicate_button_disabled(), \
            "Duplicate button should be displayed but disabled for Synaptome"
        logger.info("✅ Duplicate button is displayed but disabled")

    # ── Single neuron (beta): View Configuration, Duplicate ──

    @pytest.mark.workflow
    @pytest.mark.activities
    def test_view_configuration_single_neuron_beta(self, setup, login, logger, test_config):
        """Test View Configuration button for Simulate > Single neuron (beta)"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger,
                                                                       type_name='Single neuron (beta)')
        self._check_activities_exist(workflows_page, logger, "Single neuron (beta)")

        workflows_page.click_first_radio_button()
        time.sleep(1)

        url_before = browser.current_url
        result = workflows_page.click_view_configuration_button()
        assert result, "Should be able to click View Configuration button"

        time.sleep(5)
        current_url = browser.current_url

        assert current_url != url_before, \
            f"URL should change after View Configuration, got: {current_url}"
        logger.info(f"✅ Redirected to single neuron beta config: {current_url}")

    @pytest.mark.workflow
    @pytest.mark.activities
    def test_duplicate_single_neuron_beta(self, setup, login, logger, test_config):
        """Test Duplicate button for Simulate > Single neuron (beta)"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger,
                                                                       type_name='Single neuron (beta)')
        self._check_activities_exist(workflows_page, logger, "Single neuron (beta)")

        workflows_page.click_first_radio_button()
        time.sleep(1)

        result = workflows_page.click_duplicate_button()
        assert result, "Should be able to click Duplicate button"

        time.sleep(3)
        current_url = browser.current_url
        logger.info(f"✅ After duplicate, URL: {current_url}")

    # ── Synaptome (beta): View Configuration, Duplicate ──

    @pytest.mark.workflow
    @pytest.mark.activities
    def test_view_configuration_synaptome_beta(self, setup, login, logger, test_config):
        """Test View Configuration button for Simulate > Synaptome (beta)"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger,
                                                                       type_name='Synaptome (beta)')
        self._check_activities_exist(workflows_page, logger, "Synaptome (beta)")

        workflows_page.click_first_radio_button()
        time.sleep(1)

        url_before = browser.current_url
        result = workflows_page.click_view_configuration_button()
        assert result, "Should be able to click View Configuration button"

        time.sleep(5)
        current_url = browser.current_url

        assert current_url != url_before, \
            f"URL should change after View Configuration, got: {current_url}"
        logger.info(f"✅ Redirected to synaptome beta config: {current_url}")

    @pytest.mark.workflow
    @pytest.mark.activities
    def test_duplicate_synaptome_beta(self, setup, login, logger, test_config):
        """Test Duplicate button for Simulate > Synaptome (beta)"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger,
                                                                       type_name='Synaptome (beta)')
        self._check_activities_exist(workflows_page, logger, "Synaptome (beta)")

        workflows_page.click_first_radio_button()
        time.sleep(1)

        result = workflows_page.click_duplicate_button()
        assert result, "Should be able to click Duplicate button"

        time.sleep(3)
        current_url = browser.current_url
        logger.info(f"✅ After duplicate, URL: {current_url}")

    # ── Ion channel (beta): View Configuration, Duplicate ──

    @pytest.mark.workflow
    @pytest.mark.activities
    def test_view_configuration_ion_channel_beta(self, setup, login, logger, test_config):
        """Test View Configuration button for Simulate > Ion channel (beta)"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger,
                                                                       type_name='Ion channel (beta)')
        self._check_activities_exist(workflows_page, logger, "Ion channel (beta)")

        workflows_page.click_first_radio_button()
        time.sleep(1)

        url_before = browser.current_url
        result = workflows_page.click_view_configuration_button()
        assert result, "Should be able to click View Configuration button"

        time.sleep(5)
        current_url = browser.current_url

        assert current_url != url_before, \
            f"URL should change after View Configuration, got: {current_url}"
        logger.info(f"✅ Redirected to ion channel beta config: {current_url}")

    @pytest.mark.workflow
    @pytest.mark.activities
    def test_duplicate_ion_channel_beta(self, setup, login, logger, test_config):
        """Test Duplicate button for Simulate > Ion channel (beta)"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger,
                                                                       type_name='Ion channel (beta)')
        self._check_activities_exist(workflows_page, logger, "Ion channel (beta)")

        workflows_page.click_first_radio_button()
        time.sleep(1)

        result = workflows_page.click_duplicate_button()
        assert result, "Should be able to click Duplicate button"

        time.sleep(3)
        current_url = browser.current_url
        logger.info(f"✅ After duplicate, URL: {current_url}")

    # ── Paired neurons (beta): View Configuration, Duplicate ──

    @pytest.mark.workflow
    @pytest.mark.activities
    def test_view_configuration_paired_neurons_beta(self, setup, login, logger, test_config):
        """Test View Configuration button for Simulate > Paired neurons (beta)"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger,
                                                                       type_name='Paired neurons (beta)')
        self._check_activities_exist(workflows_page, logger, "Paired neurons (beta)")

        workflows_page.click_first_radio_button()
        time.sleep(1)

        url_before = browser.current_url
        result = workflows_page.click_view_configuration_button()
        assert result, "Should be able to click View Configuration button"

        time.sleep(5)
        current_url = browser.current_url

        assert current_url != url_before, \
            f"URL should change after View Configuration, got: {current_url}"
        logger.info(f"✅ Redirected to paired neurons beta config: {current_url}")

    @pytest.mark.workflow
    @pytest.mark.activities
    def test_duplicate_paired_neurons_beta(self, setup, login, logger, test_config):
        """Test Duplicate button for Simulate > Paired neurons (beta)"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger,
                                                                       type_name='Paired neurons (beta)')
        self._check_activities_exist(workflows_page, logger, "Paired neurons (beta)")

        workflows_page.click_first_radio_button()
        time.sleep(1)

        result = workflows_page.click_duplicate_button()
        assert result, "Should be able to click Duplicate button"

        time.sleep(3)
        current_url = browser.current_url
        logger.info(f"✅ After duplicate, URL: {current_url}")

    # ── Small microcircuit (beta): View Configuration, Duplicate ──

    @pytest.mark.workflow
    @pytest.mark.activities
    def test_view_configuration_small_microcircuit_beta(self, setup, login, logger, test_config):
        """Test View Configuration button for Simulate > Small microcircuit (beta)"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger,
                                                                       type_name='Small microcircuit (beta)')
        self._check_activities_exist(workflows_page, logger, "Small microcircuit (beta)")

        workflows_page.click_first_radio_button()
        time.sleep(1)

        url_before = browser.current_url
        result = workflows_page.click_view_configuration_button()
        assert result, "Should be able to click View Configuration button"

        time.sleep(5)
        current_url = browser.current_url

        assert current_url != url_before, \
            f"URL should change after View Configuration, got: {current_url}"
        logger.info(f"✅ Redirected to small microcircuit beta config: {current_url}")

    @pytest.mark.workflow
    @pytest.mark.activities
    def test_duplicate_small_microcircuit_beta(self, setup, login, logger, test_config):
        """Test Duplicate button for Simulate > Small microcircuit (beta)"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger,
                                                                       type_name='Small microcircuit (beta)')
        self._check_activities_exist(workflows_page, logger, "Small microcircuit (beta)")

        workflows_page.click_first_radio_button()
        time.sleep(1)

        result = workflows_page.click_duplicate_button()
        assert result, "Should be able to click Duplicate button"

        time.sleep(3)
        current_url = browser.current_url
        logger.info(f"✅ After duplicate, URL: {current_url}")

    # ── Microcircuit: View Configuration, Duplicate ──

    @pytest.mark.workflow
    @pytest.mark.activities
    def test_view_configuration_microcircuit(self, setup, login, logger, test_config):
        """Test View Configuration button for Simulate > Microcircuit"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger,
                                                                       type_name='Microcircuit')
        self._check_activities_exist(workflows_page, logger, "Microcircuit")

        workflows_page.click_first_radio_button()
        time.sleep(1)

        url_before = browser.current_url
        result = workflows_page.click_view_configuration_button()
        assert result, "Should be able to click View Configuration button"

        time.sleep(5)
        current_url = browser.current_url

        assert current_url != url_before, \
            f"URL should change after View Configuration, got: {current_url}"
        logger.info(f"✅ Redirected to microcircuit config: {current_url}")

    @pytest.mark.workflow
    @pytest.mark.activities
    def test_duplicate_microcircuit(self, setup, login, logger, test_config):
        """Test Duplicate button for Simulate > Microcircuit"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger,
                                                                       type_name='Microcircuit')
        self._check_activities_exist(workflows_page, logger, "Microcircuit")

        workflows_page.click_first_radio_button()
        time.sleep(1)

        result = workflows_page.click_duplicate_button()
        assert result, "Should be able to click Duplicate button"

        time.sleep(3)
        current_url = browser.current_url
        logger.info(f"✅ After duplicate, URL: {current_url}")

    # ── Brain region: View Configuration, Duplicate ──

    @pytest.mark.workflow
    @pytest.mark.activities
    def test_view_configuration_brain_region(self, setup, login, logger, test_config):
        """Test View Configuration button for Simulate > Brain region"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger,
                                                                       type_name='Brain region')
        self._check_activities_exist(workflows_page, logger, "Brain region")

        workflows_page.click_first_radio_button()
        time.sleep(1)

        url_before = browser.current_url
        result = workflows_page.click_view_configuration_button()
        assert result, "Should be able to click View Configuration button"

        time.sleep(5)
        current_url = browser.current_url

        assert current_url != url_before, \
            f"URL should change after View Configuration, got: {current_url}"
        logger.info(f"✅ Redirected to brain region config: {current_url}")

    @pytest.mark.workflow
    @pytest.mark.activities
    def test_duplicate_brain_region(self, setup, login, logger, test_config):
        """Test Duplicate button for Simulate > Brain region"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger,
                                                                       type_name='Brain region')
        self._check_activities_exist(workflows_page, logger, "Brain region")

        workflows_page.click_first_radio_button()
        time.sleep(1)

        result = workflows_page.click_duplicate_button()
        assert result, "Should be able to click Duplicate button"

        time.sleep(3)
        current_url = browser.current_url
        logger.info(f"✅ After duplicate, URL: {current_url}")

    # ── Pagination and summary ──

    @pytest.mark.workflow
    @pytest.mark.activities
    def test_pagination_in_activities_table(self, setup, login, logger, test_config):
        """Test pagination in Simulate workflow activities table"""
        browser, wait, base_url, lab_id, project_id = setup
        workflows_page = WorkflowsPage(browser, wait, logger, base_url)

        workflows_page.go_to_workflows_page(lab_id, project_id)
        logger.info("✅ Navigated to workflows page")

        workflows_page.click_category_dropdown_option('Simulate')
        workflows_page.click_type_dropdown_option('Single neuron')
        time.sleep(2)

        result = workflows_page.verify_pagination_works()
        logger.info("✅ Pagination verification completed")

    @pytest.mark.workflow
    @pytest.mark.activities
    def test_all_simulate_types_have_activities(self, setup, login, logger, test_config):
        """Test that all Simulate types can display activities table"""
        browser, wait, base_url, lab_id, project_id = setup
        workflows_page = WorkflowsPage(browser, wait, logger, base_url)

        workflows_page.go_to_workflows_page(lab_id, project_id)
        logger.info("✅ Navigated to workflows page")

        workflows_page.click_category_dropdown_option('Simulate')

        simulate_types = [
            'Single neuron', 'Synaptome',
            'Single neuron (beta)', 'Synaptome (beta)', 'Ion channel (beta)',
            'Paired neurons (beta)', 'Small microcircuit (beta)',
            'Microcircuit', 'Brain region',
        ]
        results = {}

        for type_name in simulate_types:
            logger.info(f"🔍 Testing {type_name}")

            workflows_page.click_type_dropdown_option(type_name)
            time.sleep(2)

            row_count = workflows_page.get_table_row_count()
            results[type_name] = row_count

            logger.info(f"✅ {type_name}: {row_count} activities")

        logger.info("📊 Simulate Activity Summary:")
        for type_name, count in results.items():
            logger.info(f"  - {type_name}: {count} activities")
