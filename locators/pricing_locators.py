# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0


from selenium.webdriver.common.by import By


class PricingLocators:
    DISCOVER_PLANS = (By.XPATH, "//h1[normalize-space()='Discover our plans']")
    PRICING_TITLE = (By.XPATH, "//h1[normalize-space()='Pricing']")
    PRICING_SUBTEXT = (By.CSS_SELECTOR, ".Hero-module__E0OG9W__content")
    OBI_HOMEPAGE_MAIN_NAV = (By.CSS_SELECTOR, "div[id='LandingPage/menu']")
    OBI_HOMEPAGE_LOGO_BTN = (By.CSS_SELECTOR, ".Menu-module__CnaVha__logo")
    OBI_MENU = (By.CSS_SELECTOR, ".Menu-module__CnaVha__items")
    VLAB_LOGIN_BTN = (By.CSS_SELECTOR, ".Menu-module__CnaVha__loginButton")
    HERO_IMG = (By.CSS_SELECTOR, "img[alt='Hero image']")
    HERO_VIDEO = (By.CSS_SELECTOR, ".Hero-module__E0OG9W__show")
    TEMP_GOTO_VLAB_BTN = (By.CSS_SELECTOR, ".TemporaryGoToLabButton-module___26Z8G__image.ProgressiveImage-module__p7HpFa__progressiveImage")
    PRICE_LIST_CONTAINER = (By.CSS_SELECTOR, ".large-screen-module__desitq__priceList")
    PRICE_LIST_PLANS = (By.XPATH, "//div[@class='PlanHeader-module__b-edzW__planHeader']")
