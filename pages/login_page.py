import time

from locators.login_locators import LoginPageLocators
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage


class LoginPage(HomePage):
    def __init__(self, browser, wait):
        super().__init__(browser, wait)
        self.login_page = HomePage(browser, wait)

    def go_to_login_page(self, url):
        self.browser.get(url)

        self.wait.until(EC.url_contains(url))

    def already_logged(self):
        return self.wait.until(EC.presence_of_element_located(LoginPageLocators.ALREADY_LOGGED))

    def find_username_field(self):
        return self.wait.until(EC.presence_of_element_located(LoginPageLocators.USERNAME))

    def find_password_field(self):
        return self.wait.until(EC.presence_of_element_located(LoginPageLocators.PASSWORD))

    def find_signin_button(self):
        return self.wait.until(EC.element_to_be_clickable(LoginPageLocators.SIGN_IN))

    def find_logout_button(self):
        return self.wait.until(EC.element_to_be_clickable(LoginPageLocators.LOGOUT))
