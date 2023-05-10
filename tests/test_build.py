import time
import pytest
from selenium.webdriver import ActionChains, Keys

from pages.build_page import BuildPage
from util.util_base import load_config


class TestBuild:
    @pytest.mark.build_page
    def test_build_page(self, setup, login_explore, logger):
        browser, wait = setup
        build_page = BuildPage(browser, wait)
        build_url = build_page.go_to_build_page()
        assert build_url == 'https://bbp.epfl.ch/mmb-beta/build/load-brain-config'

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

        # wait_for_presence_in_DOM_config = build_page.wait_for_presence_of_custom_config()
        # wait_for_visibility_config = build_page.wait_for_custom_config_to_be_visible()

        # if wait_for_visibility_config:
        # Clone the public config
        clone_public_config = build_page.clone_custom_config().click()
        logger.info("'Clone' button is clicked")

        # Edit configuration modal is found
        edit_modal = build_page.find_edit_config_modal()
        logger.info("Edit configuration modal is displayed")
        clear_default_config_name = build_page.clear_default_config_name()

        # The BACKSPACE repeatedly delete previous value (name of previous config)
        while clear_default_config_name.get_property('value'):
            clear_default_config_name.send_keys(Keys.BACKSPACE)
        set_config_name = build_page.set_your_config_name().send_keys("Cloned public config")
        time.sleep(3)