from typing import Any

import chromadb
from chromadb.utils import embedding_functions

from ai_labs.src.config import CHROMA_PERSIST_DIR, COLLECTION_NAME, EMBEDDING_MODEL, OPENAI_API_KEY


class ChromaDBClient:
    def __init__(self) -> None:
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=OPENAI_API_KEY, model_name=EMBEDDING_MODEL
        )

        self.client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME, embedding_function=self.embedding_function
        )

    def add_documents(
        self, ids: list[str], documents: list[str], metadatas: list[dict[str, str]] | None = None
    ) -> None:
        """Add documents to the collection in batch."""
        self.collection.upsert(ids=ids, documents=documents, metadatas=metadatas)

    def query(self, question: str, n_results: int = 3) -> dict[str, Any]:
        """Query the collection for relevant documents."""
        return self.collection.query(
            query_texts=[question], n_results=n_results, include=["documents", "metadatas", "distances"]
        )
