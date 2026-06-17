# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class ExploreMeModelLocators:
    """Locators for the ME-model Detail View page.

    Entry point: Login → Data → Model → ME-model → Open Detail View
    URL pattern:
    /data/view/memodel/{id}/overview?h_id={h_id}&br_id={br_id}
    """

    """Explore page: navigation to ME-model list."""
    BRAIN_REGION_PANEL = (By.CSS_SELECTOR, "div[data-label='brain-region-switcher']")
    BRAIN_REGION_SPECIES_DROPDOWN = (
        By.XPATH,
        "//span[@id='species-selector']//button[@data-slot='select-trigger']",
    )
    BRAIN_REGION_SPECIES_VALUE = (
        By.XPATH,
        "//span[@id='species-selector']//span[contains(@class,'font-bold')]",
    )
    BRAIN_REGION_SPECIES_OPTIONS = (
        By.CSS_SELECTOR,
        "div[data-slot='select-item'], div[role='option']",
    )
    BR_SEARCH_FIELD = (
        By.XPATH,
        "//input[@id='region-search']",
    )
    BR_CEREBRUM_TITLE = (
        By.XPATH,
        "//div[@data-label='brain-region-switcher']//span[contains(@class,'font-bold')]",
    )

    """Model data tab and ME-model tab."""
    MODEL_DATA_TAB = (By.XPATH, "//button[@role='tab' and text()='Model']")
    ME_MODEL_TAB = (By.XPATH, "//div[normalize-space()='ME-model']")

    """List view: table rows and search."""
    LV_TABLE_BODY = (By.CSS_SELECTOR, ".ant-table-body")
    LV_TABLE_ROWS = (
        By.XPATH,
        "//tbody[contains(@class,'ant-table-tbody')]"
        "//tr[contains(@class,'ant-table-row') and not(contains(@class,'ant-table-measure-row'))]",
    )
    INPUT_PLACEHOLDER = (By.CSS_SELECTOR, "input[placeholder='Search for entities...']")
    SPINNER = (By.XPATH, "//div[@class='ant-spin ant-spin-spinning']")

    """Mini detail view (after clicking a row)."""
    MINI_DETAIL_VIEW_BTN = (By.CSS_SELECTOR, "a[title='Go to details page']")

    """Detail View: left-hand side tabs."""
    DV_OVERVIEW_TAB = (By.XPATH, "//a[normalize-space()='Overview']")
    DV_ANALYSIS_TAB = (By.XPATH, "//a[normalize-space()='Analysis']")
    DV_CONFIGURATION_TAB = (By.XPATH, "//a[normalize-space()='Configuration']")
    DV_RELATED_ARTIFACTS_TAB = (By.XPATH, "//a[contains(@href,'related-artifacts')]")

    """Detail View: action buttons."""
    DV_COPY_ID_BTN = (
        By.XPATH,
        "//button[.//div[text()='Copy ID']]",
    )
    DV_SIMULATE_BTN = (
        By.XPATH,
        "//a[.//div[text()='Simulate']] | //button[.//div[text()='Simulate']]",
    )
    DV_DOWNLOAD_BTN = (
        By.XPATH,
        "//button[.//div[text()='Download']]",
    )

    """Detail View: Overview tab — metadata labels and values."""
    DV_NAME_VALUE = (
        By.XPATH,
        "(//div[contains(@class,'text-2xl') and contains(@class,'font-bold')])[1]"
        " | //h1[contains(@class,'font-bold')]",
    )
    DV_DESCRIPTION_LABEL = (By.XPATH, "//div[contains(@class,'text-primary-3') and contains(normalize-space(),'escription')]")
    DV_DESCRIPTION_VALUE = (By.XPATH, "//div[contains(@class,'text-primary-3') and contains(normalize-space(),'escription')]/following-sibling::div[contains(@class,'mt-2') and contains(@class,'break-words')]")
    DV_CREATED_BY_LABEL = (By.XPATH, "//div[contains(@class,'text-primary-3') and contains(normalize-space(),'reated by')]")
    DV_CREATED_BY_VALUE = (By.XPATH, "//div[contains(@class,'text-primary-3') and contains(normalize-space(),'reated by')]/following-sibling::div[contains(@class,'mt-2') and contains(@class,'break-words')]")
    DV_CONTRIBUTORS_LABEL = (By.XPATH, "//div[contains(@class,'text-primary-3') and normalize-space()='Contributors']")
    DV_CONTRIBUTORS_VALUE = (By.XPATH, "//div[contains(@class,'text-primary-3') and normalize-space()='Contributors']/following-sibling::div[contains(@class,'mt-2') and contains(@class,'break-words')]")
    DV_INSTITUTIONAL_CONTRIBUTORS_LABEL = (
        By.XPATH, "//div[contains(@class,'text-primary-3') and contains(normalize-space(),'nstitutional')]"
    )
    DV_INSTITUTIONAL_CONTRIBUTORS_VALUE = (
        By.XPATH, "//div[contains(@class,'text-primary-3') and contains(normalize-space(),'nstitutional')]/following-sibling::div[contains(@class,'mt-2') and contains(@class,'break-words')]"
    )
    DV_BRAIN_REGION_LABEL = (By.XPATH, "//div[contains(@class,'text-primary-3') and contains(normalize-space(),'rain')]")
    DV_BRAIN_REGION_VALUE = (By.XPATH, "//div[contains(@class,'text-primary-3') and contains(normalize-space(),'rain')]/following-sibling::div[contains(@class,'mt-2') and contains(@class,'break-words')]")
    DV_ETYPE_LABEL = (By.XPATH, "//div[contains(@class,'text-primary-3') and contains(normalize-space(),'-Type') and contains(normalize-space(),'E')]")
    DV_ETYPE_VALUE = (By.XPATH, "//div[contains(@class,'text-primary-3') and contains(normalize-space(),'-Type') and contains(normalize-space(),'E')]/following-sibling::div[contains(@class,'mt-2') and contains(@class,'break-words')]")
    DV_VALIDATED_LABEL = (By.XPATH, "//div[contains(@class,'text-primary-3') and contains(normalize-space(),'alidated')]")
    DV_VALIDATED_VALUE = (By.XPATH, "//div[contains(@class,'text-primary-3') and contains(normalize-space(),'alidated')]/following-sibling::div[contains(@class,'mt-2') and contains(@class,'break-words')]")
    DV_SPECIES_LABEL = (By.XPATH, "//div[contains(@class,'text-primary-3') and contains(normalize-space(),'pecies')]")
    DV_SPECIES_VALUE = (By.XPATH, "//div[contains(@class,'text-primary-3') and contains(normalize-space(),'pecies')]/following-sibling::div[contains(@class,'mt-2') and contains(@class,'break-words')]")
    DV_REGISTRATION_DATE_LABEL = (By.XPATH, "//div[contains(@class,'text-primary-3') and contains(normalize-space(),'egistration')]")
    DV_REGISTRATION_DATE_VALUE = (
        By.XPATH, "//div[contains(@class,'text-primary-3') and contains(normalize-space(),'egistration')]/following-sibling::div[contains(@class,'mt-2') and contains(@class,'break-words')]"
    )
    DV_MTYPE_LABEL = (By.XPATH, "//div[contains(@class,'text-primary-3') and contains(normalize-space(),'-Type') and contains(normalize-space(),'M')]")
    DV_MTYPE_VALUE = (By.XPATH, "//div[contains(@class,'text-primary-3') and contains(normalize-space(),'-Type') and contains(normalize-space(),'M')]/following-sibling::div[contains(@class,'mt-2') and contains(@class,'break-words')]")
    DV_STRAIN_LABEL = (By.XPATH, "//div[contains(@class,'text-primary-3') and contains(normalize-space(),'train')]")
    DV_STRAIN_VALUE = (By.XPATH, "//div[contains(@class,'text-primary-3') and contains(normalize-space(),'train')]/following-sibling::div[contains(@class,'mt-2') and contains(@class,'break-words')]")

    """Detail View: Analysis tab."""
    DV_ANALYSIS_DROPDOWN = (
        By.XPATH,
        "//div[contains(@class,'select-analysis-module')]//button[@data-slot='select-trigger']",
    )
    DV_ANALYSIS_READ_DESCRIPTION_BTN = (
        By.XPATH,
        "//div[contains(@class,'validation-explanation-module')]//button[.//div[contains(text(),'Read description')]]",
    )
    DV_ANALYSIS_PLOTS = (
        By.CSS_SELECTOR,
        "canvas.react-pdf__Page__canvas, img[alt='Stimulus plot']",
    )
    DV_ANALYSIS_PLOT_TEXT = (
        By.XPATH,
        "//div[contains(@class,'documentation-module')]",
    )
    DV_ANALYSIS_PLOT_DOWNLOAD_BTN = (
        By.XPATH,
        "//a[contains(@download,'.pdf')]",
    )
    DV_ANALYSIS_VALIDATION_CARDS = (
        By.XPATH,
        "//details[contains(@class,'validation-result-card-module')]",
    )
    DV_ANALYSIS_VALIDATION_SUMMARIES = (
        By.XPATH,
        "//details[contains(@class,'validation-result-card-module')]//summary",
    )

    """Detail View: Configuration tab."""
    DV_CONFIG_ME_MODEL_NAME = (
        By.XPATH,
        "//div[contains(@class,'text-2xl') and contains(@class,'font-bold')]",
    )
    DV_CONFIG_M_MODEL_SECTION = (
        By.XPATH,
        "//div[contains(@class,'card-container-module') and .//div[contains(text(),'M-Model')]]",
    )
    DV_CONFIG_E_MODEL_SECTION = (
        By.XPATH,
        "//div[contains(@class,'card-container-module') and .//div[contains(text(),'E-Model')]]",
    )
    DV_CONFIG_M_MODEL_MORE_DETAILS = (
        By.XPATH,
        "//div[contains(@class,'card-container-module') and .//div[contains(text(),'M-Model')]]//a[contains(text(),'More details')]",
    )
    DV_CONFIG_E_MODEL_MORE_DETAILS = (
        By.XPATH,
        "//div[contains(@class,'card-container-module') and .//div[contains(text(),'E-Model')]]//a[contains(text(),'More details')]",
    )

    """Detail View: Breadcrumbs and Close button."""
    DV_BREADCRUMB_DATA = (By.XPATH, "//a[contains(@class,'capitalize') and text()='Data']")
    DV_BREADCRUMB_MODEL = (By.XPATH, "//a[contains(@class,'capitalize') and text()='Model']")
    DV_BREADCRUMB_ME_MODEL = (By.XPATH, "//span[contains(@class,'font-bold')]//a[contains(text(),'ME-model')]")
    DV_CLOSE_BTN = (By.XPATH, "//a[@title='Close']")

    """Detail View: Related artifacts tab."""
    DV_RELATED_SIMULATION_ENTRIES = (
        By.XPATH,
        "//div[contains(@class,'@container')]"
        " | //div[contains(@class,'border') and .//div[contains(@class,'font-bold') and .//a]]",
    )
    DV_RELATED_NO_SIMULATIONS_MSG = (
        By.XPATH,
        "//*[contains(text(),'No simulations available')]"
        " | //*[contains(text(),\"haven't run any simulations\")]",
    )
