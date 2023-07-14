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
        links = self.url_scraper.scrape_links(page_source)

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

    def find_search_input_search_item(self):
        return self.wait.until(EC.presence_of_element_located(ExplorePageLocators.SEARCH_INPUT_FIELD))

    def find_filter_btn(self):
        return self.wait.until(EC.presence_of_element_located(ExplorePageLocators.FILTER_BTN))

    def find_filter_close_btn(self):
        return self.wait.until(EC.presence_of_element_located(ExplorePageLocators.FILTER_CLOSE_BTN))

    def find_plus_btn(self):
        return self.wait.until(EC.presence_of_element_located(ExplorePageLocators.SIDE_BAR_PLUS_BTN))

    def find_side_bar_explore_btn(self):
        return self.wait.until(EC.presence_of_element_located(ExplorePageLocators.SIDE_BAR_EXPLORE_BTN))

    def find_side_bar_plus_btn(self):
        return self.wait.until(EC.presence_of_element_located(ExplorePageLocators.SIDE_BAR_PLUS_BTN))

    def find_side_bar_menu(self):
        return self.wait.until(EC.presence_of_element_located(ExplorePageLocators.SIDE_BAR_MENU))

    def find_side_bar_menu_close_btn(self):
        return self.wait.until(EC.presence_of_element_located(ExplorePageLocators.SIDE_BAR_MENU_CLOSE_BTN))