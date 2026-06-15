import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
import joblib
from models.utils import save_metric

try:
    from xgboost import XGBRegressor
    HAS_XGB = True
except ImportError:
    HAS_XGB = False

def train_sales_model():
    print("Training Sales Prediction Model...")
    
    datasets_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(datasets_dir, "Sales Data.csv")
    saved_models_dir = os.path.join(datasets_dir, "saved_models")
    os.makedirs(saved_models_dir, exist_ok=True)
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Sales data not found at: {data_path}")
        
    df = pd.read_csv(data_path)
    
    # Target is profit
    y = df['profit']
    X = df.drop(columns=['profit'])
    
    # If sale_date exists in the dataset, drop it or convert it
    if 'sale_date' in X.columns:
        X = X.drop(columns=['sale_date'])
        
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    if HAS_XGB:
        print("Using XGBoost Regressor for Sales Prediction")
        model = XGBRegressor(n_estimators=100, learning_rate=0.08, max_depth=5, random_state=42)
    else:
        print("Using Random Forest Regressor for Sales Prediction")
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        
    model.fit(X_train, y_train)
    
    # Evaluate
    preds = model.predict(X_test)
    r2 = r2_score(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    print(f"Sales Model Evaluated: R2 = {r2:.4f}, RMSE = {rmse:.4f}")
    
    # Save model
    model_path = os.path.join(saved_models_dir, "sales_model.joblib")
    joblib.dump(model, model_path)
    print(f"Sales prediction model saved to {model_path}")
    
    # Save metrics
    save_metric("sales", {"sales_r2": float(r2), "sales_rmse": float(rmse)})
    
    return model
