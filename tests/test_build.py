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
        form_description = build.form_description()
        form_description.click()
        form_description.send_keys(dynamic_description)

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
        # time.sleep(20)