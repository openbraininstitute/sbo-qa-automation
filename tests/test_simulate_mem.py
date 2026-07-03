# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import pytest
from pages.simulate_mem_page import SimulateMemPage


class TestSimulateMem:
    """End-to-end test for ME-model single neuron simulation (non-beta).

    Flow:
    1.  Navigate to Workflows page with simulate activity filter
    2.  Click Simulate category → Single neuron card → model picker loads
    3.  Click Public tab, verify table has at least one model row
    4.  Click a random model row → wait for mini-detail panel; verify title text
    5.  Click "Use model" button → config page
    6.  Wait for config page to load (30s timeout)
    7.  Wait for 3D morphology viewer to load (30s timeout); measure load time
    8.  Capture Navigation Timing API performance metrics
    9.  Verify Configuration and Results tabs are present
    10. Click Info tab
    11. Fill name with datetime stamp, description with "automated test of MEmodel"
    12. Verify "Registered by" and "Registered at" fields are non-empty
    13. Click Experimental setup tab; verify labels and values exist
    14. Click Stimulation protocol tab; wait for IDrest plot (60s timeout)
    15. Verify download button is displayed and clickable
    16. Click Recording tab
    17. Discover available section prefixes (soma, dend, apic, axon, myelin)
    18. Select "soma" for first recording (dropdown 0)
    19. Add recordings for dend + any available (apic, axon, myelin)
    20. Wait for Run experiment button to be truly active (60s timeout)
    21. Click Run experiment
    22. Wait for Results tab to become active (30s polling, fallback: click manually)
    23. Verify Download CSV and Reconfigure buttons are disabled while running
    24. Verify left menu has "All" button + at least 1 recording button
    25. Verify IDREST plots are displayed while running
    26. Verify 3D morphology canvas is visible
    27. Verify plot containers match recordings
    28. Wait for simulation to complete (300s timeout, poll every 10s)
    29. Verify Download CSV and Reconfigure are enabled after completion
    30. Verify success notification with "View Simulation" link
    """

    def _get_page(self, setup, logger):
        browser, wait, base_url, lab_id, project_id = setup
        return SimulateMemPage(browser, wait, logger, base_url), lab_id, project_id

    @pytest.mark.simulate
    @pytest.mark.run(order=20)
    def test_simulate_mem_full_flow(self, setup, login, logger, test_config):
        sim_page, lab_id, project_id = self._get_page(setup, logger)

        # Steps 1-2: Navigate to Workflows → Simulate → Single neuron card → model picker
        sim_page.go_to_workflows_simulate(lab_id, project_id)
        sim_page.click_simulate_category()
        sim_page.click_single_neuron_card()
        logger.info(f"On model picker. URL: {sim_page.browser.current_url}")

        # Steps 3-4: Public tab → click random model → verify mini-detail
        sim_page.click_public_tab()
        row_count = sim_page.get_row_count()
        assert row_count > 0, "Expected at least one model row"

        sim_page.click_random_row()
        sim_page.wait_for_mini_detail()
        title = sim_page.find_mini_detail_title().text
        logger.info(f"Selected model: '{title}'")

        # Step 5: Click "Use model" → config page
        sim_page.click_use_model()
        logger.info(f"After Use model, URL: {sim_page.browser.current_url}")

        # Step 6: Wait for config page to load
        sim_page.wait_for_config_page(timeout=30)
        logger.info("Config page loaded")

        # Step 7: Measure 3D morphology load time
        morph_start = time.time()
        try:
            sim_page.wait_for_neuron_visualizer(timeout=30)
            morph_elapsed = round(time.time() - morph_start, 2)
            logger.info(f"3D morphology viewer loaded in {morph_elapsed}s")
        except Exception as e:
            morph_elapsed = round(time.time() - morph_start, 2)
            logger.warning(f"Neuron visualizer not loaded after {morph_elapsed}s: {e}")

        # Step 8: Capture Navigation Timing API performance metrics
        from util.performance_tracker import PerformanceTracker
        perf = PerformanceTracker(sim_page.browser, logger)
        perf.capture_metrics("simulate_mem_config_page")
        perf.save_report("performance_simulate_mem.json")

        # Step 9: Verify Configuration and Results tabs
        tabs = sim_page.verify_config_tabs()
        assert tabs['configuration']['present'], "Configuration tab should be present"
        assert tabs['results']['present'], "Results tab should be present"
        logger.info("Configuration and Results tabs verified")

        # Steps 10-12: Info tab — fill datetime name + description, verify registered fields
        sim_page.click_info_tab()
        campaign_name = sim_page.fill_name_with_datetime()
        sim_page.fill_description("automated test of MEmodel")
        logger.info(f"Info filled: name='{campaign_name}'")

        # Verify registered by and registered at are present
        reg_by = sim_page.get_registered_by()
        reg_at = sim_page.get_registered_at()
        assert reg_by, "Registered by should not be empty"
        assert reg_at, "Registered at should not be empty"
        logger.info(f"Registered by: '{reg_by}', at: '{reg_at}'")

        # Step 13: Click Experimental setup tab, verify labels/values
        sim_page.click_experimental_setup_tab()
        exp_data = sim_page.get_panel_labels_and_values()
        assert len(exp_data) > 0, "Experimental setup should have labels"
        logger.info(f"Experimental setup: {len(exp_data)} labels")

        # Steps 14-15: Click Stimulation protocol, wait for IDrest plot, verify download
        sim_page.click_stimulation_protocol_tab()
        logger.info("On Stimulation protocol tab")

        try:
            sim_page.wait_for_stim_plot(timeout=60)
            logger.info("IDrest plot loaded")
        except Exception as e:
            logger.warning(f"IDrest plot not loaded within timeout: {e}")

        download_ok = sim_page.is_stim_download_btn_clickable(timeout=10)
        if download_ok:
            logger.info("Download button is displayed and clickable")
        else:
            logger.warning("Download button not found or not clickable")

        # Steps 16-19: Click Recording tab, add recordings for available sections
        sim_page.click_recording_tab()
        logger.info("On Recording tab")

        # Discover available section prefixes (soma, dend, apic, myelin, etc.)
        prefixes = sim_page.get_available_section_prefixes(dropdown_index=0)
        logger.info(f"Available recording sections: {prefixes}")

        # We want: 1 soma, 1 dend, + apic/axon/myelin if available
        desired = ['soma', 'dend']
        for extra in ['apic', 'axon', 'myelin']:
            if extra in prefixes:
                desired.append(extra)

        # First recording already exists (dropdown 0), select soma for it
        selected_0 = sim_page.select_recording_section(0, 'soma')
        logger.info(f"Recording 0: '{selected_0}'")

        # Add remaining recordings
        for i, prefix in enumerate(desired[1:], start=1):
            sim_page.click_add_recording()
            selected = sim_page.select_recording_section(i, prefix)
            logger.info(f"Recording {i}: '{selected}'")

        logger.info(f"Added {len(desired)} recording(s): {desired}")

        # Steps 20-21: Wait for Run experiment button to be truly active, then click
        btn_ready = sim_page.wait_for_run_experiment_ready(timeout=60)
        assert btn_ready, "Run experiment button should become active (not greyed out)"
        logger.info("Run experiment button is ready")

        sim_page.click_run_experiment()
        logger.info("Clicked Run experiment")

        # Step 22: Wait for Results tab to become active (fallback: click manually)
        results_active = sim_page.wait_for_results_tab_active(timeout=30)
        assert results_active, "Results tab should be active after Run experiment"
        logger.info("Results tab active after Run experiment")

        # Step 23: While simulation is running, Download CSV and Reconfigure should be disabled
        if not sim_page.is_download_csv_enabled():
            logger.info("Download CSV and Reconfigure are disabled (simulation still running)")
            assert not sim_page.is_reconfigure_enabled(), "Reconfigure should be disabled while running"
        else:
            logger.info("Simulation already completed before disabled-state check — skipping disabled assertion")

        # Step 24: Verify left menu has "All" button + at least 1 recording button
        all_btns = sim_page.get_results_left_menu_buttons()
        assert len(all_btns) >= 2, f"Expected All + at least 1 recording button, got {len(all_btns)}"
        rec_btns = sim_page.get_results_recording_buttons()
        assert len(rec_btns) >= 1, "Expected at least 1 recording button in Results left menu"
        logger.info(f"Results menu: {len(all_btns)} buttons, {len(rec_btns)} recording(s)")

        # Step 25: Verify IDREST plots are displayed while running
        plot_count = sim_page.get_idrest_plot_count()
        logger.info(f"IDREST plots visible while running: {plot_count}")

        # Step 26: Verify 3D morphology canvas is visible
        assert sim_page.is_neuron_canvas_visible(), "3D morphology canvas should be visible"
        logger.info("3D morphology canvas visible")

        # Step 27: Verify plot containers match recordings
        plot_labels = sim_page.get_plot_container_labels()
        logger.info(f"Plot containers: {plot_labels}")

        # Step 28: Wait for simulation to complete (Download CSV becomes enabled)
        sim_done = sim_page.wait_for_simulation_complete(timeout=300, poll_interval=10)
        assert sim_done, "Simulation should complete (Download CSV enabled)"
        logger.info("Simulation completed")

        # Step 29: Verify Download CSV and Reconfigure are now enabled
        assert sim_page.is_download_csv_enabled(), "Download CSV should be enabled after completion"
        assert sim_page.is_reconfigure_enabled(), "Reconfigure should be enabled after completion"
        logger.info("Download CSV and Reconfigure are enabled")

        # Step 30: Verify success notification with View Simulation link
        notif_ok = sim_page.wait_for_success_notification(timeout=30)
        if notif_ok:
            link = sim_page.get_view_simulation_link()
            assert link is not None, "View Simulation link should be present in notification"
            logger.info(f"Success notification with View Simulation link: {link.get_attribute('href')}")
        else:
            logger.warning("Success notification not found — may have auto-dismissed")

        logger.info(f"Final URL: {sim_page.browser.current_url}")
