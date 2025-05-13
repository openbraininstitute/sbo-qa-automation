# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class ExplorePageLocators:
    AI_ASSISTANT_PANEL = (By.XPATH, "//button[starts-with(@class, 'literature-suggestions')]")
    AI_ASSISTANT_PANEL_BTN = (By.XPATH, "//span[@class='anticon anticon-minus']")
    ATLAS = (By.CSS_SELECTOR, "div[id='3d-area']")
    ATLAS_FULLSCREEN = (By.CSS_SELECTOR, "span[class='anticon anticon-fullscreen h-5 w-5 text-xl']")
    BOUTON_DENSITY_NRECORDS = (By.XPATH, "//a[@data-testid='experiment-dataset"
                                         "-ExperimentalBoutonDensity']//span[@class='mr-2 "
                                         "font-light']")
    BRAIN_REGION_PANEL = (By.XPATH, "//span[text()='Brain region']")
    BRP_CEREBRUM = (By.XPATH, "//span[@title='Cerebrum' and text()='Cerebrum']")
    CEREBRAL_CORTEX_TITLE = (By.XPATH, "//span[@title='Cerebral cortex']")
    CEREBRUM_BTN = (By.XPATH, "(//button[@type='button' and @aria-expanded='false'])[3]")
    CEREBRUM_TITLE = (By.XPATH, "//span[@class='line-clamp-2' and text()='Cerebrum']")
    COUNT_SWITCH = (By.CSS_SELECTOR, "button[type='button'][role='switch'][aria-checked='false']")
    DATA_PANEL = (By.CSS_SELECTOR, "div[id='statistic-panel']")
    EXPERIMENTAL_DATA_BTN = (By.XPATH, "//button[text()='Experimental data']")
    EXPLORE_LINK1 = (By.XPATH, "//a[@href='/mmb-beta/explore/simulation-campaigns']//h1[text("
                               ")='Brain & cells annotations']")
    EXPLORE_TITLE = (By.XPATH, "//a[text()='explore']")
    EXPLORE_URL = (By.XPATH, "//a[@href='/explore']")
    FULLSCREEN_EXIT = (By.CSS_SELECTOR, "span[aria-label='fullscreen-exit']")
    INTERACTIVE_EXPLORATION = (By.XPATH, "//h2[text()='Interactive exploration']")
    LITERATURE = (By.XPATH, "//button[text()='Literature']")
    LITERATURE_LINK = (By.ID, "#explore-navigation-/explore/literature")
    LITERATURE_MORPHOLOGY_TAB = (By.CSS_SELECTOR, "a[data-testid='literature-articles-ExperimentalNeuronMorphology']")
    LITERATURE_EPHYS_TAB = (By.CSS_SELECTOR, "a[data-testid='literature-articles-ExperimentalElectroPhysiology']")
    LITERATURE_NDENSITY_TAB = (By.CSS_SELECTOR, "a[data-testid='literature-articles-ExperimentalNeuronDensity']")
    LITERATURE_BDENSITY_TAB = (By.CSS_SELECTOR, "a[data-testid='literature-articles-ExperimentalBoutonDensity']")
    LITERATURE_SYNAPSES_TAB = (By.CSS_SELECTOR, "a[data-testid='literature-articles-ExperimentalSynapsePerConnection']")
    MODEL_DATA_BTN = (By.XPATH, "//button[text()='Model data']")
    MORPHOLOGY_NRECORDS = (By.XPATH, "//a[@data-testid='experiment-dataset"
                                     "-ExperimentalNeuronMorphology']//span[@class='mr-2 "
                                     "font-light']")
    NEURONS_PANEL = (By.CSS_SELECTOR, "div[id='neurons-panel']")
    NEURONS_PANEL_MTYPE = (By.XPATH, "(//div[@data-state='closed' and "
                                     "@data-orientation='vertical' and "
                                     "starts-with(@data-tree-id,'http://uri')])[1]")
    NEURONS_PANEL_GRID_MTYPES = (By.CSS_SELECTOR, "div.relative.ml-4.last\\:mb-5")
    NEURONS_PANEL_MTYPE_BTN = (By.XPATH, "(//div[starts-with(@class,"
                                         "'secondary-scrollbar')]//button[@type='button' and "
                                         "starts-with(@class,'accordion-trigger') and "
                                         "@aria-expanded='false' and "
                                         "@data-orientation='vertical'])[1]")
    NEURONS_PANEL_ETYPES_TITLE = (By.XPATH, "//h6[starts-with(@class, 'ml-4 text-sm') and text("
                                            ")='E-TYPES']")
    NEURONS_PANEL_ISOCORTEX_MTYPE = (By.XPATH, "//div[text()='L6_TPC:C']")
    NEURON_EPHYS_NRECORDS = (By.XPATH, "//a[@data-testid='experiment-dataset"
                                       "-ExperimentalElectroPhysiology']//span[@class='mr-2 "
                                       "font-light']")

    PANEL_EMODEL = (By.CSS_SELECTOR, "a[data-testid='experiment-dataset-CircuitEModel']")
    PANEL_MEMODEL = (By.CSS_SELECTOR, "a[data-testid='experiment-dataset-CircuitMEModel']")
    PANEL_SYNAPTOME = (By.CSS_SELECTOR, "a[data-testid='experiment-dataset-SingleNeuronSynaptome']")
    SELECTED_BRAIN_REGION = (By.XPATH, "//h1[@title='Isocortex']/span[text()='Isocortex']")
    SEARCH_REGION = (By.XPATH, "//input[@class='ant-select-selection-search-input']")
    SYNAPSE_PER_CONNECTION_NRECORDS = (By.XPATH, "//a[@data-testid='experiment-dataset"
                                                 "-ExperimentalSynapsePerConnection']//span["
                                                 "@class='mr-2 font-light']")
    TOTAL_COUNT_DENSITY = (By.XPATH, "//h2[@data-testid='total-count-or-density']")
    TOTAL_COUNT_N = (By.XPATH, "//small[@class='text-base font-normal text-gray-300']")
    TOTAL_COUNT_SWITCH = (By.XPATH, "//button[@type='button' and @role='switch' and "
                                    "@title='density or count' and @aria-checked='false']")

    NEURON_MORPHOLOGY = (By.XPATH, "//a[@data-testid='experiment-dataset-ExperimentalNeuronMorphology' and "
                                   "@href='/app/virtual-lab/lab/37a3a2e8-a4b4-456b-8aff-4e23e87a5cbc/project/8abcb1e3-b714-4267-a22c-3b3dc4be5306/explore/interactive/experimental/morphology']")
    NEURON_ELECTROPHYSIOLOGY = (By.XPATH, "//a[@data-testid='experiment-dataset-ExperimentalElectroPhysiology' and @href='/app/virtual-lab/lab/37a3a2e8-a4b4-456b-8aff-4e23e87a5cbc/project/8abcb1e3-b714-4267-a22c-3b3dc4be5306/explore/interactive/experimental/electrophysiology']")
    NEURON_DENSITY = (By.XPATH, "//a[@data-testid='experiment-dataset-ExperimentalNeuronDensity'"
                                "and @href='/virtual-lab/lab/37a3a2e8-a4b4-456b-8aff-4e23e87a5cbc/project/8abcb1e3-b714-4267-a22c-3b3dc4be5306/explore/interactive/experimental/neuron-density']")
    BOUTON_DENSITY = (By.XPATH, "//a[@data-testid='experiment-dataset-ExperimentalBoutonDensity' "
                                "and @href='/app/virtual-lab/lab/37a3a2e8-a4b4-456b-8aff-4e23e87a5cbc/project/8abcb1e3-b714-4267-a22c-3b3dc4be5306/explore/interactive/experimental/bouton-density']")
    SYNAPSE_PER_CONNECTION = (By.XPATH, "//a[@data-testid='experiment-dataset-ExperimentalSynapsePerConnection' and "
                                    "@href='/app/virtual-lab/lab/37a3a2e8-a4b4-456b-8aff-4e23e87a5cbc/project/8abcb1e3-b714-4267-a22c-3b3dc4be5306/explore/interactive/experimental/synapse-per-connection']")
    NEURON_DENSITY_NRECORDS = (By.XPATH, "//a[@data-testid='experiment-dataset-ExperimentalNeuronDensity']//span[@class='mr-2 font-light']")

