# processor/emailer.py

import base64
import os
from processor.types import State
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'nigelnuique@gmail.com')

def send_pdf_email(recipient: str, pdf_path: str, sender: str = SENDER_EMAIL) -> str:
    """
    Sends the specified PDF to the recipient using SendGrid.
    """
    with open(pdf_path, "rb") as f:
        pdf_data = f.read()
        encoded_pdf = base64.b64encode(pdf_data).decode()

    message = Mail(
        from_email=sender,
        to_emails=recipient,
        subject="Your Clinical Task Summary",
        plain_text_content="Please find attached the task summary PDF."
    )

    attachment = Attachment()
    attachment.file_content = FileContent(encoded_pdf)
    attachment.file_type = FileType("application/pdf")
    attachment.file_name = FileName("task_summary.pdf")
    attachment.disposition = Disposition("attachment")
    message.attachment = attachment

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        if response.status_code in [200, 202]:
            return f"✅ PDF emailed to {recipient}"
        else:
            return f"❌ Failed with status code {response.status_code}"
    except Exception as e:
        return f"❌ SendGrid error: {str(e)}"


def email_pdf_node(state: State) -> State:
    """
    LangGraph node wrapper for emailing the PDF using SendGrid.
    """
    recipient = state.get("patient_email") or "nigelnuique@gmail.com"
    pdf_path = "task_summary.pdf"
    email_status = send_pdf_email(recipient, pdf_path)
    return {**state, "email_sent": email_status}
