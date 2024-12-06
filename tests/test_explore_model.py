# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

import time
import os.path
import pytest
from selenium.webdriver import Keys

from locators.explore_page_locators import ExplorePageLocators
from pages.explore_model_page import ExploreModelDataPage
from pages.explore_page import ExplorePage


current_directory = os.getcwd()
relative_file_path = 'scraped_links.txt'
file_path = os.path.join(current_directory, relative_file_path)


class TestExploreModelPage:
    @pytest.mark.explore_page
    # @pytest.mark.run(order=3)
    def test_explore_model(self, setup, login, logger):
        """
        The commented out code below is pending changes in the platform.
        """
        browser, wait = setup
        explore_model = ExploreModelDataPage(browser, wait, logger)
        explore_model.go_to_explore_model_page()
        logger.info("Explore page is loaded")

        emodel_tab = explore_model.find_emodel_tab()
        logger.info("E-model data tab is found")


