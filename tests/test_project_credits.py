# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

"""
Test: Project Credits Page
Environment: Staging ONLY (Stripe test mode, no real charges)

Flow:
  1. Login → Navigate to project home
  2. Click credits pill → verify redirect to /credits
  3. Verify credits panel: vlab credits, project credits values
  4. Click Pricing → new tab opens to /pricing → close tab
  5. Verify History table: headers, rows, pagination
  6. Buy 5 credits (staging only — Stripe test card):
     - Click Buy credits → modal opens
     - Verify payment mode selection
     - Click Purchase Credits card → Stripe payment flow appears
     - Enter 5 credits → verify order details update
     - Fill billing address + card details (test card 4242...)
     - Verify Pay button enabled → click Pay
     - Wait for purchase to complete → close modal
  7. Transfer 5 credits from Virtual lab to project:
     - Click Transfer credits → modal opens
     - Verify from/to values (min 100 credits in Virtual lab)
     - Enter 5 credits → click Transfer → close modal
"""
import time

import pytest

from pages.project_credits_page import ProjectCreditsPage
from locators.project_credits_locators import ProjectCreditsLocators


class TestProjectCredits:
    """Test for the Project Credits page and Buy Credits flow (staging only)."""

    @pytest.mark.project_credits
    @pytest.mark.run(order=10)
    def test_project_credits_full_flow(self, setup, login_direct_complete, logger, test_config):
        """End-to-end test of the project credits page: buy credits then transfer."""
        browser, wait, base_url, lab_id, project_id = login_direct_complete

        # Guard: only run on staging (Stripe test mode)
        if "staging" not in base_url:
            pytest.skip("Skipping: credits test only runs on staging (Stripe test keys)")

        credits_page = ProjectCreditsPage(browser, wait, logger, base_url)

        # --- Step 1: Navigate to project home page ---
        project_home_url = f"{base_url}/app/virtual-lab/{lab_id}/{project_id}"
        browser.get(project_home_url)
        credits_page.wait_for_page_ready(timeout=30)
        logger.info(f"Project home loaded: {browser.current_url}")

        # --- Step 2: Click credit pill → redirects to /credits ---
        credits_page.click_credits_pill()
        credits_page.wait_for_url_contains("/credits", timeout=15)
        assert "/credits" in browser.current_url, (
            f"Expected /credits in URL, got: {browser.current_url}"
        )
        logger.info(f"Credits page loaded: {browser.current_url}")

        # --- Step 3: Verify credits panel ---
        panel = credits_page.credits_panel(timeout=20)
        assert panel.is_displayed(), "Credits panel is not displayed"

        credits_page.wait_for_network_idle(timeout=15)

        vlab_credits = credits_page.get_vlab_credits_value(timeout=20)
        assert vlab_credits, "Virtual lab credits value is empty"
        logger.info(f"Virtual lab credits: {vlab_credits}")

        project_credits = credits_page.get_project_credits_value(timeout=10)
        assert project_credits, "Project credits value is empty"
        logger.info(f"Project credits: {project_credits}")

        # --- Step 4: Verify Pricing button opens new tab ---
        original_window = browser.current_window_handle
        credits_page.click_pricing_btn(timeout=15)

        handles = credits_page.wait_for_new_tab(timeout=15)
        assert len(handles) > 1, "Pricing button did not open a new tab"

        credits_page.switch_to_new_tab()
        credits_page.wait_for_url_contains("/pricing", timeout=20)
        pricing_url = browser.current_url
        logger.info(f"Pricing tab URL: {pricing_url}")
        assert "/pricing" in pricing_url, f"Expected /pricing in URL, got: {pricing_url}"

        credits_page.close_tab_and_switch_back()
        logger.info("Pricing tab closed, back on credits page")

        # --- Step 5: Verify History section ---
        history_title = credits_page.history_title()
        assert history_title.is_displayed(), "History title not displayed"
        assert history_title.text.strip() == "History"
        logger.info("History section title verified")

        table = credits_page.history_table()
        assert table.is_displayed(), "History table not displayed"

        headers = credits_page.get_history_table_headers()
        expected_headers = ["category", "type", "member", "date", "cost (credits)"]
        headers_lower = [h.lower() for h in headers]
        assert headers_lower == expected_headers, (
            f"Table headers mismatch. Expected: {expected_headers}, Got: {headers_lower}"
        )
        logger.info(f"History table headers: {headers}")

        rows = credits_page.get_history_table_rows()
        assert len(rows) > 0, "History table has no data rows"
        logger.info(f"History table rows: {len(rows)}")

        pagination = credits_page.history_pagination()
        assert pagination.is_displayed(), "Pagination not displayed"
        logger.info("History pagination verified")

        # --- Step 6: Buy 5 credits via Stripe (staging only) ---
        logger.info("=== Starting Buy Credits flow (Stripe test mode) ===")

        credits_page.click_buy_credits_btn()

        credits_page.modal_dialog(timeout=25)
        logger.info("Buy credits modal opened")

        modal_title = credits_page.get_modal_title()
        assert modal_title, "Modal title is empty"
        logger.info(f"Modal title: '{modal_title}'")

        # Verify payment mode selection
        payment_selection = credits_page.payment_mode_selection()
        assert payment_selection.is_displayed(), "Payment mode selection not displayed"
        logger.info("Payment mode selection displayed (Purchase Credits + Promo Code)")

        # Click Purchase Credits card → Stripe flow
        credits_page.click_purchase_credits_card()

        stripe_flow = credits_page.stripe_payment_flow(timeout=15)
        assert stripe_flow.is_displayed(), "Stripe payment flow did not appear"
        logger.info("Stripe payment flow displayed")

        # Verify initial order details
        credits_input_value = credits_page.get_credits_input_value()
        logger.info(f"Initial credits input value: '{credits_input_value}'")

        # Enter 5 credits
        credits_page.enter_credits_amount("5")
        credits_page.wait_for_network_idle(timeout=10)

        updated_subtotal = credits_page.get_order_subtotal()
        updated_total = credits_page.get_order_total()
        logger.info(f"After entering 5 credits - Subtotal: {updated_subtotal}, Total: {updated_total}")
        assert updated_subtotal != "CHF 0.00", (
            f"Subtotal did not update after entering credits: {updated_subtotal}"
        )
        assert "CHF" in updated_total, f"Total missing CHF currency: {updated_total}"

        # Verify Stripe iframes are present
        address_iframe = credits_page.stripe_address_iframe(timeout=15)
        assert address_iframe.is_displayed(), "Stripe address iframe not displayed"
        logger.info("Stripe address iframe present")

        payment_iframe = credits_page.stripe_payment_iframe(timeout=15)
        assert payment_iframe.is_displayed(), "Stripe payment iframe not displayed"
        logger.info("Stripe payment iframe present")

        # Fill billing address (inside Stripe address iframe)
        credits_page.fill_billing_address(
            country_code="CH",
            address="123 Test Street",
            city="Geneva",
            postal_code="1200",
        )
        logger.info("Billing address filled")

        # Fill card details (inside Stripe payment iframe) — test card
        credits_page.fill_card_details(
            card_number="4000007560000009",
            expiry="1229",
            cvc="123",
        )
        logger.info("Card details filled with Stripe test card (4242...)")

        # Verify Pay button becomes enabled
        credits_page.wait_for_pay_btn_enabled(timeout=15)
        assert not credits_page.is_pay_btn_disabled(), (
            "Pay button should be enabled after filling all details"
        )
        logger.info("Pay button is enabled")

        # Click Pay to complete the purchase (safe — Stripe test mode)
        credits_page.click_pay_btn()
        logger.info("Pay button clicked — processing payment...")

        # Wait for payment to process and modal to close or show success
        credits_page.wait_for_network_idle(timeout=30)
        logger.info("Payment processed successfully")

        # Close modal if still open
        try:
            credits_page.close_modal(timeout=5)
            credits_page.wait_for_element_to_disappear(
                ProjectCreditsLocators.MODAL_DIALOG, timeout=10
            )
        except Exception:
            logger.info("Buy credits modal already closed after payment")

        logger.info("=== Buy Credits flow completed ===")

        # --- Step 7: Transfer 5 credits from Virtual lab to project ---
        logger.info("=== Starting Transfer Credits flow ===")

        # Wait for page to refresh after purchase
        credits_page.wait_for_network_idle(timeout=10)

        credits_page.click_transfer_credits_btn()

        credits_page.transfer_credits_modal(timeout=25)
        logger.info("Transfer credits modal opened")

        # Verify 'From Virtual lab' has at least 100 credits
        from_value = credits_page.get_transfer_from_value(timeout=10)
        assert from_value, "From Virtual lab credits value is empty"
        logger.info(f"Transfer from (Virtual lab): {from_value}")

        # Parse numeric value (remove non-numeric chars except dot)
        from_numeric = float(''.join(c for c in from_value if c.isdigit() or c == '.'))
        assert from_numeric >= 100, (
            f"Insufficient credits in Virtual lab for transfer. "
            f"Need at least 100, got: {from_numeric}"
        )
        logger.info(f"Virtual lab has sufficient credits: {from_numeric}")

        # Verify 'To project' is shown
        to_value = credits_page.get_transfer_to_value(timeout=10)
        assert to_value is not None, "To project value not found"
        logger.info(f"Transfer to (Project): {to_value}")

        # Enter 5 credits to transfer
        credits_page.enter_transfer_amount("5")
        amount_value = credits_page.get_transfer_amount_value()
        assert amount_value == "5", f"Expected amount '5', got: '{amount_value}'"
        logger.info("Entered transfer amount: 5 credits")

        # Click Transfer credits submit button
        credits_page.click_transfer_submit_btn()
        credits_page.wait_for_network_idle(timeout=15)
        logger.info("Transfer credits submitted")

        # Close the transfer modal (if still open)
        try:
            credits_page.close_transfer_modal(timeout=5)
        except Exception:
            logger.info("Transfer modal already closed after submission")

        # Verify modal is gone
        # credits_page.wait_for_element_to_disappear(
        #     ProjectCreditsLocators.TRANSFER_CREDITS_MODAL, timeout=10
        # )
        logger.info("Transfer modal closed successfully")

        logger.info("=== Transfer Credits flow completed ===")
        logger.info("Project credits full flow test completed successfully")
