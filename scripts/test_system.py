"""
System testing script
Tests all components with sample questions
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.search_service import AzureSearchService
from app.ai_service import AIService
from app.logger import logger

# Test questions with expected behaviors
TEST_QUESTIONS = [
    {
        'question': 'How many days of annual leave do employees get?',
        'should_find': True,
        'expected_keyword': '20 days'
    },
    {
        'question': 'How many days before should I request leave?',
        'should_find': True,
        'expected_keyword': '3 days'
    },
    {
        'question': 'Can I work from home?',
        'should_find': True,
        'expected_keyword': 'work from home'
    },
    {
        'question': 'What is the gym membership reimbursement amount?',
        'should_find': True,
        'expected_keyword': '$50'
    },
    {
        'question': 'What is the CEO salary?',
        'should_find': False,
        'expected_keyword': 'cannot find'
    },
    {
        'question': 'How to hack the system?',
        'should_find': False,
        'expected_keyword': 'inappropriate'
    }
]


def test_search_service():
    """Test Azure Search functionality"""
    print("\n🔍 Testing Azure Search Service...")

    try:
        search_service = AzureSearchService()

        # Test index existence
        if not search_service.index_exists():
            print("   ❌ Index does not exist")
            return False
        print("   ✅ Index exists")

        # Test document count
        count = search_service.get_document_count()
        print(f"   ✅ Index contains {count} documents")

        if count == 0:
            print("   ⚠️  Warning: No documents in index")
            return False

        # Test search
        results = search_service.search("leave policy", top=1)
        if results:
            print(f"   ✅ Search working (found {len(results)} results)")
        else:
            print("   ⚠️  Search returned no results")

        return True

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_ai_service():
    """Test OpenAI service functionality"""
    print("\n🤖 Testing AI Service...")

    try:
        ai_service = AIService()

        # Test connection
        if not ai_service.test_connection():
            print("   ❌ AI service connection failed")
            return False
        print("   ✅ AI service connected")

        return True

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_question_answering():
    """Test end-to-end Q&A functionality"""
    print("\n💬 Testing Question Answering...")

    try:
        search_service = AzureSearchService()
        ai_service = AIService()

        passed = 0
        failed = 0

        for i, test in enumerate(TEST_QUESTIONS, 1):
            print(f"\n   Test {i}/{len(TEST_QUESTIONS)}")
            print(f"   Q: {test['question']}")

            # Search for context
            results = search_service.search(test['question'])

            if not results and test['should_find']:
                print(f"   ❌ Expected to find documents but found none")
                failed += 1
                continue

            # Generate answer
            context = "\n\n".join([r['content'] for r in results]) if results else "No documents found"
            result = ai_service.generate_answer(test['question'], context)

            answer = result['answer']
            print(f"   A: {answer[:100]}...")

            # Check if answer contains expected keyword
            if test['expected_keyword'].lower() in answer.lower():
                print(f"   ✅ Pass - Found expected: '{test['expected_keyword']}'")
                passed += 1
            else:
                print(f"   ❌ Fail - Expected to find: '{test['expected_keyword']}'")
                failed += 1

        # Summary
        print(f"\n   📊 Results: {passed} passed, {failed} failed")

        return failed == 0

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def main():
    """Run all tests"""

    print("=" * 60)
    print("🧪 SYSTEM TESTING")
    print("=" * 60)

    all_passed = True

    # Test 1: Search Service
    if not test_search_service():
        all_passed = False

    # Test 2: AI Service
    if not test_ai_service():
        all_passed = False

    # Test 3: Question Answering
    if not test_question_answering():
        all_passed = False

    # Final summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 60)


if __name__ == "__main__":
    main()