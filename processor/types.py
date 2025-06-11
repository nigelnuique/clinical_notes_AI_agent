# types.py

from typing import TypedDict, Optional, List

class RiskAssessment(TypedDict):
    low_risk: List[str]
    high_risk: List[str]

class State(TypedDict):
    note: str
    radiology: Optional[str]
    pathology: Optional[str]
    medication: Optional[str]
    interaction_tasks: Optional[List[str]]
    risk_classification: Optional[RiskAssessment]
    human_review: Optional[RiskAssessment]
    pdf_generated: Optional[str]

    # Patient details
    patient_name: Optional[str]
    date_of_birth: Optional[str]
    mrn: Optional[str]
    patient_email: Optional[str]
    patient_phone: Optional[str]

    # Email status (optional, for UI/debugging)
    email_sent: Optional[str]
