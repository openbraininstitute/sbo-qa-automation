from locators.explore_page_locators import ExplorePageLocators
from selenium.webdriver.support import expected_conditions as EC

from pages.explore_page import ExplorePage
from pages.home_page import HomePage
from util.util_links_checker import LinkChecker
from util.util_scraper import UrlScraper


class ExploreElectrphysiologyPage(ExplorePage, LinkChecker):
    def __init__(self, browser, wait):
        super().__init__(browser, wait)
        self.home_page = ExplorePage(browser, wait)
        self.url_scraper = UrlScraper()

    def go_to_explore_ephys_page(self):
        self.browser.get(self.url + "/explore/electrophysiology")
        return self.browser.current_url

    def scrape_links(self):
        page_source = self.browser.page_source
        print("EPHYS page source", page_source)
        links = self.url_scraper.scrape_links(page_source)
        print("EPHYS links", links)

    def find_ephys_page_title(self):
        return self.wait.until(EC.presence_of_element_located(ExplorePageLocators.NEURON_EPHYS_PAGE_TITLE))

    def find_brain_region_header(self):
        return self.wait.until(EC.presence_of_element_located(ExplorePageLocators.BRAIN_REGION_COLUMN))

    def find_e_type_header(self):
        return self.wait.until(EC.presence_of_element_located(ExplorePageLocators.E_TYPE_COLUMN))

    def find_name_header(self):
        return self.wait.until(EC.presence_of_element_located(ExplorePageLocators.NAME_REGION_COLUMN))

    def find_species_header(self):
        return self.wait.until(EC.presence_of_element_located(ExplorePageLocators.SPECIES_REGION_COLUMN))

    def find_contributors_header(self):
        return self.wait.until(EC.presence_of_element_located(ExplorePageLocators.CONTRIBUTORS_COLUMN))

    def find_creation_date_header(self):
        return self.wait.until(EC.presence_of_element_located(ExplorePageLocators.CREATION_DATE_COLUMN))

    def find_search_label(self):
        return self.wait.until(EC.presence_of_element_located(ExplorePageLocators.SEARCH_LABEL))
