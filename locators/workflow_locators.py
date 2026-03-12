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
    
    # Category and Type dropdowns - simple approach that works
    ALL_COMBOBOXES = (By.XPATH, "//div[@id='workflow-category-and-type-selector']//button[@role='combobox']")
    FIRST_COMBOBOX = (By.XPATH, "(//div[@id='workflow-category-and-type-selector']//button[@role='combobox'])[1]")
    SECOND_COMBOBOX = (By.XPATH, "(//div[@id='workflow-category-and-type-selector']//button[@role='combobox'])[2]")
    
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
    
    # Radio buttons in table rows
    RADIO_BUTTONS = (By.XPATH, "//table//tbody//tr//input[@type='radio']")
    FIRST_RADIO_BUTTON = (By.XPATH, "(//table//tbody//tr//input[@type='radio'])[1]")
    
    # Action buttons at bottom (appear when radio button is selected)
    ACTION_BUTTONS_CONTAINER = (By.CSS_SELECTOR, "#workflow-activity-actions, [data-testid='workflow-activity-actions']")
    # View Configuration is an <a> tag with role="button"
    VIEW_CONFIGURATION_BUTTON = (By.XPATH, "//a[@role='button' and contains(., 'View configuration')]")
    # View Results is inside a button (may be disabled)
    VIEW_RESULTS_BUTTON = (By.XPATH, "//button[contains(., 'View results')]//a | //a[contains(., 'View results')]")
    # Duplicate is a button
    DUPLICATE_BUTTON = (By.XPATH, "//button[@role='button' and contains(., 'Duplicate')]")
    
    # Dropdown options for Category and Type
    DROPDOWN_OPTION = (By.XPATH, "//div[@role='option']")
    
    # No activities message
    NO_ACTIVITIES_MESSAGE = (By.XPATH, "//div[contains(text(), 'No activities') or contains(text(), 'no activities')]")
