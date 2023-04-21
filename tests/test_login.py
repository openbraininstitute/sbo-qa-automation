import time

import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage
from util.util_base import load_config

@pytest.mark.usefixtures("setup", "logger")
class TestLogin:

    def test_find_login_button(self, setup, logger):
        browser, wait = setup
        home_page = LoginPage(browser, wait)
        home_page.go_to_home_page()
        login_button = home_page.find_login_button()
        assert login_button.is_displayed()
        logger.info('the button is found')
        current_url = self.browser.current_url
        login_button.click()
        time.sleep(3)



