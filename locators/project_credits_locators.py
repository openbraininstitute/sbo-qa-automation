# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class ProjectCreditsLocators:
    # Credit pill button in top nav
    CREDITS_PILL = (By.CSS_SELECTOR, "#workspace-project-credits")

    # Credits panel (main container)
    CREDITS_PANEL = (By.CSS_SELECTOR, "[data-testid='project-credits']")

    # Credit balance cards
    VLAB_CREDITS_LABEL = (By.XPATH, "//div[normalize-space()='Virtual lab credits']")
    VLAB_CREDITS_VALUE = (
        By.XPATH,
        "//div[normalize-space()='Virtual lab credits']/following-sibling::div[contains(@class,'font-bold')]",
    )
    PROJECT_CREDITS_LABEL = (By.XPATH, "//div[normalize-space()='Project credits']")
    PROJECT_CREDITS_VALUE = (
        By.XPATH,
        "//div[normalize-space()='Project credits']/following-sibling::div[contains(@class,'font-bold')]",
    )

    # Action buttons
    PRICING_BTN = (By.XPATH, "//button[.//span[contains(text(),'Pricing')]]")
    BUY_CREDITS_BTN = (By.XPATH, "//button[contains(text(),'Buy credits')]")
    TRANSFER_CREDITS_BTN = (By.XPATH, "//button[contains(text(),'Transfer credits')]")

    # History section
    HISTORY_TITLE = (By.XPATH, "//h3[normalize-space()='History']")
    HISTORY_TABLE = (By.CSS_SELECTOR, ".ant-table")
    HISTORY_TABLE_HEADERS = (By.CSS_SELECTOR, ".ant-table-thead th.ant-table-cell")
    HISTORY_TABLE_ROWS = (
        By.CSS_SELECTOR,
        ".ant-table-tbody tr.ant-table-row",
    )
    HISTORY_PAGINATION = (By.CSS_SELECTOR, ".ant-pagination")
    HISTORY_PAGINATION_NEXT = (By.CSS_SELECTOR, ".ant-pagination-next button")

    # Transfer credits modal
    TRANSFER_CREDITS_MODAL = (By.CSS_SELECTOR, "#modal-dialog")
    TRANSFER_CREDITS_FROM_VALUE = (
        By.XPATH,
        # "//div[@data-testid='transfer-credits__from']//div[contains(@class,'font-bold')]",
        # "//span[contains(text(), 'From')]/following-sibling::div[@data-slot='badge' and text()='Virtual Lab']"
        "(//div[contains(@class,'mb-5 ml-auto flex items-center gap-2 rounded-full border border-gray-100 bg-gray-100 px-3 py-1 text-sm text-primary-9')]/child::span)[1]"
    )
    TRANSFER_CREDITS_TO_VALUE = (
        By.XPATH,
        # "//div[@data-testid='transfer-credits__to']//div[contains(@class,'font-bold')]",
        "//span[contains(text(), 'To')]/following-sibling::div[@data-slot='badge' and text()='Project']"
    )
    TRANSFER_CREDITS_AMOUNT_INPUT = (By.CSS_SELECTOR, "input#amount")
    TRANSFER_CREDITS_SUBMIT_BTN = (
        By.XPATH,
        "//button[@type='button']//span[contains(text(),'Transfer credits')]/ancestor::button[contains(@class,'bg-primary-9')]",
    )
    TRANSFER_CREDITS_CLOSE_BTN = (
        By.XPATH,
        "//button[.//span[@aria-label='close']]",
    )

    # Buy credits modal
    MODAL_DIALOG = (By.CSS_SELECTOR, "#modal-dialog")
    MODAL_TITLE = (By.CSS_SELECTOR, "#modal-title h2")
    MODAL_SUBTITLE = (
        By.CSS_SELECTOR,
        "#modal-title p",
    )
    MODAL_CLOSE_BTN = (
        By.CSS_SELECTOR,
        "#modal-header button .anticon-close",
    )

    # Payment mode selection (first screen of Buy credits modal)
    PAYMENT_MODE_SELECTION = (By.CSS_SELECTOR, "[data-testid='payment-mode-selection']")
    PURCHASE_CREDITS_CARD = (
        By.XPATH,
        "//div[@data-testid='payment-mode-selection']//button[.//h2[text()='Purchase Credits']]",
    )
    PROMO_CODE_CARD = (
        By.XPATH,
        "//div[@data-testid='payment-mode-selection']//button[.//h2[text()='Promo Code']]",
    )

    # Stripe payment flow (after clicking Purchase Credits)
    STRIPE_PAYMENT_FLOW = (By.CSS_SELECTOR, "[data-testid='stripe-payment-flow']")
    STRIPE_BACK_BTN = (
        By.XPATH,
        "//section[@data-testid='stripe-payment-flow']//button[.//span[text()='Select option']]",
    )
    CREDITS_INPUT = (By.CSS_SELECTOR, "input#credits")
    ORDER_DETAILS_SUBTOTAL = (
        By.XPATH,
        "//div[contains(@class,'rounded-2xl')]//span[text()='Subtotal excl. VAT']/following-sibling::span",
    )
    ORDER_DETAILS_VAT = (
        By.XPATH,
        "//div[contains(@class,'rounded-2xl')]//span[text()='VAT']/following-sibling::span",
    )
    ORDER_DETAILS_TOTAL = (
        By.XPATH,
        "//div[contains(@class,'rounded-2xl')]//span[text()='Total due today']/following-sibling::span",
    )
    SAVE_ADDRESS_CHECKBOX = (By.CSS_SELECTOR, "#save-address-checkbox")
    STRIPE_ADDRESS_IFRAME = (
        By.CSS_SELECTOR,
        "iframe[title='Secure address input frame']",
    )
    STRIPE_PAYMENT_IFRAME = (
        By.CSS_SELECTOR,
        "iframe[title='Secure payment input frame']",
    )
    CANCEL_BTN = (
        By.XPATH,
        "//section[@data-testid='stripe-payment-flow']//button[.//span[text()='Cancel']]",
    )
    PAY_BTN = (
        By.XPATH,
        "//section[@data-testid='stripe-payment-flow']//button[.//span[contains(text(),'Pay')]]",
    )
