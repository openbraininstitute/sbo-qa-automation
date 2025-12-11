# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.by import By


class ExplorePageLocators:
    AI_ASSISTANT_PANEL_EXPANDED = (By.XPATH, "//div[starts-with(@class,'ai-assistant-module')]")
    AI_ASSISTANT_PANEL = (By.CSS_SELECTOR, "button[aria-label='expand AI assistant']")
    AI_ASSISTANT_PANEL_BTN = (By.XPATH, "//span[@class='anticon anticon-minus']")
    AI_ASSISTANT_PANEL_CLOSE = (By.XPATH, "(//span[@aria-label='minus'])[3]")
    AI_ASSISTANT_PANEL_BTN_OPEN = (By.CSS_SELECTOR, "span[aria-label='plus']")
    ATLAS = (By.CSS_SELECTOR, "div[id='3d-area']")
    ATLAS_FULLSCREEN = (By.CSS_SELECTOR, "span[aria-label='fullscreen']")
    BOUTON_DENSITY_NRECORDS = (By.CSS_SELECTOR, "a[data-testid='dataset-experimental_bouton_density'] span[class='mr-2 font-light']")
    BRAIN_REGION_PANEL = (By.CSS_SELECTOR, "#atlas-regions-selector")
    CEREBRAL_CORTEX_TITLE = (By.XPATH, "//div[@title='Cerebral cortex']/button")
    CEREBRUM_BTN = (By.XPATH, "//div[@title='Cerebrum' and @aria-label='Cerebrum']//button[@type='button' and starts-with(@class,'ml-auto flex flex-shrink-0 items-center')]")
    CEREBRUM_BTN_VLAB = (By.XPATH, "//div[@title='Cerebrum']/button")
    CEREBRUM_TITLE_BRAIN_REGION_PANEL = (By.XPATH, "i")
    CEREBRUM_TITLE_MAIN_PAGE = (By.CSS_SELECTOR, ".line-clamp-2")
    CLOSE_BTN = (By.CSS_SELECTOR, "span[aria-label='close']")
    COUNT_SWITCH = (By.CSS_SELECTOR, "button[type='button'][role='switch'][aria-checked='false']")
    DATA_HOME = (By.CSS_SELECTOR, "#workspace-explore-data")
    DATA_PANEL = (By.CSS_SELECTOR, "div[id='statistic-panel']")
    DATA_SKIP_BTN = (By.XPATH, "//button[normalize-space()='Skip']")
    EXPERIMENTAL_DATA_BTN = (By.XPATH, "(//button[normalize-space()='Experimental'])[1]")
    EXPLORE_LINK1 = (By.XPATH, "//a[@href='/mmb-beta/explore/simulation-campaigns']//h1[text("
                               ")='Brain & cells annotations']")
    EXPLORE_TITLE = (By.XPATH, "//div[@class='flex items-center justify-center select-none' and text()='Explore']")
    EXPLORE_TITLE_VLAB = (By.XPATH, "//a[normalize-space()='explore']")
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
    MODEL_DATA_BTN = (By.XPATH, "//button[text()='Model']")
    MORPHOLOGY_NRECORDS = (By.CSS_SELECTOR, "a[data-testid='dataset-reconstruction_morphology'] span[class='mr-2 font-light']")
    NEURON_DENSITY_NRECORDS = (By.CSS_SELECTOR, "a[data-testid='dataset-experimental_neuron_density'] span[class='mr-2 font-light']")
    NEURON_EPHYS_NRECORDS = (
    By.CSS_SELECTOR, "a[data-testid='dataset-electrical_cell_recording'] span[class='mr-2 font-light']")
    NEURONS_PANEL = (By.CSS_SELECTOR, "div[id='neurons-panel']")
    NEURONS_PANEL_MTYPE = (By.XPATH, "//h6[normalize-space()='M-TYPES']")
    NEURONS_PANEL_GRID_MTYPES = (By.CSS_SELECTOR, "div.relative.ml-4.last\\:mb-5")
    NEURONS_PANEL_MTYPE_BTN = (By.XPATH, "(//div[starts-with(@class,"
                                         "'secondary-scrollbar')]//button[@type='button' and "
                                         "starts-with(@class,'accordion-trigger') and "
                                         "@aria-expanded='false' and "
                                         "@data-orientation='vertical'])[1]")
    NEURONS_PANEL_ETYPES_TITLE = (By.XPATH, "//h6[starts-with(@class, 'ml-4 text-sm') and text("
                                            ")='E-TYPES']")
    NEURONS_PANEL_ISOCORTEX_MTYPE = (By.XPATH, "//div[text()='L6_TPC:C']")
    PANEL_CIRCUIT = (By.CSS_SELECTOR, "a[data-testid='dataset-Circuit']")
    PANEL_EMODEL = (By.CSS_SELECTOR, "a[data-testid='dataset-emodel']")
    PANEL_MEMODEL = (By.CSS_SELECTOR, "a[data-testid='dataset-memodel']")
    PANEL_SYNAPTOME = (By.CSS_SELECTOR, "a[data-testid='dataset-single_neuron_synaptome']")
    PUBLIC_TAB = (By.XPATH, "//button[contains(.,'Public')]")
    PROJECT_HOME_BTN = (By.CSS_SELECTOR, "#workspace-home")
    PROJECT_TAB = (By.XPATH, "//button[contains(.,'Project')]c")
    REPORTS_BTN = (By.CSS_SELECTOR, "#workspace-reports")
    SELECTED_BRAIN_REGION = (By.XPATH, "//h1[@title='Isocortex']/span[text()='Isocortex']")
    SEARCH_REGION = (By.XPATH, "//input[@class='ant-select-selection-search-input']")
    SIMULATIONS_BTN = (By.XPATH, "//button[text()='Simulations']")
    SKIP_ONBOARDING_BTN = (By.XPATH, "//button[normalize-space()='Skip']")
    SYNAPSE_PER_CONNECTION_NRECORDS = (By.CSS_SELECTOR, "a[data-testid='dataset-experimental_synapses_per_connection'] span[class='mr-2 font-light']")
    TOTAL_COUNT_DENSITY = (By.XPATH, "//h2[@data-testid='total-count-or-density']")
    TOTAL_COUNT_N = (By.XPATH, "//small[@class='text-base font-normal text-gray-300']")
    TOTAL_COUNT_SWITCH = (By.XPATH, "//button[@type='button' and @role='switch' and "
                                    "@title='density or count' and @aria-checked='false']")

    NEURON_MORPHOLOGY = (By.XPATH, "//div[normalize-space()='Morphology']")
    NEURON_ELECTROPHYSIOLOGY = (By.XPATH, "//div[normalize-space()='Single cell electrophysiology']")
    NOTEBOOKS_BTN = (By.CSS_SELECTOR, "#workspace-notebooks")
    BOUTON_DENSITY = (By.XPATH, "//div[normalize-space()='Bouton density']")
    SYNAPSE_PER_CONNECTION = (By.XPATH, "//div[normalize-space()='Synapse per connection']")
    NEURON_DENSITY = (By.XPATH, "//div[normalize-space()='Neuron density']")
    ION_CHANNEL_EPHYS = (By.XPATH, "//div[normalize-space()='Ion channel electrophysiology']")
    WORKFLOWS_HOME_BTN = (By.CSS_SELECTOR, "#workspace-workflows")


