from locators.build_page_locators import BuildPageLocators
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage


class BuildPage(HomePage):
    def __init__(self, browser, wait):
        super().__init__(browser, wait)
        self.login_page = HomePage(browser, wait)

    # def go_to_build_page(self):
    #     self.browser.get(self.url + "/build/load-brain-config")
    #     return self.browser.current_url

    def go_to_build_page(self):
        self.browser.get("http://localhost:3000/build/load-brain-config")

    def find_recent_configurations(self):
        return self.wait.until(EC.presence_of_element_located(BuildPageLocators.RECENT_CONFIGURATIONS))

    def verify_release_version(self):
        return self.wait.until(EC.presence_of_element_located(BuildPageLocators.RELEASE_VERSION))

    def select_default_config(self):
        return self.wait.until(EC.presence_of_element_located(BuildPageLocators.BUILD_PAGE_CLICK_PLUS_ICON))

    def find_config_search_field(self):
        return self.wait.until(EC.visibility_of_element_located(BuildPageLocators.CONFIG_SEARCH_FIELD))

    def use_custom_config(self):
        return self.wait.until(EC.element_to_be_clickable(BuildPageLocators.CUSTOM_MODEL_CONFIG))

    # def clone_custom_config(self):
    #     return self.wait.until(EC.presence_of_element_located(BuildPageLocators.BTN_CLONE_CONFIG))
    def clone_custom_config(self):
        return self.wait.until(
            lambda d: EC.presence_of_element_located(BuildPageLocators.BTN_CLONE_CONFIG)(d)
        )

    def find_edit_config_modal(self):
        return self.wait.until(EC.visibility_of_element_located(BuildPageLocators.EDIT_MODAL))

    def find_default_config_name(self):
        return self.wait.until(EC.visibility_of_element_located(BuildPageLocators.CONFIG_TEXT_FIELD_NAME))

    def set_your_config_name(self):
        return self.wait.until(
            lambda d: EC.visibility_of_element_located(BuildPageLocators.CHANGE_CONFIG_NAME_TEXT_FIELD)(d)
        )

    def clear_default_description_name(self):
        return self.wait.until(
            lambda d: EC.visibility_of_element_located(BuildPageLocators.DESCRIPTION)(d)
        )

    def set_config_description(self):
        return self.wait.until(
            lambda d: EC.visibility_of_element_located(BuildPageLocators.DESCRIPTION)(d)
        )

    def click_on_description(self):
        return self.wait.until(EC.visibility_of_element_located(BuildPageLocators.DESCRIPTION))

    def push_start_editing(self):
        return self.wait.until(
            lambda d: EC.element_to_be_clickable(BuildPageLocators.BTN_START_EDITING)(d)
        )