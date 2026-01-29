# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0


import time
from zoneinfo import ZoneInfo
from datetime import datetime

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

        time.sleep(900)
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

        # Step 6: Click on "Project" tab
        print("\n📍 Step 6: Clicking Project tab...")
        logger.info("Step 6: Clicking Project tab")
        project_clicked = build_synaptome.click_project_tab(logger)
        if project_clicked:
            print("✅ Project tab clicked successfully")
        else:
            print("ℹ️ Project tab not found, may already be on project models")

        # Step 7: Select a model by ticking a radio button
        print("\n📍 Step 7: Selecting model via radio button...")
        logger.info("Step 7: Selecting model via radio button")
        model_selected = build_synaptome.select_model_via_radio_button(logger)
        assert model_selected, "Failed to select model via radio button"

        # Step 8: Click on "Synapse sets" tab
        print("\n📍 Step 8: Clicking Synapse sets tab...")
        logger.info("Step 8: Clicking Synapse sets tab")
        synapse_sets_clicked = build_synaptome.click_synapse_sets_tab(logger)
        assert synapse_sets_clicked, "Failed to click Synapse sets tab"

        print("\n✅ Synaptome workflow test completed successfully")
        logger.info("Synaptome workflow test completed successfully")