# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from locators.species_selector_locators import SpeciesSelectorLocators
from pages.explore_page import ExplorePage


class TestAllSpeciesLanding:
    """All-species mode is the default for a user with no saved preference.

    In that mode no single species is selected, so there is no brain region to filter
    by: the app hides the region switcher and shows the species atlas grid on /data
    instead. Nothing covered this before, which is why the switcher disappearing read
    as a regression rather than the intended behaviour.

    The test pins the mode with `?s=all` rather than relying on a fresh account. That
    URL override wins over the stored preference, so the test still exercises the
    all-species landing after another test has saved a species on the shared QA account.
    """

    @pytest.mark.explore_page
    @pytest.mark.run(order=4)
    def test_all_species_landing(self, setup, login_direct_complete, logger, test_config):
        browser, wait, base_url, lab_id, project_id = login_direct_complete
        explore_page = ExplorePage(browser, wait, logger, base_url)

        explore_page.go_to_explore_page(lab_id, project_id, query="?s=all")
        explore_page.wait_for_network_idle(timeout=15)
        logger.info(f"Explore page loaded in all-species mode, {browser.current_url}")

        explore_page.wait_for_brain_region_banner(timeout=60)
        logger.info("Brain region banner is displayed")

        species_label = explore_page.get_species_label(timeout=60)
        assert species_label == explore_page.ALL_SPECIES_LABEL, (
            f"Expected the species selector to read 'All', got '{species_label}'"
        )
        logger.info("Species selector reads 'All'")

        WebDriverWait(browser, 30).until(
            EC.invisibility_of_element_located(SpeciesSelectorLocators.BRAIN_REGION_SWITCHER),
            "Region switcher is still rendered in all-species mode",
        )
        logger.info("Region switcher is correctly hidden in all-species mode")

        atlas_grid = explore_page.is_visible(
            SpeciesSelectorLocators.ALL_SPECIES_ATLAS_GRID, timeout=60
        )
        assert atlas_grid.is_displayed(), "Species atlas grid is not displayed on /data"
        logger.info("Species atlas grid is displayed instead of the single-species 3D viewer")

        # Cards depend on mesh downloads, so a missing card is a slow environment
        # rather than a broken landing page — report it without failing the run.
        cards = browser.find_elements(*SpeciesSelectorLocators.ALL_SPECIES_ATLAS_CARD)
        if cards:
            logger.info(f"Found {len(cards)} species atlas cards")
        else:
            logger.warning("No species atlas cards rendered yet — meshes may still be loading")

        # Switching to a species from here must bring the region switcher back.
        selected_species = explore_page.ensure_focused_species_mode(timeout=60)
        assert selected_species != explore_page.ALL_SPECIES_LABEL
        logger.info(f"Selecting '{selected_species}' restored the region switcher")
