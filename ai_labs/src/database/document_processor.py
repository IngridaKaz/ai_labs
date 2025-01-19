import json
from pathlib import Path

from ai_labs.src.config import BATCH_SIZE, HC_ARTICLES_PATH
from ai_labs.src.database.chroma_client import ChromaDBClient
from ai_labs.src.utils.logger import setup_logger
from ai_labs.src.utils.text_splitter import split_text

logger = setup_logger(__name__)


class DocumentProcessor:
    def __init__(self, db_client: ChromaDBClient) -> None:
        self.db_client = db_client

    def load_articles(self) -> list[dict]:
        """Load articles from JSON file."""
        with Path(HC_ARTICLES_PATH).open(encoding="utf-8") as file:
            return json.load(file)

    def process_articles(self) -> None:
        """Process and embed all articles."""
        articles = self.load_articles()
        logger.info(f"Loaded {len(articles)} articles")

        current_batch = {"ids": [], "documents": [], "metadatas": []}

        for idx, article in enumerate(articles):
            logger.info(f"Processing article {idx + 1}/{len(articles)}")
            doc_content = f"{article['title']}. {article['body']}"
            chunks = split_text(doc_content)

            for chunk_idx, chunk in enumerate(chunks):
                doc_id = f"{article['url']}_{chunk_idx}"
                current_batch["ids"].append(doc_id)
                current_batch["documents"].append(chunk)
                current_batch["metadatas"].append(
                    {"url": article["url"], "title": article["title"], "chunk_index": chunk_idx}
                )

                if len(current_batch["ids"]) >= BATCH_SIZE:
                    self.db_client.add_documents(
                        current_batch["ids"], current_batch["documents"], current_batch["metadatas"]
                    )
                    logger.info(f"Uploaded batch of {len(current_batch['ids'])} chunks")
                    current_batch = {"ids": [], "documents": [], "metadatas": []}

        # Upload remaining documents
        if current_batch["ids"]:
            self.db_client.add_documents(current_batch["ids"], current_batch["documents"], current_batch["metadatas"])
