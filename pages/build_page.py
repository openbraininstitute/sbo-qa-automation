from locators.build_page_locators import BuildPageLocators
from locators.home_page_locators import HomePageLocators
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage
from pages.login_page import LoginPage


class BuildPage(HomePage):
    def __init__(self, browser, wait):
        super().__init__(browser, wait)
        self.login_page = LoginPage(browser, wait)

    def go_to_build_page(self):
        self.wait.until(EC.element_to_be_clickable(HomePageLocators.BUILD_URL)).click()


    # def click_on_build_page_url(self):
    #     self.browser.get(HomePage.BUILD_URL)

    def find_recent_configurations(self):
        self.wait.until(EC.presence_of_element_located(BuildPageLocators.RECENT_CONFIGURATIONS))
