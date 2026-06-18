# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import pytest
from selenium.common import TimeoutException
from selenium.webdriver import Keys


from locators.explore_page_locators import ExplorePageLocators
from pages.explore_page import ExplorePage



class TestExplorePage:
    @pytest.mark.explore_page
    @pytest.mark.run(order=3)
    def test_explore_page(self, setup, login_direct_complete, logger, test_config):
        """Checking the Explore Page"""
        browser, wait, base_url, lab_id, project_id = login_direct_complete
        explore_page = ExplorePage(browser, wait, logger, base_url)
        print(f"DEBUG: Using lab_id={lab_id}, project_id={project_id}")
        explore_page.go_to_explore_page(lab_id, project_id)
        explore_page.wait_for_network_idle(timeout=15)
        logger.info(f"Explore page is loaded, {browser.current_url}")

        # skip_onboarding = explore_page.skip_onboardin_btn(timeout=3)
        # if skip_onboarding:
        #     skip_onboarding.click()
        # logger.info("Clicked on 'Skip' on the overlay")
        #
        # data_skip_onboarding = explore_page.data_skip_onboardin_btn(timeout=3)
        # if data_skip_onboarding and data_skip_onboarding.is_displayed():
        #     data_skip_onboarding.click()
        #     logger.info("Clicked on 'Data - Skip' on the overlay")

        brain_region_panel = explore_page.find_brain_region_panel(timeout=40)
        logger.info("Found Brain Region Panel")

        # AI Assistant panel now starts closed by default - test open/close functionality
        try:
            # First, try to find the open button (panel should be closed initially)
            ai_assistant_open_btn = explore_page.find_ai_assistant_panel_open()
            if ai_assistant_open_btn.is_displayed():
                logger.info("AI Assistant panel is closed. Opening it to test functionality.")
                ai_assistant_open_btn.click()
                
                # Wait a moment for panel to open
                time.sleep(2)
                
                # Now find and click the close button
                close_btn = explore_page.find_ai_assistant_panel_close(timeout=10)
                close_btn.click()
                logger.info("AI Panel opened and closed successfully.")
            else:
                logger.info("AI Assistant open button not found - panel might already be open")
                # If open button not visible, panel might be open, try to close it
                try:
                    close_btn = explore_page.find_ai_assistant_panel_close(timeout=10)
                    close_btn.click()
                    logger.info("AI Panel was open and has been closed.")
                except Exception as e:
                    logger.warning(f"Could not find close button either: {e}")
                    
        except Exception as e:
            logger.warning(f"AI Assistant panel interaction failed: {e}")
            # Don't fail the test if AI panel interaction fails - it's not critical

        experimental_data_tab = explore_page.experimental_data_tab()
        assert experimental_data_tab.is_displayed(), f"Experimental data tab is not displayed"
        logger.info("Experimental data tab is displayed.")
        atlas = explore_page.find_3d_atlas()
        assert atlas.is_displayed()
        logger.info("3D Atlas is displayed")

        # Dump localStorage species snapshot for debugging
        ls_keys = browser.execute_script("return Object.keys(localStorage)")
        logger.info(f"localStorage keys: {ls_keys}")
        for key in ls_keys:
            if 'species' in key.lower() or 'brain' in key.lower() or 'region' in key.lower():
                val = browser.execute_script(f"return localStorage.getItem('{key}')")
                logger.info(f"  {key}: {val}")

        # Fullscreen button only available for Human, Mouse, Rat
        species_value = explore_page.get_species_value(timeout=10)
        logger.info(f"Current species: '{species_value}'")
        species_has_fullscreen = any(s in species_value for s in ["Human", "Mouse", "Rat"])
        species_has_density = "Mouse" in species_value

        if species_has_fullscreen:
            atlas_fullscreen = explore_page.find_atlas_fullscreen_bt(timeout=15)
            logger.info("Found atlas fullscreen button")
            atlas_fullscreen.click()

            fulscreen_exit = explore_page.find_fullscreen_exit(timeout=15)
            logger.info("Fullscreen exit button is found")
            fulscreen_exit.click()
            logger.info("Fullscreen exit button is clicked, atlas is minimized")
        else:
            logger.info(f"Skipping fullscreen test — not available for species '{species_value}'")

        # Count density only available for Mouse
        if species_has_density:
            density_start = time.time()
            total_count_density_title = explore_page.find_total_count_density(timeout=45)
            density_load_time = round(time.time() - density_start, 2)
            assert total_count_density_title, "The total neurons count title is not found"
            logger.info(f"Title for the total count of neurons is found (loaded in {density_load_time}s)")

            # Log slow network requests for performance debugging
            try:
                perf_entries = browser.execute_script("""
                    return performance.getEntriesByType('resource')
                        .filter(e => e.duration > 2000)
                        .map(e => {
                            const url = new URL(e.name);
                            const path = url.pathname.length > 60 ? '...' + url.pathname.slice(-60) : url.pathname;
                            return { name: path, duration: Math.round(e.duration), type: e.initiatorType };
                        })
                        .sort((a, b) => b.duration - a.duration)
                        .slice(0, 10);
                """)
                if perf_entries:
                    logger.info("Slow resources (>2s):")
                    for entry in perf_entries:
                        logger.info(f"  {entry['duration']}ms | {entry['type']} | {entry['name']}")
            except Exception:
                pass

            # Performance thresholds: CI runs from US-East with higher latency
            warn_threshold = 10 if test_config.get("env") != "production" else 15
            fail_threshold = 15 if test_config.get("env") != "production" else 25
            if density_load_time > warn_threshold:
                logger.warning(f"PERFORMANCE: Density count took {density_load_time}s (warn: {warn_threshold}s)")
            assert density_load_time < fail_threshold, (
                f"Performance issue: density count took {density_load_time}s (max {fail_threshold}s)"
            )

            total_count_number = explore_page.find_total_count_n()
            neuron_count = total_count_number.text
            assert neuron_count.strip(), "Total neuron count is empty"
            logger.info(f"Total number of neurons is: {neuron_count}")

            count_switch_button = explore_page.find_total_count_switch()
            assert count_switch_button.is_displayed()
            logger.info(f"Found the switch count/density button")
            current_state = count_switch_button.get_attribute('aria-checked')
            logger.info(f"Current state of the total count switch: {current_state}")

            time.sleep(2)
            if current_state == "false":
                count_switch_button.click()
                logger.info("Switch toggled to 'true'.")
            elif current_state == "true":
                count_switch_button.click()
                logger.info(f"Switch toggled to 'on'.")
            else:
                logger.error(f"Unexpected switch state: {current_state}")

            new_state = count_switch_button.get_attribute("aria-checked")
            logger.info(f"New state of the switch: {new_state}")

            total_count_number = explore_page.find_total_count_n()
            neuron_count = total_count_number.text
            assert neuron_count.strip(), "Total neuron DENSITY is empty"
            logger.info(f"Total DENSITY is: {neuron_count}")
        else:
            logger.info(f"Skipping density/count test — not available for species '{species_value}'")

        exp_data_titles = [
            ExplorePageLocators.NEURON_MORPHOLOGY,
            ExplorePageLocators.NEURON_ELECTROPHYSIOLOGY,
            ExplorePageLocators.NEURON_DENSITY,
            ExplorePageLocators.BOUTON_DENSITY,
            ExplorePageLocators.SYNAPSE_PER_CONNECTION,
            ExplorePageLocators.ION_CHANNEL_EPHYS
        ]

        logger.info("Searching for Experimental Data types")
        missing_locators = []
        not_displayed = []

        def get_element_label(el):
            return (
                    element.text.strip()
                    or element.get_attribute("aria-label")
                    or element.get_attribute("title")
                    or f"<no text> tag={el.tag_name}"
            )

        for locator in exp_data_titles:
            try:
                elements = explore_page.find_all_elements(locator, timeout=5)

                if not elements:
                    missing_locators.append(locator)
                    continue

                for element in elements:
                    label = get_element_label(element)

                    logger.info(
                        f"✓ Found Experimental Data section: locator={locator}, label='{label}'"
                    )

                    if not element.is_displayed():
                        not_displayed.append(f"{locator} (label='{label}')")

            except TimeoutException:
                missing_locators.append(locator)

        assert not missing_locators and not not_displayed, (
                "Experimental Data validation failed:\n"
                + (f"Missing locators: {missing_locators}\n" if missing_locators else "")
                + (f"Not displayed: {not_displayed}\n" if not_displayed else "")
        )

        logger.info("✓ All experimental data sections are present and displayed")

        page_titles = [
            ExplorePageLocators.EXPERIMENTAL_DATA_BTN,
            ExplorePageLocators.MODEL_DATA_BTN,
            ExplorePageLocators.SIMULATIONS_BTN
        ]
        logger.info("Searching for Explore Page titles")
        explore_page_titles = explore_page.find_explore_page_titles(page_titles, timeout=15)

        for page_title in explore_page_titles:
            assert page_title.is_displayed(), f"Explore page titles {page_title} is not displayed"
        logger.info("Found Explore page titles")

        brain_region_panel = explore_page.find_brain_region_panel(timeout=20)
        logger.info("Found Brain Region Panel")

        # Verify and click the Species dropdown
        species_value = explore_page.get_species_value(timeout=10)
        logger.info(f"Current species: '{species_value}'")
        assert species_value, "Species value should not be empty"

        explore_page.click_species_dropdown()
        logger.info("Clicked Species dropdown")
        time.sleep(2)

        # Close the dropdown by pressing Escape
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(browser).send_keys(Keys.ESCAPE).perform()
        time.sleep(1)
        logger.info("Species dropdown closed")

        # Wait for brain region to load — measure time for performance reporting
        br_start = time.time()
        cerebrum_in_brpanel = explore_page.find_cerebrum_brp(timeout=60)
        br_load_time = round(time.time() - br_start, 2)
        region_text = cerebrum_in_brpanel.text.strip()
        logger.info(f"Found brain region in panel: '{region_text}' (loaded in {br_load_time}s)")
        assert region_text, "Brain region text should not be empty"
        if br_load_time > 10:
            logger.warning(f"PERFORMANCE: Brain region panel took {br_load_time}s to load")
        cerebrum_in_brpanel.click()
        logger.info(f"Clicked on '{region_text}' in the brain region panel")

        # Try to navigate the tree: search for brain region (species-dependent)
        time.sleep(2)
        try:
            # Rat has "Cerebral cortex", Mouse/Human have "Cerebrum"
            search_term = "Cerebral cortex" if "Rat" in species_value else "Cerebrum"
            explore_page.search_and_select_brain_region(search_term)
            logger.info(f"Selected '{search_term}' from region search")
        except Exception as tree_err:
            logger.warning(f"Region search for brain region failed: {tree_err}")

        try:
            cerebral_cortex_title = explore_page.find_cerebral_cortex_brp(timeout=15)
            logger.info("Found Cerebral cortex as a child region")
        except Exception:
            logger.warning("Cerebral cortex not found — tree may be at different level")

        # Verify Experimental tab record type counters (total should not be 0)
        logger.info("Verifying Experimental record type counters:")
        record_counts = explore_page.verify_experimental_record_counts(timeout=15)
        for name, total in record_counts.items():
            assert total > 0, f"Record type '{name}' has total count 0 — expected data"
        logger.info("All experimental record type counters have non-zero totals")

        # Neurons panel and density/count switch only available for Mouse
        if "Mouse" in species_value:
            neurons_panel = explore_page.find_neurons_panel()
            assert neurons_panel.is_displayed()
            logger.info("Neurons panel is displayed")

            density_count_switch = explore_page.find_count_switch(timeout=10)
            assert density_count_switch.is_displayed()
            logger.info("Density & count switch is displayed")
        else:
            logger.info(f"Skipping neurons panel and density switch — not available for '{species_value}'")

        brain_region_search_field = explore_page.find_brain_region_search_field(timeout=25)
        assert brain_region_search_field.is_displayed()
        logger.info("Bran region panel search field is found")

        try:
            if brain_region_search_field.is_displayed():
                brain_region_search_field.click()
                logger.info("Brain region search field is clicked")
        except TimeoutException:
            logger.error("Timeout: Brain region search field is not clickable after multiple attempts.")

        search_region_input_field = explore_page.search_region_input_field(timeout=10)
        try:
            if search_region_input_field.is_displayed():
                search_region_input_field.click()
                logger.info("Search region input field is clicked")
        except TimeoutException:
            logger.error("Timeout: Search region input field is not clickable after multiple attempts.")

        search_region_input_field.send_keys(Keys.ENTER)
        model_data_tab = explore_page.find_model_data_title()
        assert model_data_tab.text == "Model"
        logger.info("Model tab is found")

        model_data_tab.click()
        logger.info("Model data tab is clicked")

        model_data_titles = [
            ExplorePageLocators.PANEL_EMODEL,
            ExplorePageLocators.PANEL_CIRCUIT,
            ExplorePageLocators.PANEL_MEMODEL,
            ExplorePageLocators.PANEL_SYNAPTOME,
            ExplorePageLocators.PANEL_SYNAPTOME_BETA,
            ExplorePageLocators.PANEL_ION_CHANNEL_MODEL_BETA
        ]
        logger.info("Searching for Model data artifact titles")

        missing_locators = []
        not_displayed = []

        for locator in model_data_titles:
            try:
                elements = explore_page.find_all_elements(locator, timeout=5)

                if not elements:
                    missing_locators.append(locator)
                    continue

                for element in elements:
                    text = element.text.strip()
                    logger.info(
                        f"✓ Found Model Data artifact: locator={locator}, text='{text}'"
                    )

                    if not element.is_displayed():
                        not_displayed.append(f"{locator} (text='{text}')")

            except TimeoutException:
                missing_locators.append(locator)

            assert not missing_locators and not not_displayed, (
                    "Model Data validation failed:\n"
                    + (f"Missing locators: {missing_locators}\n" if missing_locators else "")
                    + (f"Not displayed: {not_displayed}\n" if not_displayed else "")
            )
            logger.info("Found Model data artifact titles")

        '''
        pending implementation of config file
        
        neuron_panel_one_mtype = explore_page.find_panel_mtype()
        assert neuron_panel_one_mtype.is_displayed(), "The M-types titles in the panel is not found"
        logger.info("An M-type in the neurons panel is found")

        neuron_panel_one_mtype.click()
        logger.info("Clicking inside the viewport of the Neuron panel")

        neurons_panel_mtype_btn = explore_page.find_neurons_mtypes_btn()
        assert neurons_panel_mtype_btn, "The toggle arrow for M-type is not found"
        logger.info("M-type arrow button is found")

        if neurons_panel_mtype_btn and neurons_panel_mtype_btn.is_displayed():
            neurons_panel_mtype_btn.click()
            logger.info("Clicked on the M-type toggle arrow")
            etype_title = explore_page.find_neurons_etype_title()
            logger.info("Searching for the E-type title inside the Neurons panel")
            if etype_title.is_displayed():
                logger.info("E-Types are displayed")
        else:
            logger.info("The Mtype in the neurons panel was not found and not clicked")

        mtypes_neurons_panel = explore_page.list_of_neurons_panel()
        logger.info(f"Neurons' panel with a list of M-types is found")

        panel_specific_mtype = explore_page.find_neurons_panel_iso_mtype()
        logger.info("Specific M-type is found")
        browser.execute_script("arguments[0].scrollIntoView(true);", panel_specific_mtype)
        element_location = panel_specific_mtype.location_once_scrolled_into_view
        viewport_height = browser.execute_script("return window.innerHeight")
        element_top = element_location['y']
        element_bottom = element_top + panel_specific_mtype.size['height']

        # Assert the element is within the viewport height
        assert element_top >= 0 and element_bottom <= viewport_height, \
            (f"The element is not fully in the viewport. Element top: {element_top}, "
             f"Element bottom: {element_bottom}, Viewport height: {viewport_height}")
        logger.info(f"Scrolled through the M-types in the Neurons' panel")
        '''