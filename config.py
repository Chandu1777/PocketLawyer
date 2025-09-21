# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys (free tier)
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '')
    
    # Model Configuration
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # Free, lightweight
    LLM_MODEL = "microsoft/DialoGPT-medium"  # Free alternative
    
    # ChromaDB Configuration
    CHROMA_DB_PATH = "./data/embeddings/chroma_db"
    COLLECTION_NAME = "indian_legal_docs"
    
    # Document Processing
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    MAX_TOKENS = 512
    
    # Data Sources (Free Government Sites)
    LEGAL_SOURCES = {
        'constitution': 'https://www.india.gov.in/my-government/constitution-india',
        'supreme_court': 'https://main.sci.gov.in/',
        'legislative': 'https://sansad.in/',
        'law_commission': 'https://lawcommissionofindia.nic.in/'
    }
    
    # Security Settings
    ENABLE_LOGGING = True
    LOG_PERSONAL_DATA = False  # Never log personal information
    SESSION_TIMEOUT = 30  # minutes
    
    # Update Frequency
    AUTO_UPDATE_FREQUENCY = 7  # days
    
    # File Upload Limits
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.txt']
    
    # Directories
    RAW_DATA_DIR = "./data/raw"
    PROCESSED_DATA_DIR = "./data/processed"
    EMBEDDINGS_DIR = "./data/embeddings"
    UPLOAD_DIR = "./temp_uploads"
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories"""
        directories = [
            cls.RAW_DATA_DIR,
            cls.PROCESSED_DATA_DIR,
            cls.EMBEDDINGS_DIR,
            cls.UPLOAD_DIR
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    @classmethod
    def is_development(cls):
        return os.getenv('ENVIRONMENT', 'development') == 'development'