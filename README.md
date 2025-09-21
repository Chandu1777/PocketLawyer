# README.md - Installation and Usage Guide

"""
# Indian Pocket Lawyer 🏛️

AI-powered legal assistant for Indian Constitution and Laws

## Features

- **Legal Query Resolution**: Ask questions about Indian laws and get AI-powered answers
- **Document Analysis**: Upload legal documents for validity checking and risk assessment
- **Constitutional Knowledge**: Comprehensive database of Indian Constitution and legal provisions
- **Privacy-First**: No personal data storage, secure document processing
- **Free & Open Source**: Built using free-tier AI models and open-source technologies

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/indian-pocket-lawyer.git
cd indian-pocket-lawyer

# Install dependencies
pip install -r requirements.txt

# Setup environment
python main.py --setup --add-samples
```

### 2. Run the Application

**Web Interface (Recommended):**
```bash
python main.py --mode web
```
Then open http://localhost:8501 in your browser

**Command Line Interface:**
```bash
python main.py --mode cli
```

### 3. Configuration

Create a `.env` file in the project root:
```
HUGGINGFACE_API_KEY=your_free_huggingface_token_here
ENVIRONMENT=development
```

## Usage Examples

### Legal Queries
- "What are fundamental rights in Indian Constitution?"
- "How to file an FIR in India?"
- "What is the procedure for property registration?"
- "Rights of accused person in criminal case"

### Document Analysis
- Upload contracts, agreements, legal notices
- Get validity assessment and risk analysis
- Identify key clauses and potential issues
- Receive improvement recommendations

## Architecture

```
├── src/
│   ├── rag_system/          # RAG implementation
│   ├── data_ingestion/      # Document processing
│   ├── legal_analyzer/      # Document analysis
│   └── utils/               # Utilities and security
├── streamlit_app/           # Web interface
├── data/                    # Legal documents and embeddings
└── config.py               # Configuration
```

## Technology Stack

- **Backend**: Python, FastAPI
- **AI/ML**: Sentence Transformers, Hugging Face Transformers
- **Vector DB**: ChromaDB (local, persistent)
- **Frontend**: Streamlit
- **Security**: Built-in file validation and data sanitization

## Free Tier Components

- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2 (free, local)
- **LLM**: Hugging Face free inference API
- **Vector Storage**: ChromaDB (local, no cost)
- **Web Scraping**: BeautifulSoup4 (free)
- **Hosting**: Streamlit Cloud (free tier)

## Legal Data Sources

The system can integrate with official Indian legal sources:
- Constitution of India (india.gov.in)
- Supreme Court judgments (sci.gov.in)
- Legislative updates (sansad.in)
- Law Commission reports

## Security Features

- ✅ File validation and sanitization
- ✅ Personal data detection and masking
- ✅ Secure temporary file handling
- ✅ Query validation and cleaning
- ✅ No personal data storage
- ✅ Audit logging (without sensitive data)

## Development Roadmap

### Phase 1 (Current)
- [x] Core RAG system
- [x] Document processing
- [x] Basic web interface
- [x] Security framework

### Phase 2 (Next)
- [ ] Auto-update from legal websites
- [ ] Advanced document analysis
- [ ] Multi-language support (Hindi)
- [ ] Mobile-responsive design

### Phase 3 (Future)
- [ ] Offline model deployment
- [ ] Advanced legal reasoning
- [ ] Integration with legal databases
- [ ] Professional lawyer tools

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Legal Disclaimer

⚠️ **Important**: This AI tool provides general legal information only and should not be considered as legal advice. Always consult with a qualified lawyer for specific legal matters.

## License

MIT License - see LICENSE file for details.

## Support

- 📧 Email: support@pocketlawyer.in
- 🐛 Issues: GitHub Issues
- 📚 Documentation: Wiki section

## Deployment Options

### Local Development
```bash
python main.py --mode web
```

### Production (Streamlit Cloud)
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Deploy with one click
4. Set environment variables

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## API Integration

### Future API Endpoints
```python
# Legal Query API
POST /api/query
{
    "question": "What are fundamental rights?",
    "domain": "constitutional"  # optional
}

# Document Analysis API  
POST /api/analyze
{
    "document": "base64_encoded_content",
    "analysis_type": "complete"
}

# Legal Validity Check
POST /api/validity
{
    "document": "base64_encoded_content"
}
```

## Performance Optimization

### For Large Document Collections
- Use batch processing for embeddings
- Implement document chunking strategies
- Consider distributed vector storage
- Optimize query retrieval algorithms

### Memory Management
- Lazy loading of models
- Document streaming for large files
- Periodic cache cleanup
- Memory-mapped file handling

## Troubleshooting

### Common Issues

**1. ChromaDB Initialization Error**
```bash
# Solution: Reset the database
rm -rf ./data/embeddings/chroma_db
python main.py --setup
```

**2. Model Loading Error**
```bash
# Solution: Clear Hugging Face cache
rm -rf ~/.cache/huggingface/
pip install --upgrade transformers
```

**3. Streamlit Port Conflict**
```bash
# Solution: Use different port
streamlit run streamlit_app/app.py --server.port=8502
```

**4. Memory Issues**
```bash
# Solution: Reduce chunk size in config.py
CHUNK_SIZE = 500  # Reduce from 1000
```

## Advanced Configuration

### Custom Legal Domain
```python
# In config.py
CUSTOM_LEGAL_DOMAINS = {
    'tax_law': ['income tax', 'gst', 'customs'],
    'corporate_law': ['company act', 'sebi', 'corporate governance'],
    'environmental_law': ['pollution', 'forest rights', 'environmental clearance']
}
```

### Multi-Language Support
```python
# Future feature
SUPPORTED_LANGUAGES = ['en', 'hi', 'ta', 'te', 'bn']
TRANSLATION_API = "google_translate_free"
```

## Testing

### Run Tests
```bash
# Unit tests
python -m pytest tests/ -v

# Integration tests
python -m pytest tests/integration/ -v

# Performance tests
python -m pytest tests/performance/ -v
```

### Test Coverage
```bash
pip install coverage
coverage run -m pytest
coverage report
coverage html  # Generate HTML report
```

## Monitoring and Analytics

### Basic Metrics
- Query response time
- Document processing success rate
- User engagement patterns
- System resource usage

### Logging
```python
# Logs are stored in ./logs/
# Format: pocket_lawyer_YYYYMMDD.log
tail -f logs/pocket_lawyer_$(date +%Y%m%d).log
```

## Community and Ecosystem

### Related Projects
- Legal document templates
- Court case management
- Legal research tools
- Compliance automation

### Integration Partners
- Legal service providers
- Educational institutions
- Government agencies
- NGOs working in legal aid

---

## Getting Started Checklist

- [ ] Python 3.8+ installed
- [ ] Git repository cloned
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Environment configured (`.env` file)
- [ ] System setup completed (`python main.py --setup`)
- [ ] Sample documents added (`--add-samples`)
- [ ] Application running (`python main.py --mode web`)
- [ ] First legal query tested
- [ ] Document analysis tested

## Next Steps

1. **Start Small**: Begin with basic legal queries
2. **Add Documents**: Upload your legal documents
3. **Customize**: Modify configuration for your needs
4. **Extend**: Add new legal domains or features
5. **Deploy**: Move to production environment
6. **Scale**: Optimize for larger document collections

Ready to build your Indian Pocket Lawyer? 🚀

```bash
# Let's get started!
git clone <your-repo-url>
cd indian-pocket-lawyer
pip install -r requirements.txt
python main.py --setup --add-samples
python main.py --mode web
```

Visit http://localhost:8501 and start asking legal questions! 🏛️
"""