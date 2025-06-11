#pipeline.py

from langgraph.graph import StateGraph, END
from processor.types import State
from processor.extract import extract_all_node
from processor.classify import classify_tasks_node, check_risk_node, human_review_node
from processor.pdf_utils import generate_pdf_node
from processor.emailer import email_pdf_node

def build_pipeline():
    builder = StateGraph(State)

    builder.add_node("extract_all_node", extract_all_node)
    builder.add_node("classify_tasks_node", classify_tasks_node)
    builder.add_node("check_risk_node", check_risk_node)
    builder.add_node("human_review_node", human_review_node)
    builder.add_node("generate_pdf_node", generate_pdf_node)
    builder.add_node("email_pdf_node", email_pdf_node)

    builder.set_entry_point("extract_all_node")
    builder.add_edge("extract_all_node", "classify_tasks_node")
    builder.add_conditional_edges("classify_tasks_node", check_risk_node)
    builder.add_edge("human_review_node", "generate_pdf_node")
    builder.add_edge("check_risk_node", "generate_pdf_node")
    builder.add_edge("generate_pdf_node", "email_pdf_node")
    builder.add_edge("email_pdf_node", END)

    compiled = builder.compile()
    return compiled, builder  # return compiled graph and the builder
