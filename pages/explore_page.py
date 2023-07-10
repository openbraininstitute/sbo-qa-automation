from locators.explore_page_locators import ExplorePageLocators
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage
from util.util_links_checker import LinkChecker
from util.util_scraper import UrlScraper


class ExplorePage(HomePage, LinkChecker):
    def __init__(self, browser, wait):
        super().__init__(browser, wait)
        self.home_page = HomePage(browser, wait)
        self.url_scraper = UrlScraper()

    def go_to_explore_page(self):
        self.browser.get(self.url + "/explore")
        return self.browser.current_url

    def scrape_links(self):
        page_source = self.browser.page_source
        links = self.url_scraper.scrape_links(page_source)

    def wait_for_dynamically_loaded_links(self):
        self.wait.until(EC.presence_of_element_located(ExplorePageLocators.EXPLORE_LINK1))

    def check_explore_title_is_present(self):
        return self.wait.until(EC.element_to_be_clickable(ExplorePageLocators.EXPLORE_TITLE))

    def brain_and_cell_title(self):
        return self.wait.until(EC.presence_of_element_located(ExplorePageLocators.BRAIN_CELL_ANNOTATIONS))

    def experimental_data_title(self):
        return self.wait.until(EC.presence_of_element_located(ExplorePageLocators.EXPERIMENTAL_DATA))

    def digital_reconstruction_title(self):
        return self.wait.until(EC.presence_of_element_located(ExplorePageLocators.DIGITAL_RECONSTRUCTION))

    def simulations_title(self):
        return self.wait.until(EC.presence_of_element_located(ExplorePageLocators.SIMULATIONS))
