# src/utils/text_processing.py
import re
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class LegalTextProcessor:
    def __init__(self):
        """Initialize legal text processor"""
        # Common legal abbreviations and their expansions
        self.legal_abbreviations = {
            'CrPC': 'Code of Criminal Procedure',
            'CPC': 'Code of Civil Procedure',
            'IPC': 'Indian Penal Code',
            'BNS': 'Bharatiya Nyaya Sanhita',
            'BSA': 'Bharatiya Sakshya Adhiniyam',
            'BNSS': 'Bharatiya Nagarik Suraksha Sanhita',
            'SC': 'Supreme Court',
            'HC': 'High Court',
            'AIR': 'All India Reporter',
            'SCC': 'Supreme Court Cases',
            'Cr.L.J.': 'Criminal Law Journal'
        }
    
    def normalize_legal_text(self, text: str) -> str:
        """Normalize legal text by expanding abbreviations and standardizing format"""
        try:
            # Expand legal abbreviations
            for abbrev, expansion in self.legal_abbreviations.items():
                text = re.sub(rf'\b{abbrev}\b', expansion, text, flags=re.IGNORECASE)
            
            # Standardize section references
            text = re.sub(r'Sec\.?\s*(\d+)', r'Section \1', text)
            text = re.sub(r'Art\.?\s*(\d+)', r'Article \1', text)
            
            # Standardize case citations
            text = re.sub(r'\b(\d{4})\s*\(\s*(\d+)\s*\)\s*(SCC|AIR|SCR)', 
                         r'\1 (\2) \3', text)
            
            return text
            
        except Exception as e:
            logger.error(f"Error normalizing legal text: {e}")
            return text
    
    def extract_legal_citations(self, text: str) -> List[Dict[str, str]]:
        """Extract legal citations from text"""
        citations = []
        
        try:
            # Pattern for case citations
            case_pattern = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+v\.?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(\d{4})\s*\(\s*(\d+)\s*\)\s*(SCC|AIR|SCR)\s*(\d+)'
            
            matches = re.finditer(case_pattern, text)
            for match in matches:
                citations.append({
                    'type': 'case',
                    'plaintiff': match.group(1),
                    'defendant': match.group(2),
                    'year': match.group(3),
                    'volume': match.group(4),
                    'reporter': match.group(5),
                    'page': match.group(6),
                    'full_citation': match.group(0)
                })
            
            # Pattern for statutory references
            statute_pattern = r'(Section|Article)\s+(\d+(?:\([a-z]\))?)\s+of\s+(?:the\s+)?([A-Z][a-zA-Z\s,]+?)(?:\s+\d{4})?(?=\s|$|\.)'
            
            matches = re.finditer(statute_pattern, text)
            for match in matches:
                citations.append({
                    'type': 'statute',
                    'provision_type': match.group(1),
                    'provision_number': match.group(2),
                    'act_name': match.group(3).strip(),
                    'full_citation': match.group(0)
                })
            
            return citations
            
        except Exception as e:
            logger.error(f"Error extracting legal citations: {e}")
            return []
    
    def identify_legal_concepts(self, text: str) -> List[str]:
        """Identify key legal concepts in text"""
        legal_concepts = []
        
        # Predefined legal concepts
        concept_patterns = {
            'rights': r'\b(fundamental rights?|human rights?|legal rights?|constitutional rights?)\b',
            'procedures': r'\b(due process|fair trial|natural justice|audi alteram partem)\b',
            'remedies': r'\b(injunction|damages|specific performance|mandamus|certiorari|prohibition)\b',
            'crimes': r'\b(murder|theft|fraud|assault|defamation|conspiracy)\b',
            'contracts': r'\b(agreement|consideration|breach|void|voidable|unenforceable)\b'
        }
        
        try:
            for concept_type, pattern in concept_patterns.items():
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    legal_concepts.append({
                        'concept': match.group(0),
                        'type': concept_type,
                        'position': match.start()
                    })
            
            return legal_concepts
            
        except Exception as e:
            logger.error(f"Error identifying legal concepts: {e}")
            return []
        