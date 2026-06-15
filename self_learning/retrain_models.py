import pandas as pd
import os

def should_retrain():
    # Dynamically resolve absolute path to workspace root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    log_path = os.path.join(root_dir, "feedback_log.csv")

    if not os.path.exists(log_path):
        return False

    try:
        feedback = pd.read_csv(log_path)
    except Exception:
        return False

    if "outcome" not in feedback.columns or feedback.empty:
        return False

    success_rate = (feedback["outcome"] == "success").mean()

    if success_rate < 0.70:
        return True

    return False