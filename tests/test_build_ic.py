# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0


import time
from zoneinfo import ZoneInfo
from datetime import datetime
from selenium.webdriver.common.by import By

from pages.build_ic import BuildIcPage
from locators.build_ic_locators import BuildIcLocators


class TestBuildIc:

    def test_build_ion_channel(self, setup, login_direct_complete, logger, test_config):
        """Test the complete ion channel build workflow starting from project home"""
        browser, wait, base_url, lab_id, project_id = login_direct_complete
        
        print("\n🚀 Starting Build Ion Channel Test")
        logger.info("Starting Build Ion Channel Test")
        
        # Initialize page object with correct parameters
        build_ic = BuildIcPage(browser, wait, base_url, logger)
        
        # Step 1: Navigate to workflows page
        print("\n📍 Step 1: Navigating to workflows page...")
        logger.info("Step 1: Navigating to workflows page")
        workflows_url = build_ic.navigate_to_workflows(lab_id, project_id)
        assert "workflows" in workflows_url.lower(), "Failed to navigate to workflows page"
        print(f"✅ Successfully navigated to: {workflows_url}")
        logger.info(f"Successfully navigated to: {workflows_url}")

        # Step 2: Click Build button/section to get to build activities
        print("\n📍 Step 2: Clicking Build section...")
        logger.info("Step 2: Clicking Build section")
        build_clicked = build_ic.click_build_section(logger)
        assert build_clicked, "Failed to click Build section"

        # Step 3: Click on Ion channel card
        print("\n📍 Step 3: Clicking Ion channel card...")
        logger.info("Step 3: Clicking Ion channel card")
        ion_channel_clicked = build_ic.click_ion_channel_card(logger)
        assert ion_channel_clicked, "Failed to click Ion channel card"

        # Wait for the configuration form to load
        time.sleep(5)
        actual_url_after_click = browser.current_url
        logger.info(f"URL after clicking Ion channel card: {actual_url_after_click}")
        
        # Step 4: Click on Info tab (if needed)
        print("\n📍 Step 4: Clicking Info tab...")
        logger.info("Step 4: Clicking Info tab")
        try:
            info_clicked = build_ic.click_info_tab(logger)
            if info_clicked:
                print("✅ Info tab clicked")
        except Exception as e:
            logger.info(f"Info tab click not needed or failed: {e}")
            print("ℹ️ Info tab may already be selected")
        
        # Step 5: Fill in the Info form
        print("\n📍 Step 5: Filling Info form...")
        logger.info("Step 5: Filling Info form")
        
        # Generate unique name with current date/time
        zurich_tz = ZoneInfo('Europe/Zurich')
        current_time = datetime.now(zurich_tz)
        unique_name = current_time.strftime("%d.%m.%Y %H:%M:%S")
        dynamic_description = f"Automated ion channel test created on {unique_name} (Zurich time)"
        
        build_ic.fill_info_form(unique_name, dynamic_description, logger)
        print(f"✅ Info form filled with name: {unique_name}")

        # Step 6: Click on Initialization tab
        print("\n📍 Step 6: Clicking Initialization tab...")
        logger.info("Step 6: Clicking Initialization tab")
        init_clicked = build_ic.click_initialization_tab(logger)
        if init_clicked:
            print("✅ Initialization tab clicked")
        else:
            print("⚠️ Initialization tab not found, trying to proceed anyway")

        # Step 7: Click on "Click to select recording" button
        print("\n📍 Step 7: Clicking 'Click to select recording' button...")
        logger.info("Step 7: Clicking 'Click to select recording' button")
        try:
            select_recording_clicked = build_ic.click_ion_channel_recording_button(logger)
            if select_recording_clicked:
                print("✅ 'Click to select recording' button clicked")
        except Exception as e:
            logger.info(f"'Click to select recording' button not found or not needed: {e}")
            print(f"ℹ️ 'Click to select recording' button not found: {e}")

        # Step 8: Click on Public tab (if available)
        print("\n📍 Step 8: Checking for Public tab...")
        logger.info("Step 8: Checking for Public tab")
        try:
            public_clicked = build_ic.click_public_tab(logger)
            if public_clicked:
                print("✅ Public tab clicked successfully")
            else:
                print("ℹ️ Public tab not found")
        except Exception as e:
            logger.info(f"Public tab not available: {e}")
            print("ℹ️ Public tab not available")

        # Step 9: Select an ion channel recording via radio button
        print("\n📍 Step 9: Selecting ion channel recording via radio button...")
        logger.info("Step 9: Selecting ion channel recording via radio button")
        try:
            recording_selected = build_ic.select_model_via_radio_button(logger)
            if recording_selected:
                print("✅ Ion channel recording selected via radio button")
        except Exception as e:
            logger.error(f"Failed to select ion channel recording: {e}")
            print(f"❌ Failed to select ion channel recording: {e}")
            raise

        # Step 10: Click Select button in modal to confirm selection
        print("\n📍 Step 10: Clicking Select button to confirm recording selection...")
        logger.info("Step 10: Clicking Select button to confirm recording selection")
        try:
            select_clicked = build_ic.click_select_button_in_modal(logger)
            if select_clicked:
                print("✅ Select button clicked, recording confirmed")
        except Exception as e:
            logger.error(f"Failed to click Select button: {e}")
            print(f"❌ Failed to click Select button: {e}")
            build_ic.browser.save_screenshot("debug_select_button_not_found.png")
            raise

        # Step 11-14: Configure all 4 equation tabs (m∞, τm, h∞, τh)
        # Each tab needs to be clicked and then an equation selected from the middle column
        equation_tabs = [
            ("m∞", "m"),
            ("τm", "τ"),  
            ("h∞", "h"),
            ("τh", "τ")
        ]
        
        for i, (tab_name, tab_char) in enumerate(equation_tabs, start=11):
            print(f"\n📍 Step {i}: Configuring {tab_name} equation...")
            logger.info(f"Step {i}: Configuring {tab_name} equation")
            
            # Click the equation tab to expand it
            try:
                tab_clicked = build_ic.click_equation_tab(tab_name, logger)
                if tab_clicked:
                    print(f"✅ {tab_name} equation tab expanded")
                else:
                    print(f"⚠️ {tab_name} equation tab not found, skipping")
                    logger.info(f"{tab_name} equation tab not found, skipping")
                    continue
            except Exception as e:
                logger.error(f"Failed to click {tab_name} equation tab: {e}")
                print(f"❌ Failed to click {tab_name} equation tab: {e}")
                # Continue to next tab
                continue
            
            # Select an equation from the middle column (first available button)
            try:
                equation_selected = build_ic.select_first_equation_option(tab_name, logger)
                if equation_selected:
                    print(f"✅ {tab_name} equation selected")
                else:
                    print(f"⚠️ {tab_name} equation option not found, skipping")
                    logger.info(f"{tab_name} equation option not found, skipping")
            except Exception as e:
                logger.error(f"Failed to select {tab_name} equation: {e}")
                print(f"❌ Failed to select {tab_name} equation: {e}")
                # Continue to next tab

        # Step 15: Click Build model button (should now be enabled)
        print("\n📍 Step 15: Clicking Build model button...")
        logger.info("Step 15: Clicking Build model button")
        
        # Wait a bit for the Build button to become enabled
        time.sleep(5)
        
        try:
            build_model_clicked = build_ic.click_build_model_button(logger)
            if build_model_clicked:
                print("✅ Build model button clicked")
                # Wait for build to start
                time.sleep(5)
                logger.info(f"URL after clicking Build model: {browser.current_url}")
            else:
                print("⚠️ Build model button not found or not enabled")
                logger.info("Build model button not found or not enabled")
        except Exception as e:
            logger.error(f"Failed to click Build model button: {e}")
            print(f"⚠️ Build model button issue: {e}")
            # Take screenshot for debugging
            build_ic.browser.save_screenshot("debug_build_model_button.png")

        # Step 16: Verify URL redirect to output page
        print("\n📍 Step 16: Verifying URL redirect to output page...")
        logger.info("Step 16: Verifying URL redirect to output page")
        time.sleep(3)
        
        current_url = browser.current_url
        logger.info(f"Current URL: {current_url}")
        
        # Check if URL contains expected patterns
        url_checks = {
            'virtual-lab': 'virtual-lab' in current_url,
            'workflows/build/configure': 'workflows/build/configure' in current_url,
            'ion-channel-modeling-campaign': 'ion-channel-modeling-campaign' in current_url,
            'sessionId': 'sessionId=' in current_url,
            'panel=configuration': 'panel=configuration' in current_url or 'scope=public' in current_url
        }
        
        for check, result in url_checks.items():
            if result:
                print(f"  ✓ URL contains '{check}'")
                logger.info(f"URL check passed: {check}")
            else:
                print(f"  ✗ URL missing '{check}'")
                logger.info(f"URL check failed: {check}")

        # Step 17: Click Output tab
        print("\n📍 Step 17: Clicking Output tab...")
        logger.info("Step 17: Clicking Output tab")
        
        try:
            output_tab_clicked = build_ic.click_output_tab(logger)
            if output_tab_clicked:
                print("✅ Output tab clicked")
            else:
                print("⚠️ Output tab not found")
                logger.info("Output tab not found")
        except Exception as e:
            logger.error(f"Failed to click Output tab: {e}")
            print(f"⚠️ Output tab issue: {e}")

        # Step 18: Wait for build completion (done badge)
        print("\n📍 Step 18: Waiting for build to complete...")
        logger.info("Step 18: Waiting for build to complete")
        
        build_completed = build_ic.wait_for_build_completion(logger, timeout=120)
        assert build_completed, "Build should complete with 'done' status within timeout"
        logger.info("Build completed successfully")

        # Step 19: Verify output files are present
        logger.info("Step 19: Verifying output files")

        files_found = build_ic.verify_output_files_present(logger)
        assert files_found['outputs_section'], "Outputs section should be present"
        assert files_found['MOD'], "MOD output file should be present after build"
        assert files_found['PDF'] > 0, "At least one PDF output file should be present after build"
        logger.info(f"Output files — MOD: {files_found['MOD']}, PDFs: {files_found['PDF']}")

        # Step 20: Click MOD file and verify code preview
        mod_preview_ok = build_ic.click_mod_file_and_verify_preview(logger)
        assert mod_preview_ok, "MOD file preview should show NEURON code content"
        logger.info("MOD file preview verified")

        print(f"\n✅ Ion channel Info form filled successfully!")
        print(f"   Model Name: {unique_name}")
        print(f"   Description: {dynamic_description}")
        print(f"   Current URL: {browser.current_url}")
        
        logger.info(f"Ion channel Info form test completed successfully!")
        logger.info(f"Model Name: {unique_name}")
        logger.info(f"Current URL: {browser.current_url}")
        
        # Note: The remaining workflow (ion channel recording, M-model, E-model selection)
        # appears to be different from single neuron/synaptome workflows and requires
        # further investigation of the actual UI flow
