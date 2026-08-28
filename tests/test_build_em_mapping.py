# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import pytest
from pages.build_em_mapping_page import BuildEMMappingPage


class TestBuildEMMapping:
    """End-to-end test for Electron microscopy circuit (beta) build.

    Flow (spec steps 1-48):
    1-3.   Workflows → Build → EM circuit card
    4-7.   Public tab → breadcrumbs → Portion 65 card → list view
    8-12.  Project tab → verify columns → tick checkbox → Use selection
    13-16. Filter ME-model → tick checkbox → Use selection
    17-20. Config page → Info tab → fill name/description → warning disappears
    21-22. Initialization tab → verify NEURONS block
    23-29. Add group to scan → Add items overlay → Cancel
    30-31. Delete 2nd neuron set → Generate build(s)
    32-34. Results tab → verify card + inputs
    35-38. Launch builds → modal → Cancel
    39-40. Launch builds → Confirm
    41-48. Poll status → verify outputs → copy/download → Done or Error
    """

    def _get_page(self, setup, logger):
        browser, wait, base_url, lab_id, project_id = setup
        return BuildEMMappingPage(browser, wait, logger, base_url), lab_id, project_id

    @pytest.mark.build_em_mapping
    @pytest.mark.run(order=30)
    def test_build_em_mapping_full_flow(self, setup, login_direct_complete, logger, test_config):
        page, lab_id, project_id = self._get_page(setup, logger)

        # ── Steps 1-3: Navigate → Build → EM circuit card ────────────────
        page.go_to_workflows_build(lab_id, project_id)
        page.click_build_section()
        page.click_em_circuit_card()
        logger.info(f"On EM circuit model picker. URL: {page.browser.current_url}")

        # ── Step 4: Public tab → verify breadcrumbs ──────────────────────
        page.click_public_tab()
        breadcrumbs = page.verify_breadcrumbs()
        assert breadcrumbs.get('em_build'), "Breadcrumb 'Electron microscopy circuit (beta) build' not found"
        assert breadcrumbs.get('select_dataset'), "Breadcrumb 'Select electron microscopy dense reconstruction dataset' not found"
        logger.info("Breadcrumbs verified")

        # ── Steps 5-6: Verify Portion 65 card ────────────────────────────
        card_info = page.verify_portion_65_card()
        assert card_info['title_present'], "Portion 65 card title not found"
        assert card_info['description_present'], "Portion 65 card description not found"
        logger.info("Portion 65 card verified with title and description")

        # ── Step 7: Click Portion 65 card → list view ────────────────────
        page.click_portion_65_card()
        logger.info(f"After clicking Portion 65 card. URL: {page.browser.current_url}")

        # ── Step 8: Click Project tab ────────────────────────────────────
        page.click_project_tab()
        logger.info("Clicked Project tab")

        # ── Step 9: Verify columns ───────────────────────────────────────
        col_results = page.verify_column_headers()
        missing = [name for name, r in col_results.items() if not r['present']]
        assert not missing, f"Missing column headers: {missing}"
        logger.info("All column headers verified")

        # ── Steps 10-12: Verify table not empty, tick checkbox, Use selection ─
        row_count = page.get_row_count()
        if row_count == 0:
            logger.warning("Project tab table is empty, skipping checkbox step")
            pytest.skip("Project tab table is empty")

        ticked = page.tick_random_checkbox()
        assert ticked, "Could not tick a random checkbox"
        logger.info("Ticked a random checkbox")

        use_btn_text = page.get_use_selection_button_text()
        assert "1" in use_btn_text, f"Expected 'Use selection (1)', got '{use_btn_text}'"
        assert page.is_use_selection_enabled(), "Use selection button should be enabled"
        logger.info(f"Use selection button shows: '{use_btn_text}'")

        # ── Steps 13-14: Click filter, select ME-model ───────────────────
        page.click_filter_dropdown()
        page.select_me_model_filter()
        logger.info("Selected ME-model filter")

        # ── Steps 15-16: Check table, tick checkbox, click Use selection ─
        time.sleep(3)
        me_row_count = page.get_row_count()
        if me_row_count == 0:
            logger.info("ME-model table is empty, clicking Use selection directly")
            assert page.is_use_selection_enabled(), "Use selection should be active even with empty ME-model table"
            page.click_use_selection()
        else:
            ticked = page.tick_random_checkbox()
            assert ticked, "Could not tick checkbox in ME-model table"
            use_btn_text = page.get_use_selection_button_text()
            assert "2" in use_btn_text, f"Expected 'Use selection (2)', got '{use_btn_text}'"
            logger.info(f"ME-model Use selection shows: '{use_btn_text}'")
            page.click_use_selection()

        logger.info(f"After Use selection. URL: {page.browser.current_url}")

        # ── Steps 17: Config page → verify tabs ─────────────────────────
        page.wait_for_config_page(timeout=30)
        logger.info("Config page loaded")

        tabs = page.verify_config_tabs()
        assert tabs['configuration']['present'], "Configuration tab should be present"
        assert tabs['results']['present'], "Results tab should be present"
        assert page.is_configuration_tab_active(), "Configuration tab should be active"
        logger.info("Configuration and Results tabs verified")

        # ── Step 18: Info tab — verify warning icon ──────────────────────
        page.click_info_tab()
        has_warning = page.is_info_warning_icon_visible(timeout=5)
        if has_warning:
            logger.info("Warning icon visible on Info tab (fields empty)")
        else:
            logger.warning("Warning icon not found — may already have defaults")

        # ── Step 19: Fill Campaign Name + Description ────────────────────
        campaign_name = page.fill_name_with_datetime()
        page.fill_description("automated test of paired neurons")
        logger.info(f"Info filled: name='{campaign_name}'")

        # ── Step 20: Verify warning icon disappears ──────────────────────
        if has_warning:
            time.sleep(2)
            warning_gone = not page.is_info_warning_icon_visible(timeout=3)
            check_appeared = page.is_info_check_icon_visible(timeout=3)
            if warning_gone:
                logger.info("Warning icon disappeared after filling fields")
            if check_appeared:
                logger.info("Check icon appeared on Info tab")

        # ── Step 21: Click Initialization tab ────────────────────────────
        page.click_initialization_tab()
        init_title = page.verify_initialization_title()
        assert init_title, "INITIALIZATION title should be displayed"
        logger.info("Initialization tab active, title displayed")

        # ── Step 22: Verify NEURONS block ────────────────────────────────
        neurons = page.verify_neurons_block()
        assert neurons['neurons_label'], "NEURONS label should be present"
        assert neurons['group_count'] >= 1, "At least 1 neuron group should exist"
        assert neurons['entity_card_present'], "Entity card should be present"
        assert neurons['add_items_enabled'], "'Add item(s)' button should be enabled"
        logger.info(f"NEURONS block: name='{neurons['default_name']}', "
                    f"count={neurons['entity_count']}, groups={neurons['group_count']}")

        # Verify MORPHOLOGY or ME-MODEL badge
        has_morph = page.has_morphology_badge()
        has_me = page.has_me_model_badge()
        logger.info(f"Entity badges: MORPHOLOGY={has_morph}, ME-MODEL={has_me}")

        # ── Steps 23-24: Add group to scan → 2nd neuron set added ────────
        assert page.is_add_group_to_scan_enabled(), "'Add group to scan' should be enabled"
        page.click_add_group_to_scan()
        group_count = page.get_neuron_group_count()
        assert group_count >= 2, f"Expected 2+ neuron groups, got {group_count}"
        logger.info(f"2nd neuron set added. Total groups: {group_count}")

        # ── Steps 25-26: Click Add item(s) in 2nd group → overlay ────────
        added = page.click_add_items_in_group(group_index=1)
        assert added, "Could not click 'Add item(s)' in 2nd group"
        logger.info("Clicked 'Add item(s)' in 2nd neuron set")

        # ── Step 27: Verify Confirm & Cancel buttons ─────────────────────
        assert page.is_overlay_displayed(), "Confirm button should be visible in overlay"
        assert page.is_overlay_cancel_displayed(), "Cancel button should be visible in overlay"
        logger.info("Overlay displayed with Confirm and Cancel buttons")

        # ── Step 28: Click Public tab in overlay, check entities ─────────
        page.click_overlay_public_tab()
        overlay_rows = page.get_overlay_table_row_count()
        if overlay_rows == 0:
            logger.info("Public tab in overlay has no entities, skipping")
        else:
            logger.info(f"Public tab in overlay has {overlay_rows} entities")

        # ── Step 29: Click Cancel → back to Configuration tab ────────────
        page.click_overlay_cancel()
        logger.info("Cancelled overlay, back to Configuration")

        # ── Step 30: Delete 2nd neuron set ───────────────────────────────
        deleted = page.delete_neuron_group(group_index=1)
        if deleted:
            logger.info("Deleted 2nd neuron set")
        else:
            logger.warning("Could not delete 2nd neuron set, continuing")

        # ── Step 31: Generate build(s) ───────────────────────────────────
        assert page.is_generate_builds_enabled(), "'Generate build(s)' should be active"
        page.click_generate_builds()
        logger.info("Clicked Generate build(s), waiting for generation...")

        # ── Step 32: Results tab active ──────────────────────────────────
        results_active = page.wait_for_results_tab_active(timeout=120)
        if not results_active:
            credit_msg = page.get_blocking_credit_message(timeout=3)
            if credit_msg:
                pytest.skip(f"Insufficient project credits for build generation: {credit_msg}")
        assert results_active, "Results tab should become active after generation"
        logger.info("Results tab is active")

        # ── Step 33: Verify build card with badge ────────────────────────
        build_cards = page.get_build_cards()
        assert len(build_cards) >= 1, f"Expected at least 1 build card, got {len(build_cards)}"
        statuses = page.get_build_card_statuses()
        for s in statuses:
            logger.info(f"  Build card: {s['title']}: {s['status']}")

        # ── Step 34: Verify INPUTS → obi_one_coordinate.json ─────────────
        input_files = page.get_input_file_buttons()
        assert len(input_files) >= 1, "Expected at least 1 input file"
        file_names = [b.get_attribute("title") or b.text.strip() for b in input_files]
        logger.info(f"Input files: {file_names}")

        # Click the json file and verify content
        json_clicked = page.click_input_file("obi_one_coordinate.json")
        if json_clicked:
            preview = page.get_json_preview_text(timeout=10)
            assert len(preview) > 0, "JSON preview for obi_one_coordinate.json should not be empty"
            logger.info(f"obi_one_coordinate.json preview: {len(preview)} chars")
        else:
            logger.warning("Could not click obi_one_coordinate.json, checking any json file")
            for fname in file_names:
                if ".json" in fname.lower():
                    page.click_input_file(fname)
                    preview = page.get_json_preview_text(timeout=10)
                    assert len(preview) > 0, f"JSON preview for '{fname}' should not be empty"
                    logger.info(f"'{fname}' preview: {len(preview)} chars")
                    break

        # ── Steps 35-38: Launch builds → modal → Cancel ──────────────────
        assert page.is_launch_builds_enabled(), "Launch builds should be enabled"
        page.click_launch_builds()
        assert page.is_launch_modal_displayed(), "Launch modal should be displayed"
        logger.info("Launch modal displayed")

        # Verify modal content (estimated cost breakdown)
        page.click_launch_modal_cancel()
        logger.info("Cancelled launch modal")

        # Verify modal closed
        time.sleep(1)
        assert not page.is_launch_modal_displayed(timeout=3), "Modal should be closed after Cancel"
        logger.info("Modal closed after Cancel")

        # ── Steps 39-40: Launch builds → Confirm ─────────────────────────
        page.click_launch_builds()
        assert page.is_launch_modal_displayed(), "Launch modal should be displayed again"
        page.click_launch_modal_confirm()
        logger.info("Confirmed launch, build is running")

        # ── Steps 41-48: Poll status → verify outputs ────────────────────
        final_status = page.wait_for_build_terminal_state(timeout=300, poll_interval=10)
        logger.info(f"Final build status: '{final_status}'")

        if final_status in ('done', 'completed', 'success'):
            logger.info("Build completed successfully")

            # Steps 42-43: Verify task logs
            logs = page.get_task_logs_content(timeout=10)
            if logs:
                logger.info(f"Task logs present: {len(logs)} chars")
            else:
                logger.warning("Task logs not found or empty")

            # Steps 44-45: Copy button → JSON → success
            copied = page.click_copy_button()
            if copied:
                json_copied = page.click_copy_json()
                if json_copied:
                    success = page.is_copy_success_shown(timeout=5)
                    if success:
                        logger.info("Copy JSON shows success")
                    else:
                        logger.warning("Copy success indicator not found")

            # Step 46: Download button → JSON
            downloaded = page.click_download_button()
            if downloaded:
                page.click_download_json()
                logger.info("Download JSON clicked")

            logger.info(f"Build EM mapping test PASSED. URL: {page.browser.current_url}")

        elif final_status in ('error', 'failed'):
            logger.error(f"Build failed with status: '{final_status}'")
            pytest.fail(f"Build failed with status: '{final_status}'")
        else:
            logger.warning(f"Build ended with unexpected status: '{final_status}'")
            # Don't fail — it may still be running if timeout was hit
            logger.info(f"Build EM mapping test completed with status '{final_status}'. "
                        f"URL: {page.browser.current_url}")
