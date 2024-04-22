# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

# from locators.explore_interactive_locators import ExploreInteractiveLocators
# from pages.explore_page import ExplorePage
# from pages.home_page import HomePage
# from util.util_methods import find_element
#
#
# class ExploreInteractivePage(HomePage):
#     def __init__(self, browser, wait):
#         super().__init__(browser, wait)
#         self.home_page = ExplorePage(browser, wait)
#
#     def go_to_explore_interactive(self):
#         self.browser.get(self.url + "/explore/interactive")
#         return self.browser.current_url
#
#     def find_search_field(self):
#         return find_element(self.wait, ExploreInteractiveLocators.SEARCH_FIELD)
#
#     def find_search_active(self):
#         return find_element(self.wait, ExploreInteractiveLocators.SEARCH_FIELD_ACTIVE)
#
#     def find_search_shadow_root(self):
#         return find_element(self.wait, ExploreInteractiveLocators.SHADOW_ROOT)
#
#     def find_search_viewport(self):
#         return find_element(self.wait, ExploreInteractiveLocators.VIEWPORT)
#
#     def get_shadow_host(self):
#         return find_element(self.wait, ExploreInteractiveLocators.SHADOW_HOST)
#
#     def find_basic_cell_groups(self):
#         return find_element(self.wait, ExploreInteractiveLocators.BASIC_CELL_GROUPS)
#
#     def find_brain_stem(self):
#         return find_element(self.wait, ExploreInteractiveLocators.BRAIN_STEM)
#
#     def find_cerebellum(self):
#         return find_element(self.wait, ExploreInteractiveLocators.CEREBELLUM)
#
#     def find_cerebrum(self):
#         return find_element(self.wait, ExploreInteractiveLocators.CEREBRUM)
#
#     def find_experimental_data_tab(self):
#         return find_element(self.wait, ExploreInteractiveLocators.EXPERIMENTAL_DATA_TAB)
#
#     def find_literature_tab(self):
#         return find_element(self.wait, ExploreInteractiveLocators.LITERATURE_TAB)
#
#     def find_model_data_tab(self):
#         return find_element(self.wait, ExploreInteractiveLocators.EXPERIMENTAL_DATA_TAB)
#
#     def find_electrophysiology_link(self):
#         return find_element(self.wait, ExploreInteractiveLocators.ELECTROPHYSIOLOGY_LINK)
#
#     def find_morphology_link(self):
#         return find_element(self.wait, ExploreInteractiveLocators.MORPHOLOGY_LINK)
#
#     def find_bouton_density_link(self):
#         return find_element(self.wait, ExploreInteractiveLocators.BOUTON_DENSITY_LINK)
#
#     def find_neuron_density_link(self):
#         return find_element(self.wait, ExploreInteractiveLocators.NEURON_DENSITY_LINK)
#
#     def find_synapse_per_connection_link(self):
#         return find_element(self.wait, ExploreInteractiveLocators.SYNAPSE_PER_CONNECTION_LINK)
#
#     def find_isocortex(self):
#         return find_element(self.wait, ExploreInteractiveLocators.ISOCORTEX_OPTION)
#
#     def image_3d(self):
#         return find_element(self.wait, ExploreInteractiveLocators.IMAGE_3D)