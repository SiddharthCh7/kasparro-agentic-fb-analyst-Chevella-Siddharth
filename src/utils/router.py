

def planner_router(state):
    if "planner" in state and state["planner"]["status"] == "IN_PROGRESS":
        tool = state["planner"]["action"].get("tool_name")
        if tool in ["data_agent", "insights_agent", "evaluator_agent", "cig_agent"]:
            return tool
        return "END"
    return "END"
