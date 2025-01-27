# Copyright (c) 2024 Blue Brain Project/EPFL
#
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
    # MODAL_NEXT_BTN = (By.XPATH, "//button[@type='submit']")
    CREATE_VL = (By.XPATH, "(//button[@type='submit'])[2]")



