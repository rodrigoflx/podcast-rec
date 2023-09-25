import csv
import logging
import json
import requests

class ItunesScraper():
    ITUNES_API = "https://itunes.apple.com/lookup?id=%s"


    def scrape(self, readpath, writepath):
        """Iterate through links CSV file and place
        an API call to Itunes to get the RSS feed links
        """
        
        
        logging.info(f"Opening CSV files - Read {readpath}, Write {writepath}")
        with open(readpath, 'r') as infile, open(writepath, 'w') as outfile:
            # Setup reader and writer
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames + ['rss']
            rows = list(reader)

            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            index = 0
            for row in rows:
                if index == 20:
                    break
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
                index = index + 1
            writer.writerows(rows)
if __name__ == '__main__':
    scraper = ItunesScraper()
    scraper.scrape('genre_links.csv', 'podcasts.csv')

