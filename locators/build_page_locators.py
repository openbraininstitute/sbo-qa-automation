from selenium.webdriver.common.by import By


class BuildPageLocators:
    RECENT_CONFIGURATIONS = (By.XPATH, "//h3[contains(text(), 'Recently used configurations')]")
    RELEASE_VERSION = (By.XPATH, "//div[contains(text(), 'Release 23.01')]")
    PUBLIC_CONFIG_RELEASE = (By.XPATH, "//tbody//tr//*[contains(text(),'Release 23.01')]")
    BUILD_PAGE_CLICK_PLUS_ICON = (By.CSS_SELECTOR, "svg.icon_icon__TwrM_ > path")
    BASIC_CELL_GROUPS_REGIONS = (By.XPATH, "//span[text()='Basic cell groups and regions']")
    CONFIG_SEARCH_FIELD = (By.XPATH, "//div//input[@class='brain-config-loader-view_searchInput__mqQhO']")
    CUSTOM_MODEL_CONFIG = (By.XPATH, "//tbody/tr/td[@class='ant-table-cell' and contains(text(), 'Custom model configuration.')]")
    BTN_CLONE_CONFIG = (By.XPATH, "//tbody[@class='ant-table-tbody']/tr[@class ='ant-table-row ant-table-row-level-0'][1]/td[4]/button[2]")
    EDIT_MODAL = (By.CSS_SELECTOR, 'div[role="dialog"][aria-modal="true"]')
    EDIT_CONFIG_DIALOG = (By.XPATH, "//div[@role='dialog' and @aria-modal='true']//div[@class='ant-modal-confirm-body']//span[text()='Edit configuration']")
    CONFIG_TEXT_FIELD_NAME = (By.CSS_SELECTOR, '#name')
    CHANGE_CONFIG_NAME_TEXT_FIELD = (By.CSS_SELECTOR, "#name")
    BTN_START_EDITING = (By.XPATH, "//span[contains(text(), 'Start editing')]")