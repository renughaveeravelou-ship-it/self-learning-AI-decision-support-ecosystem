import os
import pandas as pd
import joblib

def customer_agent():
    print("Running Customer Segmentation Agent...")
    
    datasets_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(datasets_dir, "Customer data.csv")
    model_path = os.path.join(datasets_dir, "saved_models", "customer_kmeans.joblib")
    
    if not os.path.exists(data_path):
        return [{"agent": "Customer Segmentation Agent", "recommendation": "Customer dataset not found.", "priority": "High", "data_point": "N/A"}]
        
    df = pd.read_csv(data_path)
    
    # Load model
    if not os.path.exists(model_path):
        print("Customer model not found, auto-training...")
        from models.customer_segmentation import train_customer_model
        kmeans = train_customer_model()
    else:
        kmeans = joblib.load(model_path)
        
    # Predict clusters
    features = ['Annual_Income_(k$)', 'Spending_Score']
    df['Cluster'] = kmeans.predict(df[features])
    
    # Analyze clusters
    recommendations = []
    
    # Find statistics for each cluster to identify which is which
    cluster_stats = df.groupby('Cluster')[features].mean()
    
    for cluster_id, row in cluster_stats.iterrows():
        income = row['Annual_Income_(k$)']
        spending = row['Spending_Score']
        
        # High Income, Low Spending Score (At risk / High potential)
        if income > 0 and spending < 0:
            recommendations.append({
                "agent": "Customer Segmentation Agent",
                "recommendation": f"Target Cluster {cluster_id} (High Income, Low Spending) with high-end premium campaigns and personalized promotions to unlock purchasing potential.",
                "priority": "High",
                "data_point": f"Average Income: {income:.2f}, Average Spending Score: {spending:.2f}"
            })
        # High Income, High Spending (Loyal/Champions)
        elif income > 0 and spending > 0:
            recommendations.append({
                "agent": "Customer Segmentation Agent",
                "recommendation": f"Reward Cluster {cluster_id} (High Income, High Spending) with VIP perks, early access sales, and dedicated customer support to maintain high loyalty.",
                "priority": "Medium",
                "data_point": f"Average Income: {income:.2f}, Average Spending Score: {spending:.2f}"
            })
        # Low Income, High Spending (Aspirational/Impulsive)
        elif income < 0 and spending > 0:
            recommendations.append({
                "agent": "Customer Segmentation Agent",
                "recommendation": f"Monitor Cluster {cluster_id} (Low Income, High Spending) for credit risk. Focus on low-cost high-volume items and flexible payment plans.",
                "priority": "Medium",
                "data_point": f"Average Income: {income:.2f}, Average Spending Score: {spending:.2f}"
            })
        # Low Income, Low Spending (Frugal/Budget)
        elif income < 0 and spending < 0:
            recommendations.append({
                "agent": "Customer Segmentation Agent",
                "recommendation": f"Target Cluster {cluster_id} (Low Income, Low Spending) with essential goods, entry-level discount campaigns, and budget-friendly bundles.",
                "priority": "Low",
                "data_point": f"Average Income: {income:.2f}, Average Spending Score: {spending:.2f}"
            })
            
    # If no specific rule triggered, add a generic high spending recommendation
    if not recommendations:
        recommendations.append({
            "agent": "Customer Segmentation Agent",
            "recommendation": "Maintain standard marketing campaigns. Gather more demographic variables for fine-grained cluster tuning.",
            "priority": "Low",
            "data_point": "N/A"
        })
        
    return recommendations
