import time

import pytest

from locators.home_page_locators import HomePageLocators
from pages.home_page import HomePage
from selenium.webdriver.support import expected_conditions as EC


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

        # checking current URL
        current_url = browser.current_url
        login_button.click()
        wait.until(EC.url_changes(current_url))
        # time.sleep(3)

        new_url = browser.current_url
        assert new_url, "The new URL is not empty"
        logger.info(f"The user was redirected to the new URL")
        # return new_url

