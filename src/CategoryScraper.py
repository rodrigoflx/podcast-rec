import requests
from bs4 import BeautifulSoup
import csv
import logging
import re

class CategoryScraper:
    """ Tool for fetching link to categories of podcasts available in the Itunes
    Podcast Website
    """

    def __init__(self):
        self.session = requests.Session()
        
        s.mount("http://", HTTPAdapter(max_retries=1))
        s.mount("https://", HTTPAdapter(max_retries=1))

        
    ITUNES_URL = 'https://podcasts.apple.com/us/genre/podcasts/id26'
    API = "https://itunes.apple.com/lookup?id=%s"
    REGEX_ID = r"id(\d+)"

    def scrape(self):
        # Fetch response and initiate parser
        logging.info(f"Fetching HTML content from {self.ITUNES_URL}")

        try:
            response = self.session.get(self.ITUNES_URL)
        # Retried once, no luck
        except requests.exceptions.Timeout as e:
            logging.error(f"Timed out on {self.ITUNES_URL} after one retry")
            raise SystemExit(e)
        # Bad URL, aborting
        except requests.exceptions.TooManyRedirects as e:
            logging.error(f"Too many redirects for {self.ITUNES_URL}, probably a bad link")
            raise SystemExit(e)
        # Catastrophical failure, bailing
        except requests.exceptions.RequestException as e:
            logging.error(f"Too many logging errors")
            raise SystemExit(e)

        soup = BeautifulSoup(response.content, 'lxml')
        
        # Open file write-only
        logging.info("Opening 'genre_links.csv' to dump scraping contents")

        try:
            with open('genre_links.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Podcast Name', 'Podcast Category', 'Podcast URL', 'ID']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                # Open category link up and scraping podcasts
                for category in soup.find_all('a', {'class': 'top-level-genre'}):
                    podcast_category = category.text.strip()
                    category_url = category['href']

                    # Fetch category website
                    try:
                        category_response = requests.get(category_url)
                        category_response.raise_for_status()  # raise an HTTPError if the HTTP request returned an unsuccessful status code
                        soup_category = BeautifulSoup(category_response.content, 'lxml')
                    except requests.RequestException as req_err:
                        logging.error(f"Error fetching URL {category_url}: {req_err}")
                        continue  # Skip this category and move on to the next one

                    logging.info(f"Scraping genre {podcast_category}")
                    
                    # Fetch individual podcasts per category    
                    for podcast in soup_category.select('div.column ul li a'):
                        podcast_url = podcast["href"]
                        podcast_name = podcast.text.strip()

                        # Try to match id from each podcast link
                        # Example: https://podcasts.apple.com/us/podcast/podcast-name/idyyy
                        # Extracted: xxx
                        match = re.search(self.REGEX_ID, podcast_url)
                        if match:
                            podcast_id = match.group(1)
                        else:
                            logging.error(f"Failed to extract podcast ID from URL {podcast_url}")
                            continue  # Skip this podcast and move on to the next one

                        logging.info(f"Writing - Name {podcast_name} : URL {podcast_url} : ID {podcast_id}")
                        
                        # Writing to CSV file
                        try:
                            writer.writerow({
                                'Podcast Name': podcast_name,
                                'Podcast Category': podcast_category,
                                'Podcast URL': podcast_url,
                                'ID': podcast_id
                            })
                        except csv.Error as csv_err:
                            logging.error(f"Error writing to CSV: {csv_err}")

        # Error handling for IO
        except IOError as io_err:
            logging.error(f"File I/O error: {io_err}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

        logging.info("Scraping of Podcast IDs is done")
