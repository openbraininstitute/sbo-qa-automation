from selenium.webdriver.common.by import By


class BuildPageLocators:
    RECENT_CONFIGURATIONS = (By.XPATH, "//h3[contains(text(), 'Recently used configurations')]")
    RELEASE_VERSION = (By.XPATH, "//div[contains(text(), 'Release 23.01')]")
