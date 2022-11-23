import json

from cloudscraper import create_scraper
from prophesygg.storage import PROPHESY_STORAGE_CLIENT, GCSObjectStreamUpload


def scrape_url(url, stream=False):
    """Scrape a URL, return a response. If using stream == True, "data" key in output is a response object.

    Args:
        url (string): The URL to scrape
        stream (bool, optional): If one wants to stream the response. Defaults to False.

    Returns:
        dict: Returns a dictionary with the result in the "data" key.
    """
    scraper = create_scraper()
    resp = scraper.get(url, stream=stream)
    return resp
