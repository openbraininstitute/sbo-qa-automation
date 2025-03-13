# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0



from selenium.webdriver.common.by import By


class LandingLocators:
    BANNER_TITLE = (By.XPATH, "//h1[contains(text(),'Create your Virtual Lab to build digital brain mod')]")
    TITLE_ACCELERATE = (By.XPATH, "//h1[normalize-space()='Accelerating neuroscience research']")
    TITLE_RECONSTRUCT = (By.XPATH, "//h1[normalize-space()='Reconstructing digital brain models']")
    TITLE_WHO = (By.XPATH, "//h1[normalize-space()='Who is behind the Open Brain Institute']")
    TITLE_NEWS = (By.XPATH, "//h1[normalize-space()='News and events']")
    GOTO_LAB = (By.XPATH, "//a[normalize-space()='Go to your lab']")
    P_TEXT1 = (By.XPATH, "(//div[@class='SanityContentPreview_text__ivnWe'])[1]")
    P_TEXT2 = (By.XPATH, "(//div[@class='SanityContentPreview_text__ivnWe'])[2]")
    P_TEXT3 = (By.XPATH, "(//div[@class='SanityContentPreview_text__ivnWe'])[3]")
    P_TEXT4 = (By.XPATH, "(//div[@class='SanityContentPreview_text__ivnWe'])[4]")
