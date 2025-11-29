import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from prompts.planner_agent_prompt import planner
from utils.state import State
from utils.parser import parse_json_output
from utils.error_handler import handle_errors


@handle_errors
async def planner_agent(state: State) -> State:
    model = state['model']

    # Manage Iteration Count
    iteration = state.get('iteration_count', 0)
    if iteration is None:
        iteration = 0
    iteration += 1
    
    try:
        prompt = planner + f"\nUser query: {str(state['query'])}"
        prompt += f"\nCurrent Iteration: {iteration}"
        
        if 'evaluator' in state and state['evaluator']:
            eval_result = state['evaluator']

            # Check if it's a valid evaluation result (has a verdict)
            if eval_result.get('verdict'):
                prompt += f"\nEvaluator returned results.\nEvaluator results: {eval_result}"
            else:
                print("Warning: 'evaluator' in state but no 'verdict' found (or empty).")

        print("-> (Planner Agent)")
        response = model.invoke(prompt)

        json_output = parse_json_output(response.content)

    except Exception as e:
        print(f"Error in planner_agent: {e}")
        raise Exception(e)

    if "cig_campaings" in json_output:
        return {
            **state,
            "planner": {
                "status": "IN_PROGRESS",
                "action": {"tool_name": "cig_agent"}
            },
            "cig": json_output,
            "iteration_count": iteration
        }

    return {
        **state,
        "planner": json_output,
        "iteration_count": iteration
    }