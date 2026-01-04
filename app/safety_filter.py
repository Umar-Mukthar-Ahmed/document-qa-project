"""
Safety filter to block inappropriate questions and ensure responsible AI usage
This is YOUR responsibility as the system designer
"""

from app.logger import logger
from app.config import Config


class SafetyFilter:
    """Content safety and filtering system"""

    # Blocked keywords (expand this list as needed)
    BLOCKED_KEYWORDS = [
        "hack", "exploit", "bypass", "jailbreak",
        "bomb", "weapon", "illegal",
        # Add more based on your use case
    ]

    # Inappropriate patterns
    INAPPROPRIATE_PATTERNS = [
        "how to hack",
        "ways to bypass",
        "create fake",
        # Add more patterns
    ]

    @staticmethod
    def is_question_safe(question: str) -> tuple[bool, str]:
        """
        Check if a question is safe to process

        Returns:
            (is_safe, reason)
        """

        if not Config.ENABLE_CONTENT_FILTER:
            return True, "Filter disabled"

        # Check length
        if len(question) > Config.MAX_QUESTION_LENGTH:
            logger.warning(f"Question too long: {len(question)} chars")
            return False, "Question exceeds maximum length"

        # Check if question is empty
        if not question.strip():
            return False, "Question is empty"

        question_lower = question.lower()

        # Check for blocked keywords
        for keyword in SafetyFilter.BLOCKED_KEYWORDS:
            if keyword in question_lower:
                logger.warning(f"Blocked keyword detected: {keyword}")
                return False, f"Question contains inappropriate content"

        # Check for inappropriate patterns
        for pattern in SafetyFilter.INAPPROPRIATE_PATTERNS:
            if pattern in question_lower:
                logger.warning(f"Blocked pattern detected: {pattern}")
                return False, "Question contains inappropriate pattern"

        return True, "Safe"

    @staticmethod
    def sanitize_answer(answer: str) -> str:
        """
        Clean up AI-generated answer before showing to user
        Remove any potential issues
        """

        # Remove any markdown code blocks that might leak prompt
        if "```" in answer:
            answer = answer.replace("```", "")

        # Ensure answer isn't too long (prevent token exhaustion)
        if len(answer) > 2000:
            answer = answer[:2000] + "..."

        return answer.strip()

    @staticmethod
    def is_answer_grounded(answer: str) -> bool:
        """
        Check if answer appears to be grounded in documents
        vs making things up
        """

        # Check for hallucination indicators
        hallucination_phrases = [
            "i think", "probably", "maybe", "i'm not sure",
            "in my opinion", "generally speaking"
        ]

        answer_lower = answer.lower()

        for phrase in hallucination_phrases:
            if phrase in answer_lower:
                logger.warning(f"Potential hallucination detected: {phrase}")
                return False

        return True