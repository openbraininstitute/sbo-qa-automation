from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.base_page_locators import BasePageLocators
# from util.util_base import logger


class BasePage:

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 10)
        # self.logger = logger


    def wait_for_loading(self):
        self.logger.info("Waiting for element to load")
        self.wait.until_not(EC.presence_of_element_located(BasePageLocators.PAGE_LOAD))