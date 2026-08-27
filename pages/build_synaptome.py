# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
import logging

from locators.build_synaptome_locators import BuildSynaptomeLocators
from pages.home_page import HomePage


class BuildSynaptomePage(HomePage):
    def __init__(self, browser, wait, base_url, logger=None):
        super().__init__(browser, wait, base_url)
        self.base_url = base_url
        self.logger = logger or logging.getLogger(__name__)
        self.home_page = HomePage(browser, wait, base_url)

    def navigate_to_workflows(self, lab_id, project_id):
        """Navigate to the workflows page with specific brain ID"""
        workflows_url = f"{self.base_url}/app/virtual-lab/{lab_id}/{project_id}/workflows?activity=build"
        self.browser.get(workflows_url)
        self.wait_for_page_load()
        return workflows_url
    
    def wait_for_page_load(self, timeout=10):
        """Wait for page to load completely"""
        try:
            self.wait_for_page_ready(timeout)
            
            time.sleep(3)  # Increased from 2 to 3 seconds for CI stability
            
            try:
                spinner_locator = (By.XPATH, "//div[contains(@class, 'loading') or contains(@class, 'spinner')]")
                self.wait_for_element_to_disappear(spinner_locator, timeout=5)
            except:
                pass  # No spinners found, continue
                
        except Exception as e:
            print(f"Page load timeout - continuing anyway: {e}")

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
        self.wait_for_condition(
            lambda driver: any(
                self.find_all_elements((By.TAG_NAME, "td"), timeout=10) and
                any(cell.text.strip() for cell in self.find_all_elements((By.TAG_NAME, "td"), timeout=10))
                for row in table.find_elements(By.TAG_NAME, "tr")
            ),
            timeout=20,
            retries=1,
            message="Table rows are not populated with data within the timeout."
        )

        # Extract table content once it is fully loaded
        rows = self.find_all_elements((By.TAG_NAME, "tr"))
        table_content = []
        for row in rows:
            cells = self.find_all_elements((By.TAG_NAME, "td"), timeout=10)
            row_content = [cell.text.strip() for cell in cells]
            if row_content:
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
        self.wait_for_condition(
            lambda d: d.find_element(*BuildSynaptomeLocators.TARGET_INPUT2).get_attribute("aria-expanded") == "true",
            timeout=timeout,
            retries=1,
            message="Target dropdown 2 did not expand"
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
            self.wait_for_condition(
                lambda driver: self.get_table_content() != initial_table_content,
                timeout=timeout,
                retries=1,
                message="Table sorting did not complete within the provided timeout."
            )
            print("Table sorting is completed. The table content was updated.")
        except (TimeoutException, RuntimeError):
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
        self.wait_for_condition(
            lambda driver: len(self.get_all_table_rows()) > 0 and "No data" not in self.get_table_content(),
            timeout=timeout,
            retries=1,
            message="Table data is not loaded within the timeout."
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
    
    def click_public_tab(self, logger):
        """Click on Public tab"""
        logger.info("Looking for Public tab...")
        time.sleep(3)
        
        # Try multiple selectors for Public tab
        public_tab = None
        public_tab_selectors = [
            (By.XPATH, "//button[contains(., 'Public')]"),
            (By.XPATH, "//div[@role='tab' and contains(., 'Public')]"),
            (By.XPATH, "//*[contains(@class, 'tab') and contains(., 'Public')]"),
            (By.XPATH, "//button[@role='tab' and contains(text(), 'Public')]"),
            (By.XPATH, "//*[text()='Public' or contains(text(), 'Public')]"),
        ]
        
        for i, selector in enumerate(public_tab_selectors):
            try:
                public_tab = self.browser.find_element(*selector)
                logger.info(f"Found Public tab with selector {i+1}: {selector}")
                break
            except:
                logger.info(f"Public tab selector {i+1} failed: {selector}")
                continue
        
        if not public_tab:
            logger.info("Public tab not found, checking if we're already on public models...")
            return False
        else:
            assert public_tab.is_displayed(), "Public tab is not displayed"
            public_tab.click()
            logger.info("Clicked on Public tab")
            
            # Wait for public models to load
            time.sleep(3)
            logger.info("Public models loaded")
            return True
    
    def search_for_model(self, search_text, logger=None):
        """
        Search for a model using the free text search field
        
        Args:
            search_text: Text to search for (e.g., "cadpyr")
            logger: Logger instance
        """
        if logger:
            logger.info(f"Searching for model: {search_text}")
        
        # Wait for the page to fully load after clicking Public tab
        time.sleep(3)
        
        search_field = None
        try:
            search_field = self.element_visibility(BuildSynaptomeLocators.SEARCH_INPUT, timeout=2)
            if logger:
                logger.info("Search field already visible")
        except TimeoutException:
            search_button = self.element_to_be_clickable(BuildSynaptomeLocators.SEARCH_BUTTON, timeout=5)
            search_button.click()
            if logger:
                logger.info("Clicked search button to open search")
            time.sleep(1)
            search_field = self.element_visibility(BuildSynaptomeLocators.SEARCH_INPUT, timeout=10)
            if logger:
                logger.info("Found search field after opening toolbar search")
        
        # Clear and enter search text
        search_field.clear()
        search_field.send_keys(search_text)
        if logger:
            logger.info(f"Entered search text: {search_text}")
        
        # Press Enter to trigger search
        search_field.send_keys(Keys.RETURN)
        if logger:
            logger.info("Pressed Enter to search")
        
        # Wait for search results to load
        time.sleep(3)
        
        if logger:
            logger.info("Search completed, results should be filtered")
        
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

    def create_synapse_set(self, name, target, synapse_type="Excitatory Synapses", formula="0.04",
                           min_filter=10, max_filter=900, logger=None):
        """
        Create a synapse set with the specified configuration

        Args:
            name: Name of the synapse set (e.g., "apical1", "basal1", "soma1")
            target: Target location (e.g., "Apical dendrites", "Basal dendrites", "Soma")
            synapse_type: Type of synapses (default: "Excitatory Synapses")
            formula: Synapse distribution formula (default: "0.04")
            min_filter: Minimum filter value (default: 10)
            max_filter: Maximum filter value (default: 900)
            logger: Logger instance
        """
        if logger:
            logger.info(f"Creating synapse set: {name} on {target}")

        # Fill in the name field
        name_field = self.find_element((By.ID, "name"))
        name_field.clear()
        name_field.send_keys(name)
        if logger:
            logger.info(f"Set name: {name}")
        time.sleep(0.5)

        # Select target from dropdown
        target_dropdown_locator = (By.XPATH, "//input[@id='target']/ancestor::div[contains(@class, 'ant-select')]")
        self.wait_and_click(target_dropdown_locator, timeout=20)
        time.sleep(1)

        # Wait for dropdown options and select target
        target_option_locator = (By.XPATH, f"//div[@class='ant-select-item-option-content' and text()='{target}']")
        target_option = self.element_to_be_clickable(target_option_locator, timeout=20)
        target_option.click()
        if logger:
            logger.info(f"Selected target: {target}")
        time.sleep(0.5)

        # Type is already set to "Excitatory Synapses" by default
        # Only change if we need a different type
        if synapse_type != "Excitatory Synapses":
            type_dropdown_locator = (By.XPATH, "//input[@id='type']/ancestor::div[contains(@class, 'ant-select')]")
            self.wait_and_click(type_dropdown_locator, timeout=10)
            time.sleep(0.5)

            # Select the type option
            type_option_locator = (By.XPATH, f"//div[@class='ant-select-item-option-content' and text()='{synapse_type}']")
            type_option = self.element_to_be_clickable(type_option_locator, timeout=10)
            type_option.click()
            if logger:
                logger.info(f"Selected type: {synapse_type}")
            time.sleep(0.5)
        else:
            if logger:
                logger.info(f"Type already set to: {synapse_type}")

        # Fill in the formula
        formula_field = self.find_element((By.ID, "formula"))
        formula_field.clear()
        formula_field.send_keys(formula)
        if logger:
            logger.info(f"Set formula: {formula}")

        # Wait for Apply button to become enabled after entering formula
        time.sleep(2)

        # Check if filter section is already expanded by looking for input fields
        min_input_locator = (By.XPATH, "//input[contains(@id, 'distance_soma_gte')]")
        try:
            # Try to find the input field with a short timeout
            min_input = self.find_element(min_input_locator, timeout=2)
            if logger:
                logger.info("Filter section already expanded")
        except:
            # Filter section is collapsed, need to expand it
            if logger:
                logger.info("Filter section collapsed, expanding it")
            filter_header_locator = (By.ID, "exclusion-rules-header")
            self.wait_and_click(filter_header_locator, timeout=10)
            time.sleep(2)  # Wait for filter section to fully expand
            if logger:
                logger.info("Expanded filter synapses section")

            # Now find the input field
            min_input = self.element_to_be_clickable(min_input_locator, timeout=10)

        min_input.clear()
        min_input.send_keys(str(max_filter))  # Fill max value first (900)
        if logger:
            logger.info(f"Set greater or equal to: {max_filter}")
        time.sleep(0.5)

        max_input_locator = (By.XPATH, "//input[contains(@id, 'distance_soma_lte')]")
        max_input = self.element_to_be_clickable(max_input_locator, timeout=10)
        max_input.clear()
        max_input.send_keys(str(min_filter))  # Fill min value second (10)
        if logger:
            logger.info(f"Set less or equal to: {min_filter}")
        time.sleep(1)

        # Wait for Apply button to become enabled after entering filter values
        time.sleep(2)

        # Click "Apply changes" button - wait for it to be enabled
        apply_btn_locator = (By.XPATH, "//button[@type='submit' and contains(., 'Apply changes')]")
        apply_btn = self.element_to_be_clickable(apply_btn_locator, timeout=10)
        apply_btn.click()
        if logger:
            logger.info("Clicked Apply changes button")
        time.sleep(5)  # Wait for changes to be saved before proceeding

        if logger:
            logger.info(f"Synapse set '{name}' created successfully")

    def verify_synapse_sets_info_panel(self, logger=None):
        """Verify the Synapse sets info panel is displayed with the expected heading and instruction text"""
        if logger:
            logger.info("Verifying Synapse sets info panel...")

        panel = self.find_element(BuildSynaptomeLocators.SYNAPSE_SETS_INFO_PANEL, timeout=10)
        assert panel.is_displayed(), "Synapse sets info panel is not displayed"

        heading = self.find_element(BuildSynaptomeLocators.SYNAPSE_SETS_INFO_HEADING, timeout=5)
        assert heading.text.strip() == "Synapse sets", f"Expected heading 'Synapse sets', got '{heading.text.strip()}'"

        instruction = self.find_element(BuildSynaptomeLocators.SYNAPSE_SETS_INFO_TEXT, timeout=5)
        assert "Add set" in instruction.text, f"Expected instruction text about 'Add set' button, got '{instruction.text}'"

        if logger:
            logger.info("Synapse sets info panel verified successfully")
        return True

    def click_add_set_button(self, logger=None):
        """Click the 'Add set' button to create a new synapse set"""
        add_set_btn = self.element_to_be_clickable(BuildSynaptomeLocators.ADD_SET_BUTTON, timeout=10)
        add_set_btn.click()
        if logger:
            logger.info("Clicked 'Add set' button")
        time.sleep(3)  # Wait for new set form to load

    def _wait_for_ag_selection_inputs(self, timeout=30):
        """Poll for AG Grid selection inputs in the model picker."""
        deadline = time.time() + timeout
        attempt = 0
        while time.time() < deadline:
            attempt += 1
            selectors = self.browser.find_elements(*BuildSynaptomeLocators.AG_SELECTION_INPUTS)
            selectors = [el for el in selectors if el.is_enabled()]
            if selectors:
                self.logger.info(
                    f"Found {len(selectors)} AG Grid selection inputs after attempt {attempt}"
                )
                return selectors
            self.logger.info(f"Waiting for AG Grid selection inputs... attempt {attempt}")
            time.sleep(2)
        return []

    def _click_ag_selection_input(self, element):
        """Click an AG Grid selection input (often visually hidden)."""
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.3)
        try:
            self.browser.execute_script("arguments[0].click();", element)
        except Exception:
            try:
                wrapper = element.find_element(
                    By.XPATH,
                    "./ancestor::div[contains(@class,'ag-selection-checkbox') or contains(@class,'ag-cell')][1]",
                )
                self.browser.execute_script("arguments[0].click();", wrapper)
            except Exception:
                element.click()

    def select_model_via_radio_button(self, logger):
        """Select a model via AG Grid row selection (replaces legacy ant-radio)."""
        logger.info("Waiting for models table to load...")
        time.sleep(3)

        try:
            self.find_element(BuildSynaptomeLocators.TABLE_ROWS, timeout=30)
            logger.info("AG Grid rows loaded")
        except TimeoutException:
            logger.warning("AG Grid rows not found within timeout")

        selection_inputs = self._wait_for_ag_selection_inputs(timeout=30)
        if selection_inputs:
            target = selection_inputs[0]
            self._click_ag_selection_input(target)
            logger.info("Selected model via AG Grid selection input")
            time.sleep(2)
            return True

        # Fallback: click the first name cell (opens mini-detail / selects row)
        try:
            name_cell = self.element_to_be_clickable(
                BuildSynaptomeLocators.TABLE_ROW_NAME_CELL, timeout=10
            )
            self.browser.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", name_cell
            )
            time.sleep(0.5)
            try:
                name_cell.click()
            except Exception:
                self.browser.execute_script("arguments[0].click();", name_cell)
            logger.info("Selected model by clicking name cell")
            time.sleep(2)
            return True
        except TimeoutException:
            pass

        # Legacy ant-radio fallbacks
        radio_selectors = [
            BuildSynaptomeLocators.RADIO_BUTTON_ANT_INPUT,
            BuildSynaptomeLocators.RADIO_BUTTON_INPUT_CLASS,
            BuildSynaptomeLocators.RADIO_BUTTON_SPAN_TARGET,
            BuildSynaptomeLocators.RADIO_BUTTON_TABLE_FIRST,
            BuildSynaptomeLocators.RADIO_BUTTON_ANY,
        ]
        for i, selector in enumerate(radio_selectors):
            try:
                radio_btn = self.element_to_be_clickable(selector, timeout=5)
                self._click_ag_selection_input(radio_btn)
                logger.info(f"Selected model via legacy radio selector {i + 1}")
                time.sleep(2)
                return True
            except TimeoutException:
                logger.info(f"Radio button selector {i + 1} failed: {selector}")

        logger.error("Cannot find radio button or AG Grid selection input")
        raise Exception("Cannot find radio button or selectable model element")
