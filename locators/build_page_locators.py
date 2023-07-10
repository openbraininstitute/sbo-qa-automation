from selenium.webdriver.common.by import By


class BuildPageLocators:
    RECENT_CONFIGURATIONS = (By.XPATH, "//h3[contains(text(), 'Recently used configurations')]")
    RELEASE_VERSION = (By.XPATH, "//div[contains(text(), 'Release 23.01')]")
    PUBLIC_CONFIG_RELEASE = (By.XPATH, "//tbody//tr//*[contains(text(),'Release 23.01')]")
    BUILD_PAGE_CLICK_PLUS_ICON = (By.CSS_SELECTOR, "svg.icon_icon__TwrM_ > path")
    BASIC_CELL_GROUPS_REGIONS = (By.XPATH, "//span[text()='Basic cell groups and regions']")
    CONFIG_SEARCH_FIELD = (By.XPATH, "//div//input[@class='brain-config-loader-view_searchInput__mqQhO']")
    CUSTOM_MODEL_CONFIG = (By.XPATH, "//tbody/tr/td[@class='ant-table-cell' and contains(text(), 'Custom model "
                                     "configuration.')]")
    BTN_CLONE_CONFIG = (
    By.XPATH, "//tr[2]/td[contains(text(), 'Custom model configuration')]/following-sibling::td//button[2]")

    EDIT_MODAL = (By.CSS_SELECTOR, 'div[role="dialog"][aria-modal="true"]')
    EDIT_CONFIG_DIALOG = (By.XPATH, "//div[@role='dialog' and @aria-modal='true']//div["
                                    "@class='ant-modal-confirm-body']//span[text()='Edit configuration']")
    CONFIG_TEXT_FIELD_NAME = (By.CSS_SELECTOR, '#name')
    CHANGE_CONFIG_NAME_TEXT_FIELD = (By.CSS_SELECTOR, "#name")
    DESCRIPTION = (By.ID, 'description')
    BTN_START_EDITING = (By.XPATH, "//span[text()='Start editing']")
    BASIC_CELL_GROUPS_AND_REGIONS = (By.XPATH, "//span[contains(text(),'Basic cell groups and regions')]")

    CELL_COMPOSITION = (By.XPATH, "//a[text()='Cell composition']")
    CELL_MODEL_ASSIGNMENT = (By.XPATH, "//a[text()='Cell model assignment']")
    CONNECTOME_DEFINITION = (By.XPATH, "//a[text()='Connectome definition']")
    CONNECTION_MODEL_ASSIGNMENT = (By.XPATH, "//a[text()='Connection model assignment']")
    BUILD_AND_SIMULATE_BUTTON = (By.XPATH, "//button[text()='Build & Simulate' and @type='button']")

    BRAIN_BUILD_SECTION_MAIN = (By.XPATH, "//*[starts-with(@class,'build-section-main_')]")
    BRAIN_BUILD_CLOSED_DIV = (By.XPATH, "//div[@data-state='closed']")
    VISIBLE_BASIC_CELL_GROUPS_TEXT = (By.XPATH, "//span[text()='Basic cell groups and regions']")

    BASIC_CELL_GROUPS_ARROW_BTN = (
    By.XPATH, "//div[@class='py-3 flex items-center justify-between']//button[3]//*[name()='svg']")
    BLOCK_CEREBRUM = (By.XPATH, "//div[3][@data-state='closed']")
    CEREBRUM_ARROW_BUTTON = (By.XPATH, "//div[3][@data-state='closed']//descendant::button[4]//*[name()='svg']")

    CELL_COMP_INTERACTIVE = (By.XPATH, "//a[starts-with(@href, '/mmb-beta/build/cell-composition/interactive?brainModelConfigId=') and text()='Interactive']" )

