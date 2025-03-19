# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import os.path
import time
import pytest
import requests

from pages.home_page import HomePage
from util.util_links_checker import LinkChecker
from util.util_links_handler import LinkHandler
from util.util_links_writer import write_links_to_file
from util.util_scraper import UrlScraper

'''
Get the current working directory
Specify the relative path to the file from the current directory
Join the current directory with the relative file path
'''
current_directory = os.getcwd()
relative_file_path = 'scraped_links.txt'
file_path = os.path.join(current_directory, relative_file_path)


@pytest.mark.usefixtures("setup", "logger")
class TestFindLogin:
    @pytest.mark.run(order=2)
    def test_homepage(self, setup, logger):
        browser, wait, base_url = setup
        home_page = HomePage(*setup)
        home_page.go_to_home_page()
        bb_github = home_page.find_github_btn()
        assert bb_github.is_displayed(), "The BlueBrain Github button is not found"
        logger.info("BlueBrain Github button is displayed")

        about_btn = home_page.find_about_btn()
        assert about_btn.is_displayed(), "The About button is displayed"
        logger.info("About button is found")

        big_title1 = home_page.find_big_title1()
        assert big_title1.text.strip() != "", "The big title is found, but is empty"
        logger.info("First big title is found")
        big_title2 = home_page.find_big_title2()
        assert big_title2.text.strip() != "", "The big title is found, but is empty"
        logger.info("Second big title is found")

        contributor = home_page.find_contributor()
        logger.info("Found contributor")
        contributors_table = home_page.find_contributor_table()
        logger.info("Scrolled to the Github button, and it is displayed")
        assert contributors_table.is_displayed(), "The table is displayed"

        contributor_a = home_page.find_contributor()
        assert contributor_a, "Contributor is found"

        logo1 = home_page.find_bbop_logo1()
        assert logo1.is_displayed(), "The logo is not displayed"
        logger.info("Top logo is displayed")

        logo2 = home_page.find_bbop_logo1()
        assert logo1.is_displayed(), "The logo is not displayed"
        logger.info("Bottom logo is displayed")

        letter_a = home_page.find_a_letter()
        assert letter_a, f"Letter A is not found"
        letter_a.click()
        time.sleep(3)

        login_button = home_page.find_login_button()
        assert login_button.is_displayed()
        logger.info("'Login' button is found")
        login_button.click()

    # def test_links_on_homepage(self, setup):
    #     """Test all links on the homepage and check their statuses."""
    #     browser, wait, base_url = setup
    #     link_handler = LinkHandler(browser)
    #     links = link_handler.scrape_links()
    #
    #     # Optional: Save links to a file
    #     file_path = os.path.join(os.getcwd(), "scraped_links.json")
    #     link_handler.write_links_to_file(links, file_path)
    #
    #     # Validate link status
    #     link_handler.check_links(links)