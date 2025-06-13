# # Copyright (c) 2024 Blue Brain Project/EPFL
# # Copyright (c) 2025 Open Brain Institute
# # SPDX-License-Identifier: Apache-2.0
#
# from selenium.common import TimeoutException
# from pages.explore_page import ExplorePage
#
#
# class ExploreMeModel(ExplorePage):
#     def __init__(self, browser, wait, base_url, logger=None):
#         super().__init__(browser, wait, base_url)
#         self.home_page = ExplorePage(browser, wait, base_url)
#         self.logger = logger
#
#     def go_to_explore_memodel_page(self, lab_id: str, project_id: str):
#         path = f"/app/virtual-lab/lab/{lab_id}/project/{project_id}/explore/interactive/model/me-model"
#         try:
#             self.browser.set_page_load_timeout(90)
#             self.go_to_page(path)
#             self.wait_for_page_ready(timeout=60)
#         except TimeoutException:
#             raise RuntimeError("The ME-Model data page did not load within 60 seconds.")
#         return self.browser.current_url
