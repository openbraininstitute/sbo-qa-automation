# # Copyright (c) 2024 Blue Brain Project/EPFL
# #
# # SPDX-License-Identifier: Apache-2.0
# import os
# from selenium.common import NoSuchElementException
# from pages.sandbox_page import SandboxPage
# import pytest
# import time
#
# # Skip module if `SKIP_TESTS` environment variable is set
# if os.getenv("SKIP_TESTS") == "1":
#     pytest.skip("Skipping Morphology tests temporarily.", allow_module_level=True)
#
#
# @pytest.mark.usefixtures("setup", "logger", "login")
# class TestSandbox:
#     # @pytest.mark.run(order=1)
#     # @pytest.mark.skip(reason="Sorting not implemented yet.")
#     # def test_sorting_functionality(self):
#     #     # Placeholder logic for a test
#     #     assert False
#
#     def test_sandbox(self, setup, logger):
#         """Test the login process"""
#         browser, wait = setup
#         try:
#             sandbox_page = SandboxPage(browser, wait)
#             assert "sandbox/home" in browser.current_url, (f"Expected 'sandbox/home' in URL, but "
#                                                            f"got: {browser.current_url}")
#
#             logger.info("Navigated to the Sandbox Page")
#
#             sandbox_title = sandbox_page.find_sandbox_banner_title()
#             title = sandbox_title.text
#             assert title == "Welcome to Blue Brain Open Platform"
#
#             create_vlab = sandbox_page.find_create_vlab_btn().click()
#             logger.info("Create your Virtual Lab button is clicked.")
#             form_modal = sandbox_page.find_form_modal()
#             assert form_modal is not None, "Modal is not found."
#             assert form_modal.is_displayed(), "Modal is not displayed."
#
#             vl_name = sandbox_page.find_vl_name_field()
#             vl_name.send_keys()
#
#         except NoSuchElementException:
#             print(f"An error occurred:")
#             raise
