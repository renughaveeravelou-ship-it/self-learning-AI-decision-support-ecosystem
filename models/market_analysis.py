import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, mean_squared_error
import joblib
from models.utils import save_metric

def train_market_model():
    print("Training Market Analysis Model...")
    
    datasets_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(datasets_dir, "market Data.csv")
    saved_models_dir = os.path.join(datasets_dir, "saved_models")
    os.makedirs(saved_models_dir, exist_ok=True)
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Market data not found at: {data_path}")
        
    df = pd.read_csv(data_path)
    
    # Preprocess Weekday
    le = LabelEncoder()
    df['Weekday'] = le.fit_transform(df['Weekday'].astype(str))
    
    # Target is Rating
    y = df['Rating']
    # Select feature columns (excluding Rating)
    X = df.drop(columns=['Rating'])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train regressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    preds = model.predict(X_test)
    r2 = r2_score(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    print(f"Market Model Evaluated: R2 = {r2:.4f}, RMSE = {rmse:.4f}")
    
    # Save model and label encoder
    model_path = os.path.join(saved_models_dir, "market_model.joblib")
    le_path = os.path.join(saved_models_dir, "market_weekday_encoder.joblib")
    
    joblib.dump(model, model_path)
    joblib.dump(le, le_path)
    print(f"Market model saved to {model_path}")
    
    # Save metrics
    save_metric("market", {"market_r2": float(r2), "market_rmse": float(rmse)})
    
    return model
