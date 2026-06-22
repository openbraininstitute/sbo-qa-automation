# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from locators.project_credits_locators import ProjectCreditsLocators
from pages.home_page import HomePage


class ProjectCreditsPage(HomePage):
    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, base_url)
        self.logger = logger

    # --- Navigation ---

    def go_to_credits_page(self, lab_id: str, project_id: str):
        """Navigate directly to the project credits page."""
        path = f"/app/virtual-lab/{lab_id}/{project_id}/credits"
        try:
            self.browser.set_page_load_timeout(90)
            self.go_to_page(path)
            self.wait_for_page_ready(timeout=60)
        except TimeoutException:
            raise RuntimeError("The Project Credits page did not load within 60 seconds.")
        return self.browser.current_url

    def click_credits_pill(self, timeout=15):
        """Click the credit pill button in the top navigation bar."""
        pill = self.element_to_be_clickable(ProjectCreditsLocators.CREDITS_PILL, timeout=timeout)
        pill.click()
        return pill

    # --- Credits panel ---

    def credits_panel(self, timeout=20):
        """Find the main credits panel container."""
        return self.find_element(ProjectCreditsLocators.CREDITS_PANEL, timeout=timeout)

    def get_vlab_credits_value(self, timeout=10):
        """Get the virtual lab credits balance text."""
        el = self.find_element(ProjectCreditsLocators.VLAB_CREDITS_VALUE, timeout=timeout)
        return el.text.strip()

    def get_project_credits_value(self, timeout=10):
        """Get the project credits balance text."""
        el = self.find_element(ProjectCreditsLocators.PROJECT_CREDITS_VALUE, timeout=timeout)
        return el.text.strip()

    # --- Action buttons ---

    def click_pricing_btn(self, timeout=10):
        """Click the Pricing button. Opens a new tab to /pricing."""
        btn = self.element_to_be_clickable(ProjectCreditsLocators.PRICING_BTN, timeout=timeout)
        btn.click()

    def click_buy_credits_btn(self, timeout=10):
        """Click the Buy credits button. Opens the buy credits modal."""
        btn = self.element_to_be_clickable(ProjectCreditsLocators.BUY_CREDITS_BTN, timeout=timeout)
        btn.click()

    def click_transfer_credits_btn(self, timeout=10):
        """Click the Transfer credits button. Opens the transfer credits modal."""
        btn = self.element_to_be_clickable(
            ProjectCreditsLocators.TRANSFER_CREDITS_BTN, timeout=timeout
        )
        btn.click()

    # --- Transfer credits modal ---

    def transfer_credits_modal(self, timeout=15):
        """Find the transfer credits modal dialog (waits for visibility)."""
        return self.element_visibility(ProjectCreditsLocators.TRANSFER_CREDITS_MODAL, timeout=timeout)

    def get_transfer_from_value(self, timeout=10):
        """Get the 'From Virtual lab' credits value in the transfer modal."""
        el = self.find_element(ProjectCreditsLocators.TRANSFER_CREDITS_FROM_VALUE, timeout=timeout)
        return el.text.strip()

    def get_transfer_to_value(self, timeout=10):
        """Get the 'To Automated Project' credits value in the transfer modal."""
        el = self.find_element(ProjectCreditsLocators.TRANSFER_CREDITS_TO_VALUE, timeout=timeout)
        return el.text.strip()

    def enter_transfer_amount(self, amount: str, timeout=10):
        """Enter the number of credits to transfer."""
        input_field = self.find_element(
            ProjectCreditsLocators.TRANSFER_CREDITS_AMOUNT_INPUT, timeout=timeout
        )
        input_field.clear()
        input_field.send_keys(amount)
        time.sleep(0.5)

    def get_transfer_amount_value(self, timeout=10):
        """Get current value of the transfer amount input field."""
        input_field = self.find_element(
            ProjectCreditsLocators.TRANSFER_CREDITS_AMOUNT_INPUT, timeout=timeout
        )
        return input_field.get_attribute("value")

    def click_transfer_submit_btn(self, timeout=10):
        """Click the Transfer credits submit button inside the modal."""
        btn = self.element_to_be_clickable(
            ProjectCreditsLocators.TRANSFER_CREDITS_SUBMIT_BTN, timeout=timeout
        )
        btn.click()

    def close_transfer_modal(self, timeout=10):
        """Close the transfer credits modal by clicking the X button."""
        close_btn = self.element_to_be_clickable(
            ProjectCreditsLocators.TRANSFER_CREDITS_CLOSE_BTN, timeout=timeout
        )
        close_btn.click()

    # --- History table ---

    def history_title(self, timeout=10):
        return self.find_element(ProjectCreditsLocators.HISTORY_TITLE, timeout=timeout)

    def history_table(self, timeout=15):
        return self.find_element(ProjectCreditsLocators.HISTORY_TABLE, timeout=timeout)

    def get_history_table_headers(self, timeout=10):
        """Return list of header texts from the history table."""
        headers = self.find_all_elements(ProjectCreditsLocators.HISTORY_TABLE_HEADERS, timeout=timeout)
        return [h.text.strip() for h in headers if h.text.strip()]

    def get_history_table_rows(self, timeout=10):
        """Return all visible rows in the history table."""
        return self.find_all_elements(ProjectCreditsLocators.HISTORY_TABLE_ROWS, timeout=timeout)

    def history_pagination(self, timeout=10):
        return self.find_element(ProjectCreditsLocators.HISTORY_PAGINATION, timeout=timeout)

    # --- Buy credits modal ---

    def modal_dialog(self, timeout=15):
        return self.element_visibility(ProjectCreditsLocators.MODAL_DIALOG, timeout=timeout)

    def get_modal_title(self, timeout=10):
        el = self.find_element(ProjectCreditsLocators.MODAL_TITLE, timeout=timeout)
        return el.text.strip()

    def close_modal(self, timeout=10):
        """Close the modal by clicking the X button."""
        close_btn = self.element_to_be_clickable(ProjectCreditsLocators.MODAL_CLOSE_BTN, timeout=timeout)
        close_btn.click()

    # --- Payment mode selection ---

    def payment_mode_selection(self, timeout=10):
        return self.find_element(ProjectCreditsLocators.PAYMENT_MODE_SELECTION, timeout=timeout)

    def click_purchase_credits_card(self, timeout=10):
        """Click 'Purchase Credits' card in the buy credits modal."""
        card = self.element_to_be_clickable(
            ProjectCreditsLocators.PURCHASE_CREDITS_CARD, timeout=timeout
        )
        card.click()

    def click_promo_code_card(self, timeout=10):
        """Click 'Promo Code' card in the buy credits modal."""
        card = self.element_to_be_clickable(
            ProjectCreditsLocators.PROMO_CODE_CARD, timeout=timeout
        )
        card.click()

    # --- Stripe payment flow ---

    def stripe_payment_flow(self, timeout=15):
        return self.find_element(ProjectCreditsLocators.STRIPE_PAYMENT_FLOW, timeout=timeout)

    def click_stripe_back_btn(self, timeout=10):
        """Click the 'Select option' back button on the Stripe payment screen."""
        btn = self.element_to_be_clickable(ProjectCreditsLocators.STRIPE_BACK_BTN, timeout=timeout)
        btn.click()

    def enter_credits_amount(self, amount: str, timeout=10):
        """Type the number of credits to purchase."""
        input_field = self.find_element(ProjectCreditsLocators.CREDITS_INPUT, timeout=timeout)
        input_field.clear()
        input_field.send_keys(amount)
        time.sleep(1)  # Allow order details to update

    def get_credits_input_value(self, timeout=10):
        """Get current value of the credits input field."""
        input_field = self.find_element(ProjectCreditsLocators.CREDITS_INPUT, timeout=timeout)
        return input_field.get_attribute("value")

    def get_order_subtotal(self, timeout=10):
        el = self.find_element(ProjectCreditsLocators.ORDER_DETAILS_SUBTOTAL, timeout=timeout)
        return el.text.strip()

    def get_order_vat(self, timeout=10):
        el = self.find_element(ProjectCreditsLocators.ORDER_DETAILS_VAT, timeout=timeout)
        return el.text.strip()

    def get_order_total(self, timeout=10):
        el = self.find_element(ProjectCreditsLocators.ORDER_DETAILS_TOTAL, timeout=timeout)
        return el.text.strip()

    def stripe_address_iframe(self, timeout=15):
        """Find the Stripe address input iframe element."""
        return self.find_element(ProjectCreditsLocators.STRIPE_ADDRESS_IFRAME, timeout=timeout)

    def stripe_payment_iframe(self, timeout=15):
        """Find the Stripe payment input iframe element."""
        return self.find_element(ProjectCreditsLocators.STRIPE_PAYMENT_IFRAME, timeout=timeout)

    def click_cancel_btn(self, timeout=10):
        """Click Cancel on the Stripe payment form."""
        btn = self.element_to_be_clickable(ProjectCreditsLocators.CANCEL_BTN, timeout=timeout)
        btn.click()

    def pay_btn(self, timeout=10):
        """Find the Pay button (may be disabled)."""
        return self.find_element(ProjectCreditsLocators.PAY_BTN, timeout=timeout)

    def is_pay_btn_disabled(self, timeout=10):
        """Check if the Pay button is currently disabled."""
        btn = self.pay_btn(timeout=timeout)
        return btn.get_attribute("disabled") is not None

    # --- Tab management (for Pricing button) ---

    def wait_for_new_tab(self, timeout=15):
        """Wait for a second browser tab to open."""
        WebDriverWait(self.browser, timeout).until(
            lambda d: len(d.window_handles) > 1,
            "Second tab did not open within timeout",
        )
        return self.browser.window_handles

    def switch_to_new_tab(self):
        """Switch to the most recently opened tab."""
        handles = self.browser.window_handles
        self.browser.switch_to.window(handles[-1])
        return self.browser.current_url

    def close_tab_and_switch_back(self):
        """Close current tab and switch back to the first tab."""
        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[0])

    # --- Stripe iframe interactions ---

    def _switch_to_iframe(self, iframe_element, timeout=10):
        """Switch webdriver context into an iframe element."""
        WebDriverWait(self.browser, timeout).until(
            EC.frame_to_be_available_and_switch_to_it(iframe_element)
        )

    def _switch_to_default(self):
        """Switch back to main page context from an iframe."""
        self.browser.switch_to.default_content()

    def fill_billing_address(self, country_code="CH", address="123 Test Street",
                             city="Geneva", postal_code="1200", timeout=15):
        """
        Fill the billing address form inside the Stripe address iframe.
        Must be called after the Stripe payment flow is visible.

        Args:
            country_code: ISO country code (e.g. 'CH', 'US', 'DE')
            address: Street address
            city: City name
            postal_code: Postal/ZIP code
        """
        iframe = self.stripe_address_iframe(timeout=timeout)
        self.browser.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", iframe
        )
        self._switch_to_iframe(iframe)

        try:
            # Select country from dropdown
            country_select = WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "select#billingAddress-countryInput")
                )
            )
            from selenium.webdriver.support.ui import Select
            Select(country_select).select_by_value(country_code)
            time.sleep(1)  # Wait for form fields to update based on country

            # Fill address line 1
            address_input = WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input#billingAddress-addressLine1Input")
                )
            )
            address_input.clear()
            address_input.send_keys(address)

            # Fill postal code (may appear depending on country)
            try:
                postal_input = self.browser.find_element(
                    By.CSS_SELECTOR, "input#billingAddress-postalCodeInput"
                )
                if postal_input.is_displayed():
                    postal_input.clear()
                    postal_input.send_keys(postal_code)
            except Exception:
                self.logger.info("Postal code field not visible for this country")

            # Fill city (may appear depending on country)
            try:
                city_input = self.browser.find_element(
                    By.CSS_SELECTOR, "input#billingAddress-localityInput"
                )
                if city_input.is_displayed():
                    city_input.clear()
                    city_input.send_keys(city)
            except Exception:
                self.logger.info("City field not visible for this country")

        finally:
            self._switch_to_default()

        self.logger.info(
            f"Billing address filled: country={country_code}, "
            f"address={address}, city={city}, postal={postal_code}"
        )

    def fill_card_details(self, card_number="4242424242424242",
                          expiry="1229", cvc="123", timeout=15):
        """
        Fill the card payment form inside the Stripe payment iframe.
        Uses Stripe test card number by default.

        Args:
            card_number: Card number (no spaces)
            expiry: Expiry in MMYY format (e.g. '1229' for 12/29)
            cvc: 3-digit security code
        """
        iframe = self.stripe_payment_iframe(timeout=timeout)
        self.browser.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", iframe
        )
        self._switch_to_iframe(iframe)

        try:
            # Card number
            card_input = WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input#payment-numberInput")
                )
            )
            card_input.clear()
            card_input.send_keys(card_number)

            # Expiry (MM/YY)
            expiry_input = WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input#payment-expiryInput")
                )
            )
            expiry_input.clear()
            expiry_input.send_keys(expiry)

            # CVC
            cvc_input = WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input#payment-cvcInput")
                )
            )
            cvc_input.clear()
            cvc_input.send_keys(cvc)

        finally:
            self._switch_to_default()

        self.logger.info("Card details filled (Stripe test card)")

    def wait_for_pay_btn_enabled(self, timeout=15):
        """Wait until the Pay button becomes enabled (not disabled)."""
        WebDriverWait(self.browser, timeout).until(
            lambda d: d.find_element(
                *ProjectCreditsLocators.PAY_BTN
            ).get_attribute("disabled") is None,
            "Pay button did not become enabled within timeout",
        )
        self.logger.info("Pay button is now enabled")

    def click_pay_btn(self, timeout=10):
        """Click the Pay button (must be enabled first)."""
        btn = self.element_to_be_clickable(ProjectCreditsLocators.PAY_BTN, timeout=timeout)
        btn.click()
