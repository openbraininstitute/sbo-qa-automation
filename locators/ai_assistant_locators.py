# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class AIAssistantLocators:
    """Locators for AI Assistant panel elements."""
    
    # AI Assistant Panel Button (to open/close panel)
    AI_PANEL_BUTTON = (By.CSS_SELECTOR, "#workspace-ai button[aria-label='expand AI assistant']")
    AI_PANEL_BUTTON_ALT = (By.XPATH, "//button[contains(text(), 'AI') or contains(text(), 'Assistant')]")
    AI_PANEL_BUTTON_CLASS = (By.CSS_SELECTOR, "button[class*='ai'], button[class*='assistant'], .ai-button, .assistant-button")
    
    # Suggested Questions
    SUGGESTED_QUESTIONS = (By.CSS_SELECTOR, "[data-testid*='suggestion'], [data-testid*='question'], .suggestion, .suggested-question, .ai-suggestion")
    SUGGESTED_QUESTIONS_ALT = (By.XPATH, "//button[contains(@class, 'suggestion')] | //div[contains(@class, 'suggestion')]//button")
    SUGGESTED_QUESTIONS_FALLBACK = (By.XPATH, "//div[contains(@class, 'ai') or contains(@class, 'assistant')]//button[contains(text(), '?') or contains(@class, 'suggestion') or contains(@class, 'question')]")
    
    # AI Response Elements
    AI_RESPONSE = (By.CSS_SELECTOR, "[data-testid*='response'], [data-testid*='message'], .ai-response, .message, .response")
    AI_RESPONSE_ALT = (By.XPATH, "//div[contains(@class, 'response') or contains(@class, 'message')]")
    
    # AI Loading/Spinner Elements
    AI_SPINNER = (By.CSS_SELECTOR, ".spinner-module__ahu-LG__spinner")
    AI_LOADING_INDICATOR = (By.CSS_SELECTOR, "div[class*='waveLoader']")
    
    # Cancel Button (appears during AI response generation)
    CANCEL_BUTTON = (By.XPATH, "//div[contains(@class,'cancelButton')]//button")
    CANCEL_BUTTON_ALT = (By.XPATH, "//div[contains(@class, 'cancelButton')]//button[text()='Cancel']")
    CANCEL_BUTTON_GENERIC = (By.XPATH, "//button[text()='Cancel' or text()='Stop']")
    CANCEL_BUTTON_CONTAINER = (By.XPATH, "//div[contains(@class,'cancelButton')]")
    
    # Clear/Reset Chat Button
    CLEAR_CHAT_BUTTON = (By.CSS_SELECTOR, "button.chat-module__71EZLa__actionButton")
    CLEAR_CHAT_BUTTON_ALT = (By.XPATH, "//button[contains(@class, 'actionButton')]//div[text()='New Chat']")
    CLEAR_CHAT_BUTTON_TITLE = (By.XPATH, "//button//svg//title[text()='Clear']")
    CLEAR_CHAT_BUTTON_TEXT = (By.XPATH, "//button//div[text()='New Chat']")
    CLEAR_CHAT_BUTTON_FALLBACK = (By.CSS_SELECTOR, "[data-testid*='clear'], [data-testid*='reset'], [aria-label*='clear'], [aria-label*='reset']")
    CLEAR_CHAT_BUTTON_GENERIC = (By.XPATH, "//button[contains(text(), 'Clear') or contains(text(), 'Reset') or contains(text(), 'New')]")
    
    # History Button
    HISTORY_BUTTON = (By.XPATH, "//nav//button[.//svg//title[text()='History']]")
    HISTORY_BUTTON_ALT = (By.XPATH, "//button//div[text()='History']")
    HISTORY_BUTTON_SVG = (By.XPATH, "//button[contains(@class, '') and .//svg//title[text()='History']]")
    HISTORY_BUTTON_FALLBACK = (By.CSS_SELECTOR, "[data-testid*='history'], [aria-label*='history'], .history-button, .history")
    HISTORY_BUTTON_GENERIC = (By.XPATH, "//button[contains(text(), 'History') or contains(text(), 'Previous') or contains(text(), 'Past')]")
    
    # History Items
    HISTORY_ITEMS = (By.CSS_SELECTOR, "[data-testid*='history-item'], [data-testid*='chat-item'], .history-item, .chat-item, .conversation")
    HISTORY_ITEMS_ALT = (By.XPATH, "//div[contains(@class, 'history')]//div[contains(@class, 'item')]")
    
    # Today's History Section
    TODAY_HISTORY_SECTION = (By.XPATH, "//h1[text()='Today']")
    TODAY_HISTORY_CARDS = (By.XPATH, "//h1[text()='Today']/following-sibling::div[contains(@class, 'card')]")
    TODAY_HISTORY_THREADS = (By.CSS_SELECTOR, ".history-module__qIgbEa__card")
    TODAY_CURRENT_THREAD = (By.CSS_SELECTOR, ".history-module__qIgbEa__currentThread")
    
    # History Thread Buttons
    HISTORY_THREAD_BUTTON = (By.CSS_SELECTOR, ".history-module__qIgbEa__mainButton")
    HISTORY_THREAD_BUTTON_ALT = (By.XPATH, "//button[contains(@class, 'mainButton')]")
    HISTORY_EDIT_BUTTON = (By.XPATH, "//button//svg//title[text()='Edit']")
    HISTORY_DELETE_BUTTON = (By.XPATH, "//button[contains(@class,'delete')]//svg//title[text()='Delete']/ancestor::button")
    HISTORY_DELETE_BUTTONS_ALL = (By.XPATH, "//button[contains(@class,'delete') and .//svg//title[text()='Delete']]")
    HISTORY_DELETE_CONFIRM_BTN = (By.XPATH, "//dialog[contains(@class,'dialogDelete')]//button[.//span[text()='Confirm']]")
    HISTORY_DELETE_CANCEL_BTN = (By.XPATH, "//dialog[contains(@class,'dialogDelete')]//button[.//span[text()='Cancel']]")
    HISTORY_LOAD_MORE_BTN = (By.XPATH, "//button[.//div[text()='Load more']]")
    
    # AI Panel Container
    AI_PANEL_CONTAINER = (By.CSS_SELECTOR, "#workspace-ai")
    AI_PANEL_CONTAINER_ALT = (By.CSS_SELECTOR, "div[class*='aiPanel']")
    AI_PANEL_OPEN = (By.XPATH, "//div[@id='workspace-ai' and not(contains(@class,'rounded-full'))]")