# Test for launching notebook workflow using Page Object Model
# Following the proper pattern: locators -> page methods -> test calls

import pytest
import time
from pages.project_notebooks import ProjectNotebooks


class TestLaunchingNotebook:
    """Test for launching notebook workflow using proper Page Object Model pattern."""

    @pytest.mark.project_page
    def test_launching_notebook_readme(self, login_direct_complete, logger, test_config):
        """Test notebook readme functionality."""
        browser, wait, base_url, lab_id, project_id = login_direct_complete
        project_notebooks = ProjectNotebooks(browser, wait, logger, base_url)
        
        # Navigate to notebooks page
        logger.info(f"Navigating to notebooks page for lab {lab_id}, project {project_id}")
        project_notebooks.go_to_project_notebooks_page(lab_id, project_id)
        
        # Wait for table to load
        table_container = project_notebooks.table_container()
        assert table_container.is_displayed(), "Notebooks table is not displayed"
        logger.info("Notebooks table loaded successfully")
        
        # Test Readme functionality
        logger.info("Testing Readme functionality")
        
        # Click first notebook action button
        notebook_button = project_notebooks.notebook_actions_button_1()
        assert notebook_button.is_displayed(), "Notebook action button 1 is not displayed"
        logger.info("Notebook action button 1 found")
        
        notebook_button.click()
        logger.info("Notebook action button 1 clicked")
        
        # Wait for menu to appear and click readme
        time.sleep(2)  # Wait for menu animation
        readme_button = project_notebooks.action_menu_readme()
        assert readme_button.is_displayed(), "Readme action is not displayed"
        logger.info("Readme action found")
        
        readme_button.click()
        logger.info("Readme action clicked")
        
        # Try to close modal if it appears
        try:
            time.sleep(1)
            modal_close = project_notebooks.modal_close_button()
            if modal_close.is_displayed():
                modal_close.click()
                logger.info("Modal closed")
        except:
            logger.info("No modal to close")
        
        # Verify we're still on notebooks page
        assert "notebooks" in browser.current_url, "Should be on notebooks page"
        logger.info("✅ Notebook readme test completed successfully")

    @pytest.mark.project_page  
    def test_launching_notebook_download(self, login_direct_complete, logger, test_config):
        """Test notebook download functionality."""
        browser, wait, base_url, lab_id, project_id = login_direct_complete
        project_notebooks = ProjectNotebooks(browser, wait, logger, base_url)
        
        # Navigate to notebooks page
        project_notebooks.go_to_project_notebooks_page(lab_id, project_id)
        table_container = project_notebooks.table_container()
        assert table_container.is_displayed(), "Notebooks table is not displayed"
        logger.info("Notebooks table loaded successfully")
        
        # Test Download functionality
        logger.info("Testing Download functionality")
        
        # Click first notebook action button
        notebook_button = project_notebooks.notebook_actions_button_1()
        notebook_button.click()
        logger.info("Notebook action button 1 clicked")
        
        # Wait for menu and click download
        time.sleep(2)
        download_button = project_notebooks.action_menu_download()
        assert download_button.is_displayed(), "Download action is not displayed"
        logger.info("Download action found")
        
        download_button.click()
        logger.info("Download action clicked")
        
        # Try to close modal if it appears
        try:
            time.sleep(1)
            modal_close = project_notebooks.modal_close_button()
            if modal_close.is_displayed():
                modal_close.click()
                logger.info("Modal closed")
        except:
            logger.info("No modal to close")
        
        assert "notebooks" in browser.current_url, "Should be on notebooks page"
        logger.info("✅ Notebook download test completed successfully")

    @pytest.mark.project_page
    def test_launching_notebook_run(self, login_direct_complete, logger, test_config):
        """Test notebook run functionality."""
        browser, wait, base_url, lab_id, project_id = login_direct_complete
        project_notebooks = ProjectNotebooks(browser, wait, logger, base_url)
        
        # Navigate to notebooks page
        project_notebooks.go_to_project_notebooks_page(lab_id, project_id)
        table_container = project_notebooks.table_container()
        assert table_container.is_displayed(), "Notebooks table is not displayed"
        logger.info("Notebooks table loaded successfully")
        
        # Test Run functionality
        logger.info("Testing Run functionality")
        
        # Click first notebook action button
        notebook_button = project_notebooks.notebook_actions_button_1()
        notebook_button.click()
        logger.info("Notebook action button 1 clicked")
        
        # Wait for menu and click run
        time.sleep(2)
        run_button = project_notebooks.action_menu_run()
        assert run_button.is_displayed(), "Run action is not displayed"
        logger.info("Run action found")
        
        run_button.click()
        logger.info("Run action clicked")
        
        assert "notebooks" in browser.current_url, "Should be on notebooks page"
        logger.info("✅ Notebook run test completed successfully")
