from selenium.webdriver.common.by import By


class ExploreInteractiveLocators:
    SEARCH_FIELD = (By.XPATH, "//span[@class='ant-select-selection-search']")
    SEARCH_FIELD_ACTIVE = (By.XPATH, "//input[@aria-controls='rc_select_1_list']")
    SHADOW_HOST = (By.XPATH, "//input[@class='ant-select-selection-search-input']")
    SHADOW_ROOT = (By.XPATH, "//div[@id='text-field-container']")
    VIEWPORT = (By.XPATH, "editing-view-port")
    BASIC_CELL_GROUPS = (By.XPATH, "//span[@title='Basic Cell Groups and Regions']")
    BRAIN_STEM = (By.XPATH, "//span[@title='Brain Stem']")
    CEREBELLUM = (By.XPATH, "//span[@title='Cerebellum']")
    CEREBRUM = (By.XPATH, "//span[@title='Cerebrum']")
    EXPERIMENTAL_DATA_TAB = (By.XPATH, "//div[@role='tab' and text()='Experimental data']")
    LITERATURE_TAB = (By.XPATH, "//div[@role='tab' and text()='Literature']")
    MODEL_DATA_TAB = (By.XPATH, "//div[@role='tab' and text()='Model data']")
    MORPHOLOGY_LINK = (By.XPATH, "//span[@class='font-light' and text()='Morphology']")
    ELECTROPHYSIOLOGY_LINK = (By.XPATH, "//span[@class='font-light' and text()='Electrophysiology']")
    BOUTON_DENSITY_LINK = (By.XPATH, "//span[@class='font-light' and text()='Bouton density']")
    NEURON_DENSITY_LINK = (By.XPATH, "//span[@class='font-light' and text()='Neuron density']")
    SYNAPSE_PER_CONNECTION_LINK = (By.XPATH, "//span[@class='font-light' and text()='Synapse per "
                                             "connection']")

    ISOCORTEX_OPTION = (By.XPATH, "//div[@class='ant-select-item-option-content' and text("
                                  ")='Isocortex']")

    IMAGE_3D = (By.XPATH, "//canvas[@data-engine='three.js r152']")