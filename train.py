from models.customer_segmentation import train_customer_model
from models.sales_prediction import train_sales_model
from models.market_analysis import train_market_model
from models.social_analytics import train_social_model
from models.predictive_maintenance import train_maintenance_model

def train_all_models():

    train_customer_model()

    train_sales_model()

    train_market_model()

    train_social_model()

    train_maintenance_model()

    print("Training Completed")
