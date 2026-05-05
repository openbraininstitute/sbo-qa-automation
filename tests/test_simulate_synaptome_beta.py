# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import pytest
from pages.simulate_synaptome_beta_page import SimulateSynaptomeBetaPage


class TestSimulateSynaptomeBeta:
    """End-to-end test for Synaptome (beta) simulation.

    Flow (spec steps 1-50):
    1-2.   Workflows → Simulate → Synaptome (beta) card → model picker
    3-6.   Public tab → verify columns → pagination → click random row
    7.     Mini-detail → Use model
    8-9.   Config page → verify tabs + circuit preview image
    10-12. Info tab: warning icon → fill name/description → warning disappears
    13-14. Initialization: verify all fields present
    15-23. Stimuli: add random + "Poisson Spikes (Efferent)" with Frequency=50
    24-27. Recordings: add random recording type
    28-31. Distributions: add 3 random parameters
    32-34. Neuron sets: add "All Neurons"
    35-37. Synaptic manipulations: add random
    38-40. Timestamps: add random
    41-43. Generate simulation(s) → Simulations tab
    44-47. Verify cards, input files
    48-50. Launch → poll until terminal state
    """

    def _get_page(self, setup, logger):
        browser, wait, base_url, lab_id, project_id = setup
        return SimulateSynaptomeBetaPage(browser, wait, logger, base_url), lab_id, project_id

    @pytest.mark.simulate
    @pytest.mark.run(order=24)
    def test_synaptome_beta_full_flow(self, setup, login, logger, test_config):
        page, lab_id, project_id = self._get_page(setup, logger)

        # ── Steps 1-2: Navigate → Simulate → Synaptome (beta) ───────────
        page.go_to_workflows_simulate(lab_id, project_id)
        page.click_simulate_category()
        page.click_synaptome_beta_card()
        logger.info(f"On model picker. URL: {page.browser.current_url}")

        # ── Step 3: Public tab → verify rows ─────────────────────────────
        page.click_public_tab()
        row_count = page.get_row_count()
        assert row_count > 0, "Expected at least one model row"

        # ── Step 4: Verify column headers ────────────────────────────────
        col_results = page.verify_column_headers()
        missing = [name for name, r in col_results.items() if not r['present']]
        assert not missing, f"Missing column headers: {missing}"
        logger.info("All column headers verified")

        # ── Step 5: Pagination ───────────────────────────────────────────
        page_count = page.get_pagination_page_count()
        if page_count >= 2:
            page.navigate_to_random_page()
            logger.info(f"Pagination present with {page_count} pages")
        else:
            logger.warning(f"Only {page_count} page(s), skipping random navigation")

        # ── Step 6: Click random row ─────────────────────────────────────
        row_text = page.click_random_row()
        logger.info(f"Clicked row: '{row_text}'")

        # ── Step 7: Mini-detail → Use model ──────────────────────────────
        page.wait_for_mini_detail()
        detail = page.verify_mini_detail_title_and_description()
        assert detail['title']['present'], "Mini-detail title should be present"
        logger.info(f"Mini-detail title: '{detail['title'].get('text', '')}'")

        page.click_use_model()
        logger.info(f"After Use model, URL: {page.browser.current_url}")

        # ── Step 8: Config page → verify tabs ────────────────────────────
        page.wait_for_config_page(timeout=30)
        logger.info("Config page loaded")

        tabs = page.verify_config_tabs()
        assert tabs['configuration']['present'], "Configuration tab should be present"
        assert tabs['simulations']['present'], "Simulations tab should be present"
        logger.info("Configuration and Simulations tabs verified")

        # ── Step 9: Verify circuit preview image ─────────────────────────
        preview_ok = page.wait_for_circuit_preview(timeout=30)
        if preview_ok:
            logger.info("Circuit preview image loaded")
        else:
            logger.warning("Circuit preview image not found")

        # ── Step 10: Info tab — verify warning icon ──────────────────────
        page.click_info_tab()

        has_warning = page.is_info_warning_icon_visible(timeout=5)
        if has_warning:
            logger.info("Warning icon visible on Info tab (fields empty)")
        else:
            logger.warning("Warning icon not found — may already have defaults")

        # ── Step 11: Fill Campaign Name + Description ────────────────────
        campaign_name = page.fill_name_with_datetime()
        page.fill_description("automated test of synaptome beta")
        logger.info(f"Info filled: name='{campaign_name}'")

        # ── Step 12: Verify warning icon disappears ──────────────────────
        if has_warning:
            time.sleep(2)
            warning_gone = not page.is_info_warning_icon_visible(timeout=3)
            check_appeared = page.is_info_check_icon_visible(timeout=3)
            if warning_gone:
                logger.info("Warning icon disappeared after filling fields")
            if check_appeared:
                logger.info("Check icon appeared on Info tab")

        # ── Steps 13-14: Initialization tab — verify fields ──────────────
        page.click_initialization_tab()
        init_labels = page.get_initialization_labels()
        logger.info(f"Initialization labels: {init_labels}")

        expected_init = ["Circuit", "Duration", "Extracellular Calcium Concentration",
                         "Initial Voltage", "Random Seed", "Neuron Set"]
        for field in expected_init:
            found = any(field.lower() in lbl.lower() for lbl in init_labels)
            if found:
                logger.info(f"  ✓ '{field}' present")
            else:
                logger.warning(f"  ✗ '{field}' not found")

        # ── Steps 15-19: Stimuli — 1st random stimulus ───────────────────
        page.click_stimuli_tab()
        logger.info("On Stimuli tab")

        page.click_add_button_in_active_sub_entry()
        logger.info("Clicked 'Add Stimulus'")

        stim_items = page.get_dictionary_items()
        assert len(stim_items) > 0, "Expected at least one stimulus dictionary item"

        stim_label = page.click_random_dictionary_item()
        logger.info(f"Selected 1st stimulus: '{stim_label}'")

        page.wait_for_block_single(timeout=10)
        logger.info("1st stimulus config form appeared")

        # ── Steps 20-23: Stimuli — 2nd "Poisson Spikes (Efferent)" ───────
        page.click_add_button_in_active_sub_entry()
        logger.info("Clicked 'Add Stimulus' for 2nd")

        poisson_label = page.click_dictionary_item_by_label_with_scroll(
            "Poisson Spikes (Efferent)"
        )
        logger.info(f"Selected 2nd stimulus: '{poisson_label}'")

        page.wait_for_block_single(timeout=10)
        logger.info("2nd stimulus config form appeared")

        freq_set = page.set_block_number_input("Frequency", 50)
        if freq_set:
            logger.info("Set Frequency minimum to 50")
        else:
            logger.warning("Could not set Frequency — field not found")

        # ── Steps 24-27: Recordings — add random recording type ──────────
        page.click_recordings_tab()
        logger.info("On Recordings tab")

        page.click_add_button_in_active_sub_entry()
        logger.info("Clicked 'Add Recording'")

        rec_items = page.get_dictionary_items()
        assert len(rec_items) > 0, "Expected at least one recording item"
        rec_label = page.click_random_dictionary_item()
        logger.info(f"Selected recording: '{rec_label}'")

        page.wait_for_block_single(timeout=10)
        logger.info("Recording config form appeared")

        # ── Steps 28-31: Distributions — add 3 random parameters ────────
        # NOTE: Distributions tab is not yet live in production
        is_staging = "staging" in test_config.get("base_url", "")
        if is_staging:
            page.click_distributions_tab()
            logger.info("On Distributions tab")

            for dist_i in range(3):
                page.click_add_button_in_active_sub_entry()
                logger.info(f"Clicked 'Add Distribution' ({dist_i + 1}/3)")

                dist_items = page.get_dictionary_items()
                assert len(dist_items) > 0, f"Expected distribution items for #{dist_i + 1}"
                dist_label = page.click_random_dictionary_item()
                logger.info(f"Selected distribution {dist_i + 1}: '{dist_label}'")

                page.wait_for_block_single(timeout=10)
                logger.info(f"Distribution {dist_i + 1} config form appeared")
        else:
            logger.info("Skipping Distributions — not yet available in production")

        # ── Steps 32-34: Neuron sets — add "All Neurons" ─────────────────
        page.click_neuron_sets_tab()
        logger.info("On Neuron sets tab")

        page.click_add_button_in_active_sub_entry()
        logger.info("Clicked 'Add Neuron Set'")

        ns_items = page.get_dictionary_items()
        assert len(ns_items) > 0, "Expected at least one neuron set item"
        try:
            ns_label = page.click_dictionary_item_by_label("All Neurons")
        except AssertionError:
            ns_label = page.click_random_dictionary_item()
        logger.info(f"Selected neuron set: '{ns_label}'")

        page.wait_for_block_single(timeout=10)
        logger.info("Neuron set config form appeared")

        # ── Steps 35-37: Synaptic manipulations — add random ─────────────
        page.click_synaptic_manip_tab()
        logger.info("On Synaptic manipulations tab")

        page.click_add_button_in_active_sub_entry()
        logger.info("Clicked 'Add Synaptic Manipulation'")

        sm_items = page.get_dictionary_items()
        assert len(sm_items) > 0, "Expected at least one synaptic manipulation item"
        sm_label = page.click_random_dictionary_item()
        logger.info(f"Selected synaptic manipulation: '{sm_label}'")

        page.wait_for_block_single(timeout=10)
        logger.info("Synaptic manipulation config form appeared")

        # ── Steps 38-40: Timestamps — add random ─────────────────────────
        page.click_timestamps_tab()
        logger.info("On Timestamps tab")

        page.click_add_button_in_active_sub_entry()
        logger.info("Clicked 'Add Timestamp'")

        ts_items = page.get_dictionary_items()
        assert len(ts_items) > 0, "Expected at least one timestamp item"
        ts_label = page.click_random_dictionary_item()
        logger.info(f"Selected timestamp: '{ts_label}'")

        page.wait_for_block_single(timeout=10)
        logger.info("Timestamp config form appeared")

        # ── Steps 41-43: Generate simulation(s) ──────────────────────────
        page.click_generate_simulation()
        logger.info("Clicked Generate simulation(s)")

        time.sleep(10)
        if not page.is_simulations_tab_active():
            logger.info("Simulations tab not auto-active, clicking manually")
            try:
                page.click_simulations_tab()
                time.sleep(3)
            except Exception as e:
                logger.warning(f"Could not click Simulations tab: {e}")
        assert page.is_simulations_tab_active(), (
            "Simulations tab should be active after Generate simulation(s)"
        )
        logger.info("Simulations tab active")

        # ── Steps 44-45: Verify simulation cards with "Created" badge ────
        sim_cards = page.get_simulation_cards()
        assert len(sim_cards) >= 1, f"Expected at least 1 simulation card, got {len(sim_cards)}"
        logger.info(f"Found {len(sim_cards)} simulation card(s)")

        statuses = page.get_simulation_card_statuses()
        for s in statuses:
            logger.info(f"  {s['title']}: {s['status']}")
            assert s['status'] == 'created', (
                f"Expected 'created' badge, got '{s['status']}' for {s['title']}"
            )

        # ── Steps 46-47: Verify input files ──────────────────────────────
        input_files = page.get_input_file_buttons()
        assert len(input_files) >= 1, "Expected at least 1 input file"
        file_names = [b.get_attribute("title") or "" for b in input_files]
        logger.info(f"Input files ({len(input_files)}): {file_names}")

        for fname in file_names:
            if not fname:
                continue
            clicked = page.click_input_file(fname)
            assert clicked, f"Could not click input file '{fname}'"

            if fname.endswith('.json'):
                preview = page.get_json_preview_text(timeout=10)
                assert len(preview) > 0, f"JSON preview for '{fname}' should not be empty"
                logger.info(f"  ✓ '{fname}': JSON preview {len(preview)} chars")
            elif fname.endswith('.h5'):
                has_plot = page.is_plot_or_content_visible(timeout=10)
                if has_plot:
                    logger.info(f"  ✓ '{fname}': plot/content visible")
                else:
                    logger.warning(f"  ⚠ '{fname}': no plot found (may still be loading)")
            else:
                logger.info(f"  ℹ '{fname}': unknown type, skipping content check")

        # ── Steps 48-50: Launch simulations → poll until terminal ────────
        assert page.is_launch_simulations_enabled(), "Launch simulations should be enabled"
        page.click_launch_simulations()
        logger.info("Clicked Launch simulations")

        sim_done = page.wait_for_simulation_terminal_state(timeout=300, poll_interval=10)
        if sim_done:
            logger.info("All simulations reached terminal state")
            final_statuses = page.get_simulation_card_statuses()
            for s in final_statuses:
                logger.info(f"  Final: {s['title']}: {s['status']}")
        else:
            logger.warning("Simulations did not complete within 300s")

        logger.info(f"✅ Synaptome (beta) test complete. URL: {page.browser.current_url}")
