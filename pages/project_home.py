from selenium.common import TimeoutException

from locators.project_home_locators import ProjectHomeLocators
from pages.home_page import HomePage


class ProjectHome(HomePage):
    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, base_url)
        self.home_page = HomePage(browser, wait, base_url)
        self.logger = logger

    def go_to_project_page(self, lab_id: str, project_id: str):
        path = f"/app/virtual-lab/{lab_id}/{project_id}/"
        try:
            self.browser.set_page_load_timeout(90)
            self.go_to_page(path)
            self.wait_for_page_ready(timeout=60)
        except TimeoutException:
            raise RuntimeError("The Project Home data page did not load within 60 seconds.")
        return self.browser.current_url

    def skip_onboardin_btn(self):
        return self.find_element(ProjectHomeLocators.SKIP_ONBOARDING_BTN)

    def project_menu_titles(self, titles, timeout=10):
        """
        Fetch WebElement for each locator or return None if not found.
        """
        found_titles = {}
        for title in titles:
            try:
                elements = self.find_all_elements(title, timeout)  # Adjust timeout as necessary
                found_titles[title] = elements[0] if elements else None
            except Exception as e:  # Catch timeout or other exceptions
                self.logger.error(f"Error locating element for {title}: {str(e)}")
                found_titles[title] = None
        return found_titles

    def edit_btn(self):
        return self.find_element(ProjectHomeLocators.PROJECT_EDIT_BTN)

    def edit_btn_unlock(self):
        return self.find_element(ProjectHomeLocators.PROJECT_EDIT_REVERSE)

    def menu_virtual_lab(self):
        return self.find_element(ProjectHomeLocators.TOP_MENU_VLAB_MENU)

    def menu_credits(self):
        return self.find_element(ProjectHomeLocators.TOP_MENU_PROJECT_CREDITS_BTN)

    def project_description(self):
        return self.find_element(ProjectHomeLocators.PROJECT_DESCRIPTION)

    def project_show_more(self):
        return self.find_element(ProjectHomeLocators.PROJECT_DESC_SHOW_MORE_BTN)

    def project_overview_tab(self):
        return self.find_element(ProjectHomeLocators.PROJECT_OVERVIEW_TAB)

    def members_tab(self):
        return self.find_element(ProjectHomeLocators.PROJECT_MEMBERS_TAB)

    def credits_tab(self):
        return self.find_element(ProjectHomeLocators.PROJECT_CREDITS_TAB)


