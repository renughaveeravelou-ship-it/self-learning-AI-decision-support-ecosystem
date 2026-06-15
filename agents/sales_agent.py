import os
import pandas as pd
import joblib

def sales_agent():
    print("Running Sales Prediction Agent...")
    
    datasets_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(datasets_dir, "Sales Data.csv")
    model_path = os.path.join(datasets_dir, "saved_models", "sales_model.joblib")
    
    if not os.path.exists(data_path):
        return [{"agent": "Sales Prediction Agent", "recommendation": "Sales dataset not found.", "priority": "High", "data_point": "N/A"}]
        
    df = pd.read_csv(data_path)
    
    # Load model
    if not os.path.exists(model_path):
        print("Sales model not found, auto-training...")
        from models.sales_prediction import train_sales_model
        model = train_sales_model()
    else:
        model = joblib.load(model_path)
        
    recommendations = []
    
    # Analyze by category
    cat_profits = df.groupby('category')['profit'].sum()
    cat_costs = df.groupby('category')['cost'].sum()
    cat_sales = df.groupby('category')['order_value_EUR'].sum()
    
    # Analyze by country
    country_profits = df.groupby('country')['profit'].sum()
    
    # 1. Identify low profit category
    min_profit_cat = cat_profits.idxmin()
    min_profit_val = cat_profits.min()
    if min_profit_val < 0:
        recommendations.append({
            "agent": "Sales Prediction Agent",
            "recommendation": f"URGENT: Category {min_profit_cat} is running at a net loss. Optimize production costs or renegotiate supplier contracts.",
            "priority": "High",
            "data_point": f"Category: {min_profit_cat}, Net Profit: {min_profit_val:.2f}"
        })
    else:
        # If no category is negative, pick the least profitable one
        recommendations.append({
            "agent": "Sales Prediction Agent",
            "recommendation": f"Optimize marketing and product pricing for Category {min_profit_cat} to boost its profit margin.",
            "priority": "Medium",
            "data_point": f"Category: {min_profit_cat}, Net Profit: {min_profit_val:.2f}"
        })
        
    # 2. Identify low profit country
    min_profit_country = country_profits.idxmin()
    min_profit_country_val = country_profits.min()
    if min_profit_country_val < 0:
        recommendations.append({
            "agent": "Sales Prediction Agent",
            "recommendation": f"Review logistics, shipping tariffs, and localized marketing in Country Code {min_profit_country} as it is unprofitable.",
            "priority": "High",
            "data_point": f"Country Code: {min_profit_country}, Net Profit: {min_profit_country_val:.2f}"
        })
    else:
        recommendations.append({
            "agent": "Sales Prediction Agent",
            "recommendation": f"Increase sales representative allocation in Country Code {min_profit_country} to capture more market share.",
            "priority": "Low",
            "data_point": f"Country Code: {min_profit_country}, Net Profit: {min_profit_country_val:.2f}"
        })
        
    # 3. High cost to revenue ratio
    for cat in cat_profits.index:
        cost = cat_costs[cat]
        sales = cat_sales[cat]
        ratio = cost / sales if sales != 0 else 0
        # If cost is more than 80% of sales
        if ratio > 0.8:
            recommendations.append({
                "agent": "Sales Prediction Agent",
                "recommendation": f"High expense warning: Category {cat} has a cost-to-sales ratio of {ratio*100:.1f}%. Implement cost controls.",
                "priority": "Medium",
                "data_point": f"Cost: {cost:.2f}, Sales: {sales:.2f}, Ratio: {ratio:.2%}"
            })
            
    return recommendations
