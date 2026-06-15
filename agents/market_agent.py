import os
import pandas as pd
import joblib

def market_agent():
    print("Running Market Analysis Agent...")
    
    datasets_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(datasets_dir, "market Data.csv")
    model_path = os.path.join(datasets_dir, "saved_models", "market_model.joblib")
    
    if not os.path.exists(data_path):
        return [{"agent": "Market Analysis Agent", "recommendation": "Market dataset not found.", "priority": "High", "data_point": "N/A"}]
        
    df = pd.read_csv(data_path)
    
    # Load model
    if not os.path.exists(model_path):
        print("Market model not found, auto-training...")
        from models.market_analysis import train_market_model
        model = train_market_model()
    else:
        model = joblib.load(model_path)
        
    recommendations = []
    
    # Analyze Ratings
    # Mean rating is usually around 5-10
    avg_rating = df['Rating'].mean()
    
    # Group by Product Line
    prod_ratings = df.groupby('Product line')['Rating'].mean()
    # Group by Branch
    branch_ratings = df.groupby('Branch')['Rating'].mean()
    
    # 1. Product line with low ratings
    low_rating_prod = prod_ratings.idxmin()
    low_rating_prod_val = prod_ratings.min()
    recommendations.append({
        "agent": "Market Analysis Agent",
        "recommendation": f"Product Line {low_rating_prod} is receiving the lowest ratings. Conduct customer feedback surveys or review product quality control.",
        "priority": "High" if low_rating_prod_val < avg_rating * 0.9 else "Medium",
        "data_point": f"Product Line: {low_rating_prod}, Avg Rating: {low_rating_prod_val:.2f} (Global Avg: {avg_rating:.2f})"
    })
    
    # 2. Branch with low ratings
    low_rating_branch = branch_ratings.idxmin()
    low_rating_branch_val = branch_ratings.min()
    recommendations.append({
        "agent": "Market Analysis Agent",
        "recommendation": f"Branch {low_rating_branch} has the lowest satisfaction ratings. Investigate store management, staff customer service, or queue times.",
        "priority": "Medium",
        "data_point": f"Branch: {low_rating_branch}, Avg Rating: {low_rating_branch_val:.2f}"
    })
    
    # 3. High gross income but low rating transactions
    high_value_low_rating = df[(df['gross income'] > df['gross income'].quantile(0.8)) & (df['Rating'] < df['Rating'].quantile(0.2))]
    if len(high_value_low_rating) > 0:
        recommendations.append({
            "agent": "Market Analysis Agent",
            "recommendation": f"Detected {len(high_value_low_rating)} high-value transactions with very low customer satisfaction. Offer post-sale recovery rewards.",
            "priority": "High",
            "data_point": f"High value / Low rating count: {len(high_value_low_rating)}"
        })
        
    return recommendations
