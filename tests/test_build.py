import time
import uuid

import pytest
from selenium.webdriver import ActionChains, Keys
from selenium import webdriver
from pages.build_page import BuildPage
from util.util_base import load_config


class TestBuild:
    @pytest.mark.build_page
    def test_build_page(self, setup, login_explore, logger):
        browser, wait = setup
        build_page = BuildPage(browser, wait)
        build_url = build_page.go_to_build_page()
        # assert build_url == 'https://bbp.epfl.ch/mmb-beta/build/load-brain-config'

        # Find "titles on the Build Page"
        recent_config = build_page.find_recent_configurations()
        assert recent_config.text == "Recently used configurations"
        logger.info("Build page main titles are displayed, such as Recent recently used configurations")

        # Check the Release version
        verify_release_version = build_page.verify_release_version()
        assert verify_release_version.text == "Release 23.01"
        logger.info("Build page release version is displayed")

        # Find the default public config and click on it
        # plus_icon_open_default_config = build_page.select_default_config().click()
        # logger.info("Accessing default public config link via plus icon")

        # Find the search field and enter 'Custom model configuration' as a search param
        find_search_textfield = build_page.find_config_search_field()
        find_search_textfield.send_keys("Custom model configuration")

        # Use public config
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

        if find_default_description.get_property('value'):
            start_editing = build_page.push_start_editing()
            start_editing.click()

        print("Before calling is_config_page_loaded")
        is_loaded = build_page.is_config_page_loaded()
        print("After calling is_config_page_loaded")

        assert is_loaded, "Build page is not loaded correctly"
        time.sleep(5)
