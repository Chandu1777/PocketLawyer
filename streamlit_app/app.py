# streamlit_app/app.py
import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rag_system.retriever import LegalRetriever
from src.rag_system.generator import LegalResponseGenerator
from src.data_ingestion.document_processor import DocumentProcessor
from src.legal_analyzer.document_analyzer import DocumentAnalyzer
from src.utils.security import SecurityManager
from config import Config
import tempfile
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize session state
if 'legal_system' not in st.session_state:
    st.session_state.legal_system = None
    st.session_state.is_initialized = False

def initialize_system():
    """Initialize the legal system components"""
    try:
        Config.create_directories()
        
        # Initialize components
        retriever = LegalRetriever()
        generator = LegalResponseGenerator()
        document_processor = DocumentProcessor()
        document_analyzer = DocumentAnalyzer()
        security_manager = SecurityManager()
        
        st.session_state.legal_system = {
            'retriever': retriever,
            'generator': generator,
            'document_processor': document_processor,
            'document_analyzer': document_analyzer,
            'security_manager': security_manager
        }
        
        st.session_state.is_initialized = True
        return True
        
    except Exception as e:
        logger.error(f"Error initializing system: {e}")
        st.error(f"System initialization failed: {e}")
        return False

def main():
    """Main Streamlit application"""
    
    # Page configuration
    st.set_page_config(
        page_title="Indian Pocket Lawyer",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
        .main-header {
            font-size: 3rem;
            color: #1f4e79;
            text-align: center;
            margin-bottom: 2rem;
        }
        .sub-header {
            font-size: 1.5rem;
            color: #2c5aa0;
            margin-bottom: 1rem;
        }
        .info-box {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 5px solid #1f4e79;
            margin: 1rem 0;
        }
        .warning-box {
            background-color: #fff3cd;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 5px solid #ffc107;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown('<h1 class="main-header">⚖️ Indian Pocket Lawyer</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">Your AI-powered legal assistant for Indian Constitution and Laws</p>', unsafe_allow_html=True)
    
    # Initialize system if not already done
    if not st.session_state.is_initialized:
        with st.spinner("Initializing Legal AI System..."):
            if not initialize_system():
                st.stop()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a feature:",
        ["Legal Query", "Document Analysis", "Document Upload", "System Status"]
    )
    
    # Legal disclaimer
    st.sidebar.markdown("""
    <div class="warning-box">
        <strong>⚠️ Legal Disclaimer:</strong><br>
        This AI provides general legal information only. 
        Always consult a qualified lawyer for specific legal advice.
    </div>
    """, unsafe_allow_html=True)
    
    # Route to different pages
    if page == "Legal Query":
        legal_query_page()
    elif page == "Document Analysis":
        document_analysis_page()
    elif page == "Document Upload":
        document_upload_page()
    elif page == "System Status":
        system_status_page()

def legal_query_page():
    """Legal query interface"""
    st.markdown('<h2 class="sub-header">Ask a Legal Question</h2>', unsafe_allow_html=True)
    
    # Query input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_area(
            "Enter your legal question:",
            height=100,
            placeholder="e.g., What are the fundamental rights guaranteed by Indian Constitution?",
            help="Ask questions about Indian laws, constitutional rights, legal procedures, etc."
        )
    
    with col2:
        st.markdown("**Query Examples:**")
        if st.button("Fundamental Rights"):
            query = "What are the fundamental rights under Indian Constitution?"
        if st.button("Criminal Procedure"):
            query = "What is the procedure for filing an FIR?"
        if st.button("Property Laws"):
            query = "What are the property rights in India?"
    
    # Legal domain filter
    legal_domain = st.selectbox(
        "Filter by legal domain (optional):",
        ["All", "Constitutional", "Criminal", "Civil", "Family", "Corporate"]
    )
    
    # Submit query
    if st.button("Get Legal Answer", type="primary") and query.strip():
        with st.spinner("Searching legal databases..."):
            try:
                # Get system components
                retriever = st.session_state.legal_system['retriever']
                generator = st.session_state.legal_system['generator']
                
                # Apply domain filter
                domain_filter = None if legal_domain == "All" else legal_domain.lower()
                
                # Retrieve relevant documents
                if domain_filter:
                    relevant_docs = retriever.filter_by_legal_domain(query, domain_filter)
                else:
                    relevant_docs = retriever.retrieve_relevant_docs(query)
                
                if relevant_docs:
                    # Generate response
                    response_data = generator.generate_legal_response(query, relevant_docs)
                    
                    # Display response
                    st.markdown("### Legal Response")
                    st.markdown(response_data['response'])
                    
                    # Display confidence and sources
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        confidence = response_data['confidence']
                        st.metric("Confidence Score", f"{confidence:.2%}")
                    
                    with col2:
                        st.metric("Sources Found", len(response_data['sources']))
                    
                    # Show sources
                    if response_data['sources']:
                        with st.expander("📚 Legal Sources", expanded=False):
                            for i, source in enumerate(response_data['sources'], 1):
                                st.markdown(f"**{i}. {source.get('source', 'Unknown Source')}**")
                                if 'domain' in source:
                                    st.markdown(f"*Domain: {source['domain'].title()}*")
                    
                    # Show relevant document snippets
                    with st.expander("📄 Relevant Legal Text", expanded=False):
                        for i, doc in enumerate(relevant_docs[:3], 1):
                            st.markdown(f"**Excerpt {i} (Similarity: {doc['similarity_score']:.2%})**")
                            st.markdown(f"*Source: {doc['metadata'].get('source', 'Unknown')}*")
                            st.text(doc['content'][:500] + "..." if len(doc['content']) > 500 else doc['content'])
                            st.markdown("---")
                
                else:
                    st.warning("No relevant legal information found for your query. Please try rephrasing or check if you've uploaded legal documents to the system.")
                    
            except Exception as e:
                st.error(f"Error processing query: {str(e)}")
                logger.error(f"Query processing error: {e}")

