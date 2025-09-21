# src/rag_system/embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List
from config import Config
import logging

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    def __init__(self):
        """Initialize embedding model"""
        try:
            self.model = SentenceTransformer(Config.EMBEDDING_MODEL)
            logger.info(f"Loaded embedding model: {Config.EMBEDDING_MODEL}")
        except Exception as e:
            logger.error(f"Error loading embedding model: {e}")
            raise
    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts"""
        try:
            embeddings = self.model.encode(texts, 
                                         convert_to_numpy=True,
                                         show_progress_bar=True)
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    def generate_single_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for a single text"""
        return self.model.encode([text])[0]
    