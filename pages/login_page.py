from locators.login_locators import LoginPageLocators
import logging


class LoginPage:
    def __int__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)

    def enter_username(self, username):
        self.logger.info("Entering username: %s" % username)
        # username_field = self.driver.find_element(*LoginPageLocators.USERNAME)
