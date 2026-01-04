"""
Script to upload documents to Azure AI Search
Supports multiple files and formats
"""

import sys
from pathlib import Path
from datetime import datetime, timezone

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.search_service import AzureSearchService
from app.document_processor import DocumentProcessor
from app.config import Config
from app.logger import logger

def upload_document(file_path: Path, search_service: AzureSearchService) -> bool:
    """Upload a single document"""

    try:
        print(f"\n📄 Processing: {file_path.name}")

        # Validate file
        is_valid, message = DocumentProcessor.validate_file(file_path)
        if not is_valid:
            print(f"   ❌ Validation failed: {message}")
            logger.log_document_upload(file_path.name, "failed", message)
            return False

        # Extract text
        print(f"   📖 Extracting text...")
        text = DocumentProcessor.process_document(file_path)

        # Create chunks
        print(f"   ✂️  Creating chunks...")
        chunks = DocumentProcessor.chunk_text(text)

        # Prepare documents for upload with FIXED datetime format
        documents = []
        for i, chunk in enumerate(chunks):
            doc_id = f"{file_path.stem}-chunk-{i}"
            documents.append({
                'id': doc_id,
                'content': chunk['text'],
                'source': file_path.name,
                'chunk_id': i,
                'file_type': file_path.suffix.replace('.', ''),
                'upload_date': datetime.now(timezone.utc).isoformat()  # ✅ FIXED
            })

        # Upload to Azure Search
        print(f"   ☁️  Uploading {len(documents)} chunks...")
        success_count = search_service.upload_documents(documents)

        if success_count == len(documents):
            print(f"   ✅ Successfully uploaded all chunks")
            logger.log_document_upload(file_path.name, "success")
            return True
        else:
            print(f"   ⚠️  Uploaded {success_count}/{len(documents)} chunks")
            logger.log_document_upload(file_path.name, "partial", f"Only {success_count}/{len(documents)} uploaded")
            return False

    except Exception as e:
        print(f"   ❌ Error: {e}")
        logger.log_document_upload(file_path.name, "failed", str(e))
        return False

def main():
    """Main upload function"""

    print("="*60)
    print("📤 DOCUMENT UPLOAD SYSTEM")
    print("="*60)

    try:
        # Initialize search service
        search_service = AzureSearchService()

        # Check if index exists
        if not search_service.index_exists():
            print("\n❌ Index does not exist!")
            print("   Please run 'python run.py setup' first")
            sys.exit(1)

        # Get documents directory
        docs_dir = Config.DOCUMENTS_DIR

        # Find all supported files
        all_files = []
        for file_type in Config.ALLOWED_FILE_TYPES:
            all_files.extend(docs_dir.glob(f"*.{file_type}"))

        if not all_files:
            print(f"\n⚠️  No documents found in {docs_dir}")
            print(f"   Supported formats: {', '.join(Config.ALLOWED_FILE_TYPES)}")
            return

        print(f"\n📚 Found {len(all_files)} document(s)")
        print("\nFiles to upload:")
        for i, file in enumerate(all_files, 1):
            file_size = file.stat().st_size / 1024  # KB
            print(f"   {i}. {file.name} ({file_size:.1f} KB)")

        # Confirm upload
        print("\n" + "-"*60)
        response = input("Proceed with upload? (yes/no): ")
        if response.lower() != 'yes':
            print("Upload cancelled.")
            return

        # Upload each file
        print("\n" + "="*60)
        print("UPLOADING DOCUMENTS")
        print("="*60)

        success_count = 0
        for file in all_files:
            if upload_document(file, search_service):
                success_count += 1

        # Summary
        print("\n" + "="*60)
        print("📊 UPLOAD SUMMARY")
        print("="*60)
        print(f"   Total files: {len(all_files)}")
        print(f"   Successful: {success_count}")
        print(f"   Failed: {len(all_files) - success_count}")

        # Show index stats
        total_docs = search_service.get_document_count()
        print(f"\n   Total documents in index: {total_docs}")

        print("\n✅ Upload process completed!")

    except Exception as e:
        logger.error(f"Upload process failed: {e}")
        print(f"\n❌ Upload process failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()