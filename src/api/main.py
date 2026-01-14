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

# --- LIFESPAN MANAGER ---
# FIX: Explicitly type this as Dict[str, Any] so Mypy allows different objects
ml_resources: Dict[str, Any] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(" System Startup: Loading AI Engines...")
    try:
        ml_resources["llm"] = LLMEngine()
        ml_resources["ml"] = EdgeCaseDetector()
        ml_resources["codegen"] = SeleniumGenerator()
        logger.info(" Engines Online.")
    except Exception as e:
        logger.critical(f" Engine Startup Failed: {e}")
        raise e
    yield
    ml_resources.clear()
    logger.info("🛑 System Shutdown.")

# --- APP CONFIG ---
app = FastAPI(
    title="TestForge AI API",
    version="1.0.0",
    lifespan=lifespan
)

# Security: CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {
        "status": "active", 
        "engines_loaded": list(ml_resources.keys())
    }

@app.post("/generate", response_model=TestSuiteResponse)
async def generate_tests(request: GenerateRequest):
    logger.info(f"Processing generation request ({len(request.requirements_text)} chars)")
    
    if "llm" not in ml_resources:
        raise HTTPException(status_code=503, detail="AI Engines not ready")

    try:
        # 1. Generate Raw Tests
        # Type ignore helps Mypy know we trust the type here
        llm_engine: LLMEngine = ml_resources["llm"] 
        raw_tests = await llm_engine.generate_test_cases(request.requirements_text)
        
        # 2. Apply Physics/ML Analysis
        for test in raw_tests:
            if "text" not in test:
                test["text"] = f"{test.get('title', '')} {' '.join(test.get('steps', []))}"
            
        ml_engine: EdgeCaseDetector = ml_resources["ml"]
        analyzed_tests = await ml_engine.analyze_complexity(raw_tests)
        
        return TestSuiteResponse(
            suite_id=str(uuid.uuid4()),
            test_cases=analyzed_tests,
            meta={"source": "Gemini 2.5", "ml_validation": True}
        )
        
    except Exception as e:
        logger.error(f"Generation logic failed: {e}")
        raise HTTPException(status_code=500, detail="Internal processing error")

@app.post("/codegen", response_model=CodeResponse)
async def generate_code(request: CodeGenRequest):
    if "codegen" not in ml_resources:
        raise HTTPException(status_code=503, detail="Codegen Engine not ready")
        
    try:
        codegen_engine: SeleniumGenerator = ml_resources["codegen"]
        code = codegen_engine.generate_test_script(request.test_plan)
        return CodeResponse(
            filename=f"test_{uuid.uuid4().hex[:8]}.py",
            python_code=code
        )
    except Exception as e:
        logger.error(f"Codegen failed: {e}")
        raise HTTPException(status_code=500, detail="Code generation failed")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=port, reload=True)
