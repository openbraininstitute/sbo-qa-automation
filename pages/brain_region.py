# from locators.build_page_locators import BuildPageLocators
# from selenium.webdriver.support import expected_conditions as EC
# from pages.base_page import CustomBasePage
# from pages.home_page import HomePage
#
#
# from util.util_methods import find_element, element_to_be_clickable
# from util.util_scraper import UrlScraper
#
#
# class BrainRegionPage(HomePage, CustomBasePage):
#     def __init__(self, browser, wait):
#         super().__init__(browser, wait)
#         self.login_page = HomePage(browser, wait)
#         self.url_scraper = UrlScraper()
#
#     def go_to_config_page(self):
#         # return self.browser.get(
#         #     "https://bbp.epfl.ch/mmb-beta/build/cell-composition/interactive?brainModelConfigId=8a962b3a-2005-4bc1-9b35-c20c2ec4cc54")
#         # "https://bbp.epfl.ch/mmb-beta/build/cell-composition/interactive?brainModelConfigId=526807b3-57d2-463a-9af4-f15c4450c677"
#         config_id = '31ac9203-50fe-4c68-9e68-fea7af40dc02'
#         config_url = f"https://bbp.epfl.ch/mmb-beta/build/cell-composition/interactive" \
#                      f"?brainModelConfigId={config_id}"
#
#         self.browser.get(config_url)
#         return config_url
#
#     def scrape_links(self):
#         page_source = self.browser.page_source
#         links = self.url_scraper.scrape_links(page_source)
#
#     def find_build_main_section(self):
#         return find_element(self.wait, BuildPageLocators.BRAIN_BUILD_SECTION_MAIN)
#
#     def open_build_div(self):
#         return find_element(self.wait, BuildPageLocators.BRAIN_BUILD_CLOSED_DIV)
#
#     def find_visible_basic_cells(self):
#         return find_element(self.wait, BuildPageLocators.VISIBLE_BASIC_CELL_GROUPS_TEXT)
#
#     def find_search_input(self):
#         return find_element(self.wait, BuildPageLocators.SEARCH_INPUT)
#
#     def find_search_value(self):
#         return find_element(self.wait, BuildPageLocators.SEARCH_VALUE)
#
#     def find_basic_cells_arrow_btn(self):
#         return element_to_be_clickable(self.wait, BuildPageLocators.BASIC_CELL_GROUPS_ARROW_BTN)
#
#     def find_brain_stem_arrow_btn(self):
#         return element_to_be_clickable(self.wait, BuildPageLocators.BRAIN_STEM_BTN)
#
#     def find_cerebrum_arrow_btn(self):
#         return element_to_be_clickable(self.wait, BuildPageLocators.CEREBRUM_ARROW_BTN)
#
#     def find_cerebral_cortex_arrow_btn(self):
#         return element_to_be_clickable(self.wait, BuildPageLocators.CEREBRAL_CORTEX_BTN)
#
#     def find_cortical_plate_arrow_btn(self):
#         return element_to_be_clickable(self.wait, BuildPageLocators.CORTICAL_PLATE_BTN)
#
#     def find_isocortex_arrow_btn(self):
#         return element_to_be_clickable(self.wait, BuildPageLocators.ISOCORTEX_BTN)
#
#     def find_agranular_ins_area_btn(self):
#         return element_to_be_clickable(self.wait, BuildPageLocators.AGRANULAR_INS_AREA_BTN)
#
#     def find_agranular_ins_area_dorsal_p_btn(self):
#         return element_to_be_clickable(self.wait, BuildPageLocators.AGRANULAR_INS_AREA_DORSAL_P_BTN)
#
#     def find_agranular_ins_area_dorsal_p_title(self):
#         return element_to_be_clickable(self.wait, BuildPageLocators.AGRANULAR_INS_AREA_DORSAL_P_TITLE)
#
#     def find_configuration_btn(self):
#         return self.wait.until(EC.element_to_be_clickable(BuildPageLocators.SUB_MENU_CONFIGURATION))
#
#     def find_second_sub_menu(self):
#         return find_element(self.wait, BuildPageLocators.SECOND_SUB_MENU)
#
#     def configuration_button(self):
#         return element_to_be_clickable(self.wait, BuildPageLocators.SUB_MENU_CONFIGURATION)
#
#     def find_top_nav_menu(self):
#         return find_element(self.wait, BuildPageLocators.TOP_NAV_MENU)
#
#     def find_cell_composition(self):
#         return find_element(self.wait, BuildPageLocators.CELL_COMPOSITION)
#
#     def find_cell_model_assignment(self):
#         return find_element(self.wait, BuildPageLocators.CELL_MODEL_ASSIGNMENT)
#
#     def find_connectome_definition(self):
#         return find_element(self.wait, BuildPageLocators.CONNECTOME_DEFINITION)
#
#     def find_connection_model_assignment(self):
#         return find_element(self.wait, BuildPageLocators.CONNECTION_MODEL_ASSIGNMENT)
#
#     def find_build_and_simulate_button(self):
#         return find_element(self.wait, BuildPageLocators.BUILD_AND_SIMULATE_BUTTON)
#
#     def find_interactive_btn(self):
#         return find_element(self.wait, BuildPageLocators.SUB_MENU_INTERACTIVE)
