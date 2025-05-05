# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0



from selenium.webdriver.common.by import By


class MissionLocators:
    BTN_DOWNLOAD_MISSION = (By.XPATH, "//button[starts-with(@class,'MissionStatement')]")
    MISSION_PAGE_TITLE = (By.XPATH, "//div[starts-with(@class,'Hero_text')]//h1[text()='Mission']")
    MISSION_MAIN_TEXT = (By.XPATH, "//*[starts-with(@class,'Hero_content') and contains(text(), 'The Open Brain Institute')]")
    MAIN_TITLES = (By.XPATH, "//h1[starts-with(@class,'styles_blockSmall')]")
    MAIN_PAGE_PARAGRAPH = (By.XPATH, "(//div[starts-with(@class, 'Text_text')])[1]")
    MINOR_PAGE_PARAGRAPH = (By.XPATH, "(//div[starts-with(@class, 'Text_text')])[2]")
    MODELS_CARDS = (By.XPATH, "//div[starts-with(@class,'swipeable-cards-list_scroll')]")
    PLATFORM_SECTIONS = (By.XPATH, "//ul[starts-with(@class,'SanityContentItems_sanityContentItems')]")
    PDF_NEW_TAB = (By.LINK_TEXT, "https://cdn.sanity.io/files/fgi7eh1v/staging/6c892e090449e62ffaa03aaabb47e582fb8dacee.pdf")
    P_SECTION_TITLES = (By.XPATH, "//ul[starts-with(@class,'SanityContentItems_sanityContentItems')]//li//h3")
    P_SECTION_TEXTS = (By.XPATH, "//ul[starts-with(@class,'SanityContentItems_sanityContentItems')]//li//div[last()]")
    P_SECTION_IMAGES = (By.XPATH, "//ul[starts-with(@class,'SanityContentItems_sanityContentItems')]//li//img")
    SUBSCRIBE_NEWSLETTER = (By.XPATH, "//h2[text()='Subscribe to our newsletter']")

    VLAB_CARDS_BTN = (By.XPATH, "//button[starts-with(@class,'card_card')]")
    VIDEO1 = (By.CSS_SELECTOR, "video[src='https://player.vimeo.com/progressive_redirect/playback/1066685265/rendition/1080p/file.mp4?loc=external&log_user=0&signature=df8503b3df7f25c227bbfd5a1ef3981700b55b687b7095314cb47724453837c1&user_id=43466136']")
    VIDEO2 = (By.CSS_SELECTOR, "video[src='https://player.vimeo.com/progressive_redirect/playback/1066685284"
                               "/rendition/1080p/file.mp4?loc=external&log_user=0&signature=690e209823a3fa4408da7348ca899d73192896161dd51478a755e55d7852823d&user_id=43466136']")
    VIDEO3 = (By.CSS_SELECTOR, "video[src='https://player.vimeo.com/progressive_redirect/playback/1066687908/rendition/1080p/file.mp4?loc=external&log_user=0&signature=a413b42d60a559be5b4d10d3c63669d94fa226682b94e4216b3634ec82decb0b&user_id=43466136']")