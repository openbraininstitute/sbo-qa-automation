# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import random
import time
from datetime import datetime
from urllib.parse import urlparse
from selenium.webdriver import Keys
from pages.build import Build

class TestBuild:
    def test_build(self, setup, login, logger,test_config):
        browser, wait, base_url, lab_id, project_id = setup
        build = Build(browser,wait, base_url)
        lab_id = test_config["lab_id"]
        project_id = test_config["project_id"]
        print(f"DEBUG: Using lab_id={lab_id}, project_id={project_id}")
        current_url = build.go_to_build(lab_id, project_id)
        build_menu_title = build.build_menu_title().click()
        logger.info("Clicked on 'Build'")

        new_model_tab = build.new_model_tab()
        logger.info("New Model tab is displayed")

        single_neuron_title = build.single_neuron_title()
        logger.info("Single Neuron title is found in the grid")

        build_single_neuron = build.single_neuron_build_btn().click()
        logger.info("Build Single Neuron is clicked")

        form_build_sneuron_title = build.form_build_single_neuron_title()
        logger.info("Build Single Neuron title is displayed")

        model_number = random.randint(1, 100)
        current_date = datetime.now().strftime("%d-%m-%Y")
        unique_name = f"Single Neuron Model {model_number} - {current_date}"
        dynamic_description = f"This is an automated test for {unique_name}.\
        Description includes model and date."

        form_name = build.form_name()
        form_name.click()
        form_name.send_keys(unique_name)
        logger.info("Unique name for Single Neuron is provided")
        form_description = build.form_description()
        form_description.click()
        form_description.send_keys(dynamic_description)
        logger.info("Unique description for Single Neuron is provided")

        created_by_name = build.created_by_name()
        assert any(name.text.strip() for name in created_by_name), "No valid name found under 'Created by' section."
        logger.info("Verifying 'Created by' is not empty")
        names = [name.text.strip() for name in created_by_name if name.text.strip()]
        print(f"Found names: {names}")

        creation_date = build.creation_date()
        assert "Creation Date".lower() in creation_date.text.lower(), "'Creation Date' title not found."
        logger.info("'Creation date' title is found.")
        date = build.date()
        date_text = date.text.strip()
        assert date_text, "Creation date is missing or empty."
        logger.info("' Creation date' is not empty.")
        print(f"Creation date found: {date_text}")

        form_brain_region = build.form_brain_region()
        logger.info("Brain region title is found.")
        form_brain_region.click()
        form_brain_region.send_keys("Cerebrum")
        form_brain_region.send_keys(Keys.RETURN)
        logger.info("Selected 'Cerebrum' as brain region")
        start_building_btn = build.start_building_btn()
        if start_building_btn.get_attribute('disabled') is None:  # Button is not disabled
            start_building_btn.click()
            print("Button clicked!")
        else:
            print("Button is disabled, cannot click.")
        logger.info("'Start building' button is clicked.")

        sn_name = build.sn_name()
        assert sn_name.text.strip(), "Name is missing or empty."
        print(f"Name: {sn_name.text.strip()}")
        logger.info("Single neuron name is displayed.")

        sn_description = build.sn_description()
        logger.info("Single neuron description title is displayed.")
        assert sn_description.text.strip(), "'Description' title is missing."
        print(f"Description: {sn_description.text.strip()}")

        sn_brain_region = build.sn_brain_region()
        assert sn_brain_region.text.strip(), "Brain region is missing or empty."
        print(f"Brain Region: {sn_brain_region.text.strip()}")
        logger.info("Single neuron brain region is displayed.")

        sn_created_by = build.sn_created_by()
        logger.info("Single neuron 'Created by title' is displayed.")
        non_empty_names = [element.text.strip() for element in sn_created_by if element.text.strip()]
        assert non_empty_names, "Created by names are missing or empty."
        print(f"Created By: {non_empty_names}")
        logger.info("'Created by' author is displayed.")

        sn_creation_date = build.sn_creation_date()
        assert sn_creation_date.text.strip(), "Creation date is missing or empty."
        print(f"Creation Date: {sn_creation_date.text.strip()}")
        logger.info("'Creation date' is displayed.")

        sn_mtype = build.sn_mtype()
        assert sn_mtype.text.strip(), "M-type title is missing or empty."
        print(f"M-type: {sn_mtype.text.strip()}")
        logger.info("M-type title is displayed.")

        sn_etype = build.sn_etype()
        assert sn_etype.text.strip(), "E-type title is missing or empty."
        print(f"E-type: {sn_etype.text.strip()}")
        logger.info("E-type title is displayed.")

        click_select_m_model = build.select_m_model_btn()
        assert click_select_m_model.is_displayed(), "The 'Select m-model' button is not found."
        logger.info("'Select m-model' button is displayed.")

        click_select_m_model.click()
        search_input = build.find_search_input_search_item()
        logger.info("Search input field is found")
        browser.execute_script("arguments[0].click();", search_input)
        search_input.send_keys("C060114A5")
        logger.info("Searching for 'C060114A5'")

        brain_region_toggle_btn = build.brain_region_toggle_btn()
        logger.info('Found Brain Region panel toggle')
        brain_region_toggle_btn.click()
        searched_m_record = build.searched_m_record()
        assert searched_m_record.is_displayed(), "Searched record is NOT found"
        logger.info("The searched record is found")

        tick_searched_m_record = build.tick_search_m_record()
        assert tick_searched_m_record.is_displayed(), "The radio button is not displayed"
        browser.execute_script("arguments[0].click();",tick_searched_m_record)
        logger.info("Radio button of the searched record is ticked")
        select_specific_m_model_btn = build.select_specific_m_model_btn()
        if select_specific_m_model_btn.is_displayed():
            select_specific_m_model_btn.click()
        else:
            logger.info("The 'Select m-model' button is not displayed")
        logger.info("The 'M-model' is selected")

        select_e_model_btn = build.select_e_model_btn()
        assert select_e_model_btn.is_displayed(), "Select e-model button is not displayed"
        logger.info("Select e-model button is displayed")
        select_e_model_btn.click()
        logger.info("Select e-model button is clicked")

        search_input = build.find_search_input_search_item()
        logger.info("Search input field is found")
        browser.execute_script("arguments[0].click();", search_input)
        search_input.send_keys("EM__1372346__cADpyr__13")
        logger.info("Use open search to find the e-model")

        searched_e_record = build.searched_e_record()
        assert searched_e_record.is_displayed(), "The searched e-model is not found"
        logger.info("Searching for 'EM__1372346__cADpyr__13'")

        tick_searched_e_record = build.tick_search_e_record()
        assert tick_searched_e_record.is_displayed(), "The radio button is not displayed"
        logger.info("The radio button is found")
        browser.execute_script("arguments[0].click();", tick_searched_e_record)
        logger.info("Radio button of the searched record is ticked")

        select_specific_e_model_btn = build.select_specific_e_model_btn()
        if select_specific_e_model_btn.is_displayed():
            select_specific_e_model_btn.click()
            logger.info("E-model button is clicked")
        else:
            logger.info("The e-model button is not displayed")

        save_model = build.save_model()
        assert save_model.is_displayed(), "Save button is not found"
        save_model.click()

        build.wait_for_url_contains("/explore/interactive/model/me-model")
        current_url = browser.current_url
        logger.info(f"Current URL after save: {current_url}")
        parsed_url = urlparse(current_url)

        if "/explore/interactive/model/me-model" in parsed_url.path:
            logger.info("The new me-model is built")
        else:
            logger.error(f"Unexpected path: {parsed_url.path}")





