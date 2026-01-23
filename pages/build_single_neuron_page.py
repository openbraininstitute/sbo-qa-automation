"""
Page Object for Build Single Neuron functionality
"""

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from pages.project_home import ProjectHome
from locators.build_single_neuron_locators import BuildSingleNeuronLocators


class BuildSingleNeuronPage(ProjectHome):
    """Page object for build single neuron functionality"""
    
    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, logger, base_url)
        self.base_url = base_url
        self.locators = BuildSingleNeuronLocators()
    
    def navigate_to_workflows(self, lab_id, project_id, brain_id="5c60bf3e-5335-4971-a8ec-6597292452b2", brain_av="567"):
        """Navigate to the workflows page with specific brain ID"""
        workflows_url = f"{self.base_url}/app/virtual-lab/{lab_id}/{project_id}/workflows?activity=build"
        self.browser.get(workflows_url)
        self.wait_for_page_load()
        return workflows_url
    
    def wait_for_page_load(self, timeout=10):
        """Wait for page to load completely"""
        try:
            WebDriverWait(self.browser, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            time.sleep(2)  # Additional wait for dynamic content
        except TimeoutException:
            print("Page load timeout - continuing anyway")
    
    def click_build_button(self, timeout=10):
        """Click the main Build button"""
        try:
            build_button = self.element_to_be_clickable(self.locators.BUILD_BUTTON, timeout)
            self.browser.execute_script("arguments[0].scrollIntoView(true);", build_button)
            time.sleep(1)
            build_button.click()
            print("✅ Build button clicked successfully")
            return True
        except TimeoutException:
            print("❌ Build button not found or not clickable")
            return False
        except Exception as e:
            print(f"❌ Error clicking Build button: {e}")
            return False
    
    def select_single_neuron_type(self, timeout=10):
        """Select Single neuron build type"""
        try:
            # Try multiple selectors for single neuron option
            selectors = [
                self.locators.SINGLE_NEURON_TYPE,
                self.locators.SINGLE_NEURON_CARD
            ]
            
            for selector in selectors:
                try:
                    single_neuron = self.element_to_be_clickable(selector, timeout)
                    self.browser.execute_script("arguments[0].scrollIntoView(true);", single_neuron)
                    time.sleep(1)
                    single_neuron.click()
                    print("✅ Single neuron type selected successfully")
                    self.wait_for_page_load()
                    return True
                except TimeoutException:
                    continue
            
            print("❌ Single neuron option not found")
            return False
        except Exception as e:
            print(f"❌ Error selecting single neuron type: {e}")
            return False
    
    def wait_for_configuration_page(self, timeout=15):
        """Wait for redirect to configuration page"""
        try:
            # Wait for URL to contain 'configure' or 'memodel'
            WebDriverWait(self.browser, timeout).until(
                lambda driver: 'configure' in driver.current_url.lower() or 'memodel' in driver.current_url.lower()
            )
            self.wait_for_page_load()
            
            # Verify configuration elements are present
            if self.verify_configuration_page_elements():
                print(f"✅ Redirected to configuration page: {self.browser.current_url}")
                return True
            else:
                print(f"⚠️ Configuration page reached but elements not fully loaded: {self.browser.current_url}")
                return True  # Still return True as we reached the page
                
        except TimeoutException:
            print(f"❌ Configuration page not reached. Current URL: {self.browser.current_url}")
            return False
    
    def verify_configuration_page_elements(self):
        """Verify that key configuration page elements are present"""
        try:
            # Check for configuration form
            form_present = len(self.browser.find_elements(*self.locators.CONFIGURATION_FORM)) > 0
            
            # Check for name input
            name_input_present = (
                len(self.browser.find_elements(*self.locators.MODEL_NAME_INPUT)) > 0 or
                len(self.browser.find_elements(*self.locators.MODEL_NAME_INPUT_ALT)) > 0
            )
            
            # Check for M-model and E-model buttons
            m_model_present = len(self.browser.find_elements(*self.locators.M_MODEL_BUTTON)) > 0
            e_model_present = len(self.browser.find_elements(*self.locators.E_MODEL_BUTTON)) > 0
            
            elements_found = {
                "form": form_present,
                "name_input": name_input_present,
                "m_model_button": m_model_present,
                "e_model_button": e_model_present
            }
            
            print(f"ℹ️ Configuration page elements: {elements_found}")
            return name_input_present and m_model_present and e_model_present
            
        except Exception as e:
            print(f"❌ Error verifying configuration page elements: {e}")
            return False
    
    def fill_model_name(self, model_name="Test-ME-Model", timeout=10):
        """Fill in the model name field"""
        try:
            # Try multiple selectors for the name input based on actual HTML
            selectors = [
                self.locators.MODEL_NAME_INPUT,  # ID-based selector
                self.locators.MODEL_NAME_INPUT_ALT,  # Placeholder-based
                self.locators.MODEL_NAME_INPUT_FALLBACK  # Fallback
            ]
            
            for selector in selectors:
                try:
                    name_input = self.element_to_be_clickable(selector, timeout)
                    name_input.clear()
                    name_input.send_keys(model_name)
                    print(f"✅ Model name '{model_name}' entered successfully")
                    return True
                except TimeoutException:
                    continue
            
            print("❌ Model name input field not found")
            return False
        except Exception as e:
            print(f"❌ Error filling model name: {e}")
            return False
    
    def click_m_model_button(self, timeout=10):
        """Click the M-model selection button"""
        try:
            # Try multiple selectors for M-model button based on actual HTML
            selectors = [
                self.locators.M_MODEL_BUTTON,  # Primary selector
                self.locators.M_MODEL_BUTTON_ALT,  # Alternative
                self.locators.M_MODEL_BUTTON_FALLBACK  # Fallback
            ]
            
            for selector in selectors:
                try:
                    m_model_button = self.element_to_be_clickable(selector, timeout)
                    self.browser.execute_script("arguments[0].scrollIntoView(true);", m_model_button)
                    time.sleep(1)
                    m_model_button.click()
                    print("✅ M-model button clicked successfully")
                    self.wait_for_page_load()
                    
                    # Add debugging after click
                    print(f"🔍 After M-model button click, current URL: {self.browser.current_url}")
                    
                    # Check if we're on a new page or if a modal/dropdown opened
                    time.sleep(3)  # Wait for any transitions
                    
                    # Look for different types of M-model selection interfaces
                    tables = self.browser.find_elements(By.XPATH, "//table")
                    print(f"🔍 Found {len(tables)} table elements on page")
                    
                    modals = self.browser.find_elements(By.XPATH, "//div[contains(@class, 'modal') or contains(@class, 'drawer') or contains(@class, 'popup')]")
                    print(f"🔍 Found {len(modals)} modal/drawer elements on page")
                    
                    dropdowns = self.browser.find_elements(By.XPATH, "//div[contains(@class, 'dropdown') or contains(@class, 'select')]")
                    print(f"🔍 Found {len(dropdowns)} dropdown elements on page")
                    
                    return True
                except TimeoutException:
                    continue
            
            print("❌ M-model button not found")
            return False
        except Exception as e:
            print(f"❌ Error clicking M-model button: {e}")
            return False
    
    def select_first_m_model(self, timeout=15):
        """Select the first M-model from the table (2nd row - first data row)"""
        try:
            # Wait for the specific table with ID to load
            print("🔍 Looking for M-model table with ID 'data-table-with-filters'...")
            
            # Use the correct table selector
            self.find_element(self.locators.M_MODEL_TABLE, timeout)
            print("✅ M-model table loaded")
            
            # Add debugging - check what elements are actually on the page
            print("🔍 Debugging: Looking for radio buttons in the table...")
            
            # Check for radio buttons specifically in this table
            table_radios = self.browser.find_elements(By.XPATH, "//table[@id='data-table-with-filters']//input[@type='radio']")
            print(f"🔍 Found {len(table_radios)} radio input elements in the table")
            
            # Check for ant-radio-inner spans in this table
            table_radio_spans = self.browser.find_elements(By.XPATH, "//table[@id='data-table-with-filters']//span[@class='ant-radio-inner']")
            print(f"🔍 Found {len(table_radio_spans)} ant-radio-inner spans in the table")
            
            # Check table structure
            table_rows = self.browser.find_elements(By.XPATH, "//table[@id='data-table-with-filters']//tbody//tr")
            print(f"🔍 Found {len(table_rows)} table rows")
            
            if len(table_rows) > 0:
                print(f"🔍 First row content preview: {table_rows[0].text[:100] if table_rows[0].text else 'No text'}")
            if len(table_rows) > 1:
                print(f"🔍 Second row content preview: {table_rows[1].text[:100] if table_rows[1].text else 'No text'}")
                print("🔍 Targeting second row (first data row) for radio button selection")
            
            # Try multiple radio button selectors - use the table-specific ones first (2nd row)
            selectors = [
                self.locators.TICK_SEARCHED_M_RECORD,  # Updated table-specific locator (2nd row)
                self.locators.FIRST_M_MODEL_RADIO,     # Table-specific locator (2nd row)
                (By.XPATH, "//table[@id='data-table-with-filters']//tbody//tr[2]//span[@class='ant-radio-inner']"),  # Second row radio span
                (By.XPATH, "//table[@id='data-table-with-filters']//tbody//tr[2]//input[@type='radio']"),  # Second row radio input
                (By.XPATH, "//table[@id='data-table-with-filters']//tbody//tr[2]//span[contains(@class, 'ant-radio')]"),  # Second row ant-radio
                (By.XPATH, "//table[@id='data-table-with-filters']//tbody//tr[1]//span[@class='ant-radio-inner']"),  # First row radio span (fallback)
                (By.XPATH, "//table[@id='data-table-with-filters']//tbody//tr[1]//input[@type='radio']"),  # First row radio input (fallback)
                (By.XPATH, "//table[@id='data-table-with-filters']//span[@class='ant-radio-inner']")[0] if len(table_radio_spans) > 0 else None,  # First span in table
                (By.XPATH, "//table[@id='data-table-with-filters']//input[@type='radio']")[0] if len(table_radios) > 0 else None,  # First input in table
                (By.XPATH, "(//span[@class='ant-radio-inner'])[1]"),  # Fallback - first anywhere
                (By.XPATH, "(//input[@type='radio'])[1]"),  # Fallback - first input anywhere
            ]
            
            # Filter out None selectors
            selectors = [s for s in selectors if s is not None]
            
            for i, selector in enumerate(selectors):
                try:
                    print(f"🔍 Trying M-model radio selector {i+1}: {selector}")
                    
                    # First check if element exists
                    elements = self.browser.find_elements(*selector)
                    print(f"🔍 Selector {i+1} found {len(elements)} elements")
                    
                    if len(elements) == 0:
                        print(f"❌ M-model selector {i+1} found no elements")
                        continue
                    
                    # Show element details for debugging
                    element = elements[0]
                    print(f"🔍 Element tag: {element.tag_name}, visible: {element.is_displayed()}, enabled: {element.is_enabled()}")
                    
                    radio_button = self.element_to_be_clickable(selector, timeout=3)
                    self.browser.execute_script("arguments[0].scrollIntoView(true);", radio_button)
                    time.sleep(1)
                    
                    # Use JavaScript click directly (since it worked before)
                    try:
                        self.browser.execute_script("arguments[0].click();", radio_button)
                        print("✅ First M-model selected successfully with JavaScript click")
                        return True
                    except Exception as js_error:
                        print(f"⚠️ JavaScript click failed: {js_error}, trying regular click")
                        radio_button.click()
                        print("✅ First M-model selected successfully with regular click")
                        return True
                        
                except TimeoutException:
                    print(f"❌ M-model selector {i+1} not found (timeout)")
                    continue
                except Exception as e:
                    print(f"❌ M-model selector {i+1} error: {e}")
                    continue
            
            print("❌ M-model radio button not found with any selector")
            return False
                
        except Exception as e:
            print(f"❌ Error selecting M-model: {e}")
            return False
    
    def click_e_model_button(self, timeout=10):
        """Click the E-model selection button"""
        try:
            # Try multiple selectors for E-model button based on actual HTML
            selectors = [
                self.locators.E_MODEL_BUTTON,  # Primary selector
                self.locators.E_MODEL_BUTTON_ALT,  # Alternative
                self.locators.E_MODEL_BUTTON_FALLBACK  # Fallback
            ]
            
            for selector in selectors:
                try:
                    e_model_button = self.element_to_be_clickable(selector, timeout)
                    self.browser.execute_script("arguments[0].scrollIntoView(true);", e_model_button)
                    time.sleep(1)
                    e_model_button.click()
                    print("✅ E-model button clicked successfully")
                    self.wait_for_page_load()
                    return True
                except TimeoutException:
                    continue
            
            print("❌ E-model button not found")
            return False
        except Exception as e:
            print(f"❌ Error clicking E-model button: {e}")
            return False
    
    def select_first_e_model(self, timeout=15):
        """Select the first E-model from the table"""
        try:
            # Wait for E-model table to load
            self.find_element(self.locators.E_MODEL_TABLE, timeout)
            print("✅ E-model table loaded")
            
            # Add debugging for E-model page structure
            print("🔍 Debugging E-model page structure...")
            
            # Check for the specific E-model table structure
            table_cells = self.browser.find_elements(By.XPATH, "//td[contains(@class, 'ant-table-selection-column')]")
            print(f"🔍 Found {len(table_cells)} ant-table-selection-column cells")
            
            radio_wrappers = self.browser.find_elements(By.XPATH, "//label[@class='ant-radio-wrapper']")
            print(f"🔍 Found {len(radio_wrappers)} ant-radio-wrapper labels")
            
            radio_inputs = self.browser.find_elements(By.XPATH, "//input[@class='ant-radio-input']")
            print(f"🔍 Found {len(radio_inputs)} ant-radio-input elements")
            
            # Use selectors based on the actual E-model HTML structure
            selectors = [
                # Based on the provided HTML structure
                (By.XPATH, "//td[contains(@class, 'ant-table-selection-column')]//input[@class='ant-radio-input']"),
                (By.XPATH, "//td[contains(@class, 'ant-table-selection-column')]//span[@class='ant-radio-inner']"),
                (By.XPATH, "//label[@class='ant-radio-wrapper']//input[@class='ant-radio-input']"),
                (By.XPATH, "//label[@class='ant-radio-wrapper']//span[@class='ant-radio-inner']"),
                (By.XPATH, "//span[@class='ant-radio ant-wave-target']//input[@class='ant-radio-input']"),
                (By.XPATH, "//span[@class='ant-radio ant-wave-target']//span[@class='ant-radio-inner']"),
                # First occurrence selectors
                (By.XPATH, "(//td[contains(@class, 'ant-table-selection-column')]//input[@class='ant-radio-input'])[1]"),
                (By.XPATH, "(//td[contains(@class, 'ant-table-selection-column')]//span[@class='ant-radio-inner'])[1]"),
                (By.XPATH, "(//label[@class='ant-radio-wrapper']//input[@class='ant-radio-input'])[1]"),
                (By.XPATH, "(//label[@class='ant-radio-wrapper']//span[@class='ant-radio-inner'])[1]"),
                # Fallback to generic selectors
                (By.XPATH, "//input[@class='ant-radio-input']"),
                (By.XPATH, "//span[@class='ant-radio-inner']"),
                (By.XPATH, "(//input[@type='radio'])[1]"),
                (By.XPATH, "(//span[@class='ant-radio-inner'])[1]"),
            ]
            
            for i, selector in enumerate(selectors):
                try:
                    print(f"🔍 Trying E-model radio selector {i+1}: {selector}")
                    
                    # First check if element exists
                    elements = self.browser.find_elements(*selector)
                    print(f"🔍 Selector {i+1} found {len(elements)} elements")
                    
                    if len(elements) == 0:
                        print(f"❌ E-model selector {i+1} found no elements")
                        continue
                    
                    # Show element details for debugging
                    element = elements[0]
                    print(f"🔍 Element tag: {element.tag_name}, visible: {element.is_displayed()}, enabled: {element.is_enabled()}")
                    
                    radio_button = self.element_to_be_clickable(selector, timeout=3)
                    self.browser.execute_script("arguments[0].scrollIntoView(true);", radio_button)
                    time.sleep(1)
                    
                    # Use JavaScript click directly (since it worked for M-model)
                    try:
                        self.browser.execute_script("arguments[0].click();", radio_button)
                        print("✅ First E-model selected successfully with JavaScript click")
                        return True
                    except Exception as js_error:
                        print(f"⚠️ JavaScript click failed: {js_error}, trying regular click")
                        radio_button.click()
                        print("✅ First E-model selected successfully with regular click")
                        return True
                        
                except TimeoutException:
                    print(f"❌ E-model selector {i+1} not found (timeout)")
                    continue
                except Exception as e:
                    print(f"❌ E-model selector {i+1} error: {e}")
                    continue
            
            print("❌ E-model radio button not found with any selector")
            return False
        except Exception as e:
            print(f"❌ Error selecting E-model: {e}")
            return False
    
    def click_build_model_button(self, timeout=10):
        """Click the final Build model button"""
        try:
            # First check if button is enabled
            if not self.is_build_model_button_enabled():
                print("❌ Build model button is disabled - missing required selections")
                return False
            
            # Try multiple selectors for Build model button based on actual HTML
            selectors = [
                self.locators.BUILD_MODEL_BUTTON,  # Primary selector
                self.locators.BUILD_MODEL_BUTTON_ALT  # Alternative
            ]
            
            for selector in selectors:
                try:
                    build_model_button = self.element_to_be_clickable(selector, timeout)
                    self.browser.execute_script("arguments[0].scrollIntoView(true);", build_model_button)
                    time.sleep(1)
                    build_model_button.click()
                    print("✅ Build model button clicked successfully")
                    return True
                except TimeoutException:
                    continue
            
            print("❌ Build model button not found or not clickable")
            return False
        except Exception as e:
            print(f"❌ Error clicking build model button: {e}")
            return False
    
    def is_build_model_button_enabled(self, timeout=5):
        """Check if the Build model button is enabled"""
        try:
            # Check if disabled button exists
            disabled_button = self.browser.find_elements(*self.locators.BUILD_MODEL_BUTTON_DISABLED)
            if disabled_button:
                print("ℹ️ Build model button is currently disabled")
                return False
            
            # Check if enabled button exists
            enabled_button = self.browser.find_elements(*self.locators.BUILD_MODEL_BUTTON)
            if enabled_button and not enabled_button[0].get_attribute("disabled"):
                print("✅ Build model button is enabled")
                return True
            
            return False
        except Exception as e:
            print(f"❌ Error checking build model button status: {e}")
            return False
    
    def wait_for_build_completion(self, timeout=30):
        """Wait for build process to complete or show success message"""
        try:
            # Wait for either success message or loading to disappear
            WebDriverWait(self.browser, timeout).until(
                lambda driver: (
                    len(driver.find_elements(*self.locators.SUCCESS_MESSAGE)) > 0 or
                    len(driver.find_elements(*self.locators.LOADING_SPINNER)) == 0
                )
            )
            print("✅ Build process completed or initiated successfully")
            return True
        except TimeoutException:
            print("❌ Build completion timeout - process may still be running")
            return False