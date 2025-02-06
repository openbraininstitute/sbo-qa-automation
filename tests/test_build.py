# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import uuid

from pages.build import Build
from pages.vl_overview import VLOverview
import pytest

class TestBuild:
    def test_build(self, setup, login, logger):

        browser, wait, base_url = setup
        build = Build(browser,wait, base_url)
        """
        Dynamic lab and project IDs
        """
        lab_id = "37a3a2e8-a4b4-456b-8aff-4e23e87a5cbc"
        project_id = "8abcb1e3-b714-4267-a22c-3b3dc4be5306"
        current_url = build.go_to_build(lab_id, project_id)

        # Assert that the correct lab and project are in the URL
        assert lab_id in current_url and project_id in current_url, \
            f"Navigation failed. Expected IDs {lab_id} and {project_id} not found in {current_url}"



        # time.sleep(200)