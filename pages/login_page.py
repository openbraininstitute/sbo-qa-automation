from locators.home_page_locators import HomePageLocators
from locators.login_locators import LoginPageLocators
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC

from pages.home_page import HomePage


class LoginPage(HomePage):
    def __init__(self, browser, wait):
        super().__init__(browser, wait)

    def go_to_login_page(self, url):
        self.browser.get(url)
        self.wait.until(EC.url_contains(url))

    # def find_login_button(self):
    #     return self.wait.until(EC.element_to_be_clickable(LoginPageLocators.LOGIN_BUTTON))

    # def login(self, username):
    #    # return self.driver.find_element(LoginPageLocators.USERNAME)
    #     pass

    def find_username(self):
        return self.wait.until(EC.presence_of_element_located(LoginPageLocators.USERNAME))
