# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators.vlab_home_locators import VLHomeLocators
from pages.home_page import HomePage
from selenium.common import TimeoutException
import logging


class VlabHome(HomePage):
    def __init__(self, browser, wait, base_url, logger=None):
        super().__init__(browser, wait, base_url)
        self.home_page = HomePage(browser, wait, base_url)
        self.logger = logger or logging.getLogger(__name__)


    def go_to_vlab_home(self, lab_id: str, project_id: str):
        path = f"/app/virtual-lab"
        try:
            self.go_to_page(path)
            self.wait_for_page_ready(timeout=120)
        except TimeoutException:
            raise RuntimeError(f"Failed to load page at {path} within 60 seconds")
        return self.browser.current_url

    def find_home_btn(self):
        return self.find_element(VLHomeLocators.HOME_BTN)

    def find_menu_about_btn(self):
        return self.find_element(VLHomeLocators.MENU_ABOUT_OBI_BTN)

    def find_menu_contact_btn(self):
        return self.find_element(VLHomeLocators.MENU_CONTACT_OBI_BTN)

    def find_menu_terms_btn(self):
        return self.find_element(VLHomeLocators.MENU_TERMS_BTN)

    def find_num_members(self):
        return self.find_element(VLHomeLocators.NUM_MEMBERS)

    def find_num_projects(self):
        return self.find_element(VLHomeLocators.NUM_PROJECTS)

    def find_num_vlabs(self):
        return self.find_element(VLHomeLocators.NUM_VLABS)

    def find_other_vlab(self):
        return self.find_element(VLHomeLocators.OTHER_VLABS)

    def find_outside_explore(self):
        return self.find_element(VLHomeLocators.OUTSIDE_EXPLORE)

    def find_profile_btn(self):
        return self.find_element(VLHomeLocators.PROFILE_BTN)

    def find_public_projects(self, timeout=30):
        return self.find_element(VLHomeLocators.PUBLIC_PROJECTS, timeout=timeout)

    def find_qna_btn(self):
        return self.find_element(VLHomeLocators.QNA_BTN)

    def find_tutorials_carrousel(self):
        return self.find_element(VLHomeLocators.TUTORIALS_CARROUSEL)

    def find_tutorials_cards(self):
        return self.find_all_elements(VLHomeLocators.TUTORIALS_CARDS)

    def find_tutorials_title(self):
        return self.find_element(VLHomeLocators.TUTORIALS_TITLE)

    def find_user_vlab(self):
        return self.find_element(VLHomeLocators.USER_VLAB)

    def go_to_your_vlab(self):
        return self.find_element(VLHomeLocators.GO_TO_YOUR_VLAB)

    def find_profile_menu_btns(self):
        return {
            "account_profile_btn": self.find_element(VLHomeLocators.ACCOUNT_PROFILE_BTN),
            "account_invoice_btn": self.find_element(VLHomeLocators.ACCOUNT_INVOICES_BTN),
            "account_subscription_btn": self.find_element(VLHomeLocators.ACCOUNT_SUBSCRIPTIONS_BTN),
            "logout_btn": self.find_element(VLHomeLocators.LOGOUT_BTN)
        }

    def refresh_page(self):
        self.browser.refresh()
        self.wait_for_page_ready(timeout=120)

    def validate_and_return(self):
        """
        Helper method to:
        - Click the Q&A button to render menu options.
        - Click a specific menu option to navigate to its page.
        - Verify the expected URL snippet on the new page.
        - Navigate back to the original page.
        """
        qna_btn = self.find_element(VLHomeLocators.QNA_BTN)
        assert qna_btn.is_displayed(), "Q&A button is not displayed."
        qna_btn.click()
        self.logger.info("Q&A button clicked, menu options should now be visible.")

        def navigate_and_verify(menu_locator, expected_url_snippet):
            menu_btn = self.find_element(menu_locator, timeout=10)
            assert menu_btn.is_displayed(), f"Menu button is not displayed: {menu_locator}"
            menu_btn.click()
            self.logger.info(f"Menu button {menu_locator} clicked, navigating to the page.")

            self.wait_for_url_contains(expected_url_snippet, timeout=10)
            current_url = self.browser.current_url
            assert expected_url_snippet in current_url, (f"Expected URL to contain '{expected_url_snippet}', "
                                                         f"but got: {current_url}.")
            self.logger.info(f"Verified URL contains '{expected_url_snippet}': {current_url}")

            self.browser.back()
            self.logger.info(f"Navigated back from {expected_url_snippet}.")

            current_url = self.browser.current_url
            self.logger.info(f"DEBUG: Current URL after navigating back: {current_url}")

            qna_btn = WebDriverWait(self.browser, timeout=10).until(
                EC.element_to_be_clickable(VLHomeLocators.QNA_BTN)
            )
            qna_btn.click()
            self.logger.info("Q&A button re-clicked, menu options should now be visible again.")

        self.logger.info("Navigating to /about.")
        navigate_and_verify(VLHomeLocators.MENU_ABOUT_OBI_BTN, "/about")

        self.logger.info("Navigating to /contacts.")
        navigate_and_verify(VLHomeLocators.MENU_CONTACT_OBI_BTN, "/contact")

        self.logger.info("Navigating to /terms.")
        navigate_and_verify(VLHomeLocators.MENU_TERMS_BTN, "/terms")

        self.logger.info("All menu options validated successfully!")
