import time

import pytest
from selenium.common import TimeoutException
from pages.build_synaptome import BuildSynaptomePage


class TestBuildSynaptome:

    def test_build_synaptome(self, setup, login, logger, test_config):
        browser, wait, base_url, lab_id, project_id = setup
        build_synaptome = BuildSynaptomePage(browser, wait, base_url)
        lab_id = test_config["lab_id"]
        project_id = test_config["project_id"]
        print(f"DEBUG: Using lab_id={lab_id}, project_id={project_id}")
        current_url = build_synaptome.go_to_build_synaptome(lab_id, project_id)

        project_menu_build = build_synaptome.find_menu_build()
        assert project_menu_build.is_displayed(), f"Build menu is not displayed."
        logger.info("Build menu is displayed.")

        synaptome_box = build_synaptome.find_synaptome_box()
        assert synaptome_box.is_displayed(), f"Synaptome box is not displayed."
        logger.info("Synaptome box is displayed")

        synaptome_box.click()
        logger.info("Synaptome box is clicked to start building synaptome.")

        synaptome_build_btn = build_synaptome.find_synaptome_build_btn()
        assert synaptome_build_btn.is_displayed(), f"Synaptome build button is not displayed."
        logger.info("Synaptome build button is displayed.")
        synaptome_build_btn.click()
        logger.info("Synaptome build button is clicked.")
