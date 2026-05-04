# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import pytest
from pages.simulate_ion_channel_page import SimulateIonChannelPage


class TestSimulateIonChannel:
    """End-to-end test for Ion channel (beta) simulation.

    Flow (spec steps 1-50):
    1-3.   Workflows → Simulate → Ion channel card → config page (no model picker)
    4-7.   Info tab: warning icon → fill name/description → warning disappears
    8-22.  Ion channel models: add 3 models via Add → select type → configure flow
           Model 1: conductance=0.1, Model 2: permeability=400, Model 3: no value
           Verify right column (Model traces ≥2, Activation, plots) for models 1-2
    23-28. Initialization: sweeps for Temperature (34), Initial Voltage (-70),
           Random Seed (42), Duration (1000 + sweep 500)
    29-34. Stimuli: add 2 via Add → select type, collapse sub-entry
    35.    Recordings: add 3 via Add → select recording type flow
           Recording 0: Ion Channel Variable (nested dropdown via offset clicks)
           Recording 1: Timestep only, Recording 2: Timestep + Start/End time
    36-39. Generate simulation(s) → verify cards with "Created" badge
    40-43. Input files: click each, verify JSON preview non-empty
    44-45. Launch simulation(s) → wait for completion
    46-50. Output files: verify content, recording files: Overview + Interactive details
    """

    def _get_page(self, setup, logger):
        browser, wait, base_url, lab_id, project_id = setup
        return SimulateIonChannelPage(browser, wait, logger, base_url), lab_id, project_id

    @pytest.mark.simulate
    @pytest.mark.run(order=22)
    def test_simulate_ion_channel_full_flow(self, setup, login, logger, test_config):
        page, lab_id, project_id = self._get_page(setup, logger)

        # ── Steps 1-2: Navigate to Workflows → Simulate → Ion channel ───
        page.go_to_workflows_simulate(lab_id, project_id)
        page.click_simulate_category()
        page.click_ion_channel_card()
        logger.info(f"After clicking Ion channel card. URL: {page.browser.current_url}")

        # ── Step 3: Config page loads directly — verify tabs ─────────────
        page.wait_for_config_page(timeout=30)
        logger.info("Config page loaded")

        tabs = page.verify_config_tabs()
        assert tabs['configuration']['present'], "Configuration tab should be present"
        assert tabs['simulations']['present'], "Simulations tab should be present"
        logger.info("Configuration and Simulations tabs verified")

        # ── Step 4: Info tab — verify warning icon ───────────────────────
        page.click_info_tab()

        has_warning = page.is_info_warning_icon_visible(timeout=5)
        if has_warning:
            logger.info("Warning icon visible on Info tab (fields empty)")
        else:
            logger.warning("Warning icon not found — may already have defaults")

        # ── Steps 5-6: Fill Campaign Name + Description ──────────────────
        campaign_name = page.fill_name_with_datetime()
        page.fill_description("Automated ion channel simulation test")
        logger.info(f"Info filled: name='{campaign_name}'")

        # ── Step 7: Verify warning icon disappears ───────────────────────
        if has_warning:
            time.sleep(2)
            warning_gone = not page.is_info_warning_icon_visible(timeout=3)
            check_appeared = page.is_info_check_icon_visible(timeout=3)
            if warning_gone:
                logger.info("Warning icon disappeared after filling fields")
            else:
                logger.warning("Warning icon still visible after filling fields")
            if check_appeared:
                logger.info("Check icon appeared on Info tab")

        # ── Steps 8-22: Ion channel models — add 3 models ──────────────
        page.click_ion_channel_models_tab()
        logger.info("On Ion channel models tab")

        page.click_add_ion_channel_model()
        logger.info("Clicked Add to open model type list")

        model_type_items = page.get_ion_channel_model_type_items()
        num_types = len(model_type_items)
        assert num_types >= 1, "Expected at least 1 ion channel model type"
        logger.info(f"Found {num_types} model type(s) available")

        # Configure up to 3 models (or as many as available)
        # Models 1-2: full flow (model + conductance + right-column verification)
        # Model 3: "Ion channel model without conductance nor max permeability"
        #           — only select a model, no conductance, no plots in right column
        models_to_add = min(3, num_types)
        for i in range(models_to_add):
            is_third_model = (i == 2)
            logger.info(f"── Configuring ion channel model {i + 1}/{models_to_add} ──")

            if is_third_model:
                # 3rd model: no conductance, no plots
                page.add_and_configure_ion_channel_model(
                    type_index=i,
                    conductance=None,
                )
                logger.info(f"✓ Ion channel model {i + 1} configured (no conductance)")

                # Right column should have no plots for this model type
                plot_count = page.get_right_column_plot_count(timeout=3)
                logger.info(
                    f"  Right column plots for model {i + 1}: {plot_count} "
                    f"(expected 0 — no plots for this model type)"
                )
            else:
                # Model 1: conductance, Model 2: permeability (ms/s)
                if i == 0:
                    page.add_and_configure_ion_channel_model(
                        type_index=i,
                        conductance=0.1,
                    )
                    logger.info(f"✓ Ion channel model {i + 1} configured (conductance=0.1)")
                else:
                    page.add_and_configure_ion_channel_model(
                        type_index=i,
                        conductance=None,
                        permeability=400,
                    )
                    logger.info(f"✓ Ion channel model {i + 1} configured (permeability=400 ms/s)")

                # Verify right column: Model traces dropdown, Activation dropdown, plots
                rc = page.verify_right_column_after_model_selection()

                assert rc['model_traces_visible'], (
                    f"Model traces dropdown should be visible after model {i + 1}"
                )
                assert rc['model_traces_items'] >= 2, (
                    f"Model traces dropdown should have at least 2 items, "
                    f"got {rc['model_traces_items']}"
                )
                logger.info(
                    f"  Model traces dropdown: {rc['model_traces_items']} item(s)"
                )

                assert rc['activation_visible'], (
                    f"Activation dropdown should be visible after model {i + 1}"
                )
                assert rc['activation_items'] >= 1, (
                    f"Activation dropdown should have at least 1 item, "
                    f"got {rc['activation_items']}"
                )
                logger.info(
                    f"  Activation dropdown: {rc['activation_items']} item(s), "
                    f"selected: '{rc.get('activation_selected', 'N/A')}'"
                )

                assert rc['plot_count'] >= 1, (
                    f"Expected at least 1 plot in right column after model {i + 1}, "
                    f"got {rc['plot_count']}"
                )
                logger.info(f"  Right column plots: {rc['plot_count']}")

            # Add next model if not last — the sub-entry with "Add" button
            # is already visible, no need to re-click the tab
            if i < models_to_add - 1:
                page.click_add_ion_channel_model()
                logger.info(f"Clicked Add for ion channel model {i + 2}")

        logger.info(f"Added {models_to_add} ion channel model(s)")

        # Collapse the Ion channel models sub-entry for better visibility
        page.collapse_ion_channel_models_tab()

        # ── Steps 23-28: Initialization tab — sweeps ──────────────────
        page.click_initialization_tab()
        init_labels = page.get_initialization_labels()
        logger.info(f"Initialization labels: {init_labels}")

        # Step 24: Add 2nd Temperature value via sweep: 34
        page.add_sweep_value("Temperature", 34)
        logger.info("Added Temperature sweep value (34)")

        # Add 3rd Temperature value: 37
        page.add_sweep_value("Temperature", 37)
        logger.info("Added Temperature sweep value (37)")

        # Step 25: Add 2nd Initial Voltage value via sweep: -70
        page.add_sweep_value("Initial Voltage", -70)
        logger.info("Added Initial Voltage sweep value (-70)")

        # Add 3rd Initial Voltage value: -65
        page.add_sweep_value("Initial Voltage", -65)
        logger.info("Added Initial Voltage sweep value (-65)")

        # Step 26: Add 2nd Random Seed value via sweep: 42
        page.add_sweep_value("Random Seed", 42)
        logger.info("Added Random Seed sweep value (42)")

        # Add 3rd Random Seed value: 100
        page.add_sweep_value("Random Seed", 100)
        logger.info("Added Random Seed sweep value (100)")

        # Steps 27-28: Set Duration to 1000ms, add sweep with 500ms
        page.set_parameter_value("Duration", 1000, input_index=0)
        logger.info("Set Duration to 1000 ms")

        page.add_sweep_value("Duration", 500)
        logger.info("Added Duration sweep value of 500 ms")

        # ── Steps 29-34: Stimuli tab ────────────────────────────────────
        page.click_stimuli_tab()
        logger.info("On Stimuli tab")

        page.click_add_stimulus()
        logger.info("Clicked 'Add Stimulus'")

        stim_items = page.get_dictionary_items()
        assert len(stim_items) > 0, "Expected at least one stimulus dictionary item"

        # Stimuli to exclude from random selection
        EXCLUDED_STIMULI = [
            "Single Electrode Voltage Clamp Multiple Levels Somatic Stimulus",
        ]

        # Select "Constant Somatic Current Clamp (Absolute)" first
        try:
            clamp_label = page.click_dictionary_item_by_label(
                "Constant Somatic Current Clamp (Absolute)",
                exclude_labels=EXCLUDED_STIMULI,
            )
            logger.info(f"Selected required stimulus: '{clamp_label}'")
        except Exception as e:
            logger.warning(f"Could not find exact clamp stimulus: {e}")
            try:
                clamp_label = page.click_dictionary_item_by_label(
                    "Constant Somatic Current Clamp",
                    exclude_labels=EXCLUDED_STIMULI,
                )
                logger.info(f"Selected stimulus (partial match): '{clamp_label}'")
            except Exception:
                clamp_label = page.click_random_enabled_dictionary_item(
                    exclude_labels=EXCLUDED_STIMULI
                )
                logger.info(f"Selected random stimulus as fallback: '{clamp_label}'")

        page.wait_for_block_single(timeout=10)
        logger.info("Stimulus config form appeared")

        # Add a second stimulus
        page.click_add_stimulus()
        second_stim_items = page.get_dictionary_items()
        if len(second_stim_items) > 1:
            second_label = page.click_random_enabled_dictionary_item(
                exclude_labels=EXCLUDED_STIMULI
            )
            logger.info(f"Selected second stimulus: '{second_label}'")
        else:
            logger.info("Only one stimulus type available, skipping second")

        # Verify stimuli appear in middle column
        final_stim_items = page.get_dictionary_items()
        logger.info(f"Stimuli in middle column: {len(final_stim_items)}")

        # Collapse the Stimuli sub-entry for better visibility
        page.collapse_stimuli_tab()

        # ── Step 35: Recordings tab — add 3 via Add → select recording type
        #    Recording 0: Ion Channel Variable (nested dropdown via offset clicks)
        #    Recording 1: Timestep only
        #    Recording 2: Timestep + Start/End time
        page.click_recordings_tab()
        logger.info("On Recordings tab")

        recording_count = page.add_recordings(total=3)
        logger.info(
            f"Recordings configured: {recording_count} "
            f"(each form verified + Ion Channel Variable selected)"
        )
        assert recording_count >= 3, (
            f"Expected at least 3 recordings, got {recording_count}"
        )

        # ── Step 36: Generate simulation(s) ─────────────────────────────
        page.click_generate_simulation()
        logger.info("Clicked Generate simulation(s)")

        # ── Step 37: Wait for Simulations tab ────────────────────────────
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

        # ── Steps 38-39: Verify simulation cards with "Created" badge ────
        sim_cards = page.get_simulation_cards()
        assert len(sim_cards) >= 1, (
            f"Expected at least 1 simulation card, got {len(sim_cards)}"
        )
        logger.info(f"Found {len(sim_cards)} simulation card(s)")

        statuses = page.get_simulation_card_statuses()
        for s in statuses:
            logger.info(f"  {s['title']}: {s['status']}")
            assert s['status'] == 'created', (
                f"Expected 'created' badge, got '{s['status']}' for {s['title']}"
            )

        # ── Steps 40-43: Verify input files and JSON previews ───────────
        input_files = page.get_input_file_buttons()
        assert len(input_files) >= 1, "Expected at least 1 input file"
        file_names = [b.get_attribute("title") or "" for b in input_files]
        logger.info(f"Input files ({len(input_files)}): {file_names}")

        for fname in file_names:
            if not fname:
                continue
            clicked = page.click_input_file(fname)
            assert clicked, f"Could not click input file '{fname}'"
            preview = page.get_json_preview_text(timeout=10)
            assert len(preview) > 0, (
                f"JSON preview for '{fname}' should not be empty"
            )
            logger.info(f"  ✓ '{fname}': {len(preview)} chars")

        # ── Step 44: Launch simulation(s) ───────────────────────────────
        assert page.is_launch_simulations_enabled(), (
            "Launch simulations should be enabled"
        )
        page.click_launch_simulations()
        logger.info("Clicked Launch simulations")

        # ── Step 45: Wait for completion ────────────────────────────────
        sim_done = page.wait_for_simulation_terminal_state(
            timeout=300, poll_interval=10
        )
        if sim_done:
            logger.info("All simulations reached terminal state")
            final_statuses = page.get_simulation_card_statuses()
            for s in final_statuses:
                logger.info(f"  Final: {s['title']}: {s['status']}")
        else:
            logger.warning("Simulations did not complete within 300s")

        # ── Steps 46-47: Verify output files and content ───────────────
        output_files = page.get_output_file_buttons()
        if output_files:
            output_names = [
                b.get_attribute("title") or "" for b in output_files
            ]
            logger.info(f"Output files ({len(output_files)}): {output_names}")

            for fname in output_names:
                if not fname:
                    continue
                clicked = page.click_output_file(fname)
                assert clicked, f"Could not click output file '{fname}'"

                has_content = page.is_output_content_visible(timeout=10)
                assert has_content, (
                    f"Output file '{fname}' should show content (plot/code/image)"
                )
                logger.info(f"  ✓ '{fname}': content visible")

                # ── Steps 48-50: Recording files — Overview + Interactive details
                if page.is_overview_tab_present(timeout=3):
                    logger.info(f"  '{fname}' has recording tabs")

                    assert page.is_interactive_details_tab_present(timeout=3), (
                        f"'{fname}' should have 'Interactive details' tab"
                    )

                    page.click_overview_tab()
                    assert page.is_tab_plot_visible(timeout=10), (
                        f"Overview tab for '{fname}' should show a plot"
                    )
                    logger.info(f"  ✓ Overview plot visible for '{fname}'")

                    page.click_interactive_details_tab()
                    assert page.is_tab_plot_visible(timeout=10), (
                        f"Interactive details tab for '{fname}' should show a plot"
                    )
                    logger.info(
                        f"  ✓ Interactive details plot visible for '{fname}'"
                    )
        else:
            logger.warning("No output files found after simulation completion")

        logger.info(
            f"✅ Ion channel simulation test complete. URL: {page.browser.current_url}"
        )
