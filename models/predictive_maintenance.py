import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
import joblib
from models.utils import save_metric

try:
    from xgboost import XGBClassifier
    HAS_XGB = True
except ImportError:
    HAS_XGB = False

def train_maintenance_model():
    print("Training Predictive Maintenance Model (IoT)...")
    
    datasets_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(datasets_dir, "IoT data.csv")
    saved_models_dir = os.path.join(datasets_dir, "saved_models")
    os.makedirs(saved_models_dir, exist_ok=True)
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"IoT data not found at: {data_path}")
        
    # Read CSV
    df = pd.read_csv(data_path)
    
    # Target is Failure_Within_7_Days
    df['Failure_Within_7_Days'] = df['Failure_Within_7_Days'].astype(int)
    y = df['Failure_Within_7_Days']
    X = df.drop(columns=['Failure_Within_7_Days'])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    if HAS_XGB:
        print("Using XGBoost Classifier for Predictive Maintenance")
        model = XGBClassifier(n_estimators=50, max_depth=5, learning_rate=0.1, random_state=42)
    else:
        print("Using Random Forest Classifier for Predictive Maintenance")
        model = RandomForestClassifier(n_estimators=30, random_state=42, n_jobs=-1)
        
    model.fit(X_train, y_train)
    
    # Evaluate
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]
    acc = accuracy_score(y_test, preds)
    auc = roc_auc_score(y_test, probs)
    print(f"Maintenance Model Evaluated: Accuracy = {acc:.4f}, AUC = {auc:.4f}")
    
    # Save model
    model_path = os.path.join(saved_models_dir, "maintenance_model.joblib")
    joblib.dump(model, model_path)
    print(f"Maintenance model saved to {model_path}")
    
    # Save metrics
    save_metric("maintenance", {"maintenance_accuracy": float(acc), "maintenance_auc": float(auc)})
    
    return model
