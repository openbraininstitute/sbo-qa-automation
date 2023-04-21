import time
import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage

@pytest.mark.usefixtures("setup","logger", "navigate_to_login")
class TestLogin:

    def test_login(self, setup, logger, login):
        # browser, wait = setup
        # home_page = LoginPage(browser, wait)
        # home_page.go_to_home_page()
        username_field = login.find_username()
        assert username_field.is_displayed()
        logger.info('the button is found')

        time.sleep(5)



