# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException, NoSuchElementException
import logging

from locators.build_ic_locators import BuildIcLocators
from pages.home_page import HomePage


class BuildIcPage(HomePage):
    """Page object for Ion Channel build workflow"""
    
    def __init__(self, browser, wait, base_url, logger=None):
        super().__init__(browser, wait, base_url)
        self.base_url = base_url
        self.logger = logger or logging.getLogger(__name__)
        self.home_page = HomePage(browser, wait, base_url)

    def navigate_to_workflows(self, lab_id, project_id):
        """Navigate to the workflows page with specific lab and project ID"""
        workflows_url = f"{self.base_url}/app/virtual-lab/{lab_id}/{project_id}/workflows?activity=build"
        self.browser.get(workflows_url)
        self.wait_for_page_load()
        return workflows_url
    
    def wait_for_page_load(self, timeout=10):
        """Wait for page to load completely"""
        try:
            self.wait_for_page_ready(timeout)
            time.sleep(3)  # Wait for dynamic content
            
            try:
                spinner_locator = (By.XPATH, "//div[contains(@class, 'loading') or contains(@class, 'spinner')]")
                self.wait_for_element_to_disappear(spinner_locator, timeout=5)
            except:
                pass  # No spinners found, continue
                
        except Exception as e:
            print(f"Page load timeout - continuing anyway: {e}")

    def click_build_section(self, logger):
        """Click on Build button/section to get to build activities"""
        logger.info("Looking for Build button/section...")
        time.sleep(3)  # Wait for page elements to load
        
        # Try multiple selectors for the Build button/section
        build_btn = None
        build_selectors_to_try = [
            BuildIcLocators.BUILD_BUTTON,
            BuildIcLocators.BUILD_DIV,
            BuildIcLocators.BUILD_ANY,
            BuildIcLocators.BUILD_LINK,
            BuildIcLocators.BUILD_SPAN,
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

    def click_ion_channel_card(self, logger):
        """Click on Ion channel card"""
        logger.info("Looking for Ion channel card...")
        time.sleep(3)  # Wait for page elements to load
        
        # Try multiple selectors for the Ion channel card
        ion_channel_card = None
        selectors_to_try = [
            BuildIcLocators.ION_CHANNEL_CARD_PRIMARY,
            BuildIcLocators.ION_CHANNEL_CARD_COMBINED,
            BuildIcLocators.ION_CHANNEL_CARD_CLASS,
            BuildIcLocators.ION_CHANNEL_CARD_TEXT,
            BuildIcLocators.ION_CHANNEL_CARD_ANY,
            BuildIcLocators.ION_CHANNEL_CARD_BUTTON,
        ]
        
        for i, selector in enumerate(selectors_to_try):
            try:
                ion_channel_card = self.browser.find_element(*selector)
                logger.info(f"Found Ion channel card with selector {i+1}: {selector}")
                break
            except:
                logger.info(f"Selector {i+1} failed: {selector}")
                continue
        
        if not ion_channel_card:
            logger.error("Could not find Ion channel card with any selector")
            # Check page source for ion channel text
            page_source = self.browser.page_source
            if "ion channel" in page_source.lower():
                logger.info("Found 'ion channel' text in page source")
                # Try to find any clickable element containing ion channel
                try:
                    ion_channel_card = self.browser.find_element(*BuildIcLocators.ION_CHANNEL_CARD_CASE_INSENSITIVE)
                    logger.info("Found ion channel element with case-insensitive search")
                except:
                    logger.error("No ion channel element found even with case-insensitive search")
            else:
                logger.error("No 'ion channel' text found in page source")
            
            # Take screenshot for debugging
            self.browser.save_screenshot("debug_workflows_page.png")
            raise Exception("Cannot find Ion channel card on workflows page")
        
        assert ion_channel_card.is_displayed(), "Ion channel card is not displayed"
        ion_channel_card.click()
        logger.info("Clicked on Ion channel card")
        return True

    def fill_configuration_form(self, unique_name, dynamic_description, logger):
        """Fill in the configuration form with name and description"""
        # Wait a bit for the Info tab content to load
        time.sleep(2)
        
        # Fill name field - try multiple selectors with visibility wait
        name_field = None
        name_selectors = [
            BuildIcLocators.CONFIG_NAME_FIELD,
            BuildIcLocators.CONFIG_NAME_FIELD_ALT,
            BuildIcLocators.CONFIG_NAME_FIELD_FALLBACK,
        ]
        
        for i, selector in enumerate(name_selectors):
            try:
                # Use element_to_be_clickable which waits for visibility
                name_field = self.element_to_be_clickable(selector, timeout=10)
                logger.info(f"Found name field with selector {i+1}: {selector}")
                break
            except:
                logger.info(f"Name field selector {i+1} failed: {selector}")
                continue
        
        if not name_field:
            raise Exception("Cannot find name field")
            
        name_field.clear()
        name_field.send_keys(unique_name)
        logger.info(f"Filled name field with: {unique_name}")
        
        # Fill description field - try multiple selectors with visibility wait
        description_field = None
        description_selectors = [
            BuildIcLocators.CONFIG_DESCRIPTION_FIELD,
            BuildIcLocators.CONFIG_DESCRIPTION_FIELD_ALT,
            BuildIcLocators.CONFIG_DESCRIPTION_FIELD_FALLBACK,
        ]
        
        for i, selector in enumerate(description_selectors):
            try:
                # Use element_to_be_clickable which waits for visibility
                description_field = self.element_to_be_clickable(selector, timeout=10)
                logger.info(f"Found description field with selector {i+1}: {selector}")
                break
            except:
                logger.info(f"Description field selector {i+1} failed: {selector}")
                continue
        
        if not description_field:
            raise Exception("Cannot find description field")
            
        description_field.clear()
        description_field.send_keys(dynamic_description)
        logger.info(f"Filled description field with: {dynamic_description}")

        # Verify created by and created at fields are populated (make this optional)
        try:
            created_by_field = self.browser.find_element(*BuildIcLocators.CONFIG_CREATED_BY)
            if created_by_field.is_displayed() and created_by_field.text.strip():
                logger.info(f"Created by: {created_by_field.text}")
        except:
            logger.info("Created by field not found with expected selector, continuing...")
        
        try:
            created_at_field = self.browser.find_element(*BuildIcLocators.CONFIG_CREATED_AT)
            if created_at_field.is_displayed() and created_at_field.text.strip():
                logger.info(f"Created at: {created_at_field.text}")
        except:
            logger.info("Created at field not found with expected selector, continuing...")

    def click_m_model_button(self, logger):
        """Click on M-model button to proceed"""
        logger.info("Looking for M-model button...")
        time.sleep(3)
        
        # Try multiple selectors for M-model button
        m_model_btn = None
        m_model_selectors = [
            BuildIcLocators.M_MODEL_BUTTON_PRIMARY,
            BuildIcLocators.M_MODEL_BUTTON_TEXT,
            BuildIcLocators.M_MODEL_BUTTON_ANCESTOR,
            BuildIcLocators.M_MODEL_ANY,
        ]
        
        for i, selector in enumerate(m_model_selectors):
            try:
                m_model_btn = self.browser.find_element(*selector)
                logger.info(f"Found M-model button with selector {i+1}: {selector}")
                break
            except:
                logger.info(f"M-model selector {i+1} failed: {selector}")
                continue
        
        if not m_model_btn:
            raise Exception("Cannot find M-model button")
            
        assert m_model_btn.is_displayed(), "M-model button is not displayed"
        m_model_btn.click()
        logger.info("Clicked on M-model button")
        return True

    def select_recording_species_rat(self, logger):
        """Select Rat species in the recording modal to filter recordings."""
        try:
            dropdown = self.browser.find_element(*BuildIcLocators.RECORDING_SPECIES_DROPDOWN)
            if dropdown.is_displayed():
                dropdown.click()
                logger.info("Opened species dropdown in recording modal")
                time.sleep(1)
                options = self.browser.find_elements(*BuildIcLocators.RECORDING_SPECIES_OPTIONS)
                for option in options:
                    if "rat" in option.text.strip().lower():
                        option.click()
                        logger.info("Selected Rat species in recording modal")
                        time.sleep(3)
                        return True
                logger.warning("Rat option not found in species dropdown")
                # Close dropdown
                from selenium.webdriver.common.keys import Keys
                from selenium.webdriver.common.action_chains import ActionChains
                ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
        except Exception as e:
            logger.info(f"Species dropdown not available in recording modal: {e}")
        return False

    def select_model_via_radio_button(self, logger):
        """Select a random model by navigating to a random page and clicking a random radio button."""
        import random
        logger.info("Waiting for models table to load...")
        time.sleep(5)

        # Navigate to a random pagination page if pagination exists
        try:
            pagination_items = self.browser.find_elements(
                By.CSS_SELECTOR, "li.ant-pagination-item"
            )
            if len(pagination_items) > 1:
                # Pick a random page (not the currently active one)
                try:
                    active = self.browser.find_element(
                        By.CSS_SELECTOR, "li.ant-pagination-item-active"
                    )
                    active_num = active.text.strip()
                except Exception:
                    active_num = ""
                candidates = [p for p in pagination_items if p.text.strip() != active_num]
                if candidates:
                    target_page = random.choice(candidates)
                    self.browser.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'});", target_page
                    )
                    time.sleep(0.5)
                    target_page.click()
                    logger.info(f"Navigated to page {target_page.text.strip()}")
                    time.sleep(3)
        except Exception as e:
            logger.info(f"No pagination or could not navigate: {e}")

        # Find all radio buttons and pick a random one
        radio_btns = []
        radio_selectors = [
            BuildIcLocators.RADIO_BUTTON_ANT_INPUT,
            BuildIcLocators.RADIO_BUTTON_ANY,
        ]

        for selector in radio_selectors:
            try:
                radio_btns = self.browser.find_elements(*selector)
                if radio_btns:
                    logger.info(f"Found {len(radio_btns)} radio buttons")
                    break
            except Exception:
                continue

        if not radio_btns:
            logger.error("Cannot find any radio buttons")
            raise Exception("Cannot find radio buttons in the recordings table")

        # Pick a random radio button (skip first 2 to avoid test data)
        eligible = radio_btns[2:] if len(radio_btns) > 2 else radio_btns
        chosen_index = radio_btns.index(random.choice(eligible))

        # Try to extract the recording name from the row containing this radio button
        try:
            row = radio_btns[chosen_index].find_element(By.XPATH, "./ancestor::tr")
            cells = row.find_elements(By.TAG_NAME, "td")
            row_text = " | ".join(cell.text.strip() for cell in cells if cell.text.strip())
            logger.info(f"Selected ephys recording: {row_text}")
        except Exception as e:
            logger.info(f"Could not extract recording details from row: {e}")

        # Re-find and click the radio button to avoid stale element reference
        max_retries = 3
        for attempt in range(max_retries):
            try:
                fresh_radios = self.browser.find_elements(*radio_selectors[0])
                if not fresh_radios:
                    fresh_radios = self.browser.find_elements(*radio_selectors[-1])
                target = fresh_radios[chosen_index]
                self.browser.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", target
                )
                time.sleep(0.5)
                self.browser.execute_script("arguments[0].click();", target)
                logger.info("Clicked radio button to select model")
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.info(f"Stale element on attempt {attempt + 1}, retrying...")
                    time.sleep(2)
                    continue
                raise

        time.sleep(2)
        return True

    def click_e_model_button(self, logger):
        """Click on E-model button to proceed"""
        logger.info("Looking for E-model button...")
        time.sleep(3)
        
        # Try multiple selectors for E-model button
        e_model_btn = None
        e_model_selectors = [
            BuildIcLocators.E_MODEL_BUTTON_PRIMARY,
            BuildIcLocators.E_MODEL_BUTTON_TEXT,
            BuildIcLocators.E_MODEL_BUTTON_ANCESTOR,
            BuildIcLocators.E_MODEL_ANY,
        ]
        
        for i, selector in enumerate(e_model_selectors):
            try:
                e_model_btn = self.browser.find_element(*selector)
                logger.info(f"Found E-model button with selector {i+1}: {selector}")
                break
            except:
                logger.info(f"E-model selector {i+1} failed: {selector}")
                continue
        
        if not e_model_btn:
            raise Exception("Cannot find E-model button")
            
        assert e_model_btn.is_displayed(), "E-model button is not displayed"
        e_model_btn.click()
        logger.info("Clicked on E-model button")
        return True

    def click_initialization_tab(self, logger):
        """Click on Initialization tab"""
        logger.info("Looking for Initialization tab...")
        time.sleep(2)
        
        # Try multiple selectors for Initialization tab
        init_tab = None
        init_tab_selectors = [
            BuildIcLocators.INITIALIZATION_TAB_PRIMARY,
            BuildIcLocators.INITIALIZATION_TAB_TEXT,
            BuildIcLocators.INITIALIZATION_TAB_CONTAINS,
            BuildIcLocators.INITIALIZATION_TAB_ANY,
        ]
        
        for i, selector in enumerate(init_tab_selectors):
            try:
                init_tab = self.browser.find_element(*selector)
                logger.info(f"Found Initialization tab with selector {i+1}: {selector}")
                break
            except:
                logger.info(f"Initialization tab selector {i+1} failed: {selector}")
                continue
        
        if not init_tab:
            logger.info("Initialization tab not found")
            return False
            
        if init_tab.is_displayed():
            init_tab.click()
            logger.info("Clicked on Initialization tab")
            time.sleep(3)  # Wait for tab content to load
            return True
        else:
            logger.info("Initialization tab not displayed")
            return False

    def click_info_tab(self, logger):
        """Click on Info tab if it exists"""
        logger.info("Looking for Info tab...")
        time.sleep(2)
        
        # Try multiple selectors for Info tab
        info_tab = None
        info_tab_selectors = [
            BuildIcLocators.INFO_TAB_PRIMARY,
            BuildIcLocators.INFO_TAB_TEXT,
            BuildIcLocators.INFO_TAB_ANY,
        ]
        
        for i, selector in enumerate(info_tab_selectors):
            try:
                info_tab = self.browser.find_element(*selector)
                logger.info(f"Found Info tab with selector {i+1}: {selector}")
                break
            except:
                logger.info(f"Info tab selector {i+1} failed: {selector}")
                continue
        
        if not info_tab:
            logger.info("Info tab not found, may already be selected")
            return False
            
        if info_tab.is_displayed():
            info_tab.click()
            logger.info("Clicked on Info tab")
            time.sleep(2)
            return True
        else:
            logger.info("Info tab not displayed")
            return False

    def fill_info_form(self, unique_name, dynamic_description, logger):
        """Fill in the Info form with name and description"""
        # This is an alias for fill_configuration_form to maintain compatibility
        return self.fill_configuration_form(unique_name, dynamic_description, logger)

    def click_ion_channel_recording_button(self, logger):
        """Click the Ion channel recording field to open the recordings list.
        Works both when no recording is selected (placeholder) and when one is
        already selected (shows recording name with search icon).
        """
        logger.info("Looking for Ion channel recording field...")
        time.sleep(5)

        # First check if a recording is already selected — clear it by clicking the X
        try:
            close_btn = self.browser.find_element(*BuildIcLocators.RECORDING_BADGE_CLOSE_BTN)
            if close_btn.is_displayed():
                logger.info("Found previously selected recording, clearing it...")
                self.browser.execute_script("arguments[0].click();", close_btn)
                time.sleep(2)
                logger.info("Cleared previous recording selection")
        except:
            pass  # No previous selection, continue normally

        # Now find and click the recording field (should show placeholder or be clickable)
        select_recording_btn = None
        select_recording_selectors = [
            BuildIcLocators.CLICK_TO_SELECT_RECORDING_PRIMARY,
            BuildIcLocators.CLICK_TO_SELECT_RECORDING_DIV,
            BuildIcLocators.CLICK_TO_SELECT_RECORDING_ANY,
            BuildIcLocators.CLICK_TO_SELECT_RECORDING_PLACEHOLDER,
            BuildIcLocators.RECORDING_FIELD_WITH_SELECTION,
        ]
        
        for i, selector in enumerate(select_recording_selectors):
            try:
                select_recording_btn = self.browser.find_element(*selector)
                if select_recording_btn.is_displayed():
                    logger.info(f"Found recording field with selector {i+1}: {selector}")
                    break
                else:
                    select_recording_btn = None
            except:
                logger.info(f"Recording field selector {i+1} failed: {selector}")
                continue
        
        if not select_recording_btn:
            raise Exception("Cannot find Ion channel recording field")
        
        self.browser.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            select_recording_btn
        )
        time.sleep(2)
        
        try:
            select_recording_btn.click()
            logger.info("Clicked Ion channel recording field")
        except:
            self.browser.execute_script("arguments[0].click();", select_recording_btn)
            logger.info("Clicked Ion channel recording field using JavaScript")
        
        time.sleep(3)
        return True

    def click_public_tab(self, logger):
        """Click on Public tab in the recordings list"""
        logger.info("Looking for Public tab...")
        time.sleep(3)
        
        # Try multiple selectors for Public tab
        public_tab = None
        public_tab_selectors = [
            BuildIcLocators.PUBLIC_TAB_PRIMARY,
            BuildIcLocators.PUBLIC_TAB_TEXT,
            BuildIcLocators.PUBLIC_TAB_ROLE,
            BuildIcLocators.PUBLIC_TAB_ANY,
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
            logger.info("Public tab not found, may already be on public recordings...")
            return False
        else:
            assert public_tab.is_displayed(), "Public tab is not displayed"
            public_tab.click()
            logger.info("Clicked on Public tab")
            
            # Wait for public recordings to load
            time.sleep(3)
            logger.info("Public recordings loaded")
            return True

    def click_select_button_in_modal(self, logger):
        """Click the Select button in the modal footer after selecting a recording"""
        logger.info("Looking for Select button in modal...")
        time.sleep(2)
        
        # Try multiple selectors for Select button
        select_btn = None
        select_btn_selectors = [
            BuildIcLocators.SELECT_BUTTON_MODAL,
            BuildIcLocators.SELECT_BUTTON_PRIMARY,
            BuildIcLocators.SELECT_BUTTON_ANY,
        ]
        
        for i, selector in enumerate(select_btn_selectors):
            try:
                select_btn = self.element_to_be_clickable(selector, timeout=10)
                logger.info(f"Found Select button with selector {i+1}: {selector}")
                break
            except:
                logger.info(f"Select button selector {i+1} failed: {selector}")
                continue
        
        if not select_btn:
            raise Exception("Cannot find Select button in modal")
        
        # Click the Select button
        try:
            select_btn.click()
            logger.info("Clicked Select button in modal")
        except:
            # Try JavaScript click if regular click fails
            self.browser.execute_script("arguments[0].click();", select_btn)
            logger.info("Clicked Select button using JavaScript")
        
        # Wait for modal to close and selection to be applied
        time.sleep(3)
        logger.info("Recording selection confirmed")
        return True

    def click_equation_tab(self, tab_name, logger):
        """Click on an equation tab (m∞, τm, h∞, τh) to expand it"""
        logger.info(f"Looking for {tab_name} equation tab...")
        time.sleep(2)
        
        # Scroll to make sure tabs are visible
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
        time.sleep(1)
        
        # Try multiple selectors for the equation tab
        equation_tab = None
        equation_tab_selectors = [
            (By.XPATH, f"//button[.//span[contains(., '{tab_name}') and contains(., 'equation')]]"),
            (By.XPATH, f"//button[@role='button']//span[contains(text(), '{tab_name}')]"),
            (By.XPATH, f"//button[contains(., '{tab_name}')]//span[contains(., 'equation')]"),
        ]
        
        for i, selector in enumerate(equation_tab_selectors):
            try:
                equation_tab = self.element_to_be_clickable(selector, timeout=10)
                logger.info(f"Found {tab_name} equation tab with selector {i+1}: {selector}")
                break
            except:
                logger.info(f"{tab_name} equation tab selector {i+1} failed: {selector}")
                continue
        
        if not equation_tab:
            logger.info(f"Cannot find {tab_name} equation tab")
            return False
        
        # Scroll into view
        self.browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", equation_tab)
        time.sleep(1)
        
        # Click the tab to expand it
        try:
            equation_tab.click()
            logger.info(f"Clicked {tab_name} equation tab to expand")
        except:
            # Try JavaScript click if regular click fails
            self.browser.execute_script("arguments[0].click();", equation_tab)
            logger.info(f"Clicked {tab_name} equation tab using JavaScript")
        
        # Wait for tab to expand
        time.sleep(2)
        logger.info(f"{tab_name} equation tab expanded")
        return True

    def select_first_equation_option(self, tab_name, logger):
        """Select the first available equation option from the middle column"""
        logger.info(f"Looking for equation option for {tab_name}...")
        time.sleep(2)
        
        # Scroll to middle column area
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
        time.sleep(1)
        
        # Look for the specific button structure: button with class 'group relative w-full rounded-lg'
        equation_btn = None
        equation_btn_selectors = [
            # Most specific - the exact button structure from HTML
            (By.XPATH, "//button[@type='button' and contains(@class, 'group') and contains(@class, 'relative') and contains(@class, 'w-full') and contains(@class, 'rounded-lg')]"),
            # Fallback - any button with rounded-lg in middle column area
            (By.XPATH, "//div[contains(@class, 'flex-col')]//button[@type='button' and contains(@class, 'rounded-lg')]"),
            # Broader fallback
            (By.XPATH, "//button[@type='button' and contains(@class, 'rounded-lg') and contains(@class, 'border-2')]"),
        ]
        
        for i, selector in enumerate(equation_btn_selectors):
            try:
                # Find all matching buttons and get the first visible one
                buttons = self.browser.find_elements(*selector)
                logger.info(f"Found {len(buttons)} buttons with selector {i+1}")
                for btn in buttons:
                    try:
                        if btn.is_displayed() and btn.is_enabled():
                            equation_btn = btn
                            logger.info(f"Found visible equation option with selector {i+1}: {selector}")
                            break
                    except:
                        continue
                if equation_btn:
                    break
            except Exception as e:
                logger.info(f"Equation option selector {i+1} failed: {e}")
                continue
        
        if not equation_btn:
            logger.info(f"Cannot find equation option for {tab_name}, taking screenshot")
            self.browser.save_screenshot(f"debug_{tab_name}_equation_not_found.png")
            return False
        
        # Scroll into view
        self.browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", equation_btn)
        time.sleep(1)
        
        # Click the button
        try:
            equation_btn.click()
            logger.info(f"Selected equation option for {tab_name}")
        except:
            # Try JavaScript click if regular click fails
            self.browser.execute_script("arguments[0].click();", equation_btn)
            logger.info(f"Selected equation option for {tab_name} using JavaScript")
        
        # Wait for selection to register
        time.sleep(2)
        logger.info(f"Equation option for {tab_name} selected")
        return True

    def click_next_button(self, logger, tab_name=""):
        """Click the Next button to navigate to the next tab"""
        logger.info(f"Looking for Next button{' for ' + tab_name if tab_name else ''}...")
        time.sleep(2)
        
        # Try multiple selectors for Next button
        next_btn = None
        next_btn_selectors = [
            BuildIcLocators.NEXT_BUTTON_PRIMARY,
            BuildIcLocators.NEXT_BUTTON,
        ]
        
        for i, selector in enumerate(next_btn_selectors):
            try:
                next_btn = self.element_to_be_clickable(selector, timeout=10)
                logger.info(f"Found Next button with selector {i+1}: {selector}")
                break
            except:
                logger.info(f"Next button selector {i+1} failed: {selector}")
                continue
        
        if not next_btn:
            raise Exception("Cannot find Next button")
        
        # Click the button
        try:
            next_btn.click()
            logger.info(f"Clicked Next button{' for ' + tab_name if tab_name else ''}")
        except:
            # Try JavaScript click if regular click fails
            self.browser.execute_script("arguments[0].click();", next_btn)
            logger.info(f"Clicked Next button using JavaScript{' for ' + tab_name if tab_name else ''}")
        
        # Wait for next tab to load
        time.sleep(3)
        logger.info("Next tab loaded")
        return True

    def click_build_model_button(self, logger):
        """Click the Build model button (final step)"""
        logger.info("Looking for Build model button...")
        time.sleep(2)
        
        # Try multiple selectors for Build model button
        build_model_btn = None
        build_model_btn_selectors = [
            BuildIcLocators.BUILD_MODEL_BUTTON_ENABLED,
            BuildIcLocators.BUILD_MODEL_BUTTON_FINAL,
            BuildIcLocators.BUILD_MODEL_BUTTON,
            (By.XPATH, "//button[contains(., 'Build') and @type='submit']"),
            (By.XPATH, "//button[contains(., 'Build model')]"),
        ]
        
        for i, selector in enumerate(build_model_btn_selectors):
            try:
                build_model_btn = self.element_to_be_clickable(selector, timeout=5)
                logger.info(f"Found Build model button with selector {i+1}: {selector}")
                break
            except:
                logger.info(f"Build model button selector {i+1} failed: {selector}")
                continue
        
        if not build_model_btn:
            logger.info("Cannot find Build model button or it's still disabled")
            self.browser.save_screenshot("debug_build_model_button_not_found.png")
            return False
        
        # Click the button
        try:
            build_model_btn.click()
            logger.info("Clicked Build model button")
        except:
            # Try JavaScript click if regular click fails
            self.browser.execute_script("arguments[0].click();", build_model_btn)
            logger.info("Clicked Build model button using JavaScript")
        
        # Wait for build to start
        time.sleep(3)
        logger.info("Build model initiated")
        return True

    def click_configuration_tab(self, logger):
        """Click on the Configuration tab (top-level, sibling of Output tab)."""
        logger.info("Looking for Configuration tab...")
        time.sleep(2)
        try:
            config_tab = self.element_to_be_clickable(BuildIcLocators.CONFIGURATION_TAB, timeout=10)
            config_tab.click()
            logger.info("Clicked Configuration tab")
            time.sleep(2)
            return True
        except Exception as e:
            logger.warning(f"Configuration tab not found: {e}")
            return False

    def click_output_tab(self, logger):
        """Click on the Output tab to view build results"""
        logger.info("Looking for Output tab...")
        time.sleep(3)
        
        # Try multiple selectors for Output tab
        output_tab = None
        output_tab_selectors = [
            BuildIcLocators.OUTPUT_TAB,
            (By.XPATH, "//button[@role='tab'][contains(., 'Output')]"),
            (By.XPATH, "//*[@role='tab' and contains(text(), 'Output')]"),
        ]
        
        for i, selector in enumerate(output_tab_selectors):
            try:
                output_tab = self.element_to_be_clickable(selector, timeout=10)
                logger.info(f"Found Output tab with selector {i+1}: {selector}")
                break
            except:
                logger.info(f"Output tab selector {i+1} failed: {selector}")
                continue
        
        if not output_tab:
            logger.info("Cannot find Output tab")
            return False
        
        # Click the tab
        try:
            output_tab.click()
            logger.info("Clicked Output tab")
        except:
            # Try JavaScript click if regular click fails
            self.browser.execute_script("arguments[0].click();", output_tab)
            logger.info("Clicked Output tab using JavaScript")
        
        # Wait for tab content to load
        time.sleep(3)
        logger.info("Output tab loaded")
        return True

    def wait_for_build_completion(self, logger, timeout=120):
        """Wait for the build to complete (done badge appears).
        Returns 'done' if successful, 'failed' if build failed, or None if timeout.
        """
        logger.info(f"Waiting for build to complete (timeout: {timeout}s)...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Look for the "done" badge
                done_badge = self.browser.find_element(*BuildIcLocators.BUILD_STATUS_DONE)
                if done_badge.is_displayed():
                    logger.info("Build completed successfully - 'done' badge found")
                    return 'done'
            except:
                pass
            
            # Check if build failed
            try:
                failed_badge = self.browser.find_element(*BuildIcLocators.BUILD_STATUS_FAILED)
                if failed_badge.is_displayed():
                    logger.warning(f"Build FAILED - '{failed_badge.text.strip()}' badge found")
                    return 'failed'
            except:
                pass
            
            # Check if still running
            try:
                running_badge = self.browser.find_element(*BuildIcLocators.BUILD_STATUS_RUNNING)
                if running_badge.is_displayed():
                    logger.info("Build still running...")
            except:
                pass
            
            # Wait before checking again
            time.sleep(5)
        
        logger.info(f"Build did not complete within {timeout}s timeout")
        return None

    def verify_output_files_present(self, logger):
        """Verify that output files (MOD, PDF) are present in the Outputs section.
        Returns dict with 'MOD': bool, 'PDF': int (count), 'outputs_section': bool.
        """
        logger.info("Verifying output files are present...")
        time.sleep(2)

        results = {
            'MOD': False,
            'PDF': 0,
            'outputs_section': False,
        }

        # Check Outputs section header
        try:
            section = self.browser.find_element(*BuildIcLocators.OUTPUT_FILES_SECTION)
            if section.is_displayed():
                results['outputs_section'] = True
                logger.info("✓ Outputs section found")
        except Exception:
            logger.info("✗ Outputs section not found")

        # Check for MOD file button
        try:
            mod_btn = self.browser.find_element(*BuildIcLocators.OUTPUT_MOD_FILE)
            if mod_btn.is_displayed():
                results['MOD'] = True
                logger.info(f"✓ MOD file found: '{mod_btn.text.split(chr(10))[0]}'")
        except Exception:
            logger.info("✗ MOD file not found")

        # Check for PDF file buttons (there can be multiple)
        try:
            pdf_btns = self.browser.find_elements(*BuildIcLocators.OUTPUT_PDF_FILES)
            visible = [b for b in pdf_btns if b.is_displayed()]
            results['PDF'] = len(visible)
            logger.info(f"✓ {len(visible)} PDF file(s) found")
        except Exception:
            logger.info("✗ No PDF files found")

        return results

    def click_mod_file_and_verify_preview(self, logger, timeout=10):
        """Click the MOD output file and verify the code preview shows .mod content."""
        from selenium.webdriver.common.action_chains import ActionChains

        mod_btn = self.browser.find_element(*BuildIcLocators.OUTPUT_MOD_FILE)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", mod_btn)
        time.sleep(0.5)
        try:
            ActionChains(self.browser).move_to_element(mod_btn).click().perform()
        except Exception:
            self.browser.execute_script("arguments[0].click();", mod_btn)
        logger.info("Clicked MOD output file")
        time.sleep(2)

        # Verify code preview appears with NEURON mod content
        try:
            code_el = self.element_visibility(BuildIcLocators.OUTPUT_CODE_PREVIEW, timeout=timeout)
            preview_text = code_el.text.strip()
            logger.info(f"Code preview loaded ({len(preview_text)} chars)")
            has_content = len(preview_text) > 0 and 'NEURON' in preview_text
            if has_content:
                logger.info("✓ MOD file preview contains NEURON code")
            else:
                logger.warning(f"✗ MOD preview content unexpected: '{preview_text[:100]}...'")
            return has_content
        except Exception as e:
            logger.warning(f"✗ Code preview not found: {e}")
            return False
