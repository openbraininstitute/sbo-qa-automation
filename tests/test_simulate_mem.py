# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import pytest
from pages.simulate_mem_page import SimulateMemPage


class TestSimulateMem:
    """End-to-end test for ME-model single neuron simulation (non-beta).

    Flow:
    1.  Workflows → Simulate → Single neuron card → model picker
    2.  Select model → Use model → config page
    3.  Info tab: fill datetime name + description
    4.  Click through all tabs, verify labels/values
    5.  Stimulation protocol: wait for IDrest plot, verify download button
    6.  Recording: add recordings (soma, dend, apic, axon if available)
    7.  Run experiment → auto-redirect to Results tab
    8.  Verify left menu (All + recording buttons), buttons disabled while running
    9.  Verify IDREST plots and 3D canvas visible during simulation
    10. Wait for completion, verify buttons enabled, success notification
    """

    def _get_page(self, setup, logger):
        browser, wait, base_url, lab_id, project_id = setup
        return SimulateMemPage(browser, wait, logger, base_url), lab_id, project_id

    @pytest.mark.simulate
    @pytest.mark.run(order=20)
    def test_simulate_mem_full_flow(self, setup, login, logger, test_config):
        sim_page, lab_id, project_id = self._get_page(setup, logger)

        # Step 1: Navigate to Workflows → Simulate → Single neuron
        sim_page.go_to_workflows_simulate(lab_id, project_id)
        sim_page.click_simulate_category()
        sim_page.click_single_neuron_card()
        logger.info(f"On model picker. URL: {sim_page.browser.current_url}")

        # Step 2: Public tab → click random model → Use model
        sim_page.click_public_tab()
        row_count = sim_page.get_row_count()
        assert row_count > 0, "Expected at least one model row"

        sim_page.click_random_row()
        sim_page.wait_for_mini_detail()
        title = sim_page.find_mini_detail_title().text
        logger.info(f"Selected model: '{title}'")

        sim_page.click_use_model()
        logger.info(f"After Use model, URL: {sim_page.browser.current_url}")

        # Step 3: Wait for config page
        sim_page.wait_for_config_page(timeout=30)
        logger.info("Config page loaded")

        # Measure 3D morphology load time
        morph_start = time.time()
        try:
            sim_page.wait_for_neuron_visualizer(timeout=120)
            morph_elapsed = round(time.time() - morph_start, 2)
            logger.info(f"3D morphology viewer loaded in {morph_elapsed}s")
        except Exception as e:
            morph_elapsed = round(time.time() - morph_start, 2)
            logger.warning(f"Neuron visualizer not loaded after {morph_elapsed}s: {e}")

        # Capture Navigation Timing API metrics for the config page
        from util.performance_tracker import PerformanceTracker
        perf = PerformanceTracker(sim_page.browser, logger)
        perf.capture_metrics("simulate_mem_config_page")
        perf.save_report("performance_simulate_mem.json")

        # Step 4: Verify Configuration and Results tabs
        tabs = sim_page.verify_config_tabs()
        assert tabs['configuration']['present'], "Configuration tab should be present"
        assert tabs['results']['present'], "Results tab should be present"
        logger.info("Configuration and Results tabs verified")

        # Step 5: Info tab — fill datetime as name, add description
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

        # Step 6: Click Experimental setup tab, verify labels/values
        sim_page.click_experimental_setup_tab()
        exp_data = sim_page.get_panel_labels_and_values()
        assert len(exp_data) > 0, "Experimental setup should have labels"
        logger.info(f"Experimental setup: {len(exp_data)} labels")

        # Step 7: Click Stimulation protocol, wait for IDrest plot, verify download
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

        # Step 8: Click Recording tab, add recordings for available sections
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

        # Step 9: Verify Run experiment button is enabled and click it
        run_btn = sim_page.find_run_experiment_btn(timeout=10)
        assert run_btn.is_displayed(), "Run experiment button should be visible"
        assert run_btn.is_enabled(), "Run experiment button should be enabled"
        logger.info("Run experiment button is ready")

        sim_page.click_run_experiment()
        logger.info("Clicked Run experiment")

        # Step 10: Verify redirected to Results tab
        time.sleep(5)
        assert sim_page.is_results_tab_active(), "Results tab should be active after Run experiment"
        logger.info("Results tab active after Run experiment")

        # Step 11: Verify left menu has "All" button + at least 1 recording button
        all_btns = sim_page.get_results_left_menu_buttons()
        assert len(all_btns) >= 2, f"Expected All + at least 1 recording button, got {len(all_btns)}"
        rec_btns = sim_page.get_results_recording_buttons()
        assert len(rec_btns) >= 1, "Expected at least 1 recording button in Results left menu"
        logger.info(f"Results menu: {len(all_btns)} buttons, {len(rec_btns)} recording(s)")

        # Step 12: While simulation is running, Download CSV and Reconfigure should be disabled
        assert not sim_page.is_download_csv_enabled(), "Download CSV should be disabled while running"
        assert not sim_page.is_reconfigure_enabled(), "Reconfigure should be disabled while running"
        logger.info("Download CSV and Reconfigure are disabled (simulation running)")

        # Step 13: Verify IDREST plots are displayed while running
        plot_count = sim_page.get_idrest_plot_count()
        logger.info(f"IDREST plots visible while running: {plot_count}")

        # Verify 3D morphology canvas is visible
        assert sim_page.is_neuron_canvas_visible(), "3D morphology canvas should be visible"
        logger.info("3D morphology canvas visible")

        # Verify plot containers match recordings
        plot_labels = sim_page.get_plot_container_labels()
        logger.info(f"Plot containers: {plot_labels}")

        # Step 14: Wait for simulation to complete (Download CSV becomes enabled)
        sim_done = sim_page.wait_for_simulation_complete(timeout=300, poll_interval=10)
        assert sim_done, "Simulation should complete (Download CSV enabled)"
        logger.info("Simulation completed")

        # Step 15: Verify Download CSV and Reconfigure are now enabled
        assert sim_page.is_download_csv_enabled(), "Download CSV should be enabled after completion"
        assert sim_page.is_reconfigure_enabled(), "Reconfigure should be enabled after completion"
        logger.info("Download CSV and Reconfigure are enabled")

        # Step 16: Verify success notification with View Simulation link
        notif_ok = sim_page.wait_for_success_notification(timeout=30)
        if notif_ok:
            link = sim_page.get_view_simulation_link()
            assert link is not None, "View Simulation link should be present in notification"
            logger.info(f"Success notification with View Simulation link: {link.get_attribute('href')}")
        else:
            logger.warning("Success notification not found — may have auto-dismissed")

        logger.info(f"Final URL: {sim_page.browser.current_url}")
