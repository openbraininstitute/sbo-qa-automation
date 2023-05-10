
from locators.home_page_locators import HomePageLocators
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class HomePage(BasePage):

    def __init__(self, browser, wait):
        super().__init__(browser, wait)
        self.url = "https://bbp.epfl.ch/mmb-beta"
    def go_to_home_page(self):
        self.browser.get(self.url)
    def find_explore_title(self):
        return self.wait.until(EC.presence_of_element_located(HomePageLocators.EXPLORE_TITLE))

    def find_build_title(self):
        return self.wait.until(EC.presence_of_element_located(HomePageLocators.BUILD_TITLE))

    def find_simulate_title(self):
        return self.wait.until(EC.presence_of_element_located(HomePageLocators.SIMULATE_TITLE))

    def find_login_button(self):
        return self.wait.until(EC.element_to_be_clickable(HomePageLocators.LOGIN_BUTTON))
