import csv
import logging
import json
from redis import Redis
import requests
import time

from rq import Queue 
from RSSScraper import RSSScraper

SEC_PER_REQ = 3.15

logging.basicConfig(level=logging.INFO)

class ItunesScraper():
    ITUNES_API = "https://itunes.apple.com/lookup?id=%s"

    def scrape_itunes(readpath) -> None:
        """Iterate through links CSV file and place
        an API call to Itunes to get the RSS feed links

        :param readpath: Filepath to CSV file with all Itunes ID informations
        """
        # Create a session
        session = requests.Session()

        # Create an adapter with the specified number of retries
        adapter = requests.adapters.HTTPAdapter(max_retries=3)

        # Mount the adapter for both HTTP and HTTPS
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        # Initialize Redis Queue
        q = Queue('rss_queue', connection=Redis(host='redis'))
         
        logging.info(f"Opening CSV files - Read {readpath}")
        try:
            with open(readpath, 'r') as infile:
                # Setup reader and writer
                reader = csv.DictReader(infile)
                
                # Try to read from file
                try:
                    rows = list(reader)
                except csv.Error as csv_read_err:
                    logging.error(f"Error reading CSV: {csv_read_err}")
                    return 

                for row in rows:
                    active_url = ItunesScraper.ITUNES_API % row['ID']

                    
                    # Make a GET request to the Itunes API
                    # Try to extract the feed URL from it
                    try:
                        logging.info(f"Requesting {active_url}")
                    
                        start_time = time.time()
                        
                        response = requests.get(active_url)
                        response.raise_for_status()  # Check response status
                        data = json.loads(response.text)
                        results = data['results'][0]
                        
                        if 'feedUrl' in results:
                        # Submit job to Queue with the given response
                            q.enqueue(RSSScraper.scrape_rss, results)

                        # Measure endtime
                        end_time = time.time()

                        sleep_time = max(0, SEC_PER_REQ - (end_time - start_time))

                        # Sleep if rate limit has been reached
                        if (sleep_time != 0):
                            time.sleep(sleep_time)

                    except requests.RequestException as req_err:
                        logging.error(f"HTTP request error for URL {active_url}: {req_err}")
                    except json.JSONDecodeError as json_err:
                        logging.error(f"Error decoding JSON for URL {active_url}: {json_err}")
                    except (KeyError, IndexError) as data_err:
                        logging.error(f"Error accessing data for URL {active_url}: {data_err}")
                
        except IOError as io_err:
            logging.error(f"File I/O error: {io_err}")
        except Exception as unexpected_err:
            logging.error(f"Unexpected error: {unexpected_err}")

if __name__ == "__main__":
    ItunesScraper.scrape_itunes('genre_links.csv')