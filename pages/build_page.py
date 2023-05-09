from locators.build_page_locators import BuildPageLocators
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage


class BuildPage(HomePage):
    def __init__(self, browser, wait):
        super().__init__(browser, wait)
        self.login_page = HomePage(browser, wait)

    def go_to_build_page(self):
        self.browser.get(self.url + "/build/load-brain-config")
        return self.browser.current_url

    def find_recent_configurations(self):
        return self.wait.until(EC.presence_of_element_located(BuildPageLocators.RECENT_CONFIGURATIONS))

    def verify_release_version(self):
        return self.wait.until(EC.presence_of_element_located(BuildPageLocators.RELEASE_VERSION))

    def select_default_config(self):
        return self.wait.until(EC.presence_of_element_located(BuildPageLocators.BUILD_PAGE_CLICK_PLUS_ICON))

    def find_config_search_field(self):
        return self.wait.until(EC.presence_of_element_located(BuildPageLocators.CONFIG_SEARCH_FIELD))