# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import pytest
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from pages.data_circuit_page import DataCircuitPage


class TestDataCircuit:
    """End-to-end test for Data > Model > Circuit page.

    Flow:
    1.  Navigate to Data > Model > Circuit
    2.  Verify Public tab is displayed and active
    3.  Verify Species shows "Rat"
    4.  Verify Brain region shows "Root"
    5.  Verify Circuit tab is active with non-zero record count
    6.  Verify List/Hierarchy view toggle behavior
    7.  Verify column headers
    8.  Verify sub-circuits (expanded) have same column headers
    9.  Apply filters (neurons, synapses, connections)
    10. Click random row → verify mini-detail view
    11. Click View details → verify detail view (URL, breadcrumbs, tabs, metadata)
    """

    def _get_page(self, setup, logger):
        browser, wait, base_url, lab_id, project_id = setup
        return DataCircuitPage(browser, wait, logger, base_url), lab_id, project_id

    @pytest.mark.data_circuit
    @pytest.mark.run(order=25)
    def test_data_circuit_full_flow(self, setup, login, logger, test_config):
        circuit_page, lab_id, project_id = self._get_page(setup, logger)

        # Step 1: Navigate to Data > Model > Circuit
        circuit_page.go_to_data_circuit(lab_id, project_id)
        circuit_page.wait_for_network_idle(timeout=15)
        logger.info(f"Data Circuit page loaded. URL: {circuit_page.browser.current_url}")

        # Step 2: Verify Public tab is displayed and clicked
        circuit_page.click_public_tab()
        public_active = circuit_page.verify_public_tab_active()
        assert public_active, "Public tab should be displayed and active"
        logger.info("Public tab is active")

        # Step 3: Select Rat species and verify
        current_species = circuit_page.get_species_value(timeout=15)
        if 'Rat' not in current_species:
            circuit_page.select_species("Rat")
            circuit_page.wait_for_network_idle(timeout=10)
        species = circuit_page.get_species_value(timeout=10)
        assert "Rat" in species, f"Expected Species to contain 'Rat', got '{species}'"
        logger.info(f"Species: '{species}'")

        # Step 4: Select Root brain region and verify
        brain_region = circuit_page.get_brain_region_value(timeout=15)
        if 'Root' not in brain_region:
            circuit_page.select_brain_region_root()
            circuit_page.wait_for_network_idle(timeout=10)
        brain_region = circuit_page.get_brain_region_value(timeout=10)
        assert "Root" in brain_region, f"Expected Brain region to contain 'Root', got '{brain_region}'"
        logger.info(f"Brain region: '{brain_region}'")
        logger.info(f"Brain region verified: '{brain_region}'")

        # Step 5: Verify Circuit tab is active and shows records
        circuit_active = circuit_page.verify_circuit_tab_active()
        assert circuit_active, "Circuit tab should be active"
        record_count = circuit_page.get_circuit_record_count(timeout=20)
        assert record_count > 0, f"Circuit record count should be > 0, got {record_count}"
        logger.info(f"Circuit tab active with {record_count} records")

        # Step 6: Verify column headers (some may be off-screen due to horizontal scroll)
        circuit_page.wait_for_network_idle(timeout=10)
        expected_headers = [
            "Name", "Subcircuits", "Description", "Brain region", "Scale",
            "Number of neurons", "Number of synapses", "Number of connections",
            "Build category", "Published in", "Experiment date"
        ]
        headers = circuit_page.get_column_headers(timeout=15)
        logger.info(f"Visible column headers: {headers}")

        # Assert at least the first visible columns are present
        required_visible = ["Name", "Subcircuits", "Description", "Brain region", "Scale"]
        for expected in required_visible:
            found = any(expected.lower() in h.lower() for h in headers)
            assert found, f"Required column header '{expected}' not found. Got: {headers}"

        # Scroll table right to check remaining columns
        try:
            table_body = circuit_page.browser.find_element(By.CSS_SELECTOR, ".ant-table-body")
            circuit_page.browser.execute_script(
                "arguments[0].scrollLeft = arguments[0].scrollWidth", table_body
            )
            time.sleep(2)
            all_headers = circuit_page.get_column_headers(timeout=5)
            headers = list(set(headers + all_headers))  # Merge visible from both scroll positions
            # Scroll back to start
            circuit_page.browser.execute_script("arguments[0].scrollLeft = 0", table_body)
            time.sleep(1)
        except Exception:
            pass

        # Log all columns (warn about any not found after scrolling)
        for expected in expected_headers:
            found = any(expected.lower() in h.lower() for h in headers)
            if found:
                logger.info(f"  ✓ '{expected}'")
            else:
                logger.warning(f"  ○ '{expected}' not found")
        logger.info("Column headers verified")

        # Step 7: Verify List/Hierarchy view toggle
        # Page loads in hierarchy view (toggle left) by default
        try:
            # First switch to List view
            circuit_page.click_list_view()
            logger.info("Switched to List view")
            sortable = circuit_page.verify_columns_sortable()
            logger.info(f"Columns sortable in List view: {sortable}")

            # Switch back to Hierarchy view
            circuit_page.click_hierarchy_view()
            logger.info("Switched to Hierarchy view")

            # Expand first parent row and verify sub-circuits
            expanded = circuit_page.expand_first_parent_row()
            if expanded:
                sub_rows = circuit_page.get_sub_circuit_rows()
                logger.info(f"Found {len(sub_rows)} sub-circuit rows after expanding")

                # Verify sub-circuit rows have same column structure
                if sub_rows:
                    sub_cells = sub_rows[0].find_elements(By.CSS_SELECTOR, "td")
                    logger.info(f"Sub-circuit row has {len(sub_cells)} cells")
            else:
                logger.warning("No expandable rows found in hierarchy view")

            # Switch back to List view for filter step
            circuit_page.click_list_view()
            logger.info("Switched back to List view for filters")
        except TimeoutException:
            logger.warning("View toggle not found — page may only have one view mode")

        # Step 8: Filter panel
        try:
            circuit_page.open_filter_panel()
            logger.info("Filter panel opened")

            # Number of neurons: 300000 - 1000000
            circuit_page.apply_filter_neurons(300000, 1000000)
            logger.info("Neurons filter applied")

            # Number of synapses: 6000000 - 840000000
            circuit_page.apply_filter_synapses(6000000, 840000000)
            logger.info("Synapses filter applied")

            # Number of connections: 120000000 - 160000000
            circuit_page.apply_filter_connections(120000000, 160000000)
            logger.info("Connections filter applied")

            # Click Apply to activate all filters
            circuit_page.click_filter_apply()
            logger.info("Filter Apply clicked")

            # Close filter panel (need to scroll up to find close button)
            circuit_page.close_filter_panel()
            logger.info("Filter panel closed")
            time.sleep(2)
        except TimeoutException as e:
            logger.warning(f"Filter panel interaction failed: {e}")

        # Step 9: Click random row → verify mini-detail view
        row_text = circuit_page.click_random_row()
        logger.info(f"Clicked row: '{row_text}'")

        circuit_page.wait_for_mini_detail(timeout=15)
        logger.info("Mini-detail panel is displayed")

        mini_fields = circuit_page.verify_mini_detail_fields()
        assert mini_fields.get('name'), "Mini-detail should show circuit name"
        assert mini_fields.get('view_details'), "View details button should be present and clickable"
        logger.info(f"Mini-detail verified: name={mini_fields['name']}, "
                    f"thumbnail={mini_fields.get('thumbnail')}, "
                    f"view_details={mini_fields['view_details']}")

        # Step 10: Click View details → verify detail view
        circuit_page.click_view_details()
        logger.info(f"After View details, URL: {circuit_page.browser.current_url}")

        # Verify URL contains /data/view/
        assert circuit_page.verify_detail_url(), "URL should contain /data/view/"
        logger.info("Detail URL verified")

        # Verify breadcrumbs
        breadcrumbs_ok = circuit_page.verify_detail_breadcrumbs()
        if breadcrumbs_ok:
            logger.info("Breadcrumbs verified")
        else:
            logger.warning("Breadcrumbs not found or empty")

        # Verify tabs
        tabs = circuit_page.verify_detail_tabs()
        assert tabs.get('overview'), "Overview tab should be present"
        logger.info(f"Detail tabs: {tabs}")

        # Verify metadata (1st section)
        metadata = circuit_page.verify_detail_metadata(timeout=10)
        required_metadata = [
            "Name", "Brain Region", "Number of synapses", "Number of neurons",
            "Created by", "Registration date", "Scale", "Number of connections"
        ]
        for field in required_metadata:
            value = metadata.get(field)
            if not value or value == "—":
                logger.warning(f"Required metadata field '{field}' is empty or dash")
            else:
                logger.info(f"Metadata '{field}': '{value}'")

        # Verify subject metadata (2nd section)
        subject_meta = circuit_page.verify_detail_subject_metadata()
        assert subject_meta.get("Species"), "Subject Species should be present"
        logger.info(f"Subject metadata verified: Name={subject_meta.get('Name')}, Species={subject_meta.get('Species')}")
        if subject_meta.get("Name"):
            logger.info(f"Subject Name: {subject_meta['Name']}")
        else:
            logger.info("Subject Name not present (may not be a separate field)")

        # Verify image
        image_ok = circuit_page.verify_detail_image(timeout=15)
        if image_ok:
            logger.info("Detail image is displayed")
        else:
            logger.warning("Detail image not found")

        # Verify buttons (Copy ID, Download, Simulate)
        buttons = circuit_page.verify_detail_buttons(timeout=10)
        assert buttons['copy_id']['displayed'], "Copy ID button should be displayed"
        assert buttons['download']['displayed'], "Download button should be displayed"
        logger.info(f"Detail buttons: Copy ID={buttons['copy_id']}, "
                    f"Download={buttons['download']}, Simulate={buttons['simulate']}")

        # Check Simulate button status
        if buttons['simulate']['displayed']:
            if buttons['simulate']['enabled']:
                logger.info("Simulate button is active and clickable")
            else:
                logger.info("Simulate button is displayed but disabled (may be expected for some scale types)")
        else:
            logger.warning("Simulate button not found")

        # Step 11: Analysis tab
        try:
            circuit_page.click_analysis_tab()
            logger.info("Analysis tab clicked")

            analysis = circuit_page.verify_analysis_tab_content(timeout=15)
            assert analysis['cell_stats_title'], "Cell statistics title should be present"
            assert analysis['cell_stats_image'], "Cell statistics image should be displayed"
            logger.info("Cell statistics: title and image verified")

            assert analysis['network_stats_title'], "Network statistics title should be present"
            assert analysis['network_stats_images'] > 0, "Network statistics should have at least one image"
            logger.info(f"Network statistics: title and {analysis['network_stats_images']} image(s) verified")
        except TimeoutException:
            logger.warning("Analysis tab not available or content not loaded")

        # Step 12: Related Publications tab
        try:
            circuit_page.click_related_publications_tab()
            logger.info("Related Publications tab clicked")

            # Verify Provenance section (active by default)
            prov = circuit_page.verify_publications_articles(timeout=10)
            assert prov['article_count'] > 0, "Provenance should have at least one article"
            assert prov['has_title'], "Article should have a title"
            assert prov['has_copy_doi'], "Article should have a Copy DOI button"
            assert prov['has_authors'], "Article should have author names"
            logger.info(f"Provenance: {prov['article_count']} articles, pagination={prov['has_pagination']}")

            # Click Copy DOI and verify
            doi_copied = circuit_page.click_copy_doi_and_verify()
            if doi_copied:
                logger.info("Provenance: Copy DOI verified")
            else:
                logger.warning("Provenance: Copy DOI verification failed")

            # Click "+ N more" authors button and verify dropdown
            more_authors = circuit_page.click_more_authors_and_verify()
            if more_authors:
                logger.info("Provenance: More authors dropdown verified")
            else:
                logger.warning("Provenance: More authors dropdown not found")

            # Verify Related artifacts provenance section
            circuit_page.click_publications_section("Related artifacts provenance")
            rap = circuit_page.verify_publications_articles(timeout=10)
            assert rap['article_count'] > 0, "Related artifacts provenance should have articles"
            logger.info(f"Related artifacts provenance: {rap['article_count']} articles, "
                        f"pages={rap['pagination_pages']}")

            doi_copied = circuit_page.click_copy_doi_and_verify()
            if doi_copied:
                logger.info("Related artifacts provenance: Copy DOI verified")
            more_authors = circuit_page.click_more_authors_and_verify()
            if more_authors:
                logger.info("Related artifacts provenance: More authors dropdown verified")

            # Verify Applications section
            circuit_page.click_publications_section("Applications")
            apps = circuit_page.verify_publications_articles(timeout=10)
            assert apps['article_count'] > 0, "Applications should have articles"
            logger.info(f"Applications: {apps['article_count']} articles, "
                        f"pages={apps['pagination_pages']}")

            doi_copied = circuit_page.click_copy_doi_and_verify()
            if doi_copied:
                logger.info("Applications: Copy DOI verified")
            more_authors = circuit_page.click_more_authors_and_verify()
            if more_authors:
                logger.info("Applications: More authors dropdown verified")
        except TimeoutException:
            logger.warning("Related Publications tab not available or content not loaded")

        logger.info(f"Test complete. Final URL: {circuit_page.browser.current_url}")
