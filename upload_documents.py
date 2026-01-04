import os
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchFieldDataType
)
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("="*60)
print("📤 UPLOADING DOCUMENTS TO AZURE AI SEARCH")
print("="*60)

# Get credentials from environment
endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
api_key = os.getenv("AZURE_SEARCH_API_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "documents-index")

print(f"\n🔗 Connecting to: {endpoint}")
print(f"📇 Index name: {index_name}")

# Initialize index client
index_client = SearchIndexClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(api_key)
)

# Define the search index schema
fields = [
    SimpleField(
        name="id",
        type=SearchFieldDataType.String,
        key=True,
        filterable=True
    ),
    SearchableField(
        name="content",
        type=SearchFieldDataType.String,
        searchable=True
    ),
    SimpleField(
        name="source",
        type=SearchFieldDataType.String,
        filterable=True
    )
]

index = SearchIndex(name=index_name, fields=fields)

# Create or update the index
try:
    result = index_client.create_or_update_index(index)
    print(f"\n✅ Index '{index_name}' created/updated successfully!")
except Exception as e:
    print(f"\n❌ Error creating index: {e}")
    exit(1)

# Initialize search client for uploading documents
search_client = SearchClient(
    endpoint=endpoint,
    index_name=index_name,
    credential=AzureKeyCredential(api_key)
)

# Read the sample policy document
doc_path = "documents/sample_policy.txt"

try:
    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"\n📄 Read document: {doc_path}")
    print(f"   Length: {len(content)} characters")
except FileNotFoundError:
    print(f"\n❌ Error: File not found at {doc_path}")
    print("   Please create the file first!")
    exit(1)

# Prepare document for upload
documents = [{
    "id": "doc-001",
    "content": content,
    "source": "Employee Handbook 2024"
}]

# Upload to Azure Search
try:
    result = search_client.upload_documents(documents=documents)
    print(f"\n✅ Successfully uploaded {len(documents)} document(s)!")
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE! You can now run main.py")
    print("="*60)
except Exception as e:
    print(f"\n❌ Error uploading documents: {e}")
    exit(1)