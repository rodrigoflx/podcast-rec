import csv
import logging
import json
import requests

class ItunesScraper():
    
    ITUNES_API = "https://itunes.apple.com/lookup?id=%s"

    def __init__(self, readpath, max_retries=3):
        # Define paths and create session
        self.readpath = readpath
        self.session = requests.Session()

        # Define adapter so as to fix the amount of retries
        adapter = requests.adapters.HTTPAdapter(max_retries=max_retries)

        # Associate adapter to session
        self.session.mount('http://', adapter)
        self.session.mount('https://;', adapter)

    def scrape(self , writepath):
        """Iterate through links CSV file and place
        an API call to Itunes to get the RSS feed links
        """
        
        
        logging.info(f"Opening CSV files - Read {self.readpath}, Write {writepath}")
        with open(self.readpath, 'r') as infile, open(writepath, 'w') as outfile:
            # Setup reader and writer
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames + ['rss']
            rows = list(reader)

            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                # Substitute string for saved ID and send query
                active_url = self.ITUNES_API % row['ID']
                
                logging.info(f"Requesting {active_url}")
                response = requests.get(active_url)
                
                # Data is returned in JSON acordding to 
                # https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/index.html
                data = json.loads(response.text)
                results = data['results'][0]
                
                if 'feedUrl' in results:
                    row['rss'] = results['feedUrl']
                else:
                    row['rss'] = ''

            writer.writerows(rows)
