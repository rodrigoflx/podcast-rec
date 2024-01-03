from io import BytesIO
from redis import Redis
import requests
import logging

from rq import Queue, Worker
import Episode
from Transcriber import transcribe_and_write

logging.basicConfig(level=logging.INFO)

class Downloader():
    def download_data(episode  : Episode):

        # Initiate session
        session = requests.Session()

        # Setup Redis Queue
        q = Queue('transcriber_queue', connection=Redis(host='redis'))

        # Create an adapter with the specified number of retries
        adapter = requests.adapters.HTTPAdapter(max_retries=3)

        # Mount the adapter for both HTTP and HTTPS
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        with requests.get(episode.medialink, stream=True) as response:
            logging.info(f"Downloading mp3 file from : {episode.medialink}")

            response.raise_for_status()
            content = BytesIO()

            # Load chunks into the IO Stream
            for chunk in response.iter_content(chunk_size=8192):
                content.write(chunk)
            content.seek(0)  # Reset the stream's position

        logging.info(f"Enqueueing episode with transcript : {episode.title}")
        q.enqueue(transcribe_and_write, episode, content)

if __name__ == "__main__":
    redis_conn = Redis(host='redis')
    worker = Worker('downloader_queue', connection=redis_conn)
    worker.work()
