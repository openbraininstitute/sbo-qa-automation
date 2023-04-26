from selenium.webdriver.common.by import By


class ExplorePageLocators:
    EXPLORE_URL = (By.XPATH, "//a[@href='/mmb-beta/explore']")
    EXPLORE_TITLE = (By.XPATH, "//h1[text()='Explore']")
    BRAIN_CELL_ANNOTATIONS = (By.XPATH, "//h1[text()='Brain & cells annotations']")
    BRAIN_CELL_ANNOTATIONS_URL = (By.XPATH,  "//a[@href='/mmb-beta/simulation-campaigns']")
    EXPERIMENTAL_DATA = (By.CLASS_NAME, "explore_experimental__zNDmh")
    DIGITAL_RECONSTRUCTION = (By.XPATH, "//h1[text()='Digital reconstructions']")
    SIMULATIONS = (By.XPATH, "//h1[text()='Simulations']")
