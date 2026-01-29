# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from locators.ai_assistant_locators import AIAssistantLocators
from pages.project_home import ProjectHome


class AIAssistantPage(ProjectHome):
    """Page object for AI Assistant panel functionality."""
    
    def __init__(self, browser, wait, logger, base_url):
        super().__init__(browser, wait, logger, base_url)
        self.base_url = base_url
    
    def navigate_to_project_home(self, lab_id, project_id):
        """Navigate to the project home page."""
        self.logger.info(f"Navigating to project home for lab {lab_id}, project {project_id}")
        url = self.go_to_project_page(lab_id, project_id)
        time.sleep(3)  # Give the page time to fully render
        self.logger.info(f"✅ Successfully navigated to Project home: {url}")
    
    def find_ai_panel_button(self, timeout=10):
        """Find and return the AI assistant panel button."""
        self.logger.info("Looking for AI assistant panel button...")
        
        selectors = [
            AIAssistantLocators.AI_PANEL_BUTTON,
            AIAssistantLocators.AI_PANEL_BUTTON_ALT,
            AIAssistantLocators.AI_PANEL_BUTTON_CLASS
        ]
        
        for selector in selectors:
            try:
                button = self.element_to_be_clickable(selector, timeout=timeout)
                self.logger.info(f"Found AI assistant button with selector: {selector}")
                return button
            except TimeoutException:
                continue
        
        try:
            buttons = self.browser.find_elements(*self.get_by_tag("button"))
            for button in buttons:
                button_text = button.get_attribute("textContent") or ""
                aria_label = button.get_attribute("aria-label") or ""
                if any(keyword in (button_text + aria_label).lower() 
                      for keyword in ["ai", "assistant", "chat", "help"]):
                    self.logger.info(f"Found potential AI button with text: '{button_text}' and aria-label: '{aria_label}'")
                    return button
        except Exception as e:
            self.logger.warning(f"Error searching for AI button: {e}")
        
        raise NoSuchElementException("AI Assistant button not found")
    
    def open_ai_panel(self):
        """Open the AI assistant panel."""
        ai_button = self.find_ai_panel_button()
        self.scroll_to_element(ai_button)
        time.sleep(1)
        ai_button.click()
        self.logger.info("✅ Clicked AI assistant button")
        time.sleep(3)  # Wait for panel to open
    
    def find_suggested_questions(self):
        """Find and return list of suggested questions."""
        self.logger.info("Looking for suggestive questions...")
        
        # Wait a bit for the AI panel to fully load
        time.sleep(5)
        
        selectors = [
            AIAssistantLocators.SUGGESTED_QUESTIONS,
            AIAssistantLocators.SUGGESTED_QUESTIONS_ALT,
            AIAssistantLocators.SUGGESTED_QUESTIONS_FALLBACK
        ]
        
        for selector in selectors:
            try:
                elements = self.browser.find_elements(*selector)
                self.logger.info(f"Found {len(elements)} total elements with selector: {selector}")
                
                if elements:
                    # Log all found elements for debugging
                    for i, elem in enumerate(elements):
                        try:
                            if elem.is_displayed():
                                text = elem.get_attribute("textContent") or ""
                                self.logger.info(f"Element {i+1}: '{text.strip()[:100]}...'")
                        except:
                            pass
                    
                    # Filter elements to only include those that look like suggested questions
                    valid_questions = []
                    for elem in elements:
                        if elem.is_displayed():
                            text = elem.get_attribute("textContent") or ""
                            # Check if it looks like a suggested question
                            is_valid = self._is_valid_suggested_question(text, elem)
                            self.logger.info(f"Text: '{text.strip()[:50]}...' - Valid: {is_valid}")
                            if is_valid:
                                valid_questions.append(elem)
                    
                    if valid_questions:
                        self.logger.info(f"Found {len(valid_questions)} suggested questions with selector: {selector}")
                        # Log the text of found questions for debugging
                        for i, q in enumerate(valid_questions[:3]):  # Log first 3
                            try:
                                q_text = q.get_attribute("textContent") or ""
                                self.logger.info(f"Question {i+1}: '{q_text.strip()[:50]}...'")
                            except:
                                pass
                        return valid_questions
                    else:
                        self.logger.info(f"No valid questions found after filtering with selector: {selector}")
            except Exception as e:
                self.logger.info(f"Error with selector {selector}: {e}")
                continue
        
        # Fallback: try to find any buttons in the AI panel area
        self.logger.info("Trying fallback approach - looking for any buttons in AI panel area...")
        try:
            # Look for any buttons that might be suggested questions
            all_buttons = self.browser.find_elements(By.TAG_NAME, "button")
            self.logger.info(f"Found {len(all_buttons)} total buttons on page")
            
            potential_questions = []
            for i, button in enumerate(all_buttons):
                try:
                    if button.is_displayed():
                        text = button.get_attribute("textContent") or ""
                        if len(text.strip()) > 10:  # Only consider buttons with meaningful text
                            self.logger.info(f"Button {i+1}: '{text.strip()[:100]}...'")
                            # Use more lenient validation for fallback
                            if self._is_potential_question(text):
                                potential_questions.append(button)
                                self.logger.info(f"  -> Potential question: '{text.strip()[:50]}...'")
                except:
                    continue
            
            if potential_questions:
                self.logger.info(f"Found {len(potential_questions)} potential questions via fallback")
                return potential_questions[:3]  # Return first 3 potential questions
                
        except Exception as e:
            self.logger.info(f"Fallback approach failed: {e}")
        
        raise NoSuchElementException("No suggested questions found")
    
    def _is_valid_suggested_question(self, text, element):
        """Check if an element looks like a valid suggested question."""
        if not text or len(text.strip()) < 5:  # Too short to be a question
            return False
        
        text_lower = text.lower().strip()
        
        # Skip common UI buttons that are not questions
        skip_keywords = [
            'cancel', 'stop', 'clear', 'reset', 'new chat', 'history', 
            'edit', 'delete', 'save', 'close', 'minimize', 'maximize',
            'send', 'submit', 'ok', 'yes', 'no'
        ]
        
        if any(keyword in text_lower for keyword in skip_keywords):
            return False
        
        # Accept any text that's reasonably long (likely a suggested question)
        # Lowered threshold to be more inclusive
        if len(text.strip()) > 25:  # Most suggested questions are longer than 25 chars
            return True
        
        # Check for question indicators (very broad)
        question_indicators = [
            '?',  # Contains question mark
            'what', 'how', 'why', 'when', 'where', 'which', 'who',  # Question words
            'can you', 'could you', 'would you', 'do you', 'are you',  # Question phrases
            'tell me', 'show me', 'explain', 'describe', 'help', 'find',  # Request phrases
            'visualize', 'display', 'list', 'compare', 'analyze',  # Action words
            'brain', 'cerebrum', 'region', 'paper', 'circuit', 'knowledge'  # Domain-specific words
        ]
        
        if any(indicator in text_lower for indicator in question_indicators):
            return True
        
        return False
    
    def click_suggested_question(self, question_element, question_text=""):
        """Click on a suggested question with stale element handling."""
        if not question_text:
            try:
                question_text = question_element.get_attribute("textContent") or "Question"
            except Exception:
                question_text = "Question (text unavailable)"
        
        self.logger.info(f"Clicking suggested question: '{question_text}'")
        
        try:
            self.scroll_to_element(question_element)
            time.sleep(1)
            question_element.click()
            self.logger.info("✅ Clicked suggested question")
        except Exception as e:
            self.logger.warning(f"Failed to click question element: {e}")
            try:
                self.logger.info("Attempting to re-find question by text...")
                questions = self.find_suggested_questions()
                for q in questions:
                    try:
                        q_text = q.get_attribute("textContent") or ""
                        if question_text.strip() in q_text.strip() or q_text.strip() in question_text.strip():
                            self.scroll_to_element(q)
                            time.sleep(1)
                            q.click()
                            self.logger.info("✅ Successfully clicked re-found question")
                            return
                    except Exception:
                        continue
                
                if questions:
                    self.scroll_to_element(questions[0])
                    time.sleep(1)
                    questions[0].click()
                    self.logger.info("✅ Clicked first available question as fallback")
                else:
                    raise Exception("No suggested questions available")
                    
            except Exception as e2:
                self.logger.error(f"All attempts to click suggested question failed: {e2}")
                raise
    
    def wait_for_ai_response(self, timeout=30):
        """Wait for AI to provide a response."""
        self.logger.info("Waiting for AI response...")
        
        selectors = [
            AIAssistantLocators.AI_RESPONSE,
            AIAssistantLocators.AI_RESPONSE_ALT
        ]
        
        response_found = False
        for selector in selectors:
            try:
                self.wait.until(EC.presence_of_element_located(selector))
                self.logger.info(f"Found AI response with selector: {selector}")
                response_found = True
                break
            except TimeoutException:
                continue
        
        if not response_found:
            # Fallback: wait with timing
            time.sleep(10)
            self.logger.info("Waited for AI response (fallback timing)")
        
        # Now wait for the response to complete
        self.wait_for_ai_response_completion(timeout=60)
        
        self.logger.info("✅ AI response received and completed")
    
    def wait_for_ai_response_completion(self, timeout=60):
        """Wait for AI response to fully complete by waiting for cancel button to disappear."""
        self.logger.info("Waiting for AI response to complete (cancel button to disappear)...")
        
        # Wait for cancel button to disappear (indicates completion)
        cancel_selectors = [
            AIAssistantLocators.CANCEL_BUTTON,
            AIAssistantLocators.CANCEL_BUTTON_ALT,
            AIAssistantLocators.CANCEL_BUTTON_GENERIC
        ]
        
        cancel_disappeared = False
        for cancel_selector in cancel_selectors:
            try:
                # First check if cancel button exists
                cancel_elements = self.browser.find_elements(*cancel_selector)
                if cancel_elements:
                    self.logger.info(f"Found cancel button, waiting for it to disappear: {cancel_selector}")
                    # Wait for it to disappear
                    self.wait.until_not(EC.presence_of_element_located(cancel_selector))
                    self.logger.info(f"Cancel button disappeared: {cancel_selector}")
                    cancel_disappeared = True
                    break
            except TimeoutException:
                self.logger.info(f"Cancel button {cancel_selector} took too long to disappear or wasn't found")
                continue
            except Exception as e:
                self.logger.info(f"Error waiting for cancel button {cancel_selector}: {e}")
                continue
        
        if not cancel_disappeared:
            self.logger.info("No cancel button found or it didn't disappear, using fallback wait")
            time.sleep(10)  # Fallback wait
        
        self.logger.info("✅ AI response completion wait finished")
    
    def wait_for_ai_response_start(self, timeout=15):
        """Wait for AI to start responding (spinner appears)."""
        self.logger.info("Waiting for AI response to start...")
        
        spinner_selectors = [
            AIAssistantLocators.AI_SPINNER,
            AIAssistantLocators.AI_LOADING_INDICATOR
        ]
        
        spinner_found = False
        for selector in spinner_selectors:
            try:
                self.wait.until(EC.presence_of_element_located(selector))
                self.logger.info(f"Found AI spinner/loading indicator with selector: {selector}")
                spinner_found = True
                break
            except TimeoutException:
                continue
        
        if not spinner_found:
            # Fallback: short wait
            time.sleep(3)
            self.logger.info("Waited for AI response start (fallback timing)")
        
        self.logger.info("✅ AI response generation started")
    
    def find_cancel_button(self, timeout=10):
        """Find and return the cancel button that appears during AI response generation."""
        self.logger.info("Looking for cancel button...")
        
        selectors = [
            AIAssistantLocators.CANCEL_BUTTON,
            AIAssistantLocators.CANCEL_BUTTON_ALT,
            AIAssistantLocators.CANCEL_BUTTON_GENERIC
        ]
        
        for selector in selectors:
            try:
                button = self.element_to_be_clickable(selector, timeout=timeout)
                self.logger.info(f"Found cancel button with selector: {selector}")
                return button
            except TimeoutException:
                continue
        
        return None  # Cancel button might not be present or visible
    
    def cancel_ai_response(self):
        """Cancel the ongoing AI response generation."""
        cancel_button = self.find_cancel_button()
        if cancel_button:
            cancel_button.click()
            self.logger.info("✅ Clicked cancel button to stop AI response")
            time.sleep(2)  # Wait for cancellation to take effect
            return True
        else:
            self.logger.warning("Cancel button not found - AI response may have completed")
            return False
    
    def find_clear_chat_button(self, timeout=10):
        """Find and return the clear chat button."""
        self.logger.info("Looking for clear chat button...")
        
        selectors = [
            AIAssistantLocators.CLEAR_CHAT_BUTTON,
            AIAssistantLocators.CLEAR_CHAT_BUTTON_ALT,
            AIAssistantLocators.CLEAR_CHAT_BUTTON_TITLE,
            AIAssistantLocators.CLEAR_CHAT_BUTTON_TEXT,
            AIAssistantLocators.CLEAR_CHAT_BUTTON_FALLBACK,
            AIAssistantLocators.CLEAR_CHAT_BUTTON_GENERIC
        ]
        
        for selector in selectors:
            try:
                button = self.element_to_be_clickable(selector, timeout=timeout)
                self.logger.info(f"Found clear button with selector: {selector}")
                return button
            except TimeoutException:
                continue
        
        raise NoSuchElementException("Clear chat button not found")
    
    def clear_chat(self, timeout=15):
        """Clear the chat conversation."""
        self.logger.info("Attempting to clear chat...")
        
        # Try to find and click clear chat button
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                clear_button = self.find_clear_chat_button(timeout=5)
                clear_button.click()
                self.logger.info("✅ Successfully clicked clear chat button")
                time.sleep(2)
                return
            except NoSuchElementException:
                if attempt < max_attempts - 1:
                    self.logger.info(f"Clear chat button not available, waiting... (attempt {attempt + 1}/{max_attempts})")
                    time.sleep(5)
                else:
                    self.logger.error("Clear chat button not found after multiple attempts")
                    raise
    
    def find_history_button(self, timeout=10):
        """Find and return the history button."""
        self.logger.info("Looking for history button...")
        
        selectors = [
            AIAssistantLocators.HISTORY_BUTTON,
            AIAssistantLocators.HISTORY_BUTTON_ALT,
            AIAssistantLocators.HISTORY_BUTTON_SVG,
            AIAssistantLocators.HISTORY_BUTTON_FALLBACK,
            AIAssistantLocators.HISTORY_BUTTON_GENERIC
        ]
        
        for selector in selectors:
            try:
                button = self.element_to_be_clickable(selector, timeout=timeout)
                self.logger.info(f"Found history button with selector: {selector}")
                return button
            except TimeoutException:
                continue

        return None
    
    def open_history(self):
        """Open the chat history."""
        history_button = self.find_history_button()
        if history_button:
            history_button.click()
            self.logger.info("✅ Clicked history button")
            time.sleep(2)
            return True
        else:
            self.logger.warning("History button not found - this might be expected if history is always visible")
            return False
    
    def find_history_items(self):
        """Find and return chat history items."""
        self.logger.info("Looking for chat history items...")
        
        selectors = [
            AIAssistantLocators.HISTORY_ITEMS,
            AIAssistantLocators.HISTORY_ITEMS_ALT,
            AIAssistantLocators.TODAY_HISTORY_CARDS,
            AIAssistantLocators.TODAY_HISTORY_THREADS
        ]
        
        for selector in selectors:
            try:
                items = self.browser.find_elements(*selector)
                if items:
                    visible_items = [item for item in items if item.is_displayed()]
                    if visible_items:
                        self.logger.info(f"Found {len(visible_items)} history items with selector: {selector}")
                        return visible_items
            except Exception:
                continue
        
        return []
    
    def find_today_history_section(self):
        """Find the 'Today' history section."""
        try:
            today_section = self.find_element(AIAssistantLocators.TODAY_HISTORY_SECTION, timeout=5)
            self.logger.info("Found 'Today' history section")
            return today_section
        except Exception:
            self.logger.info("'Today' history section not found")
            return None
    
    def find_today_history_threads(self):
        """Find today's history thread cards."""
        self.logger.info("Looking for today's history threads...")
        
        selectors = [
            AIAssistantLocators.TODAY_HISTORY_CARDS,
            AIAssistantLocators.TODAY_HISTORY_THREADS,
            AIAssistantLocators.TODAY_CURRENT_THREAD
        ]
        
        for selector in selectors:
            try:
                threads = self.browser.find_elements(*selector)
                if threads:
                    visible_threads = [thread for thread in threads if thread.is_displayed()]
                    if visible_threads:
                        self.logger.info(f"Found {len(visible_threads)} today's threads with selector: {selector}")
                        return visible_threads
            except Exception:
                continue
        
        return []
    
    def get_history_thread_texts(self, threads):
        """Extract text content from history thread buttons."""
        thread_texts = []
        for i, thread in enumerate(threads):
            try:
                main_button = thread.find_element(*AIAssistantLocators.HISTORY_THREAD_BUTTON)
                thread_text = main_button.get_attribute("textContent") or ""
                if thread_text.strip():
                    thread_texts.append(thread_text.strip())
                    self.logger.info(f"Thread {i+1}: '{thread_text.strip()}'")
            except Exception as e:
                try:
                    thread_text = thread.get_attribute("textContent") or ""
                    if thread_text.strip():
                        cleaned_text = ' '.join(thread_text.split())
                        thread_texts.append(cleaned_text)
                        self.logger.info(f"Thread {i+1} (fallback): '{cleaned_text[:100]}...'")
                except Exception as e2:
                    self.logger.warning(f"Could not extract text from thread {i+1}: {e2}")
        
        return thread_texts
    
    def verify_chat_history(self):
        """Verify that chat history contains items, specifically looking for today's queries."""
        today_section = self.find_today_history_section()
        
        if today_section:
            self.logger.info("✅ Found 'Today' history section")
            
            today_threads = self.find_today_history_threads()
            
            if today_threads:
                self.logger.info(f"✅ Found {len(today_threads)} today's history threads")
                
                thread_texts = self.get_history_thread_texts(today_threads)
                
                if thread_texts:
                    self.logger.info(f"✅ Successfully extracted {len(thread_texts)} thread texts from today's history")
                    for i, text in enumerate(thread_texts):
                        self.logger.info(f"Today's thread {i+1}: {text[:100]}...")
                    return True
                else:
                    self.logger.warning("Found today's threads but could not extract text content")
            else:
                self.logger.warning("Found 'Today' section but no threads within it")
        
        history_items = self.find_history_items()
        
        if history_items:
            self.logger.info(f"✅ Found {len(history_items)} general history items")
            
            for i, item in enumerate(history_items[:3]):  # Show first 3 items
                try:
                    item_text = item.get_attribute("textContent") or ""
                    if item_text:
                        cleaned_text = ' '.join(item_text.split())  # Clean whitespace
                        self.logger.info(f"History item {i+1}: {cleaned_text[:100]}...")
                except Exception:
                    pass
            return True
        else:
            self.logger.warning("No chat history items found")
            return False
    
    def scroll_to_element(self, element):
        """Scroll element into view."""
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    
    def get_by_tag(self, tag_name):
        """Helper method to get By.TAG_NAME tuple."""
        from selenium.webdriver.common.by import By
        return (By.TAG_NAME, tag_name)
    
    def _is_potential_question(self, text):
        """More lenient check for potential questions (used in fallback)."""
        if not text or len(text.strip()) < 10:
            return False
        
        text_lower = text.lower().strip()
        
        # Skip obvious UI buttons
        skip_keywords = [
            'cancel', 'stop', 'clear', 'reset', 'new chat', 'history', 
            'edit', 'delete', 'save', 'close', 'minimize', 'maximize',
            'send', 'submit', 'ok', 'yes', 'no', 'login', 'logout'
        ]
        
        if any(keyword in text_lower for keyword in skip_keywords):
            return False
        
        # More lenient - accept longer text that could be questions
        if len(text.strip()) > 20:  # Longer text is likely a suggested question
            return True
        
        # Check for question indicators (more lenient)
        question_indicators = [
            '?', 'what', 'how', 'why', 'when', 'where', 'which', 'who',
            'can', 'could', 'would', 'do', 'are', 'is', 'will',
            'tell', 'show', 'explain', 'describe', 'help', 'find'
        ]
        
        if any(indicator in text_lower for indicator in question_indicators):
            return True
        
        return False