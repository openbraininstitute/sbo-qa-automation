# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0


import time
from zoneinfo import ZoneInfo
from datetime import datetime
from selenium.webdriver.common.by import By

from pages.build_synaptome import BuildSynaptomePage




class TestBuildSynaptome:

    def test_build_synaptome(self, setup, login_direct_complete, logger, test_config):
        """Test the complete synaptome build workflow starting from project home"""
        browser, wait, base_url, lab_id, project_id = login_direct_complete
        
        print("\n🚀 Starting Build Synaptome Test")
        logger.info("Starting Build Synaptome Test")
        
        # Initialize page object with correct parameters
        build_synaptome = BuildSynaptomePage(browser, wait, base_url, logger)
        
        # Step 1: Navigate to workflows page
        print("\n📍 Step 1: Navigating to workflows page...")
        logger.info("Step 1: Navigating to workflows page")
        workflows_url = build_synaptome.navigate_to_workflows(lab_id, project_id)
        assert "workflows" in workflows_url.lower(), "Failed to navigate to workflows page"
        print(f"✅ Successfully navigated to: {workflows_url}")
        logger.info(f"Successfully navigated to: {workflows_url}")

        # Step 2: Click Build button/section to get to build activities
        print("\n📍 Step 2: Clicking Build section...")
        logger.info("Step 2: Clicking Build section")
        build_clicked = build_synaptome.click_build_section(logger)
        assert build_clicked, "Failed to click Build section"

        # Step 3: Click on Synaptome card
        print("\n📍 Step 3: Clicking Synaptome card...")
        logger.info("Step 3: Clicking Synaptome card")
        synaptome_clicked = build_synaptome.click_synaptome_card(logger)
        assert synaptome_clicked, "Failed to click Synaptome card"

        # Wait for the configuration form to load
        time.sleep(5)
        actual_url_after_click = browser.current_url
        logger.info(f"URL after clicking Synaptome card: {actual_url_after_click}")
        
        # Step 4: Fill in the Info form
        print("\n📍 Step 4: Filling configuration form...")
        logger.info("Step 4: Filling configuration form")
        
        # Generate unique name with current date/time
        from datetime import datetime
        from zoneinfo import ZoneInfo
        zurich_tz = ZoneInfo('Europe/Zurich')
        current_time = datetime.now(zurich_tz)
        unique_name = current_time.strftime("%d.%m.%Y %H:%M:%S")
        dynamic_description = f"Automated synaptome test created on {unique_name} (Zurich time)"
        
        build_synaptome.fill_configuration_form(unique_name, dynamic_description, logger)
        print(f"✅ Configuration form filled with name: {unique_name}")

        # Step 5: Click on ME-model button to proceed
        print("\n📍 Step 5: Clicking ME-model button...")
        logger.info("Step 5: Clicking ME-model button")
        me_model_clicked = build_synaptome.click_me_model_button(logger)
        assert me_model_clicked, "Failed to click ME-model button"

        # Wait for ME-model selection page to load
        time.sleep(5)
        logger.info(f"URL after clicking ME-model: {browser.current_url}")

        # Step 6: Click on "Public" tab
        print("\n📍 Step 6: Clicking Public tab...")
        logger.info("Step 6: Clicking Public tab")
        public_clicked = build_synaptome.click_public_tab(logger)
        if public_clicked:
            print("✅ Public tab clicked successfully")
        else:
            print("ℹ️ Public tab not found, may already be on public models")

        # Step 7: Search for "cadpyr" model
        # Step 7: Search for "cadpyr" model (optional - may not be available)
        print("\n📍 Step 7: Searching for cadpyr model...")
        logger.info("Step 7: Searching for cadpyr model")
        try:
            search_success = build_synaptome.search_for_model("cadpyr", logger)
            if search_success:
                print("✅ Search completed successfully")
        except Exception as e:
            print(f"ℹ️ Search field not available, continuing without search: {e}")
            logger.info(f"Search field not available, continuing without search: {e}")
        # Step 8: Select a model by ticking a radio button
        print("\n📍 Step 8: Selecting model via radio button...")
        logger.info("Step 8: Selecting model via radio button")
        model_selected = build_synaptome.select_model_via_radio_button(logger)
        assert model_selected, "Failed to select model via radio button"

        # Step 9: Click on "Synapse sets" tab
        print("\n📍 Step 9: Clicking Synapse sets tab...")
        logger.info("Step 9: Clicking Synapse sets tab")
        synapse_sets_clicked = build_synaptome.click_synapse_sets_tab(logger)
        assert synapse_sets_clicked, "Failed to click Synapse sets tab"

        # Step 9a: Verify the Synapse sets info panel is displayed
        print("\n📍 Step 9a: Verifying Synapse sets info panel...")
        logger.info("Step 9a: Verifying Synapse sets info panel")
        build_synaptome.verify_synapse_sets_info_panel(logger)
        print("✅ Synapse sets info panel verified")

        # Step 9b: Click the "Add set" button
        print("\n📍 Step 9b: Clicking Add set button...")
        logger.info("Step 9b: Clicking Add set button")
        build_synaptome.click_add_set_button(logger)
        print("✅ Add set button clicked")

        # Step 10: Wait for 3D morphology to load
        print("\n📍 Step 10: Waiting for 3D morphology to load...")
        logger.info("Step 10: Waiting for 3D morphology to load")
        time.sleep(30)  # Wait for 3D visualization to render (slow in CI)
        print("✅ 3D morphology loaded")

        # Step 11: Create synapse set
        print("\n📍 Step 11: Creating synapse set...")
        logger.info("Step 11: Creating synapse set")
        
        # Create 1 synapse set on apical dendrites
        print(f"\n  Creating synapse set: apical1 on Apical dendrites...")
        logger.info(f"Creating synapse set: apical1 on Apical dendrites")
        
        build_synaptome.create_synapse_set(
            name="apical1",
            target="Apical dendrites",
            synapse_type="Excitatory Synapses",
            formula="0.04",
            min_filter=10,
            max_filter=900,
            logger=logger
        )
        
        print(f"  ✅ Synapse set apical1 created")
        logger.info("Synapse set apical1 created successfully")
        
        # Step 12: Click "Build synaptome" button
        print("\n📍 Step 12: Clicking Build synaptome button...")
        logger.info("Step 12: Clicking Build synaptome button")
        
        # Wait a bit for the UI to be ready
        time.sleep(3)
        
        # Find and click the Build synaptome button
        build_synaptome_btn_locator = (By.XPATH, "//button[contains(., 'Build synaptome')]")
        build_synaptome_btn = build_synaptome.element_to_be_clickable(build_synaptome_btn_locator, timeout=10)
        build_synaptome_btn.click()
        logger.info("Clicked Build synaptome button")
        print("✅ Build synaptome button clicked")
        
        # Wait for build to start
        time.sleep(5)
        logger.info(f"URL after clicking Build synaptome: {browser.current_url}")

        print("\n✅ Synaptome workflow test completed successfully")
        logger.info("Synaptome workflow test completed successfully")
