# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import json


class LinkLoader:
    @staticmethod
    def load_links(file_path):
        with open(file_path, 'r') as f:
            links = json.load(f)
        return links


