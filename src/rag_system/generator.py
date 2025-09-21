# src/rag_system/generator.py
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from typing import List, Dict, Any
import torch
from config import Config
import logging

logger = logging.getLogger(__name__)

class LegalResponseGenerator:
    def __init__(self):
        """Initialize response generator with free LLM"""
        try:
            # Use Hugging Face pipeline for text generation (free)
            self.generator = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-medium",  # Free model
                device=0 if torch.cuda.is_available() else -1
            )
            
            logger.info("Response generator initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing response generator: {e}")
            # Fallback to a simpler approach
            self.generator = None
    
    def generate_legal_response(self, 
                               query: str, 
                               relevant_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate legal response based on query and relevant documents"""
        try:
            # Create context from relevant documents
            context = self._create_context(relevant_docs)
            
            # Create prompt
            prompt = self._create_legal_prompt(query, context)
            
            # Generate response
            if self.generator:
                response = self._generate_with_model(prompt)
            else:
                response = self._generate_rule_based_response(query, relevant_docs)
            
            return {
                "response": response,
                "sources": [doc['metadata'] for doc in relevant_docs],
                "confidence": self._calculate_confidence(relevant_docs)
            }
            
        except Exception as e:
            logger.error(f"Error generating legal response: {e}")
            return {
                "response": "I apologize, but I'm unable to process your legal query at the moment. Please try again later.",
                "sources": [],
                "confidence": 0.0
            }
    
    def _create_context(self, relevant_docs: List[Dict[str, Any]]) -> str:
        """Create context from relevant documents"""
        context_parts = []
        for doc in relevant_docs[:3]:  # Use top 3 most relevant
            content = doc['content'][:500]  # Limit length
            source = doc['metadata'].get('source', 'Legal Document')
            context_parts.append(f"From {source}: {content}")
        
        return "\n\n".join(context_parts)
    
    def _create_legal_prompt(self, query: str, context: str) -> str:
        """Create legal prompt for LLM"""
        prompt = f"""Based on Indian legal documents and constitution, please answer the following legal question:

Query: {query}

Legal Context:
{context}

Please provide a clear, accurate response based on Indian law. If the information is insufficient, please mention that additional legal consultation may be required.

Response:"""
        
        return prompt
    
    def _generate_with_model(self, prompt: str) -> str:
        """Generate response using the model"""
        try:
            outputs = self.generator(
                prompt,
                max_length=len(prompt.split()) + 150,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.generator.tokenizer.eos_token_id
            )
            
            generated_text = outputs[0]['generated_text']
            # Extract only the response part
            response = generated_text.replace(prompt, "").strip()
            return response
            
        except Exception as e:
            logger.error(f"Error generating with model: {e}")
            return "Unable to generate response with language model."
    
    def _generate_rule_based_response(self, query: str, relevant_docs: List[Dict[str, Any]]) -> str:
        """Generate rule-based response as fallback"""
        if not relevant_docs:
            return "I couldn't find relevant legal information for your query. Please consult with a legal professional for accurate advice."
        
        # Simple rule-based response
        response = f"Based on available legal documents, here's what I found regarding your query:\n\n"
        
        for i, doc in enumerate(relevant_docs[:2]):
            response += f"{i+1}. {doc['content'][:300]}...\n\n"
        
        response += "Please note: This information is for educational purposes only. For specific legal advice, consult with a qualified legal professional."
        
        return response
    
    def _calculate_confidence(self, relevant_docs: List[Dict[str, Any]]) -> float:
        """Calculate confidence score based on document relevance"""
        if not relevant_docs:
            return 0.0
        
        # Average similarity scores
        scores = [doc.get('similarity_score', 0) for doc in relevant_docs]
        return sum(scores) / len(scores) if scores else 0.0