import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from prompts.insights_agent_prompt import insights
from utils.state import State
from utils.parser import parse_json_output
from utils.helper import append_insight
from utils.error_handler import handle_errors


@handle_errors
async def insights_agent(state: State) -> State:
    model = state['model']

    if state['planner']['action']['tool_name'] == 'insights_agent':
        feedback = state['planner']['action']['tool_input']

        inputs = {
            "User Query": state['query'],
            "info": state['evaluator']['original_statement'],
            "feedback_context": feedback
        }
    else:
        inputs = {
            "User Query": state['query'],
            "info": state['data_summary'],
            "feedback_context": ""
        }    

    prompt = insights + f"Inputs: {inputs}"
    
    print("-> (Insights agent) Invoking Insights model")
    insights_response_raw = model.invoke(prompt)

    print("-> (Insights agent) Parsing Insights model output")
    insights_response_json = parse_json_output(insights_response_raw.content)

    append_insight({
        "user_query": state['query'],
        "hypothesis": insights_response_json
    })

    return {

        **state,
        "insights": insights_response_json
    }