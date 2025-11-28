import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.state import State
from utils.parser import parse_json_output

from prompts.evaluator_agent_prompt import retrieve, evaluate
from utils.supabase_client import query_db
from utils.error_handler import handle_errors

from pprint import pprint

@handle_errors
async def evaluator_agent(state: State) -> State:
    model = state['model']
    today = "2025-03-31" # Hardcoding for now (as the data isnt getting updated at all)
    
    # Retriever
    print("-> (Evaluator agent) Generating SQL queries")
    insights = state['insights']
    retriever_prompt = retrieve.format(CURRENT_DATE=today) + str(insights)
    retriever_response_raw = model.invoke(retriever_prompt)
    retriever_response_json = parse_json_output(retriever_response_raw.content)

    # Query database
    print("-> (Evaluator agent) Retrieving data from database")
    try:
        res = query_db(retriever_response_json['sql_query'])
    except:
        res = "Unable to fetch the data."

    # Evaluator
    print("-> (Evaluator agent) Evaluating results")
    evaluator_prompt = evaluate + str(res)
    evaluator_response_raw = model.invoke(evaluator_prompt)
    evaluator_response_json = parse_json_output(evaluator_response_raw.content)

    return {
        **state,
        "evaluator": evaluator_response_json
    }