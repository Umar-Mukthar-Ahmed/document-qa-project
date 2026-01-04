"""
Setup script to initialize Azure AI Search index
Run this once before using the system
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.search_service import AzureSearchService
from app.logger import logger


def main():
    """Initialize the search index"""

    print("=" * 60)
    print("🔧 AZURE AI SEARCH INDEX SETUP")
    print("=" * 60)

    try:
        # Initialize search service
        search_service = AzureSearchService()

        # Check if index exists
        if search_service.index_exists():
            print("\n⚠️  Index already exists!")
            response = input("Do you want to recreate it? (yes/no): ")
            if response.lower() != 'yes':
                print("Setup cancelled.")
                return

        # Create index
        print("\n📋 Creating search index...")
        search_service.create_index()

        print("\n✅ Index setup completed successfully!")
        print(f"   Index name: {search_service.index_name}")
        print(f"   Endpoint: {search_service.endpoint}")

        print("\n🎉 You can now upload documents!")

    except Exception as e:
        logger.error(f"Setup failed: {e}")
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()