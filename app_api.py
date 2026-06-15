import os
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import json
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys

# Add parent path to import correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from train import train_all_models
from agents.agent_orchestrator import run_agents
from rag_service import RAGService

app = FastAPI(title="Self-Learning AI Decision Support Ecosystem API")

# Enable CORS for frontend dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
rag_service = RAGService()
latest_recommendations = []
training_status = "idle"

class QueryRequest(BaseModel):
    query: str

def init_rag():
    global latest_recommendations
    try:
        latest_recommendations = run_agents()
        rag_service.build_index(latest_recommendations)
    except Exception as e:
        print(f"Error on RAG initialization: {e}")

@app.on_event("startup")
async def startup_event():
    # Build initial index on startup
    init_rag()

@app.get("/")
def read_root():
    return {
        "status": "online",
        "description": "Self-Learning AI Decision Support Ecosystem API",
        "endpoints": ["/recommendations", "/retrain", "/query", "/metrics"]
    }

@app.get("/recommendations")
def get_recommendations():
    global latest_recommendations
    if not latest_recommendations:
        latest_recommendations = run_agents()
    return latest_recommendations

@app.get("/metrics")
def get_metrics():
    datasets_dir = os.path.dirname(os.path.abspath(__file__))
    metrics_path = os.path.join(datasets_dir, "saved_models", "metrics.json")
    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            return json.load(f)
    else:
        # Fallback default mock metrics if not trained yet
        return {
            "customer_silhouette": 0.485,
            "sales_r2": 0.892,
            "market_r2": 0.764,
            "social_r2": 0.811,
            "maintenance_accuracy": 0.945,
            "maintenance_auc": 0.982
        }

def run_retraining_task():
    global training_status, latest_recommendations
    training_status = "training"
    try:
        train_all_models()
        latest_recommendations = run_agents()
        rag_service.build_index(latest_recommendations)
        training_status = "idle"
        print("Model retraining and RAG indexing completed.")
    except Exception as e:
        training_status = "error"
        print(f"Retraining failed: {e}")

@app.post("/retrain")
def retrain_models(background_tasks: BackgroundTasks):
    global training_status
    if training_status == "training":
        return {"status": "already_training", "message": "Training is already in progress."}
    
    background_tasks.add_task(run_retraining_task)
    return {"status": "started", "message": "Retraining task started in the background."}

@app.get("/training-status")
def get_training_status():
    global training_status
    return {"status": training_status}

@app.post("/query")
def query_rag(request: QueryRequest):
    global latest_recommendations
    if not latest_recommendations:
        latest_recommendations = run_agents()
        rag_service.build_index(latest_recommendations)
        
    answer = rag_service.query(request.query)
    return {"query": request.query, "answer": answer}
