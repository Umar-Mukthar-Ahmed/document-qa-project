import os
from openai import OpenAI
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("🚀 INITIALIZING DOCUMENT Q&A SYSTEM")
print("=" * 60)

# Initialize OpenAI client
openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
print("✅ OpenAI API connected")

# Initialize Azure Search client
search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX_NAME", "documents-index"),
    credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_API_KEY"))
)
print("✅ Azure AI Search connected")
print("=" * 60)


def create_prompt(context, question):
    """
    Create a structured prompt that enforces grounded answers

    This is YOUR responsibility as the system designer:
    - Define what the AI can and cannot do
    - Set clear boundaries
    - Enforce safety constraints
    """
    prompt = f"""You are a helpful assistant that answers questions based ONLY on the provided company documents.

**STRICT RULES:**
1. Answer ONLY using information from the CONTEXT below
2. If the answer is not in the CONTEXT, you MUST say: "Not found in the documents"
3. Do not make up information or use external knowledge
4. Be concise and accurate
5. Quote relevant parts when helpful

**CONTEXT:**
{context}

**QUESTION:**
{question}

**ANSWER:**"""

    return prompt


def search_documents(question):
    """
    Search Azure AI Search for relevant document chunks

    This demonstrates the enterprise approach:
    - Documents are indexed and searchable
    - Not just dumping entire PDFs to the AI
    - Efficient and scalable
    """
    print(f"\n🔍 Searching documents for: '{question}'")

    try:
        # Search for top 3 most relevant chunks
        results = search_client.search(
            search_text=question,
            top=3,
            select=["content", "source"]
        )

        # Combine results into context
        context_parts = []
        sources = set()

        for result in results:
            context_parts.append(result['content'])
            sources.add(result['source'])

        if context_parts:
            context = "\n\n".join(context_parts)
            print(f"✅ Found relevant content from: {', '.join(sources)}")
            return context
        else:
            print("⚠️  No relevant documents found")
            return "No relevant documents found."

    except Exception as e:
        print(f"❌ Error searching documents: {e}")
        return f"Error searching documents: {str(e)}"


def get_answer(question):
    """
    Main function: Search docs → Create prompt → Get AI answer

    This is the complete flow:
    1. Search for relevant context (Azure AI Search)
    2. Build constrained prompt (Your design)
    3. Get answer from AI (OpenAI API)
    4. Return grounded response
    """

    # Step 1: Search for relevant context
    context = search_documents(question)

    # Handle search errors
    if "Error" in context or "No relevant documents" in context:
        return "I couldn't find relevant information in the documents to answer your question."

    # Step 2: Create the prompt with constraints
    prompt = create_prompt(context, question)

    # Step 3: Send to OpenAI
    print("🤖 Generating answer...")
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful document assistant. You ONLY answer based on provided context."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=500,
            temperature=0.2  # Low temperature = more focused, less creative
        )

        answer = response.choices[0].message.content
        print("✅ Answer generated")
        return answer

    except Exception as e:
        print(f"❌ Error getting answer: {e}")
        return f"Error generating answer: {str(e)}"


def run_test_questions():
    """Run a set of test questions to demonstrate the system"""

    test_questions = [
        "How many days before should I request leave?",
        "How many sick leave days do I get per year?",
        "Can I carry forward unused annual leave?",
        "What time should I arrive at work?",
        "What is the CEO's salary?",  # This should return "not found"
        "How much is the gym membership reimbursement?"
    ]

    print("\n" + "=" * 60)
    print("🧪 RUNNING TEST QUESTIONS")
    print("=" * 60)

    for i, question in enumerate(test_questions, 1):
        print(f"\n--- Test {i} ---")
        print(f"❓ Question: {question}")
        answer = get_answer(question)
        print(f"\n💡 Answer: {answer}")
        print("-" * 60)
        input("\nPress Enter to continue to next question...")


def interactive_mode():
    """Interactive Q&A mode"""

    print("\n" + "=" * 60)
    print("📚 INTERACTIVE DOCUMENT Q&A")
    print("=" * 60)
    print("\nYou can now ask questions about the uploaded documents.")
    print("Type 'quit' or 'exit' to stop.\n")

    while True:
        question = input("❓ Your question: ").strip()

        if question.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break

        if not question:
            print("⚠️  Please enter a question.\n")
            continue

        answer = get_answer(question)
        print(f"\n💡 Answer:\n{answer}\n")
        print("-" * 60)


def main():
    """Main entry point"""

    print("\n" + "=" * 60)
    print("📚 ENTERPRISE DOCUMENT Q&A SYSTEM")
    print("=" * 60)
    print("\nOptions:")
    print("1. Run test questions (demonstrates the system)")
    print("2. Interactive mode (ask your own questions)")
    print("3. Exit")

    while True:
        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":
            run_test_questions()
            break
        elif choice == "2":
            interactive_mode()
            break
        elif choice == "3":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()