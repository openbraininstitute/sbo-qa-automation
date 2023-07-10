from selenium.webdriver.common.by import By


class ExplorePageLocators:
    EXPLORE_URL = (By.XPATH, "//a[@href='/mmb-beta/explore']")
    EXPLORE_LINK1 = (By.XPATH, "//a[@href='/mmb-beta/explore/simulation-campaigns']//h1[text()='Brain & cells annotations']")
    EXPLORE_TITLE = (By.XPATH, "//h1[text()='Explore']")
    BRAIN_CELL_ANNOTATIONS = (By.XPATH, "//h1[text()='Brain & cells annotations']")
    BRAIN_CELL_ANNOTATIONS_URL = (By.XPATH,  "//a[@href='/mmb-beta/simulation-campaigns']")
    EXPERIMENTAL_DATA = (By.XPATH, "//h1[contains(text(), 'Experimental data')]")
    DIGITAL_RECONSTRUCTION = (By.XPATH, "//h1[text()='Brain models']")
    SIMULATIONS = (By.XPATH, "//h1[text()='Simulations']")
    NEURON_EPHYS = (By.XPATH, "//")