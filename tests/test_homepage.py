import time

import pytest

from locators.home_page_locators import HomePageLocators
from pages.home_page import HomePage
from selenium.webdriver.support import expected_conditions as EC



@pytest.mark.usefixtures("setup")
class TestFindLogin:

    def test_find_login_button(self, setup):
        browser, wait, logger = setup
        home_page = HomePage(browser)
        home_page.go_to_home_page()
        login_button = wait.until(EC.element_to_be_clickable(HomePageLocators.LOGIN_BUTTON))
        login_button.click()
        time.sleep(3)


        # assert home_page.find_login_button(), "Search button is found"
        logger.info('the button is found')