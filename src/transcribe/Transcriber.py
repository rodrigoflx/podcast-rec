import whisper
import logging

class Transcriber:
    def __init__(self):
        # Loads the 'base' model from Whisper's library
        self.model = whisper.load_model("base")
    
    def transcribe_and_write(self, infile : str, outfile : str) -> None:
        try:
            with open(outfile, 'w') as out:
                result = self.model.transcribe(infile)
                out.write(result["text"])

            
        except IOError as e:
            logging.error(f"Couldn't open write-file {outfile}")
            raise SystemExit(e)
        except RuntimeError as e:
            logging.error(f"Whisper couldn't open read-file {infile}")
            raise SystemExit(e)
        except:
            logging.error(f"Unidentified error, shutting down...")
            raise SystemExit()

if __name__ == "__main__":
    transcriber = Transcriber()
    transcriber.transcribe_and_write("gold_standard.mp3", "gold_standard.txt")

