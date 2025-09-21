# src/data_ingestion/document_processor.py
import os
import re
from typing import List, Dict, Any, Tuple
import PyPDF2
from docx import Document
import logging
from config import Config

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self):
        """Initialize document processor"""
        self.chunk_size = Config.CHUNK_SIZE
        self.chunk_overlap = Config.CHUNK_OVERLAP
    
    def process_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        """Process PDF document and extract text chunks"""
        try:
            chunks = []
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                full_text = ""
                for page_num, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    full_text += f"\n--- Page {page_num + 1} ---\n{text}"
                
                # Clean and chunk the text
                cleaned_text = self._clean_text(full_text)
                text_chunks = self._create_chunks(cleaned_text)
                
                # Create chunk objects with metadata
                for i, chunk in enumerate(text_chunks):
                    chunks.append({
                        'content': chunk,
                        'metadata': {
                            'source': os.path.basename(file_path),
                            'type': 'pdf',
                            'chunk_id': i,
                            'total_chunks': len(text_chunks),
                            'domain': self._identify_legal_domain(chunk)
                        }
                    })
            
            logger.info(f"Processed PDF: {file_path}, extracted {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {e}")
            return []
    
    def process_docx(self, file_path: str) -> List[Dict[str, Any]]:
        """Process DOCX document and extract text chunks"""
        try:
            chunks = []
            
            doc = Document(file_path)
            full_text = ""
            
            for paragraph in doc.paragraphs:
                full_text += paragraph.text + "\n"
            
            # Clean and chunk the text
            cleaned_text = self._clean_text(full_text)
            text_chunks = self._create_chunks(cleaned_text)
            
            # Create chunk objects with metadata
            for i, chunk in enumerate(text_chunks):
                chunks.append({
                    'content': chunk,
                    'metadata': {
                        'source': os.path.basename(file_path),
                        'type': 'docx',
                        'chunk_id': i,
                        'total_chunks': len(text_chunks),
                        'domain': self._identify_legal_domain(chunk)
                    }
                })
            
            logger.info(f"Processed DOCX: {file_path}, extracted {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            logger.error(f"Error processing DOCX {file_path}: {e}")
            return []
    
    def process_text_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Process text file and extract chunks"""
        try:
            chunks = []
            
            with open(file_path, 'r', encoding='utf-8') as file:
                full_text = file.read()
            
            # Clean and chunk the text
            cleaned_text = self._clean_text(full_text)
            text_chunks = self._create_chunks(cleaned_text)
            
            # Create chunk objects with metadata
            for i, chunk in enumerate(text_chunks):
                chunks.append({
                    'content': chunk,
                    'metadata': {
                        'source': os.path.basename(file_path),
                        'type': 'txt',
                        'chunk_id': i,
                        'total_chunks': len(text_chunks),
                        'domain': self._identify_legal_domain(chunk)
                    }
                })
            
            logger.info(f"Processed TXT: {file_path}, extracted {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            logger.error(f"Error processing text file {file_path}: {e}")
            return []
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep legal formatting
        text = re.sub(r'[^\w\s\.\,\;\:\(\)\-\[\]\"\'\/\&]', '', text)
        
        # Normalize Indian legal terms
        text = text.replace('₹', 'Rs.')
        
        # Remove page markers
        text = re.sub(r'--- Page \d+ ---', '', text)
        
        return text.strip()
    
    def _create_chunks(self, text: str) -> List[str]:
        """Create overlapping text chunks"""
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # If adding this sentence exceeds chunk size, save current chunk
            if len(current_chunk + sentence) > self.chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                
                # Start new chunk with overlap
                overlap_words = current_chunk.split()[-self.chunk_overlap:]
                current_chunk = ' '.join(overlap_words) + ' ' + sentence
            else:
                current_chunk += sentence + '. '
        
        # Add the last chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _identify_legal_domain(self, text: str) -> str:
        """Identify legal domain of the text chunk"""
        text_lower = text.lower()
        
        # Constitutional law keywords
        constitutional_keywords = ['constitution', 'fundamental rights', 'directive principles', 
                                 'amendment', 'article', 'schedule']
        
        # Criminal law keywords
        criminal_keywords = ['criminal', 'offence', 'punishment', 'bail', 'arrest', 
                           'investigation', 'charge', 'ipc', 'bns']
        
        # Civil law keywords
        civil_keywords = ['civil', 'contract', 'property', 'damages', 'injunction', 
                         'suit', 'plaintiff', 'defendant']
        
        # Family law keywords
        family_keywords = ['marriage', 'divorce', 'custody', 'maintenance', 
                          'adoption', 'succession']
        
        # Corporate/Commercial law keywords
        corporate_keywords = ['company', 'corporate', 'shares', 'director', 
                            'commercial', 'business']
        
        # Count matches for each domain
        domain_scores = {
            'constitutional': sum(1 for keyword in constitutional_keywords if keyword in text_lower),
            'criminal': sum(1 for keyword in criminal_keywords if keyword in text_lower),
            'civil': sum(1 for keyword in civil_keywords if keyword in text_lower),
            'family': sum(1 for keyword in family_keywords if keyword in text_lower),
            'corporate': sum(1 for keyword in corporate_keywords if keyword in text_lower)
        }
        
        # Return domain with highest score, default to 'general'
        max_domain = max(domain_scores.items(), key=lambda x: x[1])
        return max_domain[0] if max_domain[1] > 0 else 'general'