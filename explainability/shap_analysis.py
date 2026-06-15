import streamlit as st

try:
    import shap
    import joblib
    import matplotlib.pyplot as plt
except ImportError:
    shap = None
    joblib = None
    plt = None
import numpy as np

def explain_model(model_path, X):
    if shap is None or joblib is None or plt is None:
        st.warning("SHAP dependencies are not installed in this environment.")
        return
    try:
        model = joblib.load(model_path)
        
        # Check model type to use appropriate explainer
        model_name = type(model).__name__
        if "KMeans" in model_name:
            # KMeans is not a tree or supervised model, explain centroids instead
            st.info(f"Explaining K-Means model. Cluster Centroids: \n{model.cluster_centers_}")
            return

        # Attempt to create an explainer
        try:
            # TreeExplainer for Tree-based models (XGBoost, RandomForest)
            if "XGB" in model_name or "Forest" in model_name or "Tree" in model_name:
                explainer = shap.TreeExplainer(model)
                shap_values = explainer.shap_values(X)
            else:
                explainer = shap.Explainer(model, X)
                shap_values = explainer(X)
        except Exception:
            # Fallback to KernelExplainer
            explainer = shap.KernelExplainer(model.predict, shap.sample(X, 10))
            shap_values = explainer.shap_values(X)

        fig = plt.figure(figsize=(10, 5))
        shap.summary_plot(shap_values, X, show=False)
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        st.error(f"Error generating SHAP explanation: {e}")
