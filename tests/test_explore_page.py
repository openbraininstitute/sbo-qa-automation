import time
import os.path
import pytest
import requests

from pages.explore_page import ExplorePage
from util.util_links_checker import LinkChecker
from util.util_links_writer import write_links_to_file
from util.util_load_links import LinkUtil
from util.util_scraper import UrlScraper

current_directory = os.getcwd()
relative_file_path = 'scraped_links.txt'
file_path = os.path.join(current_directory, relative_file_path)


class TestExplorePage:
    @pytest.mark.explore_page
    def test_explore_page(self, setup, login_explore, logger):
        browser, wait = login_explore
        explore_page = ExplorePage(browser, wait)
        exp_url = explore_page.go_to_explore_page()
        assert exp_url == "https://bbp.epfl.ch/mmb-beta/explore"
        logger.info("Explore page is loaded")

        # Checking the titles of the Explore Page
        check_explore_title = explore_page.check_explore_title_is_present()
        assert check_explore_title.text.lower() == 'Explore'.lower()
        logger.info("Checking that the main title of Explore page is present")

        brain_and_cells = explore_page.brain_and_cell_title()
        brain_txt = brain_and_cells.text
        print(brain_txt)
        assert brain_txt == "Brain & cells annotations"
        logger.info("Checking that the Brain & cells annotations is present")

        experimental_data = explore_page.experimental_data_title()
        exp_data = experimental_data.text
        assert exp_data == "Experimental data"
        logger.info("Experimental data title is present on the page")

        digital_reconstruction = explore_page.digital_reconstruction_title()
        digital = digital_reconstruction.text
        print(digital, "CHECKING DIGITAL")
        assert digital == "Brain models"
        logger.info("Brain models title is present and unchanged")

        simulations = explore_page.simulations_title()
        simul = simulations.text
        print(simul, "CHECKING SIMULATIONS")
        assert simul == "Simulations"
        logger.info("Verifying Simulations title is found on the page")

    def test_links(self):
        test_directory = os.path.dirname(os.path.abspath(__file__))
        links_file_path = os.path.join(test_directory, '..', 'links.json')

        link_checker = LinkChecker()
        links = link_checker.load_links(links_file_path)['explore_page_links']
        link_checker.check_links(links)
        # url = "https://bbp.epfl.ch/mmb-beta/explore"
        # response = requests.get(url)
        # page_source = response.text
        # print(page_source, "THIS IS FROM THE EXPLORE_TEST, PAGE_LINKS")
        # url_scraper = UrlScraper()
        # scraped_links = url_scraper.scrape_links(page_source)
        #
        # write_links_to_file(file_path, scraped_links)
        # # print("Scraped links from Explore page saved to file successfully")
        # print("File path EXPLORE test", file_path)
        # print("Scraped links EXPLORE page", scraped_links)
