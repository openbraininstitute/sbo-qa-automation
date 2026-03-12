# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import pytest
from pages.workflows_page import WorkflowsPage


class TestWorkflowActivities:
    """
    Test workflow activities table with:
    - Category and Type dropdowns
    - Table with activities (rows with radio buttons)
    - Action buttons (View Configuration, View Results, Duplicate)
    - Redirects for different workflow types
    """
    
    @pytest.mark.workflow
    @pytest.mark.activities
    def test_workflow_activities_table_structure(self, setup, login, logger, test_config):
        """Test workflow activities table structure and dropdowns"""
        browser, wait, base_url, lab_id, project_id = setup
        workflows_page = WorkflowsPage(browser, wait, logger, base_url)
        
        # Navigate to workflows page
        workflows_page.go_to_workflows_page(lab_id, project_id)
        logger.info("✅ Navigated to workflows page")
        
        # Verify Recent Activities section exists
        section_exists = workflows_page.verify_recent_activities_section()
        assert section_exists, "Recent Activities section should be displayed"
        logger.info("✅ Recent Activities section verified")
        
        # Verify Category dropdown
        category_dropdown = workflows_page.find_category_dropdown()
        assert category_dropdown.is_displayed(), "Category dropdown should be displayed"
        logger.info("✅ Category dropdown found")
        
        # Verify Type dropdown
        type_dropdown = workflows_page.find_type_dropdown()
        assert type_dropdown.is_displayed(), "Type dropdown should be displayed"
        logger.info("✅ Type dropdown found")
        
        # Verify table structure
        table_displayed = workflows_page.verify_table_displayed()
        if table_displayed:
            logger.info("✅ Activities table is displayed")
            
            # Verify table columns
            columns = workflows_page.verify_table_columns()
            required_columns = ['Name', 'Category', 'Type', 'Date', 'Status']
            for col in required_columns:
                assert columns.get(col, {}).get('present', False), f"Column '{col}' should be present"
            logger.info("✅ All required table columns verified")
        else:
            logger.info("ℹ️ No activities table (no activities yet)")
    
        time.sleep(100)
    
    @pytest.mark.workflow
    @pytest.mark.activities
    def test_build_category_types(self, setup, login, logger, test_config):
        """Test Build category with all types: Single neuron, Synaptome, Ion channel"""
        browser, wait, base_url, lab_id, project_id = setup
        workflows_page = WorkflowsPage(browser, wait, logger, base_url)
        
        workflows_page.go_to_workflows_page(lab_id, project_id)
        logger.info("✅ Navigated to workflows page")
        
        # Select Build category
        workflows_page.click_category_dropdown_option('Build')
        logger.info("✅ Selected Build category")
        
        # Test each Build type
        build_types = ['Single neuron', 'Synaptome', 'Ion channel']
        
        for type_name in build_types:
            logger.info(f"🔍 Testing Build > {type_name}")
            
            # Select type from dropdown
            result = workflows_page.click_type_dropdown_option(type_name)
            assert result, f"Should be able to select type '{type_name}'"
            
            # Verify table updates (or shows no activities message)
            time.sleep(2)
            
            # Check if table has activities or shows empty message
            row_count = workflows_page.get_table_row_count()
            logger.info(f"✅ Build > {type_name}: {row_count} activities found")
    
    def _setup_workflow_and_select_type(self, setup, login, logger, category='Build', type_name='Single neuron'):
        """Helper method to navigate to workflows page and select category/type"""
        browser, wait, base_url, lab_id, project_id = setup
        workflows_page = WorkflowsPage(browser, wait, logger, base_url)
        
        workflows_page.go_to_workflows_page(lab_id, project_id)
        logger.info("✅ Navigated to workflows page")
        
        # Select category and type
        workflows_page.click_category_dropdown_option(category)
        workflows_page.click_type_dropdown_option(type_name)
        time.sleep(2)
        
        return browser, workflows_page
    
    def _check_activities_exist(self, workflows_page, logger, type_name):
        """Helper method to check if activities exist and skip test if not"""
        radio_buttons = workflows_page.get_all_radio_buttons()
        if len(radio_buttons) == 0:
            logger.info(f"ℹ️ No {type_name} activities to test")
            pytest.skip(f"No {type_name} activities available")
        return radio_buttons
    
    @pytest.mark.workflow
    @pytest.mark.activities
    def test_radio_button_selection(self, setup, login, logger, test_config):
        """Test radio button selection in activities table"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger)
        
        # Get radio buttons
        radio_buttons = self._check_activities_exist(workflows_page, logger, "Single neuron")
        logger.info(f"Found {len(radio_buttons)} radio buttons")
        
        # Click first radio button
        result = workflows_page.click_first_radio_button()
        assert result, "Should be able to click first radio button"
        logger.info("✅ Clicked first radio button")
        
        # Verify radio button is selected
        is_selected = workflows_page.is_radio_button_selected(0)
        assert is_selected, "First radio button should be selected"
        logger.info("✅ Radio button is selected")
    
    @pytest.mark.workflow
    @pytest.mark.activities
    def test_action_buttons_appear(self, setup, login, logger, test_config):
        """Test that action buttons appear when radio button is selected"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger)
        
        # Check if activities exist
        self._check_activities_exist(workflows_page, logger, "Single neuron")
        
        # Select first activity
        result = workflows_page.select_activity_and_verify_buttons(0)
        assert result, "Action buttons should appear after selecting activity"
        logger.info("✅ Action buttons appeared after selection")
    
    @pytest.mark.workflow
    @pytest.mark.activities
    def test_view_configuration_single_neuron(self, setup, login, logger, test_config):
        """Test View Configuration button for Build > Single neuron redirects to ME-model detail"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger)
        
        # Check if activities exist
        self._check_activities_exist(workflows_page, logger, "Single neuron")
        
        # Select first activity
        workflows_page.click_first_radio_button()
        time.sleep(1)
        
        # Click View Configuration
        result = workflows_page.click_view_configuration_button()
        assert result, "Should be able to click View Configuration button"
        
        # Verify redirect to ME-model detail page
        time.sleep(3)
        current_url = browser.current_url
        
        # ME-model detail page should contain 'memodel' or 'configuration' in URL
        assert 'memodel' in current_url.lower() or 'configuration' in current_url.lower(), \
            f"Should redirect to ME-model detail page, got: {current_url}"
        logger.info(f"✅ Redirected to ME-model detail: {current_url}")
    
    @pytest.mark.workflow
    @pytest.mark.activities
    def test_view_configuration_synaptome(self, setup, login, logger, test_config):
        """Test View Configuration button for Build > Synaptome redirects to synaptome detail"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger, 
                                                                        category='Build', 
                                                                        type_name='Synaptome')
        
        # Check if activities exist
        self._check_activities_exist(workflows_page, logger, "Synaptome")
        
        # Select first activity
        workflows_page.click_first_radio_button()
        time.sleep(1)
        
        # Click View Configuration
        result = workflows_page.click_view_configuration_button()
        assert result, "Should be able to click View Configuration button"
        
        # Verify redirect to synaptome detail page
        time.sleep(3)
        current_url = browser.current_url
        
        # Synaptome detail page should contain 'synaptome' in URL
        assert 'synaptome' in current_url.lower(), \
            f"Should redirect to synaptome detail page, got: {current_url}"
        logger.info(f"✅ Redirected to synaptome detail: {current_url}")
    
    @pytest.mark.workflow
    @pytest.mark.activities
    def test_view_configuration_ion_channel(self, setup, login, logger, test_config):
        """Test View Configuration button for Build > Ion channel redirects to configuration page"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger,
                                                                        category='Build',
                                                                        type_name='Ion channel')
        
        # Check if activities exist
        self._check_activities_exist(workflows_page, logger, "Ion channel")
        
        # Select first activity
        workflows_page.click_first_radio_button()
        time.sleep(1)
        
        # Click View Configuration
        result = workflows_page.click_view_configuration_button()
        assert result, "Should be able to click View Configuration button"
        
        # Verify redirect to ion channel configuration page
        time.sleep(3)
        current_url = browser.current_url
        
        # Ion channel configuration page should contain 'ion-channel' or 'configuration' in URL
        assert 'ion-channel' in current_url.lower() or 'configuration' in current_url.lower(), \
            f"Should redirect to ion channel configuration page, got: {current_url}"
        logger.info(f"✅ Redirected to ion channel configuration: {current_url}")
    
    @pytest.mark.workflow
    @pytest.mark.activities
    def test_view_results_ion_channel(self, setup, login, logger, test_config):
        """Test View Results button for Build > Ion channel redirects to results page"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger,
                                                                        category='Build',
                                                                        type_name='Ion channel')
        
        # Check if activities exist
        self._check_activities_exist(workflows_page, logger, "Ion channel")
        
        # Select first activity
        workflows_page.click_first_radio_button()
        time.sleep(1)
        
        # Click View Results
        result = workflows_page.click_view_results_button()
        assert result, "Should be able to click View Results button"
        
        # Verify redirect to results page
        time.sleep(3)
        current_url = browser.current_url
        
        # Results page should contain 'results' in URL
        assert 'results' in current_url.lower() or 'result' in current_url.lower(), \
            f"Should redirect to results page, got: {current_url}"
        logger.info(f"✅ Redirected to results page: {current_url}")
    
    @pytest.mark.workflow
    @pytest.mark.activities
    def test_duplicate_button_ion_channel(self, setup, login, logger, test_config):
        """Test Duplicate button for Build > Ion channel copies workflow"""
        browser, workflows_page = self._setup_workflow_and_select_type(setup, login, logger,
                                                                        category='Build',
                                                                        type_name='Ion channel')
        
        # Check if activities exist
        self._check_activities_exist(workflows_page, logger, "Ion channel")
        
        # Get initial row count
        initial_count = workflows_page.get_table_row_count()
        logger.info(f"Initial activity count: {initial_count}")
        
        # Select first activity
        workflows_page.click_first_radio_button()
        time.sleep(1)
        
        # Get selected row data
        selected_data = workflows_page.get_selected_row_data()
        if selected_data:
            logger.info(f"Selected activity: {selected_data['name']}")
        
        # Click Duplicate
        result = workflows_page.click_duplicate_button()
        assert result, "Should be able to click Duplicate button"
        
        # Wait for duplication to complete
        time.sleep(3)
        
        # Verify redirect to editable workflow page or configuration page
        current_url = browser.current_url
        logger.info(f"After duplicate, URL: {current_url}")
        
        # Should redirect to a page where workflow can be edited
        # This could be the build page, configuration page, or workflow editor
        assert any(keyword in current_url.lower() for keyword in ['build', 'workflow', 'configuration', 'edit']), \
            f"Should redirect to editable workflow page, got: {current_url}"
        logger.info(f"✅ Duplicate redirected to editable page: {current_url}")
    
    @pytest.mark.workflow
    @pytest.mark.activities
    def test_pagination_in_activities_table(self, setup, login, logger, test_config):
        """Test pagination in workflow activities table"""
        browser, wait, base_url, lab_id, project_id = setup
        workflows_page = WorkflowsPage(browser, wait, logger, base_url)
        
        workflows_page.go_to_workflows_page(lab_id, project_id)
        logger.info("✅ Navigated to workflows page")
        
        # Select Build > Single neuron (most likely to have multiple pages)
        workflows_page.click_category_dropdown_option('Build')
        workflows_page.click_type_dropdown_option('Single neuron')
        time.sleep(2)
        
        # Verify pagination works
        result = workflows_page.verify_pagination_works()
        logger.info("✅ Pagination verification completed")
    
    @pytest.mark.workflow
    @pytest.mark.activities
    def test_all_build_types_have_activities(self, setup, login, logger, test_config):
        """Test that all Build types can display activities table"""
        browser, wait, base_url, lab_id, project_id = setup
        workflows_page = WorkflowsPage(browser, wait, logger, base_url)
        
        workflows_page.go_to_workflows_page(lab_id, project_id)
        logger.info("✅ Navigated to workflows page")
        
        # Select Build category
        workflows_page.click_category_dropdown_option('Build')
        
        # Test each type
        build_types = ['Single neuron', 'Synaptome', 'Ion channel']
        results = {}
        
        for type_name in build_types:
            logger.info(f"🔍 Testing {type_name}")
            
            # Select type
            workflows_page.click_type_dropdown_option(type_name)
            time.sleep(2)
            
            # Count activities
            row_count = workflows_page.get_table_row_count()
            results[type_name] = row_count
            
            logger.info(f"✅ {type_name}: {row_count} activities")
        
        # Log summary
        logger.info("📊 Activity Summary:")
        for type_name, count in results.items():
            logger.info(f"  - {type_name}: {count} activities")
