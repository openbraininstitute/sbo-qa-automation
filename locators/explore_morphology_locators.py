# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class ExploreMorphologyPageLocators:
    AI_ASSISTANT_PANEL = (By.XPATH, "//div[starts-with(@class,'ai-assistant-module')]")
    AI_ASSISTANT_PANEL_CLOSE_BTN = (By.XPATH, "(//span[@aria-label='minus'])[3]")
    BACK_IE_BTN = (By.XPATH, "//div[.='Back to list']")
    BRAIN_REGION_COLUMN_TITLE = (By.XPATH, "//div[text()='Brain Region']")
    BR_SORTED = (By.XPATH, "//div[contains(@class,'ag-cell') and @col-id='brainRegion' and contains(normalize-space(),"
                           "'Primary somatosensory area')]")
    BR_SORT_ARROW = (By.CSS_SELECTOR, ".ag-header-cell[col-id='brainRegion'] .ag-header-cell-label, "
                                      ".ag-header-cell[col-id='brainRegion']")
    CELLS = (By.CSS_SELECTOR, ".ag-cell")
    CLEAR_FILTERS_BTN = (By.XPATH, "//button[@type='button']/div[text()='Clear filters']")
    CONTRIBUTORS_COLUMN_TITLE = (By.XPATH, "//div[contains(text(),'Contributors')]")
    DV_AGE_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Age']")
    DV_AP_TITLE = (By.XPATH, "//h2[text()='Apical Dendrite']")
    DV_AXON_TITLE = (By.XPATH, "//h2[text()='Axon']")
    DV_BACK_BTN = (By.XPATH, "//a[contains(@href,'/mmb-beta/explore/interactive/experimental"
                             "/morphology')]")
    DV_BD_TITLE = (By.XPATH, "//h2[text()='Basal Dendrite']")
    DV_BRAIN_REGION_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Brain "
                                       "Region']")
    DV_CONTRIBUTORS_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text("
                                       ")='Contributors']")
    DV_DESCRIPTION_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text("
                                      ")='Description']")
    DV_DOWNLOAD_BTN = (By.CSS_SELECTOR, "button[title='Download'] div[class='flex items-center px-2 group-hover:py-2']")
    DV_LICENSE_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='License']")
    DV_MORPHOMETRICS_TITLE = (By.XPATH, "//h1[.='Morphometrics']")
    DV_MTYPE_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='M-Type']")
    DV_NAME_TITLE = (By.XPATH, "//div[@class='text font-thin' and text()='Name']")
    DV_NM_TITLE = (By.XPATH, "//h2[text()='Neuron Morphology']")
    DV_REGISTRATION_DATE_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text("
                                            ")='Registration date']")
    DV_SELECTED_BR = (By.XPATH, "//div[@class='grid w-1/2 auto-rows-min grid-cols-3 gap-x-8 "
                                "gap-y-6']//div[text()='Brain Region']/following-sibling::div["
                                "text()='Anterior"
                                "cingulate area, dorsal part, layer 2/3']")
    DV_SOMA_TITLE = (By.XPATH, "//h2[text()='Soma']")
    DV_SPECIES_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Species']")
    FILTERED_MTYPE = (By.CSS_SELECTOR, ".ag-cell[col-id='mtype']")
    FILTER_MTYPE_SEARCH = (By.XPATH, "//div[@class='ant-select-selection-overflow']")
    LV_FILTER_SEARCH_FIELD = (By.XPATH, "(//div[@class='ant-select-selector'])[2]")
    FILTER_MTYPE_TEXT_INPUT = (By.XPATH, "(//input[@class='ant-select-selection-search-input'])[2]")
    FILTER_PANEL = (By.XPATH, "//div[@data-testid='listing-view-filter-panel']")
    FIRST_ROW = (By.CSS_SELECTOR, ".ag-center-cols-container .ag-row[role='row']")
    LV_BRAIN_REGION = (By.CSS_SELECTOR, ".ag-header-cell[col-id='brainRegion']")
    LV_CHECKBOX = (By.XPATH, "")
    LV_CONTRIBUTORS = (By.CSS_SELECTOR, ".ag-header-cell[col-id='contributions']")
    LV_FILTER_APPLY_BTN = (By.XPATH, "//button[contains(text(),'Apply') and @type='submit']")
    LV_FILTER_MTYPE = (By.XPATH, "//span[text()='M-type']")
    LV_FILTER_SEARCH = (By.XPATH, "//div[@class='ant-select-selection-search']")
    LV_MTYPE = (By.CSS_SELECTOR, ".ag-header-cell[col-id='mtype']")
    LV_NAME = (By.CSS_SELECTOR, ".ag-header-cell[col-id='name']")
    LV_PREVIEW = (By.CSS_SELECTOR, ".ag-header-cell[col-id='preview']")
    LV_REGISTRATION_DATE = (By.CSS_SELECTOR, ".ag-header-cell[col-id='registrationDate']")
    LV_SPECIES = (By.CSS_SELECTOR, ".ag-header-cell[col-id='species']")
    LV_THUMBNAIL = (By.CSS_SELECTOR, ".ag-cell[col-id='preview'] img")
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
    RECORDS = (By.XPATH, "//a[.//div[normalize-space()='Morphology']]//span[not(text()='of')]")
    ROW = (By.CSS_SELECTOR, ".ag-center-cols-container .ag-row[role='row']")
    SEARCH_INPUT_FIELD = (By.XPATH, "//input[@placeholder='Search for resources...']")
    SEARCH_NAME = (By.XPATH, "//div[contains(@class,'ag-cell') and @col-id='name' and normalize-space()='mtC070301B_idC']")
    SPECIES_SORTED = (By.XPATH, "//div[contains(@class,'ag-cell') and @col-id='species' and contains("
                                "normalize-space(),'Rattus norvegicus')]")
    TABLE = (By.CSS_SELECTOR, ".ag-root-wrapper, .ag-root")
    TEXT_CONTAINER = (By.XPATH, "//div[@id='text-field-container']")
