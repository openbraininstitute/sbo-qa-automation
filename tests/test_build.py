# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import random
import time
import uuid
from datetime import datetime

from selenium.webdriver import Keys

from pages.build import Build
from pages.vl_overview import VLOverview
import pytest

class TestBuild:
    def test_build(self, setup, login, logger):

        browser, wait, base_url = setup
        build = Build(browser,wait, base_url)
        """
        Dynamic lab and project IDs
        """
        lab_id = "37a3a2e8-a4b4-456b-8aff-4e23e87a5cbc"
        project_id = "8abcb1e3-b714-4267-a22c-3b3dc4be5306"
        current_url = build.go_to_build(lab_id, project_id)

        # Assert that the correct lab and project are in the URL
        assert lab_id in current_url and project_id in current_url, \
            f"Navigation failed. Expected IDs {lab_id} and {project_id} not found in {current_url}"

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
        # time.sleep(10)
        assert any(name.text.strip() for name in created_by_name), "No valid name found under 'Created by' section."
        logger.info("Verifying 'Created by' is not empty")
        names = [name.text.strip() for name in created_by_name if name.text.strip()]
        print(f"Found names: {names}")

        creation_date = build.creation_date()
        assert "Creation Date".lower() in creation_date.text.lower(), "'Creation Date' title not found."
        date = build.date()
        date_text = date.text.strip()
        assert date_text, "Creation date is missing or empty."
        logger.info("The 'Date' is not empty")
        print(f"Creation date found: {date_text}")

        form_brain_region = build.form_brain_region()
        form_brain_region.click()
        form_brain_region.send_keys("Cerebrum")
        form_brain_region.send_keys(Keys.RETURN)
        start_building_btn = build.start_building_btn()
        if start_building_btn.get_attribute('disabled') is None:  # Button is not disabled
            start_building_btn.click()
            print("Button clicked!")
        else:
            print("Button is disabled, cannot click.")

        sn_name = build.sn_name()
        assert sn_name.text.strip(), "Name is missing or empty."
        print(f"Name: {sn_name.text.strip()}")

        sn_description = build.sn_description()
        assert sn_description.text.strip(), "Description is missing or empty."
        print(f"Description: {sn_description.text.strip()}")

        sn_brain_region = build.sn_brain_region()
        assert sn_brain_region.text.strip(), "Brain region is missing or empty."
        print(f"Brain Region: {sn_brain_region.text.strip()}")

        sn_created_by = build.sn_created_by()
        non_empty_names = [element.text.strip() for element in sn_created_by if element.text.strip()]
        assert non_empty_names, "Created by names are missing or empty."
        print(f"Created By: {non_empty_names}")

        sn_creation_date = build.sn_creation_date()
        assert sn_creation_date.text.strip(), "Creation date is missing or empty."
        print(f"Creation Date: {sn_creation_date.text.strip()}")

        sn_mtype = build.sn_mtype()
        assert sn_mtype.text.strip(), "M-type is missing or empty."
        print(f"M-type: {sn_mtype.text.strip()}")

        sn_etype = build.sn_etype()
        assert sn_etype.text.strip(), "E-type is missing or empty."
        print(f"E-type: {sn_etype.text.strip()}")

        # time.sleep(20)