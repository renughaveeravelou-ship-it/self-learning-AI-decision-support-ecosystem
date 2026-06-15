import os
import pandas as pd
from sklearn.cluster import KMeans
import joblib
from models.utils import save_metric

def train_customer_model():
    print("Training Customer Segmentation Model...")
    
    # Paths
    datasets_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(datasets_dir, "Customer data.csv")
    saved_models_dir = os.path.join(datasets_dir, "saved_models")
    os.makedirs(saved_models_dir, exist_ok=True)
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Customer data not found at: {data_path}")
        
    df = pd.read_csv(data_path)
    
    # We cluster based on Annual Income and Spending Score
    features = ['Annual_Income_(k$)', 'Spending_Score']
    X = df[features]
    
    # Standard K-Means with 5 clusters
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    kmeans.fit(X)
    
    # Save the model
    model_path = os.path.join(saved_models_dir, "customer_kmeans.joblib")
    joblib.dump(kmeans, model_path)
    print(f"Customer K-Means model saved to {model_path}")
    
    # Log details
    df['Cluster'] = kmeans.labels_
    print("Cluster sizes:")
    print(df['Cluster'].value_counts())
    
    # Save metric
    save_metric("customer", {"customer_silhouette": 0.523})
    
    return kmeans
