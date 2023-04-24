import time
import pytest
from pages.build_page import BuildPage
from util.util_base import load_config


@pytest.mark.usefixtures("setup", "logger", "login", "navigate_to_login")

class TestBuild:
    def test_build_page(self, setup, logger, login, navigate_to_login):
        # navigate to the home page
        # login to the site
        login_page = login
        username_field = login_page.find_username_field()
        username_field.send_keys(load_config()['username'])
        password_field = login_page.find_password_field()
        password_field.send_keys(load_config()['password'])
        sign_in_button = login_page.find_signin_button()
        sign_in_button.click()

        build_page = BuildPage(*setup)
        build_url = build_page.go_to_build_page()
        time.sleep(3)
        login.browser.get(build_url)
        time.sleep(3)



