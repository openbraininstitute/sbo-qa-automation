# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class HomePageLocators:
    LOGIN_BUTTON = (By.XPATH, "//a[contains(.,'Log in')]")
    ABOUT = (By.XPATH, "(//a[@href='/app/about'])[2]")
    A_LETTER = (By.XPATH, "//button[.='A']")
    BB_GITHUB_BTN = (By.XPATH, "(//a[@href='https://github.com/BlueBrain'])[2]")
    BBOP1 = (By.XPATH, "(//a[@href='/app'])[1]")
    BBOP2 = (By.XPATH, "(//a[@href='/app'])[2]")
    BBP1 = (By.CSS_SELECTOR, "a[href='https://www.epfl.ch/research/domains/bluebrain/']")
    BBP2 = (By.CSS_SELECTOR, "a[href='https://portal.bluebrain.epfl.ch/']")
    BIG_TITLE1 = (By.XPATH, "//h3[contains(text(),'Why Blue Brain Github')]")
    BIG_TITLE2 = (By.XPATH, "//h3[contains(text(),'We thank the 1,000+')]")
    CONTRIBUTOR = (By.XPATH, "//button[@type='button' and text()='A']")
    CONTRIBUTOR_TABLE = (By.XPATH, "//div[@class='relative mt-4 grid w-full grid-cols-1 gap-x-12 "
                                   "gap-y-8 px-6 md:grid-cols-3 md:gap-y-20 md:px-0 "
                                   "lg:grid-cols-4 2xl:grid-cols-5']")
    DOC1 = (By.CSS_SELECTOR, "a[href='https://bluebrainnexus.io/']")
    DOC2 = (By.CSS_SELECTOR, "a[href='https://channelpedia.epfl.ch/']")
    DOC3 = (By.CSS_SELECTOR, "a[href='a[href='https://bbp.epfl.ch/nmc-portal/welcome.html']")
    DOC4 = (By.CSS_SELECTOR, "a[href='a[href='a[href='https://www.hippocampushub.eu/']")
    MAIN_TITLE = (By.XPATH, "//h1[contains(text(),'Virtual labs')]")
    P1 = (By.XPATH, "//p[contains(text(),'The Blue Brain Open Platform is built on')]")
    TITLE1 = (By.XPATH, "//h4[contains(text(),'Prefer')]")
    TITLE2 = (By.XPATH, "//h4[contains(text(),'who advanced the Blue Brain Project scientifically "
                        "over the years.')]")
