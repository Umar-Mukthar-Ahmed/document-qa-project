"""
OpenAI API service wrapper
Handles all AI model interactions with proper error handling
"""

from openai import OpenAI
from typing import Dict, List
from app.config import Config
from app.logger import logger
from app.safety_filter import SafetyFilter


class AIService:
    """OpenAI service manager"""

    def __init__(self):
        """Initialize OpenAI client"""
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL
        logger.info(f"AI Service initialized with model: {self.model}")

    def create_prompt(self, context: str, question: str) -> str:
        """
        Create structured prompt with safety constraints
        This is YOUR design - the AI follows YOUR rules
        """

        prompt = f"""You are a helpful enterprise document assistant. You answer questions based ONLY on the provided company documents.

**STRICT RULES YOU MUST FOLLOW:**
1. Answer ONLY using information from the CONTEXT below
2. If the answer is not in the CONTEXT, you MUST respond: "I cannot find this information in the available documents."
3. Do not use external knowledge or make assumptions
4. Be concise, accurate, and professional
5. If relevant, quote specific parts from the context
6. Never make up information or hallucinate facts

**CONTEXT FROM COMPANY DOCUMENTS:**
{context}

**EMPLOYEE QUESTION:**
{question}

**YOUR ANSWER:**"""

        return prompt

    def generate_answer(self, question: str, context: str) -> Dict:
        """
        Generate answer from AI model

        Returns:
            {
                'answer': str,
                'safe': bool,
                'grounded': bool,
                'error': str or None
            }
        """

        # Safety check on question
        is_safe, reason = SafetyFilter.is_question_safe(question)
        if not is_safe:
            logger.warning(f"Unsafe question blocked: {reason}")
            return {
                'answer': f"I cannot process this question: {reason}",
                'safe': False,
                'grounded': False,
                'error': reason
            }

        # Create prompt
        prompt = self.create_prompt(context, question)

        try:
            logger.debug(f"Generating answer for question: {question[:50]}...")

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful enterprise document assistant. You ONLY answer based on provided context and never make up information."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=Config.AI_MAX_TOKENS,
                temperature=Config.AI_TEMPERATURE,
                top_p=0.9,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )

            # Extract answer
            answer = response.choices[0].message.content.strip()

            # Sanitize answer
            answer = SafetyFilter.sanitize_answer(answer)

            # Check if answer is grounded
            is_grounded = SafetyFilter.is_answer_grounded(answer)

            logger.info(f"Answer generated successfully (grounded: {is_grounded})")

            return {
                'answer': answer,
                'safe': True,
                'grounded': is_grounded,
                'error': None,
                'tokens_used': response.usage.total_tokens
            }

        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return {
                'answer': "I encountered an error while processing your question. Please try again.",
                'safe': True,
                'grounded': False,
                'error': str(e)
            }

    def test_connection(self) -> bool:
        """Test if AI service is working"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            logger.info("AI service connection test successful")
            return True
        except Exception as e:
            logger.error(f"AI service connection test failed: {e}")
            return False