def document_analysis_page():
    """Document analysis interface"""
    st.markdown('<h2 class="sub-header">Document Analysis</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        Upload legal documents (contracts, agreements, legal notices) to get AI-powered analysis including:
        <ul>
            <li>Legal validity assessment</li>
            <li>Risk identification</li>
            <li>Key clause analysis</li>
            <li>Compliance check</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a document to analyze",
        type=['pdf', 'docx', 'txt'],
        help="Supported formats: PDF, DOCX, TXT (Max size: 10MB)"
    )
    
    if uploaded_file is not None:
        # Security check
        security_manager = st.session_state.legal_system['security_manager']
        
        if security_manager.validate_file_upload(uploaded_file):
            # Display file info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("File Name", uploaded_file.name)
            with col2:
                st.metric("File Size", f"{uploaded_file.size / 1024:.1f} KB")
            with col3:
                st.metric("File Type", uploaded_file.type)
            
            # Analysis options
            st.markdown("### Analysis Options")
            analysis_type = st.selectbox(
                "Select analysis type:",
                ["Complete Analysis", "Legal Validity", "Risk Assessment", "Clause Review"]
            )
            
            if st.button("Analyze Document", type="primary"):
                with st.spinner("Analyzing document..."):
                    try:
                        # Save uploaded file temporarily
                        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            tmp_file_path = tmp_file.name
                        
                        # Process document
                        document_processor = st.session_state.legal_system['document_processor']
                        document_analyzer = st.session_state.legal_system['document_analyzer']
                        
                        # Extract text based on file type
                        if uploaded_file.name.endswith('.pdf'):
                            chunks = document_processor.process_pdf(tmp_file_path)
                        elif uploaded_file.name.endswith('.docx'):
                            chunks = document_processor.process_docx(tmp_file_path)
                        else:
                            chunks = document_processor.process_text_file(tmp_file_path)
                        
                        if chunks:
                            # Combine all chunks for analysis
                            full_text = " ".join([chunk['content'] for chunk in chunks])
                            
                            # Perform analysis
                            if analysis_type == "Complete Analysis":
                                analysis_result = document_analyzer.complete_analysis(full_text)
                            elif analysis_type == "Legal Validity":
                                analysis_result = document_analyzer.check_legal_validity(full_text)
                            elif analysis_type == "Risk Assessment":
                                analysis_result = document_analyzer.assess_risks(full_text)
                            else:  # Clause Review
                                analysis_result = document_analyzer.review_clauses(full_text)
                            
                            # Display results
                            display_analysis_results(analysis_result)
                        
                        else:
                            st.error("Could not extract text from the document. Please check the file format.")
                        
                        # Clean up temporary file
                        os.unlink(tmp_file_path)
                        
                    except Exception as e:
                        st.error(f"Error analyzing document: {str(e)}")
                        logger.error(f"Document analysis error: {e}")
        
        else:
            st.error("File validation failed. Please ensure the file is safe and within size limits.")

