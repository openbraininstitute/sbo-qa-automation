import time
import pytest
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

        time.sleep(4)

