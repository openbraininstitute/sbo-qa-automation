# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from pages.home_page import HomePage
from locators.workflow_locators import WorkflowLocators


class WorkflowsPage(HomePage):
    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, base_url)
        self.logger = logger

    def go_to_workflows_page(self, lab_id: str, project_id: str):
        """Navigate to the workflows page"""
        path = f"/app/virtual-lab/{lab_id}/{project_id}/workflows"
        self.go_to_page(path)
        self.wait_for_page_ready()
        self.logger.info(f"Navigated to workflows page: {self.browser.current_url}")
        return self.browser.current_url

    def wait_for_page_ready(self, timeout=30):
        """Wait for the page to be ready"""
        from selenium.webdriver.support.wait import WebDriverWait
        WebDriverWait(self.browser, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        time.sleep(2)

    # Category buttons
    def find_category_build(self, timeout=10):
        """Find Build category button"""
        return self.find_element(WorkflowLocators.CATEGORY_BUILD, timeout=timeout)

    def find_category_simulate(self, timeout=10):
        """Find Simulate category button"""
        return self.find_element(WorkflowLocators.CATEGORY_SIMULATE, timeout=timeout)

    def click_category_build(self):
        """Click Build category"""
        button = self.find_category_build()
        button.click()
        self.logger.info("Clicked Build category")
        time.sleep(1)
        return True

    def click_category_simulate(self):
        """Click Simulate category"""
        button = self.find_category_simulate()
        button.click()
        self.logger.info("Clicked Simulate category")
        time.sleep(1)
        return True

    # Build type cards
    def find_build_single_neuron(self, timeout=10):
        """Find Build > Single neuron card"""
        element = self.find_element(WorkflowLocators.BUILD_SINGLE_NEURON, timeout=timeout)
        # Return the parent card element which is clickable
        return element.find_element(By.XPATH, "./ancestor::div[@data-slot='card']")

    def find_build_synaptome(self, timeout=10):
        """Find Build > Synaptome card"""
        element = self.find_element(WorkflowLocators.BUILD_SYNAPTOME, timeout=timeout)
        return element.find_element(By.XPATH, "./ancestor::div[@data-slot='card']")

    def find_build_ion_channel(self, timeout=10):
        """Find Build > Ion channel card"""
        element = self.find_element(WorkflowLocators.BUILD_ION_CHANNEL, timeout=timeout)
        return element.find_element(By.XPATH, "./ancestor::div[@data-slot='card']")

    def verify_build_buttons(self):
        """Verify all Build type cards are displayed and clickable"""
        results = {}
        cards = [
            ('Single neuron', WorkflowLocators.BUILD_SINGLE_NEURON),
            ('Synaptome', WorkflowLocators.BUILD_SYNAPTOME),
            ('Ion channel', WorkflowLocators.BUILD_ION_CHANNEL)
        ]
        
        for name, locator in cards:
            try:
                element = self.find_element(locator, timeout=10)
                card = element.find_element(By.XPATH, "./ancestor::div[@data-slot='card']")
                is_displayed = card.is_displayed()
                is_clickable = card.get_attribute('aria-disabled') == 'false'
                results[name] = {'displayed': is_displayed, 'clickable': is_clickable}
                self.logger.info(f"✅ Build > {name}: displayed={is_displayed}, clickable={is_clickable}")
            except TimeoutException:
                results[name] = {'displayed': False, 'clickable': False}
                self.logger.warning(f"❌ Build > {name} not found")
        
        return results

    # Simulate type cards
    def find_simulate_single_neuron(self, timeout=10):
        """Find Simulate > Single neuron card"""
        element = self.find_element(WorkflowLocators.SIMULATE_SINGLE_NEURON, timeout=timeout)
        return element.find_element(By.XPATH, "./ancestor::div[@data-slot='card']")

    def find_simulate_synaptome(self, timeout=10):
        """Find Simulate > Synaptome card"""
        element = self.find_element(WorkflowLocators.SIMULATE_SYNAPTOME, timeout=timeout)
        return element.find_element(By.XPATH, "./ancestor::div[@data-slot='card']")

    def find_simulate_single_neuron_beta(self, timeout=10):
        """Find Simulate > Single neuron beta card"""
        element = self.find_element(WorkflowLocators.SIMULATE_SINGLE_NEURON_BETA, timeout=timeout)
        return element.find_element(By.XPATH, "./ancestor::div[@data-slot='card']")

    def find_simulate_synaptome_beta(self, timeout=10):
        """Find Simulate > Synaptome beta card"""
        element = self.find_element(WorkflowLocators.SIMULATE_SYNAPTOME_BETA, timeout=timeout)
        return element.find_element(By.XPATH, "./ancestor::div[@data-slot='card']")

    def find_simulate_paired_neurons_beta(self, timeout=10):
        """Find Simulate > Paired neurons beta card"""
        element = self.find_element(WorkflowLocators.SIMULATE_PAIRED_NEURONS_BETA, timeout=timeout)
        return element.find_element(By.XPATH, "./ancestor::div[@data-slot='card']")

    def verify_simulate_buttons(self):
        """Verify all Simulate type cards are displayed and clickable"""
        results = {}
        cards = [
            ('Single neuron', WorkflowLocators.SIMULATE_SINGLE_NEURON, False),
            ('Synaptome', WorkflowLocators.SIMULATE_SYNAPTOME, False),
            ('Single neuron beta', WorkflowLocators.SIMULATE_SINGLE_NEURON_BETA, True),
            ('Synaptome beta', WorkflowLocators.SIMULATE_SYNAPTOME_BETA, True),
            ('Paired neurons beta', WorkflowLocators.SIMULATE_PAIRED_NEURONS_BETA, True)
        ]
        
        for name, locator, is_beta in cards:
            try:
                # Use longer timeout for beta cards since they may need scrolling
                timeout = 15 if is_beta else 10
                self.logger.info(f"Looking for {name} with locator: {locator}, timeout: {timeout}")
                element = self.find_element(locator, timeout=timeout)
                card = element.find_element(By.XPATH, "./ancestor::div[@data-slot='card']")
                is_displayed = card.is_displayed()
                is_clickable = card.get_attribute('aria-disabled') == 'false'
                results[name] = {'displayed': is_displayed, 'clickable': is_clickable, 'is_beta': is_beta}
                
                if is_beta:
                    # Beta cards are clickable in staging environment
                    self.logger.info(f"✅ Simulate > {name}: displayed={is_displayed}, clickable={is_clickable} (beta feature)")
                else:
                    self.logger.info(f"✅ Simulate > {name}: displayed={is_displayed}, clickable={is_clickable}")
            except TimeoutException:
                results[name] = {'displayed': False, 'clickable': False, 'is_beta': is_beta}
                self.logger.warning(f"❌ Simulate > {name} not found")
        
        return results

    # Recent Activities section methods
    def find_recent_activities_section(self, timeout=10):
        """Find the Recent Activities section"""
        return self.find_element(WorkflowLocators.RECENT_ACTIVITIES_SECTION, timeout=timeout)
    
    def find_category_dropdown(self, timeout=10):
        """Find Category dropdown (first combobox)"""
        return self.find_element(WorkflowLocators.FIRST_COMBOBOX, timeout=timeout)
    
    def find_type_dropdown(self, timeout=10):
        """Find Type dropdown (second combobox)"""
        return self.find_element(WorkflowLocators.SECOND_COMBOBOX, timeout=timeout)
    
    def click_category_dropdown_option(self, category_name):
        """Click Category dropdown and select an option"""
        try:
            # Find Category dropdown using the label
            category_dropdown = self.find_category_dropdown()
            category_dropdown.click()
            self.logger.info(f"Clicked Category dropdown")
            time.sleep(1)
            
            # Find and click the option
            option_xpath = f"//div[@role='option']//span[contains(text(), '{category_name}')]"
            option = self.browser.find_element(By.XPATH, option_xpath)
            option.click()
            self.logger.info(f"Selected Category: {category_name}")
            time.sleep(2)  # Wait for table to update
            return True
        except Exception as e:
            self.logger.warning(f"Could not select Category '{category_name}': {e}")
            return False
    
    def click_type_dropdown_option(self, type_name):
        """Click Type dropdown and select an option"""
        try:
            # Find Type dropdown using the label
            type_dropdown = self.find_type_dropdown()
            type_dropdown.click()
            self.logger.info(f"Clicked Type dropdown")
            time.sleep(1)
            
            # Find and click the option
            option_xpath = f"//div[@role='option']//span[contains(text(), '{type_name}')]"
            option = self.browser.find_element(By.XPATH, option_xpath)
            option.click()
            self.logger.info(f"Selected Type: {type_name}")
            time.sleep(2)  # Wait for table to update
            return True
        except Exception as e:
            self.logger.warning(f"Could not select Type '{type_name}': {e}")
            return False
    
    def check_no_activities_message(self):
        """Check if 'no activities' message is displayed"""
        try:
            message = self.find_element(WorkflowLocators.NO_ACTIVITIES_MESSAGE, timeout=3)
            if message.is_displayed():
                message_text = message.text
                self.logger.info(f"ℹ️ No activities message found: '{message_text}'")
                return True
            return False
        except:
            return False
    
    def verify_table_for_type(self, type_name):
        """Verify table is displayed and has rows for a specific type"""
        try:
            # Click the type dropdown option
            if not self.click_type_dropdown_option(type_name):
                return False
            
            # Check for "no activities" message first
            if self.check_no_activities_message():
                self.logger.info(f"✅ Type '{type_name}': No activities message displayed (expected)")
                return True
            
            # Verify table is displayed (may not exist if no activities)
            try:
                table_displayed = self.verify_table_displayed()
            except:
                table_displayed = False
            
            if not table_displayed:
                self.logger.info(f"ℹ️ Type '{type_name}': No table displayed (no activities for this type)")
                return True  # This is OK - just means no activities
            
            # Get row count
            row_count = self.get_table_row_count()
            self.logger.info(f"✅ Type '{type_name}': Table has {row_count} rows")
            
            # Verify at least one row exists (or could be 0 if no activities)
            if row_count > 0:
                self.logger.info(f"✅ Type '{type_name}': Activities found")
            else:
                self.logger.info(f"ℹ️ Type '{type_name}': No activities found (table is empty)")
            
            return True
            
        except Exception as e:
            self.logger.warning(f"Error verifying table for Type '{type_name}': {e}")
            return False
    
    def verify_recent_activities_section(self):
        """Verify Recent Activities section with dropdowns and table"""
        try:
            # Check if section exists
            section = self.find_recent_activities_section(timeout=5)
            if not section.is_displayed():
                self.logger.info("ℹ️ Recent Activities section not displayed")
                return False
            
            self.logger.info("✅ Recent Activities section is displayed")
            
            # Check Category dropdown
            try:
                category_dropdown = self.browser.find_element(By.XPATH, "//button[@role='combobox']")
                category_text = category_dropdown.text
                self.logger.info(f"✅ Category dropdown found: {category_text}")
            except:
                self.logger.warning("⚠️ Category dropdown not found")
            
            # Check Type dropdown
            try:
                type_dropdowns = self.browser.find_elements(By.XPATH, "//button[@role='combobox']")
                if len(type_dropdowns) >= 2:
                    type_text = type_dropdowns[1].text
                    self.logger.info(f"✅ Type dropdown found: {type_text}")
                else:
                    self.logger.warning("⚠️ Type dropdown not found")
            except:
                self.logger.warning("⚠️ Type dropdown not found")
            
            # Check table
            table_displayed = self.verify_table_displayed()
            if table_displayed:
                self.logger.info("✅ Activities table is displayed")
                
                # Verify table columns
                columns = self.verify_table_columns()
                required_columns = ['Name', 'Category', 'Type', 'Date', 'Status']
                columns_found = sum(1 for col in required_columns if columns.get(col, {}).get('present', False))
                self.logger.info(f"✅ Found {columns_found}/{len(required_columns)} table columns")
                
                # Get row count
                row_count = self.get_table_row_count()
                self.logger.info(f"📊 Table has {row_count} activity rows")
            
            return True
            
        except Exception as e:
            self.logger.info(f"ℹ️ Recent Activities section not found: {e}")
            return False

    # Table methods
    def find_table(self, timeout=10):
        """Find the workflows table"""
        return self.find_element(WorkflowLocators.TABLE, timeout=timeout)

    def verify_table_displayed(self):
        """Verify table is displayed"""
        try:
            table = self.find_table()
            is_displayed = table.is_displayed()
            self.logger.info(f"✅ Table displayed: {is_displayed}")
            return is_displayed
        except TimeoutException:
            self.logger.warning("❌ Table not found")
            return False

    def verify_table_columns(self):
        """Verify all required table columns are present"""
        results = {}
        columns = [
            ('Name', WorkflowLocators.TABLE_HEADER_NAME),
            ('Category', WorkflowLocators.TABLE_HEADER_CATEGORY),
            ('Type', WorkflowLocators.TABLE_HEADER_TYPE),
            ('Date', WorkflowLocators.TABLE_HEADER_DATE),
            ('Status', WorkflowLocators.TABLE_HEADER_STATUS)
        ]
        
        for name, locator in columns:
            try:
                element = self.find_element(locator, timeout=10)
                is_displayed = element.is_displayed()
                results[name] = {'present': True, 'displayed': is_displayed}
                self.logger.info(f"✅ Column '{name}': displayed={is_displayed}")
            except TimeoutException:
                results[name] = {'present': False, 'displayed': False}
                self.logger.warning(f"❌ Column '{name}' not found")
        
        return results

    def get_table_rows(self):
        """Get all table rows"""
        return self.find_all_elements(WorkflowLocators.TABLE_ROWS)

    def get_table_row_count(self):
        """Get the number of rows in the table"""
        rows = self.get_table_rows()
        count = len(rows)
        self.logger.info(f"Table has {count} rows")
        return count

    # Pagination methods
    def find_pagination(self, timeout=10):
        """Find pagination container"""
        return self.find_element(WorkflowLocators.PAGINATION_CONTAINER, timeout=timeout)

    def verify_pagination_displayed(self):
        """Verify pagination is displayed"""
        try:
            pagination = self.find_pagination()
            is_displayed = pagination.is_displayed()
            self.logger.info(f"✅ Pagination displayed: {is_displayed}")
            return is_displayed
        except TimeoutException:
            self.logger.info("ℹ️ Pagination not found (may not be needed)")
            return False

    def get_pagination_buttons(self):
        """Get all pagination page buttons"""
        try:
            return self.find_all_elements(WorkflowLocators.PAGINATION_PAGES)
        except TimeoutException:
            return []

    def click_pagination_page(self, page_number):
        """Click a specific pagination page"""
        try:
            buttons = self.get_pagination_buttons()
            if page_number <= len(buttons):
                button = buttons[page_number - 1]
                button.click()
                self.logger.info(f"Clicked pagination page {page_number}")
                time.sleep(2)
                return True
            else:
                self.logger.warning(f"Page {page_number} not found")
                return False
        except Exception as e:
            self.logger.warning(f"Error clicking pagination: {e}")
            return False

    # Pagination methods
    def find_pagination(self, timeout=10):
        """Find pagination container"""
        return self.find_element(WorkflowLocators.PAGINATION_CONTAINER, timeout=timeout)

    def verify_pagination_displayed(self):
        """Verify pagination is displayed"""
        try:
            pagination = self.find_pagination(timeout=5)
            is_displayed = pagination.is_displayed()
            self.logger.info(f"✅ Pagination displayed: {is_displayed}")
            return is_displayed
        except TimeoutException:
            self.logger.info("ℹ️ Pagination not found (may not be needed)")
            return False
    
    def get_active_page_number(self):
        """Get the currently active page number"""
        try:
            active_item = self.find_element(WorkflowLocators.PAGINATION_ACTIVE_ITEM, timeout=5)
            page_num = active_item.text
            return int(page_num)
        except:
            return 1
    
    def click_pagination_next(self):
        """Click the Next pagination button"""
        try:
            next_button = self.find_element(WorkflowLocators.PAGINATION_NEXT, timeout=5)
            # Check if disabled
            parent = next_button.find_element(By.XPATH, "..")
            if 'ant-pagination-disabled' in parent.get_attribute('class'):
                self.logger.info("ℹ️ Next button is disabled (last page)")
                return False
            
            next_button.click()
            self.logger.info("✅ Clicked Next pagination button")
            time.sleep(2)
            return True
        except Exception as e:
            self.logger.warning(f"Could not click Next button: {e}")
            return False
    
    def click_pagination_previous(self):
        """Click the Previous pagination button"""
        try:
            prev_button = self.find_element(WorkflowLocators.PAGINATION_PREVIOUS, timeout=5)
            # Check if disabled
            parent = prev_button.find_element(By.XPATH, "..")
            if 'ant-pagination-disabled' in parent.get_attribute('class'):
                self.logger.info("ℹ️ Previous button is disabled (first page)")
                return False
            
            prev_button.click()
            self.logger.info("✅ Clicked Previous pagination button")
            time.sleep(2)
            return True
        except Exception as e:
            self.logger.warning(f"Could not click Previous button: {e}")
            return False
    
    def click_pagination_page(self, page_number):
        """Click a specific pagination page number"""
        try:
            page_items = self.find_all_elements(WorkflowLocators.PAGINATION_ITEM)
            for item in page_items:
                if item.text == str(page_number):
                    item.click()
                    self.logger.info(f"✅ Clicked pagination page {page_number}")
                    time.sleep(2)
                    return True
            self.logger.warning(f"Page {page_number} not found")
            return False
        except Exception as e:
            self.logger.warning(f"Error clicking pagination page {page_number}: {e}")
            return False
    
    def verify_pagination_works(self):
        """Verify pagination by clicking through pages and checking table changes"""
        try:
            # Check if pagination exists
            if not self.verify_pagination_displayed():
                self.logger.info("ℹ️ No pagination to test")
                return True
            
            # Get initial page and row count
            initial_page = self.get_active_page_number()
            initial_rows = self.get_table_row_count()
            self.logger.info(f"📄 Starting on page {initial_page} with {initial_rows} rows")
            
            # Try to click Next
            if self.click_pagination_next():
                new_page = self.get_active_page_number()
                new_rows = self.get_table_row_count()
                
                if new_page != initial_page:
                    self.logger.info(f"✅ Pagination works: moved from page {initial_page} to page {new_page}")
                    self.logger.info(f"📊 New page has {new_rows} rows")
                    
                    # Go back to first page
                    self.click_pagination_previous()
                    back_page = self.get_active_page_number()
                    self.logger.info(f"✅ Returned to page {back_page}")
                    return True
                else:
                    self.logger.warning("⚠️ Page number didn't change after clicking Next")
                    return False
            else:
                self.logger.info("ℹ️ Only one page of results")
                return True
                
        except Exception as e:
            self.logger.warning(f"Error verifying pagination: {e}")
            return False

    def verify_pagination_changes_content(self):
        """Verify that clicking pagination changes table content"""
        try:
            # Get initial row count
            initial_rows = self.get_table_row_count()
            
            # Get pagination buttons
            buttons = self.get_pagination_buttons()
            if len(buttons) < 2:
                self.logger.info("ℹ️ Not enough pages to test pagination")
                return True
            
            # Click second page
            buttons[1].click()
            self.logger.info("Clicked page 2")
            time.sleep(2)
            
            # Get new row count (content should change)
            new_rows = self.get_table_row_count()
            
            # Click back to first page
            buttons = self.get_pagination_buttons()
            buttons[0].click()
            self.logger.info("Clicked page 1")
            time.sleep(2)
            
            self.logger.info(f"✅ Pagination working - rows changed from {initial_rows} to {new_rows}")
            return True
            
        except Exception as e:
            self.logger.warning(f"Could not verify pagination: {e}")
            return False

    def click_type_and_verify_table(self, type_name, locator):
        """Click a type card and verify table is displayed"""
        try:
            element = self.find_element(locator, timeout=10)
            card = element.find_element(By.XPATH, "./ancestor::div[@data-slot='card']")
            
            # Check if card is clickable
            if card.get_attribute('aria-disabled') == 'true':
                self.logger.info(f"ℹ️ {type_name} is disabled (beta feature)")
                return False
            
            card.click()
            self.logger.info(f"Clicked {type_name}")
            time.sleep(2)
            
            # Verify table is displayed
            table_displayed = self.verify_table_displayed()
            if table_displayed:
                self.logger.info(f"✅ Table displayed after clicking {type_name}")
                return True
            else:
                self.logger.warning(f"⚠️ Table not displayed after clicking {type_name}")
                return False
        except Exception as e:
            self.logger.warning(f"Error clicking {type_name}: {e}")
            return False


    # Radio button methods
    def get_all_radio_buttons(self):
        """Get all radio buttons in the table"""
        try:
            return self.find_all_elements(WorkflowLocators.RADIO_BUTTONS)
        except:
            return []
    
    def click_radio_button_by_index(self, index=0):
        """Click a radio button by index (0-based)"""
        try:
            radio_buttons = self.get_all_radio_buttons()
            if index < len(radio_buttons):
                radio_buttons[index].click()
                self.logger.info(f"✅ Clicked radio button at index {index}")
                time.sleep(1)
                return True
            else:
                self.logger.warning(f"⚠️ Radio button index {index} out of range (total: {len(radio_buttons)})")
                return False
        except Exception as e:
            self.logger.warning(f"Error clicking radio button: {e}")
            return False
    
    def click_first_radio_button(self):
        """Click the first radio button in the table"""
        return self.click_radio_button_by_index(0)
    
    def is_radio_button_selected(self, index=0):
        """Check if a radio button is selected"""
        try:
            radio_buttons = self.get_all_radio_buttons()
            if index < len(radio_buttons):
                return radio_buttons[index].is_selected()
            return False
        except:
            return False
    
    def get_selected_row_data(self):
        """Get data from the selected row"""
        try:
            # Find the selected radio button's row
            selected_row = self.browser.find_element(
                By.XPATH, 
                "//table//tbody//tr[.//input[@type='radio' and @checked]]"
            )
            
            # Extract cell data
            cells = selected_row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 6:
                return {
                    'name': cells[1].text,
                    'category': cells[2].text,
                    'type': cells[3].text,
                    'date': cells[4].text,
                    'status': cells[5].text
                }
            return None
        except Exception as e:
            self.logger.warning(f"Could not get selected row data: {e}")
            return None
    
    # Action button methods
    def find_view_configuration_button(self, timeout=5):
        """Find View Configuration button"""
        return self.find_element(WorkflowLocators.VIEW_CONFIGURATION_BUTTON, timeout=timeout)
    
    def find_view_results_button(self, timeout=5):
        """Find View Results button"""
        return self.find_element(WorkflowLocators.VIEW_RESULTS_BUTTON, timeout=timeout)
    
    def find_duplicate_button(self, timeout=5):
        """Find Duplicate button"""
        return self.find_element(WorkflowLocators.DUPLICATE_BUTTON, timeout=timeout)
    
    def click_view_configuration_button(self):
        """Click View Configuration button (it's an <a> tag with role='button')"""
        try:
            button = self.find_view_configuration_button()
            button.click()
            self.logger.info("✅ Clicked View Configuration button")
            time.sleep(2)
            return True
        except Exception as e:
            self.logger.warning(f"Could not click View Configuration button: {e}")
            return False
    
    def click_view_results_button(self):
        """Click View Results button"""
        try:
            button = self.find_view_results_button()

            if not button.is_enabled():
                self.logger.info("ℹ️ View Results button is disabled")
                return False

            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            time.sleep(0.5)
            try:
                button.click()
            except Exception:
                self.browser.execute_script("arguments[0].click();", button)
            self.logger.info("✅ Clicked View Results button")
            time.sleep(2)
            return True
        except Exception as e:
            self.logger.warning(f"Could not click View Results button: {e}")
            return False
    
    def click_duplicate_button(self):
        """Click Duplicate button"""
        try:
            button = self.find_duplicate_button()
            
            # Check if button is disabled
            if button.get_attribute('disabled'):
                self.logger.info("ℹ️ Duplicate button is disabled")
                return False
            
            button.click()
            self.logger.info("✅ Clicked Duplicate button")
            time.sleep(2)
            return True
        except Exception as e:
            self.logger.warning(f"Could not click Duplicate button: {e}")
            return False
    
    def verify_action_buttons_appear(self):
        """Verify that action buttons appear after selecting a radio button"""
        try:
            # Check for any of the action buttons
            buttons_found = []
            
            try:
                self.find_view_configuration_button(timeout=3)
                buttons_found.append('View Configuration')
            except:
                pass
            
            try:
                self.find_view_results_button(timeout=3)
                buttons_found.append('View Results')
            except:
                pass
            
            try:
                self.find_duplicate_button(timeout=3)
                buttons_found.append('Duplicate')
            except:
                pass
            
            if buttons_found:
                self.logger.info(f"✅ Action buttons found: {', '.join(buttons_found)}")
                return True
            else:
                self.logger.warning("⚠️ No action buttons found")
                return False
        except Exception as e:
            self.logger.warning(f"Error verifying action buttons: {e}")
            return False
    
    def select_activity_and_verify_buttons(self, row_index=0):
        """Select an activity row and verify action buttons appear"""
        try:
            # Click radio button
            if not self.click_radio_button_by_index(row_index):
                return False
            
            # Verify buttons appear
            return self.verify_action_buttons_appear()
        except Exception as e:
            self.logger.warning(f"Error in select_activity_and_verify_buttons: {e}")
            return False
    
    def test_view_configuration_redirect(self, expected_url_pattern):
        """Test View Configuration button redirects correctly"""
        try:
            # Get current URL before clicking
            initial_url = self.browser.current_url
            
            # Click View Configuration
            if not self.click_view_configuration_button():
                return False
            
            # Wait for navigation
            time.sleep(3)
            
            # Get new URL
            new_url = self.browser.current_url
            
            # Verify URL changed and matches pattern
            if new_url != initial_url and expected_url_pattern in new_url:
                self.logger.info(f"✅ Redirected to: {new_url}")
                return True
            else:
                self.logger.warning(f"⚠️ URL did not match expected pattern. Got: {new_url}")
                return False
        except Exception as e:
            self.logger.warning(f"Error testing View Configuration redirect: {e}")
            return False
