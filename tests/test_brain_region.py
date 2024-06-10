# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

import os
import time
import pytest
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains, Keys

# from pages.brain_region import BrainRegionPage
from util.util_base import load_config
from util.util_links_checker import LinkChecker
from util.util_links_writer import write_links_to_file
from util.util_scraper import UrlScraper

current_directory = os.getcwd()
relative_file_path = 'scraped_links.txt'
file_path = os.path.join(current_directory, relative_file_path)

'''
# class TestBrainBuild:
#     @pytest.mark.build_page
#     @pytest.mark.run(order=6)
#     def test_brain_build(self, setup, login, logger):
#         browser, wait = setup
#         brain_region_page = BrainRegionPage(browser, wait)
#         brain_region_url = brain_region_page.go_to_config_page()
#         # current_url = brain_region_page.browser.current_url
#         # logger.info(f"Brain Build Current URL {current_url}")
# 
#         search_input = brain_region_page.find_search_input()
#         logger.info("Search input is found")
#         search_input.click()
#         logger.info("Search input is clicked")
#         actions = ActionChains(browser)
#         actions.click(search_input).send_keys("Isocortex").perform()
#         search_value = brain_region_page.find_search_value()
#         actions.click(search_value).perform()
#         logger.info("Search value 'Isocortex' is clicked")
#         find_visible_basic_cells_txt = brain_region_page.find_visible_basic_cells()
#         logger.info("The Basic Cell Groups and Regions title is found")
# 
#         find_top_nav_menu = brain_region_page.find_top_nav_menu()
#         if find_top_nav_menu is not None:
#             find_top_nav_menu.click()
#             logger.info("Top navigation menu is clicked")
# 
#         # find_cell_composition = brain_region_page.find_cell_composition()
        # logger.info("Cell composition button is found")
        # find_cell_composition.click()
        # logger.info("Cell composition button is clicked")
        # find_second_submenu = brain_region_page.find_second_sub_menu().click()
        # logger.info("Second top submenu is opened")
        # configuration_btn = brain_region_page.configuration_button()
        # actions.click(configuration_btn).perform()
        # logger.info("Configuration button clicked")
        # isocortex_btn = brain_region_page.find_isocortex_arrow_btn()
        # actions.click(isocortex_btn).perform()
        # logger.info("Isocortex arrow button toggled")
        # agranular_ins_area_btn = brain_region_page.find_agranular_ins_area_btn()
        # actions.click(agranular_ins_area_btn).perform()
        # logger.info("Agranular Insular Area btn toggled")
        # agranular_ins_area_dorsal_p = brain_region_page.find_agranular_ins_area_dorsal_p_btn()
        # actions.click(agranular_ins_area_dorsal_p).perform()
        # logger.info("Agranular Insular Area Dorsal Part is toggled")
        # agranular_ins_area_dorsal_title = brain_region_page.find_agranular_ins_area_dorsal_p_title()
        # actions.click(agranular_ins_area_dorsal_title).perform()
        # logger.info("Agranular Insular Area Dorsal Part title is clicked")
        # find_click_l5_bp_btn = brain_region_page.l5_bp_arrow_btn()

        # find_main_build_section = brain_region_page.find_build_main_section()
        # open_build_div = brain_region_page.open_build_div()
        # brain_region_page.open_build_div().click()
        # find_visible_basic_cells_txt.click()
        # find_basic_cells_arrow_btn = brain_region_page.find_basic_cells_arrow_btn()
        # find_basic_cells_arrow_btn.click()
        # logger.info("Basic cell groups and regions first arrow is clicked ")
        # find_brain_stem = brain_region_page.find_brain_stem_arrow_btn()
        # find_brain_stem.click()
        # logger.info("Brain stem arrow to toggle open is clicked")
        # find_click_cerebrum_btn = brain_region_page.find_cerebrum_arrow_btn().click()
        # logger.info("Cerebrum btn toggled")
        # find_click_cerebral_cortex_btn = brain_region_page.find_cerebral_cortex_arrow_btn().click()
        # logger.info("Cerebral cortex btn toggled")
        # find_click_cortical_plate_btn = brain_region_page.find_cortical_plate_arrow_btn().click()
        # logger.info("Cortical plate btn toggled")
        # find_click_isocortex_btn = brain_region_page.find_isocortex_arrow_btn().click()
        # logger.info("Isocortex btn toggled")
        # find_click_agranular_ins_area_btn = brain_region_page.find_agranular_ins_area_btn().click()
        # logger.info("Agranular Insular Area btn toggled")
        # find_click_agranular_ins_area_dorsal_p = brain_region_page.find_agranular_ins_area_dorsal_p_btn().click()
        # logger.info("Agranular Insular Area Dorsal Part is toggled")
        # find_click_agranular_ins_area_dorsal_title = brain_region_page.find_agranular_ins_area_dorsal_p_title().click()
        # logger.info("Agranular Insular Area Dorsal Part title is clicked")
        # find_click_l5_bp_btn = brain_region_page.l5_bp_arrow_btn()
        # find_click_l5_bp_btn.txt = find_click_l5_bp_btn.text


        # find_cell_model_assignment = brain_region_page.find_cell_model_assignment()
        # logger.info("Cell model assignment button is found")
        # find_connectome_definition = brain_region_page.find_connectome_definition()
        # logger.info("Connectome definition button is found")
        # find_connection_model_assignment = brain_region_page.find_connection_model_assignment()
        # logger.info("Connectome model assignment button is found")

        # find_build_and_simulate_button = brain_region_page.find_build_and_simulate_button()
        # logger.info("Build & Simulate button is found")
  
    def test_links(self):
        test_directory = os.path.dirname(os.path.abspath(__file__))
        links_file_path = os.path.join(test_directory, '..', 'links.json')

        link_checker = LinkChecker()
        links = link_checker.load_links(links_file_path)['explore_ephys_links']
        link_checker.check_links(links)
'''