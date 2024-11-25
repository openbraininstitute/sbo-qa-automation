# Copyright (c) 2024 Blue Brain Project/EPFL
#
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class ExplorePageLocators:
    ATLAS = (By.CSS_SELECTOR, "div[id='3d-area']")
    ATLAS_FULLSCREEN = (By.CSS_SELECTOR, "span[class='anticon anticon-fullscreen h-5 w-5 text-xl']")
    BOUTON_DENSITY = (By.XPATH, "//a[@data-testid='experiment-dataset-ExperimentsBoutonDensity' "
                                "and @href='/app/explore/interactive/experimental/bouton-density']")
    BOUTON_DENSITY_NRECORDS = (By.XPATH, "//a[@data-testid='experiment-dataset"
                                         "-ExperimentsBoutonDensity']//span[@class='mr-2 "
                                         "font-light']")
    BRAIN_REGION_PANEL = (By.XPATH, "//span[text()='Brain region']")
    BRP_CEREBRUM = (By.XPATH, "//span[@title='Cerebrum' and text()='Cerebrum']")
    CEREBRAL_CORTEX_TITLE = (By.XPATH, "//span[@title='Cerebral Cortex']")
    CEREBRUM_BTN = (By.XPATH, "(//button[@type='button' and @aria-expanded='false'])[3]")
    COUNT_SWITCH = (By.CSS_SELECTOR, "button[type='button'][role='switch'][aria-checked='false']")
    EXPERIMENTAL_DATA_BTN = (By.XPATH, "//button[text()='Experimental data']")
    EXPLORE_LINK1 = (By.XPATH, "//a[@href='/mmb-beta/explore/simulation-campaigns']//h1[text("
                               ")='Brain & cells annotations']")
    EXPLORE_TITLE = (By.XPATH, "//a[text()='Explore']")
    EXPLORE_URL = (By.XPATH, "//a[@href='/app/explore']")
    FULLSCREEN_EXIT = (By.CSS_SELECTOR, "span[aria-label='fullscreen-exit']")
    INTERACTIVE_EXPLORATION = (By.XPATH, "//h2[text()='Interactive exploration']")
    LITERATURE = (By.XPATH, "//button[text()='Literature']")
    LITERATURE_LINK = (By.ID, "#explore-navigation-/explore/literature")
    MODEL_DATA_BTN = (By.XPATH, "//button[text()='Model data']")
    MORPHOLOGY_NRECORDS = (By.XPATH, "//a[@data-testid='experiment-dataset"
                                     "-ExperimentalNeuronMorphology']//span[@class='mr-2 "
                                     "font-light']")
    NEURONS_PANEL = (By.CSS_SELECTOR, "div[id='neurons-panel']")
    NEURON_DENSITY = (By.XPATH, "//a[@data-testid='experiment-dataset-ExperimentalNeuronDensity' "
                                "and @href='/app/explore/interactive/experimental/neuron-density']")
    NEURON_DENSITY_NRECORDS = (By.XPATH, "//a[@data-testid='experiment-dataset"
                                         "-ExperimentalNeuronDensity']//span[@class='mr-2 "
                                         "font-light']")
    NEURON_ELECTROPHYSIOLOGY = (By.XPATH, "//a[@data-testid='experiment-dataset"
                                          "-ExperimentalElectroPhysiology' and "
                                          "@href='/app/explore/interactive/experimental"
                                          "/electrophysiology']")
    NEURON_EPHYS_NRECORDS = (By.XPATH, "//a[@data-testid='experiment-dataset"
                                       "-ExperimentalElectroPhysiology']//span[@class='mr-2 "
                                       "font-light']")
    NEURON_MORPHOLOGY = (By.XPATH, "//a[@data-testid='experiment-dataset"
                                   "-ExperimentalNeuronMorphology' and "
                                   "@href='/app/explore/interactive/experimental/morphology']")
    SELECTED_BRAIN_REGION = (By.XPATH, "//h1[@title='Isocortex']/span[text()='Isocortex']")
    SEARCH_REGION = (By.XPATH, "//input[@class='ant-select-selection-search-input']")
    SYNAPSE_PER_CONNECTION = (By.XPATH, "//a[@data-testid='experiment-dataset"
                                        "-ExperimentalSynapsePerConnection' and "
                                        "@href='/app/explore/interactive/experimental/synapse-per"
                                        "-connection']")
    SYNAPSE_PER_CONNECTION_NRECORDS = (By.XPATH, "//a[@data-testid='experiment-dataset"
                                                 "-ExperimentalSynapsePerConnection']//span["
                                                 "@class='mr-2 font-light']")
