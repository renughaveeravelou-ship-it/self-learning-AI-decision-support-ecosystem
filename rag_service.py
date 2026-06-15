import os
import pandas as pd
import numpy as np
import glob
try:
    from langchain_community.vectorstores import FAISS
    from langchain_core.documents import Document
    from langchain_community.embeddings import HuggingFaceEmbeddings
    HAS_EMBEDDINGS = True
except ImportError:
    FAISS = None
    HuggingFaceEmbeddings = None

    class Document:
        def __init__(self, page_content, metadata=None):
            self.page_content = page_content
            self.metadata = metadata or {}

    HAS_EMBEDDINGS = False

class RAGService:
    def __init__(self):
        self.vector_store = None
        self.datasets_dir = os.path.dirname(os.path.abspath(__file__))
        
    def build_index(self, recommendations):
        """
        Build FAISS index from generated recommendations and dataset summaries.
        """
        print("Building RAG search index...")
        documents = []
        
        # 1. Add recommendations to index
        for rec in recommendations:
            content = f"Agent: {rec['agent']}\nRecommendation: {rec['recommendation']}\nPriority: {rec['priority']}\nMetrics/Data Point: {rec['data_point']}"
            metadata = {"type": "recommendation", "agent": rec['agent'], "priority": rec['priority']}
            documents.append(Document(page_content=content, metadata=metadata))
            
        # 2. Add dataset summaries to index
        # Let's summarize Sales Data
        sales_path = os.path.join(self.datasets_dir, "Sales Data.csv")
        if os.path.exists(sales_path):
            df_sales = pd.read_csv(sales_path)
            content = f"Sales Dataset Summary: Total Sales Records: {len(df_sales)}. Total Net Profit: {df_sales['profit'].sum():.2f}. Average Order Value: {df_sales['order_value_EUR'].mean():.2f}. Average Cost: {df_sales['cost'].mean():.2f}."
            documents.append(Document(page_content=content, metadata={"type": "data_summary", "dataset": "sales"}))
            
        # Summarize Market Data
        market_path = os.path.join(self.datasets_dir, "market Data.csv")
        if os.path.exists(market_path):
            df_market = pd.read_csv(market_path)
            content = f"Market Dataset Summary: Total Transactions: {len(df_market)}. Average Customer Rating: {df_market['Rating'].mean():.2f}. Most Popular Branch: {df_market['Branch'].mode()[0]}. Average Transaction Total: {df_market['Total'].mean():.2f}."
            documents.append(Document(page_content=content, metadata={"type": "data_summary", "dataset": "market"}))
            
        # Summarize Customer Data
        customer_path = os.path.join(self.datasets_dir, "Customer data.csv")
        if os.path.exists(customer_path):
            df_cust = pd.read_csv(customer_path)
            content = f"Customer Dataset Summary: Total Customers: {len(df_cust)}. Average Age: {df_cust['Age'].mean():.2f}. Average Income: {df_cust['Annual_Income_(k$)'].mean():.2f}. Average Spending Score: {df_cust['Spending_Score'].mean():.2f}."
            documents.append(Document(page_content=content, metadata={"type": "data_summary", "dataset": "customer"}))
            
        # Summarize Social Media Data
        social_path = os.path.join(self.datasets_dir, "Social Medis Data.csv")
        if os.path.exists(social_path):
            df_social = pd.read_csv(social_path)
            content = f"Social Media Dataset Summary: Total Campaigns/Apps tracked: {len(df_social)}. Average Engagement Rate: {df_social['Engagement_Rate'].mean():.2f}. Average Daily Minutes Spent: {df_social['Daily_Minutes_Spent'].mean():.2f}."
            documents.append(Document(page_content=content, metadata={"type": "data_summary", "dataset": "social"}))
            
        # Summarize IoT Data
        iot_path = os.path.join(self.datasets_dir, "IoT data.csv")
        if os.path.exists(iot_path):
            # Take a small summary since it is large
            df_iot = pd.read_csv(iot_path, nrows=10000)
            content = f"IoT Fleet Summary: Total supervised machines: 261,461. Average Operational Hours: {df_iot['Operational_Hours'].mean():.2f}. Average Temperature: {df_iot['Temperature_C'].mean():.2f}°C. Average Vibration: {df_iot['Vibration_mms'].mean():.2f}mm/s. Average Sound Level: {df_iot['Sound_dB'].mean():.2f}dB."
            documents.append(Document(page_content=content, metadata={"type": "data_summary", "dataset": "iot"}))

        if not documents:
            documents.append(Document(page_content="No decision support recommendations or datasets are loaded yet.", metadata={"type": "empty"}))
            
        # Try loading embeddings and building FAISS
        if HAS_EMBEDDINGS:
            try:
                embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
                self.vector_store = FAISS.from_documents(documents, embeddings)
                print("FAISS vector store built successfully.")
                return True
            except Exception as e:
                print(f"Error initializing HuggingFace embeddings: {e}. Falling back to keyword-based search.")
                self.vector_store = documents
                return False
        else:
            self.vector_store = documents
            print("LangChain Embeddings not available. Using keyword-based fallback store.")
            return False

    def query(self, query_text):
        """
        Query the RAG index and return relevant details.
        """
        if not self.vector_store:
            return "The RAG search index is currently empty. Please run predictions or retrain models to build the index."
            
        # If it is a FAISS vector store
        if HAS_EMBEDDINGS and FAISS is not None and isinstance(self.vector_store, FAISS):
            try:
                docs = self.vector_store.similarity_search(query_text, k=3)
                results = [doc.page_content for doc in docs]
                
                # Format response
                response = "### AI Decision Support Assistant\n\nBased on your query, here are the most relevant insights from our ecosystem:\n\n"
                for i, r in enumerate(results, 1):
                    response += f"**Insight {i}:**\n{r}\n\n"
                return response
            except Exception as e:
                return f"Error executing similarity search: {e}"
        else:
            # Keyword matching fallback
            keywords = query_text.lower().split()
            matched_docs = []
            for doc in self.vector_store:
                matches = sum(1 for kw in keywords if kw in doc.page_content.lower())
                if matches > 0:
                    matched_docs.append((matches, doc.page_content))
            
            # Sort by number of matches
            matched_docs.sort(key=lambda x: x[0], reverse=True)
            results = [content for count, content in matched_docs[:3]]
            
            if not results:
                # Return top 2 general documents if no keyword matches
                results = [doc.page_content for doc in self.vector_store[:2]]
                
            response = "### AI Decision Support Assistant (Keyword Fallback)\n\nHere are the closest matches from the decision support ecosystem:\n\n"
            for i, r in enumerate(results, 1):
                response += f"**Insight {i}:**\n{r}\n\n"
            return response
