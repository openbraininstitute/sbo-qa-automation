import time
import pytest
from pages.home_page import HomePage



@pytest.mark.usefixtures("setup", "logger")
class TestFindLogin:

    def test_find_homepage_titles(self, setup, logger, login):
        home_page = HomePage(*setup)
        home_page.go_to_home_page()
        home_page.find_explore_title()
        logger.info("explore title on the homepage is found")
        build = home_page.find_build_title()
        logger.info("build title on the homepage is found")
        simulate = home_page.find_simulate_title()
        assert simulate.text == 'Simulate'

    def test_find_login_button(self, setup, logger, login):
        home_page = HomePage(*setup)
        home_page.go_to_home_page()
        login_button = home_page.find_login_button()
        assert login_button.is_displayed()
        logger.info('the button is found')

