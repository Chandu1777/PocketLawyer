# main.py
"""
Indian Pocket Lawyer - Main Application Runner
=============================================

This script sets up and runs the Indian Pocket Lawyer application.
It can be run as a Streamlit web app or as a command-line interface.
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config import Config
from src.utils.logger import setup_logger

# Setup logging
logger = setup_logger('main')

def setup_environment():
    """Setup the application environment"""
    try:
        logger.info("Setting up Indian Pocket Lawyer environment...")
        
        # Create necessary directories
        Config.create_directories()
        logger.info("✅ Directories created successfully")
        
        # Initialize components (basic validation)
        from src.rag_system.embeddings import EmbeddingGenerator
        from src.rag_system.vector_store import VectorStore
        
        # Test embedding model
        embedding_gen = EmbeddingGenerator()
        test_embedding = embedding_gen.generate_single_embedding("test")
        logger.info("✅ Embedding model loaded successfully")
        
        # Test vector store
        vector_store = VectorStore()
        info = vector_store.get_collection_info()
        logger.info(f"✅ Vector store initialized: {info['document_count']} documents")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Environment setup failed: {e}")
        return False

def run_streamlit_app():
    """Run the Streamlit web application"""
    try:
        import streamlit.web.cli as stcli
        import sys
        
        # Setup environment first
        if not setup_environment():
            logger.error("Environment setup failed. Cannot start application.")
            return False
        
        logger.info("🚀 Starting Streamlit application...")
        
        # Run Streamlit app
        app_path = os.path.join(os.path.dirname(__file__), 'streamlit_app', 'app.py')
        
        sys.argv = [
            "streamlit",
            "run",
            app_path,
            "--server.port=8501",
            "--server.address=localhost",
            "--browser.gatherUsageStats=false"
        ]
        
        stcli.main()
        return True
        
    except ImportError:
        logger.error("Streamlit not installed. Install with: pip install streamlit")
        return False
    except Exception as e:
        logger.error(f"Error running Streamlit app: {e}")
        return False

def run_cli_mode():
    """Run in command-line interface mode"""
    try:
        if not setup_environment():
            logger.error("Environment setup failed. Cannot start CLI.")
            return False
        
        from src.rag_system.retriever import LegalRetriever
        from src.rag_system.generator import LegalResponseGenerator
        
        retriever = LegalRetriever()
        generator = LegalResponseGenerator()
        
        print("🏛️  Indian Pocket Lawyer - CLI Mode")
        print("=" * 50)
        print("Enter your legal questions (type 'quit' to exit)")
        print()
        
        while True:
            query = input("Legal Query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("Thank you for using Indian Pocket Lawyer!")
                break
            
            if not query:
                continue
            
            try:
                print("\n🔍 Searching legal databases...")
                
                # Retrieve and generate response
                relevant_docs = retriever.retrieve_relevant_docs(query)
                
                if relevant_docs:
                    response_data = generator.generate_legal_response(query, relevant_docs)
                    
                    print(f"\n📋 Legal Response:")
                    print("-" * 30)
                    print(response_data['response'])
                    print()
                    
                    print(f"📊 Confidence: {response_data['confidence']:.1%}")
                    print(f"📚 Sources: {len(response_data['sources'])}")
                    print()
                
                else:
                    print("\n❌ No relevant legal information found.")
                    print("Try rephrasing your question or add more legal documents to the system.")
                    print()
            
            except Exception as e:
                print(f"\n❌ Error processing query: {e}")
                print()
        
        return True
        
    except Exception as e:
        logger.error(f"Error in CLI mode: {e}")
        return False

def add_sample_documents():
    """Add sample legal documents for testing"""
    try:
        logger.info("Adding sample legal documents...")
        
        from src.data_ingestion.document_processor import DocumentProcessor
        from src.rag_system.vector_store import VectorStore
        
        processor = DocumentProcessor()
        vector_store = VectorStore()
        
        # Sample legal texts (basic Indian legal concepts)
        sample_docs = [
            {
                'content': """Article 14 of the Indian Constitution guarantees equality before law. 
                It states that the State shall not deny to any person equality before the law or 
                the equal protection of the laws within the territory of India. This article ensures 
                that all persons, whether citizens or non-citizens, are equal before law.""",
                'metadata': {
                    'source': 'Constitution of India - Article 14',
                    'type': 'constitutional',
                    'domain': 'constitutional',
                    'article': '14'
                }
            },
            {
                'content': """The right to freedom of speech and expression is guaranteed under Article 19(1)(a) 
                of the Indian Constitution. However, this right is not absolute and is subject to reasonable 
                restrictions under Article 19(2) in the interests of sovereignty and integrity of India, 
                security of State, friendly relations with foreign States, public order, decency or morality.""",
                'metadata': {
                    'source': 'Constitution of India - Article 19',
                    'type': 'constitutional',
                    'domain': 'constitutional',
                    'article': '19'
                }
            },
            {
                'content': """Section 302 of the Indian Penal Code deals with punishment for murder. 
                Whoever commits murder shall be punished with death, or imprisonment for life, 
                and shall also be liable to fine. Murder is defined under Section 300 as culpable 
                homicide with specific intentions or knowledge.""",
                'metadata': {
                    'source': 'Indian Penal Code - Section 302',
                    'type': 'criminal',
                    'domain': 'criminal',
                    'section': '302'
                }
            },
            {
                'content': """A contract is an agreement enforceable by law. According to Section 2(h) 
                of the Indian Contract Act, 1872, an agreement enforceable by law is a contract. 
                Essential elements of a valid contract include offer, acceptance, consideration, 
                capacity of parties, free consent, lawful object, and certainty.""",
                'metadata': {
                    'source': 'Indian Contract Act - Section 2(h)',
                    'type': 'civil',
                    'domain': 'civil',
                    'section': '2(h)'
                }
            }
        ]
        
        # Process and add documents
        texts = [doc['content'] for doc in sample_docs]
        metadatas = [doc['metadata'] for doc in sample_docs]
        
        vector_store.add_documents(texts, metadatas)
        
        logger.info(f"✅ Added {len(sample_docs)} sample documents")
        return True
        
    except Exception as e:
        logger.error(f"Error adding sample documents: {e}")
        return False

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description='Indian Pocket Lawyer - AI Legal Assistant')
    parser.add_argument(
        '--mode', 
        choices=['web', 'cli'], 
        default='web',
        help='Run mode: web (Streamlit) or cli (command line)'
    )
    parser.add_argument(
        '--setup', 
        action='store_true',
        help='Setup environment and add sample documents'
    )
    parser.add_argument(
        '--add-samples', 
        action='store_true',
        help='Add sample legal documents to the system'
    )
    
    args = parser.parse_args()
    
    print("🏛️  Indian Pocket Lawyer")
    print("=" * 50)
    print("AI-Powered Legal Assistant for Indian Constitution and Laws")
    print()
    
    # Setup mode
    if args.setup:
        print("Setting up environment...")
        if setup_environment():
            print("✅ Environment setup completed successfully!")
            if args.add_samples:
                add_sample_documents()
        else:
            print("❌ Environment setup failed!")
            return 1
    
    # Add sample documents
    elif args.add_samples:
        if add_sample_documents():
            print("✅ Sample documents added successfully!")
        else:
            print("❌ Failed to add sample documents!")
            return 1
    
    # Run application
    else:
        if args.mode == 'web':
            print("Starting web interface...")
            if not run_streamlit_app():
                return 1
        
        elif args.mode == 'cli':
            print("Starting CLI interface...")
            if not run_cli_mode():
                return 1
    
    return 0

if __name__ == "__main__":
    exit(main())