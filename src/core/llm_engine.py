import os
import json
import yaml
from pathlib import Path
from typing import List, Dict, Any
import google.generativeai as genai
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from dotenv import load_dotenv

# Load Env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    logger.critical("GEMINI_API_KEY is missing")
    raise ValueError("GEMINI_API_KEY not found in environment")

genai.configure(api_key=API_KEY)

class LLMEngine:
    """
    LLM Engine with Externalized Configuration.
    Loads prompts from config/prompts.yaml to ensure code/data separation.
    """

    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
        self.prompts = self._load_prompts()
        logger.info(f"LLM Engine initialized with {model_name}")

    def _load_prompts(self) -> Dict[str, Any]:
        """Loads prompt templates from the config directory."""
        # Resolves path relative to this file: src/core/../../config/prompts.yaml
        base_path = Path(__file__).resolve().parent.parent.parent
        config_path = base_path / "config" / "prompts.yaml"
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found at: {config_path}")
            
        with open(config_path, "r") as f:
            return yaml.safe_load(f)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    async def generate_test_cases(self, requirements_text: str) -> List[Dict[str, Any]]:
        logger.debug("Constructing prompt from configuration...")
        
        try:
            # Construct prompt from YAML templates
            config = self.prompts["test_generation"]
            system_role = config["system_role"]
            instruction = config["instruction"].format(requirements_text=requirements_text[:30000])
            fmt = config["output_format"]
            
            full_prompt = f"{system_role}\n\n{instruction}\n\nOUTPUT FORMAT:\n{fmt}"

            # Async call
            response = await self.model.generate_content_async(full_prompt)
            return self._parse_json_response(response.text)
            
        except KeyError as e:
            logger.error(f"Missing configuration key in prompts.yaml: {e}")
            raise e
        except Exception as e:
            logger.error(f"LLM Generation Failed: {e}")
            raise e

    def _parse_json_response(self, text: str) -> List[Dict[str, Any]]:
        clean_text = text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:-3]
        elif clean_text.startswith("```"):
            clean_text = clean_text[3:-3]
            
        try:
            data = json.loads(clean_text)
            if not isinstance(data, list):
                raise ValueError("Output is not a list of test cases")
            return data
        except json.JSONDecodeError as e:
            logger.error("Failed to decode JSON response")
            raise ValueError(f"Malformed JSON from LLM: {e}")
