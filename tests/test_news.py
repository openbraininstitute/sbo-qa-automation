# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from pages.news_page import NewsPage


class TestNews:
    def test_news(self, visit_public_pages, logger):
        _visit, base_url = visit_public_pages
        browser, wait = _visit("/news")
        news_page = NewsPage(browser, wait, base_url, logger=logger)

        main_hero_video = news_page.main_hero_video(timeout=10)
        assert main_hero_video.is_displayed(), "Main page video is not found."
        logger.info("Main page video is displayed.")

        main_page_image = news_page.hero_img()
        assert main_page_image.is_displayed(), "Main page image is not found."
        logger.info("Main page image is displayed.")

        main_page_title = news_page.main_title()
        assert main_page_title.is_displayed(), "Main page title is not found."
        logger.info("Main page title is displayed.")

        main_page_text = news_page.main_page_text()
        assert main_page_text.is_displayed(),"Main page text is not found."
        logger.info("Main page text is displayed.")

        initial_cards = news_page.page_cards()
        assert len(initial_cards) == 10, "There should be exactly 10 cards on the page initially."

        # Verify that all initial cards have required elements
        for i, card in enumerate(initial_cards):
            try:
                title = news_page.cards_main_titles()[i]
                assert title.is_displayed(), f"Card {i + 1} does not have a visible title."

                text = news_page.cards_text()[i]
                assert text.is_displayed(), f"Card {i + 1} does not have a visible text paragraph."

                img = news_page.cards_img()[i]
                assert img.is_displayed(), f"Card {i + 1} does not have a visible image."

                read_more_btn = news_page.cards_read_more_btn()[i]
                assert read_more_btn.is_displayed(), f"Card {i + 1} does not have a visible 'Read more' button."

                logger.info(f"Card {i + 1} has all required elements.")

            except AssertionError as e:
                logger.error(f"Assertion failed for card {i + 1}: {str(e)}")
                raise  # Reraise the error to ensure the test fails if any card is missing required elements

        load_more_button = news_page.load_more_btn()
        browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", load_more_button)
        if load_more_button.is_displayed():
            browser.execute_script("arguments[0].click();", load_more_button)
            time.sleep(2)  # This might need to be replaced with WebDriverWait

            updated_cards = news_page.page_cards()
            assert len(updated_cards) > len(
                initial_cards), "The number of cards did not increase after clicking 'Load more'."

            for i, card in enumerate(updated_cards[len(initial_cards):]):
                try:
                    title = news_page.cards_main_titles()[len(initial_cards) + i]
                    assert title.is_displayed(), f"Card {len(initial_cards) + i + 1} does not have a visible title."

                    text = news_page.cards_text()[len(initial_cards) + i]
                    assert text.is_displayed(), f"Card {len(initial_cards) + i + 1} does not have a visible text paragraph."

                    img = news_page.cards_img()[len(initial_cards) + i]
                    assert img.is_displayed(), f"Card {len(initial_cards) + i + 1} does not have a visible image."

                    read_more_btn = news_page.cards_read_more_btn()[len(initial_cards) + i]
                    assert read_more_btn.is_displayed(), f"Card {len(initial_cards) + i + 1} does not have a visible 'Read more' button."

                    logger.info(f"Card {len(initial_cards) + i + 1} has all required elements.")

                except AssertionError as e:
                    logger.error(f"Assertion failed for card {len(initial_cards) + i + 1}: {str(e)}")
                    raise  # Reraise the error to ensure the test fails if any card is missing required elements

        logger.info("All cards (initial and newly loaded) have required elements.")


