from agents.agent_orchestrator import run_agents

def run_predictions():

    recommendations = run_agents()

    print(recommendations)
