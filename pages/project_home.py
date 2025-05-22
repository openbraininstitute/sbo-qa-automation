from selenium.common import TimeoutException

from locators.project_home_locators import ProjectHomeLocators
from pages.home_page import HomePage


class ProjectHome(HomePage):
    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, base_url)
        self.home_page = HomePage(browser, wait, base_url)
        self.logger = logger

    def go_to_project_page(self, lab_id: str, project_id: str):
        path = f"/app/virtual-lab/lab/{lab_id}/project/{project_id}/home"
        try:
            self.browser.set_page_load_timeout(90)
            self.go_to_page(path)
            self.wait_for_page_ready(timeout=60)
        except TimeoutException:
            raise RuntimeError("The Project Home data page did not load within 60 seconds.")
        return self.browser.current_url

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
        return self.find_element(ProjectHomeLocators.EDIT_BTN)

    def edit_btn_unlock(self):
        return self.find_element(ProjectHomeLocators.EDIT_BTN_UNLOCKED)
