# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class ExploreMorphologyPageLocators:
    BACK_IE_BTN = (By.XPATH, "//div[.='Back to list']")
    BRAIN_REGION_COLUMN_TITLE = (By.XPATH, "//div[text()='Brain Region']")
    BR_SORTED = (By.XPATH, "//tbody[@class='ant-table-tbody']/tr[2]/descendant::td[contains(text("
                           "),'Primary somatosensory area')]")
    BR_SORT_ARROW = (By.XPATH, "//th[contains(.,'Brain region')]//div["
                               "@class='ant-table-column-sorters']")
    CELLS = (By.XPATH, "//td[starts-with(@class,'ant-table-cell')]")
    CLEAR_FILTERS_BTN = (By.XPATH, "//button[@type='button']/div[text()='Clear filters']")
    DV_AGE_TITLE = (By.XPATH, "//div[@class='uppercase text-neutral-4' and text()='Age']")
    DV_AP_TITLE = (By.XPATH, "//h2[text()='Apical Dendrite']")
    DV_AXON_TITLE = (By.XPATH, "//h2[text()='Axon']")
    DV_BACK_BTN = (By.XPATH, "//a[contains(@href,'/mmb-beta/explore/interactive/experimental"
                             "/morphology')]")
    DV_BD_TITLE = (By.XPATH, "//h2[text()='Basal Dendrite']")
    DV_BRAIN_REGION_TITLE = (By.XPATH, "//div[@class='uppercase text-neutral-4' and text()='Brain "
                                       "Region']")
    DV_CONTRIBUTORS_TITLE = (By.XPATH, "//div[@class='uppercase text-neutral-4' and text("
                                       ")='Contributors'] ")
    DV_DESCRIPTION_TITLE = (By.XPATH, "//div[@class='uppercase text-neutral-4' and text("
                                      ")='Description']")
    DV_DOWNLOAD_BTN = (By.XPATH, "//button[@type='button']/span[contains(text(),'Download')]")
    DV_LICENSE_TITLE = (By.XPATH, "//div[@class='uppercase text-neutral-4' and text()='License']")
    DV_MORPHOMETRICS_TITLE = (By.XPATH, "//h1[.='Morphometrics']")
    DV_MTYPE_TITLE = (By.XPATH, "//div[@class='uppercase text-neutral-4' and text()='M-Type']")
    DV_NAME_TITLE = (By.XPATH, "//div[@class='text font-thin' and text()='Name']")
    DV_NM_TITLE = (By.XPATH, "//h2[text()='Neuron Morphology']")
    DV_REGISTRATION_DATE_TITLE = (By.XPATH, "//div[@class='uppercase text-neutral-4' and text("
                                            ")='Registration date']")
    DV_SELECTED_BR = (By.XPATH, "//div[@class='grid w-1/2 auto-rows-min grid-cols-3 gap-x-8 "
                                "gap-y-6']//div[text()='Brain Region']/following-sibling::div["
                                "text()='Anterior"
                                "cingulate area, dorsal part, layer 2/3']")
    DV_SOMA_TITLE = (By.XPATH, "//h2[text()='Soma']")
    DV_SPECIES_TITLE = (By.XPATH, "//div[@class='uppercase text-neutral-4' and text()='Species']")
    FILTERED_MTYPE = (By.XPATH, "//td[@class='ant-table-cell text-primary-7 cursor-pointer "
                                "before:!content-none ant-table-cell-ellipsis' and "
                                "@title='L5_TPC:A']")
    FILTER_MTYPE_SEARCH = (By.XPATH, "//div[@class='ant-select-selection-overflow']")
    FILTER_MTYPE_TEXT_INPUT = (By.XPATH, "(//input[@class='ant-select-selection-search-input'])[2]")
    FILTER_PANEL = (By.XPATH, "//div[@data-testid='listing-view-filter-panel']")
    FIRST_ROW = (By.XPATH, "//tbody[@class='ant-table-tbody']/tr[2]")
    LV_BRAIN_REGION = (By.XPATH, "//span[@class='ant-table-column-title']//div[text()='Brain "
                                 "region']")
    LV_CHECKBOX = (By.XPATH, "")
    LV_CONTRIBUTORS = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Contributors']")
    LV_FILTER_APPLY_BTN = (By.XPATH, "//button[@type='submit' and text()='Apply']")
    LV_FILTER_MTYPE = (By.XPATH, "//span[text()='M-type']")
    LV_MTYPE = (By.XPATH, "//th[@data-testid='column-header']//div[text()='M-type']")
    LV_NAME = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Name']")
    LV_PREVIEW = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Preview']")
    LV_REGISTRATION_DATE = (By.XPATH, "//th[@data-testid='column-header']//div[text("
                                      ")='Registration date']")
    LV_SPECIES = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Species']")
    LV_THUMBNAIL = (By.XPATH, "//img[@alt='img preview']")
    MORPHOLOGY_FILTER = (By.XPATH, "//button[@aria-label='listing-view-filter-button']")
    MORPHOLOGY_FILTER_CLOSE_BTN = (By.XPATH, "//div[@data-testid='listing-view-filter-panel"
                                             "']//button[@type='button' and @aria-label='Close']")
    MORPHOLOGY_HOME_BTN = (By.XPATH, "//span[@aria-label='home']/preceding-sibling::h2[text("
                                     ")='Home']")
    MORPHOLOGY_SIDE_BAR_EXPLORE_BTN = (By.XPATH, "")
    MORPHOLOGY_SIDE_BAR_MENU = (By.XPATH, "//aside/div[starts-with(@class,'sidebar_expanded__')]")
    MORPHOLOGY_SIDE_BAR_MENU_CLOSE_BTN = (By.XPATH, "//button[@type='button' and starts-with("
                                                    "@class, 'ant-btn')]/span["
                                                    "@class='ant-btn-icon']")
    MORPHOLOGY_SIDE_BAR_PLUS_BTN = (By.XPATH, "//div[starts-with(@class,'sidebar_side')]//button["
                                              "starts-with(@class, 'ant-btn css')]")
    MORPHOLOGY_TAB = (By.XPATH, "//span[@class='ant-menu-title-content' and contains(text(),"
                                "'Morphology')]")
    MORPHO_VIEWER = (By.XPATH, "//div[@data-testid='morpho-viewer']")
    MORPHO_VIEWER_FULLSCREEN_BTN = (By.XPATH, "//button[@type='button' and @aria-label='Toggle "
                                              "fullscreen']")
    MORPHO_VIEWER_SETTINGS_BTN = (By.XPATH, "//button[@type='button']/div[contains(text(), "
                                            "'Settings')]")
    RESULTS = (By.XPATH, "//span[text()='Results ']")
    ROW = (By.XPATH, "//tr[starts-with(@class,'ant-table-row')]")
    SEARCH_INPUT_FIELD = (By.XPATH, "//input[@placeholder='Search for resources...']")
    SEARCH_NAME = (By.XPATH, "//td[@title='mtC070301B_idC']")
    SPECIES_SORTED = (By.XPATH, "//tbody[@class='ant-table-tbody']/tr[2]/descendant::td[contains("
                                "text(),'Rattus norvegicus')]")
    TABLE = (By.XPATH, "//tbody[@class='ant-table-tbody']")
    TEXT_CONTAINER = (By.XPATH, "//div[@id='text-field-container']")
