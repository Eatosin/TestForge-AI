from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# --- REQUESTS ---
class GenerateRequest(BaseModel):
    # Security: Limit input size to prevent context window overflow/DoS
    requirements_text: str = Field(..., min_length=10, max_length=50000, description="Raw requirements text")
    context: Optional[str] = Field(None, max_length=5000)

class AnalyzeRequest(BaseModel):
    test_cases: List[Dict[str, Any]] = Field(..., description="Test cases to analyze")

class CodeGenRequest(BaseModel):
    test_plan: Dict[str, Any] = Field(..., description="Single test case object")

# --- RESPONSES ---
class TestSuiteResponse(BaseModel):
    suite_id: str
    test_cases: List[Dict[str, Any]]
    meta: Dict[str, Any]

class CodeResponse(BaseModel):
    filename: str
    python_code: str
