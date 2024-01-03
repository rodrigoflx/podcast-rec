from io import BytesIO
from redis import Connection, Redis
from rq import Queue, Worker
import numpy as np

import whisper
import Episode
import psycopg2
import logging

logging.basicConfig(level=logging.INFO)

db_params = {
    'dbname': 'database',
    'user': 'username',
    'password': 'mysecretpassword',
    'host': 'localhost'
}   

def transcribe_and_write(episode : Episode, content : BytesIO) -> None:
    # Load model
    model = whisper.load_model("base")

    logging.info(f"Transcribing {episode.title}")

    audio_bytes = content.read()
    audio_np = np.frombuffer(audio_bytes, dtype=np.int16)

    # Transcribe
    result = model.transcribe(audio_np)

    # Save to DB
    save_to_db(episode, result['text'])

def save_to_db(episode : Episode, text : str) -> None:
    conn = psycopg2.connect(db_params)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO podcasts (podcast_id, title, mp3_url, transcript) VALUES (%s, %s, %s, %s)",
        (*episode.unpack(), text)
    )
    
    conn.commit()
    cursor.close()
    conn.close()

    logging.info(f"Saved {episode.title} together with text to DB")


if __name__ == "__main__":
    redis_conn = Redis(host='redis')
    worker = Worker('transcriber_queue', connection=redis_conn)
    worker.work()
