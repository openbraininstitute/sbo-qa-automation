# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class SpeciesSelectorLocators:
    """Brain region banner and species selector — shared by every /data page.

    The banner is always rendered. The region switcher inside it is rendered only in
    focused mode: in All-species mode there is no single species, so there is no brain
    region to point at and the app hides the switcher on purpose.
    """

    BRAIN_REGION_BANNER = (By.CSS_SELECTOR, "div[data-label='brain-region-banner']")
    BRAIN_REGION_SWITCHER = (By.CSS_SELECTOR, "div[data-label='brain-region-switcher']")

    SPECIES_SELECTOR = (By.CSS_SELECTOR, "span#species-selector")
    SPECIES_TRIGGER = (
        By.CSS_SELECTOR,
        "span#species-selector button[data-slot='select-trigger']",
    )
    # Reads "All" in all-species mode, otherwise the selected species display name.
    SPECIES_VALUE = (
        By.XPATH,
        "//span[@id='species-selector']//span[contains(@class,'font-bold')]",
    )

    SPECIES_OPTION_ALL = (By.CSS_SELECTOR, "#species-selector-option__all")
    SPECIES_OPTION_ANY = (
        By.CSS_SELECTOR,
        "[id^='species-selector-option__'][data-hierarchy-id]",
    )

    # Rendered on /data instead of the 3D viewer when no species is selected.
    ALL_SPECIES_ATLAS_GRID = (By.CSS_SELECTOR, "#all-species-atlas-grid")
    ALL_SPECIES_ATLAS_CARD = (By.CSS_SELECTOR, "[data-testid='all-species-atlas-card']")
