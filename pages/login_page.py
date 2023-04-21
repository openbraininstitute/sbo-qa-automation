from locators.home_page_locators import HomePageLocators
from locators.login_locators import LoginPageLocators
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC


class LoginPage(BasePage):
    def __init__(self, browser, wait):
        super().__init__(browser, wait)

    # def go_to_home_page(self):
    #     self.browser.get(self.url)

    def find_login_button(self):
        return self.wait.until(EC.element_to_be_clickable(LoginPageLocators.LOGIN_BUTTON))

    def login(self, username):
        # username_field = self.driver.find_element(*LoginPageLocators.USERNAME)
        pass
