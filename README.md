# 📚 Document Q&A System

Azure AI Search + OpenAI

An enterprise-grade Document Question & Answer (Q&A) system that enables users to ask questions and receive accurate, grounded answers strictly based on internal company documents.

This project is designed to avoid hallucinations by enforcing strict prompt rules and limiting answers to retrieved document context only.

## 📌 Overview

The system combines:

Azure AI Search – for document indexing and semantic retrieval

OpenAI (GPT-4o-mini) – for generating natural language answers

Strict prompting constraints – to ensure answers are grounded in documents

It is ideal for:

Internal company policies

Knowledge bases

Manuals and SOPs

Enterprise documentation systems

## 🚀 Features

🔍 Document search using Azure AI Search

🤖 AI-powered answers generated only from retrieved documents

🛑 Hallucination prevention with strict prompt enforcement

🧪 Built-in test questions to demonstrate correct behavior

💬 Interactive Q&A mode

📄 Easily extendable to PDFs, manuals, and policy documents

## 📁 Project Structure

```
umar-mukthar-ahmed-document-qa-project/
├── main.py                 # Main Q&A application
├── upload_documents.py     # Uploads documents to Azure AI Search
├── documents/
│   └── sample_policy.txt  # Sample company policy document
└── README.md
```

## ⚙️ Prerequisites

Make sure you have the following:

Python 3.9 or higher

Azure AI Search service

OpenAI API key

Active internet connection

## 🔐 Environment Variables

Create a .env file in the project root directory and add the following:

```env
OPENAI_API_KEY=your_openai_api_key

AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
AZURE_SEARCH_API_KEY=your_azure_search_api_key
AZURE_SEARCH_INDEX_NAME=documents-index
```

## 📦 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/umar-mukthar-ahmed-document-qa-project.git
cd umar-mukthar-ahmed-document-qa-project
```

### 2️⃣ Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 📤 Upload Documents to Azure AI Search

Before running the Q&A system, upload documents to Azure AI Search:

```bash
python upload_documents.py
```

✔ This script will:

Create or update the Azure Search index

Upload sample_policy.txt to the index

You can add more documents inside the documents/ folder.

## ▶️ Run the Application

Start the Q&A system using:

```bash
python main.py
```

You will be presented with three options:

Run test questions – Demonstrates correct answers and "not found" scenarios

Interactive mode – Ask your own questions in real time

Exit – Close the application

## 🧠 How It Prevents Hallucinations

Answers are generated only from retrieved search results

If no relevant content is found, the system responds with:

"The answer is not available in the provided documents."

The AI is explicitly instructed not to use prior knowledge

## 📈 Future Enhancements

PDF and Word document ingestion

Role-based access control

UI frontend (React / Blazor)

Document chunking and embeddings optimization

Logging and analytics

## 📜 License

This project is intended for educational and enterprise demonstration purposes.
