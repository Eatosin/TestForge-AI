import numpy as np
from loguru import logger

class AnomalyDetector:
    """
    The 'Sentinel' Physics Engine.
    Uses Z-Score Statistical Analysis to detect outliers in test data.
    Ported from the Sentinel MLOps project.
    """
    
    def __init__(self, threshold: float = 2.5):
        self.threshold = threshold
        # We don't use a rolling window here because we analyze a batch of requirements at once.
        # But we keep the logic: Mean vs Standard Deviation.

    def detect(self, data_points: list) -> list:
        """
        Input: A list of numbers (e.g., Requirement Complexity Scores).
        Output: A list of booleans (True = Anomaly).
        """
        if not data_points or len(data_points) < 2:
            return [False] * len(data_points)

        # 1. Calculate Physics Metrics
        arr = np.array(data_points)
        mean = np.mean(arr)
        std_dev = np.std(arr)

        if std_dev == 0:
            return [False] * len(arr)

        # 2. Calculate Z-Scores
        z_scores = (arr - mean) / std_dev
        
        # 3. Flag Anomalies
        anomalies = []
        for i, z in enumerate(z_scores):
            is_anomaly = abs(z) > self.threshold
            anomalies.append(is_anomaly)
            
            if is_anomaly:
                logger.warning(f"Sentinel Alert: Data point {data_points[i]} has Z-Score {z:.2f} (Threshold: {self.threshold})")
        
        return anomalies
