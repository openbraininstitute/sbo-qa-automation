from selenium.webdriver.common.by import By


class BuildPageLocators:
    RECENT_CONFIGURATIONS = (By.XPATH, "//h3[contains(text(), 'Recently used configurations')]")
    RELEASE_VERSION = (By.XPATH, "//div[contains(text(), 'Release 23.01')]")
    PUBLIC_CONFIG_RELEASE = (By.XPATH, "//tbody//tr//*[contains(text(),'Release 23.01')]")
    # BUILD_CONFIGURATION_NEXT_PAGE = (By.XPATH, "//ul//li//*[contains(text(),'Next Page')]")
    # BUILD_CONFIGURATION_NEXT_PAGE = (By.CSS_SELECTOR, "li[class='ant-pagination-next']")
    BUILD_PAGE_CLICK_PLUS_ICON = (By.CSS_SELECTOR, "svg.icon_icon__TwrM_ > path")