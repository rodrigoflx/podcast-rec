import csv
import logging
import json
import requests

class ItunesScraper():
    
    ITUNES_API = "https://itunes.apple.com/lookup?id=%s"

    def __init__(self, readpath : str, max_retries : int =3):
        """
        Constructor for ItunesScrapper class.

        Attributes:
        -----------
        readpath : str
            Filepath to file containing podcasts IDs.
        """

        # Define paths and create session
        self.readpath = readpath
        self.session = requests.Session()

        # Define adapter so as to fix the amount of retries
        adapter = requests.adapters.HTTPAdapter(max_retries=max_retries)

        # Associate adapter to session
        self.session.mount('http://', adapter)
        self.session.mount('https://;', adapter)

    def scrape(self : ItunesScraper , writepath : str) -> None:
        """Iterate through links CSV file and place
        an API call to Itunes to get the RSS feed links

        :param writepath: Filepath to CSV file with all podcast informations.
        """
        
        
        logging.info(f"Opening CSV files - Read {self.readpath}, Write {writepath}")
        
        try:
            with open(self.readpath, 'r') as infile, open(writepath, 'w') as outfile:
                # Setup reader and writer
                reader = csv.DictReader(infile)
                fieldnames = reader.fieldnames + ['rss']
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                
                # Try to read from file
                try:
                    rows = list(reader)
                except csv.Error as csv_read_err:
                    logging.error(f"Error reading CSV: {csv_read_err}")
                    return 

                for row in rows:
                    active_url = self.ITUNES_API % row['ID']
                    
                    # Make a GET request to the Itunes API
                    # Try to extract the feed URL from it
                    try:
                        logging.info(f"Requesting {active_url}")
                        response = requests.get(active_url)
                        response.raise_for_status()  # Check response status
                        data = json.loads(response.text)
                        results = data['results'][0]
                        
                        if 'feedUrl' in results:
                            row['rss'] = results['feedUrl']
                        else:
                            row['rss'] = ''
                    except requests.RequestException as req_err:
                        logging.error(f"HTTP request error for URL {active_url}: {req_err}")
                    except json.JSONDecodeError as json_err:
                        logging.error(f"Error decoding JSON for URL {active_url}: {json_err}")
                    except (KeyError, IndexError) as data_err:
                        logging.error(f"Error accessing data for URL {active_url}: {data_err}")

                # Write the result to the CSV file
                try:
                    writer.writerows(rows)
                except csv.Error as csv_write_err:
                    logging.error(f"Error writing to CSV: {csv_write_err}")
                
        except IOError as io_err:
            logging.error(f"File I/O error: {io_err}")
        except Exception as unexpected_err:
            logging.error(f"Unexpected error: {unexpected_err}")
