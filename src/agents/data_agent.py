import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from prompts.data_agent_prompt import extract, summarize, fix_query
from utils.state import State
from utils.parser import parse_json_output
from utils.supabase_client import query_db, get_dates
from utils.error_handler import handle_errors

from pprint import pprint
import time

@handle_errors
async def data_agent(state:State) -> State:
    model = state['model']
    
    # First: Extractor
    today = "2025-03-31" # Hardcoding for now (as the data isnt getting updated at all)
    extractor_prompt = extract.format(CURRENT_DATE=today, DATES=get_dates()) + f"Input: {state['query']}"

    print("-> (Data agent) Invoking Extractor")
    extractor_response_raw = model.invoke(extractor_prompt)

    query = extractor_response_raw.content

    # Extract data with retry logic
    print("-> (Data agent) Querying database")
    data = query_db(query)
    for _ in range(2):
        if isinstance(data, str) and data.startswith("ERROR"):
            print("=====Error in syntax, trying again.=====")
            fix_prompt = fix_query + f"query: {query}" + f"error: {data}"
            fix_res = model.invoke(fix_prompt)
            data = query_db(fix_res.content)

    # Second: Summarizer
    inputs = {
        "User Query": state['query'],
        "SQL Query": query,
        "Data": data
    }
    summarizer_prompt = summarize + f"inputs: {inputs}"
    print("-> (Data agent) Invoking Summarizer")
    time.sleep(1)
    summarizer_response_raw = model.invoke(summarizer_prompt)
    summarizer_response_json = parse_json_output(summarizer_response_raw.content)

    return {
        **state,
        "data_summary": summarizer_response_json
    }

