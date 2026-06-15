import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
import joblib
from models.utils import save_metric

def train_social_model():
    print("Training Social Analytics Model...")
    
    datasets_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(datasets_dir, "Social Medis Data.csv")
    saved_models_dir = os.path.join(datasets_dir, "saved_models")
    os.makedirs(saved_models_dir, exist_ok=True)
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Social media data not found at: {data_path}")
        
    df = pd.read_csv(data_path)
    
    # Target is Engagement_Rate
    y = df['Engagement_Rate']
    X = df.drop(columns=['Engagement_Rate'])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    preds = model.predict(X_test)
    r2 = r2_score(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    print(f"Social Model Evaluated: R2 = {r2:.4f}, RMSE = {rmse:.4f}")
    
    # Save
    model_path = os.path.join(saved_models_dir, "social_model.joblib")
    joblib.dump(model, model_path)
    print(f"Social model saved to {model_path}")
    
    # Save metrics
    save_metric("social", {"social_r2": float(r2), "social_rmse": float(rmse)})
    
    return model
