from agents.customer_agent import customer_agent
from agents.sales_agent import sales_agent
from agents.market_agent import market_agent
from agents.social_agent import social_agent
from agents.maintenance_agent import maintenance_agent

def run_agents():

    recommendations = []

    recommendations.extend(
        customer_agent()
    )

    recommendations.extend(
        sales_agent()
    )

    recommendations.extend(
        market_agent()
    )

    recommendations.extend(
        social_agent()
    )

    recommendations.extend(
        maintenance_agent()
    )

    return recommendations
