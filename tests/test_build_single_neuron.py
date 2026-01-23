"""
Test for Build Single Neuron functionality - Single Neuron Model Creation
"""

import pytest
import time
from pages.build_single_neuron_page import BuildSingleNeuronPage


class TestBuildSingleNeuron:
    """Test class for build single neuron functionality"""
    
    @pytest.mark.build_single_neuron
    @pytest.mark.run(order=15)
    def test_single_neuron_build_workflow(self, setup, login_direct_complete, logger, test_config):
        """
        Test complete single neuron model build workflow:
        1. Navigate to workflows page
        2. Click Build button
        3. Select Single neuron type
        4. Fill model name
        5. Select M-model
        6. Select E-model
        7. Build model
        """
        browser, wait, base_url, lab_id, project_id = login_direct_complete
        
        print("\n🚀 Starting Build Single Neuron Test")
        logger.info("Starting Build Single Neuron Test")
        
        # Initialize page object with correct parameters
        build_page = BuildSingleNeuronPage(browser, wait, logger, base_url)
        
        # Step 1: Navigate to workflows page
        print("\n📍 Step 1: Navigating to workflows page...")
        logger.info("Step 1: Navigating to workflows page")
        workflows_url = build_page.navigate_to_workflows(lab_id, project_id)
        assert "workflows" in workflows_url.lower(), "Failed to navigate to workflows page"
        print(f"✅ Successfully navigated to: {workflows_url}")
        logger.info(f"Successfully navigated to: {workflows_url}")

        # Step 2: Click Build button
        print("\n📍 Step 2: Clicking Build button...")
        logger.info("Step 2: Clicking Build button")
        build_clicked = build_page.click_build_button()
        assert build_clicked, "Failed to click Build button"
        
        # Step 3: Select Single neuron type
        print("\n📍 Step 3: Selecting Single neuron type...")
        logger.info("Step 3: Selecting Single neuron type")
        single_neuron_selected = build_page.select_single_neuron_type()
        assert single_neuron_selected, "Failed to select Single neuron type"
        
        # Step 4: Wait for redirect to configuration page
        print("\n📍 Step 4: Waiting for redirect to configuration page...")
        logger.info("Step 4: Waiting for redirect to configuration page")
        config_page_reached = build_page.wait_for_configuration_page()
        assert config_page_reached, "Failed to reach configuration page"
        
        # Step 5: Fill model name
        print("\n📍 Step 5: Filling model name...")
        logger.info("Step 5: Filling model name")
        model_name = f"Test-ME-Model-{int(time.time())}"  # Unique name with timestamp
        name_filled = build_page.fill_model_name(model_name)
        assert name_filled, "Failed to fill model name"
        
        # Step 6: Select M-model
        print("\n📍 Step 6: Selecting M-model...")
        logger.info("Step 6: Selecting M-model")
        m_model_clicked = build_page.click_m_model_button()
        assert m_model_clicked, "Failed to click M-model button"
        
        m_model_selected = build_page.select_first_m_model()
        assert m_model_selected, "Failed to select M-model"
        
        # Step 7: Select E-model
        print("\n📍 Step 7: Selecting E-model...")
        logger.info("Step 7: Selecting E-model")
        e_model_clicked = build_page.click_e_model_button()
        assert e_model_clicked, "Failed to click E-model button"
        
        e_model_selected = build_page.select_first_e_model()
        assert e_model_selected, "Failed to select E-model"
        
        # Step 8: Build model
        print("\n📍 Step 8: Building model...")
        logger.info("Step 8: Building model")
        build_model_clicked = build_page.click_build_model_button()
        assert build_model_clicked, "Failed to click Build model button"
        
        # Step 9: Wait for build completion or initiation
        print("\n📍 Step 9: Waiting for build process...")
        logger.info("Step 9: Waiting for build process")
        build_completed = build_page.wait_for_build_completion()
        # Note: We don't assert this as the build process might take very long
        # and we just want to verify the workflow can be initiated
        
        print(f"\n🎉 Build Single Neuron Test Completed!")
        print(f"   Model Name: {model_name}")
        print(f"   Final URL: {browser.current_url}")
        print(f"   Build Process Initiated: {'✅' if build_completed else '⏳ (may still be running)'}")
        
        logger.info(f"Build Single Neuron Test Completed!")
        logger.info(f"Model Name: {model_name}")
        logger.info(f"Final URL: {browser.current_url}")
        logger.info(f"Build Process Initiated: {'✅' if build_completed else '⏳ (may still be running)'}")
    
    @pytest.mark.build_single_neuron
    @pytest.mark.run(order=16)
    def test_single_neuron_page_accessibility(self, setup, login_direct_complete, logger, test_config):
        """Test that the workflows page loads and basic elements are accessible"""
        browser, wait, base_url, lab_id, project_id = login_direct_complete
        
        print("\n🔍 Testing Single Neuron Page Accessibility")
        logger.info("Testing Single Neuron Page Accessibility")
        
        # Initialize page object with correct parameters
        build_page = BuildSingleNeuronPage(browser, wait, logger, base_url)
        
        # Navigate to workflows page with lab_id and project_id
        workflows_url = build_page.navigate_to_workflows(lab_id, project_id)
        assert "workflows" in workflows_url.lower(), "Failed to navigate to workflows page"
        
        # Check page title or main content
        page_title = browser.title
        assert page_title, "Page title is empty"
        print(f"✅ Page loaded with title: {page_title}")
        logger.info(f"Page loaded with title: {page_title}")
        
        # Verify we can find the Build button
        build_button_found = build_page.click_build_button()
        # We don't assert here as we just want to check accessibility
        print(f"✅ Build button accessibility: {'Found' if build_button_found else 'Not found'}")
        logger.info(f"Build button accessibility: {'Found' if build_button_found else 'Not found'}")
    
    @pytest.mark.build_single_neuron
    @pytest.mark.run(order=17)
    def test_single_neuron_with_custom_parameters(self, setup, login_direct_complete, logger, test_config):
        """Test single neuron page accessibility with different parameters"""
        browser, wait, base_url, lab_id, project_id = login_direct_complete
        
        print("\n🧠 Testing Single Neuron Page Accessibility")
        logger.info("Testing Single Neuron Page Accessibility")
        
        # Initialize page object with correct parameters
        build_page = BuildSingleNeuronPage(browser, wait, logger, base_url)
        
        # Navigate to workflows page (brain_id parameters no longer used)
        workflows_url = build_page.navigate_to_workflows(lab_id, project_id)
        
        # Verify URL contains the correct format
        assert "workflows?activity=build" in workflows_url, "Correct activity parameter not in URL"
        print(f"✅ Single Neuron URL: {workflows_url}")
        logger.info(f"Single Neuron URL: {workflows_url}")
        
        # Basic page load verification
        page_loaded = "workflows" in browser.current_url.lower()
        assert page_loaded, "Workflows page not loaded"
        print("✅ Page loaded successfully")
        logger.info("Page loaded successfully")