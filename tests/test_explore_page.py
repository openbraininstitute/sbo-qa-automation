import time
import pytest
from pages.explore_page import ExplorePage
from selenium.webdriver.support import expected_conditions as EC


class TestExplorePage:
    @pytest.mark.explore_page
    def test_explore_page(self, setup, login_explore, logger):
        browser, wait = login_explore
        explore_page = ExplorePage(browser, wait)
        exp_url = explore_page.go_to_explore_page()
        # assert EC.url_contains("explore") in browser.current_url
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

        experimental_data = explore_page.experimental_data_title()
        exp_data = experimental_data.text
        assert exp_data == "Experimental Data"

        digital_reconstruction = explore_page.digital_reconstruction_title()
        digital = digital_reconstruction.text
        print(digital, "CHECKING DIGITAL")
        assert digital == "Digital reconstructions"

        simulations = explore_page.simulations_title()
        simul = simulations.text
        print(simul, "CHECKING SIMULATIONS")
        assert simul == "Simulations"