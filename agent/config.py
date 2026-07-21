import os

from dotenv import load_dotenv
from netfree_unstrict_ssl import unstrict_ssl

load_dotenv()
unstrict_ssl()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")