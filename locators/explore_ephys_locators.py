# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class ExploreEphysLocators:
    ALL_CHECKBOXES = (By.XPATH, "//span[@class='ant-checkbox ant-wave-target']")
    AI_ASSISTANT_PANEL = (By.XPATH, "//div[starts-with(@class,'ai-assistant-module')]")
    AI_ASSISTANT_PANEL_CLOSE_BTN = (By.XPATH, "(//span[@aria-label='minus'])[3]")
    APPLY_BTN = (By.XPATH, "//button[@type='submit' and text()='Apply']")
    BRAIN_REGION_PANEL_CLOSE_BTN = (By.CSS_SELECTOR, ".ant-btn-icon")
    BRAIN_REGION_PANEL_OPEN_BTN = (By.CSS_SELECTOR, "span[class='anticon anticon-plus']")
    CHECKBOXES = (By.XPATH, "//input[@class='ant-checkbox-input' and @type='checkbox']")
    DOWNLOAD_RESOURCES = (By.XPATH, "//button[@type='button' and "
                                    "@aria-label='download-resources-button']")
    DV_AGE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Age']")
    DV_BRAIN_REG_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Brain "
                                    "Region']")
    DV_BR_REG = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Brain "
                           "Region']/following-sibling::div[@class='mt-2 break-words']")
    DV_CONTRIBUTORS = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text("
                                 ")='Contributors']/following-sibling::div[@class='mt-2 break-words']")
    DV_CONTRIBUTORS_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text("
                                       ")='Contributors']")
    DV_DESC = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text("
                         ")='Description']/following-sibling::div[@class='mt-2 break-words']")
    DV_DESC_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Description']")
    DV_DOWNLOAD_BTN = (By.XPATH, "//div[text()='Download']")
    DV_ETYPE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text("
                          ")='E-Type']/following-sibling::div[@class='mt-2 break-words']")
    DV_ETYPE_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='E-Type']")
    DV_ID_PLOTS = (By.XPATH, "//div[@class='flex flex-col gap-10 2xl:flex-row']")
    DV_ID_REPETITION_TITLE = (By.XPATH, "//div[@class='flex gap-8']//label[text()='Repetition']")
    DV_ID_STIMULUS_TITLE = (By.XPATH, "//div[@class='flex gap-8']//label[text()='Stimulus']")
    DV_ID_SWEEP_TITLE = (By.XPATH, "//div[@class='flex gap-8']//span[text()='Sweep']")
    DV_INTER_DETAILS = (By.XPATH, "//span[contains(text(),' Interactive Details')]")
    DV_LICENSE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text("
                            ")='License']/following-sibling::div[@class='mt-2 break-words']")
    DV_LICENSE_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='License']")
    DV_NAME = (By.XPATH, "//div[text()='Name']//following::div[@class='col-span-3 text-2xl "
                         "font-bold']")
    DV_NAME_TITLE = (By.XPATH, "//div[@class='text font-thin' and text()='Name']")
    DV_NUM_MEAS_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='N° of "
                                   "Measurements']")
    DV_OVERVIEW = (By.XPATH, "//span[contains(text(),' Overview')]")
    DV_PLOTS = (By.XPATH, "//div[@class='plot-container plotly']")
    DV_REG_DATE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Registration "
                             "date']/following-sibling::div[@class='mt-2 break-words']")
    DV_REG_DATE_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text("
                                   ")='Registration date']")
    DV_SPECIES = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text("
                            ")='Species']/following-sibling::div[@class='mt-2 break-words']")
    DV_SPECIES_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Species']")
    DV_STIMULUS_ALL = (By.XPATH, "//div[@class='ant-select-item-option-content' and text()='All']")
    DV_STIMULUS_BTN = (By.XPATH, "//div[@class='ant-select-selector']")
    DV_STIMULUS_SEARCH = (By.XPATH, "//input[@id='rc_select_2']")
    DV_STIMULUS_IMG_GRID = (By.XPATH, "//div[@class='flex flex-col gap-10']")
    DV_STIM_IMAGES = (By.XPATH, "//div[@class='flex flex-col gap-3 divide-y "
                                "divide-neutral-2']//div[@class='grid grid-cols-4 gap-7 pt-5 "
                                "2xl:grid-cols-6']")
    EPHYS_TAB_TITLE = (By.XPATH, "//span[@class='ant-menu-title-content' and contains(text(),"
                                 "'Electrophysiology')]")
    FILTERED_ETYPE = (By.XPATH, "(//td[@class='ant-table-cell text-primary-7 cursor-pointer before:!content-none "
                                "ant-table-cell-ellipsis']/div[@title='bNAC'])[2]")
    FILTER_ETYPE_BTN = (By.XPATH,
                    "//button[starts-with(@class, 'filters-module__') and starts-with(@id, 'radix-') and "
                    "@type='button']//span[text()='E-type']")

    FILTER_ETYPE_SEARCH_INPUT = (By.XPATH, "(//input[@class='ant-select-selection-search-input"
                                           "'])[2]")
    FILTER_ETYPE_INPUT_TYPE_AREA = (By.XPATH, "//div[@class='ant-select-selection-search']")
    FILTER_ETYPE_SEARCH = (By.XPATH, "//div[@class='ant-select-selection-overflow']")
    LOAD_MORE_BUTTON = (By.XPATH, "//button[@type='button' and text()='Load 30 more results...']")
    LV_GRID_VIEW = (By.XPATH, "//div[@data-testid='explore-section-listing-view']")
    LV_BRAIN_REGION = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Brain region']")
    LV_CONTRIBUTORS = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Contributors']")
    LV_ETYPE = (By.XPATH, "//th[@data-testid='column-header']//div[text()='E-type']")
    LV_FILTER_APPLY_BTN = (By.XPATH, "//button[@type='submit' and text()='Apply']")
    LV_FILTER_BTN = (By.XPATH, "//button[@type='button' and "
                               "@aria-label='listing-view-filter-button']")
    LV_FILTER_CLOSE_BTN = (By.XPATH, "//button[@type='button' and @aria-label='Close']")
    LV_FILTER_MTYPE = (By.XPATH, "//span[text()='M-type']")
    LV_NAME = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Name']")
    LV_PREVIEW = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Preview']")
    LV_REGISTRATION_DATE = (By.XPATH, "//th[@data-testid='column-header']//div[text("
                                      ")='Registration date']")
    LV_ROW1 = (By.XPATH, "(//td[@class='ant-table-cell text-primary-7 cursor-pointer "
                         "before:!content-none ant-table-cell-ellipsis'])[1]")
    LV_SPECIES = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Species']")
    LV_THUMBNAIL = (By.XPATH, "//img[@alt='img preview']")
    LV_TOTAL_RESULTS = (By.XPATH, "//div[@class='w-max']")
    SEARCHED_SPECIES = (By.XPATH, "//td[@title='Rattus norvegicus' and contains(text(),'Rattus "
                                  "norvegicus')][1]")
    SEARCH_BUTTON = (By.XPATH, "//span[@aria-label='search']/parent::button[@type='button']")
    SEARCH_INPUT_FIELD = (By.XPATH, "//input[@placeholder='Search for resources...']")
    TABLE = (By.XPATH, "//tbody[@class='ant-table-tbody']")
    TABLE_CELLS = (By.CSS_SELECTOR, "tbody.ant-table-tbody "
                                    "td.ant-table-cell.text-primary-7.cursor-pointer.ant-table"
                                    "-cell-ellipsis")
    TABLE_ROWS = (By.CSS_SELECTOR, "tbody.ant-table-tbody tr.ant-table-row")
