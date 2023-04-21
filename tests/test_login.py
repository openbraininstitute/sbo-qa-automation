import time
import pytest
from util.util_base import load_config


@pytest.mark.usefixtures("setup", "logger", "navigate_to_login")
class TestLogin:

    def test_login(self, setup, logger, login):
        # Defining config to use the credentials from the JSON file
        config = load_config()

        # Searching and entering USERNAME
        username_field = login.find_username_field()
        assert username_field.is_displayed()
        logger.info('The username field is displayed')
        username_field.send_keys(config['username'])

        # Searching and entering PASSWORD
        password_field = login.find_password_field()
        assert password_field.is_displayed()
        logger.info('The password field is displayed')
        password_field.send_keys(config['password'])

        # Searching and clicking on SIGN IN button
        sign_in_button = login.find_signin_button()
        assert sign_in_button.is_displayed()
        sign_in_button.click()
        logger.info('The user is logged in the SBO')
        time.sleep(4)

        # Searching for LOGOUT button
        logout_button = login.find_logout_button()
        assert logout_button.is_displayed()
        logger.info('The user is logged in and logout button is displayed')
