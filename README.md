"""
Indian Pocket Lawyer - Project Structure
=======================================

pocket_lawyer/
│
├── requirements.txt
├── config.py
├── main.py
├── 
├── data/
│   ├── raw/                    # Original legal documents
│   ├── processed/              # Cleaned and chunked data
│   └── embeddings/            # Vector embeddings
│
├── src/
│   ├── __init__.py
│   ├── data_ingestion/
│   │   ├── __init__.py
│   │   ├── document_processor.py    # Process legal docs
│   │   ├── web_scraper.py          # Scrape latest updates
│   │   └── pdf_processor.py        # Handle uploaded docs
│   │
│   ├── rag_system/
│   │   ├── __init__.py
│   │   ├── embeddings.py           # Generate embeddings
│   │   ├── vector_store.py         # ChromaDB operations
│   │   ├── retriever.py            # Query matching
│   │   └── generator.py            # Response generation
│   │
│   ├── legal_analyzer/
│   │   ├── __init__.py
│   │   ├── document_analyzer.py    # Analyze uploaded docs
│   │   ├── validity_checker.py     # Check legal validity
│   │   └── contract_reviewer.py    # Review contracts
│   │
│   ├── updater/
│   │   ├── __init__.py
│   │   ├── law_monitor.py          # Monitor legal changes
│   │   └── database_updater.py     # Update embeddings
│   │
│   └── utils/
│       ├── __init__.py
│       ├── security.py             # Privacy & security
│       ├── text_processing.py      # Text cleaning
│       └── logger.py               # Logging system
│
├── tests/
│   ├── test_rag_system.py
│   ├── test_document_processor.py
│   └── test_legal_analyzer.py
│
├── notebooks/
│   ├── data_exploration.ipynb
│   └── model_testing.ipynb
│
└── streamlit_app/
    ├── app.py                      # Main Streamlit interface
    ├── pages/
    │   ├── document_upload.py
    │   ├── legal_query.py
    │   └── validity_check.py
    └── utils/
        └── ui_helpers.py

"""