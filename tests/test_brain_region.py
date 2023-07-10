import os
import time

import pytest
import requests
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium import webdriver

from pages.brain_region import BrainRegionPage
from util.util_base import load_config
from util.util_links_checker import LinkChecker
from util.util_links_writer import write_links_to_file
from util.util_scraper import UrlScraper

current_directory = os.getcwd()
relative_file_path = 'scraped_links.txt'
file_path = os.path.join(current_directory, relative_file_path)


class TestBrainBuild:
    @pytest.mark.build_page
    def test_build_page(self, setup, login_explore, logger):
        browser, wait = setup
        brain_region_page = BrainRegionPage(browser, wait)
        brain_region_url = brain_region_page.go_to_config_page()

        find_main_build_section = brain_region_page.find_build_main_section()
        open_build_div = brain_region_page.open_build_div()
        browser.execute_script("arguments[0].style.display = 'block'; arguments[0].style.visibility = 'visible';",
                               open_build_div)

        find_visible_basic_cells_txt = brain_region_page.find_visible_basic_cells()
        find_visible_basic_cells_txt.click()

        find_basic_cells_arrow_btn = brain_region_page.find_basic_cells_arrow_btn()
        find_basic_cells_arrow_btn.click()
        logger.info("Basic cell groups and regions first arrow is clicked ")

        find_brain_stem = brain_region_page.find_brain_stem_arrow_btn()
        find_brain_stem.click()
        logger.info("Brain stem arrow to toggle open is clicked")
        find_click_cerebrum_btn = brain_region_page.find_cerebrum_arrow_btn().click()
        logger.info("Cerebrum btn toggled")
        find_click_cerebral_cortex_btn = brain_region_page.find_cerebral_cortex_arrow_btn().click()
        logger.info("Cerebral cortex btn toggled")
        find_click_cortical_plate_btn = brain_region_page.find_cortical_plate_arrow_btn().click()
        logger.info("Cortical plate btn toggled")
        find_click_isocortex_btn = brain_region_page.find_isocortex_arrow_btn().click()
        logger.info("Isocortex btn toggled")
        find_click_agranular_ins_area_btn = brain_region_page.find_agranular_ins_area_btn().click()
        logger.info("Agranular Insular Area btn toggled")
        find_click_agranular_ins_area_dorsal_p = brain_region_page.find_agranular_ins_area_dorsal_p_btn().click()
        logger.info("Agranular Insular Area Dorsal Part is toggled")
        find_click_agranular_ins_area_dorsal_title = brain_region_page.find_agranular_ins_area_dorsal_p_title().click()
        logger.info("Agranular Insular Area Dorsal Part title is clicked")
        time.sleep(10)
        find_click_configuration_btn = brain_region_page.find_configuration_btn()
        if find_click_configuration_btn:
            find_click_configuration_btn.click()
            print("CONFIG BUTTON FOUND")
        else:
            print("CONFIG BUTTON NOT FOUND")

        find_click_l5_bp_btn = brain_region_page.l5_bp_arrow_btn()
        find_click_l5_bp_btn.txt = find_click_l5_bp_btn.text
        print(find_click_l5_bp_btn)

        find_l5_bp_slider = brain_region_page.l5_bp_slider_handle()

        if find_l5_bp_slider.is_enabled():
            move = ActionChains(browser)
            move.click_and_hold(find_l5_bp_slider).pause(0).move_by_offset(50, 0).release().perform()
        else:
            print("L5_BP slider is not there")
        time.sleep(15)


"""
    Below is a code snippet for scraping links


    def test_links(self):
        test_directory = os.path.dirname(os.path.abspath(__file__))
        links_file_path = os.path.join(test_directory, '..', 'links.json')

        link_checker = LinkChecker()
        links = link_checker.load_links(links_file_path)['brain_build_page_links']
        link_checker.check_links(links)
        
        
        # url = "https://bbp.epfl.ch/mmb-beta/build/cell-composition/interactive?brainModelConfigId=8a962b3a-2005-4bc1-9b35-c20c2ec4cc54"
        # response = requests.get(url)
        # page_source = response.text
        # url_scraper = UrlScraper()
        # scraped_links = url_scraper.scrape_links(page_source)
        #
        # write_links_to_file(file_path, scraped_links)
        # print("Scraped links from BRAIN REGION saved to file successfully")
        # print("File path BRAIN test", file_path)
        # print("Scraped links BRAIN page", scraped_links) 
"""
