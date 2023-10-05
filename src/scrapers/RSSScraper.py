from bs4 import BeautifulSoup
import requests
import logging
from Episode import Episode


class RSSScraper:

    def __init__(self, max_retries : int =3):
        """
        Initializes the RSSScraper with the given amount of maximal retries for establishing a connection through HTTP

        :param max_retries: Number of retries for HTTP Connection
        """

        self.session = requests.Session()

        # Create an adapter with the specified number of retries
        adapter = requests.adapters.HTTPAdapter(max_retries=max_retries)

        # Mount the adapter for both HTTP and HTTPS
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        
    def scrape_rss(self, url : str, podcast : str) -> [Episode]:
        """ 
        Scrape the RSS feed given by the 'url' parameter and dump the podcasts onto a
        list with the podcasts name ('parameter') attached to it

        :param url: URL to RSS feed 
        :param podcast: Name of the podcast
        """
        podcasts = []
        try:
            response = session.get(url, timeout=10)  # Setting a timeout can be useful
            response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
   
            try:
                soup = BeautifulSoup(response.content, 'lxml-xml')
            except Exception as e:
                logging.error(f"Error parsing the content from {url}: {e}")
                return podcasts

            if not soup.find("rss"):
                logging.error("Given URL doesn't point to a RSS feed")
                return podcasts

            # Each item corresponds to one episode of the podcast
            for item in soup.find_all('item'):
                enclosure = item.find('enclosure')

                title = getattr(item, 'title', None)
                guid = getattr(item, 'guid', None)
                
                if enclosure and title and guid:
                    podcasts.append(Episode(title, guid, podcast, enclosure.get('url', '')))
                else:
                    logging.info(f"No enclosure found for {title if title else 'unknown item'}")

        except requests.Timeout:
            logging.error(f"Timeout occurred while fetching {url}")
        except requests.RequestException as e:
            logging.error(f"Error occurred while fetching {url}: {e}")

        return podcasts

    def download_podcast(self, filename, url):
        response = requests.get(url, stream=True)

        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

if __name__ == '__main__':
    scraper = RSSScraper()
    scraper.download_podcast("gold_standard.mp3", "https://traffic.megaphone.fm/RRTET6328440039.mp3?updated=1696474062")