def document_upload_page():
    """Document upload for training data"""
    st.markdown('<h2 class="sub-header">Upload Legal Documents</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        Upload legal documents to enhance the AI's knowledge base. 
        These documents will be processed and added to the system for better responses.
    </div>
    """, unsafe_allow_html=True)
    
    # Multiple file upload
    uploaded_files = st.file_uploader(
        "Choose legal documents",
        type=['pdf', 'docx', 'txt'],
        accept_multiple_files=True,
        help="Upload multiple legal documents to improve the system"
    )
    
    if uploaded_files:
        st.write(f"Selected {len(uploaded_files)} files for upload")
        
        # Display file list
        for file in uploaded_files:
            st.write(f"📄 {file.name} ({file.size / 1024:.1f} KB)")
        
        if st.button("Process and Add Documents", type="primary"):
            with st.spinner("Processing documents..."):
                try:
                    document_processor = st.session_state.legal_system['document_processor']
                    retriever = st.session_state.legal_system['retriever']
                    
                    total_chunks = 0
                    
                    for uploaded_file in uploaded_files:
                        # Save file temporarily
                        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            tmp_file_path = tmp_file.name
                        
                        # Process based on file type
                        if uploaded_file.name.endswith('.pdf'):
                            chunks = document_processor.process_pdf(tmp_file_path)
                        elif uploaded_file.name.endswith('.docx'):
                            chunks = document_processor.process_docx(tmp_file_path)
                        else:
                            chunks = document_processor.process_text_file(tmp_file_path)
                        
                        # Add to vector store
                        if chunks:
                            texts = [chunk['content'] for chunk in chunks]
                            metadatas = [chunk['metadata'] for chunk in chunks]
                            
                            retriever.vector_store.add_documents(texts, metadatas)
                            total_chunks += len(chunks)
                        
                        # Clean up
                        os.unlink(tmp_file_path)
                    
                    st.success(f"Successfully processed {len(uploaded_files)} documents and added {total_chunks} text chunks to the knowledge base!")
                    
                except Exception as e:
                    st.error(f"Error processing documents: {str(e)}")
                    logger.error(f"Document upload error: {e}")

def system_status_page():
    """System status and information"""
    st.markdown('<h2 class="sub-header">System Status</h2>', unsafe_allow_html=True)
    
    try:
        # Get system information
        retriever = st.session_state.legal_system['retriever']
        collection_info = retriever.vector_store.get_collection_info()
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Documents in Database", collection_info['document_count'])
        
        with col2:
            st.metric("System Status", "✅ Online")
        
        with col3:
            st.metric("Last Update", "Manual")
        
        # System information
        st.markdown("### System Configuration")
        
        config_info = {
            "Embedding Model": Config.EMBEDDING_MODEL,
            "Chunk Size": Config.CHUNK_SIZE,
            "Database Type": "ChromaDB",
            "Security": "✅ Enabled"
        }
        
        for key, value in config_info.items():
            st.write(f"**{key}:** {value}")
        
        # Database actions
        st.markdown("### Database Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Clear Database"):
                if st.checkbox("I confirm this action"):
                    # This would clear the database
                    st.warning("Database clearing functionality would be implemented here")
        
        with col2:
            if st.button("Export Database"):
                st.info("Database export functionality would be implemented here")
        
    except Exception as e:
        st.error(f"Error retrieving system status: {str(e)}")

def display_analysis_results(analysis_result):
    """Display document analysis results"""
    if 'summary' in analysis_result:
        st.markdown("### Analysis Summary")
        st.info(analysis_result['summary'])
    
    if 'validity_score' in analysis_result:
        st.markdown("### Legal Validity Score")
        score = analysis_result['validity_score']
        st.progress(score)
        st.write(f"Validity Score: {score:.1%}")
    
    if 'risks' in analysis_result:
        st.markdown("### Identified Risks")
        for risk in analysis_result['risks']:
            st.warning(f"⚠️ {risk}")
    
    if 'recommendations' in analysis_result:
        st.markdown("### Recommendations")
        for rec in analysis_result['recommendations']:
            st.success(f"✅ {rec}")
    
    if 'key_clauses' in analysis_result:
        st.markdown("### Key Clauses")
        for clause in analysis_result['key_clauses']:
            st.markdown(f"- **{clause['type']}:** {clause['content'][:200]}...")

if __name__ == "__main__":
    main()