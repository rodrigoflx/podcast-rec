from bs4 import BeautifulSoup
import requests
import logging
from Episode import Episode


class RSSSCraper:

    def __init__(self, max_retries=3):
        self.session = requests.Session()

        # Create an adapter with the specified number of retries
        adapter = requests.adapters.HTTPAdapter(max_retries=max_retries)

        # Mount the adapter for both HTTP and HTTPS
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        
    def scrape_url(self, url, podcast):
        podcasts = []
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'lxml-xml')

            i = 0

            # Each item corresponds to one episode of the podcast
            for item in soup.find_all('item'):
                if i == 5:
                    break
                enclosure = item.find('enclosure')
                if enclosure:
                    episode = Episode(item.title, item.guid, podcast, enclosure['url'])
                    podcasts.append(episode)
                else:
                    logging.info(f"No enclosure found for {item.title}")
                i = i + 1 
               
            return podcasts
        except:
            logging.error(f" Connection on {url} failed")
            return None
        finally:
            response.close()

    def download_podcast(self, filename, url):
        response = requests.get(url, stream=True)

        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
               
        response.close() 
               
if __name__ == '__main__':
    scraper = RSSSCraper()
    podcasts = scraper.scrape_url('https://feeds.simplecast.com/p7Q9jZ0K', 'Audio Poem of the Day')
    
    for podcast in podcasts:
        print(podcast.medialink)
