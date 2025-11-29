
import os

from utils.helper import REPORT_SUMMARIES_DIR


from utils.state import State
from utils.parser import parse_json_output
from utils.error_handler import handle_errors

@handle_errors
def generate_draft_report(state: State):

    llm = state['model']
    user_query = state['query']
    insights = state['insights']
    new_creatives = state['cig'] or "None provided"
    related_info = state['data_summary'] or "None provided"
    
    # Construct the prompt for the report content
    prompt_content = """
    You are an expert business analyst assistant. Your goal is to write a concise, easy-to-read report for a business user based on the following information.
    
    USER QUERY: "{user_query}"
    
    INSIGHTS (Accepted/Rejected):
    {insights}
    
    NEW CREATIVES (Optional):
    {new_creatives}
    
    ADDITIONAL CONTEXT:
    {related_info}
    
    INSTRUCTIONS:
    1. Start with a clear Executive Summary answering the user query.
    2. Explain the key insights found, highlighting why they were accepted or rejected and their impact.
    3. If new creatives are provided, briefly describe them and how they align with the insights.
    4. Conclude with recommended next steps.
    5. The output must be a valid JSON object with exactly two keys:
       - "title": A short, descriptive title for the report.
       - "content": The full report text formatted in Markdown.
    
    OUTPUT FORMAT (Strict JSON):
    {{
      "title": "Report Title Here",
      "content": "Executive Summary\n\n..."
    }}
    """

    # Generate the report content
    response = llm.invoke(prompt_content.format(
        user_query=user_query,
        insights=insights,
        new_creatives=new_creatives,
        related_info=related_info
    ))
    report_content = parse_json_output(response.content)

    # Generate a concise filename
    filename = report_content['title'].strip().replace(" ", "_").lower() + ".md"

    # Save the file
    os.makedirs(REPORT_SUMMARIES_DIR, exist_ok=True)
    file_path = os.path.join(REPORT_SUMMARIES_DIR, filename)
    
    with open(file_path, "w") as f:
        f.write(report_content['content'])
        
    print("-> Draft report generated at:", file_path)
