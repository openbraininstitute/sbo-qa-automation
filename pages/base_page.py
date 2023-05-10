from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.base_page_locators import BasePageLocators
import pytest

@pytest.mark.usefixtures("setup", "logger")
class BasePage:

    def __init__(self, browser, wait):
        self.browser = browser
        self.wait = wait
        self.url = "https://bbp.epfl.ch/mmb-beta"
    #
    # def wait_for_loading(self, logger):
    #     logger.info("Waiting for element to load")
    #     element = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(BasePageLocators.PAGE_LOAD))