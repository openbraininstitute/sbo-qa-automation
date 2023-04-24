from selenium.webdriver.common.by import By


class BuildPageLocators:
    RECENT_CONFIGURATIONS = (By.XPATH, "//h3[contains(text(), 'Recently used configurations')]")
