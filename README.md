# 📚 Enterprise Document Q&A System

A production-ready document question-answering system built with Azure AI Search and OpenAI, designed to provide accurate, document-grounded responses with enterprise-grade safety and logging.

## 🌟 Features

- ✅ **Document-Grounded Answers**: Only answers based on uploaded documents
- ✅ **Multi-Format Support**: PDF, TXT, and DOCX files
- ✅ **Safety Filtering**: Blocks inappropriate questions and validates responses
- ✅ **Comprehensive Logging**: Tracks all interactions and system operations
- ✅ **Web Interface**: User-friendly Flask web application
- ✅ **CLI Interface**: Command-line option for testing and automation
- ✅ **Error Handling**: Graceful handling of corrupted files and edge cases
- ✅ **Production Ready**: Professional structure and best practices

## 🏗️ Architecture

```
User Question
     ↓
Safety Filter (validate question)
     ↓
Azure AI Search (retrieve relevant documents)
     ↓
Context Assembly
     ↓
Prompt Template (enforce constraints)
     ↓
OpenAI API (generate grounded answer)
     ↓
Safety Filter (validate response)
     ↓
Grounded Answer Delivered
```

## 📋 Prerequisites

- Python 3.8+
- Azure account with AI Search service
- OpenAI API key

## 🚀 Quick Start

### 1. Clone and Setup

```bash
cd document-qa-enterprise
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file with your credentials:

```env
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini

# Azure Search Configuration
AZURE_SEARCH_ENDPOINT=https://yourname-search-service.search.windows.net
AZURE_SEARCH_API_KEY=your-azure-search-admin-key
AZURE_SEARCH_INDEX_NAME=enterprise-documents

# Application Settings
APP_ENV=development
LOG_LEVEL=INFO
MAX_FILE_SIZE_MB=10
ALLOWED_FILE_TYPES=pdf,txt,docx

# Safety Settings
ENABLE_CONTENT_FILTER=true
MAX_QUESTION_LENGTH=500
```

### 3. Initialize System

```bash
# Create search index
python run.py setup

# Upload documents
# First, add PDF/TXT files to data/documents/
python run.py upload

# Test system
python run.py test
```

### 4. Run Application

**Web Interface:**
```bash
python run.py web
# Open http://localhost:5000
```

**CLI Interface:**
```bash
python run.py cli
```

## 📁 Project Structure

```
document-qa-enterprise/
├── app/                    # Core application
│   ├── config.py          # Configuration
│   ├── logger.py          # Logging system
│   ├── search_service.py  # Azure Search
│   ├── ai_service.py      # OpenAI integration
│   ├── document_processor.py  # File processing
│   └── safety_filter.py   # Content safety
├── web/                   # Web interface
│   ├── app.py            # Flask application
│   ├── templates/        # HTML templates
│   └── static/           # CSS, JS
├── scripts/              # Utility scripts
│   ├── setup_index.py   # Initialize search
│   ├── upload_documents.py  # Bulk upload
│   └── test_system.py   # System testing
├── data/
│   ├── documents/       # Document storage
│   └── logs/           # Application logs
└── run.py              # Main entry point
```

## 🔧 Configuration

Edit `.env` to customize:

- **MAX_FILE_SIZE_MB**: Maximum file size (default: 10MB)
- **ALLOWED_FILE_TYPES**: Supported formats (default: pdf,txt,docx)
- **ENABLE_CONTENT_FILTER**: Enable safety filter (default: true)
- **LOG_LEVEL**: Logging level (INFO, DEBUG, WARNING, ERROR)

## 📊 Usage Examples

### CLI Mode

```bash
python run.py cli

❓ Your question: How many days of annual leave?

💡 Answer:
Employees receive 20 days of paid annual leave per year.
```

### Web Mode

1. Start server: `python run.py web`
2. Open browser: `http://localhost:5000`
3. Ask questions in the chat interface
4. Upload documents via `/upload` page

## 🧪 Testing

Run automated tests:

```bash
python run.py test
```

Tests include:
- Azure Search connectivity
- OpenAI API connectivity
- End-to-end Q&A functionality
- Safety filter validation

## 📝 Logging

All operations are logged to `data/logs/app_YYYYMMDD.log`:

- User questions and answers
- Document uploads
- Errors and warnings
- System operations

## 🔒 Security Features

1. **Content Filtering**: Blocks inappropriate questions
2. **Input Validation**: Checks file size, type
3. **Grounded Answers**: Only from uploaded documents
4. **Audit Trail**: Complete logging of all interactions
5. **Error Handling**: Graceful failure management

## 🎯 Assignment Submission

Include:
1. Screenshots of web interface
2. Sample Q&A interactions
3. Document upload proof
4. Test results output
5. This README

## 🐛 Troubleshooting

### "Index does not exist"
```bash
# Solution
python run.py setup
```

### "No documents found"
```bash
# Solution
# Add files to data/documents/
python run.py upload
```

### "API key error"
- Check `.env` file has correct keys
- Ensure no extra spaces in keys

## 📚 Additional Resources

- [Azure AI Search Docs](https://docs.microsoft.com/azure/search/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 👨‍💻 Author

Umar Mukthar Ahmed

## 📄 License

Educational Project - MIT License
