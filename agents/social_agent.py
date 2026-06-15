import os
import pandas as pd
import joblib

def social_agent():
    print("Running Social Analytics Agent...")
    
    datasets_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(datasets_dir, "Social Medis Data.csv")
    model_path = os.path.join(datasets_dir, "saved_models", "social_model.joblib")
    
    if not os.path.exists(data_path):
        return [{"agent": "Social Analytics Agent", "recommendation": "Social media dataset not found.", "priority": "High", "data_point": "N/A"}]
        
    df = pd.read_csv(data_path)
    
    # Load model
    if not os.path.exists(model_path):
        print("Social model not found, auto-training...")
        from models.social_analytics import train_social_model
        model = train_social_model()
    else:
        model = joblib.load(model_path)
        
    recommendations = []
    
    # Analyze Engagement
    avg_engagement_rate = df['Engagement_Rate'].mean()
    
    # Group by App
    app_engagement = df.groupby('App')['Engagement_Rate'].mean()
    app_time = df.groupby('App')['Daily_Minutes_Spent'].mean()
    
    # 1. App with lowest engagement
    low_engage_app = app_engagement.idxmin()
    low_engage_val = app_engagement.min()
    recommendations.append({
        "agent": "Social Analytics Agent",
        "recommendation": f"App ID {low_engage_app} shows critically low user engagement rate. Diversify content styles (e.g. short-form video, stories) and review user demographics on this platform.",
        "priority": "High" if low_engage_val < avg_engagement_rate * 0.8 else "Medium",
        "data_point": f"App ID: {low_engage_app}, Engagement Rate: {low_engage_val:.2f} (Avg: {avg_engagement_rate:.2f})"
    })
    
    # 2. High time spent but low engagement
    # That represents an opportunity!
    for app in app_engagement.index:
        time_spent = app_time[app]
        engage = app_engagement[app]
        if time_spent > df['Daily_Minutes_Spent'].median() and engage < avg_engagement_rate:
            recommendations.append({
                "agent": "Social Analytics Agent",
                "recommendation": f"Users spend significant daily minutes on App ID {app} but engagement rate is below average. Launch interactive polls, surveys, and comment call-to-actions to convert passive scrolling into active participation.",
                "priority": "Medium",
                "data_point": f"App ID: {app}, Daily Minutes: {time_spent:.2f}, Engagement: {engage:.2f}"
            })
            
    return recommendations
