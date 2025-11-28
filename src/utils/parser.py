import json
import re

def parse_json_output(raw_output: str):
    """
    Extracts and parses JSON from model output that may contain code fences or extra text.
    Returns a dict if successful, else raises ValueError with context.
    """

    try:
        if not isinstance(raw_output, str):
            raise TypeError("Input must be a string")

        # Step 1: Remove any code fences or formatting artifacts
        cleaned = re.sub(r"^```[\w-]*\s*|```$", "", raw_output.strip(), flags=re.MULTILINE).strip()

        # Step 2: Extract JSON block if embedded within markdown-like text
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if not match:
            raise ValueError("No JSON object found in the input")

        json_str = match.group(0)

        parsed = json.loads(json_str)
        return parsed
    except Exception as e:
        return f"Error while parsing json: {e}"
