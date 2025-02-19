import pytest
from util.util_links_handler import LinkHandler  # Adjust import if necessary


# @pytest.mark.usefixtures("setup")
# class TestAllLinks:
#     def test_all_links(self, setup):
#         """Crawls and tests links for all pages in the platform."""
#         browser, wait, base_url = setup
#         link_tester = LinkTester(browser)
#
#         # Define all pages to test (add more if needed)
#         pages = [
#             "/home",
#             "/about",
#             "/contact",
#             "/services",
#             "/blog",
#             "/virtual-lab/lab/c162b0b2-62a2-4776-96d7-d469df196abd",
#             "/virtual-lab/lab/c162b0b2-62a2-4776-96d7-d469df196abd/project/88a7a13c-7fbf-4bd5-be2d-5af9fda7a0eb/home",
#             "/virtual-lab/lab/c162b0b2-62a2-4776-96d7-d469df196abd/project/88a7a13c-7fbf-4bd5-be2d-5af9fda7a0eb/home/explore",
#             "/virtual-lab/lab/c162b0b2-62a2-4776-96d7-d469df196abd/project/88a7a13c-7fbf-4bd5-be2d-5af9fda7a0eb/home/explore_morphology",
#         ]
#         for page in pages:
#             url = f"{base_url}{page}"
#             link_tester.test_links_on_page(url)