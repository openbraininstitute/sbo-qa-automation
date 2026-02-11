# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class WorkflowLocators:
    # Category buttons
    CATEGORY_BUILD = (By.XPATH, "(//div[@role='group' and @aria-roledescription='slide'])[1]")
    CATEGORY_SIMULATE = (By.XPATH, "(//div[@data-slot='card'])[2]")
    
    # Type carousel container
    TYPE_CAROUSEL = (By.CSS_SELECTOR, "#workflow-category-menu")
    TYPE_CAROUSEL_HEADER = (By.XPATH, "//h1[text()='Type']")
    
    # Build type cards (clickable cards with aria-disabled="false")
    BUILD_SINGLE_NEURON = (By.XPATH, "//div[@data-slot='card' and @aria-disabled='false']//div[text()='Single neuron']")
    BUILD_SYNAPTOME = (By.XPATH, "//div[@data-slot='card' and @aria-disabled='false']//div[text()='Synaptome']")
    BUILD_ION_CHANNEL = (By.XPATH, "//div[@data-slot='card' and @aria-disabled='false']//div[text()='Ion channel']")
    
    # Simulate type cards
    # Non-beta cards - must NOT contain "beta" anywhere
    SIMULATE_SINGLE_NEURON = (By.XPATH, "//div[@data-slot='card']//div[@data-slot='card-title'][contains(., 'Single neuron') and not(contains(., 'beta'))]")
    SIMULATE_SYNAPTOME = (By.XPATH, "//div[@data-slot='card']//div[@data-slot='card-title'][contains(., 'Synaptome') and not(contains(., 'beta'))]")
    
    # Beta cards - contain "(beta)" in the text (same pattern as non-beta cards)
    SIMULATE_SINGLE_NEURON_BETA = (By.XPATH, "//div[@data-slot='card']//div[@data-slot='card-title'][contains(., 'Single neuron (beta)')]")
    SIMULATE_SYNAPTOME_BETA = (By.XPATH, "//div[@data-slot='card']//div[@data-slot='card-title'][contains(., 'Synaptome (beta)')]")
    SIMULATE_PAIRED_NEURONS_BETA = (By.XPATH, "//div[@data-slot='card']//div[@data-slot='card-title'][contains(., 'Paired neurons (beta)')]")
    # Note: Small microcircuit beta does not exist in staging environment
    
    # All type cards (for verification)
    ALL_TYPE_CARDS = (By.XPATH, "//div[@data-slot='card']")
    CLICKABLE_TYPE_CARDS = (By.XPATH, "//div[@data-slot='card' and @aria-disabled='false']")
    DISABLED_TYPE_CARDS = (By.XPATH, "//div[@data-slot='card' and @aria-disabled='true']")
    
    # Carousel navigation
    CAROUSEL_PREV_BUTTON = (By.XPATH, "//button//span[@aria-label='left']")
    CAROUSEL_NEXT_BUTTON = (By.XPATH, "//button//span[@aria-label='right']")
    
    # Recent activities section
    RECENT_ACTIVITIES_SECTION = (By.CSS_SELECTOR, "#workflow-activity-content")
    ACTIVITY_TABLE_SECTION = (By.CSS_SELECTOR, "#activity-table-with-filters")
    
    # Category and Type dropdowns
    CATEGORY_DROPDOWN = (By.XPATH, "//div[contains(text(), 'Category')]/following-sibling::button[@role='combobox']")
    TYPE_DROPDOWN = (By.XPATH, "//div[contains(text(), 'Type')]/following-sibling::button[@role='combobox']")
    
    # Empty state message
    NO_ACTIVITIES_MESSAGE = (By.XPATH, "//*[contains(text(), 'do not have') or contains(text(), 'No activities') or contains(text(), 'no activities')]")
    
    # Table elements
    ACTIVITIES_TABLE = (By.CSS_SELECTOR, "#workflow-activities-table")
    TABLE = (By.XPATH, "//table")
    TABLE_HEADER_NAME = (By.XPATH, "//th[text()='Name']")
    TABLE_HEADER_CATEGORY = (By.XPATH, "//th[text()='Category']")
    TABLE_HEADER_TYPE = (By.XPATH, "//th[text()='Type']")
    TABLE_HEADER_DATE = (By.XPATH, "//th[text()='Date']")
    TABLE_HEADER_STATUS = (By.XPATH, "//th[text()='Status']")
    TABLE_ROWS = (By.XPATH, "//table//tbody//tr")
    TABLE_CELLS = (By.XPATH, "//table//tbody//td")
    
    # Pagination
    PAGINATION_CONTAINER = (By.CSS_SELECTOR, "ul.ant-pagination")
    PAGINATION_NEXT = (By.CSS_SELECTOR, "li.ant-pagination-next button")
    PAGINATION_PREVIOUS = (By.CSS_SELECTOR, "li.ant-pagination-prev button")
    PAGINATION_ITEM = (By.CSS_SELECTOR, "li.ant-pagination-item")
    PAGINATION_ACTIVE_ITEM = (By.CSS_SELECTOR, "li.ant-pagination-item-active")
