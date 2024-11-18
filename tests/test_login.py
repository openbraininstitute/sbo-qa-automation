# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

from selenium.common import NoSuchElementException
from selenium.webdriver import Keys

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
            logger.info("login button found")
            # logger.info("Current URL", browser.current_url)
            # browser.execute_script("arguments[0].click();", github_btn)
            # logger.info("Clicked Github login button")
            # username_field = login_page.find_username_field()
            # logger.info("The 'username' field is displayed")
            # username_field.send_keys(load_config()['username'])

            # browser.execute_script("arguments[0].click();", github_btn)
            # logger.info("Clicked Github login button")
            username_field = login_page.find_username_field()
            logger.info("The 'username' field is displayed")
            browser.execute_script("arguments[0].click();", username_field)
            username_field.send_keys(load_config()['username'])
            # password_field = login_page.find_password_field()
            # assert password_field.is_displayed()
            # logger.info("The 'password' field is displayed")
            # password_field.send_keys(load_config()['password'])

            password_field = login_page.find_password_field()
            assert password_field.is_displayed()
            logger.info("The 'password' field is displayed")
            browser.execute_script("arguments[0].click();", password_field)
            typed_pass = password_field.send_keys(load_config()['password'])
            password_field.send_keys(Keys.ENTER)
            time.sleep(2)

            # password_field.send_keys("some text" + Keys.ENTER)
            # submit_btn = login_page.find_submit()
            # text = submit_btn.text()
            # print(text)
            # browser.execute_script("arguments[0].click();", submit_btn)
            # logger.info("User clicked on 'ENTER' key.")

            time.sleep(3)
            expected_url = 'https://openbluebrain.com/mmb-beta/virtual-lab/sandbox/home'
            assert browser.current_url == expected_url
            # sign_in_button = login_page.find_signin_button()
            # assert sign_in_button.is_displayed()
            # sign_in_button.click()
            # logger.info("The 'Sign in' button clicked")

            # login_page.wait_for_login_complete()  # Wait for login to complete

            # logout_button = login_page.find_logout_button()
            # assert logout_button.text == 'Log out'
            # assert logout_button.is_displayed()
            # logger.info("The user is logged in")

        except NoSuchElementException:
            print(f"An error occurred:")
            raise
