# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class ExploreEphysLocators:
    # Public/Project tab selector
    PUBLIC_PROJECT_TAB_CONTAINER = (By.XPATH, "//div[@role='tablist' and @aria-orientation='horizontal']")
    PUBLIC_TAB = (By.XPATH, "//button[@role='tab' and text()='Public']")
    PROJECT_TAB = (By.XPATH, "//button[@role='tab' and text()='Project']")

    # Filter functionality (updated)
    FILTER_BUTTON = (By.XPATH, "//button[@aria-label='listing-view-filter-button']")
    FILTER_COUNT = (By.XPATH, "//span[@class='bg-primary-8 rounded-sm px-2.5 py-1 text-sm font-bold text-white']")
    
    # Thumbnails (images within table cells)
    THUMBNAILS = (By.XPATH, "//td//img")
    
    # Data type selector tabs (Experimental, Model, Simulations)
    DATA_TYPE_SELECTOR = (By.CSS_SELECTOR, "#data-type-selector")
    EXPERIMENTAL_TAB = (By.XPATH, "//button[@type='button' and @role='tab' and @data-state='active' and text()='Experimental']")
    EXPERIMENTAL_TAB_ANY = (By.XPATH, "//button[@type='button' and @role='tab' and text()='Experimental']")
    MODEL_TAB = (By.XPATH, "//button[@type='button' and @role='tab' and text()='Model']")
    SIMULATIONS_TAB = (By.XPATH, "//button[@type='button' and @role='tab' and text()='Simulations']")
    
    # Single cell electrophysiology button
    SINGLE_CELL_ELECTROPHYSIOLOGY_BTN = (By.CSS_SELECTOR, "#counter-electrical_cell_recording")
    SINGLE_CELL_ELECTROPHYSIOLOGY_TEXT = (By.CSS_SELECTOR, "a[id='counter-electrical_cell_recording'] div["
                                                           "class='font-bold text-current']")
    # Data table with filters
    DATA_TABLE_WITH_FILTERS = (By.CSS_SELECTOR, "#data-table-with-filters")
    
    # Search functionality
    SEARCH_BUTTON = (By.XPATH, "//button[@aria-label='Open search']")
    SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search for entities...']")
    SEARCH_CLEAR_BTN = (By.XPATH, "//button[@aria-label='Clear search']")
    
    # Table columns based on your requirements
    TABLE_HEADER_PREVIEW = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Preview']")
    TABLE_HEADER_BRAIN_REGION = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Brain region']")
    TABLE_HEADER_ETYPE = (By.XPATH, "//th[@data-testid='column-header']//div[text()='E-type']")
    TABLE_HEADER_NAME = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Name']")
    TABLE_HEADER_SPECIES = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Species']")
    TABLE_HEADER_CONTRIBUTORS = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Contributors']")
    TABLE_HEADER_REGISTRATION_DATE = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Registration date']")
    
    # Table content
    TABLE_ROWS = (By.CSS_SELECTOR, "tbody.ant-table-tbody tr.ant-table-row")
    TABLE_CELLS = (By.CSS_SELECTOR, "tbody.ant-table-tbody td.ant-table-cell")
    TABLE_BRAIN_REGION_CELLS = (By.XPATH, "//td[@class='ant-table-cell text-primary-7 cursor-pointer "
                                          "before:!content-none ant-table-cell-ellipsis' and @title]")
    
    # Base locator for brain region cells (to be formatted in page object)
    TABLE_BRAIN_REGION_CELL_EXACT_TEMPLATE = ("//td[@class='ant-table-cell text-primary-7 cursor-pointer "
                                              "before:!content-none ant-table-cell-ellipsis' and @title='{}']")
    TABLE_BRAIN_REGION_CELL_PARTIAL_TEMPLATE = ("//td[@class='ant-table-cell text-primary-7 cursor-pointer "
                                                "before:!content-none ant-table-cell-ellipsis' and contains(@title, "
                                                "'{}')]")
    # Filter panel locators
    FILTER_SPECIES_BUTTON = (By.XPATH, "//span[text()='Species']")
    FILTER_SPECIES_TEXT = (By.XPATH, "//span[text()='Rattus norvegicus']")
    FILTER_SPECIES_TICK = (By.CSS_SELECTOR, "button[value='on']")
    FILTER_CONTRIBUTORS_BUTTON = (By.XPATH, "//span[text()='Contributors']")
    FILTER_CONTRIBUTORS_SEARCH = (By.XPATH, "//input[@placeholder='Search contributors...']")
    FILTER_APPLY_BUTTON = (By.CSS_SELECTOR, "button[role='button'][type='button']")
    FILTER_CLOSE_BUTTON = (By.XPATH, "//button[@aria-label='Close']")
    
    # Mini-detail view locators
    MINI_DETAIL_VIEW = (By.CSS_SELECTOR, "#mini-detail-view-container")
    MINI_DETAIL_VIEW_CARD = (By.CSS_SELECTOR, "#mini-viewer")
    MDV_NAME = (By.XPATH, "//h1[@class='text-2xl font-bold break-all']")
    MDV_DESCRIPTION = (By.CSS_SELECTOR, "#record-description")
    MDV_IMAGE = (By.XPATH, "//div[@class='ant-image  w-full  h-80']//img")
    MDV_BRAIN_REGION_LABEL = (By.XPATH, "//div[text()='Brain Region']")
    MDV_BRAIN_REGION_VALUE = (By.XPATH, "//div[text()='Brain Region']/following-sibling::div")
    MDV_ETYPE_LABEL = (By.XPATH, "//div[text()='E-Type']")
    MDV_ETYPE_VALUE = (By.XPATH, "//div[text()='E-Type']/following-sibling::div")
    MDV_SPECIES_LABEL = (By.XPATH, "//div[text()='Species']")
    MDV_SPECIES_VALUE = (By.XPATH, "//div[text()='Species']/following-sibling::div")
    MDV_LICENSE_LABEL = (By.XPATH, "//div[text()='License']")
    MDV_LICENSE_VALUE = (By.XPATH, "//div[text()='License']/following-sibling::div//a")
    MDV_COPY_BUTTON = (By.XPATH, "//button[@title='Copy ID']")
    MDV_DOWNLOAD_BUTTON = (By.XPATH, "//button[@title='download']")
    MDV_VIEW_DETAILS_BUTTON = (By.XPATH, "//a[@title='Go to details page' and contains(text(), 'View details')]")
    
    # Legacy locators (keeping for backward compatibility)
    ALL_CHECKBOXES = (By.XPATH, "//span[@class='ant-checkbox ant-wave-target']")
    AI_ASSISTANT_PANEL = (By.XPATH, "//div[starts-with(@class,'ai-assistant-module')]")
    AI_ASSISTANT_PANEL_CLOSE_BTN = (By.XPATH, "(//span[@aria-label='minus'])[3]")
    APPLY_BTN = (By.XPATH, "//button[@type='submit' and text()='Apply']")
    BRAIN_REGION_PANEL_CLOSE_BTN = (By.CSS_SELECTOR, ".ant-btn-icon")
    BRAIN_REGION_PANEL_OPEN_BTN = (By.CSS_SELECTOR, "span[class='anticon anticon-plus']")
    CHECKBOXES = (By.XPATH, "//input[@class='ant-checkbox-input' and @type='checkbox']")
    DOWNLOAD_RESOURCES = (By.XPATH, "//button[@type='button' and @aria-label='download-resources-button']")
    # Breadcrumbs
    DV_BREADCRUMB_DATA = (By.XPATH, "//span[@class='text-primary-8']//a[text()='Data']")
    DV_BREADCRUMB_EXPERIMENTAL = (By.XPATH, "//span[@class='text-primary-8']//a[text()='Experimental']")
    DV_BREADCRUMB_SINGLE_CELL = (By.XPATH, "//span[@class='text-primary-8 font-bold']//a[contains(text(), 'Single cell electrophysiology')]")
    
    # Tabs
    DV_OVERVIEW_TAB = (By.XPATH, "//label[contains(@class, 'ant-radio-button-wrapper')]//span[contains(text(), 'Overview')]")
    DV_INTERACTIVE_DETAILS_TAB = (By.XPATH, "//label[contains(@class, 'ant-radio-button-wrapper')]//span[contains(text(), 'Interactive Details')]")
    
    # Action buttons
    DV_COPY_ID_BUTTON = (By.XPATH, "//div[text()='Copy ID']")
    DV_DOWNLOAD_BUTTON = (By.XPATH, "//div[text()='Download']")
    
    # Main fields
    DV_NAME_LABEL = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Name']")
    DV_NAME_VALUE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Name']/following-sibling::div")
    DV_DESCRIPTION_LABEL = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Description']")
    DV_DESCRIPTION_VALUE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Description']/following-sibling::div")
    DV_REGISTERED_BY_LABEL = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Registered by']")
    DV_REGISTERED_BY_VALUE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Registered by']/following-sibling::div")
    DV_CONTRIBUTORS_LABEL = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Contributors']")
    DV_CONTRIBUTORS_VALUE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Contributors']/following-sibling::div")
    DV_INSTITUTIONAL_CONTRIBUTORS_LABEL = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Institutional Contributors']")
    DV_INSTITUTIONAL_CONTRIBUTORS_VALUE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Institutional Contributors']/following-sibling::div")
    DV_REGISTRATION_DATE_LABEL = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Registration date']")
    DV_REGISTRATION_DATE_VALUE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Registration date']/following-sibling::div")
    DV_BRAIN_REGION_LABEL = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Brain Region']")
    DV_BRAIN_REGION_VALUE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Brain Region']/following-sibling::div")
    DV_ETYPE_LABEL = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='E-Type']")
    DV_ETYPE_VALUE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='E-Type']/following-sibling::div")
    DV_LICENSE_LABEL = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='License']")
    DV_LICENSE_LINK = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='License']/following-sibling::div//a")
    
    # Subject section
    DV_SUBJECT_HEADER = (By.XPATH, "//h2[text()='Subject']")
    DV_SUBJECT_NAME_LABEL = (By.XPATH, "//h2[text()='Subject']/following::div[@class='text-neutral-4 uppercase' and text()='Name'][1]")
    DV_SUBJECT_NAME_VALUE = (By.XPATH, "//h2[text()='Subject']/following::div[@class='text-neutral-4 uppercase' and text()='Name'][1]/following-sibling::div")
    DV_SUBJECT_DESCRIPTION_LABEL = (By.XPATH, "//h2[text()='Subject']/following::div[@class='text-neutral-4 uppercase' and text()='Description'][1]")
    DV_SUBJECT_DESCRIPTION_VALUE = (By.XPATH, "//h2[text()='Subject']/following::div[@class='text-neutral-4 uppercase' and text()='Description'][1]/following-sibling::div")
    DV_SUBJECT_SPECIES_LABEL = (By.XPATH, "//h2[text()='Subject']/following::div[@class='text-neutral-4 uppercase' and text()='Species'][1]")
    DV_SUBJECT_SPECIES_VALUE = (By.XPATH, "//h2[text()='Subject']/following::div[@class='text-neutral-4 uppercase' and text()='Species'][1]/following-sibling::div")
    DV_SUBJECT_STRAIN_LABEL = (By.XPATH, "//h2[text()='Subject']/following::div[@class='text-neutral-4 uppercase' and text()='Strain'][1]")
    DV_SUBJECT_STRAIN_VALUE = (By.XPATH, "//h2[text()='Subject']/following::div[@class='text-neutral-4 uppercase' and text()='Strain'][1]/following-sibling::div")
    DV_SUBJECT_SEX_LABEL = (By.XPATH, "//h2[text()='Subject']/following::div[@class='text-neutral-4 uppercase' and text()='Sex'][1]")
    DV_SUBJECT_SEX_VALUE = (By.XPATH, "//h2[text()='Subject']/following::div[@class='text-neutral-4 uppercase' and text()='Sex'][1]/following-sibling::div")
    DV_SUBJECT_WEIGHT_LABEL = (By.XPATH, "//h2[text()='Subject']/following::div[@class='text-neutral-4 uppercase' and text()='Weight'][1]")
    DV_SUBJECT_WEIGHT_VALUE = (By.XPATH, "//h2[text()='Subject']/following::div[@class='text-neutral-4 uppercase' and text()='Weight'][1]/following-sibling::div")
    DV_SUBJECT_AGE_LABEL = (By.XPATH, "//h2[text()='Subject']/following::div[@class='text-neutral-4 uppercase' and text()='Age'][1]")
    DV_SUBJECT_AGE_VALUE = (By.XPATH, "//h2[text()='Subject']/following::div[@class='text-neutral-4 uppercase' and text()='Age'][1]/following-sibling::div")
    DV_SUBJECT_AGE_MIN_LABEL = (By.XPATH, "//h2[text()='Subject']/following::div[@class='text-neutral-4 uppercase' and text()='Age min'][1]")
    DV_SUBJECT_AGE_MIN_VALUE = (By.XPATH, "//h2[text()='Subject']/following::div[@class='text-neutral-4 uppercase' and text()='Age min'][1]/following-sibling::div")
    DV_SUBJECT_AGE_MAX_LABEL = (By.XPATH, "//h2[text()='Subject']/following::div[@class='text-neutral-4 uppercase' and text()='Age max'][1]")
    DV_SUBJECT_AGE_MAX_VALUE = (By.XPATH, "//h2[text()='Subject']/following::div[@class='text-neutral-4 uppercase' and text()='Age max'][1]/following-sibling::div")
    DV_SUBJECT_AGE_PERIOD_LABEL = (By.XPATH, "//h2[text()='Subject']/following::div[@class='text-neutral-4 uppercase' and text()='Age period'][1]")
    DV_SUBJECT_AGE_PERIOD_VALUE = (By.XPATH, "//h2[text()='Subject']/following::div[@class='text-neutral-4 uppercase' and text()='Age period'][1]/following-sibling::div")
    
    # Overview and Interactive Details tabs (in detail view)
    DV_OVERVIEW_TAB_BUTTON = (By.XPATH, "//label[contains(@class, 'ant-radio-button-wrapper')]//span[contains(text(), 'Overview')]")
    DV_INTERACTIVE_DETAILS_TAB_BUTTON = (By.XPATH, "//label[contains(@class, 'ant-radio-button-wrapper')]//span[contains(text(), 'Interactive Details')]")
    DV_OVERVIEW_TAB_ACTIVE = (By.XPATH, "//label[contains(@class, 'ant-radio-button-wrapper-checked')]//span[contains(text(), 'Overview')]")
    DV_INTERACTIVE_DETAILS_TAB_ACTIVE = (By.XPATH, "//label[contains(@class, 'ant-radio-button-wrapper-checked')]//span[contains(text(), 'Interactive Details')]")
    
    # Overview plots
    DV_OVERVIEW_PLOTS = (By.XPATH, "//div[@class='plot-container plotly']")
    DV_OVERVIEW_PLOT_IMAGES = (By.XPATH, "//div[@class='flex flex-col gap-10']//div[contains(@class, 'aspect-4/3')]")
    
    # Interactive Details plots and controls
    DV_INTERACTIVE_PLOTS = (By.XPATH, "//div[@class='plot-container plotly']")
    DV_STIMULUS_SELECTOR = (By.XPATH, "//div[@class='ant-select-selector']")
    DV_STIMULUS_DROPDOWN = (By.XPATH, "//div[@class='ant-select-item-option-content']")
    DV_STIMULUS_ALL_OPTION = (By.XPATH, "//div[@class='ant-select-item-option-content' and text()='All']")
    DV_REPETITION_LABEL = (By.XPATH, "//label[text()='Repetition']")
    DV_SWEEP_LABEL = (By.XPATH, "//span[text()='Sweep']")
    
    # Plot interaction controls (Plotly)
    DV_PLOT_MODEBAR = (By.CSS_SELECTOR, ".modebar-container")
    DV_PLOT_ZOOM_BUTTON = (By.CSS_SELECTOR, "[data-title='Zoom']")
    DV_PLOT_PAN_BUTTON = (By.CSS_SELECTOR, "[data-title='Pan']")
    DV_PLOT_RESET_BUTTON = (By.CSS_SELECTOR, "[data-title='Reset axes']")
    DV_PLOT_DOWNLOAD_BUTTON = (By.CSS_SELECTOR, "[data-title='Download plot as a png']")
    DV_AGE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Age']")
    DV_BRAIN_REG_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Brain Region']")
    DV_BR_REG = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Brain Region']/following-sibling::div[@class='mt-2 break-words']")
    DV_CONTRIBUTORS = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Contributors']/following-sibling::div[@class='mt-2 break-words']")
    DV_CONTRIBUTORS_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Contributors']")
    DV_DESC = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Description']/following-sibling::div[@class='mt-2 break-words']")
    DV_DESC_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Description']")
    DV_DOWNLOAD_BTN = (By.XPATH, "//div[text()='Download']")
    DV_ETYPE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='E-Type']/following-sibling::div[@class='mt-2 break-words']")
    DV_ETYPE_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='E-Type']")
    DV_ID_PLOTS = (By.XPATH, "//div[@class='flex flex-col gap-10 2xl:flex-row']")
    DV_ID_REPETITION_TITLE = (By.XPATH, "//div[@class='flex gap-8']//label[text()='Repetition']")
    DV_ID_STIMULUS_TITLE = (By.XPATH, "//div[@class='flex gap-8']//label[text()='Stimulus']")
    DV_ID_SWEEP_TITLE = (By.XPATH, "//div[@class='flex gap-8']//span[text()='Sweep']")
    DV_INTER_DETAILS = (By.XPATH, "//span[contains(text(),' Interactive Details')]")
    DV_LICENSE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='License']/following-sibling::div[@class='mt-2 break-words']")
    DV_LICENSE_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='License']")
    DV_NAME = (By.XPATH, "//div[text()='Name']//following::div[@class='col-span-3 text-2xl font-bold']")
    DV_NAME_TITLE = (By.XPATH, "//div[@class='text font-thin' and text()='Name']")
    DV_NUM_MEAS_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='N° of Measurements']")
    DV_OVERVIEW = (By.XPATH, "//span[contains(text(),' Overview')]")
    DV_PLOTS = (By.XPATH, "//div[@class='plot-container plotly']")
    DV_REG_DATE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Registration date']/following-sibling::div[@class='mt-2 break-words']")
    DV_REG_DATE_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Registration date']")
    DV_SPECIES = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Species']/following-sibling::div[@class='mt-2 break-words']")
    DV_SPECIES_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Species']")
    DV_STIMULUS_ALL = (By.XPATH, "//div[@class='ant-select-item-option-content' and text()='All']")
    DV_STIMULUS_BTN = (By.XPATH, "//div[@class='ant-select-selector']")
    DV_STIMULUS_SEARCH = (By.XPATH, "//input[@id='rc_select_2']")
    DV_STIMULUS_IMG_GRID = (By.XPATH, "//div[@class='flex flex-col gap-10']")
    DV_STIM_IMAGES = (By.XPATH, "//div[@class='flex flex-col gap-3 divide-y divide-neutral-2']//div[@class='grid grid-cols-4 gap-7 pt-5 2xl:grid-cols-6']")
    
    # List View locators
    FILTERED_ETYPE = (By.XPATH, "(//td[@class='ant-table-cell text-primary-7 cursor-pointer before:!content-none ant-table-cell-ellipsis']/div[@title='bNAC'])[2]")
    FILTER_ETYPE_BTN = (By.XPATH, "//button[starts-with(@class, 'filters-module__') and starts-with(@id, 'radix-') and @type='button']//span[text()='E-type']")
    FILTER_ETYPE_SEARCH_INPUT = (By.XPATH, "(//input[@class='ant-select-selection-search-input'])[2]")
    FILTER_ETYPE_INPUT_TYPE_AREA = (By.XPATH, "//div[@class='ant-select-selection-search']")
    FILTER_ETYPE_SEARCH = (By.XPATH, "//div[@class='ant-select-selection-overflow']")
    LOAD_MORE_BUTTON = (By.XPATH, "//button[@type='button' and text()='Load 30 more results...']")
    LV_GRID_VIEW = (By.CSS_SELECTOR, "#base-table-wrapper")
    LV_BRAIN_REGION = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Brain region']")
    LV_CONTRIBUTORS = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Contributors']")
    LV_ETYPE = (By.XPATH, "//th[@data-testid='column-header']//div[text()='E-type']")
    LV_FILTER_APPLY_BTN = (By.XPATH, "//button[@type='submit' and text()='Apply']")
    LV_FILTER_BTN = (By.XPATH, "//button[@type='button' and @aria-label='listing-view-filter-button']")
    LV_FILTER_CLOSE_BTN = (By.XPATH, "//button[@type='button' and @aria-label='Close']")
    LV_FILTER_MTYPE = (By.XPATH, "//span[text()='M-type']")
    LV_NAME = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Name']")
    LV_PREVIEW = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Preview']")
    LV_REGISTRATION_DATE = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Registration date']")
    LV_ROW1 = (By.XPATH, "(//td[@class='ant-table-cell text-primary-7 cursor-pointer before:!content-none ant-table-cell-ellipsis'])[1]")
    LV_SPECIES = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Species']")
    LV_THUMBNAIL = (By.XPATH, "//td//img")
    LV_TOTAL_RESULTS = (By.XPATH, "//div[@class='w-max']")
    SEARCHED_SPECIES = (By.XPATH, "//td[@title='Rattus norvegicus' and contains(text(),'Rattus norvegicus')][1]")
    SEARCH_INPUT_FIELD = (By.XPATH, "button[aria-label='Open search']")
    TABLE = (By.XPATH, "//tbody[@class='ant-table-tbody']")
    # TABLE_CELLS = (By.CSS_SELECTOR, "tbody.ant-table-tbody td.ant-table-cell.text-primary-7.cursor-pointer.ant-table-cell-ellipsis")
