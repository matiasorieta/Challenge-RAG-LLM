from dotenv import load_dotenv
import os

load_dotenv()


COHERE_API_KEY = os.getenv('COHERE_API_KEY')
metadata_cohere_options = {
  "hnsw:space": "ip"
}
