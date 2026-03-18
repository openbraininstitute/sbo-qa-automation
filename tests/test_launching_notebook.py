# Test for launching notebook workflow using Page Object Model
# Following the proper pattern: locators -> page methods -> test calls

import pytest
import time
from pages.project_notebooks import ProjectNotebooks


class TestLaunchingNotebook:
    """Test for launching notebook workflow using proper Page Object Model pattern."""

    @pytest.mark.project_page
    def test_launching_notebook(self, login_direct_complete, logger, test_config):
        """Test notebook Readme, Download and Run functionality in a single session."""
        browser, wait, base_url, lab_id, project_id = login_direct_complete
        project_notebooks = ProjectNotebooks(browser, wait, logger, base_url)

        logger.info(f"Navigating to notebooks page for lab {lab_id}, project {project_id}")
        project_notebooks.go_to_project_notebooks_page(lab_id, project_id)

        table_container = project_notebooks.table_container()
        assert table_container.is_displayed(), "Notebooks table is not displayed"
        logger.info("Notebooks table loaded successfully")

        logger.info("Testing Readme functionality")
        project_notebooks.open_notebook_actions_menu(1)

        readme_button = project_notebooks.action_menu_readme()
        assert readme_button.is_displayed(), "Readme action is not displayed"
        readme_button.click()
        logger.info("Readme action clicked")

        try:
            time.sleep(1)
            modal_close = project_notebooks.modal_close_button()
            if modal_close.is_displayed():
                modal_close.click()
                logger.info("Modal closed")
        except:
            logger.info("No modal to close")

        logger.info("Readme test passed")

        logger.info("Testing Download functionality")
        time.sleep(2)
        project_notebooks.open_notebook_actions_menu(1)

        download_button = project_notebooks.action_menu_download()
        assert download_button.is_displayed(), "Download action is not displayed"
        download_button.click()
        logger.info("Download action clicked")

        try:
            time.sleep(1)
            modal_close = project_notebooks.modal_close_button()
            if modal_close.is_displayed():
                modal_close.click()
                logger.info("Modal closed")
        except:
            logger.info("No modal to close")

        logger.info("Download test passed")

        logger.info("Testing Run functionality")
        time.sleep(2)
        project_notebooks.open_notebook_actions_menu(1)

        run_button = project_notebooks.action_menu_run()
        assert run_button.is_displayed(), "Run action is not displayed"
        project_notebooks.js_click(run_button)
        logger.info("Run action clicked")

        jupyter_url = project_notebooks.wait_for_jupyter_tab(timeout=30)
        assert "jupyter" in jupyter_url.lower() or "lab" in jupyter_url.lower(), \
            f"Expected Jupyter notebook URL, got: {jupyter_url}"
        logger.info("Jupyter notebook tab opened successfully")

        notebook_loaded = project_notebooks.verify_jupyter_notebook_loaded(timeout=120)
        assert notebook_loaded, "Jupyter notebook did not load in the second tab"
        logger.info("Jupyter notebook loaded and verified")

        assert "notebooks" in browser.current_url, "Should be on notebooks page"
        logger.info("Notebook Readme, Download and Run test completed successfully")
