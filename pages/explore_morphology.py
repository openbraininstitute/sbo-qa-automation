# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0
import time

from selenium.common import ElementNotVisibleException, TimeoutException, \
    StaleElementReferenceException

from pages.explore_page import ExplorePage
from locators.explore_morphology_locators import ExploreMorphologyPageLocators
from util.util_links_checker import LinkChecker
from util.util_scraper import UrlScraper


class ExploreMorphologyPage(ExplorePage, LinkChecker):
    def __init__(self, browser, wait, logger):
        super().__init__(browser, wait)
        self.home_page = ExplorePage(browser, wait)
        self.url_scraper = UrlScraper()
        self.logger = logger

    def go_to_explore_morphology_page(self):
        try:
            self.go_to_page("/explore/interactive/experimental/morphology")
            self.wait_for_page_ready(timeout=60)
        except TimeoutException:
            raise RuntimeError("The Explore Morphology page did not load within 60 seconds")
        return self.browser.current_url

    def find_morphology_tab(self):
        return self.find_element(ExploreMorphologyPageLocators.MORPHOLOGY_TAB)

    def morphology_filter(self):
        return self.element_visibility(ExploreMorphologyPageLocators.MORPHOLOGY_FILTER)

    def morphology_filter_close_btn(self):
        return self.find_element(ExploreMorphologyPageLocators.MORPHOLOGY_FILTER_CLOSE_BTN)

    def find_column_headers(self, column_locators):
        column_headers = []
        for locator in column_locators:
            column_headers.extend(self.find_all_elements(locator))
        return column_headers

    def find_thumbnails(self):
        return self.find_all_elements(ExploreMorphologyPageLocators.LV_THUMBNAIL)

    def scroll_to_element(self, element):
        """Scrolls the page to bring the element into the viewport."""
        self.browser.execute_script("arguments[0].scrollIntoView();", element)

    def scroll_to_bottom(self):
        """Scrolls to the bottom of the page to trigger lazy-loading."""
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Allow time for lazy-loaded content to load

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

    def find_results(self):
        return self.find_element(ExploreMorphologyPageLocators.RESULTS)

    def find_br_sort_arrow(self):
        return self.element_visibility(ExploreMorphologyPageLocators.BR_SORT_ARROW)

    def find_br_sorted(self):
        return self.element_visibility(ExploreMorphologyPageLocators.BR_SORTED)

    def find_species_sorted(self):
        return self.element_visibility(ExploreMorphologyPageLocators.SPECIES_SORTED)

    def find_brain_region_column_title(self):
        return self.is_visible(ExploreMorphologyPageLocators.BRAIN_REGION_COLUMN_TITLE)

    def find_first_row(self):
        return self.element_visibility(ExploreMorphologyPageLocators.FIRST_ROW)

    def find_table(self):
        return self.find_element(ExploreMorphologyPageLocators.TABLE)

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

    def find_back_to_ie_btn(self):
        return self.find_element(ExploreMorphologyPageLocators.BACK_IE_BTN)

    def find_dv_headers(self, dv_header_locators):
        result_list = []
        for locator in dv_header_locators:
            result_list.extend(self.find_all_elements(locator))
        return result_list

    def confirm_selected_br(self):
        return self.find_element(ExploreMorphologyPageLocators.DV_SELECTED_BR)

    def find_morphometrics_title(self):
        return self.find_element(ExploreMorphologyPageLocators.DV_MORPHOMETRICS_TITLE)

    def find_morphology_titles(self, morpho_title):
        morpho_title = []
        for title in morpho_title:
            morpho_title.extend(self.find_all_elements(title))
        return morpho_title

    def find_morpho_viewer(self):
        return self.find_element(ExploreMorphologyPageLocators.MORPHO_VIEWER)

    def find_fullscreen_btn(self):
        return self.find_element(ExploreMorphologyPageLocators.MORPHO_VIEWER_FULLSCREEN_BTN)

    def morpho_viewer_settings_btn(self):
        return self.find_element(ExploreMorphologyPageLocators.MORPHO_VIEWER_SETTINGS_BTN)

    def find_download_btn(self):
        return self.find_element(ExploreMorphologyPageLocators.DV_DOWNLOAD_BTN)

    def find_back_to_list_btn(self):
        return self.element_visibility(ExploreMorphologyPageLocators.DV_BACK_BTN)

    def filter_mtype(self):
        return self.element_visibility(ExploreMorphologyPageLocators.LV_FILTER_MTYPE)

    def filter_mtype_search(self):
        return self.find_element(ExploreMorphologyPageLocators.FILTER_MTYPE_SEARCH)

    def filter_mtype_text_input(self):
        return self.find_element(ExploreMorphologyPageLocators.FILTER_MTYPE_TEXT_INPUT)

    def lv_filter_apply(self, timeout=10):
        return self.find_element(ExploreMorphologyPageLocators.LV_FILTER_APPLY_BTN, timeout=timeout)

    def find_filtered_mtype(self):
        return self.find_all_elements(ExploreMorphologyPageLocators.FILTERED_MTYPE)

    def find_search_input_search_item(self):
        return self.find_element(ExploreMorphologyPageLocators.SEARCH_INPUT_FIELD)

    def search_name(self):
        return self.element_visibility(ExploreMorphologyPageLocators.SEARCH_NAME)

    def clear_filters_btn(self):
        return self.find_element(ExploreMorphologyPageLocators.CLEAR_FILTERS_BTN)

    def is_filter_panel_closed(self):
        try:
            # Use a locator for the filter panel (e.g., its container element)
            filter_panel = self.element_visibility(ExploreMorphologyPageLocators.FILTER_PANEL,
                                                   timeout=5)
            return not filter_panel.is_displayed()
        except TimeoutException:
            return True

    def lv_filter_search(self):
        return self.find_element(ExploreMorphologyPageLocators.LV_FILTER_SEARCH)
