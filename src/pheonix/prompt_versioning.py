import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from phoenix.client import Client
from phoenix.client.types import PromptVersion
from prompts.planner_agent_prompt import planner
from prompts.data_agent_prompt import extract, summarize
from prompts.insights_agent_prompt import insights
from prompts.evaluator_agent_prompt import retrieve, evaluate
from prompts.cig_agent_prompt import cig
from utils.error_handler import handle_errors

from dotenv import load_dotenv
load_dotenv()


class PheonixPromptObject:
    prompt: str
    prompt_name: str
    prompt_description: str

@handle_errors
def version_prompts(data: PheonixPromptObject):
    Client().prompts.create(
        name=data['prompt_name'],
        prompt_description=data['prompt_description'],
        version=PromptVersion(
            [{"role": "system", "content": data['prompt']}],
            model_name="gemini-2.5-flash",
        ),
    )

@handle_errors
def main(agent):
    if agent == "planner":
        planner_obj: PheonixPromptObject = {
            "prompt": planner,
            "prompt_name": "planner_prompt",
            "prompt_description": "Prompt for planner agent"
        }
        version_prompts(planner_obj)
    elif agent == "extract":
        extract_obj: PheonixPromptObject = {
            "prompt":extract,
            "prompt_name":"extract_prompt",
            "prompt_description":"extract prompt of data agent"
        }
        version_prompts(extract_obj)
    elif agent == "summarize":
        summarize_obj: PheonixPromptObject = {
            "prompt":summarize,
            "prompt_name":"summarize_prompt",
            "prompt_description":"summarize prompt of data agent"
        }
        version_prompts(summarize_obj)
    elif agent == "insights":
        insights_obj: PheonixPromptObject = {
            "prompt":insights,
            "prompt_name":"insights_prompt",
            "prompt_description":"prompt for insights agent"
        }
        version_prompts(insights_obj)
    elif agent == "evaluator":
        evaluator_obj: PheonixPromptObject = {
            "prompt":evaluator,
            "prompt_name":"evaluator_prompt",
            "prompt_description":"prompt for evaluator agent"
        }
        version_prompts(evaluator_obj)
    elif agent == "cig":
        cig_obj: PheonixPromptObject = {
            "prompt":cig,
            "prompt_name":"cig_prompt",
            "prompt_description":"prompt for cig agent"
        }
        version_prompts(cig_obj)

if __name__ == "__main__":
    # main("planner")
    # main("extract")
    # main("summarize")
    # main("insights")
    # main("evaluator")
    # main("cig")

    pass
