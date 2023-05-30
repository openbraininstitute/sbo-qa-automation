import time
import uuid

import pytest
from selenium.webdriver import ActionChains, Keys
from selenium import webdriver
from pages.build_page import BuildPage
from util.util_base import load_config


class TestBuild:
    @pytest.mark.build_page
    def test_build_page(self, setup, login_explore, logger):
        browser, wait = setup
        build_page = BuildPage(browser, wait)
        build_url = build_page.go_to_build_page()
        # assert build_url == 'https://bbp.epfl.ch/mmb-beta/build/load-brain-config'

        # Find "titles on the Build Page"
        recent_config = build_page.find_recent_configurations()
        assert recent_config.text == "Recently used configurations"
        logger.info("Build page main titles are displayed, such as Recent recently used configurations")

        # Check the Release version
        verify_release_version = build_page.verify_release_version()
        assert verify_release_version.text == "Release 23.01"
        logger.info("Build page release version is displayed")

        # Find the default public config and click on it
        # plus_icon_open_default_config = build_page.select_default_config().click()
        # logger.info("Accessing default public config link via plus icon")

        # Find the search field and enter 'Custom model configuration' as a search param
        find_search_textfield = build_page.find_config_search_field()
        find_search_textfield.send_keys("Custom model configuration")

        # Use public config
        use_public_config = build_page.use_custom_config()

        # Clone the public config
        clone_public_config = build_page.clone_custom_config().click()
        logger.info("'Clone' button is clicked")

        # Find the name input field in the modal
        find_default_config_name = build_page.find_default_config_name()

        # Clear any existing value in the name input field
        while find_default_config_name.get_property('value'):
            find_default_config_name.send_keys(Keys.BACKSPACE)
        if not find_default_config_name.get_attribute('value'):
            generate_config_name = "Config_" + str(uuid.uuid4())
            find_default_config_name.click()

        #
        # if not find_default_config_name.get_attribute('value'):
        #     generate_config_name = "Config_" + str(uuid.uuid4())
        #     find_default_config_name.click()
        #
        # find_default_config_name.send_keys(generate_config_name)
        # browser.execute_script("arguments[0].dispatchEvent(new Event('input'))", find_default_config_name)
        # browser.execute_script("arguments[0].dispatchEvent(new Event('change'))", find_default_config_name)

        # if not find_default_config_name.get_attribute('value'):
        #     generate_config_name = "Config_" + str(uuid.uuid4())
        #     find_default_config_name.click()

        find_default_config_name.send_keys(generate_config_name)
        # browser.execute_script("arguments[0].dispatchEvent(new Event('input'))", find_default_config_name)
        # browser.execute_script("arguments[0].dispatchEvent(new Event('change'))", find_default_config_name)


        # Find the description input field in the modal
        find_default_description = build_page.clear_default_description_name()

        # Clear any existing value in the description input field
        while find_default_description.get_property('value'):
            find_default_description.send_keys(Keys.BACKSPACE)

        # Generate a unique configuration description
        generate_config_description = "Description_" + str(uuid.uuid4())
        #
        # # Enter the generated configuration description in the input field
        find_default_description.send_keys(generate_config_description)
        find_default_description.send_keys(Keys.SPACE)


        # time.sleep(30)
        # clear_default_description = build_page.clear_default_description_name()
        # while clear_default_description.get_property('value'):
        #     clear_default_description.send_keys(Keys.BACKSPACE)
        #     time.sleep(2)
        # generate_config_description = "Description_" + str(uuid.uuid4())
        # set_description_name = build_page.set_config_description().send_keys(generate_config_description)



        # Click Start editing button

        start_editing = build_page.push_start_editing()

        # Execute JavaScript code to enable the "Start editing" button
        # browser.execute_script("arguments[0].removeAttribute('disabled');", start_editing)

        # Click the "Start editing" button
        if start_editing.is_enabled():
            start_editing.click()

        else:
            print("The button to edit the config is disabled")
        # start_editing.click()
        time.sleep(15)
        # Get the current URL and assert that it matches the expected URL
        current_url = browser.current_url
        assert "https://bbp.epfl.ch/mmb-beta/build/cell-composition" in current_url

        # Get the current URL and assert that it matches the expected URL

        # start_editing = build_page.push_start_editing()
        # max_wait_time = 10
        # # Perform custom wait loop until element is visible and clickable or timeout occurs
        # start_time = time.time()
        # while time.time() - start_time < max_wait_time:
        #     try:
        #         element = wait.until(start_editing)
        #         wait.until(element_clickable)
        #         break  # Exit the loop if element is both visible and clickable
        #     except:
        #         time.sleep(1)  # Delay for 1 second before the next check
        # start_editing.click()
        # time.sleep(3)
        #
        #
        #
        # # Get the current URL and assert that it matches the expected URL

        # current_url = browser.current_url
        # assert "https://bbp.epfl.ch/mmb-beta/build/cell-composition" in current_url
        #

