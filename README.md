# Self-Learning AI Decision Support Ecosystem

A state-of-the-art, multi-agent enterprise decision support system that integrates predictive machine learning models, GenAI/LLM-powered agents, Retrieval-Augmented Generation (RAG), and a self-learning loop based on human-in-the-loop feedback.

---

## Key Features

*   **Multi-Agent Collaborative Engine**: Dynamic team of dedicated agents (Sales, Customer, Market, Social, and Maintenance) that collaborate and discuss corporate decisions in real-time.
*   **Self-Learning Feedback Loop**: Real-time feedback monitoring and automated model retraining pipelines to continuously adapt predictions based on decisions and outcomes.
*   **Advanced RAG Integration**: High-performance Retrieval-Augmented Generation using Google Gemini and FAISS vector search for context-aware document and policy querying.
*   **Explainable AI (XAI)**: Native SHAP (SHapley Additive exPlanations) analysis to ensure transparency and trust in all predictive engine results.
*   **Dual Interface Stack**:
    *   **Interactive Streamlit Dashboard**: Sleek, modular control center displaying KPIs, agent discussion spaces, SHAP explanations, drift detection, and RAG assistance.
    *   **FastAPI Backend Service**: High-performance REST APIs for predictions, recommendations, and feedback logging.
*   **Enterprise Monitoring**: Built-in drift detection and detailed audit logging to maintain ecosystem health and compliance.

---

##  Tech Stack

*   **Core Logic**: Python 3.10+, Pandas, NumPy, Joblib
*   **Machine Learning**: Scikit-Learn, XGBoost, TensorFlow
*   **Explainable AI**: SHAP, Matplotlib
*   **Generative AI & RAG**: Google Gemini API (`google-generativeai`), LangChain, FAISS (CPU), Sentence-Transformers
*   **Web Frameworks**: Streamlit (Dashboard), FastAPI & Uvicorn (Backend)
*   **Deployment**: Docker & Docker Compose

---

##  Project Architecture

```
Self-Learning AI Decision Support Ecosystem/
│
├── agents/                  # Multi-agent orchestrators & individual agent roles
│   ├── customer_agent.py    # Segmentation analysis agent
│   ├── sales_agent.py       # Revenue/demand forecasting agent
│   ├── market_agent.py      # Trend analysis agent
│   ├── social_agent.py      # Sentiment analysis agent
│   ├── maintenance_agent.py # IoT/Predictive maintenance agent
│   └── agent_orchestrator.py# Coordinates multi-agent team discussions
│
├── analytics/               # Metrics, KPIs, and decision scoring
├── api/                     # FastAPI backend application, routes, and schemas
├── auth/                    # Role-based access control (RBAC) and authentication
├── collaboration/           # Agent-to-agent communication layers
├── copilot/                 # GenAI Copilot for executive insights
├── dashboard/               # Streamlit control panels and modular sub-pages
├── decision_engine/         # Core recommendation algorithms
├── drift/                   # Dataset and model performance drift detectors
├── explainability/          # XAI integration utilizing SHAP 
├── llm/                     # Direct connectors to Gemini API
├── memory/                  # Long-term/short-term memory for agent contexts
├── models/                  # ML training and inference logic (XGBoost, KMeans, etc.)
├── monitoring/              # System health, log monitoring, and audit trails
├── rag/                     # Embedding generators and vector databases
├── reporting/               # Automated monthly executive PDF report generation
├── self_learning/           # Logs feedback & handles automated model retraining
│
├── main.py                  # Direct entrypoint to train all models and execute predictions
├── docker-compose.yml       # Production-ready multi-container configuration
├── Dockerfile               # Consolidated container build blueprint
└── requirment.txt           # Main ecosystem dependencies
```

---

## Installation & Configuration

### Prerequisites
- Python 3.10 or 3.11 installed.
- A valid Google Gemini API Key.

### 1. Set Up Environment Variables
Create a `.env` file in the root directory (or export directly to your shell environment):
```bash
GEMINI_API_KEY="your-gemini-api-key-here"
```

### 2. Local Installation
Clone the repository, initialize a virtual environment, and install dependencies:
```bash
# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install required dependencies
pip install -r requirment.txt
```

### 3. Initialize Models & Predictions
Before running the services, train the machine learning models and run the initial prediction pipeline:
```bash
python main.py
```

---

##  Running the Application

You can spin up the ecosystem either locally or using Docker.

### Option A: Local Run (Development)

**Start the FastAPI Backend:**
```bash
uvicorn api.api:app --reload --port 8000
```
*API docs will be available at [http://localhost:8000/docs](http://localhost:8000/docs).*

**Start the Streamlit Dashboard:**
```bash
streamlit run dashboard/dashboard3.py --server.port 8501
```
*The dashboard will open automatically in your browser at [http://localhost:8501](http://localhost:8501).*

---

### Option B: Docker Compose (Production Setup)

Spin up both the Dashboard and the API in containers using a single command:
```bash
docker-compose up --build
```
This launches:
- **Streamlit Dashboard** on port `8501`
- **FastAPI Backend** on port `8000`

---

##  Feedback & Self-Learning Cycle

1. **Prediction & Action**: The system recommends actions based on predictions (e.g., maintenance scheduling, discount targeting).
2. **User Feedback**: Through the Streamlit Control Center, users rate or adjust recommendations.
3. **Data Logging**: Feedback and modifications are continuously logged into `feedback_log.csv`.
4. **Automated Retraining**: The ecosystem regularly refits core models based on logged corrections, improving accuracy and adapting to dynamic patterns.
