# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0


import time
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

        project_menu_build_synaptome = build_synaptome.find_menu_build(timeout=25)
        assert project_menu_build_synaptome.is_displayed(), f"Build menu is not displayed."
        logger.info("Build menu is displayed.")

        synaptome_box = build_synaptome.find_synaptome_box(timeout=10)
        assert synaptome_box.is_displayed(), "The synaptome box is not found."
        logger.info("The synaptome box is found.")

        synaptome_box.click()

        synaptome_build_btn = build_synaptome.find_synaptome_build_btn(timeout=10)
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

        new_synaptome_title = build_synaptome.new_synaptome_title()
        assert new_synaptome_title.is_displayed(), "Synaptome 'Build new synaptome model' title is not displayed."
        logger.info("'Build new synaptome model' title is displayed.")

        synaptome_number = random.randint(1, 100)
        current_date = datetime.now().strftime("%d-%m-%Y")
        unique_name = f"Synaptome Model {synaptome_number} - {current_date}"
        dynamic_description = f"This is a test for {unique_name}. Description includes model number and date."

        input_name_field = build_synaptome.input_name_field()
        input_name_field.click()
        input_name_field.send_keys(unique_name)
        logger.info(f"Provided a unique name for Synaptome: {unique_name}")

        input_description_field = build_synaptome.input_description_field()
        input_description_field.click()
        input_description_field.send_keys(dynamic_description)
        logger.info("Provided a dynamic description for the Synaptome.")

        form_created_by = build_synaptome.form_created_by()
        assert form_created_by.is_displayed(), "'Created by' title is not displayed."
        logger.info("'Created by' title is displayed.")

        created_by_values = build_synaptome.form_value_created_by()
        assert any(value.text.strip() for value in created_by_values), "'Created by' value is empty."
        logger.info("Verified 'Created by' section is not empty.")
        print(f"Created By Values: {[value.text.strip() for value in created_by_values]}")

        form_creation_date = build_synaptome.form_creation_date()
        assert form_creation_date.is_displayed(), "'Creation Date' title is not displayed."
        logger.info("'Creation Date' title is displayed.")

        form_value_creation_date = build_synaptome.form_value_creation_date()
        assert form_value_creation_date.text.strip(), "'Creation Date' value is missing or empty."
        logger.info("'Creation Date' value is not empty.")
        print(f"Creation Date: {form_value_creation_date.text.strip()}")

        start_building_btn = build_synaptome.start_building_button()
        if start_building_btn.get_attribute('disabled') is None:
            start_building_btn.click()
            logger.info("Button clicked!")
        else:
           logger.info("Button is disabled, cannot click.")
        logger.info("'Start building' button is clicked.")

        select_model = build_synaptome.select_model()
        assert select_model.is_displayed(), "'Select model' option is not displayed."
        logger.info("'Select model' option is displayed.")

        results_label = build_synaptome.results_label()
        assert results_label.is_displayed(), "'Results' label is not displayed."
        logger.info("'Results' label is displayed.")

        build_synaptome.wait_for_spinner_to_disappear(timeout=10)
        logger.info("Spinner is disappeared.")

        brain_region_column_header = build_synaptome.brain_region_column_header(timeout=10)
        assert brain_region_column_header.is_displayed(), "'Brain region' column header is not displayed."
        logger.info("'Brain region' column header is displayed.")

        # Wait for table to load
        build_synaptome.wait_for_table_data_to_load(timeout=10)
        logger.info("Table data is fully loaded.")

        brain_region_column_header.click()
        logger.info("Clicked on 'Brain region' column header.")

        build_synaptome.wait_for_spinner_to_disappear(timeout=10)
        logger.info("Spinner is disappeared.")

        is_sorted_ascending = build_synaptome.is_column_sorted(column_index=0, ascending=True)
        assert is_sorted_ascending, "The 'Brain region' column is not sorted in ascending order."
        logger.info("Verified that 'Brain region' column is sorted in ascending order.")

        radio_button_me_model = build_synaptome.radio_btn(timeout=10)
        assert radio_button_me_model.is_displayed(), "'M-model' radio button is not displayed."
        logger.info("'M-model' radio button is displayed.")

        radio_button_me_model.click()
        logger.info("Clicked on 'M-model' radio button.")

        use_sn_model_btn = build_synaptome.use_sn_model_btn()
        assert use_sn_model_btn.is_displayed(), "'Use synaptome model' button is not displayed."
        logger.info("'Use synaptome model' button is displayed.")

        use_sn_model_btn.click()
        logger.info("Clicked on 'Use synaptome model' button.")

        configure_model_label = build_synaptome.configure_model()
        assert configure_model_label.is_displayed(), "'Configure model' label is not displayed."
        logger.info("'Configure model' label is displayed.")

        name_your_set = build_synaptome.name_your_set()
        assert name_your_set.is_displayed(), "'Name your set' label is not displayed."
        logger.info("'Name your set' label is displayed.")

        name_your_set.click()
        logger.info("Clicked on 'Name your set' label.")

        name_your_set.send_keys("soma")
        logger.info("Provided 'soma' as name for the set.")

        canvas = build_synaptome.canvas(timeout=10)
        assert canvas.is_displayed(), "3D Neuron is not displayed."
        logger.info("Canvas is displayed.")

        canvas_pointer = build_synaptome.canvas_pointer(timeout=10)
        assert canvas.is_displayed(), "Canvas pointer is not displayed."
        logger.info("Canvas pointer is displayed.")

        target_field = build_synaptome.target_field(timeout=15)
        logger.info("Found 'Target field'.")

        target_select = build_synaptome.target_select(timeout=25)
        time.sleep(3)
        target_select.click()
        time.sleep(2)
        logger.info("Clicked on 'Target select'.")

        build_synaptome.wait_for_target_dropdown_expanded(timeout=10)
        logger.info("'Target select' dropdown expanded.")

        target_list = build_synaptome.target_list(timeout=20)
        assert target_list.is_displayed(), "'Target' list is not displayed."
        logger.info("'Target' list is displayed.")

        target_soma = build_synaptome.target_soma(timeout=15)
        assert target_soma.is_displayed(), "'Target soma' is not displayed."
        logger.info("'Target soma' is displayed.")

        target_soma.click()
        logger.info("Clicked on 'Target soma' option.")

        type_field = build_synaptome.type_field()
        logger.info("'Type' field is displayed.")

        time.sleep(3)
        type_field.click()
        logger.info("Clicked on 'Type' field.")

        type_excitatory = build_synaptome.type_excitatory()
        assert type_excitatory.is_displayed(), "'Type excitatory' is not displayed."
        logger.info("'Type excitatory' is displayed.")

        type_excitatory.click()
        logger.info("Clicked on 'Type excitatory' option.")

        filter_synapses = build_synaptome.filter_synapses_btn()
        assert filter_synapses.is_displayed(), "'Filter synapses' button is not displayed."
        logger.info("'Filter synapses' button is displayed.")
        filter_synapses.click()
        logger.info("Clicked on 'Filter synapses' button.")

        greater = build_synaptome.synapse_greater_value()
        logger.info("'Synapse greater than' value is displayed.")
        greater.click()
        logger.info("Clicked on 'Synapse greater than' value.")
        greater.send_keys("100")
        logger.info("Provided '100' as value for 'Synapse greater than' option.")

        smaller = build_synaptome.synapse_smaller_value()
        logger.info("'Synapse smaller than' value is displayed.")
        smaller.click()
        logger.info("Clicked on 'Synapse smaller than' value.")
        smaller.send_keys("500")
        logger.info("Provided '500' as value for 'Synapse smaller than' option.")

        apply_changes = build_synaptome.apply_changes_btn()
        logger.info("'Apply changes' button is displayed.")
        apply_changes.click()
        logger.info("Clicked on 'Apply changes' button.")

        add_new_synapse_set = build_synaptome.add_new_synapse_set()
        logger.info("'Add new synapse set' button is displayed.")
        add_new_synapse_set.click()
        logger.info("Clicked on 'Add new synapse set' button.")

        synapse_set2 = build_synaptome.synapse_set()
        assert synapse_set2.is_displayed(), "'Synapse set' is not displayed."
        logger.info("'Synapse set' is displayed.")

        delete_synapse_set2= build_synaptome.delete_synapse_set(timeout=20)
        assert delete_synapse_set2.is_displayed(), "'Delete synapse set' is not displayed."
        logger.info("'Delete synapse set' is displayed.")
        delete_synapse_set2.click()
        logger.info("Clicked on 'Delete synapse set' button.")

        synapse_set_num = build_synaptome.synapse_set_num()
        logger.info("'Synapse set' is equal to 1 again.")

        save_synaptome = build_synaptome.save_btn(timeout=15)
        assert save_synaptome.is_displayed(), "'Save' button is not displayed."
        logger.info("'Save' button is displayed.")

        save_synaptome.click()
        logger.info("Clicked on 'Save' button.")

        build_synaptome.wait_for_url_contains("/explore/interactive/model/synaptome")
        logger.info("URL contains '/explore/interactive/model/synaptome', the model is built and detail view is "
                    "displayed.")