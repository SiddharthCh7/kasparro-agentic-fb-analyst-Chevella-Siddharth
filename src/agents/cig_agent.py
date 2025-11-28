import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from prompts.cig_agent_prompt import cig
from utils.parser import parse_json_output
from utils.supabase_client import query_db
from utils.state import State
from utils.error_handler import handle_errors
from utils.helper import append_creative

@handle_errors
async def cig_agent(state: State) -> State:

    print("-> (CIG agent) Invoking CIG model")

    model = state['model']
    campaigns = state['planner']['action']['tool_input']['cig_campaings']
    quoted = ", ".join(f"'{c}'" for c in campaigns)

    SQL = f"""
    SELECT campaign_name, creative_message
    FROM campaigns_data
    WHERE campaign_name IN ({quoted});
    """

    data = query_db(SQL)

    prompt = cig + f"Underperforming campaigns are their creative message: {data}"

    cig_response_raw = model.invoke(prompt)
    cig_response_json = parse_json_output(cig_response_raw.content)
    append_creative(cig_response_json)

    return {
        **state,
        "cig": cig_response_json
    }
