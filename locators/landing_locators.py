# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0



from selenium.webdriver.common.by import By


class LandingLocators:
    BANNER_TITLE = (By.XPATH, "//h1[contains(text(),'Create your Virtual Lab')]")
    BIG_IMG1 = (By.XPATH, "(//div[starts-with(@class,'SanityContentPreview-module__hsTF2G__vignette')])[1]")
    BIG_IMG2 = (By.XPATH, "(//div[starts-with(@class,'SanityContentPreview-module__hsTF2G__vignette')])[2]")
    BIG_IMG3 = (By.XPATH, "(//div[starts-with(@class,'SanityContentPreview-module__hsTF2G__vignette')])[3]")
    DIGITAL_BRAINS_VIDEO = (By.XPATH, "//div[@class='sanity-content-video-module__8kGZUG__sanityContentVideo "
                                  "styles-module__5IYxQa__blockMedium']")
    DIGITAL_BRAINS_PLAY_BTN = (By.CSS_SELECTOR, "button[aria-label='play video']")
    DIGITAL_BRAINS_PAUSE_BTN = (By.CSS_SELECTOR, "button[aria-label='pause video']")
    DIGITAL_BRAINS_VIDEO_CURRENT_STEP = (By.CSS_SELECTOR, ".sanity-content-video-module__8kGZUG__currentStep")
    DIGITAL_BRAINS_VIDEO_STEP = (By.XPATH, "//button[@class='sanity-content-video-module__8kGZUG__step']")
    DIGITAL_BRAINS_SCALES = (By.XPATH, "//h1[normalize-space()='Digital brain models at different scales']")
    FOOTER_OBI_LOGO = (By.CSS_SELECTOR, "div[class='FooterPanel-module__YUozGG__title'] h2")
    FOOTER_OBI_COPYRIGHT = (By.CSS_SELECTOR, ".FooterPanel-module__YUozGG__copyright")
    FOOTER_LINK_TITLES = (By.CSS_SELECTOR,"div.FooterPanel-module__YUozGG__links a")
    FOOTER_SUBSCRIBE_BLOCK = (By.XPATH, "//div[@class='FooterPanel-module__YUozGG__subscribe "
                                        "NewsLetterSubscription-module__C5psVq__newsLetterSubscription']")
    FOOTER_SOCIAL_MEDIA_LINKS = (By.XPATH, "//div[contains(@class,'socialMediaLinks')]//a[@href]")
    GOTO_LAB = (By.XPATH, "//a[@href='/app/virtual-lab/sync']")
    HERO_BACKGROUND_IMG = (By.CSS_SELECTOR, ".Hero-module__E0OG9W__background")
    HERO_BACKGROUND_VIDEO = (By.CSS_SELECTOR, ".Hero-module__E0OG9W__show")
    LOGIN_BUTTON = (By.XPATH, "//a[@href='/app/virtual-lab']")
    # --- Top-level dropdown menu buttons (the <button> elements) ---
    NAV_ABOUT_BUTTON = (
        By.XPATH,
        "//button[@class='Menu-module__CnaVha__menuButton']"
        "[.//span[@class='Menu-module__CnaVha__menuButtonContent'][starts-with(normalize-space(),'About')]]",
    )
    NAV_PLATFORM_BUTTON = (
        By.XPATH,
        "//button[@class='Menu-module__CnaVha__menuButton']"
        "[.//span[@class='Menu-module__CnaVha__menuButtonContent'][starts-with(normalize-space(),'The Platform')]]",
    )

    # --- Wrapper div that contains button + submenu (for scoping submenu items) ---
    NAV_ABOUT_DROPDOWN = (
        By.XPATH,
        "//div[contains(@class,'Menu-module__CnaVha__menuItemWithSubmenu')]"
        "[.//span[@class='Menu-module__CnaVha__menuButtonContent'][starts-with(normalize-space(),'About')]]",
    )
    NAV_PLATFORM_DROPDOWN = (
        By.XPATH,
        "//div[contains(@class,'Menu-module__CnaVha__menuItemWithSubmenu')]"
        "[.//span[@class='Menu-module__CnaVha__menuButtonContent'][starts-with(normalize-space(),'The Platform')]]",
    )

    # --- About submenu items (scoped inside the About dropdown wrapper) ---
    NAV_ABOUT_OBI = (By.XPATH,
        "//div[contains(@class,'Menu-module__CnaVha__menuItemWithSubmenu')]"
        "[.//span[starts-with(normalize-space(),'About')]]"
        "//a[@class='Menu-module__CnaVha__submenuItem'][@href='/about']")
    NAV_OUR_STORY = (By.XPATH,
        "//div[contains(@class,'Menu-module__CnaVha__menuItemWithSubmenu')]"
        "[.//span[starts-with(normalize-space(),'About')]]"
        "//a[@class='Menu-module__CnaVha__submenuItem'][@href='/the-real-digital-brain-story']")
    NAV_MISSION = (By.XPATH,
        "//div[contains(@class,'Menu-module__CnaVha__menuItemWithSubmenu')]"
        "[.//span[starts-with(normalize-space(),'About')]]"
        "//a[@class='Menu-module__CnaVha__submenuItem'][@href='/mission']")
    NAV_TEAM = (By.XPATH,
        "//div[contains(@class,'Menu-module__CnaVha__menuItemWithSubmenu')]"
        "[.//span[starts-with(normalize-space(),'About')]]"
        "//a[@class='Menu-module__CnaVha__submenuItem'][@href='/team']")

    # --- The Platform submenu items (scoped inside the Platform dropdown wrapper) ---
    NAV_FEATURES = (By.XPATH,
        "//div[contains(@class,'Menu-module__CnaVha__menuItemWithSubmenu')]"
        "[.//span[starts-with(normalize-space(),'The Platform')]]"
        "//a[@class='Menu-module__CnaVha__submenuItem'][@href='/features']")
    NAV_SHOWCASES = (By.XPATH,
        "//div[contains(@class,'Menu-module__CnaVha__menuItemWithSubmenu')]"
        "[.//span[starts-with(normalize-space(),'The Platform')]]"
        "//a[@class='Menu-module__CnaVha__submenuItem'][@href='/showcases']")
    NAV_PRICING = (By.XPATH,
        "//div[contains(@class,'Menu-module__CnaVha__menuItemWithSubmenu')]"
        "[.//span[starts-with(normalize-space(),'The Platform')]]"
        "//a[@class='Menu-module__CnaVha__submenuItem'][@href='/pricing']")

    # --- Direct top-level nav links ---
    NAV_NEWS = (By.XPATH, "//div[@class='Menu-module__CnaVha__items']//a[contains(@class,'Menu-module__CnaVha__menuLink') and @href='/news']")
    NAV_CONTACT = (By.XPATH, "//div[@class='Menu-module__CnaVha__items']//a[contains(@class,'Menu-module__CnaVha__menuLink') and @href='/contact']")
    OBI_LOGO = (By.XPATH, "(//h2[contains(text(),'Open Brain Institute')])[1]")
    PARA_TEXT = (By.XPATH, "//div[contains(@class, 'Text-module__KTJYiG__text')]")
    P_TEXT1 = (By.XPATH, "(//div[@class='SanityContentPreview-module__hsTF2G__text'])[1]")
    P_TEXT2 = (By.XPATH, "(//div[@class='SanityContentPreview-module__hsTF2G__text'])[2]")
    P_TEXT3 = (By.XPATH, "(//div[@class='SanityContentPreview-module__hsTF2G__text'])[3]")
    P_TEXT4 = (By.XPATH, "(//div[@class='SanityContentPreview-module__hsTF2G__text'])[4]")
    P_TEXT5 = (By.XPATH, "//div[@class='Text-module__KTJYiG__text']/p[contains(text(), 'Digital brains are advanced')]")
    SECTION_BTN1 = (By.XPATH, "(//button[starts-with(@class,'SanityContentPreview-module__hsTF2G__button')])[1]")
    SECTION_BTN2 = (By.XPATH, "(//button[starts-with(@class,'SanityContentPreview-module__hsTF2G__button')])[2]")
    SECTION_BTN3 = (By.XPATH, "(//button[starts-with(@class,'SanityContentPreview-module__hsTF2G__button')])[3]")
    SECTION_BTN4 = (By.XPATH, "(//button[starts-with(@class,'SanityContentPreview-module__hsTF2G__button')])[4]")
    SECTION_BTN5 = (By.XPATH, "(//button[starts-with(@class,'SanityContentPreview-module__hsTF2G__button')])[5]")
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
    VIDEO_CONTAINER = (By.XPATH, "(//div[starts-with(@class,'sanity-content-video-module')])[1]")
    VIDEO_POINTER = (By.CSS_SELECTOR, ".Video-module__ZeAqaq__pointer")


