import os
import time
import uuid

import pytest
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium import webdriver
from pages.build_page import BuildPage
from util.util_base import load_config
from util.util_links_checker import LinkChecker
from util.util_load_links import LinkUtil

current_directory = os.getcwd()
relative_file_path = 'scraped_links.txt'
file_path = os.path.join(current_directory, relative_file_path)





class TestBuild:
    @pytest.mark.build_page
    def test_build_page(self, setup, login_explore, logger):
        browser, wait = setup
        build_page = BuildPage(browser, wait)
        build_url = build_page.go_to_build_page()

        recent_config = build_page.find_recent_configurations()
        assert recent_config.text == "Recently used configurations"
        logger.info("Build page main titles are displayed, such as Recent recently used configurations")

        verify_release_version = build_page.verify_release_version()
        assert verify_release_version.text == "Release 23.01"
        logger.info("Build page release version is displayed")

        # TO KEEP THIS ONE FOR NOW: Find the default public config and click on it
        # plus_icon_open_default_config = build_page.select_default_config().click()
        # logger.info("Accessing default public config link via plus icon")

        find_search_textfield = build_page.find_config_search_field()
        find_search_textfield.send_keys("Custom model configuration")

        use_public_config = build_page.use_custom_config()
        clone_public_config = build_page.clone_custom_config().click()
        logger.info("'Clone' button is clicked")

        # Find the name input field in the modal
        find_default_config_name = build_page.find_default_config_name()
        find_default_config_name.send_keys(Keys.COMMAND + 'a')
        find_default_config_name.send_keys(Keys.DELETE)
        if not find_default_config_name.get_attribute('value'):
            generate_config_name = "Config_" + str(uuid.uuid4())
            find_default_config_name.click()
            find_default_config_name.send_keys(generate_config_name)

        # Find the description input field in the modal
        find_default_description = build_page.clear_default_description_name()

        # Wait until 'Start editing button is enabled"
        if find_default_description.get_property('value'):
            print("The default description has a value")
        else:
            print('description value is EMPTY')

        time.sleep(10)
        start_editing = build_page.push_start_editing()
        str_ed_txt = start_editing.text
        logger.info("start editing text is found")
        start_editing.click()
        logger.info("Start editing button was clicked")

        is_loaded = build_page.is_config_page_loaded()
        time.sleep(15)

        brain_cells_regions = build_page.find_basic_cell_groups()
        logger.info("Title brain cells and groups are present")

        find_cell_composition = build_page.find_cell_composition()
        logger.info("Cell composition link/button is found")

        find_cell_model_assignment = build_page.find_cell_model_assignment()
        logger.info("Cell model assignment link/button is found")

        find_connectome_definition = build_page.find_connectome_definition()
        logger.info("Connectome definition link/button is found")

        find_connection_model_assignment = build_page.find_connection_model_assignment()
        logger.info("Find connection model assignment link/button is found")

        find_build_and_simulate_button = build_page.find_build_and_simulate_button()
        logger.info("Build & Simulate button is found")

    def test_links(self):
        test_directory = os.path.dirname(os.path.abspath(__file__))
        links_file_path = os.path.join(test_directory, '..', 'links.json')

        link_checker = LinkChecker()
        links = link_checker.load_links(links_file_path)['build_page_links']
        link_checker.check_links(links)
