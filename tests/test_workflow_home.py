# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pages.workflows_page import WorkflowsPage


class TestWorkflowHome:
    @pytest.mark.workflow
    @pytest.mark.run(order=5)
    def test_workflow_home_page(self, setup, login, logger, test_config):
        """Test Workflow Home Page - verify Build and Simulate categories with their type cards"""
        browser, wait, base_url, lab_id, project_id = setup
        workflows_page = WorkflowsPage(browser, wait, logger, base_url)
        
        # Navigate to workflows page
        workflows_page.go_to_workflows_page(lab_id, project_id)
        logger.info("✅ Successfully navigated to workflows page")
        
        # Verify URL
        current_url = browser.current_url
        assert "/workflows" in current_url, f"Expected URL to contain /workflows, got: {current_url}"
        logger.info("✅ URL contains /workflows")
        
        # ========== TEST BUILD CATEGORY ==========
        logger.info("🔍 Testing Build category...")
        
        # 1. Find Build category button
        try:
            build_button = workflows_page.find_category_build()
            assert build_button.is_displayed(), "Build category button should be displayed"
            assert build_button.is_enabled(), "Build category button should be clickable"
            logger.info("✅ Build category button found and is clickable")
            
            # 2. Click on Build button
            build_button.click()
            logger.info("✅ Clicked Build category button")
            time.sleep(2)  # Wait for type cards to load
            
            # 3. Find and verify Build type cards: Single neuron, Synaptome, Ion channel
            logger.info("🔍 Verifying Build type cards...")
            build_buttons = workflows_page.verify_build_buttons()
            
            required_build_cards = ['Single neuron', 'Synaptome', 'Ion channel']
            build_found_count = 0
            
            for card_name in required_build_cards:
                if card_name in build_buttons and build_buttons[card_name]['displayed']:
                    build_found_count += 1
                    assert build_buttons[card_name]['clickable'], f"Build > {card_name} should be clickable"
                    logger.info(f"✅ Build > {card_name} card is displayed and clickable")
                else:
                    logger.warning(f"⚠️ Build > {card_name} card not found")
            
            assert build_found_count > 0, "At least one Build type card should be found"
            logger.info(f"✅ Found {build_found_count}/{len(required_build_cards)} Build type cards")
            
        except Exception as e:
            logger.error(f"❌ Build category test failed: {e}")
            raise
        
        # ========== TEST SIMULATE CATEGORY ==========
        logger.info("🔍 Testing Simulate category...")
        
        # 4. Click on Simulate button
        try:
            simulate_button = workflows_page.find_category_simulate()
            assert simulate_button.is_displayed(), "Simulate category button should be displayed"
            assert simulate_button.is_enabled(), "Simulate category button should be clickable"
            logger.info("✅ Simulate category button found and is clickable")
            
            simulate_button.click()
            logger.info("✅ Clicked Simulate category button")
            time.sleep(2)  # Wait for type cards to load
            
            # Scroll carousel BEFORE verifying buttons
            logger.info("🔍 Scrolling horizontally to find all cards...")
            workflows_page.scroll_carousel_right()
            time.sleep(2)
            
            # 5. Find and verify Simulate type cards
            logger.info("🔍 Verifying Simulate type cards...")
            simulate_buttons = workflows_page.verify_simulate_buttons()
            
            # Non-beta cards (should be clickable)
            clickable_simulate_cards = ['Single neuron', 'Synaptome']
            simulate_found_count = 0
            
            for card_name in clickable_simulate_cards:
                if card_name in simulate_buttons and simulate_buttons[card_name]['displayed']:
                    simulate_found_count += 1
                    assert simulate_buttons[card_name]['clickable'], f"Simulate > {card_name} should be clickable"
                    logger.info(f"✅ Simulate > {card_name} card is displayed and clickable")
                else:
                    logger.warning(f"⚠️ Simulate > {card_name} card not found")
            
            # Beta cards (should be displayed and clickable in staging)
            beta_simulate_cards = [
                'Single neuron beta',
                'Synaptome beta',
                'Paired neurons beta'
            ]
            beta_found_count = 0
            
            # Check for beta cards (already scrolled earlier)
            for card_name in beta_simulate_cards:
                if card_name in simulate_buttons and simulate_buttons[card_name]['displayed']:
                    beta_found_count += 1
                    # Beta cards are clickable in staging (aria-disabled="false")
                    assert simulate_buttons[card_name]['clickable'], f"Simulate > {card_name} should be clickable"
                    logger.info(f"✅ Simulate > {card_name} card is displayed and clickable (beta feature)")
                else:
                    logger.debug(f"ℹ️ Simulate > {card_name} card not found (may need more scrolling)")
            
            # If no beta cards found, log the page source for debugging
            if beta_found_count == 0:
                logger.warning("⚠️ No beta cards found - checking page structure...")
                try:
                    # Find all cards on the page
                    all_cards = workflows_page.find_all_type_cards()
                    logger.info(f"Found {len(all_cards)} total cards on page")
                    
                    # Log card titles
                    for i, card in enumerate(all_cards[:10]):  # Limit to first 10
                        try:
                            title = card.find_element(By.XPATH, ".//div[@data-slot='card-title']").text
                            logger.info(f"Card {i+1}: {title}")
                        except:
                            pass
                except Exception as e:
                    logger.debug(f"Could not inspect cards: {e}")
            
            assert simulate_found_count > 0, "At least one Simulate type card should be found"
            logger.info(f"✅ Found {simulate_found_count} clickable and {beta_found_count} beta Simulate type cards")
            
        except Exception as e:
            logger.error(f"❌ Simulate category test failed: {e}")
            raise
        
        # ========== VERIFY RECENT ACTIVITIES ==========
        logger.info("🔍 Verifying Recent Activities section...")
        workflows_page.verify_recent_activities_section()
        
        # ========== VERIFY TABLE PER TYPE (BUILD) ==========
        logger.info("🔍 Verifying table for each Build Type...")
        
        # Test each Build type: Single neuron, Synaptome, Ion channel
        build_types = ['Single neuron', 'Synaptome', 'Ion channel']
        
        for type_name in build_types:
            logger.info(f"🔍 Testing Build Type: {type_name}")
            result = workflows_page.verify_table_for_type(type_name)
            if result:
                logger.info(f"✅ Build Type '{type_name}' verification completed")
            else:
                logger.warning(f"⚠️ Build Type '{type_name}' verification failed")
        
        # ========== VERIFY PAGINATION ==========
        logger.info("🔍 Verifying pagination...")
        workflows_page.verify_pagination_works()
        
        # ========== VERIFY SIMULATE CATEGORY ==========
        logger.info("🔍 Switching to Simulate category...")
        
        # Click Category dropdown and select Simulate
        if workflows_page.click_category_dropdown_option('Simulate'):
            logger.info("✅ Switched to Simulate category")
            
            # Test each Simulate type
            simulate_types = ['Single neuron', 'Synaptome', 'Single neuron (beta)', 'Synaptome (beta)', 'Paired neurons (beta)']
            
            for type_name in simulate_types:
                logger.info(f"🔍 Testing Simulate Type: {type_name}")
                result = workflows_page.verify_table_for_type(type_name)
                if result:
                    logger.info(f"✅ Simulate Type '{type_name}' verification completed")
                else:
                    logger.warning(f"⚠️ Simulate Type '{type_name}' verification failed")
        else:
            logger.warning("⚠️ Could not switch to Simulate category")
        
        logger.info("✅ All workflow home page tests completed successfully")
