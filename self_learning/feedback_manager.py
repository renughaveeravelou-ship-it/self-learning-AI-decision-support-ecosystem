import pandas as pd
import os

def save_feedback(recommendation, outcome):
    # Dynamically resolve absolute path to workspace root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    log_path = os.path.join(root_dir, "feedback_log.csv")

    feedback = pd.DataFrame([{
        "recommendation": recommendation,
        "outcome": outcome
    }])

    # Check if header needs to be written
    write_header = not os.path.exists(log_path) or os.path.getsize(log_path) == 0

    feedback.to_csv(
        log_path,
        mode="a",
        index=False,
        header=write_header
    )