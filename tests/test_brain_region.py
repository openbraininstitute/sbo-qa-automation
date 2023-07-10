import time

import pytest
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium import webdriver

from pages.brain_region import BrainRegionPage
from util.util_base import load_config


class TestBrainBuild:
    @pytest.mark.build_page
    def test_build_page(self, setup, login_explore, logger):
        browser, wait = setup
        brain_region_page = BrainRegionPage(browser, wait)
        brain_region_url = brain_region_page.go_to_config_page()

        find_main_build_section = brain_region_page.find_build_main_section()
        open_build_div = brain_region_page.open_build_div()
        browser.execute_script("arguments[0].style.display = 'block'; arguments[0].style.visibility = 'visible';",
                               open_build_div)

        find_visible_basic_cells_txt = brain_region_page.find_visible_basic_cells()
        find_visible_basic_cells_txt.click()

        find_basic_cells_arrow_btn = brain_region_page.find_basic_cells_arrow_btn()
        # arrow_txt = find_basic_cells_arrow_btn.text
        # print("arrow is found and visible*************")
        find_basic_cells_arrow_btn.click()
        logger.info("Basic cell groups and regions first arrow is clicked ")

        # find_cerebrum_block = brain_region_page.find_block_cerebrum()
        # cerebrum_block_txt = find_cerebrum_block.text
        # print("CEREBRUM block found", cerebrum_block_txt)
        # # find_cerebrum_block.click()
        # browser.execute_script("arguments[0].style.display = 'block'; arguments[0].style.visibility = 'visible';",
        #                        find_cerebrum_block)
        #
        # find_cerebrum_arrow_btn = brain_region_page.find_basic_cells_arrow_btn()
        # arrow_btn_txt = find_cerebrum_arrow_btn.text
        # print("CEREBRUM ARRROW", cerebrum_block_txt)
        # find_cerebrum_arrow_btn.click()
        time.sleep(5)
