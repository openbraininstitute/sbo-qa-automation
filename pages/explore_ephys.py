# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

from selenium.common import ElementNotVisibleException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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
                return self.browser.current_url  # Return immediately on success
            except TimeoutException:
                self.logger.warning(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                time.sleep(delay)
                if attempt == retries - 1:
                    raise RuntimeError("The Explore Electrophysiology page did not load within 60 seconds")
        
        return self.browser.current_url

    def find_public_project_tab_container(self, timeout=10):
        """Find the Public/Project tab container"""
        return self.find_element(ExploreEphysLocators.PUBLIC_PROJECT_TAB_CONTAINER, timeout=timeout)

    def find_public_tab(self, timeout=10):
        """Find the Public tab"""
        return self.find_element(ExploreEphysLocators.PUBLIC_TAB, timeout=timeout)

    def find_project_tab(self, timeout=10):
        """Find the Project tab"""
        return self.find_element(ExploreEphysLocators.PROJECT_TAB, timeout=timeout)

    def verify_public_tab_selected(self):
        """Verify that the Public tab is selected"""
        public_tab = self.find_public_tab()
        is_selected = public_tab.get_attribute('aria-selected') == 'true'
        assert is_selected, "Public tab should be selected by default"
        self.logger.info("✅ Public tab is selected")
        return is_selected

    def click_public_tab(self):
        """Click the Public tab"""
        public_tab = self.find_public_tab()
        public_tab.click()
        self.logger.info("Clicked Public tab")
        return True

    def click_project_tab(self):
        """Click the Project tab"""
        project_tab = self.find_project_tab()
        project_tab.click()
        self.logger.info("Clicked Project tab")
        return True

    # Enhanced search functionality
    def perform_name_search(self, search_term):
        """Perform a search by name"""
        search_button = self.find_search_button()
        search_button.click()
        self.logger.info("Clicked search button")
        
        # Wait for search input to appear
        time.sleep(1)
        
        search_input = self.find_search_input()
        search_input.clear()
        search_input.send_keys(search_term)
        self.logger.info(f"Entered search term: {search_term}")
        
        # Press Enter or wait for search results
        search_input.send_keys("\n")
        time.sleep(2)  # Wait for search results to load
        return True

    def clear_search(self):
        """Clear the search input"""
        try:
            clear_button = self.find_element(ExploreEphysLocators.SEARCH_CLEAR_BTN, timeout=5)
            clear_button.click()
            self.logger.info("Cleared search")
            return True
        except TimeoutException:
            self.logger.warning("Clear search button not found")
            return False

    def find_thumbnails(self):
        """Find all thumbnails"""
        return self.find_all_elements(ExploreEphysLocators.THUMBNAILS)

    def verify_thumbnails_present(self):
        """Verify that thumbnails are present and displayed"""
        thumbnails = self.find_thumbnails()
        displayed_thumbnails = []
        failed_thumbnails = []
        
        for i, thumbnail in enumerate(thumbnails):
            try:
                if thumbnail.is_displayed():
                    displayed_thumbnails.append(i)
                    self.logger.info(f"✅ Thumbnail {i+1} is displayed")
                else:
                    failed_thumbnails.append(i)
                    self.logger.warning(f"❌ Thumbnail {i+1} is not displayed")
            except Exception as e:
                failed_thumbnails.append(i)
                self.logger.warning(f"❌ Thumbnail {i+1} error: {e}")
        
        self.logger.info(f"Found {len(displayed_thumbnails)} displayed thumbnails out of {len(thumbnails)} total")
        return displayed_thumbnails, failed_thumbnails

    def verify_search_results_brain_region(self, expected_brain_region):
        """Verify that search results contain the expected brain region"""
        # Wait for table to load after search
        time.sleep(2)
        
        table_rows = self.get_table_rows()
        if not table_rows:
            self.logger.warning("No table rows found after search")
            return False
        
        matching_rows = 0
        
        # Look for cells with the specific brain region using locators from locators file
        try:
            exact_xpath = ExploreEphysLocators.TABLE_BRAIN_REGION_CELL_EXACT_TEMPLATE.format(expected_brain_region)
            brain_region_cells = self.find_all_elements((By.XPATH, exact_xpath))
            
            if brain_region_cells:
                matching_rows = len(brain_region_cells)
                self.logger.info(f"✅ Found {matching_rows} cells with brain region '{expected_brain_region}'")
                
                # Log first few matches for verification
                for i, cell in enumerate(brain_region_cells[:5]):
                    cell_text = cell.text.strip()
                    self.logger.info(f"  Row {i+1}: '{cell_text}'")
                
                return True
            else:
                self.logger.warning(f"❌ No cells found with brain region '{expected_brain_region}'")
                
                partial_xpath = ExploreEphysLocators.TABLE_BRAIN_REGION_CELL_PARTIAL_TEMPLATE.format(expected_brain_region)
                partial_match_cells = self.find_all_elements((By.XPATH, partial_xpath))
                
                if partial_match_cells:
                    matching_rows = len(partial_match_cells)
                    self.logger.info(f"✅ Found {matching_rows} cells with brain region containing '{expected_brain_region}' (partial match)")
                    
                    # Log first few matches
                    for i, cell in enumerate(partial_match_cells[:5]):
                        cell_title = cell.get_attribute('title')
                        self.logger.info(f"  Row {i+1}: '{cell_title}'")
                    
                    return True
                else:
                    self.logger.warning(f"❌ No cells found containing '{expected_brain_region}' even with partial match")
                    return False
                    
        except Exception as e:
            self.logger.error(f"Error verifying search results: {e}")
            return False

    def get_search_results_count(self):
        """Get the number of search results"""
        try:
            results_count_element = self.find_element((By.XPATH, "//div[contains(text(), 'results') or contains(text(), 'found')]"), timeout=5)
            return results_count_element.text
        except TimeoutException:
            # Fallback: count table rows
            rows = self.get_table_rows()
            return f"{len(rows)} rows found"

    def apply_species_filter(self, species_name):
        """Verify the Species filter label is displayed in the filter panel.
        The Species filter is no longer an expandable accordion — just verify the label exists.
        """
        try:
            species_label = self.find_element(ExploreEphysLocators.FILTER_SPECIES_BUTTON, timeout=10)
            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", species_label)
            time.sleep(0.5)
            is_displayed = species_label.is_displayed()
            self.logger.info(f"Species filter label displayed: {is_displayed}, text: '{species_label.text.strip()}'")
            return is_displayed
        except TimeoutException:
            self.logger.warning("Species filter label not found in filter panel")
            return False

    def apply_contributor_filter(self, contributor_name):
        """Apply filter by contributor"""
        try:
            contributor_filter = self.find_element(ExploreEphysLocators.FILTER_CONTRIBUTORS_BUTTON, timeout=10)
            contributor_filter.click()
            self.logger.info("Clicked Contributors filter")
            time.sleep(1)
            
            contributor_search = self.find_element(ExploreEphysLocators.FILTER_CONTRIBUTORS_SEARCH, timeout=5)
            contributor_search.send_keys(contributor_name)
            self.logger.info(f"Entered contributor: {contributor_name}")
            time.sleep(1)
            
            contributor_option = self.find_element((By.XPATH, f"//div[contains(text(), '{contributor_name}')]"), timeout=5)
            contributor_option.click()
            self.logger.info(f"Selected contributor: {contributor_name}")
            
            return True
        except TimeoutException:
            self.logger.warning("Contributor filter not found or not accessible")
            return False

    def apply_filters(self):
        """Apply the selected filters"""
        try:
            apply_button = self.find_element((By.XPATH, "//button[@role='button']//span[text()='Apply']//parent::button"), timeout=10)
            
            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", apply_button)
            time.sleep(0.5)
            
            try:
                apply_button.click()
            except Exception as e:
                self.logger.warning(f"Regular click failed on Apply button, using JavaScript click: {e}")
                self.browser.execute_script("arguments[0].click();", apply_button)
            
            self.logger.info("Applied filters")
            time.sleep(2)  # Wait for results to load
            return True
        except TimeoutException:
            self.logger.warning("Apply button not found")
            return False

    def close_filter_panel(self):
        """Close the filter panel"""
        try:
            close_button = self.find_element(ExploreEphysLocators.FILTER_CLOSE_BUTTON, timeout=5)
            close_button.click()
            self.logger.info("Closed filter panel")
            return True
        except TimeoutException:
            self.logger.warning("Close button not found")
            return False

    def verify_filtered_results(self, expected_value, column_type="species"):
        """Verify that filtered results contain the expected value"""
        table_rows = self.get_table_rows()
        if not table_rows:
            self.logger.warning("No table rows found")
            return False
        
        found_matches = 0
        total_checked = 0
        
        for row in table_rows[:10]:  # Check first 10 rows
            try:
                total_checked += 1
                cells = row.find_elements(By.TAG_NAME, "td")
                
                if column_type == "species":
                    species_cell = None
                    
                    if len(cells) > 5:
                        species_cell = cells[5]
                    
                    if species_cell:
                        cell_text = species_cell.text.strip()
                        cell_title = species_cell.get_attribute('title') or ""
                        
                        if expected_value.lower() in cell_text.lower() or expected_value.lower() in cell_title.lower():
                            found_matches += 1
                            self.logger.debug(f"Row {total_checked}: ✅ Found match - text: '{cell_text}', title: '{cell_title}'")
                        else:
                            # Log all cells for debugging
                            all_cells_text = [f"[{i}]: '{c.text.strip()}'" for i, c in enumerate(cells)]
                            self.logger.debug(f"Row {total_checked}: ❌ No match in column 5 - text: '{cell_text}', title: '{cell_title}'. All cells: {', '.join(all_cells_text[:7])}")
                    
                elif column_type == "contributor":
                    if len(cells) > 6:
                        contributor_cell = cells[6]
                        if expected_value.lower() in contributor_cell.text.lower():
                            found_matches += 1
                            
            except Exception as e:
                self.logger.debug(f"Could not check row {total_checked} for {column_type}: {e}")
                continue
        
        if found_matches > 0:
            self.logger.info(f"✅ Found {found_matches} matching results out of {total_checked} rows for {column_type}: {expected_value}")
            return True
        else:
            self.logger.warning(f"❌ No matching results found for {column_type}: {expected_value} (checked {total_checked} rows)")
            return False

    def find_data_type_selector(self, timeout=10):
        """Find the data type selector container"""
        return self.find_element(ExploreEphysLocators.DATA_TYPE_SELECTOR, timeout=timeout)

    def find_experimental_tab(self, timeout=10):
        """Find the Experimental tab"""
        try:
            return self.find_element(ExploreEphysLocators.EXPERIMENTAL_TAB, timeout=timeout)
        except TimeoutException:
            # Fallback to finding any Experimental tab (active or not)
            return self.find_element(ExploreEphysLocators.EXPERIMENTAL_TAB_ANY, timeout=timeout)

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
        missing_locators = []

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

    def lv_filter_apply(self):
        return self.find_element(ExploreEphysLocators.LV_FILTER_APPLY_BTN)

    def lv_row1(self):
        return self.find_element(ExploreEphysLocators.LV_ROW1)

    def click_random_row_with_pagination(self):
        """Navigate to a random page (if pagination exists) and click a random row.
        Returns the row text for logging.
        """
        import random
        from selenium.webdriver.common.action_chains import ActionChains

        # Check if pagination exists and pick a random page
        try:
            pages = self.browser.find_elements(*ExploreEphysLocators.PAGINATION_PAGES)
            if len(pages) > 1:
                target_page = random.choice(pages)
                page_num = target_page.get_attribute("title") or target_page.text.strip()
                # Skip if already on this page
                if 'ant-pagination-item-active' not in (target_page.get_attribute("class") or ""):
                    self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_page)
                    time.sleep(0.5)
                    target_page.click()
                    self.logger.info(f"Navigated to page {page_num}")
                    time.sleep(3)
                else:
                    self.logger.info(f"Already on page {page_num}")
        except Exception as e:
            self.logger.info(f"No pagination or single page: {e}")

        # Click a random row from the current page
        try:
            rows = self.find_all_elements(ExploreEphysLocators.TABLE_ROWS, timeout=10)
            if not rows:
                self.logger.warning("No table rows found, falling back to lv_row1")
                return self.lv_row1().click()

            row = random.choice(rows[:min(10, len(rows))])
            row_text = row.text.split('\n')[0][:60]
            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", row)
            time.sleep(0.5)
            try:
                ActionChains(self.browser).move_to_element(row).click().perform()
            except Exception:
                self.browser.execute_script("arguments[0].click();", row)
            self.logger.info(f"Clicked random row: '{row_text}...'")
            time.sleep(2)
            return row_text
        except Exception as e:
            self.logger.warning(f"Failed to click random row: {e}, falling back to row 1")
            self.lv_row1().click()
            return "row 1 (fallback)"

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

    def wait_for_page_ready(self, timeout=30):
        """Wait for the page to be ready"""
        WebDriverWait(self.browser, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        try:
            self.find_data_table_with_filters(timeout=timeout)
        except TimeoutException:
            # Fallback to legacy grid view
            self.find_explore_section_grid()

    def find_mini_detail_view(self, timeout=10):
        """Find the mini-detail view container"""
        return self.find_element(ExploreEphysLocators.MINI_DETAIL_VIEW, timeout=timeout)

    def verify_mini_detail_view_present(self):
        """Verify that the mini-detail view is displayed"""
        mini_view = self.find_mini_detail_view()
        assert mini_view.is_displayed(), "Mini-detail view should be displayed"
        self.logger.info("✅ Mini-detail view is displayed")
        return mini_view

    def get_mdv_name(self, timeout=10):
        """Get the name from mini-detail view"""
        element = self.find_element(ExploreEphysLocators.MDV_NAME, timeout=timeout)
        return element.text.strip()

    def get_mdv_description(self, timeout=10):
        """Get the description from mini-detail view"""
        element = self.find_element(ExploreEphysLocators.MDV_DESCRIPTION, timeout=timeout)
        return element.text.strip()

    def get_mdv_image(self, timeout=10):
        """Get the image element from mini-detail view"""
        return self.find_element(ExploreEphysLocators.MDV_IMAGE, timeout=timeout)

    def get_mdv_brain_region(self, timeout=10):
        """Get the brain region value from mini-detail view"""
        element = self.find_element(ExploreEphysLocators.MDV_BRAIN_REGION_VALUE, timeout=timeout)
        return element.text.strip()

    def get_mdv_etype(self, timeout=10):
        """Get the E-type value from mini-detail view"""
        element = self.find_element(ExploreEphysLocators.MDV_ETYPE_VALUE, timeout=timeout)
        return element.text.strip()

    def get_mdv_species(self, timeout=10):
        """Get the species value from mini-detail view"""
        element = self.find_element(ExploreEphysLocators.MDV_SPECIES_VALUE, timeout=timeout)
        return element.text.strip()

    def get_mdv_license(self, timeout=10):
        """Get the license element from mini-detail view (can be link or text)"""
        return self.find_element(ExploreEphysLocators.MDV_LICENSE_VALUE, timeout=timeout)

    def find_mdv_copy_button(self, timeout=10):
        """Find the Copy button in mini-detail view"""
        return self.find_element(ExploreEphysLocators.MDV_COPY_BUTTON, timeout=timeout)

    def find_mdv_download_button(self, timeout=10):
        """Find the Download button in mini-detail view"""
        return self.find_element(ExploreEphysLocators.MDV_DOWNLOAD_BUTTON, timeout=timeout)

    def find_mdv_view_details_button(self, timeout=10):
        """Find the View Details button in mini-detail view"""
        return self.find_element(ExploreEphysLocators.MDV_VIEW_DETAILS_BUTTON, timeout=timeout)

    def verify_mini_detail_view_fields(self):
        """Verify all fields in mini-detail view have values and are displayed"""
        results = {}
        
        try:
            name = self.get_mdv_name()
            results['name'] = {'present': True, 'has_value': bool(name), 'value': name}
            self.logger.info(f"✅ Name: '{name}'")
        except Exception as e:
            results['name'] = {'present': False, 'error': str(e)}
            self.logger.warning(f"❌ Name field error: {e}")
        
        try:
            description = self.get_mdv_description()
            results['description'] = {'present': True, 'has_value': bool(description), 'value': description[:50] + '...' if len(description) > 50 else description}
            self.logger.info(f"✅ Description: '{description[:50]}...'")
        except Exception as e:
            results['description'] = {'present': False, 'error': str(e)}
            self.logger.warning(f"❌ Description field error: {e}")
        
        try:
            image = self.get_mdv_image()
            is_displayed = image.is_displayed()
            src = image.get_attribute('src')
            results['image'] = {'present': True, 'displayed': is_displayed, 'has_src': bool(src)}
            self.logger.info(f"✅ Image: displayed={is_displayed}, has_src={bool(src)}")
        except Exception as e:
            results['image'] = {'present': False, 'error': str(e)}
            self.logger.warning(f"❌ Image field error: {e}")
        
        try:
            brain_region = self.get_mdv_brain_region()
            results['brain_region'] = {'present': True, 'has_value': bool(brain_region), 'value': brain_region}
            self.logger.info(f"✅ Brain Region: '{brain_region}'")
        except Exception as e:
            results['brain_region'] = {'present': False, 'error': str(e)}
            self.logger.warning(f"❌ Brain Region field error: {e}")
        
        try:
            etype = self.get_mdv_etype()
            results['etype'] = {'present': True, 'has_value': bool(etype) and etype != '—', 'value': etype}
            self.logger.info(f"✅ E-Type: '{etype}'")
        except Exception as e:
            results['etype'] = {'present': False, 'error': str(e)}
            self.logger.warning(f"❌ E-Type field error: {e}")
        
        try:
            species = self.get_mdv_species()
            results['species'] = {'present': True, 'has_value': bool(species), 'value': species}
            self.logger.info(f"✅ Species: '{species}'")
        except Exception as e:
            results['species'] = {'present': False, 'error': str(e)}
            self.logger.warning(f"❌ Species field error: {e}")
        
        try:
            license_element = self.get_mdv_license()
            is_displayed = license_element.is_displayed()
            license_text = license_element.text.strip()
            
            # Check if it's a link or just text (hyphen)
            try:
                # Try to find a link within the element
                license_link = license_element.find_element(By.TAG_NAME, 'a')
                href = license_link.get_attribute('href')
                is_clickable = bool(href)
            except:
                # No link found, it's just text (probably a hyphen)
                href = None
                is_clickable = False
            
            has_value = bool(license_text) and license_text != '—' and license_text != '-'
            results['license'] = {
                'present': True, 
                'displayed': is_displayed, 
                'has_value': has_value, 
                'value': license_text, 
                'clickable': is_clickable, 
                'href': href
            }
            self.logger.info(f"✅ License: '{license_text}' (clickable: {is_clickable})")
        except Exception as e:
            results['license'] = {'present': False, 'error': str(e)}
            self.logger.warning(f"❌ License field error: {e}")
        
        return results

    def verify_mini_detail_view_buttons(self):
        """Verify all buttons in mini-detail view are present and clickable"""
        results = {}
        
        try:
            copy_btn = self.find_mdv_copy_button()
            is_displayed = copy_btn.is_displayed()
            is_enabled = copy_btn.is_enabled()
            results['copy'] = {'present': True, 'displayed': is_displayed, 'clickable': is_enabled}
            self.logger.info(f"✅ Copy button: displayed={is_displayed}, clickable={is_enabled}")
        except Exception as e:
            results['copy'] = {'present': False, 'error': str(e)}
            self.logger.warning(f"❌ Copy button error: {e}")
        
        try:
            download_btn = self.find_mdv_download_button()
            is_displayed = download_btn.is_displayed()
            is_enabled = download_btn.is_enabled()
            results['download'] = {'present': True, 'displayed': is_displayed, 'clickable': is_enabled}
            self.logger.info(f"✅ Download button: displayed={is_displayed}, clickable={is_enabled}")
        except Exception as e:
            results['download'] = {'present': False, 'error': str(e)}
            self.logger.warning(f"❌ Download button error: {e}")
        
        try:
            view_details_btn = self.find_mdv_view_details_button()
            is_displayed = view_details_btn.is_displayed()
            href = view_details_btn.get_attribute('href')
            results['view_details'] = {'present': True, 'displayed': is_displayed, 'clickable': bool(href), 'href': href}
            self.logger.info(f"✅ View Details button: displayed={is_displayed}, clickable={bool(href)}")
        except Exception as e:
            results['view_details'] = {'present': False, 'error': str(e)}
            self.logger.warning(f"❌ View Details button error: {e}")
        
        return results

    def click_mdv_view_details(self):
        """Click the View Details button in mini-detail view"""
        view_details_btn = self.find_mdv_view_details_button()
        
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_details_btn)
        time.sleep(0.5)

        try:
            view_details_btn.click()
        except Exception as e:
            self.logger.warning(f"Regular click failed, using JavaScript click: {e}")
            self.browser.execute_script("arguments[0].click();", view_details_btn)
        
        self.logger.info("Clicked 'View Details' button")
        time.sleep(2)  # Wait for navigation
        return True

    def verify_detail_view_breadcrumbs(self):
        """Verify breadcrumbs are present and clickable"""
        results = {}
        breadcrumbs = [
            ('Data', ExploreEphysLocators.DV_BREADCRUMB_DATA),
            ('Experimental', ExploreEphysLocators.DV_BREADCRUMB_EXPERIMENTAL),
            ('Single cell electrophysiology', ExploreEphysLocators.DV_BREADCRUMB_SINGLE_CELL)
        ]
        
        for name, locator in breadcrumbs:
            try:
                element = self.find_element(locator, timeout=10)
                is_displayed = element.is_displayed()
                href = element.get_attribute('href')
                results[name] = {'present': True, 'displayed': is_displayed, 'clickable': bool(href)}
                self.logger.info(f"✅ Breadcrumb '{name}': displayed={is_displayed}, clickable={bool(href)}")
            except Exception as e:
                results[name] = {'present': False, 'error': str(e)}
                self.logger.warning(f"❌ Breadcrumb '{name}' error: {e}")
        
        return results

    def verify_detail_view_tabs(self):
        """Verify Overview tab is displayed and active"""
        results = {}
        
        try:
            overview_tab = self.find_element(ExploreEphysLocators.DV_OVERVIEW_TAB, timeout=10)
            is_displayed = overview_tab.is_displayed()
            # Check if tab is active by looking at parent label class
            parent = overview_tab.find_element(By.XPATH, "..")
            is_active = 'ant-radio-button-wrapper-checked' in parent.get_attribute('class')
            results['overview'] = {'present': True, 'displayed': is_displayed, 'active': is_active}
            self.logger.info(f"✅ Overview tab: displayed={is_displayed}, active={is_active}")
        except Exception as e:
            results['overview'] = {'present': False, 'error': str(e)}
            self.logger.warning(f"❌ Overview tab error: {e}")
        
        return results

    def verify_detail_view_buttons(self):
        """Verify Copy ID and Download buttons are present and clickable"""
        results = {}
        buttons = [
            ('Copy ID', ExploreEphysLocators.DV_COPY_ID_BUTTON),
            ('Download', ExploreEphysLocators.DV_DOWNLOAD_BUTTON)
        ]
        
        for name, locator in buttons:
            try:
                element = self.find_element(locator, timeout=10)
                is_displayed = element.is_displayed()
                # Check if element or parent is clickable
                is_clickable = element.is_enabled()
                results[name] = {'present': True, 'displayed': is_displayed, 'clickable': is_clickable}
                self.logger.info(f"✅ Button '{name}': displayed={is_displayed}, clickable={is_clickable}")
            except Exception as e:
                results[name] = {'present': False, 'error': str(e)}
                self.logger.warning(f"❌ Button '{name}' error: {e}")
        
        return results

    def verify_detail_view_main_fields(self):
        """Verify main detail view fields"""
        results = {}
        required_fields = [
            ('Name', ExploreEphysLocators.DV_NAME_VALUE),
            ('Created by', ExploreEphysLocators.DV_CREATED_BY_VALUE),
            ('Registration date', ExploreEphysLocators.DV_REGISTRATION_DATE_VALUE),
            ('Brain Region', ExploreEphysLocators.DV_BRAIN_REGION_VALUE)
        ]
        
        # Fields that may not have values
        optional_fields = [
            ('Description', ExploreEphysLocators.DV_DESCRIPTION_VALUE),
            ('Contributors', ExploreEphysLocators.DV_CONTRIBUTORS_VALUE),
            ('Institutional Contributors', ExploreEphysLocators.DV_INSTITUTIONAL_CONTRIBUTORS_VALUE),
            ('E-Type', ExploreEphysLocators.DV_ETYPE_VALUE)
        ]
        
        for name, locator in required_fields:
            try:
                element = self.find_element(locator, timeout=10)
                value = element.text.strip()
                has_value = bool(value) and value != '—'
                results[name] = {'present': True, 'has_value': has_value, 'value': value[:50] if len(value) > 50 else value}
                if has_value:
                    self.logger.info(f"✅ {name}: '{value[:50]}...' (required)")
                else:
                    self.logger.warning(f"⚠️ {name}: No value (required field)")
            except Exception as e:
                results[name] = {'present': False, 'error': str(e)}
                self.logger.warning(f"❌ {name} error: {e}")
        
        for name, locator in optional_fields:
            try:
                element = self.find_element(locator, timeout=10)
                value = element.text.strip()
                has_value = bool(value) and value != '—'
                results[name] = {'present': True, 'has_value': has_value, 'value': value[:50] if len(value) > 50 else value}
                if has_value:
                    self.logger.info(f"✅ {name}: '{value[:50]}...' (optional)")
                else:
                    self.logger.info(f"ℹ️ {name}: No value (optional field)")
            except Exception as e:
                results[name] = {'present': False, 'error': str(e)}
                self.logger.warning(f"❌ {name} error: {e}")
        
        try:
            license_element = self.find_element(ExploreEphysLocators.DV_LICENSE_LINK, timeout=10)
            value = license_element.text.strip()
            
            # Check if it's a link or just text (hyphen)
            try:
                # Try to find a link within the element
                license_link = license_element.find_element(By.TAG_NAME, 'a')
                href = license_link.get_attribute('href')
                is_clickable = bool(href)
            except:
                # No link found, it's just text (probably a hyphen)
                href = None
                is_clickable = False
            
            has_value = bool(value) and value != '—' and value != '-'
            results['License'] = {
                'present': True, 
                'has_value': has_value, 
                'value': value, 
                'clickable': is_clickable, 
                'href': href
            }
            self.logger.info(f"✅ License: '{value}' (clickable: {is_clickable})")
        except Exception as e:
            results['License'] = {'present': False, 'error': str(e)}
            self.logger.warning(f"❌ License error: {e}")
        
        return results

    def verify_detail_view_subject_fields(self):
        """Verify Subject section fields"""
        results = {}
        
        try:
            subject_header = self.find_element(ExploreEphysLocators.DV_SUBJECT_HEADER, timeout=10)
            results['Subject Header'] = {'present': True, 'displayed': subject_header.is_displayed()}
            self.logger.info("✅ Subject section header is present")
        except Exception as e:
            results['Subject Header'] = {'present': False, 'error': str(e)}
            self.logger.warning(f"❌ Subject header error: {e}")
            return results  # If header not found, skip field checks
        
        # All subject fields (all optional)
        subject_fields = [
            ('Name', ExploreEphysLocators.DV_SUBJECT_NAME_VALUE),
            ('Description', ExploreEphysLocators.DV_SUBJECT_DESCRIPTION_VALUE),
            ('Species', ExploreEphysLocators.DV_SUBJECT_SPECIES_VALUE),
            ('Strain', ExploreEphysLocators.DV_SUBJECT_STRAIN_VALUE),
            ('Sex', ExploreEphysLocators.DV_SUBJECT_SEX_VALUE),
            ('Weight', ExploreEphysLocators.DV_SUBJECT_WEIGHT_VALUE),
            ('Age', ExploreEphysLocators.DV_SUBJECT_AGE_VALUE),
            ('Age min', ExploreEphysLocators.DV_SUBJECT_AGE_MIN_VALUE),
            ('Age max', ExploreEphysLocators.DV_SUBJECT_AGE_MAX_VALUE),
            ('Age period', ExploreEphysLocators.DV_SUBJECT_AGE_PERIOD_VALUE)
        ]
        
        for name, locator in subject_fields:
            try:
                element = self.find_element(locator, timeout=5)
                value = element.text.strip()
                has_value = bool(value) and value != '—'
                results[f'Subject {name}'] = {'present': True, 'has_value': has_value, 'value': value}
                if has_value:
                    self.logger.info(f"✅ Subject {name}: '{value}'")
                else:
                    self.logger.info(f"ℹ️ Subject {name}: No value")
            except Exception as e:
                results[f'Subject {name}'] = {'present': False, 'error': str(e)}
                self.logger.debug(f"Subject {name} not found: {e}")
        
        return results

    def find_overview_tab(self, timeout=10):
        """Find the Overview tab button"""
        return self.find_element(ExploreEphysLocators.DV_OVERVIEW_TAB_BUTTON, timeout=timeout)

    def find_interactive_details_tab(self, timeout=10):
        """Find the Interactive Details tab button"""
        return self.find_element(ExploreEphysLocators.DV_INTERACTIVE_DETAILS_TAB_BUTTON, timeout=timeout)

    def is_overview_tab_active(self):
        """Check if Overview tab is active"""
        try:
            self.find_element(ExploreEphysLocators.DV_OVERVIEW_TAB_ACTIVE, timeout=5)
            return True
        except TimeoutException:
            return False

    def is_interactive_details_tab_active(self):
        """Check if Interactive Details tab is active"""
        try:
            self.find_element(ExploreEphysLocators.DV_INTERACTIVE_DETAILS_TAB_ACTIVE, timeout=5)
            return True
        except TimeoutException:
            return False

    def click_overview_tab(self):
        """Click the Overview tab"""
        overview_tab = self.find_overview_tab()
        
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", overview_tab)
        time.sleep(0.5)
        
        try:
            overview_tab.click()
        except Exception as e:
            self.logger.warning(f"Regular click failed, using JavaScript click: {e}")
            self.browser.execute_script("arguments[0].click();", overview_tab)
        
        self.logger.info("Clicked Overview tab")
        time.sleep(1)
        return True

    def click_interactive_details_tab(self):
        """Click the Interactive Details tab"""
        interactive_tab = self.find_interactive_details_tab()
        
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", interactive_tab)
        time.sleep(0.5)
        
        try:
            interactive_tab.click()
        except Exception as e:
            self.logger.warning(f"Regular click failed, using JavaScript click: {e}")
            self.browser.execute_script("arguments[0].click();", interactive_tab)
        
        self.logger.info("Clicked Interactive Details tab")
        time.sleep(1)
        return True

    def find_overview_plots(self, timeout=30):
        """Find all plots in Overview tab. Scrolls containers to trigger lazy loading."""
        # Try scrolling various containers to trigger lazy-loaded plots
        try:
            # Scroll the main content area and any scrollable parent
            scrollable = self.browser.find_elements(By.CSS_SELECTOR,
                "div[class*='overflow-y-auto'], div[class*='overflow-auto']")
            for container in scrollable[:3]:
                self.browser.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight / 3;", container)
            time.sleep(2)
            for container in scrollable[:3]:
                self.browser.execute_script("arguments[0].scrollTop = 0;", container)
            time.sleep(1)
        except Exception:
            pass

        try:
            # Primary: plotly container
            plots = self.browser.find_elements(By.CSS_SELECTOR, "div.plot-container.plotly")
            if plots:
                visible = [p for p in plots if p.is_displayed()]
                self.logger.info(f"Found {len(visible)} visible overview plots (plotly)")
                return visible if visible else plots

            # Fallback: js-plotly-plot
            plots = self.browser.find_elements(By.CSS_SELECTOR, "div.js-plotly-plot")
            if plots:
                self.logger.info(f"Found {len(plots)} overview plots (js-plotly-plot)")
                return plots

            # Fallback: SVG main-svg (plotly renders SVGs)
            plots = self.browser.find_elements(By.CSS_SELECTOR, "svg.main-svg")
            if plots:
                self.logger.info(f"Found {len(plots)} overview plots (svg.main-svg)")
                return plots

            # Last resort: wait with explicit wait
            plots = self.find_all_elements(ExploreEphysLocators.DV_OVERVIEW_PLOTS, timeout=timeout)
            return plots
        except TimeoutException:
            self.logger.warning("No overview plots found")
            return []

    def verify_plot_interactions(self):
        """Verify plot interaction controls are available"""
        results = {}
        
        try:
            plots = self.find_overview_plots()
            if plots:
                first_plot = plots[0]
                self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_plot)
                time.sleep(0.5)
                
                # Move mouse to plot to trigger modebar
                from selenium.webdriver.common.action_chains import ActionChains
                actions = ActionChains(self.browser)
                actions.move_to_element(first_plot).perform()
                time.sleep(1)
                
                # Check for modebar
                try:
                    modebar = self.find_element(ExploreEphysLocators.DV_PLOT_MODEBAR, timeout=3)
                    results['modebar_present'] = True
                    
                    # Check for specific controls
                    controls = [
                        ('zoom', ExploreEphysLocators.DV_PLOT_ZOOM_BUTTON),
                        ('pan', ExploreEphysLocators.DV_PLOT_PAN_BUTTON),
                        ('reset', ExploreEphysLocators.DV_PLOT_RESET_BUTTON),
                        ('download', ExploreEphysLocators.DV_PLOT_DOWNLOAD_BUTTON)
                    ]
                    
                    for control_name, locator in controls:
                        try:
                            self.find_element(locator, timeout=2)
                            results[f'{control_name}_available'] = True
                        except TimeoutException:
                            results[f'{control_name}_available'] = False
                
                except TimeoutException:
                    results['modebar_present'] = False
            else:
                results['no_plots'] = True
        
        except Exception as e:
            results['error'] = str(e)
            self.logger.debug(f"Error testing plot interactions: {e}")
        
        return results

    def find_interactive_plots(self):
        """Find all plots in Interactive Details tab"""
        try:
            plots = self.find_all_elements(ExploreEphysLocators.DV_INTERACTIVE_PLOTS)
            return plots
        except TimeoutException:
            self.logger.warning("No interactive plots found")
            return []

    def verify_interactive_controls(self):
        """Verify interactive controls are present"""
        results = {}
        
        try:
            stimulus_selector = self.find_element(ExploreEphysLocators.DV_STIMULUS_SELECTOR, timeout=10)
            results['stimulus_selector'] = stimulus_selector.is_displayed()
        except TimeoutException:
            results['stimulus_selector'] = False
        
        try:
            repetition_label = self.find_element(ExploreEphysLocators.DV_REPETITION_LABEL, timeout=5)
            results['repetition_selector'] = repetition_label.is_displayed()
        except TimeoutException:
            results['repetition_selector'] = False
        
        try:
            sweep_label = self.find_element(ExploreEphysLocators.DV_SWEEP_LABEL, timeout=5)
            results['sweep_selector'] = sweep_label.is_displayed()
        except TimeoutException:
            results['sweep_selector'] = False
        
        return results



    def click_sweep_color_and_verify(self):
        """Click a random unselected sweep color checkbox and verify the plot updates.
        Returns dict: {'clicked': bool, 'sweep_value': str, 'plot_visible': bool}.
        """
        from selenium.webdriver.common.action_chains import ActionChains
        results = {'clicked': False, 'sweep_value': '', 'plot_visible': False}

        try:
            labels = self.browser.find_elements(*ExploreEphysLocators.DV_SWEEP_LABELS)
            if not labels:
                self.logger.warning("No sweep color labels found")
                return results

            # Pick a random unselected one
            import random
            unselected = [l for l in labels if 'selected' not in (l.find_element(By.XPATH, "..").get_attribute("class") or "")]
            target = random.choice(unselected) if unselected else random.choice(labels)

            bg_color = target.get_attribute("style") or ""
            sweep_input = target.find_element(By.CSS_SELECTOR, "input")
            results['sweep_value'] = sweep_input.get_attribute("value") or ""

            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", target)
            time.sleep(0.5)
            try:
                ActionChains(self.browser).move_to_element(target).click().perform()
            except Exception:
                self.browser.execute_script("arguments[0].click();", target)
            results['clicked'] = True
            self.logger.info(f"Clicked sweep: '{results['sweep_value']}', color: {bg_color[:40]}")
            time.sleep(2)

            # Verify plot area is still visible
            try:
                plot = self.browser.find_element(By.CSS_SELECTOR, "rect.nsewdrag")
                results['plot_visible'] = plot.is_displayed()
            except Exception:
                pass

        except Exception as e:
            self.logger.warning(f"Error clicking sweep: {e}")

        return results

    def click_reset_and_verify(self):
        """Click the Reset button and verify Protocol/Repetition/Sweep controls reappear.
        Returns dict: {'reset_clicked': bool, 'protocol_visible': bool, 'repetition_visible': bool, 'sweep_visible': bool, 'plots_visible': bool}.
        """
        results = {'reset_clicked': False, 'protocol_visible': False, 'repetition_visible': False, 'sweep_visible': False, 'plots_visible': False}

        try:
            reset_btn = self.element_to_be_clickable(ExploreEphysLocators.DV_RESET_BUTTON, timeout=10)
            reset_btn.click()
            results['reset_clicked'] = True
            self.logger.info("Clicked Reset button")
            time.sleep(3)

            # Verify controls reappear
            try:
                self.find_element(ExploreEphysLocators.DV_PROTOCOL_DROPDOWN, timeout=5)
                results['protocol_visible'] = True
            except Exception:
                pass
            try:
                self.find_element(ExploreEphysLocators.DV_REPETITION_DROPDOWN, timeout=5)
                results['repetition_visible'] = True
            except Exception:
                pass
            try:
                labels = self.browser.find_elements(*ExploreEphysLocators.DV_SWEEP_LABELS)
                results['sweep_visible'] = len(labels) > 0
            except Exception:
                pass
            try:
                plots = self.browser.find_elements(By.CSS_SELECTOR, "div.js-plotly-plot")
                results['plots_visible'] = any(p.is_displayed() for p in plots)
            except Exception:
                pass

        except TimeoutException:
            self.logger.warning("Reset button not found")

        return results

    def toggle_unit_to_na_and_verify(self):
        """Click the nA unit toggle and verify the Y-axis values change.
        Returns dict: {'toggled': bool, 'values_changed': bool, 'before': list, 'after': list}.
        """
        from selenium.webdriver.common.action_chains import ActionChains
        results = {'toggled': False, 'values_changed': False, 'before': [], 'after': []}

        try:
            # Capture Y-axis tick values before toggle
            yticks_before = self.browser.find_elements(*ExploreEphysLocators.DV_PLOT_YTICK_VALUES)
            results['before'] = [t.text.strip() for t in yticks_before if t.text.strip()]
            self.logger.info(f"Y-axis values before nA toggle: {results['before']}")

            # Click nA radio button label
            na_btn = self.find_element(ExploreEphysLocators.DV_UNIT_TOGGLE_NA, timeout=10)
            # Click the parent label wrapper to trigger the radio change
            na_label = na_btn.find_element(By.XPATH, "./ancestor::label")
            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", na_label)
            time.sleep(0.5)
            try:
                ActionChains(self.browser).move_to_element(na_label).click().perform()
            except Exception:
                self.browser.execute_script("arguments[0].click();", na_label)
            results['toggled'] = True
            self.logger.info("Clicked nA unit toggle")
            time.sleep(2)

            # Capture Y-axis tick values after toggle
            yticks_after = self.browser.find_elements(*ExploreEphysLocators.DV_PLOT_YTICK_VALUES)
            results['after'] = [t.text.strip() for t in yticks_after if t.text.strip()]
            self.logger.info(f"Y-axis values after nA toggle: {results['after']}")

            # Values should be different after toggling units
            results['values_changed'] = results['before'] != results['after']
            if results['values_changed']:
                self.logger.info("Y-axis values changed after nA toggle")
            else:
                self.logger.warning("Y-axis values did NOT change after nA toggle")

        except TimeoutException:
            self.logger.warning("nA toggle button not found")
        except Exception as e:
            self.logger.warning(f"Error toggling nA unit: {e}")

        return results

    def test_stimulus_selector(self):
        """Test stimulus selector functionality"""
        try:
            stimulus_selector = self.find_element(ExploreEphysLocators.DV_STIMULUS_SELECTOR, timeout=10)
            stimulus_selector.click()
            self.logger.info("Clicked stimulus selector")
            time.sleep(1)
            
            try:
                dropdown_options = self.find_all_elements(ExploreEphysLocators.DV_STIMULUS_DROPDOWN)
                if dropdown_options:
                    self.logger.info(f"Found {len(dropdown_options)} stimulus options")
                    
                    # Try to select "All" option if available
                    try:
                        all_option = self.find_element(ExploreEphysLocators.DV_STIMULUS_ALL_OPTION, timeout=3)
                        all_option.click()
                        self.logger.info("Selected 'All' stimulus option")
                        time.sleep(2)
                        return True
                    except TimeoutException:
                        # Click first option if "All" not found
                        if dropdown_options:
                            dropdown_options[0].click()
                            self.logger.info("Selected first stimulus option")
                            time.sleep(2)
                            return True
                else:
                    return False
            except TimeoutException:
                return False
        
        except Exception as e:
            self.logger.debug(f"Error testing stimulus selector: {e}")
            return False
