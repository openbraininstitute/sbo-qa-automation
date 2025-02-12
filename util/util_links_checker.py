# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import json
import requests

from util.util_load_links import LinkLoader


class LinkChecker:
    def __init__(self):
        self.valid_status_codes = range(200, 500)

    def check_link_status(self, link):
        response = requests.head(link)
        status_code = response.status_code
        if status_code == 200:
            return True
        else:
            print(f"Broken link found (Status Code {status_code}: {link} ")
            return False

    def check_links(self, links_to_check):
        for link in links_to_check:
            is_valid = self.check_link_status(link)
            if is_valid:
                print(f"Link is valid: {link}")
            else:
                print(f"Broken link found: {link}")

    @staticmethod
    def load_links(file_path):
        return LinkLoader.load_links(file_path)
