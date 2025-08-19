current_actions = [
    {
        "timestamp": "2025-08-19T10:02:45",
        "action_type": "user_query",
        "details": "Tell me about Systems Ltd pricing models"
    },
    {
        "timestamp": "2025-08-19T10:02:47",
        "action_type": "llm_reasoning",
        "details": {"reasoning_output": "The query seems to be about pricing models, I should search my tools."}
    },
    {
        "timestamp": "2025-08-19T10:02:50",
        "action_type": "tool_execution",
        "details": {
            "tool": "search_pricing_models",
            "keywords": ["Systems Ltd", "pricing models"],
            "result": "Found 3 relevant pricing models: Fixed bid, Time & Material, Subscription",
        }
    }
]

def actions_to_narrative(actions):
    narrative = [f"For the current query: \"{actions[0]['details']}\":"]
    for act in actions:
        if act["action_type"] == "llm_reasoning":
            narrative.append(f"I thought: {act['details']['reasoning_output']}")
        elif act["action_type"] == "tool_execution":
            d = act["details"]
            input_info = f"keywords {d.get('keywords')}" if "keywords" in d else f"query '{d.get('query')}'"
            narrative.append(f"I used the tool '{d['tool']}' with {input_info}.")
            narrative.append(f"It returned: {d['result']}")
    return "\n".join(narrative)


print(actions_to_narrative(current_actions))