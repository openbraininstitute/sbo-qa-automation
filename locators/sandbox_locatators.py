# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute

# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class SandboxPageLocators:
    SANDBOX_BANNER_TITLE = (By.CSS_SELECTOR, '[data-testid=sandbox-banner-name-element]')
    CREATE_VLAB_BTN = (By.XPATH, "(//button[@type='button'])[2]")
    FORM_MODAL = (By.XPATH, "//div[@class='ant-modal-content']")
    INPUT_VLAB_NAME = (By.CSS_SELECTOR, "input[id='lab_form_name']")
    INPUT_VLAB_DESC = (By.CSS_SELECTOR, "textarea[id='lab_form_description']")
    INPUT_VLAB_EMAIL = (By.CSS_SELECTOR, "input[id='lab_form_email']")
    INPUT_VLAB_ENTITY = (By.CSS_SELECTOR, "input[id='lab_form_entity']")
    MODAL_NEXT_BTN = (By.XPATH, "//button[@type='submit']/span[contains(text(), 'Next')]")
    CREATE_VL = (By.XPATH, "(//button[@type='submit'])[2]")
    VL_BANNER_TITLE = (By.XPATH, "//span[@data-testid='lab-detail-banner-name-element' and contains(text(), 'UI Tests Virtual Lab')]")
    VL_OVERVIEW = (By.XPATH, "//div[@class='mx-4' and text()='Virtual lab overview']")
    PROJECTS = (By.XPATH, "//span[.='Projects']")
    CREATE_PROJECT_BTN = (By.XPATH, "(//button[@type='button'])[3]")
    INPUT_PROJECT_NAME = (By.XPATH, "//input[@id='name']")
    INPUT_PROJECT_DESCRIPTION = (By.XPATH, "//textarea[@id='description']")
    SAVE_PROJECT = (By.XPATH, "//button[@title='Save Changes' and @type='submit']")



