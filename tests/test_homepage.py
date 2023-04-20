import time

import pytest

from locators.home_page_locators import HomePageLocators
from pages.home_page import HomePage
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.usefixtures("setup", "logger")
class TestFindLogin:

    def test_find_explore_title(self, setup, logger):
        browser, wait = setup
        home_page = HomePage(browser, wait)
        home_page.go_to_home_page()
        home_page.find_explore_title()
        logger.info("explore title is found")

    def test_find_login_button(self, setup, logger):
        browser, wait = setup
        home_page = HomePage(browser, wait)
        home_page.go_to_home_page()
        login_button = home_page.find_login_button()
        assert login_button.is_displayed()
        login_button.click()
        time.sleep(1)
        # login_button = home_page.find_login_button()


        # assert home_page.find_login_button(), "Search button is found"
        logger.info('the button is found')
