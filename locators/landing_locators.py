# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0



from selenium.webdriver.common.by import By


class LandingLocators:
    BANNER_TITLE = (By.XPATH, "//h1[contains(text(),'Create your Virtual Lab')]")
    BIG_IMG1 = (By.XPATH, "(//div[contains(@class,'__vignette')])[1]")
    BIG_IMG2 = (By.XPATH, "(//div[contains(@class,'__vignette')])[2]")
    BIG_IMG3 = (By.XPATH, "(//div[contains(@class,'__vignette')])[3]")
    DIGITAL_BRAINS_VIDEO = (By.XPATH, "//div[contains(@class,'sanity-content-video-module') and contains(@class,'__sanityContentVideo')]")
    DIGITAL_BRAINS_PLAY_BTN = (By.CSS_SELECTOR, "button[aria-label='play video']")
    DIGITAL_BRAINS_PAUSE_BTN = (By.CSS_SELECTOR, "button[aria-label='pause video']")
    DIGITAL_BRAINS_VIDEO_CURRENT_STEP = (By.CSS_SELECTOR, "div[class*='__currentStep']")
    DIGITAL_BRAINS_VIDEO_STEP = (By.XPATH, "//button[contains(@class,'__step')]")
    DIGITAL_BRAINS_SCALES = (By.XPATH, "//h1[normalize-space()='Digital brain models at different scales']")
    FOOTER_OBI_LOGO = (By.XPATH, "//div[contains(@class,'footer-panel-module') and contains(@class,'__title')]//h2")
    FOOTER_OBI_COPYRIGHT = (By.XPATH, "//div[contains(@class,'footer-panel-module') and contains(@class,'__copyright')]")
    FOOTER_LINK_TITLES = (By.XPATH, "//div[contains(@class,'footer-panel-module') and contains(@class,'__links')]//a")
    FOOTER_SUBSCRIBE_BLOCK = (By.XPATH, "//div[contains(@class,'footer-panel-module') and contains(@class,'__subscribe')]")
    FOOTER_SOCIAL_MEDIA_LINKS = (By.XPATH, "//div[contains(@class,'social-media-links-module') and contains(@class,'__socialMediaLinks')]//a[@href]")
    GOTO_LAB = (By.XPATH, "//a[@href='/app/virtual-lab/sync']")
    HERO_BACKGROUND_IMG = (By.CSS_SELECTOR, "div[class*='__background']")
    HERO_BACKGROUND_VIDEO = (By.CSS_SELECTOR, "video[class*='__show']")
    LOGIN_BUTTON = (By.XPATH, "//a[@href='/app/virtual-lab']")
    # --- Top-level dropdown menu buttons (the <button> elements) ---
    NAV_ABOUT_BUTTON = (
        By.XPATH,
        "//button[contains(@class,'menuButton')]"
        "[.//span[contains(@class,'menuButtonContent')][starts-with(normalize-space(),'About')]]",
    )
    NAV_PLATFORM_BUTTON = (
        By.XPATH,
        "//button[contains(@class,'menuButton')]"
        "[.//span[contains(@class,'menuButtonContent')][starts-with(normalize-space(),'The Platform')]]",
    )

    # --- Wrapper div that contains button + submenu (for scoping submenu items) ---
    NAV_ABOUT_DROPDOWN = (
        By.XPATH,
        "//div[contains(@class,'menuItemWithSubmenu')]"
        "[.//span[contains(@class,'menuButtonContent')][starts-with(normalize-space(),'About')]]",
    )
    NAV_PLATFORM_DROPDOWN = (
        By.XPATH,
        "//div[contains(@class,'menuItemWithSubmenu')]"
        "[.//span[contains(@class,'menuButtonContent')][starts-with(normalize-space(),'The Platform')]]",
    )

    # --- About submenu items (scoped inside the About dropdown wrapper) ---
    NAV_ABOUT_OBI = (By.XPATH,
        "//div[contains(@class,'menuItemWithSubmenu')]"
        "[.//span[starts-with(normalize-space(),'About')]]"
        "//a[contains(@class,'submenuItem')][@href='/about']")
    NAV_OUR_STORY = (By.XPATH,
        "//div[contains(@class,'menuItemWithSubmenu')]"
        "[.//span[starts-with(normalize-space(),'About')]]"
        "//a[contains(@class,'submenuItem')][@href='/the-real-digital-brain-story']")
    NAV_MISSION = (By.XPATH,
        "//div[contains(@class,'menuItemWithSubmenu')]"
        "[.//span[starts-with(normalize-space(),'About')]]"
        "//a[contains(@class,'submenuItem')][@href='/mission']")
    NAV_TEAM = (By.XPATH,
        "//div[contains(@class,'menuItemWithSubmenu')]"
        "[.//span[starts-with(normalize-space(),'About')]]"
        "//a[contains(@class,'submenuItem')][@href='/team']")

    # --- The Platform submenu items (scoped inside the Platform dropdown wrapper) ---
    NAV_FEATURES = (By.XPATH,
        "//div[contains(@class,'menuItemWithSubmenu')]"
        "[.//span[starts-with(normalize-space(),'The Platform')]]"
        "//a[contains(@class,'submenuItem')][@href='/features']")
    NAV_SHOWCASES = (By.XPATH,
        "//div[contains(@class,'menuItemWithSubmenu')]"
        "[.//span[starts-with(normalize-space(),'The Platform')]]"
        "//a[contains(@class,'submenuItem')][@href='/showcases']")
    NAV_PRICING = (By.XPATH,
        "//div[contains(@class,'menuItemWithSubmenu')]"
        "[.//span[starts-with(normalize-space(),'The Platform')]]"
        "//a[contains(@class,'submenuItem')][@href='/pricing']")

    # --- Direct top-level nav links ---
    NAV_NEWS = (By.XPATH, "//div[contains(@class,'items')]//a[contains(@class,'menuLink') and @href='/news']")
    NAV_CONTACT = (By.XPATH, "//div[contains(@class,'items')]//a[contains(@class,'menuLink') and @href='/contact']")
    OBI_LOGO = (By.XPATH, "(//h2[contains(text(),'Open Brain Institute')])[1]")
    PARA_TEXT = (By.XPATH, "//div[contains(@class, 'text-module') and contains(@class, '__text')] | //div[contains(@class, 'Text-module') and contains(@class, '__text')]")
    P_TEXT1 = (By.XPATH, "(//div[contains(@class,'sanity-content-preview-module') and contains(@class,'__text')])[1]")
    P_TEXT2 = (By.XPATH, "(//div[contains(@class,'sanity-content-preview-module') and contains(@class,'__text')])[2]")
    P_TEXT3 = (By.XPATH, "(//div[contains(@class,'sanity-content-preview-module') and contains(@class,'__text')])[3]")
    P_TEXT4 = (By.XPATH, "(//div[contains(@class,'sanity-content-preview-module') and contains(@class,'__text')])[4]")
    P_TEXT5 = (By.XPATH, "//div[contains(@class,'text-module') and contains(@class,'__text')]/p[contains(text(), 'Digital brains are advanced')]")
    SECTION_BTN1 = (By.XPATH, "(//a[contains(@class,'sanity-content-preview-module') and contains(@class,'__button')])[1]")
    SECTION_BTN2 = (By.XPATH, "(//a[contains(@class,'sanity-content-preview-module') and contains(@class,'__button')])[2]")
    SECTION_BTN3 = (By.XPATH, "(//a[contains(@class,'sanity-content-preview-module') and contains(@class,'__button')])[3]")
    SECTION_BTN4 = (By.XPATH, "(//a[contains(@class,'sanity-content-preview-module') and contains(@class,'__button')])[4]")
    SECTION_BTN5 = (By.XPATH, "(//a[contains(@class,'sanity-content-preview-module') and contains(@class,'__button')])[5]")
    HORIZONTAL_CARDS_SECTION1 = (By.XPATH, "(//div[starts-with(@class,'swipeable-cards-list')])[1]")
    HORIZONTAL_CARDS_SECTION2 = (By.XPATH, "(//div[starts-with(@class,'swipeable-cards-list')])[2]")
    HORIZONTAL_CARDS_SECTION3 = (By.XPATH, "(//div[starts-with(@class,'swipeable-cards-list')])[3]")
    NEWS_CARD1 = (By.XPATH, "(//button[starts-with(@class,'NewsCard')])[1]")
    NEWS_CARD2 = (By.XPATH, "(//button[starts-with(@class,'NewsCard')])[2]")
    NEWS_CARD3 = (By.XPATH, "(//button[starts-with(@class,'NewsCard')])[3]")
    NEWS_CARD4 = (By.XPATH, "(//button[starts-with(@class,'NewsCard')])[4]")
    NEWS_CARD_CONTENT1 = (By.XPATH, "(//div[starts-with(@class,'NewsCard_content')])[1]")
    NEWS_CARD_CONTENT2 = (By.XPATH, "(//div[starts-with(@class,'NewsCard_content')])[2]")
    NEWS_CARD_CONTENT3 = (By.XPATH, "(//div[starts-with(@class,'NewsCard_content')])[3]")
    NEWS_CARD_CONTENT4 = (By.XPATH, "(//div[starts-with(@class,'NewsCard_content')])[4]")
    NEWS_CARD_PIC1 = (By.XPATH, "(//div[starts-with(@class,'NewsCard_picture')])[1]")
    NEWS_CARD_PIC2 = (By.XPATH, "(//div[starts-with(@class,'NewsCard_picture')])[2]")
    NEWS_CARD_PIC3 = (By.XPATH, "(//div[starts-with(@class,'NewsCard_picture')])[3]")
    NEWS_CARD_PIC4 = (By.XPATH, "(//div[starts-with(@class,'NewsCard_picture')])[4]")
    TITLE_ACCELERATE = (By.XPATH, "//h1[normalize-space()='Accelerating neuroscience research']")
    TITLE_DIG_BRAIN = (By.XPATH, "//h1[normalize-space()='What are digital brains?']")
    TITLE_WHO = (By.XPATH, "//h1[normalize-space()='Who is behind the Open Brain Institute']")
    TITLE_NEWS = (By.XPATH, "//h1[normalize-space()='News and events']")
    TOP_MENU = (By.CSS_SELECTOR, "(div[id='LandingPage/menu'])")
    TOP_ABOUT_DROPDOWN = NAV_ABOUT_DROPDOWN
    TOP_ABOUT_OBI = NAV_ABOUT_OBI
    TOP_OUR_STORY = NAV_OUR_STORY
    TOP_MISSION = NAV_MISSION
    TOP_TEAM = NAV_TEAM
    TOP_PLATFORM_DROPDOWN = NAV_PLATFORM_DROPDOWN
    TOP_FEATURES = NAV_FEATURES
    TOP_SHOWCASES = NAV_SHOWCASES
    TOP_PRICING = NAV_PRICING
    TOP_NEWS = NAV_NEWS
    TOP_CONTACT = NAV_CONTACT
    TOP_MENU_LOGO = (By.XPATH, "//a[starts-with(@class,'Menu_logo')]")
    VIDEO_TITLE1 = (By.XPATH, "//h3[normalize-space()='01. Fill with Neurons']")
    VIDEO_CONTAINER = (By.XPATH, "(//div[contains(@class,'sanity-content-video-module')])[1]")
    VIDEO_POINTER = (By.CSS_SELECTOR, "div[class*='__pointer']")


