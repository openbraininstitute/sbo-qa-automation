# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

import time
import os.path
import pytest
import requests

from locators.explore_page_locators import ExplorePageLocators
from pages.explore_page import ExplorePage
from util.util_links_checker import LinkChecker
from util.util_links_writer import write_links_to_file
from util.util_scraper import UrlScraper

current_directory = os.getcwd()
relative_file_path = 'scraped_links.txt'
file_path = os.path.join(current_directory, relative_file_path)


class TestExplorePage:
    @pytest.mark.explore_page
    @pytest.mark.run(order=3)
    def test_explore_page(self, setup, login, logger):
        """
        The commented out code below is pending changes in the platform.
        """
        browser, wait = setup
        explore_page = ExplorePage(browser, wait)
        exp_url = explore_page.go_to_explore_page()
        logger.info("Explore page is loaded")

        """Checking the titles of the Explore Page"""
        check_explore_title = explore_page.check_explore_title_is_present()
        logger.info("Explore page title is present")

        exp_data_titles = [
            ExplorePageLocators.NEURON_MORPHOLOGY,
            ExplorePageLocators.NEURON_ELECTROPHYSIOLOGY,
            ExplorePageLocators.NEURON_DENSITY,
            ExplorePageLocators.BOUTON_DENSITY,
            ExplorePageLocators.SYNAPSE_PER_CONNECTION
        ]
        logger.info("Searching for Experimental Data types")
        exp_data_titles = explore_page.find_experimental_data_titles(exp_data_titles)
        for title in exp_data_titles:
            assert title.is_displayed(), f"Experimental data {title} is not displayed."
        logger.info("Found Experimental data titles")

        page_titles = [
            ExplorePageLocators.EXPERIMENTAL_DATA_BTN,
            ExplorePageLocators.MODEL_DATA_BTN,
            ExplorePageLocators.LITERATURE
        ]
        logger.info("Found Explore Page titles")
        explore_page_titles = explore_page.find_explore_page_titles(page_titles)

        for page_title in explore_page_titles:
            assert page_title.is_displayed(), f"Explore page titles {page_title} is not displayed"
        logger.info("Found Explore page titles")

        record_count_locators = [
            ExplorePageLocators.MORPHOLOGY_NRECORDS,
            ExplorePageLocators.NEURON_EPHYS_NRECORDS,
            ExplorePageLocators.NEURON_DENSITY_NRECORDS,
            ExplorePageLocators.BOUTON_DENSITY_NRECORDS,
            ExplorePageLocators.SYNAPSE_PER_CONNECTION_NRECORDS
        ]
        record_counts = explore_page.get_experiment_record_count(record_count_locators)
        for record_count in record_counts:
            assert record_count >= 1, f"Record count is less than 100: {record_count}"
        logger.info("Record counts validation passed")

    # def test_links(self):
    #     """
    #     test_links methods checks the request status
    #     Also, writes non-dynamic URLs that are present on the page to a text file.
    #     """
    #     test_directory = os.path.dirname(os.path.abspath(__file__))
    #     links_file_path = os.path.join(test_directory, '..', 'links.json')
    #
    #     link_checker = LinkChecker()
    #     links = link_checker.load_links(links_file_path)['explore_links']
    #     link_checker.check_links(links)
    #     url = "https://openbluebrain.com/app/explore/electrophysiology"
    #     response = requests.get(url)
    #     page_source = response.text
    #     url_scraper = UrlScraper()
    #     scraped_links = url_scraper.scrape_links(page_source)
    #     write_links_to_file(file_path, scraped_links)
