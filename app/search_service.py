"""
Azure AI Search service wrapper
Handles all document indexing and searching operations
"""

from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchFieldDataType
)
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import ResourceNotFoundError
from typing import List, Dict
from datetime import datetime
from app.config import Config
from app.logger import logger


class AzureSearchService:
    """Azure AI Search service manager"""

    def __init__(self):
        """Initialize search clients"""

        self.endpoint = Config.AZURE_SEARCH_ENDPOINT
        self.api_key = Config.AZURE_SEARCH_API_KEY
        self.index_name = Config.AZURE_SEARCH_INDEX_NAME

        # Initialize clients
        self.index_client = SearchIndexClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.api_key)
        )

        self.search_client = SearchClient(
            endpoint=self.endpoint,
            index_name=self.index_name,
            credential=AzureKeyCredential(self.api_key)
        )

        logger.info("Azure Search service initialized")

    def create_index(self) -> bool:
        """
        Create or update the search index
        Defines the schema for document storage
        """

        try:
            fields = [
                SimpleField(
                    name="id",
                    type=SearchFieldDataType.String,
                    key=True,
                    filterable=True
                ),
                SearchableField(
                    name="content",
                    type=SearchFieldDataType.String,
                    searchable=True,
                    analyzer_name="en.microsoft"
                ),
                SimpleField(
                    name="source",
                    type=SearchFieldDataType.String,
                    filterable=True,
                    facetable=True
                ),
                SimpleField(
                    name="chunk_id",
                    type=SearchFieldDataType.Int32,
                    filterable=True
                ),
                SimpleField(
                    name="upload_date",
                    type=SearchFieldDataType.DateTimeOffset,
                    filterable=True,
                    sortable=True
                ),
                SimpleField(
                    name="file_type",
                    type=SearchFieldDataType.String,
                    filterable=True,
                    facetable=True
                )
            ]

            index = SearchIndex(
                name=self.index_name,
                fields=fields
            )

            result = self.index_client.create_or_update_index(index)
            logger.info(f"Index '{self.index_name}' created/updated successfully")
            return True

        except Exception as e:
            logger.error(f"Error creating index: {e}")
            raise

    def index_exists(self) -> bool:
        """Check if index exists"""
        try:
            self.index_client.get_index(self.index_name)
            return True
        except ResourceNotFoundError:
            return False
        except Exception as e:
            logger.error(f"Error checking index existence: {e}")
            return False

    def upload_documents(self, documents: List[Dict]) -> int:
        """
        Upload multiple documents to the index
        Returns number of successfully uploaded documents
        """

        try:
            from datetime import datetime, timezone
            # Add metadata
            for doc in documents:
                if 'upload_date' not in doc:
                    doc['upload_date'] = datetime.now(timezone.utc).isoformat()  # ✅ This was fixed

            result = self.search_client.upload_documents(documents=documents)

            success_count = sum(1 for r in result if r.succeeded)
            logger.info(f"Uploaded {success_count}/{len(documents)} documents")

            return success_count

        except Exception as e:
            logger.error(f"Error uploading documents: {e}")
            raise

    def search(self, query: str, top: int = None) -> List[Dict]:
        """
        Search for relevant documents
        Returns list of matching documents with scores
        """

        if top is None:
            top = Config.SEARCH_TOP_K

        try:
            logger.debug(f"Searching for: '{query}' (top {top})")

            results = self.search_client.search(
                search_text=query,
                top=top,
                select=["content", "source", "chunk_id", "file_type"],
                include_total_count=True
            )

            documents = []
            for result in results:
                documents.append({
                    'content': result['content'],
                    'source': result['source'],
                    'chunk_id': result.get('chunk_id', 0),
                    'file_type': result.get('file_type', 'unknown'),
                    'score': result.get('@search.score', 0)
                })

            logger.info(f"Found {len(documents)} relevant documents")
            return documents

        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            raise

    def delete_document(self, doc_id: str) -> bool:
        """Delete a document from the index"""
        try:
            self.search_client.delete_documents(documents=[{"id": doc_id}])
            logger.info(f"Deleted document: {doc_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting document {doc_id}: {e}")
            return False

    def get_document_count(self) -> int:
        """Get total number of documents in index"""
        try:
            results = self.search_client.search(search_text="*", include_total_count=True)
            return results.get_count()
        except Exception as e:
            logger.error(f"Error getting document count: {e}")
            return 0