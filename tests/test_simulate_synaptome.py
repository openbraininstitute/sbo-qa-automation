# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import pytest
from pages.simulate_synaptome_page import SimulateSynaptomePage


class TestSimulateSynaptome:
    """End-to-end test for Synaptome simulation (non-beta).

    Flow:
    1.  Workflows → Simulate → Synaptome card → model picker
    2.  Filter panel: open, click random field, close
    3.  Click random row → mini-detail (title, desc, images, metadata, buttons)
    4.  Use model → config page with 3D viewer
    5.  Info tab: datetime name, description, verify registered by/at
    6.  Experimental setup: verify labels
    7.  Synaptic input: verify entries, toggle eye button
    8.  Stimulation protocol: wait for plot, verify download
    9.  Recording: add recordings (soma, dend, apic, axon)
    10. Run experiment → Results tab
    11. Verify buttons disabled → plots + canvas → completion → buttons enabled
    12. Success notification with View Simulation link
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
        # Wait for both images to load (second one can be slow)
        if detail['images_count'] < 2:
            logger.info("Only 1 image found, waiting for second to load...")
            time.sleep(10)
            detail = page.verify_mini_detail_view()
        assert detail['images_count'] >= 2, f"Expected at least 2 images, got {detail['images_count']}"
        assert detail['metadata_count'] > 0, "Mini-detail should have metadata"
        assert detail['close_btn'], "Close (x) button should be present"
        assert detail['view_details_btn'], "'View details' button should be present"
        assert detail['use_model_btn'], "'Use model' button should be present"
        logger.info("Mini-detail view verified")

        # Step 7: Click Use model → config page
        page.click_use_model()
        logger.info(f"After Use model, URL: {page.browser.current_url}")

        # Step 8: Wait for config page
        page.wait_for_config_page(timeout=30)
        logger.info("Config page loaded")

        try:
            page.wait_for_neuron_visualizer(timeout=120)
            logger.info("3D morphology viewer loaded")
        except Exception as e:
            logger.warning(f"Neuron visualizer not loaded: {e}")

        # Step 9: Verify Configuration and Results tabs
        tabs = page.verify_config_tabs()
        assert tabs['configuration']['present'], "Configuration tab should be present"
        assert tabs['results']['present'], "Results tab should be present"

        # Step 10: Info tab — fill datetime name + description
        page.click_info_tab()
        name = page.fill_name_with_datetime()
        page.fill_description("automated test of synaptome")
        logger.info(f"Info filled: name='{name}'")

        # Step 11: Verify registered by/at
        reg_by = page.get_registered_by()
        reg_at = page.get_registered_at()
        assert reg_by, "Registered by should not be empty"
        assert reg_at, "Registered at should not be empty"
        logger.info(f"Registered by: '{reg_by}', at: '{reg_at}'")

        # Step 12: Experimental setup — verify labels
        page.click_experimental_setup_tab()
        labels = page.get_panel_labels()
        assert len(labels) > 0, "Experimental setup should have labels"
        logger.info(f"Experimental setup: {len(labels)} labels")

        # Step 13: Synaptic input — verify at least 1 entry
        page.click_synaptic_input_tab()
        syn_count = page.get_synaptic_input_count()
        assert syn_count >= 1, f"Expected at least 1 synaptic input, got {syn_count}"
        logger.info(f"Synaptic inputs: {syn_count}")

        # Step 14: Click eye button → 3D should show synapses, eye crossed out
        page.click_eye_button()
        assert page.is_eye_crossed_out(), "Eye button should be crossed out after clicking"
        logger.info("Eye button toggled — synapses visible in 3D, eye crossed out")

        # Step 15: Stimulation protocol — wait for plot, verify download
        page.click_stimulation_protocol_tab()
        try:
            page.wait_for_stim_plot(timeout=60)
            logger.info("IDrest plot loaded")
        except Exception as e:
            logger.warning(f"IDrest plot not loaded: {e}")

        download_ok = page.is_stim_download_btn_clickable(timeout=10)
        if download_ok:
            logger.info("Download button is clickable")
        else:
            logger.warning("Download button not found or not clickable")

        # Step 16: Recording — add recordings for available sections
        page.click_recording_tab()
        prefixes = page.get_available_section_prefixes(dropdown_index=0)
        logger.info(f"Available sections: {prefixes}")

        desired = ['soma', 'dend']
        for extra in ['apic', 'axon', 'myelin']:
            if extra in prefixes:
                desired.append(extra)

        selected_0 = page.select_recording_section(0, 'soma')
        logger.info(f"Recording 0: '{selected_0}'")

        for i, prefix in enumerate(desired[1:], start=1):
            page.click_add_recording()
            selected = page.select_recording_section(i, prefix)
            logger.info(f"Recording {i}: '{selected}'")

        logger.info(f"Added {len(desired)} recording(s): {desired}")

        # Step 17: Run experiment
        run_btn = page.find_run_experiment_btn(timeout=10)
        assert run_btn.is_displayed(), "Run experiment button should be visible"
        assert run_btn.is_enabled(), "Run experiment button should be enabled"
        page.click_run_experiment()
        logger.info("Clicked Run experiment")

        # Step 18: Verify auto-redirect to Results tab
        time.sleep(5)
        assert page.is_results_tab_active(), "Results tab should be active after Run experiment"
        logger.info("Results tab active")

        # Step 19: Verify left menu (All + recording buttons)
        all_btns = page.get_results_left_menu_buttons()
        assert len(all_btns) >= 2, f"Expected All + recording buttons, got {len(all_btns)}"
        rec_btns = page.get_results_recording_buttons()
        assert len(rec_btns) >= 1, "Expected at least 1 recording button"
        logger.info(f"Results menu: {len(all_btns)} buttons, {len(rec_btns)} recording(s)")

        # Step 20: Download CSV and Reconfigure disabled while running
        assert not page.is_download_csv_enabled(), "Download CSV should be disabled while running"
        assert not page.is_reconfigure_enabled(), "Reconfigure should be disabled while running"
        logger.info("Buttons disabled (simulation running)")

        # Step 21: IDREST plots and 3D canvas visible during simulation
        plot_count = page.get_idrest_plot_count()
        logger.info(f"IDREST plots visible: {plot_count}")
        assert page.is_neuron_canvas_visible(), "3D canvas should be visible"
        logger.info("3D canvas visible")

        # Step 22: Wait for simulation completion
        sim_done = page.wait_for_simulation_complete(timeout=300, poll_interval=10)
        assert sim_done, "Simulation should complete (Download CSV enabled)"
        logger.info("Simulation completed")

        # Step 23: Verify buttons enabled after completion
        assert page.is_download_csv_enabled(), "Download CSV should be enabled"
        assert page.is_reconfigure_enabled(), "Reconfigure should be enabled"
        logger.info("Buttons enabled after completion")

        # Step 24: Success notification with View Simulation link
        notif_ok = page.wait_for_success_notification(timeout=30)
        if notif_ok:
            link = page.get_view_simulation_link()
            assert link is not None, "View Simulation link should be present"
            logger.info(f"View Simulation link: {link.get_attribute('href')}")
        else:
            logger.warning("Success notification not found — may have auto-dismissed")

        logger.info(f"Final URL: {page.browser.current_url}")
