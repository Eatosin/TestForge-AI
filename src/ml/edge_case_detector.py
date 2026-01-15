
import numpy as np
import asyncio
from concurrent.futures import ThreadPoolExecutor
from sklearn.ensemble import IsolationForest
from typing import List, Dict
from loguru import logger
from pydantic import BaseModel
from src.ml.anomaly_detection import AnomalyDetector

class RequirementAnalysis(BaseModel):
    id: str
    text: str
    is_edge_case: bool
    risk_level: str
    complexity_score: float
    risk_sources: List[str]

class EdgeCaseDetector:
    def __init__(self, contamination: float = 0.1):
        self.ml_model = IsolationForest(contamination=contamination, random_state=42)
        self.physics_engine = AnomalyDetector(threshold=2.5)
        self.executor = ThreadPoolExecutor(max_workers=4)

    def _extract_features(self, requirements: List[Dict]) -> np.ndarray:
        features = []
        for req in requirements:
            text = req.get("text", "")
            features.append([
                len(text),
                text.count(",") + text.count("and"),
                1 if "must" in text.lower() else 0,
                1 if "user" in text.lower() else 0,
                1 if "error" in text.lower() else 0
            ])
        return np.array(features, dtype=float)

    def _sanitize(self, value):
        if hasattr(value, "item"):
            return value.item()
        if isinstance(value, list) and len(value) == 1:
            return value[0]
        return value

    def _analyze_sync(self, requirements: List[Dict]) -> List[RequirementAnalysis]:
        if not requirements:
            return []
        try:
            X = self._extract_features(requirements)
            ml_predictions = self.ml_model.fit_predict(X).tolist()
            physics_anomalies = self.physics_engine.detect(X[:, 0].tolist())

            results = []
            for i, req in enumerate(requirements):
                is_ml = (ml_predictions[i] == -1)
                is_phys = bool(physics_anomalies[i])
                
                risk = "NORMAL"
                if is_ml and is_phys:
                    risk = "CRITICAL"
                elif is_ml or is_phys:
                    risk = "HIGH"

                sources = []
                if is_ml:
                    sources.append("Statistical_Outlier")
                if is_phys:
                    sources.append("Physics_ZScore_Deviation")

                results.append(RequirementAnalysis(
                    id=req.get("id", f"REQ_{i}"),
                    text=req.get("text", ""),
                    is_edge_case=is_ml or is_phys,
                    risk_level=risk,
                    complexity_score=float(X[i][0]),
                    risk_sources=sources
                ))
            return results
        except Exception as e:
            logger.error(f"ML Error: {e}")
            return []

    async def analyze_complexity(self, requirements: List[Dict]) -> List[RequirementAnalysis]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, self._analyze_sync, requirements)
