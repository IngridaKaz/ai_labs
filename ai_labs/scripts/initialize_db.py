import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from ai_labs.src.database.chroma_client import ChromaDBClient
from ai_labs.src.database.document_processor import DocumentProcessor
from ai_labs.src.utils.logger import setup_logger

logger = setup_logger(__name__)


def main() -> None:
    logger.info("Initializing database...")
    db_client = ChromaDBClient()
    processor = DocumentProcessor(db_client)

    logger.info("Processing and embedding articles...")
    processor.process_articles()
    logger.info("Database initialization complete!")


if __name__ == "__main__":
    main()
