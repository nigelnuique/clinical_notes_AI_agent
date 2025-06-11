# In processor/pdf_utils.py

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_task_summary_pdf(state: dict, filename: str):
    """
    Creates a summary PDF of extracted tasks and risk classifications.
    """
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y = height - 40

    def write_section(title, items):
        nonlocal y
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, title)
        y -= 20
        c.setFont("Helvetica", 10)
        if not items:
            c.drawString(60, y, "None")
            y -= 15
        else:
            for item in items:
                c.drawString(60, y, f"- {item}")
                y -= 15
        y -= 10

    write_section("📞 Extracted Tasks", state.get("interaction_tasks", []))
    write_section("🤖 AI Risk – Low Risk", state.get("risk_classification", {}).get("low_risk", []))
    write_section("🤖 AI Risk – High Risk", state.get("risk_classification", {}).get("high_risk", []))
    write_section("🧑‍⚕️ Human Review – Low Risk", state.get("human_review", {}).get("low_risk", []))
    write_section("🧑‍⚕️ Human Review – High Risk", state.get("human_review", {}).get("high_risk", []))
    
    c.save()

def generate_pdf_node(state: dict) -> dict:
    filename = "task_summary.pdf"
    generate_task_summary_pdf(state, filename)
    return {**state, "pdf_generated": f"PDF saved to: {filename}"}