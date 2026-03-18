# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class ExploreNDensityPageLocators:
    AI_ASSISTANT_PANEL = (By.XPATH, "//div[starts-with(@class,'ai-assistant-module')]")
    AI_ASSISTANT_PANEL_CLOSE = (By.XPATH, "(//span[@aria-label='minus'])[3]")
    BRAIN_REGIONS_PANEL_BTN = (By.CSS_SELECTOR, ".ant-btn-icon")
    BR_REGION_BANNER = (By.CSS_SELECTOR, "div[aria-label='brain-region-banner']")
    BR_REGION_CLOSE_BTN = (By.XPATH, "//div[@aria-label='brain-region-banner']//span[@aria-label='close']")
    BR_REGION_SEARCH_INPUT = (By.CSS_SELECTOR, "input#region-search")
    BR_REGION_ROOT_OPTION = (By.XPATH, "//button[@title='Root']")
    LOAD_MORE_BUTTON = (By.XPATH, "//button[@type='button' and text()='Load 30 more results...']")
    BR_VERTICAL_PANEL_CEREBRUM = (By.XPATH, "//div[@aria-label='brain-region-banner']//span[contains(@class, 'font-bold') and text()='Cerebrum']")
    TABLE_ROWS = (By.CSS_SELECTOR, "tbody.ant-table-tbody tr.ant-table-row")
    TABLE_CELLS = (
        By.CSS_SELECTOR,
        "tbody.ant-table-tbody td.ant-table-cell.text-primary-7.cursor-pointer.ant"
        "-table-cell-ellipsis")
    NDENSITY_TAB = (By.CSS_SELECTOR, "a#counter-experimental_neuron_density")
    LV_THUMBNAIL = (By.XPATH, "//img[starts-with(@alt,'Morphology preview')]")
    LV_BRAIN_REGION = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Brain region']")
    LV_MTYPE = (By.XPATH, "//th[@data-testid='column-header']//div[text()='M-type']")
    LV_ETYPE = (By.XPATH, "//th[@data-testid='column-header']//div[text()='E-type']")
    LV_DENSITY = (By.XPATH, "//th[@data-testid='column-header']//div[contains(text(),'Density')]")
    LV_NMEASUREMENTS = (By.XPATH, "//th[@data-testid='column-header']//div[contains(text(),'N° of "
                                  "measurements')]")
    LV_NAME = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Name']")
    LV_SPECIES = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Species']")
    LV_AGE = (By.XPATH, "//th[@data-testid='column-header']//div[contains(text(),'Age')]")
    LV_CONTRIBUTORS = (By.XPATH, "//th[@data-testid='column-header']//div[text()='Contributors']")
    LV_REGISTRATION_DATE = (By.XPATH, "//th[@data-testid='column-header']//div[text("
                                      ")='Registration "
                                      "date']")
    LV_FILTER_MTYPE = (By.XPATH, "//span[text()='M-type']")
    LV_BR_ROW1 = (By.XPATH, "(//td[@class='ant-table-cell text-primary-7 cursor-pointer before:!content-none ant-table-cell-ellipsis'])[1]")
    DV_NAME_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Name']")
    DV_DESC_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Description']")
    DV_CONTRIBUTORS_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text("
                                       ")='Contributors']")
    DV_REG_DATE_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text("
                                   ")='Registration date']")
    DV_BRAIN_REG_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Brain "
                                    "Region']")
    DV_LICENSE_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='License']")
    DV_SPECIES_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Species']")
    DV_NUM_MEAS_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='N° of "
                                   "Measurements']")
    DV_MTYPE_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='M-Type']")
    DV_ETYPE_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='E-Type']")
    DV_DENSITY_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Density']")
    DV_AGE_TITLE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Age']")
    DV_DOWNLOAD_BTN = (By.XPATH, "//div[text()='Download']")
    DV_NAME_VALUE = (By.XPATH,
                     "//div[@class='text-neutral-4 uppercase' and normalize-space(text())='Name']/following-sibling::div")
    DV_DESC_VALUE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Description']/following-sibling::div")
    DV_CONTRIBUTORS_VALUE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Contributors']/following-sibling::div")
    DV_REG_DATE_VALUE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Registration date']/following-sibling::div")
    DV_BRAIN_REG_VALUE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Brain Region']/following-sibling::div")
    DV_SPECIES_VALUE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Species']/following-sibling::div")
    DV_LICENSE_VALUE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='License']/following-sibling::div")
    DV_MTYPE_VALUE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='M-Type']/following-sibling::div")
    DV_AGE_VALUE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Age']/following-sibling::div")
    DV_ETYPE_VALUE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='E-Type']/following-sibling::div")
    DV_DENSITY_VALUE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='Density']/following-sibling::div")
    DV_NUM_MEAS_VALUE = (By.XPATH, "//div[@class='text-neutral-4 uppercase' and text()='N° of Measurements']/following-sibling::div")
    SCROLL_SIDEWAYS = (By.XPATH, "(//button[starts-with(@class,'ant-btn ant-btn-circle ant-btn-default')])[2]")

    MINI_DETAIL_VIEW = (By.CSS_SELECTOR, "#mini-detail-view-container")
    MDV_NAME = (By.XPATH, "//h1[@class='text-2xl font-bold break-all']")
    MDV_DESCRIPTION = (By.CSS_SELECTOR, "#record-description")
    MDV_BRAIN_REGION_LABEL = (By.XPATH, "//div[text()='Brain Region']")
    MDV_BRAIN_REGION_VALUE = (By.XPATH, "//div[text()='Brain Region']/following-sibling::div")
    MDV_SPECIES_LABEL = (By.XPATH, "//div[text()='Species']")
    MDV_SPECIES_VALUE = (By.XPATH, "//div[text()='Species']/following-sibling::div")
    MDV_MTYPE_LABEL = (By.XPATH, "//div[text()='M-Type']")
    MDV_MTYPE_VALUE = (By.XPATH, "//div[text()='M-Type']/following-sibling::div")
    MDV_ETYPE_LABEL = (By.XPATH, "//div[text()='E-Type']")
    MDV_ETYPE_VALUE = (By.XPATH, "//div[text()='E-Type']/following-sibling::div")
    MDV_LICENSE_LABEL = (By.XPATH, "//div[text()='License']")
    MDV_LICENSE_VALUE = (By.XPATH, "//div[text()='License']/following-sibling::div")
    MDV_VIEW_DETAILS_BUTTON = (By.XPATH, "//a[@title='Go to details page' and contains(text(), 'View details')]")

