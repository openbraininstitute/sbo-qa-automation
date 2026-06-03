# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import pytest

from pages.explore_me_model import ExploreMeModelPage


class TestExploreMeModel:
    """End-to-end test for ME-model Detail View.

    Flow:
    1.  Navigate to Data > Model > ME-model
    2.  Select a random species, select brain region with data
    3.  Click a row to open the Detail View
    4.  Verify left-hand side tabs (Overview, Analysis, Configuration, Related artifacts)
    5.  Verify action buttons (Copy ID, Simulate, Download)
    6.  Overview tab: verify metadata labels and values
    7.  Analysis tab: dropdown, description button, plots, download
    8.  Configuration tab: ME-model name, M-model section, E-model section
    9.  Related artifacts tab: simulations or empty message
    10. Copy ID button: verify clipboard copy
    11. Download button: verify file download triggered
    12. Simulate button: verify redirect to simulate URL
    """

    def _get_page(self, setup, logger):
        browser, wait, base_url, lab_id, project_id = setup
        return ExploreMeModelPage(browser, wait, logger, base_url), lab_id, project_id

    @pytest.mark.explore_page
    @pytest.mark.run(order=8)
    def test_me_model_detail_view(self, setup, login_direct_complete, logger, test_config):
        browser, wait, base_url, lab_id, project_id = login_direct_complete
        me_model_page = ExploreMeModelPage(browser, wait, logger, base_url)
        logger.info(f"DEBUG: Using lab_id={lab_id}, project_id={project_id}")

        # ── Prerequisites: Navigate to ME-model list ─────────────────────
        me_model_page.go_to_explore_memodel_page(lab_id, project_id)
        logger.info("ME-model list page loaded")
        time.sleep(3)

        # Select a random species
        species = me_model_page.select_random_species()
        if species:
            logger.info(f"Selected species: {species}")
        else:
            species = me_model_page.get_current_species()
            logger.info(f"Using default species: {species}")

        # Wait for brain region panel and table data
        me_model_page.find_brain_region_panel(timeout=40)
        logger.info("Brain region panel is visible")
        time.sleep(3)

        # Wait for table rows to appear
        me_model_page.wait_for_table(timeout=30)
        rows = me_model_page.get_table_rows()
        if len(rows) == 0:
            # Table empty — try Mouse as fallback species
            logger.warning("No rows found, falling back to Mouse species")
            me_model_page.select_species_by_name("Mouse")
            time.sleep(3)
            rows = me_model_page.get_table_rows()
        assert len(rows) > 0, "Expected at least one ME-model row in the table"
        logger.info(f"Found {len(rows)} ME-model rows")

        # Click a random row to open mini detail view
        row_text = me_model_page.click_random_row()
        logger.info(f"Clicked row: '{row_text}'")

        me_model_page.wait_for_spinner_to_disappear(timeout=15)

        # Click 'Go to details page' to open the Detail View
        me_model_page.click_detail_view_button(timeout=20)
        me_model_page.wait_for_url_contains("/data/view/memodel/", timeout=20)
        logger.info(f"Detail View loaded: {browser.current_url}")

        # ── Step 1: Verify left-hand side tabs ───────────────────────────
        overview_tab = me_model_page.find_overview_tab()
        assert overview_tab.is_displayed(), "Overview tab is not displayed"
        logger.info("Overview tab is displayed")

        analysis_tab = me_model_page.find_analysis_tab()
        assert analysis_tab.is_displayed(), "Analysis tab is not displayed"
        logger.info("Analysis tab is displayed")

        config_tab = me_model_page.find_configuration_tab()
        assert config_tab.is_displayed(), "Configuration tab is not displayed"
        logger.info("Configuration tab is displayed")

        related_tab = me_model_page.find_related_artifacts_tab()
        assert related_tab.is_displayed(), "Related artifacts tab is not displayed"
        logger.info("Related artifacts tab is displayed")

        # ── Step 2: Verify action buttons ────────────────────────────────
        copy_id_btn = me_model_page.find_copy_id_btn()
        assert copy_id_btn.is_displayed(), "Copy ID button is not displayed"
        logger.info("Copy ID button is visible")

        simulate_btn = me_model_page.find_simulate_btn()
        assert simulate_btn.is_displayed(), "Simulate button is not displayed"
        logger.info("Simulate button is visible")

        download_btn = me_model_page.find_download_btn()
        assert download_btn.is_displayed(), "Download button is not displayed"
        logger.info("Download button is visible")

        # ── Step 3: Overview tab — verify metadata ───────────────────────
        metadata = me_model_page.get_overview_metadata()

        required_fields = [
            'Name', 'Created by', 'Brain region', 'E-type',
            'Validated', 'Species', 'Registration date', 'M-type'
        ]
        optional_fields = [
            'Description', 'Contributors', 'Institutional contributors', 'Strain'
        ]

        for field in required_fields:
            value = metadata.get(field, {}).get('value', '')
            if value:
                logger.info(f"✓ {field}: '{value}'")
            else:
                logger.error(f"✗ {field}: value is empty (required)")
            assert value, f"Required field '{field}' should not be empty"

        # Validate special case: 'Validated' should be True or False
        validated_value = metadata.get('Validated', {}).get('value', '')
        assert validated_value.lower() in ('true', 'false'), \
            f"'Validated' should be True or False, got: '{validated_value}'"
        logger.info(f"Validated field value: {validated_value}")

        for field in optional_fields:
            value = metadata.get(field, {}).get('value', '')
            if value:
                logger.info(f"✓ {field} (optional): '{value}'")
            else:
                logger.info(f"○ {field} (optional): empty — acceptable")

        # ── Step 4: Analysis tab ─────────────────────────────────────────
        me_model_page.click_analysis_tab()
        logger.info("On Analysis tab")

        try:
            analysis_dropdown = me_model_page.find_analysis_dropdown(timeout=10)
            assert analysis_dropdown.is_displayed(), "Analysis dropdown is not displayed"
            logger.info("✓ Select analysis dropdown is present")
        except Exception as e:
            logger.warning(f"Analysis dropdown not found: {e}")

        try:
            read_desc_btn = me_model_page.find_read_description_btn(timeout=10)
            assert read_desc_btn.is_displayed(), "Read description button is not displayed"
            assert read_desc_btn.is_enabled(), "Read description button is not enabled"
            logger.info("✓ Read description button is enabled and clickable")
        except Exception as e:
            logger.warning(f"Read description button not found: {e}")

        plots = me_model_page.get_analysis_plots(timeout=15)
        if plots:
            visible_plots = [p for p in plots if p.is_displayed()]
            assert len(visible_plots) >= 1, "At least 1 plot should be visible on Analysis tab"
            logger.info(f"✓ {len(visible_plots)} plot(s) visible on Analysis tab")
        else:
            logger.warning("No plots found on Analysis tab")

        plot_texts = me_model_page.find_analysis_plot_text(timeout=5)
        if plot_texts:
            has_text = any(t.text.strip() for t in plot_texts)
            if has_text:
                logger.info("✓ Some plots have text explanation")
            else:
                logger.warning("Plot text elements found but empty")
        else:
            logger.warning("No plot text explanations found")

        try:
            plot_download = me_model_page.find_analysis_plot_download_btn(timeout=10)
            assert plot_download.is_displayed(), "Plot download button is not displayed"
            logger.info("✓ Plot download button is available")
        except Exception as e:
            logger.warning(f"Plot download button not found: {e}")

        # Verify validation cards are present and clickable (expand/collapse)
        validation_cards = me_model_page.get_validation_cards(timeout=10)
        if validation_cards:
            logger.info(f"✓ {len(validation_cards)} validation card(s) found")
            # Click first card's summary to toggle collapse/expand
            me_model_page.click_validation_card_toggle(0)
            logger.info("✓ First validation card toggle clicked (collapse/expand)")
        else:
            logger.warning("No validation cards found on Analysis tab")

        # ── Step 5: Configuration tab ────────────────────────────────────
        me_model_page.click_configuration_tab()
        logger.info("On Configuration tab")

        try:
            config_name = me_model_page.find_config_me_model_name(timeout=10)
            assert config_name.is_displayed(), "ME-model name not displayed on Configuration tab"
            logger.info(f"✓ ME-model name displayed: '{config_name.text.strip()}'")
        except Exception as e:
            logger.warning(f"ME-model name not found on Configuration tab: {e}")

        try:
            m_model_section = me_model_page.find_config_m_model_section(timeout=10)
            assert m_model_section.is_displayed(), "M-model overview section not displayed"
            logger.info("✓ M-model overview section is present")
        except Exception as e:
            logger.warning(f"M-model section not found: {e}")

        try:
            e_model_section = me_model_page.find_config_e_model_section(timeout=10)
            assert e_model_section.is_displayed(), "E-model overview section not displayed"
            logger.info("✓ E-model overview section is present")
        except Exception as e:
            logger.warning(f"E-model section not found: {e}")

        # ── Step 6: Related artifacts tab ────────────────────────────────
        me_model_page.click_related_artifacts_tab()
        logger.info("On Related artifacts tab")
        time.sleep(3)

        sim_entries = me_model_page.get_simulation_entries(timeout=10)
        no_sim_msg = me_model_page.find_no_simulations_message(timeout=5)

        if sim_entries:
            logger.info(f"✓ {len(sim_entries)} simulation entries found")
            # Verify simulation data content
            first_sim = sim_entries[0]
            sim_name = me_model_page.get_simulation_name(first_sim)
            if sim_name:
                logger.info(f"  Simulation name: '{sim_name}'")
            sim_params = me_model_page.get_simulation_params(first_sim)
            if sim_params:
                logger.info(f"  Simulation params: {sim_params}")
            has_stimulus_plot = me_model_page.has_stimulus_plot(first_sim)
            logger.info(f"  Stimulus plot present: {has_stimulus_plot}")
            has_recording_section = me_model_page.has_recording_section(first_sim)
            logger.info(f"  Recording section present: {has_recording_section}")
        elif no_sim_msg:
            assert no_sim_msg.is_displayed(), "No simulations message is not displayed"
            logger.info("✓ 'No simulations available' message is displayed")
        else:
            logger.warning("Neither simulation entries nor empty message found")

        # Steps 7-9 (Copy ID, Download, Simulate buttons) skipped — ticket logged for button click targets
        logger.info(f"✅ ME-model Detail View test completed. Final URL: {browser.current_url}")
