def generate_recommendations(agent_outputs):
    recommendations = []
    for agent in agent_outputs:
        if isinstance(agent, dict):
            # First check for 'recommendation' or 'message' keys, then fall back to casting the dict to string
            msg = agent.get("recommendation") or agent.get("message") or str(agent)
        else:
            msg = str(agent)

        # Retain original hardcoded recommendation mappings for compatibility if they trigger
        if "Premium customers declining" in msg:
            recommendations.append("Launch retention campaign")
        elif "Revenue forecast negative" in msg:
            recommendations.append("Increase marketing budget")
        elif "Machine failure risk" in msg:
            recommendations.append("Schedule maintenance")
        else:
            # Otherwise, use the dynamic recommendation directly
            recommendations.append(msg)

    return recommendations