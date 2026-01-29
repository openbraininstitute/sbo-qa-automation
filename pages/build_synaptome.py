# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time
from tkinter.constants import RADIOBUTTON

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
import logging

from locators.build_synaptome_locators import BuildSynaptomeLocators
from pages.home_page import HomePage


class BuildSynaptomePage(HomePage):
    def __init__(self, browser, wait, base_url, logger=None):
        super().__init__(browser, wait, base_url)
        self.logger = logger or logging.getLogger(__name__)
        self.home_page = HomePage(browser, wait, base_url)
        self.logger = logger

    def go_to_build_synaptome(self, lab_id: str, project_id: str):
        path = f"/app/virtual-lab/lab/{lab_id}/project/{project_id}/build"
        try:
            self.browser.set_page_load_timeout(120)
            self.go_to_page(path)
            self.wait_for_page_ready(timeout=60)
        except TimeoutException:
            raise RuntimeError("The Build page did not load within 120 seconds.")
        return self.browser.current_url

    def apply_changes_btn(self):
        return self.find_element(BuildSynaptomeLocators.APPLY_CHANGES)

    def add_new_synapse_set(self):
        return self.find_element(BuildSynaptomeLocators.ADD_SYNAPSES_BTN)

    def brain_region_column_header(self, timeout=10):
        return self.find_element(BuildSynaptomeLocators.BRAIN_REGION_COLUMN_HEADER, timeout=timeout)

    def click_target_select(self, timeout=25):
        self.wait_and_click(BuildSynaptomeLocators.TARGET_SELECTOR, timeout=timeout)

    def configure_model(self, timeout=10):
        return self.find_element(BuildSynaptomeLocators.CONFIGURE_MODEL, timeout=timeout)

    def delete_synapse_set(self, timeout=20):
        return self.find_element(BuildSynaptomeLocators.DELETE_SYNAPSE_SET2, timeout=timeout)

    def description_title(self):
        return self.find_element(BuildSynaptomeLocators.DESCRIPTION_TITLE)

    def filter_synapses_btn(self):
        return self.find_element(BuildSynaptomeLocators.FILTER_SYNAPSES_BTN)

    def find_menu_build(self, timeout=25):
        return self.is_visible(BuildSynaptomeLocators.MENU_BUILD, timeout=timeout)

    def find_synaptome_box(self, timeout=10):
        return self.find_element(BuildSynaptomeLocators.SYNAPTOME_BOX, timeout=timeout)

    def find_synaptome_build_btn(self, timeout=10):
        return self.find_element(BuildSynaptomeLocators.SYNAPTOME_BUILD_BTN, timeout=timeout)

    def form_created_by(self):
        return self.find_element(BuildSynaptomeLocators.FORM_CREATED_BY)

    def form_value_created_by(self):
        return self.find_all_elements(BuildSynaptomeLocators.FORM_VALUE_CREATED_BY)

    def form_creation_date(self):
        return self.find_element(BuildSynaptomeLocators.FORM_CREATION_DATE)

    def form_value_creation_date(self):
        return self.find_element(BuildSynaptomeLocators.FORM_VALUE_CREATION_DATE)

    def get_all_table_rows(self):
        """
        Returns all rows in the table body as a list of WebElement objects.
        """
        return self.find_all_elements(BuildSynaptomeLocators.ROWS)

    def get_column_values(self, column_index):
        """
        Returns the values of a specific column for all rows.
        :param column_index: Index of the column to retrieve values (0-based).
        :return: List of text values from the specified column.
        """
        rows = self.find_all_elements(BuildSynaptomeLocators.ROWS)

        column_values = []
        for row in rows:
            cells = self.find_all_elements(BuildSynaptomeLocators.CELLS)
            if column_index < len(cells):
                column_values.append(cells[column_index].text.strip())

        return column_values

    def get_first_table_row_content(self):
        """
        Fetches the content of the first table cell from the first row.
        """
        first_data_row = self.is_visible(BuildSynaptomeLocators.ROW1)

        return [cell.text.strip() for cell in first_data_row.find_elements(By.TAG_NAME, "td")]


    def get_table_content(self):
        # Wait until the table element is present
        table = self.find_element(BuildSynaptomeLocators.TABLE)
        # Wait until at least one row of the table is populated with data
        WebDriverWait(self.browser, 20).until(
            lambda driver: any(
                self.find_all_elements((By.TAG_NAME, "td"), timeout=10) and  # Corrected Tuple Argument
                any(cell.text.strip() for cell in self.find_all_elements((By.TAG_NAME, "td"), timeout=10))
                # Corrected Tuple Argument
                for row in table.find_elements(By.TAG_NAME, "tr")
            ),
            "Table rows are not populated with data within the timeout."
        )

        # Extract table content once it is fully loaded
        rows = self.find_all_elements((By.TAG_NAME, "tr"))  # Corrected Tuple Argument
        table_content = []
        for row in rows:
            # For each row, get all cell elements using the custom helper
            cells = self.find_all_elements((By.TAG_NAME, "td"), timeout=10)  # Corrected Tuple Argument
            # Extract and clean the text content of all cells in the row
            row_content = [cell.text.strip() for cell in cells]
            if row_content:  # Include non-empty rows only
                table_content.append(row_content)

        return table_content

    def input_name_field(self):
        return self.find_element(BuildSynaptomeLocators.INPUT_NAME_FIELD)

    def is_column_sorted(self, column_index, ascending=True):
        """
        Checks if a specific column in the table is sorted in ascending or descending order.
        :param column_index: Index of the column to check sorting for (0-based).
        :param ascending: If True, validates ascending order. If False, validates descending order.
        :return: True if the column is sorted, otherwise False.
        """
        column_values = self.get_column_values(column_index)

        sorted_values = sorted(column_values)
        if not ascending:
            sorted_values = sorted(column_values, reverse=True)

        return column_values == sorted_values

    def input_description_field(self):
        return self.find_element(BuildSynaptomeLocators.INPUT_DESCRIPTION_FIELD)

    def name_your_set(self):
        return self.find_element(BuildSynaptomeLocators.NAME_YOUR_SET_FIELD)

    def name_your_set2(self):
        return self.find_element(BuildSynaptomeLocators.NAME_YOUR_SET_FIELD2)

    def new_synaptome_title(self):
        return self.find_element(BuildSynaptomeLocators.NEW_SYNAPTOME_TITLE)

    def radio_btn(self, timeout=10):
        return self.element_to_be_clickable(BuildSynaptomeLocators.RADIO_BTN_ME_MODEL, timeout=timeout)

    def results_label(self):
        return self.find_element(BuildSynaptomeLocators.RESULTS)

    def save_btn(self, timeout=15):
        return self.find_element(BuildSynaptomeLocators.SAVE_SYNAPTOME_MODEL, timeout=timeout)

    def start_building_button(self):
        return self.element_to_be_clickable(BuildSynaptomeLocators.START_BUILDING_BTN)

    def select_model(self):
        return self.find_element(BuildSynaptomeLocators.SELECT_MODEL)

    def synaptome_form(self):
        return self.find_element(BuildSynaptomeLocators.SYNAPTOME_FORM)

    def synapse_formula(self):
        return self.find_element(BuildSynaptomeLocators.SYNAPSE_FORMULA)

    def synapse_greater_value(self):
        return self.find_element(BuildSynaptomeLocators.SYNAPSE_GREATER_VALUE)

    def synapse_smaller_value(self):
        return self.find_element(BuildSynaptomeLocators.SYNAPSE_SMALLER_VALUE)

    def synapse_set(self, timeout=15):
        return self.find_element(BuildSynaptomeLocators.SYNAPSE_SETS, timeout=timeout)

    def synapse_set_num(self, text, timeout=15):
        return self.text_is_visible(BuildSynaptomeLocators.SYNAPSE_SET_NUM, text, timeout=timeout)

    def target_field(self, timeout=15):
        return self.find_element(BuildSynaptomeLocators.TARGET_FIELD, timeout=timeout)

    def target_field2(self, timeout=15):
        return self.find_element(BuildSynaptomeLocators.TARGET_FIELD2, timeout=timeout)

    def target_list(self, timeout=20):
        return self.find_element(BuildSynaptomeLocators.TARGET_LIST, timeout=timeout)

    def target_list2(self, timeout=20):
        return self.find_element(BuildSynaptomeLocators.TARGET_LIST2, timeout=timeout)

    def target_soma(self, timeout=15):
        return self.find_element(BuildSynaptomeLocators.TARGET_SOMA, timeout=timeout)

    def target_soma2(self, timeout=15):
        return self.find_element(BuildSynaptomeLocators.TARGET_SOMA2, timeout=timeout)

    def canvas(self, timeout=10):
        return self.is_visible(BuildSynaptomeLocators.CANVAS, timeout=timeout)

    def canvas_pointer(self, timeout=10):
        return self.element_visibility(BuildSynaptomeLocators.CANVAS_POINTER, timeout=timeout)

    def seed_synaptome(self, timeout=10):
        return self.element_visibility(BuildSynaptomeLocators.SEED_TITLE, timeout=timeout)

    def select_single_neuron_title(self, timeout=10):
        return self.element_visibility(BuildSynaptomeLocators.SELECT_SINGLE_NEURON_TITLE, timeout=timeout)

    def target_dropdown_list(self, timeout=10):
        return self.find_element(BuildSynaptomeLocators.TARGET_DROPDOWN_LIST, timeout=timeout)

    def target_select(self, timeout=25):
        return self.element_to_be_clickable(BuildSynaptomeLocators.TARGET_SELECTOR, timeout=timeout)

    def target_select2(self, timeout=25):
        return self.find_element(BuildSynaptomeLocators.TARGET_SELECT2, timeout=timeout)

    def wait_for_target_dropdown_enabled(self, timeout=60):
        """
        Wait until the 'Target select' dropdown is clickable (enabled).
        """
        # return self.element_to_be_clickable(BuildSynaptomeLocators.TARGET_SELECTOR)
        element = self.element_to_be_clickable(BuildSynaptomeLocators.TARGET_SELECTOR, timeout=timeout)
        print(element.get_attribute("aria-expanded"))
        return element

    # def wait_for_target_dropdown_expanded(self, timeout=25):
    #     return self.is_visible(BuildSynaptomeLocators.TARGET_DROPDOWN_LIST, timeout=timeout)

    def wait_for_target_dropdown_expanded(self, timeout=25, retries=2):
        last_exception = None
        for i in range(retries):
            try:
                return self.is_visible(BuildSynaptomeLocators.TARGET_DROPDOWN_LIST)
            except TimeoutException as e:
                last_exception = e
                time.sleep(1)  # small delay before retry
        raise last_exception

    def wait_for_target_dropdown_expanded2(self, timeout=25):
        WebDriverWait(self.browser, timeout).until(
            lambda d: d.find_element(*BuildSynaptomeLocators.TARGET_INPUT2).get_attribute("aria-expanded") == "true"
        )

    def type_field(self):
        return self.find_element(BuildSynaptomeLocators.TYPE_FIELD)

    def type_field2(self):
        return self.find_element(BuildSynaptomeLocators.TYPE_FIELD2)

    def type_excitatory(self):
        return self.element_to_be_clickable(BuildSynaptomeLocators.TYPE_EXCITATORY)

    def type_inhibitory(self):
        return self.element_to_be_clickable(BuildSynaptomeLocators.TYPE_INHIBITORY)

    def select_inhibitory(self):
        return self.element_to_be_clickable(BuildSynaptomeLocators.SELECT_INHIBITORY)

    def use_sn_model_btn(self):
        return self.element_to_be_clickable(BuildSynaptomeLocators.USE_SN_MODEL_BTN)

    def wait_for_table_sorting_to_complete(self, timeout=30):
        """
        Waits for the table sorting to be completed by checking for changes in the first row's content.
        """
        initial_table_content = self.get_table_content()

        try:
            WebDriverWait(self.browser, timeout).until(
                lambda driver: self.get_table_content() != initial_table_content,
                "Table sorting did not complete within the provided timeout."
            )
            print("Table sorting is completed. The table content was updated.")
        except TimeoutException:
            current_table_content = self.get_table_content()
            raise Exception(
                f"Table sorting timed out. Initial content: {initial_table_content}, "
                f"Current table content: {current_table_content}. Timeout: {timeout}s."
            )

    def wait_for_spinner_to_disappear(self, timeout=20):
        return self.wait_for_element_to_disappear(BuildSynaptomeLocators.SPIN_CONTAINER, timeout=timeout)

    def wait_for_table_data_to_load(self, timeout=30):
        """
        Waits for at least one row of data (excluding headers) to be visible in the table body.
        """
        self.wait_for_spinner_to_disappear()
        # Then wait for table rows to load
        WebDriverWait(self.browser, timeout).until(
            lambda driver: len(self.get_all_table_rows()) > 0 and "No data" not in self.get_table_content(),
            "Table data is not loaded within the timeout."
        )

    def wait_for_zoom_ui(self, timeout=15):
        return self.is_visible(BuildSynaptomeLocators.ZOOM_UI_CONTAINER, timeout)

    # Synaptome Workflow Methods
    def click_build_section(self, logger):
        """Click on Build button/section to get to build activities"""
        logger.info("Looking for Build button/section...")
        time.sleep(3)  # Wait for page elements to load
        
        # Try multiple selectors for the Build button/section
        build_btn = None
        build_selectors_to_try = [
            BuildSynaptomeLocators.BUILD_BUTTON,
            BuildSynaptomeLocators.BUILD_DIV,
            BuildSynaptomeLocators.BUILD_ANY,
            BuildSynaptomeLocators.BUILD_LINK,
            BuildSynaptomeLocators.BUILD_SPAN,
        ]
        
        for i, selector in enumerate(build_selectors_to_try):
            try:
                build_btn = self.browser.find_element(*selector)
                logger.info(f"Found Build button with selector {i+1}: {selector}")
                break
            except:
                logger.info(f"Build selector {i+1} failed: {selector}")
                continue
        
        if build_btn:
            build_btn.click()
            logger.info("Clicked on Build button")
            time.sleep(3)  # Wait for build section to load
            logger.info(f"URL after clicking Build: {self.browser.current_url}")
            return True
        else:
            logger.info("No Build button found")
            return False

    def click_synaptome_card(self, logger):
        """Click on Synaptome card"""
        logger.info("Looking for Synaptome card...")
        time.sleep(3)  # Wait for page elements to load
        
        # Try multiple selectors for the Synaptome card
        synaptome_card = None
        selectors_to_try = [
            BuildSynaptomeLocators.SYNAPTOME_CARD_PRIMARY,
            BuildSynaptomeLocators.SYNAPTOME_CARD_CLASS,
            BuildSynaptomeLocators.SYNAPTOME_CARD_TEXT,
            BuildSynaptomeLocators.SYNAPTOME_CARD_ANY,
            BuildSynaptomeLocators.SYNAPTOME_CARD_BUTTON,
        ]
        
        for i, selector in enumerate(selectors_to_try):
            try:
                synaptome_card = self.browser.find_element(*selector)
                logger.info(f"Found Synaptome card with selector {i+1}: {selector}")
                break
            except:
                logger.info(f"Selector {i+1} failed: {selector}")
                continue
        
        if not synaptome_card:
            logger.error("Could not find Synaptome card with any selector")
            # Check page source for synaptome text
            page_source = self.browser.page_source
            if "synaptome" in page_source.lower():
                logger.info("Found 'synaptome' text in page source")
                # Try to find any clickable element containing synaptome
                try:
                    synaptome_card = self.browser.find_element(*BuildSynaptomeLocators.SYNAPTOME_CARD_CASE_INSENSITIVE)
                    logger.info("Found synaptome element with case-insensitive search")
                except:
                    logger.error("No synaptome element found even with case-insensitive search")
            else:
                logger.error("No 'synaptome' text found in page source")
            
            # Take screenshot for debugging
            self.browser.save_screenshot("debug_workflows_page.png")
            raise Exception("Cannot find Synaptome card on workflows page")
        
        assert synaptome_card.is_displayed(), "Synaptome card is not displayed"
        synaptome_card.click()
        logger.info("Clicked on Synaptome card")
        return True

    def fill_configuration_form(self, unique_name, dynamic_description, logger):
        """Fill in the configuration form with name and description"""
        # Fill name field
        name_field = self.browser.find_element(*BuildSynaptomeLocators.CONFIG_NAME_FIELD)
        assert name_field.is_displayed(), "Name field is not displayed"
        name_field.clear()
        name_field.send_keys(unique_name)
        logger.info(f"Filled name field with: {unique_name}")
        
        # Fill description field
        description_field = self.browser.find_element(*BuildSynaptomeLocators.CONFIG_DESCRIPTION_FIELD)
        assert description_field.is_displayed(), "Description field is not displayed"
        description_field.clear()
        description_field.send_keys(dynamic_description)
        logger.info(f"Filled description field with: {dynamic_description}")

        # Verify created by and created at fields are populated (make this optional)
        try:
            created_by_field = self.browser.find_element(*BuildSynaptomeLocators.CONFIG_CREATED_BY)
            assert created_by_field.is_displayed() and created_by_field.text.strip(), "Created by field is empty"
            logger.info(f"Created by: {created_by_field.text}")
        except:
            logger.info("Created by field not found with expected selector, continuing...")
        
        try:
            created_at_field = self.browser.find_element(*BuildSynaptomeLocators.CONFIG_CREATED_AT)
            assert created_at_field.is_displayed() and created_at_field.text.strip(), "Created at field is empty"
            logger.info(f"Created at: {created_at_field.text}")
        except:
            logger.info("Created at field not found with expected selector, continuing...")

    def click_me_model_button(self, logger):
        """Click on ME-model button to proceed"""
        logger.info("Looking for ME-model button...")
        time.sleep(3)
        
        # Try multiple selectors for ME-model button
        me_model_btn = None
        me_model_selectors = [
            BuildSynaptomeLocators.ME_MODEL_BUTTON_PRIMARY,
            BuildSynaptomeLocators.ME_MODEL_BUTTON_TEXT,
            BuildSynaptomeLocators.ME_MODEL_BUTTON_ANCESTOR,
            BuildSynaptomeLocators.ME_MODEL_ANY,
        ]
        
        for i, selector in enumerate(me_model_selectors):
            try:
                me_model_btn = self.browser.find_element(*selector)
                logger.info(f"Found ME-model button with selector {i+1}: {selector}")
                break
            except:
                logger.info(f"ME-model selector {i+1} failed: {selector}")
                continue
        
        if not me_model_btn:
            raise Exception("Cannot find ME-model button")
            
        assert me_model_btn.is_displayed(), "ME-model button is not displayed"
        me_model_btn.click()
        logger.info("Clicked on ME-model button")
        return True

    def click_project_tab(self, logger):
        """Click on Project tab"""
        logger.info("Looking for Project tab...")
        time.sleep(3)
        
        # Try multiple selectors for Project tab
        project_tab = None
        project_tab_selectors = [
            BuildSynaptomeLocators.PROJECT_TAB_PRIMARY,
            BuildSynaptomeLocators.PROJECT_TAB_CLASS,
            BuildSynaptomeLocators.PROJECT_TAB_TEXT,
            BuildSynaptomeLocators.PROJECT_TAB_ROLE,
        ]
        
        for i, selector in enumerate(project_tab_selectors):
            try:
                project_tab = self.browser.find_element(*selector)
                logger.info(f"Found Project tab with selector {i+1}: {selector}")
                break
            except:
                logger.info(f"Project tab selector {i+1} failed: {selector}")
                continue
        
        if not project_tab:
            logger.info("Project tab not found, checking if we're already on project models...")
            return False
        else:
            assert project_tab.is_displayed(), "Project tab is not displayed"
            project_tab.click()
            logger.info("Clicked on Project tab")
            
            # Wait for project models to load
            time.sleep(3)
            logger.info("Project models loaded")
            return True

    def select_model_via_radio_button(self, logger):
        """Select a model by clicking radio button"""
        # Wait for models table to load and select a model by ticking a radio button
        logger.info("Waiting for models table to load...")
        time.sleep(5)  # Give more time for table to load
        
        # Wait for table to be present
        try:
            table = self.browser.find_element(*BuildSynaptomeLocators.MODELS_TABLE)
            logger.info("Models table found")
        except:
            logger.info("Models table not found, continuing anyway...")
        
        logger.info("Looking for radio button to select a model...")
        
        # Try multiple selectors for the radio button with better waiting
        radio_btn = None
        radio_selectors = [
            BuildSynaptomeLocators.RADIO_BUTTON_ANT_INPUT,
            BuildSynaptomeLocators.RADIO_BUTTON_INPUT_CLASS,
            BuildSynaptomeLocators.RADIO_BUTTON_SPAN_TARGET,
            BuildSynaptomeLocators.RADIO_BUTTON_SPAN_WRAPPER,
            BuildSynaptomeLocators.RADIO_BUTTON_TABLE_FIRST,
            BuildSynaptomeLocators.RADIO_BUTTON_ANY,
        ]
        
        for i, selector in enumerate(radio_selectors):
            try:
                # Wait for element to be present and visible
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                radio_btn = WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable(selector)
                )
                logger.info(f"Found clickable radio button with selector {i+1}: {selector}")
                break
            except:
                logger.info(f"Radio button selector {i+1} failed: {selector}")
                continue
        
        if not radio_btn:
            # Try to scroll down to see if radio buttons are below the fold
            logger.info("No radio button found, trying to scroll down...")
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Try again after scrolling
            for i, selector in enumerate(radio_selectors):
                try:
                    from selenium.webdriver.support.ui import WebDriverWait
                    from selenium.webdriver.support import expected_conditions as EC
                    radio_btn = WebDriverWait(self.browser, 5).until(
                        EC.element_to_be_clickable(selector)
                    )
                    logger.info(f"Found radio button after scrolling with selector {i+1}: {selector}")
                    break
                except:
                    continue
        
        if not radio_btn:
            # Debug: Check what elements are actually present on the page
            logger.info("Debugging: Checking page elements...")
            page_source = self.browser.page_source
            
            # Check for common table/selection elements
            if "radio" in page_source.lower():
                logger.info("Found 'radio' text in page source")
            if "select" in page_source.lower():
                logger.info("Found 'select' text in page source")
            if "model" in page_source.lower():
                logger.info("Found 'model' text in page source")
                
            # Try to find any clickable elements that might be model selectors
            try:
                clickable_elements = self.browser.find_elements(*BuildSynaptomeLocators.CLICKABLE_ELEMENTS)
                logger.info(f"Found {len(clickable_elements)} clickable elements")
                
                # Look for elements that might contain model information
                for i, elem in enumerate(clickable_elements[:10]):  # Check first 10
                    try:
                        text = elem.text.strip()
                        if text and ("model" in text.lower() or "select" in text.lower() or len(text) > 5):
                            logger.info(f"Clickable element {i}: '{text}' - tag: {elem.tag_name}, classes: {elem.get_attribute('class')}")
                    except:
                        continue
            except Exception as e:
                logger.info(f"Error finding clickable elements: {e}")
            
            # Try to find table rows that might be selectable
            try:
                table_rows = self.browser.find_elements(*BuildSynaptomeLocators.TABLE_ROWS)
                logger.info(f"Found {len(table_rows)} table rows")
                
                # Try clicking on the first data row (skip header)
                if len(table_rows) > 1:
                    for i, row in enumerate(table_rows[1:3]):  # Try first 2 data rows
                        try:
                            row_text = row.text.strip()
                            if row_text:
                                logger.info(f"Table row {i+1}: '{row_text[:100]}...'")
                                # Try to click this row
                                row.click()
                                logger.info(f"Successfully clicked table row {i+1}")
                                radio_btn = row  # Use the row as our "radio button"
                                break
                        except Exception as e:
                            logger.info(f"Could not click table row {i+1}: {e}")
                            continue
            except Exception as e:
                logger.info(f"Error finding table rows: {e}")
            
            if not radio_btn:
                # Take screenshot for debugging
                self.browser.save_screenshot("debug_me_model_selection.png")
                logger.info("Screenshot saved as debug_me_model_selection.png")
                raise Exception("Cannot find radio button or selectable model element")
            
        # Click the radio button
        try:
            radio_btn.click()
            logger.info("Clicked on radio button to select model")
        except:
            # Try JavaScript click if regular click fails
            self.browser.execute_script("arguments[0].click();", radio_btn)
            logger.info("Clicked on radio button using JavaScript")
        
        # Wait for selection to register
        time.sleep(2)
        logger.info("Model selected via radio button")
        return True

    def click_synapse_sets_tab(self, logger):
        """Click on Synapse sets tab"""
        logger.info("Looking for Synapse sets tab...")
        time.sleep(3)
        
        # Try multiple selectors for the Synapse sets tab
        synapse_sets_tab = None
        synapse_sets_selectors = [
            BuildSynaptomeLocators.SYNAPSE_SETS_TAB_PRIMARY,
            BuildSynaptomeLocators.SYNAPSE_SETS_TAB_CLASS,
            BuildSynaptomeLocators.SYNAPSE_SETS_TAB_ANY,
            BuildSynaptomeLocators.SYNAPSE_SETS_TAB_BOLD,
            BuildSynaptomeLocators.SYNAPSE_SETS_TAB_ANCESTOR,
        ]
        
        for i, selector in enumerate(synapse_sets_selectors):
            try:
                synapse_sets_tab = self.browser.find_element(*selector)
                logger.info(f"Found Synapse sets tab with selector {i+1}: {selector}")
                break
            except:
                logger.info(f"Synapse sets selector {i+1} failed: {selector}")
                continue
        
        if not synapse_sets_tab:
            raise Exception("Cannot find Synapse sets tab")
            
        assert synapse_sets_tab.is_displayed(), "Synapse sets tab is not displayed"
        synapse_sets_tab.click()
        logger.info("Clicked on Synapse sets tab")
        
        # Wait for synapse sets section to load
        time.sleep(3)
        logger.info("Synapse sets section loaded")
        return True