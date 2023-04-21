import time

import pytest

from locators.home_page_locators import HomePageLocators
from pages.home_page import HomePage
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage


@pytest.mark.usefixtures("setup", "logger")
class TestFindLogin:

    def test_find_homepage_titles(self, setup, logger):
        browser, wait = setup
        home_page = HomePage(browser, wait)
        home_page.go_to_home_page()
        home_page.find_explore_title()
        logger.info("explore title on the homepage is found")
        build = home_page.find_build_title()
        logger.info("build title on the homepage is found")
        simulate = home_page.find_simulate_title()
        assert simulate.text == 'Simulate'

    def test_find_login_button(self, setup, logger):
        browser, wait = setup
        home_page = HomePage(browser, wait)
        home_page.go_to_home_page()
        login_button = home_page.find_login_button()
        assert login_button.is_displayed()
        logger.info('the button is found')

        # Checking current URL
        login_button.click()
        wait.until(EC.url_contains("auth"))
        login_url = browser.current_url

        # Navigate to the login page
        login_page = LoginPage(browser, wait)
        login_page.go_to_login_page(login_url)
        logger.info(f"The user was redirected to the new URL")

        username_field = login_page.find_username()
        assert username_field.is_displayed()
        logger.info('the button is found')
