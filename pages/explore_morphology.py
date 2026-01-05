# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

from selenium.common import ElementNotVisibleException, TimeoutException, \
    StaleElementReferenceException

from pages.explore_page import ExplorePage
from locators.explore_morphology_locators import ExploreMorphologyPageLocators


class ExploreMorphologyPage(ExplorePage):
    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, logger, base_url)
        self.logger = logger

    def go_to_explore_morphology_page(self, lab_id: str, project_id: str, retries=3, delay=5):
        path = f"/app/virtual-lab/{lab_id}/{project_id}/data/browse/entity/cell-morphology"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(90)
                self.go_to_page(path)
                self.wait_for_page_ready(timeout=60)
            except TimeoutException:
                print(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                time.sleep(delay)
                if attempt == retries - 1:
                    raise RuntimeError("The Explore Morphology page did not load within 60 seconds")
            return self.browser.current_url
        return None

    def clear_filters_btn(self):
        return self.find_element(ExploreMorphologyPageLocators.CLEAR_FILTERS_BTN)

    def confirm_selected_br(self):
        return self.find_element(ExploreMorphologyPageLocators.DV_SELECTED_BR)

    def find_ai_panel_btn(self):
        return self.find_element(ExploreMorphologyPageLocators.AI_ASSISTANT_PANEL_CLOSE_BTN)

    def find_column_headers(self, column_locators):
        column_headers = []
        missing_locators = []

        for locator in column_locators:
            try:
                elements = self.find_all_elements(locator)
                if elements:
                    self.logger.info(f"Found {len(elements)} elements for locator: {locator}")
                    column_headers.extend(elements)
                else:
                    self.logger.warning(f"No elements found for locator: {locator}")
                    missing_locators.append(locator)
            except TimeoutException:
                self.logger.error(f"Timeout while trying to find elements for locator: {locator}")
                missing_locators.append(locator)

        if missing_locators:
            raise Exception(f"Missing or timed out locators: {missing_locators}")

        return column_headers

    def find_morphology_tab(self):
        return self.find_element(ExploreMorphologyPageLocators.MORPHOLOGY_TAB)

    def find_thumbnails(self):
        return self.find_all_elements(ExploreMorphologyPageLocators.LV_THUMBNAIL)

    def find_results(self):
        return self.find_element(ExploreMorphologyPageLocators.RECORDS)

    def find_brain_region_column_title(self):
        return self.is_visible(ExploreMorphologyPageLocators.BRAIN_REGION_COLUMN_TITLE)

    def find_br_sort_arrow(self):
        return self.element_visibility(ExploreMorphologyPageLocators.BR_SORT_ARROW)

    def find_br_sorted(self):
        return self.element_visibility(ExploreMorphologyPageLocators.BR_SORTED)

    def find_first_row(self):
        return self.element_visibility(ExploreMorphologyPageLocators.FIRST_ROW)

    def find_species_sorted(self):
        return self.element_visibility(ExploreMorphologyPageLocators.SPECIES_SORTED)

    def find_table(self):
        return self.find_element(ExploreMorphologyPageLocators.TABLE)

    def find_back_to_ie_btn(self):
        return self.find_element(ExploreMorphologyPageLocators.BACK_IE_BTN)

    def find_back_to_list_btn(self):
        return self.element_visibility(ExploreMorphologyPageLocators.DV_BACK_BTN)

    def find_dv_title_header(self, title_locators):
        title_headers = []
        missing_locators = []

        for locator in title_locators:
            try:
                elements = self.find_all_elements(locator)
                if elements:
                    self.logger.info(f"Foound {len(elements)} elements for locator: {locator}")
                    title_headers.extend(elements)
                else:
                    self.logger.error(f"No elements found for locator: {locator}")
                    missing_locators.append(locator)
            except TimeoutException:
                self.logger.error(f"Timeout while trying to find elements for locator: {locator}")
                missing_locators.append(locator)
        if missing_locators:
            raise Exception(f"Missing elements for locators: {missing_locators}")
        return title_headers

    def find_morphometrics_title(self):
        return self.find_element(ExploreMorphologyPageLocators.DV_MORPHOMETRICS_TITLE)

    def find_morphology_titles(self, morpho_title):
        morpho_title = []
        for title in morpho_title:
            morpho_title.extend(self.find_all_elements(title))
        return morpho_title

    def find_morpho_viewer(self):
        return self.find_element(ExploreMorphologyPageLocators.MORPHO_VIEWER)

    def find_download_btn(self):
        return self.find_element(ExploreMorphologyPageLocators.DV_DOWNLOAD_BTN)

    def find_fullscreen_btn(self):
        return self.find_element(ExploreMorphologyPageLocators.MORPHO_VIEWER_FULLSCREEN_BTN)

    def filter_mtype(self):
        return self.element_visibility(ExploreMorphologyPageLocators.LV_FILTER_MTYPE)

    def filter_mtype_search(self):
        return self.find_element(ExploreMorphologyPageLocators.FILTER_MTYPE_SEARCH)

    def filter_mtype_text_input(self):
        return self.find_element(ExploreMorphologyPageLocators.FILTER_MTYPE_TEXT_INPUT)

    def find_filtered_mtype(self):
        return self.find_all_elements(ExploreMorphologyPageLocators.FILTERED_MTYPE)

    def find_search_input_search_item(self):
        return self.find_element(ExploreMorphologyPageLocators.SEARCH_INPUT_FIELD)

    def get_table_data(self):
        """Fetches all table data, row by row, with handling for dynamic changes to the DOM."""
        max_retries = 3  # Number of retries to handle stale elements
        table_data = []

        for attempt in range(max_retries):
            try:
                # Find the table element fresh each time to avoid stale references
                table = self.find_element(ExploreMorphologyPageLocators.TABLE)
                self.wait_for_page_ready(timeout=15)
                rows = table.find_elements(*ExploreMorphologyPageLocators.ROW)
                table_data = []
                for row in rows:
                    cells = row.find_elements(*ExploreMorphologyPageLocators.CELLS)
                    row_data = [cell.text.strip() for cell in cells]
                    table_data.append(row_data)

                return table_data

            except StaleElementReferenceException as e:
                self.logger.warning(
                    f"Stale element encountered on attempt {attempt + 1}. Retrying...")
                if attempt == max_retries - 1:
                    raise e  # Re-raise if we've reached the max retries

        raise RuntimeError("Failed to fetch table data due to persistent stale elements.")


    def is_sorted(self, data, col_index=0):
        # Check if data is not None and has at least one row
        if data and len(data) > 0 and data[0] is not None:
            col_values = [row[col_index] for row in data if len(row) > col_index]
            return col_values == sorted(col_values)
        return False

    def is_filter_panel_closed(self):
        try:
            # Use a locator for the filter panel (e.g., its container element)
            filter_panel = self.element_visibility(ExploreMorphologyPageLocators.FILTER_PANEL,
                                                   timeout=5)
            return not filter_panel.is_displayed()
        except TimeoutException:
            return True

    def lv_filter_apply(self, timeout=10):
        return self.find_element(ExploreMorphologyPageLocators.LV_FILTER_APPLY_BTN, timeout=timeout)

    def lv_filter_search(self):
        return self.find_element(ExploreMorphologyPageLocators.LV_FILTER_SEARCH)

    def lv_filter_search_field(self):
        return self.find_element(ExploreMorphologyPageLocators.LV_FILTER_SEARCH_FIELD)

    def morphology_filter(self):
        return self.element_visibility(ExploreMorphologyPageLocators.MORPHOLOGY_FILTER)

    def morphology_filter_close_btn(self):
        return self.find_element(ExploreMorphologyPageLocators.MORPHOLOGY_FILTER_CLOSE_BTN)

    def morpho_viewer_settings_btn(self):
        return self.find_element(ExploreMorphologyPageLocators.MORPHO_VIEWER_SETTINGS_BTN)

    def scroll_to_element(self, element):
        """Scrolls the page to bring the element into the viewport."""
        self.browser.execute_script("arguments[0].scrollIntoView();", element)

    def scroll_to_bottom(self):
        """Scrolls to the bottom of the page to trigger lazy-loading."""
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Allow time for lazy-loaded content to load

    def search_name(self):
        return self.element_visibility(ExploreMorphologyPageLocators.SEARCH_NAME)

    def verify_all_thumbnails_displayed(self):
        thumbnails = []
        last_height = 0

        while True:
            # Find thumbnails currently loaded
            new_thumbnails = self.find_thumbnails()
            for thumbnail in new_thumbnails:
                if thumbnail not in thumbnails:  # Avoid duplicate entries
                    thumbnails.append(thumbnail)

            # Scroll and update viewport height
            self.scroll_to_bottom()
            new_height = self.browser.execute_script("return document.body.scrollHeight;")

            # If no new height, assume we reached the end of the page
            if new_height == last_height:
                break
            last_height = new_height

        # Check displayed status for all found thumbnails
        thumbnail_status = []
        for thumbnail in thumbnails:
            try:
                self.scroll_to_element(thumbnail)  # Ensure it's in view
                is_displayed = thumbnail.is_displayed()
            except ElementNotVisibleException:
                self.logger.debug("Thumbnail is present but not visible in the viewport.")
                is_displayed = False
            thumbnail_status.append({
                'element': thumbnail,
                'is_displayed': is_displayed
            })

        return thumbnail_status

