from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict

class State(TypedDict):
    model: Any
    query: str

    planner: Optional[Dict]
    data_summary: Optional[Dict]
    insights: Optional[Dict]
    evaluator: Optional[Dict]
    cig: Optional[Dict]
    iteration_count: Optional[int]