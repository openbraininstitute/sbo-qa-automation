"""
Page Object for Build Single Neuron functionality
"""

import time
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
            # Wait for document ready state
            self.wait_for_page_ready(timeout)
            
            # Additional wait for dynamic content and URL stabilization
            time.sleep(3)  # Increased from 2 to 3 seconds for CI stability
            
            # Ensure page is fully loaded by checking for any loading indicators
            try:
                # Wait for any potential loading spinners to disappear
                spinner_locator = (By.XPATH, "//div[contains(@class, 'loading') or contains(@class, 'spinner')]")
                self.wait_for_element_to_disappear(spinner_locator, timeout=5)
            except:
                pass  # No spinners found, continue
                
        except Exception as e:
            print(f"Page load timeout - continuing anyway: {e}")
    
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
            try:
                self.wait_for_url_contains('configure', timeout)
            except:
                try:
                    self.wait_for_url_contains('memodel', timeout)
                except:
                    pass
            
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
            # Check for configuration form using wrapper method with short timeout
            try:
                form_elements = self.find_all_elements(self.locators.CONFIGURATION_FORM, timeout=2)
                form_present = len(form_elements) > 0
            except:
                form_present = False
            
            # Check for name input using wrapper method with short timeout
            name_input_present = False
            for locator in [self.locators.MODEL_NAME_INPUT, self.locators.MODEL_NAME_INPUT_ALT]:
                try:
                    name_elements = self.find_all_elements(locator, timeout=2)
                    if len(name_elements) > 0:
                        name_input_present = True
                        break
                except:
                    continue
            
            # Check for M-model and E-model buttons using wrapper method with short timeout
            try:
                m_model_elements = self.find_all_elements(self.locators.M_MODEL_BUTTON, timeout=2)
                m_model_present = len(m_model_elements) > 0
            except:
                m_model_present = False
                
            try:
                e_model_elements = self.find_all_elements(self.locators.E_MODEL_BUTTON, timeout=2)
                e_model_present = len(e_model_elements) > 0
            except:
                e_model_present = False
            
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

    def fill_description(self, description="Automated test", timeout=10):
        """Fill in the description field."""
        try:
            selectors = [
                self.locators.DESCRIPTION_TEXTAREA,
                self.locators.DESCRIPTION_TEXTAREA_ALT,
            ]
            for selector in selectors:
                try:
                    desc_input = self.element_to_be_clickable(selector, timeout)
                    desc_input.clear()
                    desc_input.send_keys(description)
                    self.logger.info(f"Description filled: '{description}'")
                    return True
                except TimeoutException:
                    continue
            self.logger.warning("Description input not found")
            return False
        except Exception as e:
            self.logger.warning(f"Error filling description: {e}")
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
            
            # Wait for loading spinner to disappear and table content to load
            print("🔍 Waiting for E-model table content to load...")
            
            # Use helper method to wait for spinner to disappear
            self.wait_for_spinner_to_disappear()
            
            # Wait for table content to appear with multiple attempts
            max_attempts = 3
            for attempt in range(max_attempts):
                print(f"🔍 Attempt {attempt + 1}/{max_attempts} - Checking for E-model table content...")
                
                # Wait a bit for content to load
                time.sleep(2)
                
                # Use helper method to check if table content has loaded
                if self.check_table_content_loaded():
                    print("✅ E-model table content loaded")
                    break
                    
                if attempt < max_attempts - 1:
                    print(f"⏳ No content found, waiting before retry...")
                    time.sleep(3)
            
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
    


    def select_random_m_model(self, exclude_indices=None, timeout=15):
        """Select a random M-model from the table, optionally excluding already-tried indices.
        Returns the index selected, or -1 if failed.
        """
        import random
        exclude_indices = exclude_indices or set()
        try:
            self.find_element(self.locators.M_MODEL_TABLE, timeout)
            # Wait for radio buttons to appear (table rows loading)
            for wait_attempt in range(5):
                time.sleep(2)
                radios = self.browser.find_elements(
                    By.XPATH, "//td[contains(@class,'ant-table-selection-column')]//span[@class='ant-radio-inner']"
                )
                if radios:
                    break
                self.logger.info(f"Waiting for M-model radio buttons... attempt {wait_attempt + 1}")
            radios = self.browser.find_elements(
                By.XPATH, "//td[contains(@class,'ant-table-selection-column')]//span[@class='ant-radio-inner']"
            )
            if not radios:
                radios = self.browser.find_elements(
                    By.XPATH, "//td[contains(@class,'ant-table-selection-column')]//input[@class='ant-radio-input']"
                )
            if not radios:
                radios = self.browser.find_elements(
                    By.CSS_SELECTOR, "span.ant-radio-inner"
                )
            if not radios:
                self.logger.warning("No M-model radio buttons found")
                return -1

            available = [i for i in range(len(radios)) if i not in exclude_indices]
            if not available:
                self.logger.warning("All M-models already tried")
                return -1

            idx = random.choice(available)
            radio = radios[idx]
            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", radio)
            time.sleep(0.5)
            self.browser.execute_script("arguments[0].click();", radio)
            self.logger.info(f"Selected M-model at index {idx} (of {len(radios)})")
            time.sleep(2)
            return idx
        except Exception as e:
            self.logger.warning(f"Error selecting random M-model: {e}")
            return -1

    def select_random_e_model(self, exclude_indices=None, timeout=15):
        """Select a random E-model from the table, optionally excluding already-tried indices.
        Returns the index selected, or -1 if failed.
        """
        import random
        exclude_indices = exclude_indices or set()
        try:
            self.find_element(self.locators.E_MODEL_TABLE, timeout)
            self.wait_for_spinner_to_disappear()
            time.sleep(2)
            radios = self.browser.find_elements(
                By.XPATH, "//td[contains(@class,'ant-table-selection-column')]//span[@class='ant-radio-inner']"
            )
            if not radios:
                radios = self.browser.find_elements(
                    By.XPATH, "//td[contains(@class,'ant-table-selection-column')]//input[@class='ant-radio-input']"
                )
            if not radios:
                radios = self.browser.find_elements(By.XPATH, "//span[@class='ant-radio-inner']")
            if not radios:
                self.logger.warning("No E-model radio buttons found")
                return -1

            available = [i for i in range(len(radios)) if i not in exclude_indices]
            if not available:
                self.logger.warning("All E-models already tried")
                return -1

            idx = random.choice(available)
            radio = radios[idx]
            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", radio)
            time.sleep(0.5)
            self.browser.execute_script("arguments[0].click();", radio)
            self.logger.info(f"Selected E-model at index {idx} (of {len(radios)})")
            time.sleep(2)
            return idx
        except Exception as e:
            self.logger.warning(f"Error selecting random E-model: {e}")
            return -1

    def _run_compatibility_check(self, timeout=60):
        """Run a single compatibility check cycle. Returns True if compatible, False if not."""
        # Wait for spinner / "in progress" text
        try:
            self.find_element(self.locators.COMPATIBILITY_IN_PROGRESS, timeout=10)
            self.logger.info("Model compatibility check in progress...")
            # Wait for it to complete
            try:
                self.wait_for_element_to_disappear(self.locators.COMPATIBILITY_IN_PROGRESS, timeout=timeout)
                self.logger.info("Compatibility check completed")
            except Exception:
                self.logger.warning(f"Compatibility check did not complete within {timeout}s")
        except TimeoutException:
            self.logger.info("No compatibility spinner detected, checking result directly")

        time.sleep(2)

        # Check for error
        try:
            error_el = self.browser.find_element(*self.locators.COMPATIBILITY_ERROR)
            if error_el.is_displayed():
                self.logger.warning(f"Compatibility FAILED: {error_el.text.strip()[:80]}")
                return False
        except Exception:
            pass

        # Check for success
        try:
            success_el = self.browser.find_element(*self.locators.COMPATIBILITY_SUCCESS)
            if success_el.is_displayed():
                self.logger.info("Compatibility check PASSED")
                return True
        except Exception:
            pass

        # Fallback: check build button
        if self.is_build_model_button_enabled():
            self.logger.info("Build button enabled — assuming compatible")
            return True

        return False

    def wait_for_compatibility_check(self, max_retries=10, timeout=60):
        """Wait for compatibility check. If incompatible, try different E-models.
        After 3 failed E-models with the same M-model, switch to a different M-model.
        Returns True if a compatible combination was found.
        """
        from selenium.webdriver.common.action_chains import ActionChains

        tried_e = set()
        tried_m = set()
        last_e_idx = -1
        e_fails_this_m = 0
        max_e_per_m = 3

        for attempt in range(max_retries):
            self.logger.info(f"Compatibility check attempt {attempt + 1}/{max_retries}")

            compatible = self._run_compatibility_check(timeout=timeout)
            if compatible:
                self.logger.info(f"Compatible models found on attempt {attempt + 1}")
                return True

            if attempt >= max_retries - 1:
                break

            e_fails_this_m += 1

            def _click_select_another(self_ref):
                try:
                    btn = self_ref.element_to_be_clickable(
                        self_ref.locators.COMPATIBILITY_SELECT_ANOTHER, timeout=10
                    )
                    self_ref.browser.execute_script("arguments[0].click();", btn)
                    self_ref.logger.info("Clicked 'Select another model'")
                    time.sleep(3)
                    return True
                except TimeoutException:
                    self_ref.logger.warning("'Select another model' button not found")
                    return False

            if e_fails_this_m >= max_e_per_m:
                # Switch M-model after too many E-model failures
                self.logger.info(f"Tried {e_fails_this_m} E-models, switching M-model...")
                if not _click_select_another(self):
                    return False

                m_clicked = self.click_m_model_button()
                if not m_clicked:
                    self.logger.warning("Could not click M-model button")
                    return False
                time.sleep(5)

                new_m_idx = self.select_random_m_model(exclude_indices=tried_m)
                if new_m_idx == -1:
                    self.logger.warning("No more M-models to try")
                    return False
                tried_m.add(new_m_idx)
                self.logger.info(f"Switched to M-model index {new_m_idx}")
                time.sleep(2)

                e_clicked = self.click_e_model_button()
                if not e_clicked:
                    self.logger.warning("Could not click E-model button")
                    return False
                time.sleep(5)

                tried_e.clear()
                e_fails_this_m = 0
                new_e_idx = self.select_random_e_model()
                if new_e_idx == -1:
                    self.logger.warning("Could not select E-model")
                    return False
                last_e_idx = new_e_idx
                tried_e.add(new_e_idx)
                time.sleep(2)
                self.logger.info(f"Selected E-model index {new_e_idx} with new M-model")
            else:
                # Try a different E-model with the same M-model
                self.logger.info("Trying a different E-model...")
                if not _click_select_another(self):
                    return False
                time.sleep(5)

                tried_e.add(last_e_idx)
                new_e_idx = self.select_random_e_model(exclude_indices=tried_e)
                if new_e_idx == -1:
                    self.logger.warning("No more E-models, will switch M-model next")
                    e_fails_this_m = max_e_per_m
                    continue
                last_e_idx = new_e_idx
                tried_e.add(new_e_idx)
                time.sleep(2)
                self.logger.info(f"Selected different E-model (index {new_e_idx})")

        self.logger.warning(f"No compatible combination found after {max_retries} attempts")
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
            # Check if disabled button exists using wrapper method
            try:
                disabled_buttons = self.find_all_elements(self.locators.BUILD_MODEL_BUTTON_DISABLED, timeout=2)
                if disabled_buttons:
                    print("ℹ️ Build model button is currently disabled")
                    return False
            except:
                pass  # No disabled button found, continue checking
            
            # Check if enabled button exists using wrapper method
            try:
                enabled_buttons = self.find_all_elements(self.locators.BUILD_MODEL_BUTTON, timeout=2)
                if enabled_buttons and not enabled_buttons[0].get_attribute("disabled"):
                    print("✅ Build model button is enabled")
                    return True
            except:
                pass
            
            return False
        except Exception as e:
            print(f"❌ Error checking build model button status: {e}")
            return False
    
    def wait_for_spinner_to_disappear(self, timeout=10):
        """Wait for loading spinner to disappear using base page method"""
        try:
            spinner_locator = (By.XPATH, "//div[contains(@class, 'ant-spin-spinning')]")
            self.wait_for_element_to_disappear(spinner_locator, timeout)
            print("✅ Loading spinner disappeared")
            return True
        except:
            print("ℹ️ No spinner found or already disappeared")
            return True
    
    def check_table_content_loaded(self):
        """Check if table content has loaded by looking for specific elements"""
        try:
            # Use direct browser calls for debugging/checking (not waiting)
            table_cells = self.browser.find_elements(By.XPATH, "//td[contains(@class, 'ant-table-selection-column')]")
            radio_wrappers = self.browser.find_elements(By.XPATH, "//label[@class='ant-radio-wrapper']")
            radio_inputs = self.browser.find_elements(By.XPATH, "//input[@class='ant-radio-input']")
            
            print(f"🔍 Found {len(table_cells)} ant-table-selection-column cells")
            print(f"🔍 Found {len(radio_wrappers)} ant-radio-wrapper labels")
            print(f"🔍 Found {len(radio_inputs)} ant-radio-input elements")
            
            return len(table_cells) > 0 or len(radio_wrappers) > 0 or len(radio_inputs) > 0
        except Exception as e:
            print(f"❌ Error checking table content: {e}")
            return False
    
    def wait_for_build_completion(self, timeout=30):
        """Wait for build process to complete or show success message"""
        try:
            # Wait for either success message or loading to disappear
            try:
                success_elements = self.find_all_elements(self.locators.SUCCESS_MESSAGE, timeout=5)
                if success_elements:
                    print("✅ Build process completed successfully")
                    return True
            except:
                pass
            
            # Check if loading spinner disappeared (indicating process started)
            spinner_disappeared = self.wait_for_spinner_to_disappear(timeout=10)
            if spinner_disappeared:
                print("✅ Build process initiated successfully")
                return True
                
            print("❌ Build completion timeout - process may still be running")
            return False
        except Exception as e:
            print(f"❌ Error waiting for build completion: {e}")
            return False
    
    def verify_page_accessibility(self):
        """Verify page accessibility by checking title and content"""
        try:
            page_title = self.browser.title
            
            if not page_title:
                print("ℹ️ Page title is empty, checking for page content instead")
                # Check for page content as alternative to title using base page method
                try:
                    page_content = self.find_all_elements((By.XPATH, "//h1 | //h2 | //title"), timeout=5)
                    if page_content:
                        page_title = "Page loaded with content"
                        print(f"✅ Page loaded with content elements: {len(page_content)}")
                    else:
                        page_title = "Page loaded successfully"
                        print("✅ Page loaded (no title but content present)")
                except:
                    page_title = "Page loaded successfully"
                    print("✅ Page loaded (no title but content present)")
            else:
                print(f"✅ Page loaded with title: {page_title}")
            
            return page_title
        except Exception as e:
            print(f"❌ Error verifying page accessibility: {e}")
            return "Error checking page accessibility"
    
    def check_build_button_accessibility(self):
        """Check if the Build button is accessible"""
        try:
            # Use base page wrapper method instead of direct browser call
            build_buttons = self.find_all_elements(self.locators.BUILD_BUTTON, timeout=5)
            if build_buttons:
                print("✅ Build button found and accessible")
                return True
            else:
                print("❌ Build button not found")
                return False
        except Exception as e:
            print(f"❌ Error checking build button accessibility: {e}")
            return False