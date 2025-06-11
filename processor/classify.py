# processor/classify.py

import json
from typing import Literal
from langchain_core.messages import HumanMessage
from processor.types import State
from processor.llm import llm
from processor.utils import strip_markdown_codeblock

def classify_tasks_node(state: State) -> State:
    tasks = state.get("interaction_tasks", [])
    prompt = f"""
    Categorize each of the following patient interaction tasks based on clinical risk.

    Respond with JSON:
    {{
      "low_risk": [...],
      "high_risk": [...]
    }}

    Tasks:
    {json.dumps(tasks, indent=2)}
    """.strip()
    result = llm.invoke([HumanMessage(content=prompt)])
    try:
        classified = json.loads(strip_markdown_codeblock(result.content))
        return {**state, "risk_classification": classified}
    except json.JSONDecodeError:
        return {**state, "risk_classification": {"error": "Invalid JSON", "raw": result.content}}

def check_risk_node(state: State) -> Literal["human_review_node", "generate_pdf_node"]:
    high_risk = state.get("risk_classification", {}).get("high_risk", [])
    return "human_review_node" if high_risk else "generate_pdf_node"

def human_review_node(state: State) -> State:
    prompt = f"""
    You are a human reviewer verifying clinical risk classification.

    Review and re-categorize the following tasks:
    {json.dumps(state['risk_classification'].get('high_risk', []), indent=2)}

    Respond with valid JSON:
    {{
      "low_risk": [...],
      "high_risk": [...]
    }}
    """.strip()
    result = llm.invoke([HumanMessage(content=prompt)])
    try:
        review = json.loads(strip_markdown_codeblock(result.content))
        return {**state, "human_review": review}
    except json.JSONDecodeError:
        return {**state, "human_review": {"error": "Invalid JSON", "raw": result.content}}
