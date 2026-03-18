# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
from selenium.common import TimeoutException

from locators.pricing_locators import PricingLocators
from pages.home_page import HomePage


class PricingPage(HomePage):
    def __init__(self, browser, wait, base_url, lab_url=None, logger=None):
        super().__init__(browser, wait, base_url)
        self.home_page = HomePage(browser, wait, base_url)
        self.logger = logger
        self.base_url = base_url
        self.lab_url = lab_url

    def go_to_page(self, retries=3, delay=5):
        pricing_url = f"{self.base_url}/pricing"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(60)
                self.browser.get(pricing_url)
                self.wait_for_page_ready(timeout=60)
                self.logger.info("✅ Pricing Page loaded successfully.")
                return
            except TimeoutException:
                self.logger.warning(
                    f"⚠️ Pricing Page load attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                import time
                time.sleep(delay)
        raise TimeoutException("❌ Failed to load Pricing Page after multiple attempts.")

    # Top nav
    def obi_homepage_logo(self):
        return self.is_visible(PricingLocators.OBI_HOMEPAGE_LOGO_BTN)

    def obi_menu(self):
        return self.element_visibility(PricingLocators.OBI_MENU)

    def obi_homepage_main_nav(self):
        return self.element_visibility(PricingLocators.OBI_HOMEPAGE_MAIN_NAV)

    # Hero section
    def pricing_main_title(self, timeout=10):
        return self.element_visibility(PricingLocators.PRICING_TITLE, timeout=timeout)

    def hero_img(self, timeout=15):
        return self.element_visibility(PricingLocators.HERO_IMG, timeout=timeout)

    def hero_video(self, timeout=20):
        return self.element_visibility(PricingLocators.HERO_VIDEO, timeout=timeout)

    def discover_plans_button(self, timeout=10):
        return self.find_element(PricingLocators.DISCOVER_PLANS, timeout=timeout)

    def scroll_to_plans(self):
        """Scroll down to the plan cards section and ensure window is wide enough for xl:grid."""
        self.browser.set_window_size(1440, 900)
        discover_btn = self.find_element(PricingLocators.DISCOVER_PLANS, timeout=10)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", discover_btn)
        discover_btn.click()
        import time
        time.sleep(2)

    # Plan cards
    def plan_cards_container(self, timeout=10):
        """Find the plan cards container. Note: uses presence check since the xl:grid
        container may be hidden on smaller viewports."""
        return self.find_element(PricingLocators.PLAN_CARDS_CONTAINER, timeout=timeout)

    def plan_cards(self, timeout=10):
        return self.find_all_elements(PricingLocators.PLAN_CARDS, timeout=timeout)

    def plan_card_free(self, timeout=10):
        return self.find_element(PricingLocators.PLAN_CARD_FREE, timeout=timeout)

    def plan_card_pro(self, timeout=10):
        return self.find_element(PricingLocators.PLAN_CARD_PRO, timeout=timeout)

    def plan_card_enterprise(self, timeout=10):
        return self.find_element(PricingLocators.PLAN_CARD_ENTERPRISE, timeout=timeout)

    def plan_card_education(self, timeout=10):
        return self.find_element(PricingLocators.PLAN_CARD_EDUCATION, timeout=timeout)

    # Contact Us
    def contact_us_enterprise(self, timeout=10):
        return self.find_element(PricingLocators.CONTACT_US_ENTERPRISE, timeout=timeout)

    def contact_us_education(self, timeout=10):
        return self.find_element(PricingLocators.CONTACT_US_EDUCATION, timeout=timeout)

    # Pro plan
    def pro_price(self, timeout=10):
        return self.find_element(PricingLocators.PRO_PRICE, timeout=timeout)

    def pro_subscription_toggle(self, timeout=10):
        return self.find_element(PricingLocators.PRO_SUBSCRIPTION_TOGGLE, timeout=timeout)

    # Footer
    def footer(self):
        return self.find_element(PricingLocators.FOOTER)

    # Legacy methods kept for backward compat
    def page_title(self, timeout=10):
        return self.discover_plans_button(timeout=timeout)

    def temp_goto_vlab_btn(self):
        return self.find_element(PricingLocators.TEMP_GOTO_VLAB_BTN)
