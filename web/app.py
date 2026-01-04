"""
Flask web application for Document Q&A system
Provides a user-friendly interface for asking questions
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.search_service import AzureSearchService
from app.ai_service import AIService
from app.document_processor import DocumentProcessor
from app.config import Config
from app.logger import logger

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize services
search_service = AzureSearchService()
ai_service = AIService()


@app.route('/')
def index():
    """Main page"""
    try:
        doc_count = search_service.get_document_count()
    except:
        doc_count = 0

    return render_template('index.html', document_count=doc_count)


@app.route('/upload')
def upload_page():
    """Document upload page"""
    return render_template('upload.html')


@app.route('/api/ask', methods=['POST'])
def ask_question():
    """
    API endpoint for asking questions

    Request JSON:
        {
            "question": "Your question here"
        }

    Response JSON:
        {
            "answer": "The answer",
            "sources": ["source1.pdf", "source2.pdf"],
            "safe": true,
            "grounded": true
        }
    """

    try:
        data = request.get_json()
        question = data.get('question', '').strip()

        if not question:
            return jsonify({
                'error': 'Question is required',
                'answer': None
            }), 400

        logger.info(f"Web request - Question: {question[:50]}...")

        # Search for relevant documents
        results = search_service.search(question)

        if not results:
            return jsonify({
                'answer': 'I could not find any relevant information in the documents to answer your question.',
                'sources': [],
                'safe': True,
                'grounded': False
            })

        # Extract context and sources
        context = "\n\n".join([r['content'] for r in results])
        sources = list(set([r['source'] for r in results]))

        # Generate answer
        result = ai_service.generate_answer(question, context)

        # Log the interaction
        logger.log_question(question, result['answer'], sources)

        return jsonify({
            'answer': result['answer'],
            'sources': sources,
            'safe': result['safe'],
            'grounded': result['grounded'],
            'tokens_used': result.get('tokens_used', 0)
        })

    except Exception as e:
        logger.error(f"Error processing question: {e}")
        return jsonify({
            'error': str(e),
            'answer': 'An error occurred while processing your question.'
        }), 500


@app.route('/api/upload', methods=['POST'])
def upload_document():
    """
    API endpoint for uploading documents
    """

    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Save file temporarily
        file_path = Config.DOCUMENTS_DIR / file.filename
        file.save(file_path)

        logger.info(f"File uploaded: {file.filename}")

        # Validate file
        is_valid, message = DocumentProcessor.validate_file(file_path)
        if not is_valid:
            file_path.unlink()  # Delete invalid file
            return jsonify({'error': message}), 400

        # Process document
        text = DocumentProcessor.process_document(file_path)
        chunks = DocumentProcessor.chunk_text(text)

        # Prepare for upload
        from datetime import datetime, timezone
        documents = []
        for i, chunk in enumerate(chunks):
            doc_id = f"{file_path.stem}-chunk-{i}"
            documents.append({
                'id': doc_id,
                'content': chunk['text'],
                'source': file.filename,
                'chunk_id': i,
                'file_type': file_path.suffix.replace('.', ''),
                'upload_date': datetime.now(timezone.utc).isoformat()
            })

        # Upload to search
        success_count = search_service.upload_documents(documents)

        logger.log_document_upload(file.filename, "success")

        return jsonify({
            'message': f'Successfully uploaded {file.filename}',
            'chunks': len(documents),
            'uploaded': success_count
        })

    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats')
def get_stats():
    """Get system statistics"""
    try:
        doc_count = search_service.get_document_count()

        return jsonify({
            'document_count': doc_count,
            'index_name': search_service.index_name
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🌐 Starting Web Application")
    print("=" * 60)
    print(f"Environment: {Config.APP_ENV}")
    print(f"Index: {Config.AZURE_SEARCH_INDEX_NAME}")
    print("=" * 60)

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=(Config.APP_ENV == 'development')
    )