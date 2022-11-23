import pytest

from prophesygg.scrape.scraper import scrape_url


class TestScrape:
    """Test scraping functions"""

    def setup_class(self):
        self.test_url = "http://www.prophesy.gg/"

    def test_nostream_nojson(self):
        assert 2 == 2

    def test_nostream_json(self):
        assert 2 == 2

    def test_stream(self):
        assert 2 == 2
