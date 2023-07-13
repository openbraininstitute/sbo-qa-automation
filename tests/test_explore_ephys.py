import os
import time
import pytest
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium import webdriver

from pages.explore_efys import ExploreElectrphysiologyPage
from pages.explore_page import ExplorePage
from util.util_base import load_config
from util.util_links_checker import LinkChecker
from util.util_load_links import LinkUtil

current_directory = os.getcwd()
relative_file_path = 'scraped_links.txt'
file_path = os.path.join(current_directory, relative_file_path)


class TestExploreEphys:
    @pytest.mark.build_page
    def test_explore_ephys_page(self, setup, login_explore, logger):
        browser, wait = setup
        explore_ephys_page = ExploreElectrphysiologyPage(browser, wait)
        ephys_page = explore_ephys_page.go_to_explore_ephys_page()
        assert ephys_page == "https://bbp.epfl.ch/mmb-beta/explore/electrophysiology"
        time.sleep(3)

        find_ephys_page_title = explore_ephys_page.find_ephys_page_title()
        logger.info("Neuron electrophysiology title is present")

        find_ephys_brain_region_c_header = explore_ephys_page.find_brain_region_header()
        logger.info("Electrophysiology brain region column header")
        find_ephys_e_type_c_header = explore_ephys_page.find_e_type_header()
        logger.info("Electrophysiology E_Type column header")
        find_ephys_name_c_header = explore_ephys_page.find_name_header()
        logger.info("Electrophysiology Name column header")
        find_ephys_species_c_header = explore_ephys_page.find_species_header()
        logger.info("Electrophysiology Species column header")
        find_ephys_contributors_c_header = explore_ephys_page.find_contributors_header()
        logger.info("Electrophysiology Contributors column header")
        find_ephys_date_c_header = explore_ephys_page.find_creation_date_header()
        logger.info("Electrophysiology date creation column header")

        find_search_field = explore_ephys_page.find_search_label()
        assert find_search_field is not None
        logger.info("Search field is found")