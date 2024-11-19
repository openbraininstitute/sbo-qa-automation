# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

import os.path
import time
import pytest
import requests

from pages.home_page import HomePage
from util.util_links_checker import LinkChecker
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
        browser, wait = setup
        home_page = HomePage(*setup)
        home_page.go_to_home_page()

        login_button = home_page.find_login_button()
        assert login_button.is_displayed()
        logger.info("'Login' button is found")
        login_button.click()



        # github_btn = home_page.find_github_btn()
        # logger.info("Github button found")
        # browser.execute_script("arguments[0].click();", github_btn)
        # logger.info("Github button CLICKED")


