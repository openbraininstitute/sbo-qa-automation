from locators.build_page_locators import BuildPageLocators
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import CustomBasePage
from seleniumbase import BaseCase
from pages.home_page import HomePage
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from urllib.parse import urlparse, parse_qs


class BrainRegionPage(HomePage, CustomBasePage):
    def __init__(self, browser, wait):
        super().__init__(browser, wait)
        self.login_page = HomePage(browser, wait)

    def go_to_config_page(self):
        # return self.browser.get(
        #     "https://bbp.epfl.ch/mmb-beta/build/cell-composition/interactive?brainModelConfigId=8a962b3a-2005-4bc1-9b35-c20c2ec4cc54")
        config_id = '8a962b3a-2005-4bc1-9b35-c20c2ec4cc54'  # Set the desired config ID
        config_url = f"https://bbp.epfl.ch/mmb-beta/build/cell-composition/interactive?brainModelConfigId={config_id}"
        self.browser.get(config_url)
        return config_url

    def find_build_main_section(self):
        return self.wait.until(EC.presence_of_element_located(BuildPageLocators.BRAIN_BUILD_SECTION_MAIN))

    def open_build_div(self):
        return self.wait.until(EC.presence_of_element_located(BuildPageLocators.BRAIN_BUILD_CLOSED_DIV))

    def find_visible_basic_cells(self):
        return self.wait.until(EC.visibility_of_element_located(BuildPageLocators.VISIBLE_BASIC_CELL_GROUPS_TEXT))

    def find_basic_cells_arrow_btn(self):
        return self.wait.until(EC.element_to_be_clickable(BuildPageLocators.BASIC_CELL_GROUPS_ARROW_BTN))

    def find_block_cerebrum(self):
        return self.wait.until(EC.visibility_of_element_located(BuildPageLocators.BLOCK_CEREBRUM))

    def cerebrum_arrow_btn(self):
        return self.wait.until(EC.element_to_be_clickable(BuildPageLocators.CEREBRUM_ARROW_BUTTON))
