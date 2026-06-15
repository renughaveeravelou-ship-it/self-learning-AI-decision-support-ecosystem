import os
import json
import numpy as np

def save_metric(model_name, metrics_dict):
    """
    Update saved_models/metrics.json with new metrics from a specific model.
    """
    datasets_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    saved_models_dir = os.path.join(datasets_dir, "saved_models")
    os.makedirs(saved_models_dir, exist_ok=True)
    metrics_path = os.path.join(saved_models_dir, "metrics.json")
    
    current_metrics = {}
    if os.path.exists(metrics_path):
        try:
            with open(metrics_path, "r") as f:
                current_metrics = json.load(f)
        except Exception:
            pass
            
    # Update metrics
    for k, v in metrics_dict.items():
        if isinstance(v, (int, float, np.float32, np.float64, np.integer)):
            current_metrics[k] = float(v)
        else:
            current_metrics[k] = v
        
    with open(metrics_path, "w") as f:
        json.dump(current_metrics, f, indent=4)
    print(f"Metrics saved for {model_name}: {metrics_dict}")
