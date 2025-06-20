# # Copyright (c) 2024 Blue Brain Project/EPFL
# # Copyright (c) 2025 Open Brain Institute
# # SPDX-License-Identifier: Apache-2.0
#
# from pages.explore_me_model import ExploreMeModel
#
#
# class TestExploreMeModel:
#
#     def test_build_synaptome(self, setup, login, logger, test_config):
#         browser, wait, base_url, lab_id, project_id = setup
#         explore_me_model = ExploreMeModel(browser, wait, base_url)
#         lab_id = test_config["lab_id"]
#         project_id = test_config["project_id"]
#         print(f"DEBUG: Using lab_id={lab_id}, project_id={project_id}")
#         current_url = explore_me_model.go_to_explore_memodel_page(lab_id, project_id)
#
#
# '''
#         This is commented out because it will be used at a later point.
#
#         # Step 9: Verify the Synaptome name, description, and other attributes after creation
#         sn_name = build_synaptome.input_name_field()
#         assert sn_name.text.strip(), "Synaptome name is missing or empty after creation."
#         logger.info("Synaptome name is displayed.")
#         print(f"Synaptome Name: {sn_name.text.strip()}")
#         time.sleep(5)
#         sn_description = build_synaptome.input_description_field()
#         assert sn_description.text.strip(), "Synaptome description is missing or empty after creation."
#         logger.info("Synaptome 'Description' is displayed.")
#         print(f"Synaptome Description: {sn_description.text.strip()}")
#
#         # Step 10: Validate the 'created by' section again after creation
#         sn_created_by = build_synaptome.form_value_created_by()
#         logger.info("Validating 'Created by' author section after creation.")
#         non_empty_names = [element.text.strip() for element in sn_created_by if element.text.strip()]
#         assert non_empty_names, "Created by names are missing or empty after creation."
#         print(f"Created By: {non_empty_names}")
#
#         # Step 11: Validate the 'creation date' after creation
#         sn_creation_date = build_synaptome.form_value_creation_date()
#         assert sn_creation_date.text.strip(), "Creation Date is missing or empty after creation."
#         logger.info("'Creation Date' is displayed after creation.")
#         print(f"Creation Date: {sn_creation_date.text.strip()}")
#         '''
