from agents.customer_agent import customer_agent
from agents.sales_agent import sales_agent
from agents.market_agent import market_agent
from agents.maintenance_agent import maintenance_agent

def run_discussion():

    customer = customer_agent()

    sales = sales_agent()

    market = market_agent()

    maintenance = maintenance_agent()

    discussion = {

        "customer":
            customer,

        "sales":
            sales,

        "market":
            market,

        "maintenance":
            maintenance
    }

    return discussion
