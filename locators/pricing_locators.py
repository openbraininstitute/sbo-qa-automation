# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0


from selenium.webdriver.common.by import By


class PricingLocators:
    # Top nav / header
    OBI_HOMEPAGE_MAIN_NAV = (By.CSS_SELECTOR, "div[id='LandingPage/menu']")
    OBI_HOMEPAGE_LOGO_BTN = (By.CSS_SELECTOR, ".Menu-module__CnaVha__logo")
    OBI_MENU = (By.CSS_SELECTOR, ".Menu-module__CnaVha__items")
    VLAB_LOGIN_BTN = (By.CSS_SELECTOR, ".Menu-module__CnaVha__loginButton")

    # Hero section
    PRICING_TITLE = (By.XPATH, "//h1[normalize-space()='Pricing']")
    HERO_IMG = (By.CSS_SELECTOR, "img[alt='Hero image']")
    HERO_VIDEO = (By.CSS_SELECTOR, ".Hero-module__E0OG9W__show")
    PRICING_SUBTEXT = (By.CSS_SELECTOR, ".Hero-module__E0OG9W__content")

    # "Discover our plans" button (below hero)
    DISCOVER_PLANS = (By.CSS_SELECTOR, "button[aria-label='Discover our plans']")

    # Plan cards grid container (4-column grid with Free, Pro, Enterprise, Education)
    # The xl:grid container is hidden on smaller viewports; use presence not visibility
    PLAN_CARDS_CONTAINER = (By.XPATH, "//div[contains(@class, 'grid-cols-4')]")

    # Individual plan cards by title text
    PLAN_CARD_FREE = (By.XPATH, "//div[contains(@class, 'font-serif') and text()='Free']")
    PLAN_CARD_PRO = (By.XPATH, "//div[contains(@class, 'font-serif') and text()='Pro']")
    PLAN_CARD_ENTERPRISE = (By.XPATH, "//div[contains(@class, 'font-serif') and text()='Enterprise']")
    PLAN_CARD_EDUCATION = (By.XPATH, "//div[contains(@class, 'font-serif') and text()='Education']")

    # All plan card headers (rounded-xl border cards)
    PLAN_CARDS = (By.XPATH, "//div[contains(@class, 'grid-cols-4')]/div[contains(@class, 'rounded-xl')]")

    # Contact Us links (Enterprise and Education cards have mailto links)
    CONTACT_US_ENTERPRISE = (By.XPATH, "//div[contains(@class, 'font-serif') and text()='Enterprise']/ancestor::div[contains(@class, 'rounded-xl')]//a[contains(text(), 'Contact Us')]")
    CONTACT_US_EDUCATION = (By.XPATH, "//div[contains(@class, 'font-serif') and text()='Education']/ancestor::div[contains(@class, 'rounded-xl')]//a[contains(text(), 'Contact Us')]")
    CONTACT_US_ANY = (By.XPATH, "//a[contains(text(), 'Contact Us')]")

    # Pro plan price
    PRO_PRICE = (By.XPATH, "//span[contains(@class, 'font-bold') and contains(text(), 'CHF')]")

    # Pro plan subscription toggle
    PRO_SUBSCRIPTION_TOGGLE = (By.XPATH, "//button[@aria-label='Switch to year subscription']")

    # Footer
    FOOTER = (By.CSS_SELECTOR, ".FooterPanel-module__YUozGG__footerPanel")

    # Temporary go-to-vlab button (if still present)
    TEMP_GOTO_VLAB_BTN = (By.CSS_SELECTOR, ".TemporaryGoToLabButton-module___26Z8G__image.ProgressiveImage-module__p7HpFa__progressiveImage")
