import time
import pytest
from util.util_base import load_config


@pytest.mark.usefixtures("setup", "logger", "login")
class TestLogin:
    @pytest.mark.run(order=1)
    def test_login(self, setup, logger, login):
        """Access the login fixture
        Find the username/password fields and enter credentials"""
        login_page = login
        username_field = login_page.find_username_field()
        assert username_field.is_displayed()
        logger.info('The username field is displayed')
        username_field.send_keys(load_config()['username'])

        password_field = login_page.find_password_field()
        assert password_field.is_displayed()
        logger.info('The password field is displayed')
        password_field.send_keys(load_config()['password'])

        # Find and click on sign in button
        sign_in_button = login_page.find_signin_button()
        assert sign_in_button.is_displayed()
        sign_in_button.click()
        logger.info('The user is logged in the SBO')


        # If he user is logged in, log out button should be present
        logout_button = login_page.find_logout_button()
        lgt_btn = logout_button.text
        print("THIS IS LOGOUT BUTTON: ", lgt_btn)
        assert lgt_btn == 'Logout'
        assert logout_button.is_displayed()
        logger.info('The user is logged in and logout button is displayed')
