# src/rag_system/retriever.py
from typing import List, Dict, Any, Tuple
from .vector_store import VectorStore
from .embeddings import EmbeddingGenerator
import logging

logger = logging.getLogger(__name__)

class LegalRetriever:
    def __init__(self):
        """Initialize retriever with vector store"""
        self.vector_store = VectorStore()
        self.embedding_generator = EmbeddingGenerator()
    
    def retrieve_relevant_docs(self, 
                             query: str, 
                             n_docs: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant legal documents for a query"""
        try:
            # Search vector store
            results = self.vector_store.similarity_search(
                query=query,
                n_results=n_docs
            )
            
            # Format results
            relevant_docs = []
            if results['documents'][0]:  # Check if results exist
                for i, (doc, metadata, distance) in enumerate(zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                )):
                    relevant_docs.append({
                        'content': doc,
                        'metadata': metadata,
                        'similarity_score': 1 - distance,  # Convert distance to similarity
                        'rank': i + 1
                    })
            
            logger.info(f"Retrieved {len(relevant_docs)} relevant documents")
            return relevant_docs
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            return []
    
    def filter_by_legal_domain(self, 
                              query: str, 
                              legal_domain: str = None) -> List[Dict[str, Any]]:
        """Filter results by specific legal domain (constitutional, criminal, civil, etc.)"""
        try:
            where_filter = {}
            if legal_domain:
                where_filter["domain"] = legal_domain
            
            results = self.vector_store.similarity_search(
                query=query,
                n_results=10,
                where=where_filter if where_filter else None
            )
            
            # Format and return results
            relevant_docs = []
            if results['documents'][0]:
                for i, (doc, metadata, distance) in enumerate(zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                )):
                    relevant_docs.append({
                        'content': doc,
                        'metadata': metadata,
                        'similarity_score': 1 - distance,
                        'rank': i + 1
                    })
            
            return relevant_docs
            
        except Exception as e:
            logger.error(f"Error filtering by legal domain: {e}")
            return []