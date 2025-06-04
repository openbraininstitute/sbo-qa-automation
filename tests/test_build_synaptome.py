import time

import pytest
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.build_synaptome import BuildSynaptomePage
import random
from datetime import datetime




class TestBuildSynaptome:

    def test_build_synaptome(self, setup, login, logger, test_config):
        browser, wait, base_url, lab_id, project_id = setup
        build_synaptome = BuildSynaptomePage(browser, wait, base_url)
        lab_id = test_config["lab_id"]
        project_id = test_config["project_id"]
        print(f"DEBUG: Using lab_id={lab_id}, project_id={project_id}")
        current_url = build_synaptome.go_to_build_synaptome(lab_id, project_id)

        project_menu_build_synaptome = build_synaptome.find_menu_build()
        assert project_menu_build_synaptome.is_displayed(), f"Build menu is not displayed."
        logger.info("Build menu is displayed.")

        synaptome_box = build_synaptome.find_synaptome_box()
        assert synaptome_box.is_displayed(), f"Synaptome box is not displayed."
        logger.info("Synaptome box is displayed")

        synaptome_box.click()
        logger.info("Synaptome box is clicked to start building synaptome.")

        synaptome_build_btn = build_synaptome.find_synaptome_build_btn()
        assert synaptome_build_btn.is_displayed(), f"Synaptome build button is not displayed."
        logger.info("Synaptome build button is displayed.")
        synaptome_build_btn.click()
        logger.info("Synaptome build button is clicked.")

        build_synaptome.wait_for_url_contains("/build/synaptome/new")

        synaptome_number = random.randint(1, 100)
        current_date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        unique_name = f"Synaptome {synaptome_number} - {current_date_time}"
        dynamic_description = f"This is an automated test for {unique_name}. Description includes synaptome number, date, and time."

        synaptome_form = build_synaptome.synaptome_form()
        assert synaptome_form.is_displayed(), "Synaptome form is not visible."
        logger.info("Synaptome form is displayed.")

        # Step 2: Verify the title of the Synaptome building page
        new_synaptome_title = build_synaptome.new_synaptome_title()
        assert new_synaptome_title.is_displayed(), "Synaptome 'Build new synaptome model' title is not displayed."
        logger.info("'Build new synaptome model' title is displayed.")

        # Step 3: Generate a unique name and dynamic description
        synaptome_number = random.randint(1, 100)
        current_date = datetime.now().strftime("%d-%m-%Y")
        unique_name = f"Synaptome Model {synaptome_number} - {current_date}"
        dynamic_description = f"This is a test for {unique_name}. Description includes model number and date."

        # Step 4: Fill in the Synaptome name
        input_name_field = build_synaptome.input_name_field()
        input_name_field.click()
        input_name_field.send_keys(unique_name)
        logger.info(f"Provided a unique name for Synaptome: {unique_name}")

        # Step 5: Fill in the Synaptome description
        input_description_field = build_synaptome.input_description_field()
        input_description_field.click()
        input_description_field.send_keys(dynamic_description)
        logger.info("Provided a dynamic description for the Synaptome.")

        # Step 6: Verify 'created by' section
        form_created_by = build_synaptome.form_created_by()
        assert form_created_by.is_displayed(), "'Created by' title is not displayed."
        logger.info("'Created by' title is displayed.")

        created_by_values = build_synaptome.form_value_created_by()
        assert any(value.text.strip() for value in created_by_values), "'Created by' value is empty."
        logger.info("Verified 'Created by' section is not empty.")
        print(f"Created By Values: {[value.text.strip() for value in created_by_values]}")

        # Step 7: Verify 'creation date' section
        form_creation_date = build_synaptome.form_creation_date()
        assert form_creation_date.is_displayed(), "'Creation Date' title is not displayed."
        logger.info("'Creation Date' title is displayed.")

        form_value_creation_date = build_synaptome.form_value_creation_date()
        assert form_value_creation_date.text.strip(), "'Creation Date' value is missing or empty."
        logger.info("'Creation Date' value is not empty.")
        print(f"Creation Date: {form_value_creation_date.text.strip()}")

        # Step 8: Start building (if button is enabled)
        start_building_btn = build_synaptome.start_building_button()
        if start_building_btn.get_attribute('disabled') is None:
            start_building_btn.click()
            print("Button clicked!")
        else:
            print("Button is disabled, cannot click.")
        logger.info("'Start building' button is clicked.")

        # # Step 9: Verify the Synaptome name, description, and other attributes after creation
        # sn_name = build_synaptome.input_name_field()
        # assert sn_name.text.strip(), "Synaptome name is missing or empty after creation."
        # logger.info("Synaptome name is displayed.")
        # print(f"Synaptome Name: {sn_name.text.strip()}")
        # time.sleep(5)
        # sn_description = build_synaptome.input_description_field()
        # assert sn_description.text.strip(), "Synaptome description is missing or empty after creation."
        # logger.info("Synaptome 'Description' is displayed.")
        # print(f"Synaptome Description: {sn_description.text.strip()}")
        #
        # # Step 10: Validate the 'created by' section again after creation
        # sn_created_by = build_synaptome.form_value_created_by()
        # logger.info("Validating 'Created by' author section after creation.")
        # non_empty_names = [element.text.strip() for element in sn_created_by if element.text.strip()]
        # assert non_empty_names, "Created by names are missing or empty after creation."
        # print(f"Created By: {non_empty_names}")
        #
        # # Step 11: Validate the 'creation date' after creation
        # sn_creation_date = build_synaptome.form_value_creation_date()
        # assert sn_creation_date.text.strip(), "Creation Date is missing or empty after creation."
        # logger.info("'Creation Date' is displayed after creation.")
        # print(f"Creation Date: {sn_creation_date.text.strip()}")
        #
        # time.sleep(10)

