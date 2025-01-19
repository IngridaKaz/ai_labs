import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-3.5-turbo"
EMBEDDING_MODEL = "text-embedding-3-small"

# ChromaDB Configuration
CHROMA_PERSIST_DIR = "chroma_persistent_storage"
COLLECTION_NAME = "help-center-articles"

# Document Processing Configuration
CHUNK_SIZE = 500
CHUNK_OVERLAP = 0
BATCH_SIZE = 20

# Data Paths
DATA_DIR = Path("data")
HC_ARTICLES_PATH = DATA_DIR / "cleaned_hc_articles.json"
