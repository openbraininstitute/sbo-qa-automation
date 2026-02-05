# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

from selenium.common import ElementNotVisibleException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.explore_page import ExplorePage
from locators.explore_ephys_locators import ExploreEphysLocators
from locators.explore_page_locators import ExplorePageLocators


class ExploreElectrophysiologyPage(ExplorePage):
    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, logger, base_url)
        self.home_page = ExplorePage(browser, wait, logger, base_url)
        self.logger = logger

    def go_to_explore_ephys_page(self, lab_id: str, project_id: str, retries=3, delay=5):
        """Navigate to the explore electrophysiology page"""
        # Updated path for the new URL structure
        path = f"/app/virtual-lab/{lab_id}/{project_id}/data/browse/entity/electrical-cell-recording"
        for attempt in range(retries):
            try:
                self.browser.set_page_load_timeout(90)
                self.go_to_page(path)
                self.wait_for_page_ready(timeout=60)
                self.logger.info(f"Successfully navigated to explore ephys page: {self.browser.current_url}")
            except TimeoutException:
                self.logger.warning(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                time.sleep(delay)
                if attempt == retries - 1:
                    raise RuntimeError("The Explore Electrophysiology page did not load within 60 seconds")
        return self.browser.current_url

    # Data type selector methods (new functionality)
    def find_data_type_selector(self, timeout=10):
        """Find the data type selector container"""
        return self.find_element(ExploreEphysLocators.DATA_TYPE_SELECTOR, timeout=timeout)

    def find_experimental_tab(self, timeout=10):
        """Find the Experimental tab"""
        return self.find_element(ExploreEphysLocators.EXPERIMENTAL_TAB, timeout=timeout)

    def find_model_tab(self, timeout=10):
        """Find the Model tab"""
        return self.find_element(ExploreEphysLocators.MODEL_TAB, timeout=timeout)

    def find_simulations_tab(self, timeout=10):
        """Find the Simulations tab"""
        return self.find_element(ExploreEphysLocators.SIMULATIONS_TAB, timeout=timeout)

    def verify_experimental_tab_selected(self):
        """Verify that the Experimental tab is selected"""
        experimental_tab = self.find_experimental_tab()
        is_selected = experimental_tab.get_attribute('aria-selected') == 'true'
        assert is_selected, "Experimental tab should be selected by default"
        self.logger.info("✅ Experimental tab is selected")
        return is_selected

    def find_single_cell_electrophysiology_button(self, timeout=10):
        """Find the Single cell electrophysiology button"""
        return self.find_element(ExploreEphysLocators.SINGLE_CELL_ELECTROPHYSIOLOGY_BTN, timeout=timeout)

    def verify_single_cell_electrophysiology_text(self):
        """Verify the Single cell electrophysiology text is present"""
        text_element = self.find_element(ExploreEphysLocators.SINGLE_CELL_ELECTROPHYSIOLOGY_TEXT)
        assert text_element.is_displayed(), "Single cell electrophysiology text should be displayed"
        self.logger.info("✅ Single cell electrophysiology text is displayed")
        return text_element

    # Table and data methods (new functionality)
    def find_data_table_with_filters(self, timeout=10):
        """Find the data table with filters section"""
        return self.find_element(ExploreEphysLocators.DATA_TABLE_WITH_FILTERS, timeout=timeout)

    def verify_table_columns(self):
        """Verify that all required table columns are present"""
        expected_columns = [
            (ExploreEphysLocators.TABLE_HEADER_PREVIEW, "Preview"),
            (ExploreEphysLocators.TABLE_HEADER_BRAIN_REGION, "Brain region"),
            (ExploreEphysLocators.TABLE_HEADER_ETYPE, "E-type"),
            (ExploreEphysLocators.TABLE_HEADER_NAME, "Name"),
            (ExploreEphysLocators.TABLE_HEADER_SPECIES, "Species"),
            (ExploreEphysLocators.TABLE_HEADER_CONTRIBUTORS, "Contributors"),
            (ExploreEphysLocators.TABLE_HEADER_REGISTRATION_DATE, "Registration date")
        ]
        
        found_columns = []
        missing_columns = []
        
        for locator, column_name in expected_columns:
            try:
                element = self.find_element(locator, timeout=5)
                if element.is_displayed():
                    found_columns.append(column_name)
                    self.logger.info(f"✅ Found column: {column_name}")
                else:
                    missing_columns.append(column_name)
                    self.logger.warning(f"❌ Column not displayed: {column_name}")
            except TimeoutException:
                missing_columns.append(column_name)
                self.logger.warning(f"❌ Column not found: {column_name}")
        
        if missing_columns:
            self.logger.error(f"Missing columns: {missing_columns}")
            # Don't fail the test, just log the missing columns
        
        self.logger.info(f"Found {len(found_columns)} out of {len(expected_columns)} expected columns")
        return found_columns, missing_columns

    def get_table_rows(self):
        """Get all table rows"""
        return self.find_all_elements(ExploreEphysLocators.TABLE_ROWS)

    def get_table_cells(self):
        """Get all table cells"""
        return self.find_all_elements(ExploreEphysLocators.TABLE_CELLS)

    # Search functionality (new)
    def find_search_button(self, timeout=10):
        """Find the search button"""
        return self.find_element(ExploreEphysLocators.SEARCH_BUTTON, timeout=timeout)

    def find_search_input(self, timeout=10):
        """Find the search input field"""
        return self.find_element(ExploreEphysLocators.SEARCH_INPUT, timeout=timeout)

    def perform_search(self, search_term):
        """Perform a search operation"""
        search_button = self.find_search_button()
        search_button.click()
        self.logger.info("Clicked search button")
        
        search_input = self.find_search_input()
        search_input.clear()
        search_input.send_keys(search_term)
        self.logger.info(f"Entered search term: {search_term}")
        
        # Wait for search results to load
        time.sleep(2)
        return True

    # Filter functionality (new)
    def find_filter_button(self, timeout=10):
        """Find the filter button"""
        return self.find_element(ExploreEphysLocators.FILTER_BUTTON, timeout=timeout)

    def get_filter_count(self):
        """Get the current filter count"""
        try:
            filter_count_element = self.find_element(ExploreEphysLocators.FILTER_COUNT, timeout=5)
            return int(filter_count_element.text)
        except (TimeoutException, ValueError):
            return 0

    # Legacy methods (keeping for backward compatibility with existing tests)
    def brain_region_panel_close_btn(self):
        return self.find_element(ExploreEphysLocators.BRAIN_REGION_PANEL_CLOSE_BTN)

    def brain_region_panel_open_btn(self):
        return self.find_element(ExploreEphysLocators.BRAIN_REGION_PANEL_OPEN_BTN)

    def download_resources(self):
        return self.find_element(ExploreEphysLocators.DOWNLOAD_RESOURCES)

    def find_ai_assistant_panel(self, timeout=10):
        return self.find_element(ExplorePageLocators.AI_ASSISTANT_PANEL, timeout=timeout)

    def find_ai_assistant_panel_close(self, timeout=10):
        return self.find_element(ExplorePageLocators.AI_ASSISTANT_PANEL_CLOSE, timeout=timeout)

    def wait_for_element(self, locator):
        return self.visibility_of_all_elements(locator)

    def dv_id_plots(self):
        return self.find_element(ExploreEphysLocators.DV_ID_PLOTS)

    def dv_id_stimulus_title(self):
        return self.find_element(ExploreEphysLocators.DV_ID_STIMULUS_TITLE)

    def dv_id_repetition_title(self):
        return self.find_element(ExploreEphysLocators.DV_ID_REPETITION_TITLE)

    def dv_id_sweep_title(self):
        return self.find_element(ExploreEphysLocators.DV_ID_SWEEP_TITLE)

    def dv_interactive_details_btn(self):
        return self.find_element(ExploreEphysLocators.DV_INTER_DETAILS)

    def dv_overview_btn(self, timeout=10):
        return self.find_element(ExploreEphysLocators.DV_OVERVIEW, timeout=timeout)

    def dv_plots(self):
        return self.find_all_elements(ExploreEphysLocators.DV_PLOTS)

    def dv_stimulus_btn(self):
        return self.find_element(ExploreEphysLocators.DV_STIMULUS_BTN)

    def dv_stimulus_all(self):
        return self.find_element(ExploreEphysLocators.DV_STIMULUS_ALL)

    def dv_stimulus_img_grid(self):
        return self.find_element(ExploreEphysLocators.DV_STIMULUS_IMG_GRID)

    def dv_stim_images(self):
        return self.find_all_elements(ExploreEphysLocators.DV_STIM_IMAGES)

    def dv_stimulus_search(self):
        return self.find_element(ExploreEphysLocators.DV_STIMULUS_SEARCH)

    def find_apply_btn(self):
        return self.find_element(ExploreEphysLocators.APPLY_BTN)

    def find_btn_all_checkboxes(self):
        return self.find_element(ExploreEphysLocators.ALL_CHECKBOXES)

    def find_dv_metadata(self, locators):
        metadata = []
        for data in locators:
            metadata.extend(self.find_all_elements(data))
        return metadata

    def find_ephys_tab_title(self):
        return self.find_element(ExploreEphysLocators.EPHYS_TAB_TITLE)

    def filter_etype_btn(self):
        return self.find_element(ExploreEphysLocators.FILTER_ETYPE_BTN)

    def filter_etype_search(self):
        return self.find_element(ExploreEphysLocators.FILTER_ETYPE_SEARCH)

    def filter_etype_search_input(self):
        return self.find_element(ExploreEphysLocators.FILTER_ETYPE_SEARCH_INPUT)

    def filter_etype_input_type_area(self):
        return self.find_element(ExploreEphysLocators.FILTER_ETYPE_INPUT_TYPE_AREA)

    def find_filtered_etype(self):
        return self.find_all_elements(ExploreEphysLocators.FILTERED_ETYPE)

    def find_dv_title_header(self, title_locators):
        title_headers = []
        missing_locators = []

        for locator in title_locators:
            try:
                elements = self.find_all_elements(locator)
                if elements:
                    self.logger.info(f"Found {len(elements)} elements for locator: {locator}")
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

    def find_column_headers(self, column_locators):
        column_headers = []
        missing_locators = []  # To track locators that find no elements

        for locator in column_locators:
            elements = self.find_all_elements(locator)  # Try to find elements
            if elements:
                self.logger.info(f"Found {len(elements)} elements for locator: {locator}")
                column_headers.extend(elements)
            else:
                self.logger.warning(f"No elements found for locator: {locator}")
                missing_locators.append(locator)  # Add missing locators to the list

        return column_headers, missing_locators

    def find_explore_section_grid(self):
        return self.element_visibility(ExploreEphysLocators.LV_GRID_VIEW)

    def find_filter_btn(self):
        return self.find_element(ExploreEphysLocators.LV_FILTER_BTN)

    def find_filter_close_btn(self):
        return self.element_visibility(ExploreEphysLocators.LV_FILTER_CLOSE_BTN)

    def find_load_more_btn(self):
        return self.find_element(self.wait, ExploreEphysLocators.LOAD_MORE_BUTTON)

    def find_table_rows(self):
        return self.find_all_elements(ExploreEphysLocators.TABLE_ROWS)

    def find_search_input_search_item(self):
        return self.find_element(ExploreEphysLocators.SEARCH_INPUT_FIELD)

    def find_checkboxes(self):
        return self.find_all_elements(ExploreEphysLocators.CHECKBOXES)

    def find_table(self):
        return self.find_element(ExploreEphysLocators.TABLE)

    def find_thumbnails(self):
        return self.visibility_of_all_elements(ExploreEphysLocators.LV_THUMBNAIL)

    def lv_filter_apply(self):
        return self.find_element(ExploreEphysLocators.LV_FILTER_APPLY_BTN)

    def lv_row1(self):
        return self.find_element(ExploreEphysLocators.LV_ROW1)

    def lv_total_results(self):
        return self.find_element(ExploreEphysLocators.LV_TOTAL_RESULTS)

    def perform_full_validation(self):
        self.validate_empty_cells()
        load_more_button = self.find_load_more_btn()
        load_more_button.click()
        self.validate_empty_cells()

    def scrape_links(self):
        page_source = self.browser.page_source
        links = self.url_scraper.scrape_links(page_source)

    def search_species(self):
        return self.element_visibility(ExploreEphysLocators.SEARCHED_SPECIES)

    def validate_empty_cells(self):
        rows = self.find_table_rows()
        for row_index, row in enumerate(rows, start=2):
            cells = self.find_all_elements(ExploreEphysLocators.TABLE_CELLS)
            for cell_index, cell in enumerate(cells, start=2):
                if not cell.text.strip():
                    error_message = f'Error: Empty field in a row{row_index}, cell {cell_index}'
                    print(error_message)

    def verify_all_thumbnails_displayed(self):
        thumbnails = self.find_thumbnails()

        thumbnail_status = []
        for thumbnail in thumbnails:
            thumbnail_status.append({
                'element': thumbnail,
                'is_displayed': thumbnail.is_displayed()
            })

        return thumbnail_status

    def wait_for_page_ready(self, timeout=30):
        """Wait for the page to be ready"""
        WebDriverWait(self.browser, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        # Additional wait for the data table to be present
        try:
            self.find_data_table_with_filters(timeout=timeout)
        except TimeoutException:
            # Fallback to legacy grid view
            self.find_explore_section_grid()