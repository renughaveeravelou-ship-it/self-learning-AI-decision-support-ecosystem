import pandas as pd

def detect_drift(
        baseline_accuracy,
        current_accuracy):

    drift = baseline_accuracy - current_accuracy

    if drift > 0.05:

        return {
            "drift_detected": True,
            "drift_score": drift
        }

    return {
        "drift_detected": False,
        "drift_score": drift
    }