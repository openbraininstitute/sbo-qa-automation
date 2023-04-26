from locators.explore_page_locators import ExplorePageLocators
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage


class ExplorePage(HomePage):
    def __init__(self, browser, wait):
        super().__init__(browser, wait)
        self.login_page = HomePage(browser, wait)

    def go_to_explore_page(self):
        self.browser.get(self.url + "/explore")
        return self.browser.current_url

    def check_explore_title_is_present(self):
        return self.wait.until(EC.element_to_be_clickable(ExplorePageLocators.EXPLORE_TITLE))
