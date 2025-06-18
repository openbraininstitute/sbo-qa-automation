# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class ExploreNDensityPageLocators:
    AI_ASSISTANT_PANEL = (By.XPATH, "//div[starts-with(@class,'ai-assistant-module')]")
    AI_ASSISTANT_PANEL_CLOSE = (By.XPATH, "(//span[@aria-label='minus'])[2]")
    BRAIN_REGIONS_PANEL_BTN = (By.XPATH, "(//span[@class='anticon anticon-minus'])[1]")
    LOAD_MORE_BUTTON = (By.XPATH, "//button[@type='button' and text()='Load 30 more results...']")
    BRP_CEREBRUM = (By.XPATH, "//div[@class='whitespace-nowrap text-sm text-secondary-4' and text()='Cerebrum']")
    TABLE_ROWS = (By.CSS_SELECTOR, "tbody.ant-table-tbody tr.ant-table-row")
    TABLE_CELLS = (
        By.CSS_SELECTOR,
        "tbody.ant-table-tbody td.ant-table-cell.text-primary-7.cursor-pointer.ant"
        "-table-cell-ellipsis")
    NDENSITY_TAB = (By.XPATH, "//span[@class='ant-menu-title-content' and contains(text(),'Neuron "
                              "density')]")
    LV_THUMBNAIL = (By.XPATH, "//img[starts-with(@alt,'Morphology preview')]")
    LV_BRAIN_REGION = (By.XPATH, "//th[@data-testid='column-header']//div[contains(@class, 'explore-module') and text()='Brain region']")
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
    LV_BR_ROW1 = (By.XPATH, "(//td[starts-with(@class, 'ant-table-cell')])[13]")
    DV_NAME_TITLE = (By.XPATH, "//div[@class='text font-thin' and text()='Name']")
    DV_DESC_TITLE = (By.XPATH, "//div[@class='uppercase text-neutral-4' and text()='Description']")
    DV_CONTRIBUTORS_TITLE = (By.XPATH, "//div[@class='uppercase text-neutral-4' and text("
                                       ")='Contributors']")
    DV_REG_DATE_TITLE = (By.XPATH, "//div[@class='uppercase text-neutral-4' and text("
                                   ")='Registration date']")
    DV_BRAIN_REG_TITLE = (By.XPATH, "//div[@class='uppercase text-neutral-4' and text()='Brain "
                                    "Region']")
    DV_LICENSE_TITLE = (By.XPATH, "//div[@class='uppercase text-neutral-4' and text()='License']")
    DV_SPECIES_TITLE = (By.XPATH, "//div[@class='uppercase text-neutral-4' and text()='Species']")
    DV_NUM_MEAS_TITLE = (By.XPATH, "//div[@class='uppercase text-neutral-4' and text()='N° of "
                                   "Measurements']")
    DV_MTYPE_TITLE = (By.XPATH, "//div[@class='uppercase text-neutral-4' and text()='M-Type']")
    DV_ETYPE_TITLE = (By.XPATH, "//div[@class='uppercase text-neutral-4' and text()='E-Type']")
    DV_DENSITY_TITLE = (By.XPATH, "//div[@class='uppercase text-neutral-4' and text()='Density']")
    DV_AGE_TITLE = (By.XPATH, "//div[@class='uppercase text-neutral-4' and text()='Age']")
    DV_DOWNLOAD_BTN = (By.XPATH, "//div[text()='Download']")
    DV_NAME_VALUE = (By.XPATH,
                     "//div[@class='text font-thin' and normalize-space(text())='Name']/following-sibling::div//div[contains(@class, 'font-bold')]")
    DV_DESC_VALUE = (By.XPATH, "//div[div[normalize-space(text())='Description']]/div[2]")
    DV_CONTRIBUTORS_VALUE = (By.XPATH, "//div[div[normalize-space(text())='Contributors']]/div[2]")
    DV_REG_DATE_VALUE = (By.XPATH, "//div[div[normalize-space(text())='Registration date']]/div[2]")
    DV_BRAIN_REG_VALUE = (By.XPATH, "//div[div[normalize-space(text())='Brain Region']]/div[2]")
    DV_SPECIES_VALUE = (By.XPATH, "//div[div[normalize-space(text())='Species']]/div[2]")
    DV_LICENSE_VALUE = (By.XPATH, "//div[div[normalize-space(text())='License']]/div[2]")
    DV_MTYPE_VALUE = (By.XPATH, "//div[div[normalize-space(text())='M-Type']]/div[2]")
    DV_AGE_VALUE = (By.XPATH, "//div[div[normalize-space(text())='Age']]/div[2]")
    DV_ETYPE_VALUE = (By.XPATH, "//div[div[normalize-space(text())='E-Type']]/div[2]")
    DV_DENSITY_VALUE = (By.XPATH, "//div[div[normalize-space(text())='Density']]/div[2]")
    DV_NUM_MEAS_VALUE = (By.XPATH, "//div[div[normalize-space(text())='N° of Measurements']]/div[2]")

