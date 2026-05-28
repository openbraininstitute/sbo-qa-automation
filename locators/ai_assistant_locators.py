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
    SUGGESTED_QUESTIONS = (By.XPATH, "//div[contains(@class,'suggested-questions-module') and contains(@class,'__suggestions')]//button")
    SUGGESTED_QUESTIONS_ALT = (By.XPATH, "//div[contains(@class,'__suggestedQuestionsContainer')]//button")
    SUGGESTED_QUESTIONS_FALLBACK = (By.XPATH, "//div[contains(@class,'suggested-questions')]//button[.//svg and .//div]")
    
    # AI Response Elements
    AI_RESPONSE = (By.CSS_SELECTOR, "[data-testid*='response'], [data-testid*='message'], .ai-response, .message, .response")
    AI_RESPONSE_ALT = (By.XPATH, "//div[contains(@class, 'response') or contains(@class, 'message')]")
    
    # AI Loading/Spinner Elements
    AI_SPINNER = (By.CSS_SELECTOR, ".spinner-module__ahu-LG__spinner")
    AI_LOADING_INDICATOR = (By.CSS_SELECTOR, "div[class*='waveLoader']")
    
    # Cancel Button (appears during AI response generation)
    CANCEL_BUTTON = (By.XPATH, "//button[@aria-label='Cancel']")
    CANCEL_BUTTON_ALT = (By.XPATH, "//button[contains(@class,'__stopButton')]")
    CANCEL_BUTTON_GENERIC = (By.XPATH, "//button[@aria-label='Cancel' or text()='Cancel' or text()='Stop']")
    CANCEL_BUTTON_CONTAINER = (By.XPATH, "//button[contains(@class,'stopButton')]")
    
    # Clear/Reset Chat Button
    CLEAR_CHAT_BUTTON = (By.XPATH, "//button[@aria-label='New Chat' or @title='New Chat']")
    CLEAR_CHAT_BUTTON_ALT = (By.XPATH, "//button[contains(@class,'__newChatBtn')]")
    CLEAR_CHAT_BUTTON_TITLE = (By.XPATH, "//button[.//svg//title[text()='New Chat']]")
    CLEAR_CHAT_BUTTON_TEXT = (By.XPATH, "//button//div[text()='New Chat']")
    CLEAR_CHAT_BUTTON_FALLBACK = (By.CSS_SELECTOR, "[aria-label='New Chat']")
    CLEAR_CHAT_BUTTON_GENERIC = (By.XPATH, "//button[contains(text(), 'Clear') or contains(text(), 'Reset') or contains(text(), 'New')]")
    
    # History Button
    CHAT_TAB_BUTTON = (By.XPATH, "//button[@aria-label='New Chat' or @title='New Chat']")
    HISTORY_BUTTON = (By.XPATH, "//button[@aria-label='History' or @title='History']")
    NEW_CHAT_BUTTON = (By.XPATH, "//button[@aria-label='New Chat' or @title='New Chat']")
    HISTORY_BUTTON_ALT = (By.XPATH, "//button[.//svg//title[text()='History']]")
    HISTORY_BUTTON_SVG = (By.XPATH, "//button[contains(@class,'__historyBtn')]")
    HISTORY_BUTTON_FALLBACK = (By.CSS_SELECTOR, "[aria-label='History']")
    HISTORY_BUTTON_GENERIC = (By.XPATH, "//button[contains(text(), 'History')]")
    
    # History Items
    HISTORY_ITEMS = (By.CSS_SELECTOR, "[data-testid*='history-item'], [data-testid*='chat-item']")
    HISTORY_ITEMS_ALT = (By.XPATH, "//div[contains(@class, 'history')]//div[contains(@class, 'item')]")
    
    # Today's History Section
    TODAY_HISTORY_SECTION = (By.XPATH, "//h1[text()='Today']")
    TODAY_HISTORY_CARDS = (By.XPATH, "//h1[text()='Today']/following-sibling::div[contains(@class, 'card')]")
    TODAY_HISTORY_THREADS = (By.XPATH, "//div[contains(@class,'__card')]")
    TODAY_CURRENT_THREAD = (By.XPATH, "//div[contains(@class,'__currentThread')]")
    
    # History Thread Buttons
    HISTORY_THREAD_BUTTON = (By.XPATH, "//button[contains(@class,'__mainButton')]")
    HISTORY_THREAD_BUTTON_ALT = (By.XPATH, "//button[contains(@class, 'mainButton')]")
    HISTORY_EDIT_BUTTON = (By.XPATH, "//button[contains(@class,'__edit')]")
    HISTORY_DELETE_BUTTON = (By.XPATH, "//button[contains(@class,'__delete')]")
    HISTORY_DELETE_BUTTONS_ALL = (By.XPATH, "//button[contains(@class,'__delete')]")
    HISTORY_DELETE_CONFIRM_BTN = (By.XPATH, "//dialog[contains(@class,'dialogDelete')]//button[.//span[text()='Confirm']]")
    HISTORY_DELETE_CANCEL_BTN = (By.XPATH, "//dialog[contains(@class,'dialogDelete')]//button[.//span[text()='Cancel']]")
    HISTORY_LOAD_MORE_BTN = (By.XPATH, "//button[.//div[text()='Load more']]")
    
    # AI Panel Container
    AI_PANEL_CONTAINER = (By.CSS_SELECTOR, "#workspace-ai")
    AI_PANEL_CONTAINER_ALT = (By.CSS_SELECTOR, "div[class*='aiPanel']")
    AI_PANEL_OPEN = (By.XPATH, "//div[@id='workspace-ai' and not(contains(@class,'rounded-full'))]")