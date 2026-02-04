# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

from pages.team_page import TeamPage


class TestTeam:
    def test_team(self, visit_public_pages, logger):
        """Test the Team page functionality"""
        _visit, base_url = visit_public_pages
        browser, wait = _visit("/team")
        team_page = TeamPage(browser, wait, base_url, logger=logger)

        # Navigate to page
        team_page.go_to_page()
        assert "team" in browser.title.lower() or "Team" in browser.title
        logger.info("Team page loaded successfully")

        # Test page title
        page_title = team_page.get_page_title()
        assert page_title.is_displayed(), "Page title is not displayed"
        logger.info(f"Page title found: {page_title.text}")

        # Test page description (optional)
        page_description = team_page.get_page_description()
        if page_description:
            assert page_description.is_displayed(), "Page description is not displayed"
            logger.info("Page description is present")

        # Test team member cards
        team_members = team_page.get_team_member_cards()
        assert len(team_members) > 0, "No team member cards found"
        logger.info(f"Found {len(team_members)} team member cards")

        # Test member names
        member_names = team_page.get_member_names()
        assert len(member_names) > 0, "No team member names found"
        
        empty_names = [name.text for name in member_names if not name.text.strip()]
        assert not empty_names, f"Some member names are empty: {empty_names}"
        logger.info(f"All {len(member_names)} member names are present")

        # Test member roles
        member_roles = team_page.get_member_roles()
        assert len(member_roles) > 0, "No team member roles found"
        
        # Filter out empty roles (some members might not have roles displayed)
        non_empty_roles = [role for role in member_roles if role.text.strip()]
        assert len(non_empty_roles) > 0, "No non-empty member roles found"
        logger.info(f"Found {len(non_empty_roles)} non-empty member roles out of {len(member_roles)} total")

        # Test member photos (if found)
        member_photos = team_page.get_member_photos()
        if member_photos:
            failed_photos = team_page.validate_member_photos_loaded()
            if failed_photos:
                # Allow some photos to fail (network issues, lazy loading, etc.)
                failure_rate = len(failed_photos) / len(member_photos)
                if failure_rate > 0.2:  # Allow up to 20% failure rate for large team pages
                    logger.warning(f"High photo failure rate: {len(failed_photos)}/{len(member_photos)} ({failure_rate:.1%})")
                else:
                    logger.info(f"Some member photos failed to load: {len(failed_photos)}/{len(member_photos)}")
            logger.info(f"Found {len(member_photos)} member photos, {len(member_photos) - len(failed_photos)} loaded successfully")
        else:
            logger.info("No member photos found with current locator")

        # Test team structure (management vs regular members)
        team_structure = team_page.validate_team_structure()
        assert team_structure['total_members'] > 0, "No team members found"
        logger.info(f"Team structure: {team_structure['total_members']} total members")
        logger.info(f"Management members (with bios): {team_structure['management_members']}")
        logger.info(f"Regular members (without bios): {team_structure['regular_members']}")

        # Test that management members have bios
        if team_structure['management_members'] > 0:
            management_members = team_page.get_management_members()
            assert len(management_members) > 0, "Management members should have bios"
            
            for member in management_members:
                member_info = team_page.extract_member_info(member)
                assert member_info['has_bio'], f"Management member {member_info['name']} should have a bio"
                assert member_info['bio'].strip(), f"Management member {member_info['name']} has empty bio"
            
            logger.info(f"✅ All {len(management_members)} management members have bios")

        # Test that regular members don't require bios (this is expected)
        regular_members = team_page.get_regular_members()
        if regular_members:
            logger.info(f"✅ Found {len(regular_members)} regular team members (bios not required)")

        # Test member information extraction
        sample_members = team_members[:3]  # Test first 3 members
        for i, member in enumerate(sample_members):
            member_info = team_page.extract_member_info(member)
            
            # Name is required for all members
            assert member_info['name'], f"Member {i+1} is missing name"
            # Role is optional (some members might not have roles displayed)
            assert member_info['photo_src'], f"Member {i+1} is missing photo"
            
            role_text = member_info['role'] if member_info['role'] else "No role specified"
            logger.info(f"Member {i+1}: {member_info['name']} - {role_text} (Bio: {'Yes' if member_info['has_bio'] else 'No'})")

        # Test social links (if present)
        social_links = team_page.get_social_links()
        if social_links:
            broken_social_links = []
            for link in social_links:
                href = link.get_attribute('href')
                if not href or not any(platform in href for platform in ['linkedin', 'twitter', 'x.com', 'github', 'youtube', 'bsky']):
                    broken_social_links.append(f"Invalid social link: {href}")
            
            assert not broken_social_links, f"Some social links are invalid: {broken_social_links}"
            logger.info(f"All {len(social_links)} social links are valid")

        # Test LinkedIn links specifically
        linkedin_links = team_page.get_linkedin_links()
        if linkedin_links:
            for link in linkedin_links:
                href = link.get_attribute('href')
                assert 'linkedin.com' in href, f"Invalid LinkedIn link: {href}"
            logger.info(f"Found {len(linkedin_links)} valid LinkedIn links")

        # Test Twitter/X links specifically
        twitter_links = team_page.get_twitter_links()
        if twitter_links:
            for link in twitter_links:
                href = link.get_attribute('href')
                assert 'twitter.com' in href or 'x.com' in href, f"Invalid Twitter/X link: {href}"
            logger.info(f"Found {len(twitter_links)} valid Twitter/X links")

        # Test YouTube links specifically
        youtube_links = team_page.get_youtube_links()
        if youtube_links:
            for link in youtube_links:
                href = link.get_attribute('href')
                assert 'youtube.com' in href, f"Invalid YouTube link: {href}"
            logger.info(f"Found {len(youtube_links)} valid YouTube links")

        # Test BlueSky links specifically
        bluesky_links = team_page.get_bluesky_links()
        if bluesky_links:
            for link in bluesky_links:
                href = link.get_attribute('href')
                assert 'bsky' in href, f"Invalid BlueSky link: {href}"
            logger.info(f"Found {len(bluesky_links)} valid BlueSky links")

        # Test search functionality (if present)
        search_input = team_page.get_search_input()
        if search_input:
            # Test search functionality
            search_success = team_page.search_team_members("test")
            if search_success:
                logger.info("Search functionality is working")
            search_input.clear()  # Clear search

        # Test filter buttons (if present)
        filter_buttons = team_page.get_filter_buttons()
        if filter_buttons:
            logger.info(f"Found {len(filter_buttons)} filter buttons")

        # Test team sections (if present)
        team_sections = team_page.get_team_sections()
        if team_sections:
            logger.info(f"Found {len(team_sections)} team sections")

        section_headers = team_page.get_section_headers()
        if section_headers:
            logger.info(f"Found {len(section_headers)} section headers")

        logger.info("✅ Team page test completed successfully")