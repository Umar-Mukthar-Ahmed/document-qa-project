# 📚 Enterprise Document Q&A System

A production-ready document question-answering system built with Azure AI Search and OpenAI.

## 🌟 Features

- ✅ **Document-Grounded Answers**: Only answers based on uploaded documents
- ✅ **Multi-Format Support**: PDF, TXT files
- ✅ **Safety Filtering**: Blocks inappropriate questions
- ✅ **Comprehensive Logging**: Tracks all interactions
- ✅ **Web Interface**: User-friendly Flask web app
- ✅ **CLI Interface**: Command-line option for testing
- ✅ **Error Handling**: Graceful handling of corrupted files
- ✅ **Production Ready**: Proper structure and best practices

## 🏗️ Architecture
```
User Question
     ↓
Safety Filter (check question)
     ↓
Azure AI Search (find relevant documents)
     ↓
Context Retrieved
     ↓
Prompt Template (enforce constraints)
     ↓
OpenAI API (generate answer)
     ↓
Safety Filter (validate answer)
     ↓
Grounded Answer Returned