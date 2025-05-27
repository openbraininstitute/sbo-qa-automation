# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0


import random
import time
from datetime import datetime
from urllib.parse import urlparse
from selenium.webdriver import Keys

from pages.vl_home import VlabHome

class TestVlabHome:
    def test_vl_home(self, setup, login, logger,test_config):
        browser, wait, base_url, lab_id, project_id = setup
        vlab_home = VlabHome(browser,wait, base_url, logger=logger)
        lab_id = test_config["lab_id"]
        project_id = test_config["project_id"]
        print(f"DEBUG: Using lab_id={lab_id}, project_id={project_id}")

        public_projects = vlab_home.find_public_projects()
        assert public_projects.is_displayed(), f"Public projects are not displayed."
        logger.info("Public projects are displayed.")

        outside_explore = vlab_home.find_outside_explore()
        assert outside_explore.is_displayed(), f"Outside explore is not displayed."
        logger.info("Outside explore is displayed.")

        user_vlab = vlab_home.find_user_vlab()
        if not user_vlab.is_displayed():
            logger.info(f"Vlab has not been created yet.")
        else:
            logger.info(f"User vlab is displayed.")

        other_vlab = vlab_home.find_other_vlab()
        if not other_vlab.is_displayed():
            logger.info("The user has no virtual labs and has not been invited yet.")
        else:
            logger.info("The user has other virtual labs.")

        if user_vlab.is_displayed():
            go_to_your_lab = vlab_home.go_to_your_vlab()
            if go_to_your_lab.is_displayed():
                logger.info("Go to your lab page")
                num_projects_element = vlab_home.find_num_projects()
                num_projects = num_projects_element.text
                logger.info(f"Number of projects: {num_projects}")

                num_members_element = vlab_home.find_num_members()
                num_members = num_members_element.text
                logger.info(f"Number of members: {num_members}")
            else:
                logger.info("Go to your lab button is not displayed because the user has no virtual labs.")

        tutorials_carrousel = vlab_home.find_tutorials_carrousel()
        assert tutorials_carrousel.is_displayed(), f"Tutorials carrousel is not displayed."
        logger.info("Tutorials carrousel is displayed.")

        tutorials_title = vlab_home.find_tutorials_title()
        assert tutorials_title.is_displayed(), f"Tutorials title is not displayed."
        logger.info("Tutorials title is displayed.")

        tutorials_cards = vlab_home.find_tutorials_carts()
        assert len(tutorials_cards) == 3, f"Tutorials cards are not displayed."

        for idx, card in enumerate(tutorials_cards):
            print(f"Card {idx + 1} content: {card.text}")

        vlab_home.validate_and_return()

        qna_btn = vlab_home.find_qna_btn()
        assert qna_btn.is_displayed(), f"Q&A button is not displayed."
        logger.info("Q&A button is displayed.")

        qna_btn.click()
        logger.info("Q&A button is clicked.")
        menu_terms = vlab_home.find_menu_terms_btn()
        assert menu_terms.is_displayed(), f"Menu about button is not displayed."
        logger.info("Menu about button is displayed.")
        menu_terms.click()

        browser.back()
        current_url = browser.current_url
        logger.info(f"Navigated back from {current_url}.")

        home_btn = vlab_home.find_home_btn()
        assert home_btn.is_displayed(), f"Home button is not displayed."
        logger.info("Home button is displayed.")

        profile_btn = vlab_home.find_profile_btn()
        assert profile_btn.is_displayed(), f"Profile button is not displayed."
        logger.info("Profile button is displayed.")

        profile_btn.click()

        profile_menu_buttons = vlab_home.find_profile_menu_btns()
        for idx, (key, btn) in enumerate(profile_menu_buttons.items()):
            assert btn.is_displayed(), f"Profile menu button '{key}' is not displayed."
            logger.info(f"Profile menu button '{key}' ({idx + 1}) is displayed.")
