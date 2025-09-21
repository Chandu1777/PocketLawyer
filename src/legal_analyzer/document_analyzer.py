# src/legal_analyzer/document_analyzer.py
import re
from typing import Dict, List, Any, Tuple
import logging
from src.utils.text_processing import LegalTextProcessor

logger = logging.getLogger(__name__)

class DocumentAnalyzer:
    def __init__(self):
        """Initialize document analyzer"""
        self.text_processor = LegalTextProcessor()
        
        # Legal validity indicators
        self.validity_indicators = {
            'positive': [
                'executed', 'signed', 'witnessed', 'stamped', 'registered',
                'valid consideration', 'mutual consent', 'lawful object',
                'competent parties', 'free consent'
            ],
            'negative': [
                'void', 'voidable', 'illegal', 'unenforceable', 'fraudulent',
                'coercion', 'undue influence', 'mistake', 'misrepresentation',
                'breach', 'violation'
            ]
        }
        
        # Risk indicators
        self.risk_indicators = {
            'high': [
                'penalty', 'liquidated damages', 'termination', 'default',
                'breach', 'liability', 'indemnity', 'force majeure'
            ],
            'medium': [
                'dispute', 'arbitration', 'jurisdiction', 'governing law',
                'modification', 'assignment', 'confidentiality'
            ],
            'low': [
                'notice period', 'renewal', 'amendment', 'severability'
            ]
        }
    
    def complete_analysis(self, document_text: str) -> Dict[str, Any]:
        """Perform complete document analysis"""
        try:
            # Basic analysis
            validity_result = self.check_legal_validity(document_text)
            risk_result = self.assess_risks(document_text)
            clause_result = self.review_clauses(document_text)
            
            # Extract additional information
            citations = self.text_processor.extract_legal_citations(document_text)
            concepts = self.text_processor.identify_legal_concepts(document_text)
            
            # Compile complete analysis
            analysis = {
                'summary': self._generate_summary(document_text),
                'validity_score': validity_result.get('score', 0),
                'validity_assessment': validity_result.get('assessment', ''),
                'risks': risk_result.get('risks', []),
                'risk_level': risk_result.get('level', 'Unknown'),
                'key_clauses': clause_result.get('clauses', []),
                'legal_citations': citations,
                'legal_concepts': concepts,
                'recommendations': self._generate_recommendations(validity_result, risk_result),
                'document_type': self._identify_document_type(document_text)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in complete analysis: {e}")
            return {'error': str(e)}
    
    def check_legal_validity(self, document_text: str) -> Dict[str, Any]:
        """Check legal validity of document"""
        try:
            validity_score = 0.5  # Base score
            assessment_points = []
            
            # Check for positive indicators
            positive_count = sum(1 for indicator in self.validity_indicators['positive'] 
                               if indicator.lower() in document_text.lower())
            
            # Check for negative indicators
            negative_count = sum(1 for indicator in self.validity_indicators['negative'] 
                               if indicator.lower() in document_text.lower())
            
            # Adjust score based on indicators
            validity_score += (positive_count * 0.1)
            validity_score -= (negative_count * 0.15)
            validity_score = max(0, min(1, validity_score))  # Keep between 0 and 1
            
            # Check essential elements
            essential_elements = {
                'parties': self._check_parties(document_text),
                'consideration': self._check_consideration(document_text),
                'object': self._check_lawful_object(document_text),
                'consent': self._check_consent(document_text)
            }
            
            # Assessment based on essential elements
            if essential_elements['parties']:
                assessment_points.append("✅ Parties are clearly identified")
            else:
                assessment_points.append("❌ Parties need clearer identification")
                validity_score -= 0.2
            
            if essential_elements['consideration']:
                assessment_points.append("✅ Consideration is mentioned")
            else:
                assessment_points.append("⚠️ Consideration should be clearly stated")
                validity_score -= 0.15
            
            # Generate assessment text
            if validity_score >= 0.8:
                assessment = "Document appears to be legally valid with strong enforceability."
            elif validity_score >= 0.6:
                assessment = "Document has good validity but may need minor improvements."
            elif validity_score >= 0.4:
                assessment = "Document has moderate validity with some concerns to address."
            else:
                assessment = "Document has significant validity issues that need attention."
            
            return {
                'score': validity_score,
                'assessment': assessment,
                'details': assessment_points,
                'essential_elements': essential_elements
            }
            
        except Exception as e:
            logger.error(f"Error checking legal validity: {e}")
            return {'score': 0, 'assessment': 'Error in analysis', 'error': str(e)}
    
    def assess_risks(self, document_text: str) -> Dict[str, Any]:
        """Assess risks in the document"""
        try:
            risks = []
            risk_score = 0
            
            # Check for high-risk indicators
            for indicator in self.risk_indicators['high']:
                if indicator.lower() in document_text.lower():
                    risks.append(f"High Risk: Contains {indicator} clause")
                    risk_score += 3
            
            # Check for medium-risk indicators
            for indicator in self.risk_indicators['medium']:
                if indicator.lower() in document_text.lower():
                    risks.append(f"Medium Risk: Contains {indicator} provision")
                    risk_score += 2
            
            # Check for low-risk indicators
            for indicator in self.risk_indicators['low']:
                if indicator.lower() in document_text.lower():
                    risks.append(f"Low Risk: Contains {indicator} clause")
                    risk_score += 1
            
            # Determine overall risk level
            if risk_score >= 10:
                risk_level = "High"
            elif risk_score >= 5:
                risk_level = "Medium"
            elif risk_score > 0:
                risk_level = "Low"
            else:
                risk_level = "Minimal"
            
            # Add specific risk checks
            specific_risks = self._check_specific_risks(document_text)
            risks.extend(specific_risks)
            
            return {
                'risks': risks,
                'risk_score': risk_score,
                'level': risk_level
            }
            
        except Exception as e:
            logger.error(f"Error assessing risks: {e}")
            return {'risks': [], 'level': 'Unknown', 'error': str(e)}
    
    def review_clauses(self, document_text: str) -> Dict[str, Any]:
        """Review and analyze key clauses in the document"""
        try:
            clauses = []
            
            # Define clause patterns
            clause_patterns = {
                'termination': r'(termination|terminate|end|expiry|expire).*?(?=\.|;|\n)',
                'payment': r'(payment|pay|amount|fee|consideration|remuneration).*?(?=\.|;|\n)',
                'liability': r'(liability|liable|responsible|damages|compensation).*?(?=\.|;|\n)',
                'confidentiality': r'(confidential|non-disclosure|proprietary|secret).*?(?=\.|;|\n)',
                'dispute': r'(dispute|arbitration|court|jurisdiction|governing law).*?(?=\.|;|\n)',
                'force_majeure': r'(force majeure|act of god|unforeseeable|beyond control).*?(?=\.|;|\n)'
            }
            
            for clause_type, pattern in clause_patterns.items():
                matches = re.finditer(pattern, document_text, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    clause_text = match.group(0).strip()
                    if len(clause_text) > 20:  # Filter out very short matches
                        clauses.append({
                            'type': clause_type.replace('_', ' ').title(),
                            'content': clause_text,
                            'position': match.start(),
                            'analysis': self._analyze_clause(clause_type, clause_text)
                        })
            
            return {'clauses': clauses}
            
        except Exception as e:
            logger.error(f"Error reviewing clauses: {e}")
            return {'clauses': [], 'error': str(e)}
    
    def _check_parties(self, text: str) -> bool:
        """Check if parties are clearly identified"""
        party_indicators = ['party', 'parties', 'between', 'whereas', 'contractor', 'client']
        return any(indicator in text.lower() for indicator in party_indicators)
    
    def _check_consideration(self, text: str) -> bool:
        """Check if consideration is mentioned"""
        consideration_indicators = ['consideration', 'payment', 'amount', 'fee', 'sum', 'rupees', 'rs.']
        return any(indicator in text.lower() for indicator in consideration_indicators)
    
    def _check_lawful_object(self, text: str) -> bool:
        """Check for lawful object"""
        unlawful_indicators = ['illegal', 'unlawful', 'criminal', 'fraud', 'bribe']
        return not any(indicator in text.lower() for indicator in unlawful_indicators)
    
    def _check_consent(self, text: str) -> bool:
        """Check for free consent"""
        consent_indicators = ['agree', 'consent', 'willing', 'voluntary']
        coercion_indicators = ['coercion', 'force', 'threat', 'undue influence']
        
        has_consent = any(indicator in text.lower() for indicator in consent_indicators)
        has_coercion = any(indicator in text.lower() for indicator in coercion_indicators)
        
        return has_consent and not has_coercion
    
    def _check_specific_risks(self, text: str) -> List[str]:
        """Check for specific legal risks"""
        risks = []
        
        # Unlimited liability risk
        if 'unlimited liability' in text.lower():
            risks.append("Critical Risk: Unlimited liability exposure")
        
        # Personal guarantee risk
        if 'personal guarantee' in text.lower():
            risks.append("High Risk: Personal guarantee required")
        
        # Automatic renewal risk
        if 'automatic renewal' in text.lower() or 'auto renewal' in text.lower():
            risks.append("Medium Risk: Automatic renewal clause")
        
        # Exclusive dealing risk
        if 'exclusive' in text.lower() and 'deal' in text.lower():
            risks.append("Medium Risk: Exclusive dealing arrangement")
        
        # Intellectual property risk
        if 'intellectual property' in text.lower() and 'assign' in text.lower():
            risks.append("High Risk: IP assignment clause")
        
        return risks
    
    def _analyze_clause(self, clause_type: str, clause_text: str) -> str:
        """Analyze specific clause and provide insights"""
        analysis = ""
        
        if clause_type == 'termination':
            if 'notice' in clause_text.lower():
                analysis = "Good: Includes notice period for termination"
            else:
                analysis = "Consider: Adding notice period requirements"
        
        elif clause_type == 'payment':
            if 'within' in clause_text.lower() and 'days' in clause_text.lower():
                analysis = "Good: Payment timeline specified"
            else:
                analysis = "Consider: Specify clear payment timelines"
        
        elif clause_type == 'liability':
            if 'limited' in clause_text.lower():
                analysis = "Good: Liability is limited"
            elif 'unlimited' in clause_text.lower():
                analysis = "Caution: Unlimited liability exposure"
            else:
                analysis = "Consider: Clarifying liability limits"
        
        elif clause_type == 'dispute':
            if 'arbitration' in clause_text.lower():
                analysis = "Good: Dispute resolution mechanism specified"
            else:
                analysis = "Consider: Adding dispute resolution process"
        
        return analysis
    
    def _generate_summary(self, text: str) -> str:
        """Generate document summary"""
        doc_type = self._identify_document_type(text)
        word_count = len(text.split())
        
        summary = f"This appears to be a {doc_type} with approximately {word_count} words. "
        
        # Add key observations
        if 'agreement' in text.lower():
            summary += "It contains contractual agreements between parties. "
        
        if 'payment' in text.lower():
            summary += "Financial obligations are mentioned. "
        
        if 'termination' in text.lower():
            summary += "Termination conditions are specified. "
        
        return summary
    
    def _identify_document_type(self, text: str) -> str:
        """Identify the type of legal document"""
        text_lower = text.lower()
        
        if 'service agreement' in text_lower or 'services agreement' in text_lower:
            return "Service Agreement"
        elif 'employment' in text_lower and ('contract' in text_lower or 'agreement' in text_lower):
            return "Employment Contract"
        elif 'lease' in text_lower or 'rent' in text_lower:
            return "Lease Agreement"
        elif 'non-disclosure' in text_lower or 'confidentiality' in text_lower:
            return "Non-Disclosure Agreement"
        elif 'partnership' in text_lower:
            return "Partnership Agreement"
        elif 'sale' in text_lower and 'purchase' in text_lower:
            return "Sale Agreement"
        elif 'license' in text_lower:
            return "License Agreement"
        elif 'contract' in text_lower:
            return "Contract"
        elif 'agreement' in text_lower:
            return "Legal Agreement"
        elif 'notice' in text_lower:
            return "Legal Notice"
        elif 'will' in text_lower and ('testament' in text_lower or 'estate' in text_lower):
            return "Will/Testament"
        else:
            return "Legal Document"
    
    def _generate_recommendations(self, validity_result: Dict, risk_result: Dict) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        # Validity-based recommendations
        validity_score = validity_result.get('score', 0)
        if validity_score < 0.6:
            recommendations.append("Consider consulting a lawyer to improve document validity")
        
        if not validity_result.get('essential_elements', {}).get('parties', False):
            recommendations.append("Clearly identify all parties with full names and addresses")
        
        if not validity_result.get('essential_elements', {}).get('consideration', False):
            recommendations.append("Specify the consideration/payment terms clearly")
        
        # Risk-based recommendations
        risk_level = risk_result.get('level', 'Unknown')
        if risk_level == 'High':
            recommendations.append("High-risk elements detected - legal review strongly recommended")
        
        risks = risk_result.get('risks', [])
        if any('unlimited liability' in risk.lower() for risk in risks):
            recommendations.append("Consider limiting liability exposure")
        
        if any('personal guarantee' in risk.lower() for risk in risks):
            recommendations.append("Carefully evaluate personal guarantee implications")
        
        # General recommendations
        recommendations.append("Ensure all parties sign and date the document")
        recommendations.append("Keep original copies in a secure location")
        recommendations.append("Review document periodically for compliance")
        
        return recommendations