# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class ExplorePageLocators:
    EXPLORE_LINK1 = (By.XPATH, "//a[@href='/mmb-beta/explore/simulation-campaigns']//h1[text("
                               ")='Brain & cells annotations']")
    EXPLORE_TITLE = (By.XPATH, "//a[text()='explore']")
    INTERACTIVE_EXPLORATION = (By.XPATH, "//h2[text()='Interactive exploration']")

    EXPERIMENTAL_DATA_BTN = (By.XPATH, "//button[text()='Experimental data']")

    MODEL_DATA_BTN = (By.XPATH, "//button[text()='Model data']")

    SIMULATIONS = (By.XPATH, "//h2[text()='Simulations']")
    PORTALS = (By.XPATH, "//h2[text()='Portals']")
    GALLERY = (By.XPATH, "//h2[text()='Gallery']")
    LITERATURE = (By.XPATH, "//button[text()='Literature']")
    NEURON_ELECTROPHYSIOLOGY = (By.XPATH, "//h3[contains(text(),'Neuron "
                                          "electrophysiology')]//ancestor::a[1]["
                                          "@href='/mmb-beta/explore/electrophysiology']")
    NEURON_MORPHOLOGY = (By.XPATH, "//h3[contains(text(),'Neuron morphology')]//ancestor::a[1]["
                                   "@href='/mmb-beta/explore/morphology']")
    BOUTON_DENSITY = (By.XPATH, "//h3[contains(text(),'Bouton density')]//ancestor::a[1]["
                                "@href='/mmb-beta/explore/bouton-density']")
    NEURON_DENSITY = (By.XPATH, "//h3[contains(text(),'Neuron density')]//ancestor::a[1]["
                                "@href='/mmb-beta/explore/neuron-density']")
    LAYER_THICKNESS = (By.XPATH, "//h3[contains(text(),'Layer thickness')]//ancestor::a[1]["
                                 "@href='/mmb-beta/explore/layer-thickness']")
    SYNAPSE_PER_CONNECTION = (By.XPATH, "//h3[contains(text(),'Synapse per "
                                        "connection')]//ancestor::a[1]["
                                        "@href='/mmb-beta/explore/synapse-per-connection']")

    EXPLORE_URL = (By.XPATH, "//a[@href='/mmb-beta/explore']")
    INTERACTIVE_EXPLORATION_LINK = (By.ID, "#explore-navigation-/explore/interactive")
    BRAIN_MODELS_LINK = (By.XPATH, "//h2[contains(text(),'Brain Models')]//ancestor::a[1]["
                                   "@href='/mmb-beta/explore/brain-models']")
    SIMULATIONS_LINK = (By.XPATH, "//h2[contains(text(),'Simulations')]//ancestor::a[1]["
                                  "@href='/mmb-beta/explore/simulation-campaigns']")
    PORTALS_LINK = (By.ID, "#explore-navigation-/explore/portals")
    GALLERY_LINK = (By.ID, "#explore-navigation-/explore/gallery")
    LITERATURE_LINK = (By.ID, "#explore-navigation-/explore/literature")