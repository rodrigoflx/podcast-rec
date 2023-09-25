import requests
from bs4 import BeautifulSoup
import csv
import logging


class CategoryScraper:
    """ Tool for fetching link to categories of podcasts available in the Itunes
    Podcast Website
    """

    ITUNES_URL = 'https://podcasts.apple.com/us/genre/podcasts/id26'
    API = "https://itunes.apple.com/lookup?id=%s"
    REGEX = 
   
    def scrape(self):
        # Fetch response and initiate parser
        logging.info(f"Fetching HTML content from {self.ITUNES_URL}")
        response = requests.get(self.ITUNES_URL)
        soup = BeautifulSoup(response.content, 'lxml')

        # Open file write-only
        logging.info("Opening 'genre_links.csv' to dump scraping contents")
        with open('genre_links.csv', 'w', newline='', encoding='utf-8') as csvfile:
            # Write header names as in fieldnames
            fieldnames = ['Podcast Name', 'Podcast Category', 'Podcast URL', 'ID']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # Loop through tags from retrieved HTML content
            for category in soup.find_all('a', {'class', 'top-level-genre'}):
                podcast_category = category.text.strip()
                category_url = Category['href']

                # Fetch podcast page 
                podcast_response = requests.get(category_url)
                soup_podcast = BeautifulSoup(podcast_response.content, 'lxml')
                
                logging.info("Scraping podcasts for each genre")
                
        logging.info("Done Scraping")

