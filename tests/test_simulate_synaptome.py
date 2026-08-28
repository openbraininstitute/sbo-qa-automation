# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import pytest
from pages.simulate_synaptome_page import SimulateSynaptomePage


class TestSimulateSynaptome:
    """End-to-end test for Synaptome simulation (non-legacy card).

    Entry is via Workflows → Simulate → Cellular Synaptome (non-legacy, non-beta).
    After Use model, the config UI matches Synaptome beta (scan-config), so the
    post-picker flow reuses SimulateSynaptomeBetaPage.
    """

    def _get_page(self, setup, logger):
        browser, wait, base_url, lab_id, project_id = setup
        return SimulateSynaptomePage(browser, wait, logger, base_url), lab_id, project_id

    @pytest.mark.simulate
    @pytest.mark.run(order=30)
    def test_simulate_synaptome_full_flow(self, setup, login, logger, test_config):
        page, lab_id, project_id = self._get_page(setup, logger)

        # Step 1-2: Navigate to Workflows → Simulate → Synaptome
        page.go_to_workflows_simulate(lab_id, project_id)
        page.click_simulate_category()
        page.click_synaptome_card()
        logger.info(f"On model picker. URL: {page.browser.current_url}")

        # Step 3: Public tab, verify rows
        page.click_public_tab()
        assert page.get_row_count() > 0, "Expected at least one model row"

        # Step 4: Open filter panel, click random field, close
        page.open_filter_panel()
        filter_label = page.click_random_filter_accordion()
        assert filter_label is not None, "Should be able to click a filter accordion"
        logger.info(f"Filter accordion clicked: '{filter_label}'")
        page.close_filter_panel()

        # Step 5: Click random row (skip excluded)
        row_text = page.click_random_row()
        logger.info(f"Clicked row: '{row_text}'")

        # Step 6: Verify mini-detail view
        page.wait_for_mini_detail()
        detail = page.verify_mini_detail_view()
        assert detail['title'], "Mini-detail title should be present"
        assert detail['description'], "Mini-detail description should be present"
        if detail['images_count'] < 1:
            logger.info("No images found, waiting for preview to load...")
            time.sleep(10)
            detail = page.verify_mini_detail_view()
        assert detail['images_count'] >= 1, f"Expected at least 1 image, got {detail['images_count']}"
        if detail['images_count'] < 2:
            logger.warning(f"Only {detail['images_count']} mini-detail image(s) — continuing")
        assert detail['metadata_count'] > 0, "Mini-detail should have metadata"
        assert detail['close_btn'], "Close (x) button should be present"
        assert detail['view_details_btn'], "'View details' button should be present"
        assert detail['use_model_btn'], "'Use model' button should be present"
        logger.info("Mini-detail view verified")

        # Step 7: Click Use model → hand off to shared scan-config UI
        page.click_use_model()
        logger.info(f"After Use model, URL: {page.browser.current_url}")

        beta = page.as_synaptome_beta_page()

        # Step 8: Config page → verify tabs
        beta.wait_for_config_page(timeout=30)
        logger.info("Config page loaded")

        tabs = beta.verify_config_tabs()
        assert tabs['configuration']['present'], "Configuration tab should be present"
        assert tabs['simulations']['present'], "Simulations tab should be present"
        logger.info("Configuration and Simulations tabs verified")

        preview_ok = beta.wait_for_circuit_preview(timeout=30)
        if preview_ok:
            logger.info("Circuit preview image loaded")
        else:
            logger.warning("Circuit preview image not found")

        # Step 9: Info tab — fill name/description
        beta.click_info_tab()
        campaign_name = beta.fill_name_with_datetime()
        beta.fill_description("automated test of synaptome")
        logger.info(f"Info filled: name='{campaign_name}'")

        # Step 10: Initialization
        beta.click_initialization_tab()
        init_labels = beta.get_initialization_labels()
        logger.info(f"Initialization labels: {init_labels}")

        # Step 11: Stimuli — one random stimulus
        beta.click_stimuli_tab()
        beta.click_add_button_in_active_sub_entry()
        stim_items = beta.get_dictionary_items()
        assert len(stim_items) > 0, "Expected at least one stimulus dictionary item"
        stim_label = beta.click_random_dictionary_item()
        logger.info(f"Selected stimulus: '{stim_label}'")
        beta.wait_for_block_single(timeout=10)

        # Step 12: Recordings
        beta.click_recordings_tab()
        beta.click_add_button_in_active_sub_entry("Recording")
        rec_items = beta.get_dictionary_items()
        assert len(rec_items) > 0, "Expected at least one recording item"
        rec_label = beta.click_random_dictionary_item()
        logger.info(f"Selected recording: '{rec_label}'")
        beta.wait_for_block_single(timeout=10)

        # Step 13: Neuron sets
        beta.click_neuron_sets_tab()
        beta.click_add_button_in_active_sub_entry("Neuron Set")
        ns_items = beta.get_dictionary_items()
        assert len(ns_items) > 0, "Expected at least one neuron set item"
        try:
            ns_label = beta.click_dictionary_item_by_label("ALL POPULATIONS")
        except AssertionError:
            try:
                ns_label = beta.click_dictionary_item_by_label("SINGLE POPULATION (Virtual)")
            except AssertionError:
                ns_label = beta.click_random_dictionary_item()
        logger.info(f"Selected neuron set: '{ns_label}'")
        beta.wait_for_block_single(timeout=10)

        # Step 14: Synaptic manipulations
        beta.click_synaptic_manip_tab()
        beta.click_add_button_in_active_sub_entry("Synaptic Manipulation")
        sm_items = beta.get_dictionary_items()
        assert len(sm_items) > 0, "Expected at least one synaptic manipulation item"
        sm_label = beta.click_random_dictionary_item()
        logger.info(f"Selected synaptic manipulation: '{sm_label}'")
        beta.wait_for_block_single(timeout=10)

        # Step 15: Timestamps
        beta.click_timestamps_tab()
        beta.click_add_button_in_active_sub_entry("Timestamp")
        ts_items = beta.get_dictionary_items()
        assert len(ts_items) > 0, "Expected at least one timestamp item"
        try:
            ts_label = beta.click_dictionary_item_by_label("Timestamp")
        except AssertionError:
            ts_label = beta.click_random_dictionary_item()
        logger.info(f"Selected timestamp: '{ts_label}'")
        beta.wait_for_block_single(timeout=10)

        # Step 16: Generate → Simulations tab
        beta.click_generate_simulation()
        logger.info("Clicked Generate simulation(s)")

        from selenium.webdriver.support.ui import WebDriverWait
        try:
            WebDriverWait(beta.browser, 60).until(
                lambda d: beta.is_simulations_tab_active()
            )
        except Exception:
            logger.info("Simulations tab not auto-active after 60s, clicking manually")
            try:
                beta.click_simulations_tab()
                time.sleep(3)
            except Exception as e:
                logger.warning(f"Could not click Simulations tab: {e}")

        assert beta.is_simulations_tab_active(), (
            "Simulations tab should be active after Generate simulation(s)"
        )
        logger.info("Simulations tab active")

        sim_cards = beta.get_simulation_cards()
        assert len(sim_cards) >= 1, f"Expected at least 1 simulation card, got {len(sim_cards)}"
        logger.info(f"Found {len(sim_cards)} simulation card(s)")

        input_files = beta.get_input_file_buttons()
        assert len(input_files) >= 1, "Expected at least 1 input file"
        file_names = [b.get_attribute("title") or "" for b in input_files]
        logger.info(f"Input files ({len(input_files)}): {file_names}")

        # Step 17: Launch and poll
        assert beta.is_launch_simulations_enabled(), "Launch simulations should be enabled"
        beta.click_launch_simulations()
        logger.info("Clicked Launch simulations")

        sim_done = beta.wait_for_simulation_terminal_state(timeout=300, poll_interval=10)
        if sim_done:
            logger.info("All simulations reached terminal state")
            final_statuses = beta.get_simulation_card_statuses()
            for s in final_statuses:
                logger.info(f"  Final: {s['title']}: {s['status']}")
        else:
            logger.warning("Simulations did not complete within 300s")

        logger.info(f"Final URL: {page.browser.current_url}")
