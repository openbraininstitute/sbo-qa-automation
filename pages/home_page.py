from locators.home_page_locators import HomePageLocators
from selenium.common.exceptions import TimeoutException
import logging
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
# from util.util_base import logger


class HomePage(BasePage):

    def __init__(self, browser):
        # super().__init__(browser)
        self.browser = browser
        self.url = "https://bbp.epfl.ch/mmb-beta"

    # def load(self):
    def go_to_home_page(self):
        self.browser.get(self.url)

    def find_login_button(self):
        return self.wait.until(EC.element_to_be_clickable(*HomePageLocators.LOGIN_BUTTON))
