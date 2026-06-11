# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class DataCircuitLocators:
    """Locators for Data > Model > Circuit page."""

    # Tabs (Experimental, Model, Simulations)
    MODEL_TAB = (By.XPATH, "//button[@role='tab' and text()='Model']")
    MODEL_TAB_ACTIVE = (By.XPATH, "//button[@role='tab' and @data-state='active' and text()='Model']")

    # Circuit tab in left sidebar (active state has bg-primary-9)
    CIRCUIT_TAB = (By.CSS_SELECTOR, "a#counter-circuit")
    CIRCUIT_TAB_ACTIVE = (By.XPATH, "//a[@id='counter-circuit' and contains(@class,'bg-primary-9')]")
    CIRCUIT_TAB_COUNT = (By.XPATH, "//a[@id='counter-circuit']//span[@class='font-bold']")

    # Public / Project scope tabs
    PUBLIC_TAB = (By.XPATH, "//button[normalize-space()='Public'] | //div[normalize-space()='Public']")

    # Species and Brain region (in the header area)
    SPECIES_DROPDOWN = (By.XPATH, "//span[@id='species-selector']//button[@data-slot='select-trigger']")
    SPECIES_VALUE = (By.XPATH, "//span[@id='species-selector']//span[contains(@class,'font-bold')]")
    SPECIES_OPTIONS = (By.CSS_SELECTOR, "div[data-slot='select-item'], div[role='option']")
    BRAIN_REGION_SWITCHER = (By.XPATH, "//div[@data-label='brain-region-switcher']")
    BRAIN_REGION_VALUE = (By.XPATH, "//div[@data-label='brain-region-switcher']//span[contains(@class,'font-bold')]")

    # View toggle (Hierarchy / List)
    # translate-x-[2px] = hierarchy view, translate-x-[21px] = list view
    VIEW_TOGGLE_BTN = (By.ID, "toggle-view")

    # Table structure
    TABLE_CONTAINER = (By.CSS_SELECTOR, "#circuit-table-container")
    TABLE_BODY = (By.CSS_SELECTOR, ".ant-table-body")
    TABLE_ROWS = (
        By.XPATH,
        "//tbody[contains(@class,'ant-table-tbody')]"
        "//tr[contains(@class,'ant-table-row') and not(contains(@class,'ant-table-measure-row'))]",
    )
    TABLE_COLUMN_HEADERS = (
        By.XPATH,
        "//thead//th[@data-testid='column-header']//div[contains(@class,'columnTitle')]",
    )

    # Hierarchy expand button (chevron in rows)
    HIERARCHY_EXPAND_BTN = (By.CSS_SELECTOR, "button.ant-table-row-expand-icon")

    # Search input
    SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search for entities...']")

    # Filter panel
    FILTER_BTN = (By.XPATH, "//button[@aria-label='listing-view-filter-button']")
    FILTER_NEURONS = (By.XPATH, "//button[contains(@class,'accordionTrigger') and .//span[contains(text(),'Number of neurons')]]")
    FILTER_SYNAPSES = (By.XPATH, "//button[contains(@class,'accordionTrigger') and .//span[contains(text(),'Number of synapses')]]")
    FILTER_CONNECTIONS = (By.XPATH, "//button[contains(@class,'accordionTrigger') and .//span[contains(text(),'Number of connections')]]")
    FILTER_APPLY_BTN = (By.XPATH, "//button[.//span[contains(text(),'Apply')]]")
    FILTER_CLOSE_BTN = (By.XPATH, "//button[@aria-label='Close']")
    FILTER_INPUT_MIN = (By.CSS_SELECTOR, "input#value-range-min")
    FILTER_INPUT_MAX = (By.CSS_SELECTOR, "input#value-range-max")
    FILTER_INPUT_FIELDS = (By.XPATH, "//input[@type='number']")

    # Mini-detail view
    MINI_DETAIL_VIEW = (By.CSS_SELECTOR, "[data-testid='mini-viewer']")
    MINI_DETAIL_CLOSE_BTN = (By.XPATH, "//*[@data-testid='mini-viewer']//button[.//span[@aria-label='close']]")
    MINI_DETAIL_NAME = (By.XPATH, "//*[@data-testid='mini-viewer']//h1")
    MINI_DETAIL_THUMBNAIL = (By.XPATH, "//*[@data-testid='mini-viewer']//img[@class='ant-image-img']")
    MINI_DETAIL_VIEW_DETAILS_BTN = (By.XPATH, "//*[@data-testid='mini-viewer']//a[@title='Go to details page']")
    MINI_DETAIL_COPY_BTN = (By.XPATH, "//*[@data-testid='mini-viewer']//button[@title='Copy ID']")
    MINI_DETAIL_DOWNLOAD_BTN = (By.XPATH, "//*[@data-testid='mini-viewer']//button[@title='download']")
    MINI_DETAIL_DESCRIPTION = (By.CSS_SELECTOR, "#record-description")
    MINI_DETAIL_FIELDS = (By.XPATH, "//*[@data-testid='mini-viewer']//div[contains(@class,'text-primary-3') and contains(@class,'font-light')]")

    # Detail view - tabs
    DV_OVERVIEW_TAB = (By.XPATH, "//a[contains(@href,'overview')]")
    DV_ANALYSIS_TAB = (By.XPATH, "//a[contains(@href,'analysis')]")
    DV_RELATED_PUBLICATIONS_TAB = (By.XPATH, "//a[contains(@href,'related-publications')]")
    DV_RELATED_ARTIFACTS_TAB = (By.XPATH, "//a[contains(@href,'related-artifacts')]")
    DV_CLOSE_BTN = (By.XPATH, "//a[@title='Close']")

    # Detail view - breadcrumbs
    DV_BREADCRUMB_DATA = (By.XPATH, "//a[contains(@class,'capitalize') and text()='Data']")
    DV_BREADCRUMB_MODEL = (By.XPATH, "//a[contains(@class,'capitalize') and text()='Model']")
    DV_BREADCRUMB_CIRCUIT = (By.XPATH, "//span[contains(@class,'font-bold')]//a[contains(text(),'Circuit')]")

    # Detail view - metadata
    DV_METADATA_LABELS = (By.XPATH, "//div[contains(@class,'text-neutral-4') and contains(@class,'uppercase')]")

    # Detail view - image and buttons
    DV_IMAGE = (By.XPATH, "//img[contains(@alt,'')]")
    DV_COPY_ID_BTN = (By.XPATH, "//div[.//div[text()='Copy ID'] and .//span[@aria-label='copy']]")
    DV_DOWNLOAD_BTN = (By.XPATH, "//div[.//div[text()='Download'] and .//span[@aria-label='download']]")
    DV_SIMULATE_BTN = (By.XPATH, "//div[.//div[text()='Simulate'] and .//span[@aria-label='experiment']]")
