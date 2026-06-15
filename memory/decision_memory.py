import pandas as pd
import os
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(current_dir, "decision_history.csv")

def save_decision(
        decision,
        outcome,
        confidence):

    record = pd.DataFrame([{
        "timestamp":
            datetime.now(),

        "decision":
            decision,

        "outcome":
            outcome,

        "confidence":
            confidence
    }])

    if os.path.exists(FILE_PATH):

        record.to_csv(
            FILE_PATH,
            mode="a",
            header=False,
            index=False
        )

    else:

        record.to_csv(
            FILE_PATH,
            index=False
        )

def get_decision_history():

    if os.path.exists(FILE_PATH):

        return pd.read_csv(FILE_PATH)

    return pd.DataFrame()