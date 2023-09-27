import requests
from bs4 import BeautifulSoup
import csv
import logging
import re

class CategoryScraper:
    """ Tool for fetching link to categories of podcasts available in the Itunes
    Podcast Website
    """

    ITUNES_URL = 'https://podcasts.apple.com/us/genre/podcasts/id26'
    API = "https://itunes.apple.com/lookup?id=%s"
    REGEX_ID = r"id(\d+)"

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
                category_url = category['href']

                # Fetch genre page 
                category_response = requests.get(category_url)
                soup_category = BeautifulSoup(category_response.content, 'lxml')
                
                # Scrap links for the given genre
                logging.info(f"Scraping genre {podcast_category}")
                for podcast in soup_category.select('div.column ul li a'):
                    podcast_url = podcast["href"]
                    podcast_name = podcast.text.strip()

                    print(podcast_url)

                    podcast_id = re.search(self.REGEX_ID, podcast_url).group(1)

                    logging.info(f"Writing - Name {podcast_name} : URL {podcast_url} : ID {podcast_id}")
                    writer.writerow({
                        'Podcast Name' : podcast_name, 
                        'Podcast Category' : podcast_category,
                        'Podcast URL' : podcast_url,
                        'ID' : podcast_id
                        })
                    
        logging.info("Scraping of Podcast IDs is done")
