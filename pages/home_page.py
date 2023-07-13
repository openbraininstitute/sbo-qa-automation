import json

from locators.home_page_locators import HomePageLocators
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import CustomBasePage
from util.util_links_checker import LinkChecker
from util.util_scraper import UrlScraper


class HomePage(CustomBasePage, LinkChecker):

    def __init__(self, browser, wait):
        super().__init__(browser, wait)
        self.url_scraper = UrlScraper()

    def go_to_home_page(self):
        self.browser.get(self.url)

    def scrape_links(self):
        page_source = self.browser.page_source
        links = self.url_scraper.scrape_links(page_source)

    def find_explore_title(self):
        return self.wait.until(EC.presence_of_element_located(HomePageLocators.EXPLORE_TITLE))

    def find_build_title(self):
        return self.wait.until(EC.presence_of_element_located(HomePageLocators.BUILD_TITLE))

    def find_simulate_title(self):
        return self.wait.until(EC.presence_of_element_located(HomePageLocators.SIMULATE_TITLE))

    def find_login_button(self):
        return self.wait.until(EC.element_to_be_clickable(HomePageLocators.LOGIN_BUTTON))
