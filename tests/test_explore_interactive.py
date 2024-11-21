# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

# import time
# import pytest
# from pages.explore_interactive import ExploreInteractivePage
"""The commented out code below is pending changes in the platform."""

# class TestExploreInteractivePage:
#     @pytest.mark.explore_page
#     # @pytest.mark.run(order=0)
#     def test_explore_interactive(self, setup, login, logger):
#         browser, wait = setup
#         explore_interactive = ExploreInteractivePage(browser, wait)
#         exp_url = explore_interactive.go_to_explore_interactive()
#         assert exp_url == "https://bbp.epfl.ch/mmb-beta/explore/interactive"
#         logger.info("Explore interactive is loaded")
#
#         '''
#         Verifying all the main titles are present on the page
#         '''
#         basic_cell_groups = explore_interactive.find_basic_cell_groups()
#         logger.info("Basic cell groups and regions is displayed")
#         brain_stem = explore_interactive.find_brain_stem()
#         logger.info("Brain stem is displayed")
#         cerebellum = explore_interactive.find_cerebellum()
#         logger.info("Cerebellum is displayed")
#         cerebrum = explore_interactive.find_cerebrum()
#         logger.info("Cerebrum is displayed")
#         experimental_data_tab = explore_interactive.find_experimental_data_tab()
#         logger.info("Experimental data tab is displayed")
#         literature_tab = explore_interactive.find_literature_tab()
#         logger.info("Literature tab is displayed")
#         model_data_tab = explore_interactive.find_model_data_tab()
#         logger.info("Model data is displayed")
#
#         morphology = explore_interactive.find_morphology_link()
#         logger.info("Morphology is displayed")
#         electrophysiology = explore_interactive.find_morphology_link()
#         logger.info("Electrophysiology is displayed")
#         neuron_density = explore_interactive.find_neuron_density_link()
#         logger.info("Neuron density is displayed")
#         bouton_density = explore_interactive.find_bouton_density_link()
#         logger.info("Bouton density is displayed")
#         synapse_per_connection = explore_interactive.find_synapse_per_connection_link()
#         logger.info("Synapse per connection is displayed")
#         image_3d = explore_interactive.image_3d()
#         if image_3d.is_displayed():
#             logger.info("3D image is displayed on the page.")
#         else:
#             logger.info("3D image is not displayed on the page.")
#
#         '''
#         Verifying that search field is working
#         '''
#         search_field = explore_interactive.find_search_field()
#         search_field.click()
#         shadow_host = explore_interactive.get_shadow_host()
#         shadow_host.click()
#         logger.info("Search region field is clicked")
#         shadow_host.send_keys("Isocortex")
#         isocortex_option = explore_interactive.find_isocortex()
#         isocortext = isocortex_option.text
#         assert isocortext == "Isocortex"
#         logger.info("Isocortex selected as brain region")
#         isocortex_option.click()
#         logger.info("Isocortex and its sub-regions are displayed")
#         # morphology.click()
