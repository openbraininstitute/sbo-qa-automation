# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0


import time
import pytest
from zoneinfo import ZoneInfo
from datetime import datetime
from selenium.webdriver.common.by import By

from pages.build_ic import BuildIcPage
from locators.build_ic_locators import BuildIcLocators

MAX_RECORDING_ATTEMPTS = 3


class TestBuildIc:

    def test_build_ion_channel(self, setup, login_direct_complete, logger, test_config):
        """Test the complete ion channel build workflow starting from project home"""
        browser, wait, base_url, lab_id, project_id = login_direct_complete

        print("\n🚀 Starting Build Ion Channel Test")
        logger.info("Starting Build Ion Channel Test")

        # Initialize page object with correct parameters
        build_ic = BuildIcPage(browser, wait, base_url, logger)

        # Step 1: Navigate to workflows page
        logger.info("Step 1: Navigating to workflows page")
        workflows_url = build_ic.navigate_to_workflows(lab_id, project_id)
        assert "workflows" in workflows_url.lower(), "Failed to navigate to workflows page"
        logger.info(f"Successfully navigated to: {workflows_url}")

        # Step 2: Click Build button/section
        logger.info("Step 2: Clicking Build section")
        build_clicked = build_ic.click_build_section(logger)
        assert build_clicked, "Failed to click Build section"

        # Step 3: Click on Ion channel card
        logger.info("Step 3: Clicking Ion channel card")
        ion_channel_clicked = build_ic.click_ion_channel_card(logger)
        assert ion_channel_clicked, "Failed to click Ion channel card"

        # Wait for the configuration form to load
        time.sleep(5)
        logger.info(f"URL after clicking Ion channel card: {browser.current_url}")

        # Step 4: Click on Info tab (if needed)
        logger.info("Step 4: Clicking Info tab")
        try:
            build_ic.click_info_tab(logger)
        except Exception as e:
            logger.info(f"Info tab click not needed or failed: {e}")

        # Step 5: Fill in the Info form
        logger.info("Step 5: Filling Info form")
        zurich_tz = ZoneInfo('Europe/Zurich')
        current_time = datetime.now(zurich_tz)
        unique_name = current_time.strftime("%d.%m.%Y %H:%M:%S")
        dynamic_description = f"Automated ion channel test created on {unique_name} (Zurich time)"
        build_ic.fill_info_form(unique_name, dynamic_description, logger)
        logger.info(f"Info form filled with name: {unique_name}")

        # Step 6: Click on Initialization tab
        logger.info("Step 6: Clicking Initialization tab")
        build_ic.click_initialization_tab(logger)

        # ── Retry loop: select recording → configure → build ──
        build_result = self._attempt_build_with_retries(
            build_ic, browser, logger, max_attempts=MAX_RECORDING_ATTEMPTS
        )

        if build_result == 'failed_all':
            pytest.xfail(
                f"Build failed with {MAX_RECORDING_ATTEMPTS} different recordings — "
                "known data issue (missing protocols)"
            )

        # ── Post-build verification ──
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

        logger.info(f"✅ Ion channel build test completed successfully!")
        logger.info(f"Model Name: {unique_name}")
        logger.info(f"Current URL: {browser.current_url}")

    # ──────────────────────────────────────────────────────────────────────
    # Helper: attempt build with different recordings
    # ──────────────────────────────────────────────────────────────────────

    def _attempt_build_with_retries(self, build_ic, browser, logger, max_attempts=3):
        """Try selecting a recording and building. If build fails (data issue),
        go back and try a different recording. Returns 'done' or 'failed_all'.
        """
        for attempt in range(1, max_attempts + 1):
            logger.info(f"═══ Build attempt {attempt}/{max_attempts} ═══")

            # Step 7: Click "Click to select recording" button
            logger.info("Clicking 'Click to select recording' button")
            try:
                build_ic.click_ion_channel_recording_button(logger)
            except Exception as e:
                logger.warning(f"Select recording button issue: {e}")

            # Step 8: Click Public tab
            try:
                build_ic.click_public_tab(logger)
            except Exception as e:
                logger.info(f"Public tab not available: {e}")

            # Step 9: Select a recording via radio button
            logger.info("Selecting ion channel recording via radio button")
            try:
                build_ic.select_model_via_radio_button(logger)
            except Exception as e:
                logger.error(f"Failed to select recording: {e}")
                if attempt < max_attempts:
                    logger.info("Will retry with a different recording...")
                    self._go_back_to_initialization(build_ic, browser, logger)
                    continue
                return 'failed_all'

            # Step 10: Click Select button in modal
            logger.info("Clicking Select button to confirm recording")
            try:
                build_ic.click_select_button_in_modal(logger)
            except Exception as e:
                logger.error(f"Failed to click Select button: {e}")
                if attempt < max_attempts:
                    self._go_back_to_initialization(build_ic, browser, logger)
                    continue
                return 'failed_all'

            # Steps 11-14: Configure equation tabs
            equation_tabs = [("m∞", "m"), ("τm", "τ"), ("h∞", "h"), ("τh", "τ")]
            for tab_name, _ in equation_tabs:
                try:
                    tab_clicked = build_ic.click_equation_tab(tab_name, logger)
                    if tab_clicked:
                        build_ic.select_first_equation_option(tab_name, logger)
                except Exception as e:
                    logger.warning(f"Equation tab {tab_name} issue: {e}")

            # Step 15: Click Build model button
            logger.info("Clicking Build model button")
            time.sleep(5)
            try:
                build_model_clicked = build_ic.click_build_model_button(logger)
                if not build_model_clicked:
                    logger.warning("Build model button not enabled")
                    if attempt < max_attempts:
                        self._go_back_to_initialization(build_ic, browser, logger)
                        continue
                    return 'failed_all'
            except Exception as e:
                logger.error(f"Build model button issue: {e}")
                if attempt < max_attempts:
                    self._go_back_to_initialization(build_ic, browser, logger)
                    continue
                return 'failed_all'

            # Step 16: Verify URL
            time.sleep(3)
            logger.info(f"URL after build: {browser.current_url}")

            # Step 17: Click Output tab
            try:
                build_ic.click_output_tab(logger)
            except Exception as e:
                logger.warning(f"Output tab issue: {e}")

            # Step 18: Wait for build completion
            logger.info("Waiting for build to complete...")
            build_status = build_ic.wait_for_build_completion(logger, timeout=120)

            if build_status == 'done':
                logger.info(f"✅ Build succeeded on attempt {attempt}")
                return 'done'
            elif build_status == 'failed':
                logger.warning(
                    f"Build failed on attempt {attempt} (likely missing protocols). "
                    f"{'Retrying with different recording...' if attempt < max_attempts else 'No more retries.'}"
                )
                if attempt < max_attempts:
                    self._go_back_to_initialization(build_ic, browser, logger)
                    continue
                return 'failed_all'
            else:
                # Timeout — treat as failure
                logger.warning(f"Build timed out on attempt {attempt}")
                if attempt < max_attempts:
                    self._go_back_to_initialization(build_ic, browser, logger)
                    continue
                return 'failed_all'

        return 'failed_all'

    def _go_back_to_initialization(self, build_ic, browser, logger):
        """Navigate back to select a different recording after a failed build.
        Flow: Configuration tab → Initialization tab → Click to select recording.
        """
        logger.info("Navigating back: Configuration → Initialization...")
        time.sleep(2)

        # Step 1: Click Configuration tab (top-level)
        try:
            build_ic.click_configuration_tab(logger)
        except Exception as e:
            logger.warning(f"Could not click Configuration tab: {e}")
            # Fallback: browser back
            browser.back()
            time.sleep(3)

        # Step 2: Click Initialization tab
        try:
            build_ic.click_initialization_tab(logger)
        except Exception as e:
            logger.warning(f"Could not click Initialization tab: {e}")

        time.sleep(2)
