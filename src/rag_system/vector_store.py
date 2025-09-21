# src/rag_system/vector_store.py
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
import uuid
from config import Config
import logging

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        """Initialize ChromaDB vector store"""
        try:
            # Create ChromaDB client (persistent)
            self.client = chromadb.PersistentClient(
                path=Config.CHROMA_DB_PATH,
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=Config.COLLECTION_NAME,
                metadata={"description": "Indian Legal Documents"}
            )
            
            logger.info(f"ChromaDB initialized with collection: {Config.COLLECTION_NAME}")
            
        except Exception as e:
            logger.error(f"Error initializing vector store: {e}")
            raise
    
    def add_documents(self, 
                     texts: List[str], 
                     metadatas: List[Dict[str, Any]], 
                     embeddings: List[List[float]] = None):
        """Add documents to vector store"""
        try:
            # Generate IDs
            ids = [str(uuid.uuid4()) for _ in texts]
            
            if embeddings:
                self.collection.add(
                    documents=texts,
                    metadatas=metadatas,
                    embeddings=embeddings,
                    ids=ids
                )
            else:
                self.collection.add(
                    documents=texts,
                    metadatas=metadatas,
                    ids=ids
                )
            
            logger.info(f"Added {len(texts)} documents to vector store")
            
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            raise
    
    def similarity_search(self, 
                         query: str, 
                         n_results: int = 5,
                         where: Dict[str, Any] = None) -> Dict[str, Any]:
        """Search for similar documents"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where
            )
            return results
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            raise
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection"""
        try:
            count = self.collection.count()
            return {
                "name": Config.COLLECTION_NAME,
                "document_count": count
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {"name": Config.COLLECTION_NAME, "document_count": 0}
        