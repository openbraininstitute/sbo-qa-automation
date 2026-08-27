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
    CIRCUIT_TAB_COUNT = (
        By.XPATH,
        "//a[@id='counter-circuit']//span[contains(@class,'font-bold')]",
    )
    RESULTS_COUNT = (
        By.XPATH,
        "//span[contains(@class,'text-xs') and contains(text(),'results')]",
    )

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

    # Table structure (AG Grid)
    TABLE_CONTAINER = (By.CSS_SELECTOR, ".ag-root, #circuit-table-container")
    TABLE_BODY = (By.CSS_SELECTOR, ".ag-body-viewport, .ag-center-cols-viewport")
    TABLE_ROWS = (
        By.CSS_SELECTOR,
        ".ag-center-cols-container .ag-row[role='row']",
    )
    TABLE_COLUMN_HEADERS = (
        By.CSS_SELECTOR,
        ".ag-header-cell[role='columnheader']",
    )

    # Hierarchy expand button (AG Grid group / tree expand — contracted only)
    HIERARCHY_EXPAND_BTN = (
        By.CSS_SELECTOR,
        ".ag-group-contracted, .ag-icon-tree-closed, "
        ".ag-row .ag-group-contracted, .ag-cell .ag-icon-tree-closed, "
        "button[aria-label*='Expand'], .ag-row button.ag-group-contracted"
    )

    # Search input
    SEARCH_INPUT = (
        By.XPATH,
        "//input[contains(@placeholder,'Search for entities')]",
    )

    # Filter panel
    FILTER_BTN = (
        By.XPATH,
        "//button[@aria-label='Filters' or @title='Filters' or @aria-label='listing-view-filter-button']"
    )
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

    # Detail view - tabs (DetailMenu renders NextLink tabs as
    # /data/view/{type}/{id}/{section}; section label is capitalize(section).
    # Do NOT use bare contains(@href,'analysis') — that also matches
    # notebooks/browse/analysis_notebook_template in the top nav.
    DV_OVERVIEW_TAB = (
        By.XPATH,
        "//a[normalize-space()='Overview' and contains(@href,'/data/view/') and contains(@href,'/overview')]",
    )
    DV_ANALYSIS_TAB = (
        By.XPATH,
        "//a[normalize-space()='Analysis' and contains(@href,'/data/view/') and contains(@href,'/analysis') and not(contains(@href,'notebook'))]",
    )
    DV_RELATED_PUBLICATIONS_TAB = (
        By.XPATH,
        "//a[normalize-space()='Related publications' and contains(@href,'/data/view/') and contains(@href,'related-publications')]",
    )
    DV_RELATED_ARTIFACTS_TAB = (
        By.XPATH,
        "//a[normalize-space()='Related artifacts' and contains(@href,'/data/view/') and contains(@href,'related-artifacts')]",
    )
    DV_CLOSE_BTN = (By.XPATH, "//a[@title='Close']")

    # Detail view - breadcrumbs
    DV_BREADCRUMB_DATA = (By.XPATH, "//a[contains(@class,'capitalize') and text()='Data']")
    DV_BREADCRUMB_MODEL = (By.XPATH, "//a[contains(@class,'capitalize') and text()='Model']")
    DV_BREADCRUMB_CIRCUIT = (By.XPATH, "//span[contains(@class,'font-bold')]//a[contains(text(),'Circuit')]")

    # Detail view - metadata
    DV_METADATA_LABELS = (By.XPATH, "//div[contains(@class,'text-primary-3') and contains(@class,'uppercase')]")

    # Detail view - image and buttons
    DV_IMAGE = (By.XPATH, "//*[@data-testid='visualization']//img | //img[contains(@alt,'visualization')]")
    DV_COPY_ID_BTN = (By.XPATH, "//button[.//div[text()='Copy ID']]")
    DV_DOWNLOAD_BTN = (By.XPATH, "//button[.//div[text()='Download']]")
    DV_SIMULATE_BTN = (By.XPATH, "//a[.//div[text()='Simulate']] | //button[.//div[text()='Simulate']]")

    # Analysis tab content (circuit Overview component under Analysis section)
    # titles from Header; sections use data-testid="{cell|network}-overview"
    DV_ANALYSIS_CELL_STATS_TITLE = (
        By.XPATH,
        "//div[normalize-space()='Cell statistics']"
    )
    DV_ANALYSIS_CELL_STATS_IMAGE = (
        By.CSS_SELECTOR,
        "[data-testid='cell-overview'] img"
    )
    DV_ANALYSIS_NETWORK_STATS_TITLE = (
        By.XPATH,
        "//div[normalize-space()='Network statistics']"
    )
    DV_ANALYSIS_NETWORK_STATS_IMAGES = (
        By.CSS_SELECTOR,
        "[data-testid='network-overview'] img"
    )

    # Related Publications tab
    DV_PUB_PROVENANCE_BTN = (
        By.XPATH,
        "//button[@data-slot='button'][contains(.,'Provenance') and not(contains(.,'Related artifacts'))]"
    )
    DV_PUB_RELATED_ARTIFACTS_PROV_BTN = (
        By.XPATH,
        "//button[@data-slot='button'][contains(.,'Related artifacts provenance')]"
    )
    DV_PUB_APPLICATIONS_BTN = (
        By.XPATH,
        "//button[@data-slot='button'][contains(.,'Applications')]"
    )
    DV_PUB_ARTICLE_ITEMS = (
        By.CSS_SELECTOR,
        "li.ant-list-item, [data-testid='publication-card'], article, "
        "div[class*='publication'] li, [data-testid='related-publications'] li"
    )
    DV_PUB_ARTICLE_TITLE = (
        By.XPATH,
        "//li[contains(@class,'ant-list-item')]//h2[contains(@class,'font-bold')]"
        " | //*[@data-testid='publication-card']//h2"
        " | //article//h2"
    )
    DV_PUB_COPY_DOI_BTN = (By.XPATH, "//button[contains(.,'Copy DOI')]")
    DV_PUB_AUTHOR_NAMES = (By.XPATH, "//div[contains(@class,'text-paper-author')]//span")
    DV_PUB_MORE_AUTHORS_BTN = (By.XPATH, "//button[contains(@class,'ant-btn-text')]//span[contains(text(),'+ ')]")
    DV_PUB_READ_MORE_BTN = (By.XPATH, "//button[@aria-label='Read more']")
    DV_PUB_PAGINATION = (By.CSS_SELECTOR, "ul.ant-pagination")
    DV_PUB_PAGINATION_ITEMS = (By.CSS_SELECTOR, "li.ant-pagination-item")
    DV_PUB_PAGINATION_NEXT = (By.CSS_SELECTOR, "li.ant-pagination-next button")

    # Related Artifacts tab
    DV_ART_SUBCIRCUITS_BTN = (
        By.XPATH,
        "//button[@data-slot='button'][contains(.,'Subcircuits') and not(contains(.,'Derived'))]"
    )
    DV_ART_DERIVED_CIRCUITS_BTN = (
        By.XPATH,
        "//button[@data-slot='button'][contains(.,'Derived circuits')]"
    )
    DV_ART_TABLE_ROWS = (
        By.XPATH,
        "//tbody[contains(@class,'ant-table-tbody')]"
        "//tr[contains(@class,'ant-table-row') and not(contains(@class,'ant-table-measure-row'))]"
    )
    DV_ART_TABLE_HEADERS = (
        By.XPATH,
        "//thead//th[@data-testid='column-header']//div[contains(@class,'columnTitle')]"
    )
    DV_ART_EXPAND_BTN = (
        By.XPATH,
        "//tr[contains(@class,'ant-table-row')]//td[contains(@class,'ant-table-row-expand-icon-cell')]//button"
    )
    DV_ART_DOWNLOAD_BTN = (
        By.XPATH,
        "//tr[contains(@class,'ant-table-row') and not(contains(@class,'ant-table-measure-row'))]"
        "//td[1]//button[contains(@class,'ant-btn')]"
    )
    DV_ART_EXPANDED_ROW = (By.CSS_SELECTOR, "tr.ant-table-expanded-row")
    DV_ART_NESTED_TABLE_ROWS = (
        By.XPATH,
        "//tr[contains(@class,'ant-table-expanded-row')]"
        "//tbody[contains(@class,'ant-table-tbody')]"
        "//tr[contains(@class,'ant-table-row') and not(contains(@class,'ant-table-measure-row'))]"
    )

    # Download panel
    DV_DOWNLOAD_PANEL = (By.CSS_SELECTOR, "[data-testid='circuit-download-panel']")
    DV_DOWNLOAD_PANEL_CLOSE_BTN = (By.XPATH, "//*[@data-testid='circuit-download-panel']//button[@aria-label='Close']")

    # Detail view - metadata name (special element)
    DV_METADATA_NAME = (
        By.XPATH,
        "//div[contains(@class,'text-primary-8') and contains(@class,'text-2xl') and contains(@class,'font-bold')]"
    )

    # Subject section container
    DV_SUBJECT_SECTION = (
        By.XPATH,
        "(//*[@data-testid='subject-details'] | //h2[contains(text(),'Subject')]/ancestor::div[contains(@class,'rounded')])[3]"
    )
    DV_SUBJECT_SECTION_FALLBACK = (By.XPATH, "//h2[contains(text(),'Subject')]/..")

    # Brain region search (used in select_brain_region_root)
    BRAIN_REGION_SEARCH_INPUT = (By.ID, "region-search")
    BRAIN_REGION_ROOT_OPTION = (
        By.XPATH,
        "//div[contains(@class,'ant-select-item')]//div[text()='Root']"
    )
