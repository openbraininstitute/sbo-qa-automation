# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import pytest
from pages.run_skeletonization_page import RunSkeletonizationPage


class TestRunSkeletonization:
    """End-to-end test for EM mesh skeletonization workflow.

    Flow:
    1.  Workflows → Process Data → EM mesh skeletonization → model picker
    2.  Public tab → verify rows → navigate random page → click random row
    3.  Mini-detail: verify name, description, metadata, buttons → Use model
    4.  Config page: verify Configuration tab active, Info tab active
    5.  Info tab: fill Campaign name (datestamp) + Campaign description ("automated test")
    6.  Initialization tab: verify EM cell mesh not empty, voxel sizes filled, checkbox ticked
    7.  Click Generate skeletonization(s) → Skeletonizations tab active
    8.  Verify cards with "Created" badge, input files, JSON preview
    9.  Click Launch skeletonizations → poll status until terminal (300s)
    """

    def _get_page(self, setup, logger):
        browser, wait, base_url, lab_id, project_id = setup
        return RunSkeletonizationPage(browser, wait, logger, base_url), lab_id, project_id

    @pytest.mark.process_data
    @pytest.mark.run(order=25)
    def test_run_skeletonization_full_flow(self, setup, login, logger, test_config):
        page, lab_id, project_id = self._get_page(setup, logger)

        # Step 1: Navigate to Workflows → Process Data → EM mesh skeletonization
        page.go_to_workflows(lab_id, project_id)
        page.click_process_data_category()
        page.click_em_mesh_skeletonization_card()
        logger.info(f"On model picker. URL: {page.browser.current_url}")

        # Step 2: Public tab → verify table has rows
        page.click_public_tab()
        row_count = page.get_row_count()
        assert row_count > 0, "Expected at least one row in the table"
        # Step 3: Verify pagination and navigate to random page
        page_count = page.get_pagination_page_count()
        if page_count >= 2:
            logger.info(f"Pagination present with {page_count} pages")
            page.navigate_to_random_page()
            logger.info("Navigated to random pagination page")
        else:
            logger.warning(f"Pagination has only {page_count} page(s), skipping random navigation")

        # Step 4: Click random row
        row_text = page.click_random_row()
        logger.info(f"Clicked row: '{row_text}'")

        # Step 5: Mini-detail: verify contents
        page.wait_for_mini_detail()
        detail = page.verify_mini_detail_contents()
        assert detail['title']['present'], "Mini-detail title should be present"
        logger.info(f"Mini-detail title: '{detail['title'].get('text', '')}'")

        if not detail.get('description', {}).get('present'):
            logger.warning("Mini-detail description not found")
        if detail.get('metadata', {}).get('present'):
            logger.info("Mini-detail metadata section present")
        if detail.get('use_model_btn', {}).get('present'):
            logger.info("Mini-detail 'Use model' button present")

        # Step 6: Click Use model → config page
        page.click_use_model()
        logger.info(f"After Use model, URL: {page.browser.current_url}")

        # Step 7: Wait for config page, verify Configuration tab active
        page.wait_for_config_page(timeout=30)
        logger.info("Config page loaded")

        tabs = page.verify_config_tabs()
        assert tabs['configuration']['present'], "Configuration tab should be present"
        assert tabs['skeletonizations']['present'], "Skeletonizations tab should be present"

        config_active = page.is_configuration_tab_active()
        if config_active:
            logger.info("Configuration tab is active")
        else:
            logger.warning("Configuration tab not detected as active")

        # Step 8: Verify Info tab is active
        info_active = page.is_info_tab_active()
        if info_active:
            logger.info("Info tab is active by default")
        else:
            logger.warning("Info tab not detected as active, clicking it")
            page.click_info_tab()

        # Step 9: Fill Campaign name with datestamp, description with "automated test"
        campaign_name = page.fill_name_with_datetime()
        page.fill_description("automated test")
        logger.info(f"Info filled: name='{campaign_name}', description='automated test'")

        # Step 10: Click Initialization tab, verify Info has no warning
        time.sleep(2)
        has_warning = page.is_info_warning_icon_visible(timeout=3)
        if has_warning:
            logger.warning("Warning icon still visible on Info tab after filling fields")
        else:
            logger.info("No warning icon on Info tab — fields filled correctly")

        page.click_initialization_tab()
        logger.info("Clicked Initialization tab")

        # Step 11: Verify Initialization title and description
        init_info = page.verify_initialization_title_and_description()
        if init_info['description']:
            logger.info("Initialization description present: 'Parameters for initializing the skeletonization'")

        # Step 12: Verify EM cell mesh fields are not empty
        mesh_values = page.get_em_cell_mesh_values()
        assert mesh_values['id'] or mesh_values['name'], \
            "EM cell mesh should have at least ID or name pre-filled"
        logger.info(f"EM cell mesh — ID: '{mesh_values['id']}', Name: '{mesh_values['name']}'")

        # Step 13: Verify Neuron voxel size is filled
        neuron_voxel = page.get_neuron_voxel_size_value()
        assert neuron_voxel, "Neuron voxel size should be filled"
        logger.info(f"Neuron voxel size: '{neuron_voxel}'")

        # Step 14: Verify Spine voxel size is filled
        spine_voxel = page.get_spine_voxel_size_value()
        assert spine_voxel, "Spine voxel size should be filled"
        logger.info(f"Spine voxel size: '{spine_voxel}'")

        # Step 15: Verify Include full resolution spines checkbox is ticked
        spines_checked = page.is_include_full_res_spines_checked()
        assert spines_checked, "Include full resolution spines should be ticked by default"
        logger.info("Include full resolution spines checkbox is ticked")

        # Step 16: Click Generate skeletonization(s)
        page.click_generate_skeletonization()
        logger.info("Clicked Generate skeletonization(s)")

        # Step 17: Verify Skeletonizations tab becomes active
        time.sleep(10)
        if not page.is_skeletonizations_tab_active():
            logger.info("Skeletonizations tab not auto-active, clicking it manually")
            try:
                page.click_skeletonizations_tab()
                time.sleep(3)
            except Exception as e:
                logger.warning(f"Could not click Skeletonizations tab: {e}")
        assert page.is_skeletonizations_tab_active(), \
            "Skeletonizations tab should be active after Generate"
        logger.info("Skeletonizations tab active")

        # Step 18: Verify Select all is present
        select_all_ok = page.verify_select_all_present()
        if select_all_ok:
            logger.info("Select all checkbox present and ticked")

        # Step 19: Verify skeletonization cards with "Created" badge
        skel_cards = page.get_skeletonization_cards()
        assert len(skel_cards) >= 1, f"Expected at least 1 skeletonization card, got {len(skel_cards)}"
        logger.info(f"Found {len(skel_cards)} skeletonization card(s)")

        statuses = page.get_skeletonization_card_statuses()
        for s in statuses:
            logger.info(f"  {s['title']}: {s['status']}")
            assert s['status'] == 'created', \
                f"Expected 'created' badge, got '{s['status']}' for {s['title']}"

        # Step 20: Verify input files — obi_one_coordinate.json
        input_files = page.get_input_file_buttons()
        assert len(input_files) >= 1, "Expected at least 1 input file"
        file_names = [b.get_attribute("title") or b.text.strip() for b in input_files]
        logger.info(f"Input files: {file_names}")

        # Click obi_one_coordinate.json and verify JSON preview
        clicked = page.click_input_file("obi_one_coordinate.json")
        assert clicked, "Could not click obi_one_coordinate.json"

        preview = page.get_json_preview_text(timeout=10)
        assert len(preview) > 0, "JSON preview for obi_one_coordinate.json should not be empty"
        logger.info(f"JSON preview: {len(preview)} chars")

        # Step 21: Verify Launch skeletonizations button is enabled with count
        assert page.is_launch_skeletonizations_enabled(), \
            "Launch skeletonizations button should be enabled"
        launch_count = page.get_launch_skeletonizations_count()
        assert launch_count == len(skel_cards), \
            f"Launch count ({launch_count}) should match card count ({len(skel_cards)})"
        logger.info(f"Launch skeletonizations({launch_count}) matches card count")

        # Step 22: Click Launch skeletonizations
        page.click_launch_skeletonizations()
        logger.info("Clicked Launch skeletonizations")

        # Step 23: Verify cost modal appears
        modal_title = page.verify_cost_modal_title(timeout=10)
        assert modal_title, "Cost modal should appear with title"
        logger.info(f"Cost modal title: '{modal_title}'")

        # Step 24: Verify modal shows skeletonization item with checkbox and credits
        modal_items = page.get_cost_modal_items()
        assert len(modal_items) >= 1, "Modal should show at least 1 skeletonization item"
        logger.info(f"Modal items: {modal_items}")

        # Step 25: Toggle the checkbox (untick and re-tick)
        page.toggle_cost_modal_checkbox(index=0)
        logger.info("Unticked modal checkbox")
        time.sleep(0.5)
        page.toggle_cost_modal_checkbox(index=0)
        logger.info("Re-ticked modal checkbox")

        # Step 26: Verify total credits displayed
        total_credits = page.get_cost_modal_total_credits()
        logger.info(f"Total credits: '{total_credits}'")

        # Step 27: Verify Cancel and Confirm buttons present
        assert page.is_cost_modal_cancel_present(), "Cancel button should be present"
        assert page.is_cost_modal_confirm_present(), "Confirm button should be present"

        # Step 28: Click Confirm
        page.click_cost_modal_confirm()
        logger.info("Clicked Confirm in cost modal")

        # Step 29: Handle consent tab (opens and auto-closes after ~5s)
        page.handle_consent_tab(timeout=15)
        logger.info("Consent tab handled, back on skeletonization page")

        # Step 30: Poll status until terminal state (done/error) — 900s timeout (can take 10+ min)
        skel_done = page.wait_for_skeletonization_terminal_state(timeout=900, poll_interval=15)
        if skel_done:
            logger.info("All skeletonizations reached terminal state")
            final_statuses = page.get_skeletonization_card_statuses()
            for s in final_statuses:
                logger.info(f"  Final: {s['title']}: {s['status']}")
        else:
            logger.warning("Skeletonizations did not complete within 300s")

        # Step 31: Verify output file(s) appear after completion
        output_files = page.get_output_file_buttons(timeout=15)
        if output_files:
            output_names = [b.get_attribute("title") or b.get_attribute("data-file-name") or "" for b in output_files]
            logger.info(f"Output files: {output_names}")

            # Click the first output file (Skeletonized morphology)
            clicked = page.click_output_file("Skeletonized morphology")
            if clicked:
                # Step 32: Verify preview card content
                preview = page.verify_output_preview()
                assert preview['title'], "Output preview should have a title"
                logger.info(f"Output preview title: '{preview['title']}'")
                if preview['description']:
                    logger.info(f"Output description: '{preview['description'][:60]}'")
                if preview['image_visible']:
                    logger.info("Output morphology image is visible")
                if preview['metadata_count'] > 0:
                    logger.info(f"Output metadata fields: {preview['metadata_count']}")

                # Step 33: Verify action buttons
                buttons = page.verify_output_action_buttons()
                assert buttons.get('copy_id'), "Copy ID button should be present"
                assert buttons.get('download'), "Download button should be present"
                assert buttons.get('view_details'), "View details button should be present"
                logger.info("All output action buttons present")

                # Step 34: Click View details → redirects to detail view
                href = page.click_output_view_details()
                logger.info(f"Clicked View details, navigated to: {page.browser.current_url}")
                assert "data/view" in page.browser.current_url, \
                    f"Should redirect to detail view, got: {page.browser.current_url}"
            else:
                logger.warning("Could not click Skeletonized morphology output file")
        else:
            logger.warning("No output files found after skeletonization completion")

        logger.info(f"✅ Skeletonization test complete. Final URL: {page.browser.current_url}")
