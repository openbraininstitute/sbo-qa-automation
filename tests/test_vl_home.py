# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0


import random
from datetime import datetime
from urllib.parse import urlparse
from selenium.webdriver import Keys

from pages.vl_home import VlabHome

class TestVlabHome:
    def test_vl_home(self, setup, login, logger,test_config):
        browser, wait, base_url, lab_id, project_id = setup
        vlab_home = VlabHome(browser,wait, base_url)
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


        qna_btn = vlab_home.find_qna_btn()
        if qna_btn.is_displayed():
            qna_btn.click()
            logger.info("Q&A button is clicked.")
            menu_about = vlab_home.find_menu_about_btn()
            logger.info("Menu about button is displayed.")
            menu_contact = vlab_home.find_menu_contact_btn()
            logger.info("Menu contact button is displayed.")
            menu_terms = vlab_home.find_menu_terms_btn()
            logger.info("Menu terms button is displayed.")
        else:
            logger.info("Q&A button is not displayed.")

        home_btn = vlab_home.find_home_btn()
        assert home_btn.is_displayed(), f"Home button is not displayed."
        logger.info("Home button is displayed.")

        profile_btn = vlab_home.find_profile_btn()
        assert profile_btn.is_displayed(), f"Profile button is not displayed."
        logger.info("Profile button is displayed.")

