# processor/extract.py

import json
from langchain_core.messages import HumanMessage
from processor.types import State
from processor.llm import llm
from processor.utils import strip_markdown_codeblock


def extract_all_node(state: State) -> State:
    note = state["note"]

    # Extract patient info
    patient_prompt = f"""
    Extract the following patient information from the clinical note:
    - Full name
    - Date of birth (DOB)
    - MRN (Medical Record Number)
    - Email address (if mentioned)
    - Phone number (if mentioned)

    Respond only with valid JSON using these exact keys:
    {{
      "patient_name": "...",
      "date_of_birth": "...",
      "mrn": "...",
      "patient_email": "...",
      "patient_phone": "..."
    }}

    Note:
    {note}
    """.strip()
    patient_result = llm.invoke([HumanMessage(content=patient_prompt)]).content
    try:
        patient_info = json.loads(strip_markdown_codeblock(patient_result))
    except json.JSONDecodeError:
        patient_info = {k: None for k in ["patient_name", "date_of_birth", "mrn", "patient_email", "patient_phone"]}

    # Radiology
    rad_prompt = f"""
    Extract all radiology orders from the following clinical operation note.
    Respond with only valid JSON.
    Note:
    {note}
    """.strip()
    radiology_json = strip_markdown_codeblock(llm.invoke([HumanMessage(content=rad_prompt)]).content)

    # Pathology
    path_prompt = f"""
    Extract all pathology and lab orders from the following clinical operation note.
    Respond with only valid JSON.
    Note:
    {note}
    """.strip()
    pathology_json = strip_markdown_codeblock(llm.invoke([HumanMessage(content=path_prompt)]).content)

    # Medication
    med_prompt = f"""
    Extract all medication prescriptions or slips from the following clinical operation note.
    Respond with only valid JSON.
    Note:
    {note}
    """.strip()
    medication_json = strip_markdown_codeblock(llm.invoke([HumanMessage(content=med_prompt)]).content)

    # Tasks
    task_prompt = f"""
    Extract all patient interaction tasks from the clinical note below.
    These include:
    - phone calls
    - in-clinic appointments
    - SMS reminders
    - coordination tasks

    Respond with a JSON list of task strings. Do not include markdown or commentary.
    Note:
    {note}
    """.strip()
    task_result = llm.invoke([HumanMessage(content=task_prompt)]).content
    try:
        task_list = json.loads(strip_markdown_codeblock(task_result))
    except json.JSONDecodeError:
        task_list = ["⚠️ Could not parse tasks", task_result]

    return {
        **state,
        "radiology": radiology_json,
        "pathology": pathology_json,
        "medication": medication_json,
        "interaction_tasks": task_list,
        **patient_info,
    }
