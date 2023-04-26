import time
import pytest
from pages.explore_page import ExplorePage
from selenium.webdriver.support import expected_conditions as EC


class TestExplorePage:
    @pytest.mark.explore_page
    def test_explore_page(self, setup, login_explore, logger):
        browser, wait = login_explore
        explore_page = ExplorePage(browser, wait)
        exp_url = explore_page.go_to_explore_page()
        # assert EC.url_contains("explore") in browser.current_url
        assert exp_url == "https://bbp.epfl.ch/mmb-beta/explore"
        logger.info("Explore page is loaded")
        check_explore_title = explore_page.check_explore_title_is_present()
        assert check_explore_title.text.lower() == 'Explore'.lower()
        logger.info("Checking that the main title of Explore page is present")
