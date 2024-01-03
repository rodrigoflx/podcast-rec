import logging
import requests

from redis import Redis
from bs4 import BeautifulSoup
from rq import Queue, Worker

from Episode import Episode
from Downloader import Downloader

logging.basicConfig(level=logging.INFO)

class RSSScraper():
    def scrape_rss(get_response) -> None:
        """ 
        Scrape the RSS feed given by the 'url' parameter and dump the podcasts onto a
        list with the podcasts name ('parameter') attached to it

        :param get_response: Key-value collection of a given Itunes GET Response, guaranteed to have a 'feedUrl' field
        """
        logging.info(f"Scrapping RSS Feed given by : {get_response['feedUrl']}")
        # Create a Session
        session = requests.Session()

        # Create an adapter with the specified number of retries
        adapter = requests.adapters.HTTPAdapter(max_retries=3)

        # Mount the adapter for both HTTP and HTTPS
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        q = Queue('downloader_queue', connection=Redis(host='redis'))

        # List of all podcasts found in the RSS feed
        url = get_response['feedUrl']
        itunesId = get_response['collectionId']

        try:
            response = session.get(url, timeout=10)  # Setting a timeout can be useful
            response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
            logging.info(f"Fetching HTTP content from : {url}")

            try:
                soup = BeautifulSoup(response.content, 'lxml-xml')
            except Exception as e:
                logging.error(f"Error parsing the content from {url}: {e}")
                return

            if not soup.find("rss"):
                logging.error("Given URL doesn't point to a RSS feed")
                return

            # Each item corresponds to one episode of the podcast
            for item in soup.find_all('item'):

                enclosure = item.find('enclosure')

                title = item.find('title')

                if enclosure and title:
                    title = title.get_text(strip=True)
                    logging.info(f"Parsing episode \"{title}\"")
                    episode = Episode(title, itunesId, enclosure.get('url', ''))
                    q.enqueue(Downloader.download_data , episode)
                else:
                    logging.info(f"No enclosure found for {title if title else 'unknown item'}")

        except requests.Timeout:
            logging.error(f"Timeout occurred while fetching {url}")
        except requests.RequestException as e:
            logging.error(f"Error occurred while fetching {url}: {e}")

if __name__ == "__main__":
    redis_conn = Redis(host='redis')
    worker = Worker('rss_queue', connection=redis_conn)
    worker.work()
