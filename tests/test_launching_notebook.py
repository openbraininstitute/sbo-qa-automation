# Auto-generated test code - REFACTORED to use Page Object Model
# Generated: 2026-01-14T14:39:53.473269
# Test: launching_notebook
# NOTE: This test was auto-generated and then manually refactored to use
# the existing Page Object Model structure (locators + pages + tests)

import pytest
from pages.project_notebooks import ProjectNotebooks


class TestLaunchingNotebook:
    """Test for launching notebook workflow"""

    def test_launching_notebook(self, login_direct_complete, logger, test_config):
        """Test notebook launching workflow using Page Object Model."""
        browser, wait, base_url, lab_id, project_id = login_direct_complete
        
        # Initialize page object
        notebooks_page = ProjectNotebooks(browser, wait, logger, base_url)
        
        # Navigate to notebooks page
        logger.info(f"Navigating to notebooks page for lab {lab_id}, project {project_id}")
        notebooks_page.go_to_project_notebooks_page(lab_id, project_id)
        
        # TODO: Add your test actions here based on what you recorded
        # The recorder captured these actions (refactor as needed):
        # 1. Click filter button
        # 2. Interact with filter options
        # 3. Click on notebook items
        # 4. Click run button
        # 5. Navigate to credits
        
        # Example: Click filter button (using existing locator)
        logger.info("Clicking filter button")
        filter_btn = notebooks_page.page_filter()
        filter_btn.click()
        
        # Add more actions here based on your workflow
        # Use the existing page object methods and locators
        
        # Add assertions
        assert "notebooks" in browser.current_url, "Should be on notebooks page"
        logger.info("✅ Notebook page loaded successfully")
