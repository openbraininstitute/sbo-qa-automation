# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class ExplorePageLocators:
    EXPLORE_LINK1 = (By.XPATH, "//a[@href='/mmb-beta/explore/simulation-campaigns']//h1[text("
                               ")='Brain & cells annotations']")
    EXPLORE_TITLE = (By.XPATH, "//a[text()='Explore']")
    INTERACTIVE_EXPLORATION = (By.XPATH, "//h2[text()='Interactive exploration']")
    EXPERIMENTAL_DATA_BTN = (By.XPATH, "//button[text()='Experimental data']")
    MODEL_DATA_BTN = (By.XPATH, "//button[text()='Model data']")
    LITERATURE = (By.XPATH, "//button[text()='Literature']")
    NEURON_ELECTROPHYSIOLOGY = (By.XPATH, "//h3[contains(text(),'Neuron "
                                          "electrophysiology')]//ancestor::a[1]["
                                          "@href='/app/explore/electrophysiology']")
    NEURON_MORPHOLOGY = (By.XPATH, "//h3[contains(text(),'Neuron morphology')]//ancestor::a[1]["
                                   "@href='/app/explore/morphology']")
    BOUTON_DENSITY = (By.XPATH, "//h3[contains(text(),'Bouton density')]//ancestor::a[1]["
                                "@href='/app/explore/bouton-density']")
    NEURON_DENSITY = (By.XPATH, "//h3[contains(text(),'Neuron density')]//ancestor::a[1]["
                                "@href='/app/explore/neuron-density']")
    SYNAPSE_PER_CONNECTION = (By.XPATH, "//h3[contains(text(),'Synapse per "
                                        "connection')]//ancestor::a[1]["
                                        "@href='/app/explore/synapse-per-connection']")
    EXPLORE_URL = (By.XPATH, "//a[@href='/app/explore']")
    LITERATURE_LINK = (By.ID, "#explore-navigation-/explore/literature")
