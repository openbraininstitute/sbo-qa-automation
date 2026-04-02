# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import pytest
from pages.simulate_small_microcircuit_page import SimulateSmallMicrocircuitPage


class TestSimulateSmallMicrocircuit:
    """End-to-end test for Small microcircuit (beta) simulation.

    Flow:
    1.  Workflows → Simulate → Small microcircuit card → model picker
    2.  Public tab → verify columns → verify pagination → random page → click row
    3.  Mini-detail: verify title/description → Use model
    4.  Config page: verify Configuration + Results tabs
    5.  Wait for 3D morphology viewer (non-blocking, 120s)
    6.  Info tab: fill datetime name + description, verify Created by / Registration date
    7.  Experimental setup: verify labels present
    8.  Stimulation protocol: wait for plot, verify download button
    9.  Recording: add recordings for available sections
    10. Generate simulation(s) → auto-redirect to Results tab
    11. Verify left menu (All + recording buttons), buttons disabled while running
    12. Verify plots and 3D canvas visible during simulation
    13. Wait for completion (300s), verify buttons enabled, success notification
    """

    def _get_page(self, setup, logger):
        browser, wait, base_url, lab_id, project_id = setup
        return SimulateSmallMicrocircuitPage(browser, wait, logger, base_url), lab_id, project_id

    @pytest.mark.simulate
    @pytest.mark.run(order=21)
    def test_small_microcircuit_full_flow(self, setup, login, logger, test_config):
        sim_page, lab_id, project_id = self._get_page(setup, logger)

        # Step 1-2: Navigate to Workflows → Simulate → Small microcircuit
        sim_page.go_to_workflows_simulate(lab_id, project_id)
        sim_page.click_simulate_category()
        sim_page.click_small_microcircuit_card()
        logger.info(f"On model picker. URL: {sim_page.browser.current_url}")

        # Step 3: Public tab → verify table has rows
        sim_page.click_public_tab()
        row_count = sim_page.get_row_count()
        assert row_count > 0, "Expected at least one model row"

        # Step 4: Verify column headers
        col_results = sim_page.verify_column_headers()
        missing = [name for name, r in col_results.items() if not r['present']]
        assert not missing, f"Missing column headers: {missing}"
        logger.info("All column headers verified")

        # Step 5: Verify pagination is present (2+ pages)
        page_count = sim_page.get_pagination_page_count()
        if page_count >= 2:
            logger.info(f"Pagination present with {page_count} pages")

            # Step 6: Navigate to a random page
            sim_page.navigate_to_random_page()
            logger.info("Navigated to random pagination page")
        else:
            logger.warning(f"Pagination has only {page_count} page(s), skipping random navigation")

        '''
        This is commented out because the Rat data is not visible in staging.
        
        '''

        # # Step 7: Click random row
        # row_text = sim_page.click_random_row()
        # logger.info(f"Clicked row: '{row_text}'")

        # # Step 8: Mini-detail: verify title, description, click "Use model"
        # sim_page.wait_for_mini_detail()
        # detail = sim_page.verify_mini_detail_title_and_description()
        # assert detail['title']['present'], "Mini-detail title should be present"
        # logger.info(f"Mini-detail title: '{detail['title'].get('text', '')}'")
        # if not detail.get('description', {}).get('present'):
        #     logger.warning("Mini-detail description not found")

        # sim_page.click_use_model()
        # logger.info(f"After Use model, URL: {sim_page.browser.current_url}")

        # # Step 9: Config page: wait for layout, verify Configuration + Results tabs
        # sim_page.wait_for_config_page(timeout=30)
        # logger.info("Config page loaded")

        # tabs = sim_page.verify_config_tabs()
        # assert tabs['configuration']['present'], "Configuration tab should be present"
        # assert tabs['simulations']['present'], "Simulations tab should be present"
        # logger.info("Configuration and Results tabs verified")

        # # Step 10: Verify circuit preview image is displayed
        # preview_ok = sim_page.wait_for_circuit_preview(timeout=30)
        # if preview_ok:
        #     logger.info("Circuit preview image loaded")
        # else:
        #     logger.warning("Circuit preview image not found")

        # # Step 11: Info tab — fill Campaign Name + Description
        # sim_page.click_info_tab()
        # campaign_name = sim_page.fill_name_with_datetime()
        # sim_page.fill_description("automated test of small microcircuit")
        # logger.info(f"Info filled: name='{campaign_name}'")

        # # Step 12: Initialization tab — verify all fields have data
        # sim_page.click_initialization_tab()
        # init_blocks = sim_page.get_config_block_labels_and_values()
        # assert len(init_blocks) > 0, "Initialization should have config blocks"
        # for b in init_blocks:
        #     assert b['label'], f"Block has empty label: {b}"
        # logger.info(f"Initialization: {len(init_blocks)} blocks, all with labels")

        # # Step 13: Stimuli tab — click Add Stimulus → select random → verify form
        # sim_page.click_stimuli_tab()
        # sim_page.click_add_button_in_active_sub_entry()
        # logger.info("Clicked 'Add Stimulus'")

        # stim_items = sim_page.get_dictionary_items()
        # assert len(stim_items) > 0, "Expected at least one stimulus dictionary item"
        # stim_label = sim_page.click_random_dictionary_item()
        # logger.info(f"Selected stimulus: '{stim_label}'")

        # sim_page.wait_for_block_single(timeout=10)
        # logger.info("Stimulus config form appeared with data")

        # # Step 14: Recordings tab — click Add Recording → select random → verify form
        # sim_page.click_recordings_tab()
        # sim_page.click_add_button_in_active_sub_entry()
        # logger.info("Clicked 'Add Recording'")

        # rec_items = sim_page.get_dictionary_items()
        # assert len(rec_items) > 0, "Expected at least one recording dictionary item"
        # rec_label = sim_page.click_random_dictionary_item()
        # logger.info(f"Selected recording: '{rec_label}'")

        # sim_page.wait_for_block_single(timeout=10)
        # logger.info("Recording config form appeared with data")

        # # Step 15: Neuron sets tab — click Add Neuron Set → select random → verify form
        # sim_page.click_neuron_sets_tab()
        # sim_page.click_add_button_in_active_sub_entry()
        # logger.info("Clicked 'Add Neuron Set'")

        # ns_items = sim_page.get_dictionary_items()
        # assert len(ns_items) > 0, "Expected at least one neuron set dictionary item"
        # ns_label = sim_page.click_random_dictionary_item()
        # logger.info(f"Selected neuron set: '{ns_label}'")

        # sim_page.wait_for_block_single(timeout=10)
        # logger.info("Neuron set config form appeared with data")

        # # Step 16: Synaptic manipulations tab — click Add → select random → verify form
        # sim_page.click_synaptic_manip_tab()
        # sim_page.click_add_button_in_active_sub_entry()
        # logger.info("Clicked 'Add Synaptic Manipulation'")

        # sm_items = sim_page.get_dictionary_items()
        # assert len(sm_items) > 0, "Expected at least one synaptic manipulation item"
        # sm_label = sim_page.click_random_dictionary_item()
        # logger.info(f"Selected synaptic manipulation: '{sm_label}'")

        # sim_page.wait_for_block_single(timeout=10)
        # logger.info("Synaptic manipulation config form appeared with data")

        # # Step 17: Timestamps tab — click Add → select random → verify form
        # sim_page.click_timestamps_tab()
        # sim_page.click_add_button_in_active_sub_entry()
        # logger.info("Clicked 'Add Timestamp'")

        # ts_items = sim_page.get_dictionary_items()
        # assert len(ts_items) > 0, "Expected at least one timestamp dictionary item"
        # ts_label = sim_page.click_random_dictionary_item()
        # logger.info(f"Selected timestamp: '{ts_label}'")

        # sim_page.wait_for_block_single(timeout=10)
        # logger.info("Timestamp config form appeared with data")

        # # Step 18: Click Generate simulation(s)
        # sim_page.click_generate_simulation()
        # logger.info("Clicked Generate simulation(s)")

        # # Step 17: Results tab: verify auto-redirect, left menu has All + recording buttons
        # time.sleep(5)
        # assert sim_page.is_results_tab_active(), "Results tab should be active after Generate simulation(s)"
        # logger.info("Results tab active after Generate simulation(s)")

        # all_btns = sim_page.get_results_left_menu_buttons()
        # assert len(all_btns) >= 2, f"Expected All + at least 1 recording button, got {len(all_btns)}"
        # rec_btns = sim_page.get_results_recording_buttons()
        # assert len(rec_btns) >= 1, "Expected at least 1 recording button in Results left menu"
        # logger.info(f"Results menu: {len(all_btns)} buttons, {len(rec_btns)} recording(s)")

        # # Step 18: Verify Download CSV and Reconfigure disabled while running
        # assert not sim_page.is_download_csv_enabled(), "Download CSV should be disabled while running"
        # assert not sim_page.is_reconfigure_enabled(), "Reconfigure should be disabled while running"
        # logger.info("Download CSV and Reconfigure are disabled (simulation running)")

        # # Step 19: Verify plots and 3D canvas visible during simulation
        # plot_count = sim_page.get_idrest_plot_count()
        # logger.info(f"IDREST plots visible while running: {plot_count}")

        # logger.info("Circuit preview (no 3D canvas for microcircuit)")

        # # Step 20: Wait for simulation completion (Download CSV enabled, 300s timeout)
        # sim_done = sim_page.wait_for_simulation_complete(timeout=300, poll_interval=10)
        # assert sim_done, "Simulation should complete (Download CSV enabled)"
        # logger.info("Simulation completed")

        # # Step 21: Verify Download CSV and Reconfigure enabled after completion
        # assert sim_page.is_download_csv_enabled(), "Download CSV should be enabled after completion"
        # assert sim_page.is_reconfigure_enabled(), "Reconfigure should be enabled after completion"
        # logger.info("Download CSV and Reconfigure are enabled")

        # # Step 22: Verify success notification with View Simulation link
        # notif_ok = sim_page.wait_for_success_notification(timeout=30)
        # if notif_ok:
        #     link = sim_page.get_view_simulation_link()
        #     assert link is not None, "View Simulation link should be present in notification"
        #     logger.info(f"Success notification with View Simulation link: {link.get_attribute('href')}")
        # else:
        #     logger.warning("Success notification not found — may have auto-dismissed")

        # logger.info(f"Final URL: {sim_page.browser.current_url}")
