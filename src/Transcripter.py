class Transcripter:
    def __init__(self):
        return

    def download_podcast(self, filename, url):
        response = requests.get(url, stream=True)

        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
               
