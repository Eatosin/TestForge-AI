import numpy as np
import asyncio
from concurrent.futures import ThreadPoolExecutor
from sklearn.ensemble import IsolationForest
from typing import List, Dict, Any
from loguru import logger
from pydantic import BaseModel, Field
from src.ml.anomaly_detection import AnomalyDetector

# --- DATA MODELS ---
class RequirementAnalysis(BaseModel):
    id: str
    text: str
    is_edge_case: bool
    risk_level: str
    complexity_score: float
    risk_sources: List[str]

class EdgeCaseDetector:
    """
    Async Physics-Informed Anomaly Detector.
    Offloads heavy CPU compute to a separate thread pool to keep FastAPI responsive.
    """

    def __init__(self, contamination: float = 0.1):
        self.ml_model = IsolationForest(contamination=contamination, random_state=42)
        self.physics_engine = AnomalyDetector(threshold=2.5)
        self.executor = ThreadPoolExecutor(max_workers=4) # Prevent CPU blocking
        logger.info("ML Engine Initialized: Async IsolationForest + Z-Score")

    def _extract_features(self, requirements: List[Dict]) -> np.ndarray:
        """Internal helper to convert text to vectors."""
        features = []
        for req in requirements:
            text = req.get("text", "")
            features.append([
                len(text),                               # Complexity: Length
                text.count(",") + text.count("and"),     # Complexity: Logic Density
                1 if "must" in text.lower() else 0,      # Strictness
                1 if "user" in text.lower() else 0,      # Interaction
                1 if "error" in text.lower() or "fail" in text.lower() else 0 # Negative path
            ])
        return np.array(features)

    def _analyze_sync(self, requirements: List[Dict]) -> List[RequirementAnalysis]:
        """Synchronous core logic (CPU bound)."""
        if not requirements:
            return []

        # 1. Feature Extraction
        X = self._extract_features(requirements)
        lengths = X[:, 0]

        # 2. Run Models
        ml_predictions = self.ml_model.fit_predict(X)
        physics_anomalies = self.physics_engine.detect(lengths)

        # 3. Synthesize Results into Pydantic Models
        results = []
        for i, req in enumerate(requirements):
            is_ml = ml_predictions[i] == -1
            is_physics = physics_anomalies[i]
            
            sources = []
            if is_ml: sources.append("Statistical_Outlier")
            if is_physics: sources.append("Physics_ZScore_Deviation")

            risk = "NORMAL"
            if is_ml and is_physics: risk = "CRITICAL"
            elif is_ml or is_physics: risk = "HIGH"

            results.append(RequirementAnalysis(
                id=req.get("id", f"REQ_{i}"),
                text=req.get("text", ""),
                is_edge_case=is_ml or is_physics,
                risk_level=risk,
                complexity_score=float(X[i, 0]), # Use length as proxy for complexity
                risk_sources=sources
            ))
            
        return results

    async def analyze_complexity(self, requirements: List[Dict]) -> List[RequirementAnalysis]:
        """
        Async wrapper. Offloads the heavy lifting to a thread pool.
        This ensures the API never freezes while calculating Z-Scores.
        """
        logger.info(f"Analyzing {len(requirements)} requirements for Edge Cases...")
        loop = asyncio.get_running_loop()
        # Run CPU-bound task in executor
        return await loop.run_in_executor(
            self.executor, 
            self._analyze_sync, 
            requirements
        )
