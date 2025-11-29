from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio
import os

from dotenv import load_dotenv
load_dotenv()

from utils.state import State
from utils.router import planner_router
from utils.draft_report import generate_draft_report
from utils.helper import load_config

# Agents
from agents.planner_agent import planner_agent
from agents.data_agent import data_agent
from agents.insights_agent import insights_agent
from agents.evaluator_agent import evaluator_agent
from agents.cig_agent import cig_agent


import logging
import os
from datetime import datetime

config=load_config()

# Ensure the 'logs' directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')
# Generate a filename based on the current date and time
log_filename = os.path.join('logs', datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log')

# Set up logging to the file with the generated filename
logging.basicConfig(filename=log_filename, 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


async def log_event(event):
    event_type = event.get("event")
    
    if event_type == "on_chain_end":
        node = event.get("metadata", {}).get("langgraph_node")
        if node:
            output = event.get("data", {}).get("output")

            if isinstance(output, dict):
                log_data = {}
                if node == "planner_agent":
                    log_data = output.get("planner")
                elif node == "data_agent":
                    log_data = output.get("data_summary")
                elif node == "insights_agent":
                    log_data = output.get("insights")
                elif node == "evaluator_agent":
                    log_data = output.get("evaluator")
                elif node == "cig_agent":
                    log_data = output.get("cig")
                
                if log_data:
                    logging.info(f"AGENT: {node} | OUTPUT: {log_data}")
            else:
                logging.info(f"AGENT: {node} | OUTPUT: {output}")


async def main():

    graph = StateGraph(State)

    graph.add_node("planner_agent", planner_agent)
    graph.add_node("data_agent", data_agent)
    graph.add_node("insights_agent", insights_agent)
    graph.add_node("evaluator_agent", evaluator_agent)
    graph.add_node("cig_agent", cig_agent)

    graph.set_entry_point("planner_agent")
    graph.add_conditional_edges(
        "planner_agent",
        planner_router,
        {
            "data_agent": "data_agent",
            "insights_agent": "insights_agent",
            "cig_agent": "cig_agent",
            "END": END
        }
    )
    graph.add_edge("data_agent","insights_agent")
    graph.add_edge("insights_agent", "evaluator_agent")
    graph.add_edge("evaluator_agent", "planner_agent")
    graph.add_edge("cig_agent", END)

    print("Enter the query:")
    inp = input()

    initial_state : State = {
        "model": ChatGoogleGenerativeAI(model=config['llm']['model'], google_api_key=os.getenv("GEMINI_API_KEY")),
        "query": inp,
        "planner": {},
        "data_summary": {},
        "insights": {},
        "evaluator": {},
        "cig": {},
        "feedback": {},
    }
    

    graph = graph.compile()
    async for event in graph.astream_events(initial_state, version="v2"):
        await log_event(event)

    print("-> Generating draft report...")
    generate_draft_report(initial_state)

if __name__ == "__main__":
    asyncio.run(main())
