import time
import pytest
from pages.build_page import BuildPage
from util.util_base import load_config


@pytest.mark.usefixtures("setup", "logger", "login", "navigate_to_login")

class TestBuild:
    def test_build_page(self, setup, logger, login, navigate_to_login):
        # Navigate to the home page
        # Login to the site
        login_page = login
        username_field = login_page.find_username_field()
        username_field.send_keys(load_config()['username'])
        password_field = login_page.find_password_field()
        password_field.send_keys(load_config()['password'])
        sign_in_button = login_page.find_signin_button()
        sign_in_button.click()

        # Navigate to the Build page
        build_page = BuildPage(*setup)
        build_url = build_page.go_to_build_page()
        assert build_url == 'https://bbp.epfl.ch/mmb-beta/build/load-brain-config'

        # Find "Text on Build Page"
        recent_config = build_page.find_recent_configurations()
        assert recent_config.text == "Recently used configurations"

        # Check the Release version
        verify_release_version = build_page.verify_release_version()
        assert verify_release_version.text == "Release 23.01"

        plus_icon_open_default_config = build_page.select_default_config().click()

        # Find the public configuration referring to Release 23.01
        # select_public_config = build_page.public_config_release().click()
        # txt = select_public_config.text
        # print("FINDING PUBLIC CONFIG WITH THE LATEST RELEASE VERSION", txt)

