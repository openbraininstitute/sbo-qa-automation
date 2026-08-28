# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import pytest
from pages.simulate_mem_page import SimulateMemPage


class TestSimulateMem:
    """End-to-end test for Single neuron simulation (ME-model circuit UI).

    Entry is via Workflows → Simulate → Single neuron (non-beta card).
    After Use model, the config UI matches ME-beta (scan-config), so the
    post-picker flow reuses SimulateMeBetaPage.
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

        # Step 5: Click "Use model" → config page (shared ME-beta UI)
        sim_page.click_use_model()
        logger.info(f"After Use model, URL: {sim_page.browser.current_url}")

        beta = sim_page.as_me_beta_page()

        # Step 6: Wait for config page to load
        beta.wait_for_config_page(timeout=30)
        logger.info("Config page loaded")

        # Step 7: Measure 3D morphology load time
        morph_start = time.time()
        try:
            beta.wait_for_neuron_visualizer(timeout=30)
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

        # Step 9: Verify Configuration and Simulations tabs
        tabs = beta.verify_config_tabs()
        assert tabs['configuration']['present'], "Configuration tab should be present"
        assert tabs['simulations']['present'], "Simulations tab should be present"
        logger.info("Configuration and Simulations tabs verified")

        # Steps 10-11: Info tab — fill campaign name + description
        if beta.is_info_tab_active():
            from datetime import datetime
            campaign_name = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            beta.fill_campaign_name(campaign_name)
            beta.fill_campaign_description("automated test of MEmodel")
            logger.info(f"Info filled: name='{campaign_name}'")
        else:
            logger.info("Info tab is not active, skipping form fill")

        # Step 12: Initialization tab — verify labels/values, add one sweep
        beta.click_initialization_tab()
        assert beta.is_initialization_tab_active(), "Initialization tab should be active"
        init_blocks = beta.verify_initialization_data()
        logger.info(f"Initialization: {len(init_blocks)} blocks")

        import random as rnd

        def random_value_for(label):
            if 'RANDOM SEED' in label:
                return rnd.randint(1, 5)
            elif 'INITIAL VOLTAGE' in label:
                return round(rnd.uniform(-80, 0), 1)
            elif 'EXTRACELLULAR CALCIUM' in label:
                return round(rnd.uniform(0.5, 5.0), 1)
            elif 'DURATION' in label:
                return rnd.randint(100, 2000)
            else:
                return round(rnd.uniform(0.1, 100.0), 2)

        numeric_blocks = [b for b in init_blocks if b['has_number_input']]
        assert len(numeric_blocks) >= 1, "Need at least 1 numeric config block"
        chosen = rnd.choice(numeric_blocks)
        sweep_value = random_value_for(chosen['label'])
        beta.add_parameter_sweep_value(chosen['index'], sweep_value)
        logger.info(f"Added sweep on '{chosen['label']}': {sweep_value}")

        # Step 13: Stimuli → Add Stimulus → pick dictionary item
        beta.click_stimuli_tab()
        assert beta.is_stimuli_tab_active(), "Stimuli tab should be active"
        beta.click_add_button_in_active_sub_entry()
        stim_items = beta.get_dictionary_items()
        assert len(stim_items) > 0, "Expected at least one stimulus dictionary item"
        stim_label = beta.click_random_dictionary_item()
        logger.info(f"Selected stimulus: '{stim_label}'")
        beta.wait_for_block_single(timeout=10)

        # Step 14: Recordings → Add Recording → pick dictionary item
        beta.click_recordings_tab()
        assert beta.is_recordings_tab_active(), "Recordings tab should be active"
        beta.click_add_button_in_active_sub_entry("Recording")
        rec_items = beta.get_dictionary_items()
        assert len(rec_items) > 0, "Expected at least one recording dictionary item"
        rec_label = beta.click_random_dictionary_item()
        logger.info(f"Selected recording: '{rec_label}'")
        beta.wait_for_block_single(timeout=10)

        # Step 15: Timestamps → Add → pick item → add sweep value
        beta.click_timestamps_tab()
        assert beta.is_timestamps_tab_active(), "Timestamps tab should be active"
        beta.click_add_button_in_active_sub_entry("Timestamp")
        ts_items = beta.get_dictionary_items()
        assert len(ts_items) > 0, "Expected at least one timestamp dictionary item"
        ts_label = beta.click_random_dictionary_item()
        logger.info(f"Selected timestamp: '{ts_label}'")
        beta.wait_for_block_single(timeout=10)
        beta.add_timestamp_sweep_value(rnd.randint(50, 2000))

        # Step 16: Generate simulation(s)
        gen_btn = beta.find_generate_simulation_btn(timeout=10)
        assert gen_btn.is_displayed() and gen_btn.is_enabled(), (
            "Generate simulation button should be visible and enabled"
        )
        beta.click_generate_simulation()
        logger.info("Clicked Generate simulation(s)")

        # Step 17: Simulations page — cards + input files
        beta.wait_for_simulations_page(timeout=60)
        sim_cards = beta.get_simulation_cards(timeout=15)
        assert len(sim_cards) > 0, "Expected at least one simulation card"
        logger.info(f"Found {len(sim_cards)} simulation card(s)")

        expected_files = ['node_sets.json', 'obi_one_coordinate.json', 'simulation_config.json']
        file_buttons = beta.get_input_file_buttons(timeout=10)
        actual_filenames = [name for _, name in file_buttons]
        for expected in expected_files:
            assert expected in actual_filenames, (
                f"Expected input file '{expected}' not found. Actual: {actual_filenames}"
            )
        logger.info(f"All expected input files present: {expected_files}")

        # Step 18: Launch and wait for completion
        launch_btn = beta.find_launch_simulations_btn(timeout=10)
        assert launch_btn.is_displayed(), "Launch simulations button should be visible"
        beta.click_launch_simulations()
        logger.info("Clicked Launch simulations")

        final_statuses = beta.wait_for_simulations_complete(timeout=300, poll_interval=10)
        logger.info(f"Final simulation statuses: {final_statuses}")
        failed = [s for s in final_statuses if s in ('failed', 'error')]
        assert not failed, (
            f"{len(failed)}/{len(final_statuses)} simulation(s) finished with errors. "
            f"Statuses: {final_statuses}"
        )
        logger.info(f"Final URL: {sim_page.browser.current_url}")
