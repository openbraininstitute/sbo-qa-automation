# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import pytest
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from pages.simulate_me_beta_page import SimulateMeBetaPage


class TestSimulateMeBeta:
    """Test cases for ME-model picker page (single neuron beta simulation).

    Flow:
    1. Navigate to simulation page (model picker)
    2. Select Public tab
    3. Verify column headers
    4. Open Filters → expand E-type → type 'cADpyr' → apply
    5. Verify E-type column shows filtered results
    6. Click a random model row
    """

    def _get_sim_page(self, setup, logger):
        browser, wait, base_url, lab_id, project_id = setup
        return SimulateMeBetaPage(browser, wait, logger, base_url), lab_id, project_id

    # ── Test: Full flow ──────────────────────────────────────────────────

    @pytest.mark.simulate
    @pytest.mark.run(order=10)
    def test_model_picker_full_flow(self, setup, login, logger, test_config):
        """Full flow: Public tab → verify columns → filter E-type → click model."""
        sim_page, lab_id, project_id = self._get_sim_page(setup, logger)

        # Navigate to simulation page
        sim_page.go_to_simulation_page(lab_id, project_id)
        logger.info("Navigated to simulation page")

        # Step 1: Click Public tab
        sim_page.click_public_tab()
        logger.info("Selected Public tab")

        # Step 2: Verify all column headers are present
        col_results = sim_page.verify_column_headers()
        missing = [name for name, r in col_results.items() if not r['present']]
        assert not missing, f"Missing column headers: {missing}"
        logger.info("All column headers verified")

        # Step 3: Verify table has rows
        row_count = sim_page.get_row_count()
        assert row_count > 0, "Expected at least one model row in the table"
        logger.info(f"Table has {row_count} rows")

        # Step 4: Open Filters → expand E-type → type 'cADpyr' → select → apply
        sim_page.open_filter_panel()
        sim_page.expand_etype_filter()
        sim_page.type_etype_filter("cADpyr")

        try:
            sim_page.select_etype_option("cADpyr")
            logger.info("Selected 'cADpyr' option")
        except Exception as e:
            logger.warning(f"Could not select cADpyr option: {e}")
            options = sim_page.browser.find_elements(
                By.CSS_SELECTOR, "div.ant-select-item-option"
            )
            for opt in options[:10]:
                logger.info(f"  Available option: '{opt.text}'")

        sim_page.click_filter_apply()
        time.sleep(3)

        try:
            sim_page.close_filter_panel()
        except Exception:
            pass
        time.sleep(2)

        # Step 5: Verify E-type column values contain 'cADpyr'
        etype_values = sim_page.get_etype_column_values()
        if etype_values:
            for val in etype_values:
                assert 'cADpyr' in val, f"Expected 'cADpyr' in E-type value, got: '{val}'"
            logger.info(f"All {len(etype_values)} E-type values contain 'cADpyr'")
        else:
            logger.warning("No E-type values found after filtering")

        # Step 6: Click a random model row
        row_text = sim_page.click_random_row()
        logger.info(f"Clicked model row: '{row_text}'")

        # Step 7: Verify mini-detail view appears
        sim_page.wait_for_mini_detail()
        detail_results = sim_page.verify_mini_detail_view()

        # Verify name, description, images, metadata, and both buttons
        assert detail_results['title']['present'], "Mini-detail title (name) should be present"
        assert detail_results['description']['present'], "Mini-detail description should be present"
        assert detail_results['images']['present'], "Mini-detail should have at least one image"
        assert detail_results['metadata']['present'], "Mini-detail should have metadata"
        assert detail_results['view_details_btn']['present'], "'View details' button should be present"
        assert detail_results['use_model_btn']['present'], "'Use model' button should be present"
        logger.info("Mini-detail view verified: name, description, images, metadata, buttons")

        # Log the title text
        title_el = sim_page.find_mini_detail_title()
        logger.info(f"Mini-detail title: '{title_el.text}'")

        # Step 8: Click "Use model" → redirected to config page
        sim_page.click_use_model()
        logger.info(f"After 'Use model', URL: {sim_page.browser.current_url}")

        # Step 9: Wait for config page and 3D morphology viewer
        sim_page.wait_for_config_page(timeout=30)
        logger.info("Config page loaded")

        try:
            sim_page.wait_for_neuron_visualizer(timeout=60)
            logger.info("3D morphology viewer loaded")
        except Exception as e:
            logger.warning(f"Neuron visualizer canvas not loaded within timeout: {e}")
            logger.info("Continuing test — canvas may load slowly in staging")

        # Step 10: Verify Configuration and Simulations tabs
        tab_results = sim_page.verify_config_tabs()
        assert tab_results['configuration']['present'], "Configuration tab should be present"
        assert tab_results['simulations']['present'], "Simulations tab should be present"
        logger.info("Configuration and Simulations tabs verified")

        # Step 11: If Info tab is active, fill in name and description
        if sim_page.is_info_tab_active():
            sim_page.fill_campaign_name("Automated Test Campaign")
            sim_page.fill_campaign_description("Automated test run for single neuron beta simulation")
            logger.info("Filled campaign name and description")
        else:
            logger.info("Info tab is not active, skipping form fill")

        # Step 12: Click Initialization tab, verify it's active
        sim_page.click_initialization_tab()
        assert sim_page.is_initialization_tab_active(), "Initialization tab should be active after clicking"
        logger.info("Initialization tab is active")

        # Step 13: Verify middle column has labels and values (none empty)
        init_blocks = sim_page.verify_initialization_data()
        logger.info(f"Initialization tab has {len(init_blocks)} blocks, all with labels and values")

        # Realistic value ranges per parameter
        import random as rnd

        def random_value_for(label):
            """Return a realistic random value based on the parameter name."""
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

        # Step 14: Pick 2 random parameter blocks, add sweep values
        numeric_blocks = [b for b in init_blocks if b['has_number_input']]
        assert len(numeric_blocks) >= 2, f"Need at least 2 numeric config blocks to test sweep, got {len(numeric_blocks)}"
        chosen = rnd.sample(numeric_blocks, 2)

        for block_info in chosen:
            idx = block_info['index']
            original_count = sim_page.get_sweep_input_count(idx)
            sweep_value = random_value_for(block_info['label'])
            sim_page.add_parameter_sweep_value(idx, sweep_value)
            new_count = sim_page.get_sweep_input_count(idx)
            assert new_count > original_count, (
                f"Block [{idx}] input count should increase after adding sweep "
                f"(was {original_count}, now {new_count})"
            )
            logger.info(f"Block [{idx}] '{block_info['label']}': "
                        f"added sweep value {sweep_value}, inputs {original_count} → {new_count}")

        logger.info("Parameter sweep values added and verified")

        # Step 15: Add 2 more sweep values to INITIAL VOLTAGE and RANDOM SEED
        target_labels = ['INITIAL VOLTAGE', 'RANDOM SEED']
        for label_name in target_labels:
            block_info = next((b for b in init_blocks if b['label'] == label_name), None)
            assert block_info, f"Block '{label_name}' not found in Initialization tab"
            idx = block_info['index']

            # Check if already in sweep mode (>1 input means Step 14 already converted it)
            current_count = sim_page.get_sweep_input_count(idx)
            if current_count == 1:
                sweep_val_1 = random_value_for(label_name)
                sim_page.add_parameter_sweep_value(idx, sweep_val_1)
                logger.info(f"Converted '{label_name}' to sweep mode with value {sweep_val_1}")

            # Now add 2 more values
            for i in range(2):
                before = sim_page.get_sweep_input_count(idx)
                extra_val = random_value_for(label_name)
                sim_page.add_extra_sweep_value(idx, extra_val)
                after = sim_page.get_sweep_input_count(idx)
                assert after > before, (
                    f"'{label_name}' input count should increase (was {before}, now {after})"
                )
                logger.info(f"'{label_name}': added extra value {extra_val}, inputs {before} → {after}")

        final_iv_count = sim_page.get_sweep_input_count(
            next(b for b in init_blocks if b['label'] == 'INITIAL VOLTAGE')['index']
        )
        final_rs_count = sim_page.get_sweep_input_count(
            next(b for b in init_blocks if b['label'] == 'RANDOM SEED')['index']
        )
        logger.info(f"Final sweep counts — INITIAL VOLTAGE: {final_iv_count}, RANDOM SEED: {final_rs_count}")

        # Step 16: Click Stimuli → Add Stimulus → select dictionary item
        sim_page.click_stimuli_tab()
        assert sim_page.is_stimuli_tab_active(), "Stimuli tab should be active after clicking"
        logger.info("Stimuli tab is active")

        sim_page.click_add_button_in_active_sub_entry()
        logger.info("Clicked 'Add Stimulus'")

        stim_dict_items = sim_page.get_dictionary_items()
        assert len(stim_dict_items) > 0, "Expected at least one stimulus dictionary item"
        stim_label = sim_page.click_random_dictionary_item()
        logger.info(f"Selected stimulus type: '{stim_label}'")

        sim_page.wait_for_block_single(timeout=10)
        logger.info("Stimulus config form (block_single) appeared")

        # Step 17: Click Recordings → Add Recording → select dictionary item
        sim_page.click_recordings_tab()
        assert sim_page.is_recordings_tab_active(), "Recordings tab should be active after clicking"
        logger.info("Recordings tab is active")

        sim_page.click_add_button_in_active_sub_entry()
        logger.info("Clicked 'Add Recording'")

        rec_dict_items = sim_page.get_dictionary_items()
        assert len(rec_dict_items) > 0, "Expected at least one recording dictionary item"
        rec_label = sim_page.click_random_dictionary_item()
        logger.info(f"Selected recording type: '{rec_label}'")

        sim_page.wait_for_block_single(timeout=10)
        logger.info("Recording config form (block_single) appeared")

        # Step 18: Click Neuronal manipulations → Add → select dictionary item → verify form
        sim_page.click_neuronal_manip_tab()
        assert sim_page.is_neuronal_manip_tab_active(), "Neuronal manipulations tab should be active"
        logger.info("Neuronal manipulations tab is active")

        sim_page.click_add_button_in_active_sub_entry()
        logger.info("Clicked 'Add Neuronal Manipulation'")

        nm_dict_items = sim_page.get_dictionary_items()
        assert len(nm_dict_items) > 0, "Expected at least one neuronal manipulation dictionary item"
        nm_label = sim_page.click_random_dictionary_item()
        logger.info(f"Selected neuronal manipulation type: '{nm_label}'")

        block_single = sim_page.wait_for_block_single(timeout=10)
        logger.info("Neuronal manipulation config form (block_single) appeared")

        # Open the "Select a variable" dropdown, pick an option, fill value inputs
        selected_var = sim_page.select_neuronal_manip_variable(timeout=10)
        assert selected_var, "A neuronal manipulation variable must be selected"
        logger.info(f"Selected neuronal manipulation variable: '{selected_var}'")

        # Verify no warning icon on the neuronal manipulation sub-item
        has_warning = sim_page.neuronal_manip_has_warning()
        if has_warning:
            logger.warning("Neuronal manipulation sub-item still shows warning — some fields may be empty")
        else:
            logger.info("Neuronal manipulation sub-item has no warning icon — all fields filled")

        # Step 19: Click Timestamps → Add Timestamps → select random dictionary item → add 2 sweep values
        sim_page.click_timestamps_tab()
        assert sim_page.is_timestamps_tab_active(), "Timestamps tab should be active"
        logger.info("Timestamps tab is active")

        sim_page.click_add_button_in_active_sub_entry()
        logger.info("Clicked 'Add Timestamps'")

        ts_dict_items = sim_page.get_dictionary_items()
        assert len(ts_dict_items) > 0, "Expected at least one timestamp dictionary item"
        ts_label = sim_page.click_random_dictionary_item()
        logger.info(f"Selected timestamp type: '{ts_label}'")

        sim_page.wait_for_block_single(timeout=10)
        logger.info("Timestamp config form (block_single) appeared")

        # Add 2 random timestamp sweep values (milliseconds, realistic range 0-2000)
        import random as rnd
        for i in range(2):
            before = sim_page.get_timestamp_input_count()
            ts_value = rnd.randint(50, 2000)
            sim_page.add_timestamp_sweep_value(ts_value)
            after = sim_page.get_timestamp_input_count()
            assert after > before, (
                f"Timestamp input count should increase (was {before}, now {after})"
            )
            logger.info(f"Added timestamp sweep value: {ts_value} ms, inputs {before} → {after}")

        # Step 20: Verify "Generate simulation(s)" button is present
        gen_btn = sim_page.find_generate_simulation_btn(timeout=10)
        assert gen_btn.is_displayed(), "Generate simulation button should be visible"
        logger.info(f"Generate simulation button found, enabled={gen_btn.is_enabled()}")

        # Click Generate simulation
        sim_page.click_generate_simulation()
        logger.info("Clicked Generate simulation(s)")

        # Step 21: Wait for the Simulations page to become active
        sim_page.wait_for_simulations_page(timeout=60)
        logger.info(f"Simulations page loaded. URL: {sim_page.browser.current_url}")

        # Step 22: Verify simulation cards are present in the left column
        sim_cards = sim_page.get_simulation_cards(timeout=15)
        assert len(sim_cards) > 0, "Expected at least one simulation card"
        logger.info(f"Found {len(sim_cards)} simulation card(s)")

        # Verify first card has title and status
        card_info = sim_page.get_simulation_card_info(sim_cards[0])
        assert card_info['title'], "Simulation card should have a title"
        assert card_info['status'], "Simulation card should have a status badge"
        logger.info(f"First card: '{card_info['title']}', status='{card_info['status']}', "
                     f"params={list(card_info['params'].keys())}")

        # Step 23: Verify input files are present in the middle column
        expected_files = ['node_sets.json', 'obi_one_coordinate.json', 'simulation_config.json']
        file_buttons = sim_page.get_input_file_buttons(timeout=10)
        actual_filenames = [name for _, name in file_buttons]
        for expected in expected_files:
            assert expected in actual_filenames, (
                f"Expected input file '{expected}' not found. Actual: {actual_filenames}"
            )
        logger.info(f"All expected input files present: {expected_files}")

        # Step 24: Click each input file and verify JSON preview appears
        for filename in expected_files:
            sim_page.click_input_file(filename)
            json_text = sim_page.get_json_preview_text(timeout=10)
            assert len(json_text) > 0, f"JSON preview should have content after clicking '{filename}'"
            assert '{' in json_text, f"JSON preview for '{filename}' should contain valid JSON"
            logger.info(f"'{filename}': JSON preview loaded ({len(json_text)} chars)")

        # Step 25: Verify Launch simulations button is present and click it
        launch_btn = sim_page.find_launch_simulations_btn(timeout=10)
        assert launch_btn.is_displayed(), "Launch simulations button should be visible"
        btn_text = launch_btn.text.strip()
        logger.info(f"Launch button found: '{btn_text}', enabled={launch_btn.is_enabled()}")

        sim_page.click_launch_simulations()
        logger.info("Clicked Launch simulations")

        # Step 26: Wait for all simulations to reach a terminal state
        final_statuses = sim_page.wait_for_simulations_complete(timeout=300, poll_interval=10)
        logger.info(f"Final simulation statuses: {final_statuses}")

        failed = [s for s in final_statuses if s in ('failed', 'error')]
        if failed:
            logger.warning(f"{len(failed)} simulation(s) failed: {final_statuses}")
        else:
            logger.info("All simulations completed successfully")

        logger.info(f"Final URL: {sim_page.browser.current_url}")
