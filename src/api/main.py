
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Dict, Any
from src.core.llm_engine import LLMEngine
from src.ml.edge_case_detector import EdgeCaseDetector
from src.core.code_generator import SeleniumGenerator
from src.api.models import GenerateRequest, TestSuiteResponse, CodeGenRequest, CodeResponse
import uvicorn
import uuid
import os
from loguru import logger

ml_resources: Dict[str, Any] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("⚡ Zeta System Startup...")
    try:
        ml_resources["llm"] = LLMEngine()
        ml_resources["ml"] = EdgeCaseDetector()
        ml_resources["codegen"] = SeleniumGenerator()
        logger.info("✅ Engines Online.")
    except Exception as e:
        logger.critical(f"❌ Startup Failed: {e}")
    yield
    ml_resources.clear()
    logger.info("🛑 System Shutdown.")

app = FastAPI(title="Zeta API", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
async def health_check():
    return {"status": "active", "engines": list(ml_resources.keys())}

@app.post("/generate", response_model=TestSuiteResponse)
async def generate_tests(request: GenerateRequest):
    if "llm" not in ml_resources:
        raise HTTPException(503, "Engines not ready")
    
    try:
        raw_tests = await ml_resources["llm"].generate_test_cases(request.requirements_text)
        for test in raw_tests:
            if "text" not in test:
                test["text"] = f"{test.get('title', '')} {' '.join(test.get('steps', []))}"
            
        analysis_objects = await ml_resources["ml"].analyze_complexity(raw_tests)
        
        # Merge logic
        final_test_cases = []
        for original, analysis in zip(raw_tests, analysis_objects):
            merged = original.copy()
            merged["risk_analysis"] = analysis.model_dump()
            final_test_cases.append(merged)

        return TestSuiteResponse(
            suite_id=str(uuid.uuid4()),
            test_cases=final_test_cases, 
            meta={"source": "Gemini 2.5", "ml_validation": True}
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(500, str(e))

@app.post("/codegen", response_model=CodeResponse)
async def generate_code(request: CodeGenRequest):
    try:
        code = ml_resources["codegen"].generate_test_script(request.test_plan)
        return CodeResponse(filename=f"test_{uuid.uuid4().hex[:8]}.py", python_code=code)
    except Exception as e:
        raise HTTPException(500, str(e))

if __name__ == "__main__":
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
