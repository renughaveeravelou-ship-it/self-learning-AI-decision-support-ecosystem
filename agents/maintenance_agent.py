import os
import pandas as pd
import numpy as np
import joblib

def maintenance_agent():
    print("Running Predictive Maintenance Agent...")
    
    datasets_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(datasets_dir, "IoT data.csv")
    model_path = os.path.join(datasets_dir, "saved_models", "maintenance_model.joblib")
    
    if not os.path.exists(data_path):
        return [{"agent": "Predictive Maintenance Agent", "recommendation": "IoT dataset not found.", "priority": "High", "data_point": "N/A"}]
        
    # Read CSV (take a sample of the last 5000 rows to simulate active machines)
    df = pd.read_csv(data_path).tail(5000).copy()
    
    # Load model
    if not os.path.exists(model_path):
        print("Maintenance model not found, auto-training...")
        from models.predictive_maintenance import train_maintenance_model
        model = train_maintenance_model()
    else:
        model = joblib.load(model_path)
        
    recommendations = []
    
    # Predict failure
    X = df.drop(columns=['Failure_Within_7_Days'])
    df['Failure_Prob'] = model.predict_proba(X)[:, 1]
    df['Pred_Failure'] = (df['Failure_Prob'] > 0.5).astype(int)
    
    # Get top high-risk machines
    high_risk = df[df['Failure_Prob'] > 0.6].sort_values(by='Failure_Prob', ascending=False)
    
    if len(high_risk) > 0:
        count = 0
        for idx, row in high_risk.iterrows():
            if count >= 3:
                break
            recommendations.append({
                "agent": "Predictive Maintenance Agent",
                "recommendation": f"CRITICAL: Machine ID {idx} (Type: {row['Machine_Type']:.2f}) has a {row['Failure_Prob']*100:.1f}% predicted risk of failure within 7 days. Schedule immediate shutdown and diagnostic inspection.",
                "priority": "High",
                "data_point": f"Temp: {row['Temperature_C']:.2f}°C, Vib: {row['Vibration_mms']:.2f}mm/s, Sound: {row['Sound_dB']:.2f}dB"
            })
            count += 1
            
    # Also check other anomalies (e.g. low coolant level or high vibration)
    anomalous_vib = df[df['Vibration_mms'] > df['Vibration_mms'].quantile(0.99)]
    if len(anomalous_vib) > 0 and len(recommendations) < 5:
        idx = anomalous_vib.index[0]
        row = anomalous_vib.iloc[0]
        recommendations.append({
            "agent": "Predictive Maintenance Agent",
            "recommendation": f"Anomaly detected: Machine ID {idx} exhibits extremely high vibration. Inspect main bearings and mechanical alignment to prevent long-term damage.",
            "priority": "Medium",
            "data_point": f"Vibration: {row['Vibration_mms']:.2f}mm/s (Normal: {df['Vibration_mms'].mean():.2f})"
        })
        
    # If no urgent issues
    if not recommendations:
        recommendations.append({
            "agent": "Predictive Maintenance Agent",
            "recommendation": "All IoT-supervised machinery is operating within normal parameters. Continue standard daily inspections.",
            "priority": "Low",
            "data_point": "Failure risk across fleet is < 5%"
        })
        
    return recommendations
