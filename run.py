"""
Main entry point for the Document Q&A system
Provides CLI interface to run different components
"""

import sys
import argparse
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.logger import logger
from app.config import Config


def run_web():
    """Start the web application"""
    from web.app import app

    print("=" * 60)
    print("🌐 STARTING WEB APPLICATION")
    print("=" * 60)
    print(f"Environment: {Config.APP_ENV}")
    print("URL: http://localhost:5000")
    print("=" * 60)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=(Config.APP_ENV == "development"),
    )


def run_cli():
    """Start CLI interface"""
    from app.search_service import AzureSearchService
    from app.ai_service import AIService

    print("=" * 60)
    print("💬 COMMAND LINE INTERFACE")
    print("=" * 60)

    search_service = AzureSearchService()
    ai_service = AIService()

    print("\nType 'quit' to exit\n")

    while True:
        question = input("❓ Your question: ").strip()

        if question.lower() in ["quit", "exit", "q"]:
            print("👋 Goodbye!")
            break

        if not question:
            continue

        # Search
        results = search_service.search(question)

        if not results:
            print("💡 I couldn't find relevant information in the documents.\n")
            continue

        # Generate answer
        context = "\n\n".join([r["content"] for r in results])
        result = ai_service.generate_answer(question, context)

        print(f"\n💡 Answer:\n{result['answer']}\n")
        print("-" * 60)


def main():
    """Main function"""

    parser = argparse.ArgumentParser(
        description="Enterprise Document Q&A System"
    )
    parser.add_argument(
        "mode",
        choices=["web", "cli", "setup", "upload", "test"],
        help="Mode to run: web, cli, setup, upload, or test",
    )

    args = parser.parse_args()

    try:
        if args.mode == "web":
            run_web()
        elif args.mode == "cli":
            run_cli()
        elif args.mode == "setup":
            from scripts.setup_index import main as setup_main

            setup_main()
        elif args.mode == "upload":
            from scripts.upload_documents import main as upload_main

            upload_main()
        elif args.mode == "test":
            from scripts.test_system import main as test_main

            test_main()

    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
