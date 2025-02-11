# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute

# SPDX-License-Identifier: Apache-2.0

import time
import os.path
import pytest
from selenium.webdriver import Keys, ActionChains

from locators.explore_page_locators import ExplorePageLocators
from pages.explore_page import ExplorePage

current_directory = os.getcwd()
relative_file_path = 'scraped_links.txt'
file_path = os.path.join(current_directory, relative_file_path)


class TestExplorePage:
    @pytest.mark.explore_page
    @pytest.mark.run(order=3)
    def test_explore_page(self, setup, login, logger):
        browser, wait, base_url = setup
        explore_page = ExplorePage(browser, wait, base_url)
        """
        Dynamic lab and project IDs
        """
        lab_id = "37a3a2e8-a4b4-456b-8aff-4e23e87a5cbc"
        project_id = "8abcb1e3-b714-4267-a22c-3b3dc4be5306"
        current_url = explore_page.go_to_explore_page(lab_id, project_id)

        # explore_page.go_to_explore_page()
        logger.info("Explore page is loaded")

        """Checking the titles of the Explore Page"""
        explore_page.check_explore_title_is_present()
        logger.info("Explore page title is present")
        cerebrum_title = explore_page.cerebrum_title()
        assert cerebrum_title, f"Cerebrum title is not found"
        logger.info("Cerebrum title is displayed")
        # time.sleep(3320)
        exp_data_titles = [
            ExplorePageLocators.NEURON_MORPHOLOGY,
            ExplorePageLocators.NEURON_ELECTROPHYSIOLOGY,
            ExplorePageLocators.NEURON_DENSITY,
            ExplorePageLocators.BOUTON_DENSITY,
            ExplorePageLocators.SYNAPSE_PER_CONNECTION
        ]
        logger.info("Searching for Experimental Data types")
        exp_data_elements = explore_page.find_experimental_data_titles(exp_data_titles)

        found_titles = [element.text for element in exp_data_elements]
        logger.info(f"Found experimental data titles: {found_titles}")
        for element in exp_data_elements:
            assert element.is_displayed(), f"Experimental data {element} is not displayed."
        logger.info("Found Experimental data titles")

        page_titles = [
            ExplorePageLocators.EXPERIMENTAL_DATA_BTN,
            ExplorePageLocators.MODEL_DATA_BTN,
            ExplorePageLocators.LITERATURE
        ]
        logger.info("Searching for Explore Page titles")
        explore_page_titles = explore_page.find_explore_page_titles(page_titles)

        for page_title in explore_page_titles:
            assert page_title.is_displayed(), f"Explore page titles {page_title} is not displayed"
        logger.info("Found Explore page titles")

        record_count_locators = [
            ExplorePageLocators.MORPHOLOGY_NRECORDS,
            ExplorePageLocators.NEURON_EPHYS_NRECORDS,
            ExplorePageLocators.NEURON_DENSITY_NRECORDS,
            ExplorePageLocators.BOUTON_DENSITY_NRECORDS,
            ExplorePageLocators.SYNAPSE_PER_CONNECTION_NRECORDS
        ]
        record_counts = explore_page.get_experiment_record_count(record_count_locators)
        for record_count in record_counts:
            assert record_count >= 1, f"Record count is less than 100: {record_count}"
        logger.info("Number of records for data types are displayed")

        brain_region_panel = explore_page.find_brain_region_panel()
        logger.info("Found Brain Region Panel")

        cerebrum_in_brpanel = explore_page.find_cerebrum_brp()
        logger.info("Found Cerebrum in the brain region panel")

        cerebrum_arrow_btn = explore_page.find_cerebrum_arrow_btn()
        logger.info("Cerebrum - parent arrow button is clicked")
        browser.execute_script("arguments[0].click();", cerebrum_arrow_btn)

        cerebral_cortex_title = explore_page.find_cerebral_cortex_brp()
        logger.info("Found Cerebral cortex as a child of Cerebrum")

        neurons_panel = explore_page.find_neurons_panel()
        assert neurons_panel.is_displayed()
        logger.info("Neurons panel is displayed")

        density_count_switch = explore_page.find_count_switch()
        assert density_count_switch.is_displayed()
        logger.info("Density & count switch is displayed")

        brain_region_search_field = explore_page.find_brain_region_search_field(timeout=25)
        assert brain_region_search_field.is_displayed()
        logger.info("Bran region panel search field is found")
        brain_region_search_field.send_keys(Keys.ENTER)
        find_input_file_and_wait = ExplorePageLocators.SEARCH_REGION
        explore_page.wait_for_long_load(find_input_file_and_wait)
        logger.info("Waiting for page to load")

        brain_region_search_field.send_keys("Isocortex")
        logger.info("Searching for 'Isocortex'")
        brain_region_search_field.send_keys(Keys.ENTER)
        selected_brain_region_title = explore_page.find_selected_brain_region_title()
        assert selected_brain_region_title.text == 'Isocortex'
        logger.info("Found 'Isocortex' in the brain region panel and the title is displayed ")
        explore_page.wait_for_page_ready(timeout=20)
        logger.info("Wait for the sorting action to complete.")
        model_data_tab = explore_page.find_model_data_title()
        assert model_data_tab.text == "Model data"
        logger.info("Model data tab is found")

        model_data_tab.click()
        logger.info("Model data tab is clicked")
        expected_panel = explore_page.find_data_panel()
        assert expected_panel.is_displayed(), \
            "Model data panel did not appear after clicking the tab."
        logger.info("Model data panel is displayed after clicking the tab.")

        panel_emodel = explore_page.find_panel_emodel()
        logger.info("E-model is found in the types panel")

        panel_memodel = explore_page.find_panel_memodel()
        logger.info("ME-model is found in the types panel")

        panel_synaptome = explore_page.find_panel_synaptome()
        logger.info("Synaptome is found in the types panel")

        liteture_tab = explore_page.literature_title().click()
        logger.info("Found and clicked on Literature tab")

        expected_panel = explore_page.find_data_panel()
        assert expected_panel.is_displayed(), \
            "Literature data panel did not appear after clicking the tab."
        logger.info("Literature data panel is displayed after clicking the tab.")

        literature_panel_data_titles = [
            ExplorePageLocators.LITERATURE_MORPHOLOGY_TAB,
            ExplorePageLocators.LITERATURE_EPHYS_TAB,
            ExplorePageLocators.LITERATURE_NDENSITY_TAB,
            ExplorePageLocators.LITERATURE_BDENSITY_TAB,
            ExplorePageLocators.LITERATURE_SYNAPSES_TAB
        ]
        logger.info("Searching for Literature panel data titles")
        literature_panel = explore_page.find_literature_panel_data(literature_panel_data_titles)

        for panel_title in literature_panel:
            assert panel_title.is_displayed(), f"Literature panel {panel_title} is not displayed"
        logger.info("Found Literature panel data titles")

        atlas = explore_page.find_3d_atlas()
        assert atlas.is_displayed()
        logger.info("3D Atlas is displayed")

        atlas_fullscreen = explore_page.find_atlas_fullscreen_bt(timeout=15)
        logger.info("Found atlas fullscreen button")
        atlas_fullscreen.click()

        fulscreen_exit = explore_page.find_fullscreen_exit(timeout=15)
        logger.info("Fullscreen exit button is found")
        fulscreen_exit.click()
        logger.info("Fullscreen exit button is clicked, atlas is minimized")
        total_count_density_title = explore_page.find_total_count_density()
        assert total_count_density_title, "The total neurons count title is not found"
        logger.info("Title for the total count of neurons is found")

        total_count_number = explore_page.find_total_count_n()
        neuron_count = total_count_number.text
        assert neuron_count.strip(), "Total neuron count is empty"
        logger.info(f"Total number of neurons is: {neuron_count}")

        count_switch_button = explore_page.find_total_count_switch()
        assert count_switch_button.is_displayed()
        logger.info(f"Found the switch count/density button")
        current_state = count_switch_button.get_attribute('aria-checked')
        logger.info(f"Current state of the total count switch: {current_state}")

        # Temporarily adding time.sleep()
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
