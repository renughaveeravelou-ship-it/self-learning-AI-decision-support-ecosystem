from collaboration.agent_discussion import run_discussion

def executive_summary():

    discussion = run_discussion()

    summary = []

    for key, value in discussion.items():

        summary.append(
            f"{key.upper()} : {value}"
        )

    return "\n".join(summary)
