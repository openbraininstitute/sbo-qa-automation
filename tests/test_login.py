from selenium.common import NoSuchElementException

from pages.home_page import HomePage
from pages.login_page import LoginPage
from util.util_base import load_config
import pytest
import time


class TestLogin:
    @pytest.mark.run(order=1)
    def test_login_process(self, setup, logger):
        """Test the login process"""
        browser, wait = setup
        try:
            login_page = LoginPage(browser, wait)
            login_url = login_page.navigate_to_homepage()
            login_button = login_page.find_login_button()
            login_button.click()
            username_field = login_page.find_username_field()
            logger.info("The 'username' field is displayed")
            username_field.send_keys(load_config()['username'])

            password_field = login_page.find_password_field()
            assert password_field.is_displayed()
            logger.info("The 'password' field is displayed")
            password_field.send_keys(load_config()['password'])

            sign_in_button = login_page.find_signin_button()
            assert sign_in_button.is_displayed()
            sign_in_button.click()
            logger.info("The 'Sign in' button clicked")

            login_page.wait_for_login_complete()  # Wait for login to complete

            logout_button = login_page.find_logout_button()
            assert logout_button.text == 'Log out'
            assert logout_button.is_displayed()
            logger.info("The user is logged in")

        except NoSuchElementException:
            print(f"An error occurred:")
            raise


