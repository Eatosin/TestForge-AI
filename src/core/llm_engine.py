import os
import json
from typing import List, Dict, Any
import google.generativeai as genai
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from dotenv import load_dotenv

# Load Env
load_dotenv()

# Configure Google AI
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    logger.critical("GEMINI_API_KEY is missing!")
    raise ValueError("GEMINI_API_KEY not found in environment")

genai.configure(api_key=API_KEY)

class LLMEngine:
    """
    Resilient LLM Wrapper for Google Gemini 2.5 Flash.
    Handles retries, rate limits, and structured response parsing.
    """

    def __init__(self, model_name: str = "gemini-2.5-flash"): # Updated to 2026 standard
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
        logger.info(f"LLM Engine initialized with {model_name}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(Exception), # Refine this to catch specific API errors in prod
        reraise=True
    )
    async def generate_test_cases(self, requirements_text: str) -> List[Dict[str, Any]]:
        """
        Generates structured test cases from requirements text.
        Returns a list of JSON objects.
        """
        logger.debug("Generating test cases via LLM...")

        # SOTA Prompt Engineering: Role + Context + Output Constraints
        prompt = f"""
        ROLE: Senior QA Automation Architect.
        TASK: Analyze the software requirements below and generate comprehensive test cases.
        
        REQUIREMENTS:
        {requirements_text[:30000]}  # Truncate to avoid context overflow if needed
        
        INSTRUCTIONS:
        1. Identify Happy Paths (Positive testing).
        2. Identify Edge Cases (Boundary values, Nulls, Invalid inputs).
        3. Identify Security Cases (Injection, Auth).
        
        OUTPUT FORMAT (Strict JSON Array):
        [
            {{
                "id": "TC_001",
                "title": "Test Case Title",
                "type": "Happy Path" | "Edge Case" | "Security",
                "preconditions": "User is logged in",
                "steps": ["Step 1", "Step 2"],
                "expected_result": "Success message shown"
            }}
        ]
        
        Return ONLY the JSON. No markdown.
        """

        try:
            # Async call to Gemini
            response = await self.model.generate_content_async(prompt)
            return self._parse_json_response(response.text)
        except Exception as e:
            logger.error(f"LLM Generation Failed: {e}")
            raise e

    def _parse_json_response(self, text: str) -> List[Dict[str, Any]]:
        """
        Sanitizes and parses the LLM output into a Python List.
        """
        clean_text = text.strip()
        # Remove Markdown formatting if present
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:-3]
        if clean_text.startswith("```"):
            clean_text = clean_text[3:-3]
            
        try:
            data = json.loads(clean_text)
            if not isinstance(data, list):
                raise ValueError("Output is not a list of test cases")
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON: {text[:100]}...")
            raise ValueError(f"Malformed JSON from LLM: {e}")
