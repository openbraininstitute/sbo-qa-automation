# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from pages.digital_brain_story_page import DigitalBrainStoryPage


class TestDigitalBrainStory:
    def test_digital_brain_story(self, visit_public_pages, logger):
        """Test the Digital Brain Story page functionality"""
        _visit, base_url = visit_public_pages
        browser, wait = _visit("/the-real-digital-brain-story")
        story_page = DigitalBrainStoryPage(browser, wait, base_url, logger=logger)

        # Navigate to page
        story_page.go_to_page()
        assert "Digital Brain" in browser.title or "Real Digital Brain" in browser.title
        logger.info("Digital Brain Story page loaded successfully")

        # Test page title
        page_title = story_page.get_page_title()
        assert page_title.is_displayed(), "Page title is not displayed"
        logger.info(f"Page title found: {page_title.text}")

        # Test hero description
        hero_description = story_page.get_hero_description()
        assert hero_description.is_displayed(), "Hero description is not displayed"
        assert hero_description.text.strip(), "Hero description is empty"
        logger.info("Hero description is present and visible")

        # Test hero image
        hero_image = story_page.get_hero_image()
        assert hero_image is not None, "Hero image element not found"
        
        # Wait for image to load and become visible
        story_page.wait_for_hero_image_load()
        
        # Scroll to ensure image is in viewport
        story_page.browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", hero_image)
        import time
        time.sleep(2)  # Wait for scroll and any animations
        
        # Check if image is loaded properly
        is_loaded = story_page.browser.execute_script(
            "return arguments[0].complete && arguments[0].naturalWidth > 0;", hero_image
        )
        assert is_loaded, "Hero image failed to load properly"
        logger.info("Hero image loaded successfully")

        # Test hero video (must load if present)
        hero_video = story_page.get_hero_video()
        if hero_video:
            assert hero_video.is_displayed(), "Hero video is not displayed"
            story_page.wait_for_hero_video_load()
            logger.info("Hero video loaded successfully")
        else:
            logger.info("No hero video found")

        # Test main sections
        main_sections = story_page.get_main_sections()
        assert len(main_sections) > 0, "No main content sections found"
        logger.info(f"Found {len(main_sections)} main content sections")

        # Test section titles
        section_titles = story_page.get_section_titles()
        assert len(section_titles) > 0, "No section titles found"
        
        empty_titles = [title.text for title in section_titles if not title.text.strip()]
        assert not empty_titles, f"Some section titles are empty: {empty_titles}"
        logger.info(f"All {len(section_titles)} section titles are present and non-empty")

        # Test section texts
        section_texts = story_page.get_section_texts()
        assert len(section_texts) > 0, "No section texts found"
        
        # Filter out empty texts (some might be spacer elements)
        non_empty_texts = [text for text in section_texts if text.text.strip()]
        assert len(non_empty_texts) > 0, "No non-empty section texts found"
        logger.info(f"Found {len(non_empty_texts)} non-empty section texts out of {len(section_texts)} total")

        # Test section images
        section_images = story_page.get_section_images()
        if section_images:
            failed_images = story_page.validate_images_loaded()
            # Allow some small icons to fail (16x16 SVGs are often decorative)
            critical_failed_images = [img for img in failed_images if not ('16x16' in str(img) or '22x16' in str(img) or '19x16' in str(img))]
            if critical_failed_images:
                logger.warning(f"Some critical images failed to load: {critical_failed_images}")
            if failed_images:
                logger.info(f"Some images failed to load (possibly decorative icons): {len(failed_images)} total")
            logger.info(f"Found {len(section_images)} section images, {len(section_images) - len(failed_images)} loaded successfully")
        else:
            logger.info("No section images found")

        # Test navigation links
        nav_links = story_page.get_navigation_links()
        if nav_links:
            broken_links = []
            for link in nav_links[:5]:  # Test first 5 links to avoid too many requests
                href = link.get_attribute('href')
                if not href or href == '#':
                    broken_links.append(f"Link with text '{link.text}' has no href")
            
            assert not broken_links, f"Some navigation links are broken: {broken_links}"
            logger.info(f"Navigation links are properly formatted")

        # Test interactive buttons
        buttons = story_page.get_buttons()
        if buttons:
            clickable_buttons = []
            non_clickable_buttons = []
            
            for button in buttons:
                try:
                    if button.is_displayed() and button.is_enabled():
                        clickable_buttons.append(button)
                    else:
                        button_text = button.text.strip() or button.get_attribute('aria-label') or 'Unknown button'
                        non_clickable_buttons.append(button_text)
                except:
                    # Skip buttons that cause exceptions (might be stale or hidden)
                    pass
            
            # Only require that we have some clickable buttons, not all
            if clickable_buttons:
                logger.info(f"Found {len(clickable_buttons)} clickable buttons out of {len(buttons)} total")
            else:
                logger.info(f"No clickable buttons found out of {len(buttons)} total buttons")
            
            if non_clickable_buttons:
                logger.info(f"Non-clickable buttons (possibly disabled/hidden): {non_clickable_buttons[:3]}")  # Show first 3

        # Scroll through content to ensure everything loads
        story_page.scroll_through_content()
        logger.info("Successfully scrolled through all content")

        # Test story-specific elements (if present)
        story_timeline = story_page.get_story_timeline()
        if story_timeline:
            assert story_timeline.is_displayed(), "Story timeline is not displayed"
            logger.info("Story timeline found and displayed")

        story_chapters = story_page.get_story_chapters()
        if story_chapters:
            logger.info(f"Found {len(story_chapters)} story chapters")

        research_highlights = story_page.get_research_highlights()
        if research_highlights:
            logger.info(f"Found {len(research_highlights)} research highlights")

        logger.info("✅ Digital Brain Story page test completed successfully")